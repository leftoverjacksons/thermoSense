// pid_controller.h
#ifndef PID_CONTROLLER_H
#define PID_CONTROLLER_H

class PIDController {
private:
    float kp, ki, kd;
    float setpoint;
    float lastError;
    float integral;
    float lastOutput;
    unsigned long lastTime;
    float minOutput;
    float maxOutput;
    float maxRate;        // Maximum change per second
    float integralLimit;  // Anti-windup limit
    
public:
    PIDController(float p, float i, float d, float min, float max) 
        : kp(p), ki(i), kd(d), setpoint(0), lastError(0), integral(0), 
          lastOutput(0), lastTime(0), minOutput(min), maxOutput(max),
          maxRate(50.0f), integralLimit(30.0f) {}
    
    void setSetpoint(float sp) {
        if (sp != setpoint) {
            integral = 0;  // Reset integral term on setpoint change
            lastError = 0;
            lastTime = 0;  // Force derivative term to reset
        }
        setpoint = sp;
    }
    
    float compute(float input) {
        unsigned long now = millis();
        float deltaTime = (now - lastTime) / 1000.0f; // Convert to seconds
        
        // On first call, initialize and return minimum output
        if (lastTime == 0) {
            lastTime = now;
            lastOutput = minOutput;
            return minOutput;
        }
        
        float error = setpoint - input;
        
        // Proportional term
        float P = kp * error;
        
        // Integral term with anti-windup
        integral += error * deltaTime;
        // Limit integral term
        if (integral > integralLimit) integral = integralLimit;
        if (integral < -integralLimit) integral = -integralLimit;
        float I = ki * integral;
        
        // Derivative term on measurement (not error) for smoother response
        float dInput = deltaTime > 0 ? (input - lastError) / deltaTime : 0;
        float D = -kd * dInput;  // Negative because we want derivative of measurement
        
        // Calculate output
        float output = P + I + D;
        
        // Rate limiting
        float rate = (output - lastOutput) / deltaTime;
        if (rate > maxRate) {
            output = lastOutput + maxRate * deltaTime;
        } else if (rate < -maxRate) {
            output = lastOutput - maxRate * deltaTime;
        }
        
        // Clamp output to limits
        if (output > maxOutput) {
            output = maxOutput;
            // Anti-windup - only integrate error if not saturated
            integral -= error * deltaTime;
        }
        if (output < minOutput) {
            output = minOutput;
            // Anti-windup - only integrate error if not saturated
            integral -= error * deltaTime;
        }
        
        // Store values for next iteration
        lastError = input;  // Store input for derivative term
        lastOutput = output;
        lastTime = now;
        
        return output;
    }
    
    void setMaxRate(float rate) {
        maxRate = rate > 0 ? rate : 50.0f;
    }
    
    void setIntegralLimit(float limit) {
        integralLimit = limit > 0 ? limit : 30.0f;
    }
    
    float getSetpoint() {
        return setpoint;
    }
    
    void reset() {
        integral = 0;
        lastError = 0;
        lastTime = 0;
        lastOutput = minOutput;
    }
};

#endif