// heater_control.h
#ifndef HEATER_CONTROL_H
#define HEATER_CONTROL_H

#include "pid_controller.h"

class HeaterControl {
public:
    enum State {
        HEATING,
        COOLING,
        STABILIZING
    };
    
private:
    PIDController pid;
    State currentState;
    int heaterPin;
    float highTemp;
    float lowTemp;
    float stabilizationTime;  // Time to maintain temperature before switching
    unsigned long stateStartTime;
    float stabilizationThreshold;  // How close to target temp before starting stabilization timer
    
public:
    HeaterControl(int pin, float kp, float ki, float kd)
        : pid(kp, ki, kd, 0, 255),  // PWM range is 0-255
          currentState(HEATING),
          heaterPin(pin),
          highTemp(60.0f),
          lowTemp(25.0f),
          stabilizationTime(10000),  // 10 seconds default
          stateStartTime(0),
          stabilizationThreshold(2.0f)  // Within 2°C of target
    {
        pinMode(heaterPin, OUTPUT);
        analogWrite(heaterPin, 0);
    }
    
    void update(float currentTemp) {
        float targetTemp;
        unsigned long currentTime = millis();
        
        switch (currentState) {
            case HEATING:
                targetTemp = highTemp;
                pid.setSetpoint(targetTemp);
                if (abs(currentTemp - targetTemp) <= stabilizationThreshold) {
                    currentState = STABILIZING;
                    stateStartTime = currentTime;
                }
                break;
                
            case COOLING:
                targetTemp = lowTemp;
                pid.setSetpoint(targetTemp);
                if (abs(currentTemp - targetTemp) <= stabilizationThreshold) {
                    currentState = STABILIZING;
                    stateStartTime = currentTime;
                }
                break;
                
            case STABILIZING:
                if (currentTime - stateStartTime >= stabilizationTime) {
                    // Switch between heating and cooling
                    currentState = (pid.getSetpoint() == highTemp) ? COOLING : HEATING;
                    pid.reset();  // Reset PID when changing direction
                }
                break;
        }
        
        // Calculate and apply PWM output
        float output = pid.compute(currentTemp);
        
        // If we're cooling, turn off the heater
        if (currentState == COOLING) {
            output = 0;
        }
        
        analogWrite(heaterPin, (int)output);
    }
    
    State getState() const {
        return currentState;
    }
    
    void setTemperatures(float low, float high) {
        lowTemp = low;
        highTemp = high;
    }
    
    void setStabilizationTime(float seconds) {
        stabilizationTime = seconds * 1000;  // Convert to milliseconds
    }
    
    void setStabilizationThreshold(float threshold) {
        stabilizationThreshold = threshold;
    }

    // Add the new methods to pass through to PID controller
    void setMaxRate(float rate) {
        pid.setMaxRate(rate);
    }
    
    void setIntegralLimit(float limit) {
        pid.setIntegralLimit(limit);
    }
};

#endif