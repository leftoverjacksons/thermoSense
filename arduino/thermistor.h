// thermistor.h
#ifndef THERMISTOR_H
#define THERMISTOR_H

#include <Arduino.h>
#include "constants.h"
#include "moving_average.h"

// Forward declarations
class MovingAverageFilter;

extern const float THERMISTOR_R25;
extern const float THERMISTOR_BETA;
extern const float SERIES_R;
extern const float KELVIN_OFFSET;

class Thermistor {
private:
    float rawToTemp(float adcValue);
    const int pin;
    float alpha;
    float lastValue;
    bool firstReading;
    
public:
    Thermistor(int pin_number) : 
        pin(pin_number),
        alpha(0.1f),  // Smoothing factor (0.1 = more smoothing)
        lastValue(0),
        firstReading(true) {}
    
    float readTemperature();
    void setSmoothing(float newAlpha);
};

#endif // THERMISTOR_H