// pins.h

#ifndef PINS_H
#define PINS_H

#include <Arduino.h>

// Pin definitions
extern const int NUM_PINS;
extern const int PINS[];
extern const int PRESSURE_PIN;
extern const int THERMISTOR_PIN;
extern const int PH_SENSOR_PIN;

// Pin initialization
void initializePins();
void initializeADC();

#endif