// ph_sensor.h
#ifndef PH_SENSOR_H
#define PH_SENSOR_H

#include <Arduino.h>
#include "constants.h"

class PHSensor {
private:
    const int pin;
    const int arrayLength = 40;
    int pHArray[40];
    int pHArrayIndex = 0;
    float offset;
    float lastValue;
    bool firstReading;
    float alpha;
    
    // Helper function for averaging readings
    float averageArray(int* arr, int number);
    
public:
    PHSensor(int pin_number, float calib_offset = 0.00)
        : pin(pin_number),
          offset(calib_offset),
          lastValue(7.0),
          firstReading(true),
          alpha(0.1f) {
        // Initialize pH array
        for (int i = 0; i < arrayLength; i++) {
            pHArray[i] = 0;
        }
    }
    
    float readPH();
    void setSmoothing(float newAlpha);
    void setOffset(float newOffset);
};

#endif // PH_SENSOR_H