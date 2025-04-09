// thermistor.cpp
#include "thermistor.h"
#include "pins.h"

const float THERMISTOR_R25 = 10000.0f;
const float THERMISTOR_BETA = 3950.0f;
const float SERIES_R = 10000.0f;
const float KELVIN_OFFSET = 273.15f;

float Thermistor::rawToTemp(float adcValue) {
    float voltage = (adcValue * V_SUPPLY) / 4096.0f;
    
    // Bound voltage
    if (voltage <= 0.0f) voltage = 0.001f;
    if (voltage > V_SUPPLY) voltage = V_SUPPLY;
    
    float thermistor_r = SERIES_R * ((V_SUPPLY / voltage) - 1);
    if (thermistor_r <= 0.0f) thermistor_r = 0.001f;
    
    float steinhart = log(thermistor_r / THERMISTOR_R25) / THERMISTOR_BETA;
    steinhart += 1.0f / (25.0f + KELVIN_OFFSET);
    float temp_c = (1.0f / steinhart) - KELVIN_OFFSET;
    
    // Bound temperature
    if (temp_c < -40.0f) temp_c = -40.0f;
    if (temp_c > 125.0f) temp_c = 125.0f;
    
    return temp_c;
}

float Thermistor::readTemperature() {
    const int NUM_SAMPLES = 10;
    float sum = 0;
    
    // Take multiple ADC samples
    for (int i = 0; i < NUM_SAMPLES; i++) {
        sum += analogRead(pin);
        delayMicroseconds(100);
    }
    
    // Calculate average ADC value
    float avgADC = sum / NUM_SAMPLES;
    
    // Convert to temperature
    float currentTemp = rawToTemp(avgADC);
    
    // Apply exponential smoothing
    if (firstReading) {
        lastValue = currentTemp;
        firstReading = false;
        return currentTemp;
    }
    
    // Exponential smoothing formula: output = α × input + (1 - α) × lastOutput
    float smoothedTemp = alpha * currentTemp + (1 - alpha) * lastValue;
    lastValue = smoothedTemp;
    
    return smoothedTemp;
}

void Thermistor::setSmoothing(float newAlpha) {
    if (newAlpha >= 0.0f && newAlpha <= 1.0f) {
        alpha = newAlpha;
    }
}