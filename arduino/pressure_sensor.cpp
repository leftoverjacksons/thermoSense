// pressure_sensor.cpp
#include "pressure_sensor.h"
#include "pins.h"

// Remove V_SUPPLY from here since it's now in constants.cpp
const float V_MIN = 0.5f;
const float V_MAX = 4.5f;
const float P_MAX = 100.0f;

float readPressureSensor() {
    const int NUM_SAMPLES = 10;
    long pressure_sum = 0;
    
    for(int i = 0; i < NUM_SAMPLES; i++) {
        pressure_sum += analogRead(PRESSURE_PIN);
        delayMicroseconds(100);
    }
    
    float rawValue = static_cast<float>(pressure_sum) / NUM_SAMPLES;
    float voltage = (rawValue * V_SUPPLY) / 4096.0f;  // V_SUPPLY comes from constants.h
    
    // Add bounds checking for voltage
    if (voltage < V_MIN) voltage = V_MIN;
    if (voltage > V_MAX) voltage = V_MAX;
    
    return voltage;
}

float convertToPressure(float voltage) {
    float pressure = (((voltage - V_MIN) * P_MAX) / (V_MAX - V_MIN)) * 10.0f;
    
    // Bound pressure
    if (pressure < 0.0f) pressure = 0.0f;
    if (pressure > P_MAX * 10.0f) pressure = P_MAX * 10.0f;
    
    return pressure;
}