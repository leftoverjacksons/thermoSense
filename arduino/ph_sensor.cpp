// ph_sensor.cpp
#include "ph_sensor.h"

float PHSensor::readPH() {
    // Add new reading to array
    pHArray[pHArrayIndex++] = analogRead(pin);
    if (pHArrayIndex == arrayLength) pHArrayIndex = 0;
    
    // Calculate voltage from averaged readings
    float voltage = averageArray(pHArray, arrayLength) * V_SUPPLY / 4096.0f;
    
    // Convert voltage to pH value
    // The formula 3.5*voltage is based on your sample code
    // You may need to adjust this based on your specific pH probe calibration
    float currentPH = 3.5f * voltage + offset;
    
    // Bound pH value to realistic range
    if (currentPH < 0.0f) currentPH = 0.0f;
    if (currentPH > 14.0f) currentPH = 14.0f;
    
    // Apply exponential smoothing
    if (firstReading) {
        lastValue = currentPH;
        firstReading = false;
        return currentPH;
    }
    
    // Exponential smoothing formula
    float smoothedPH = alpha * currentPH + (1 - alpha) * lastValue;
    lastValue = smoothedPH;
    
    return smoothedPH;
}

float PHSensor::averageArray(int* arr, int number) {
    if (number <= 0) return 0;
    
    if (number < 5) {
        // For small arrays, simple average
        long amount = 0;
        for (int i = 0; i < number; i++) {
            amount += arr[i];
        }
        return (float)amount / number;
    } else {
        // For larger arrays, discard min and max values
        int min, max;
        long amount = 0;
        
        if (arr[0] < arr[1]) {
            min = arr[0]; max = arr[1];
        } else {
            min = arr[1]; max = arr[0];
        }
        
        for (int i = 2; i < number; i++) {
            if (arr[i] < min) {
                amount += min;
                min = arr[i];
            } else if (arr[i] > max) {
                amount += max;
                max = arr[i];
            } else {
                amount += arr[i];
            }
        }
        
        return (float)amount / (number - 2);
    }
}

void PHSensor::setSmoothing(float newAlpha) {
    if (newAlpha >= 0.0f && newAlpha <= 1.0f) {
        alpha = newAlpha;
    }
}

void PHSensor::setOffset(float newOffset) {
    offset = newOffset;
}