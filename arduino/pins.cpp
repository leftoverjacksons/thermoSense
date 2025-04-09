// pins.cpp

#include "pins.h"

const int NUM_PINS = 5;
const int PINS[NUM_PINS] = {15, 2, 0, 4, 16};  // MOSFETs
const int PRESSURE_PIN = 26;  // Pressure transducer input
const int THERMISTOR_PIN = 36;  // Thermistor input
const int PH_SENSOR_PIN = 12; // As per your requirements, pH meter on GPIO12

void initializePins() {
    for(int i = 0; i < NUM_PINS; i++) {
        pinMode(PINS[i], OUTPUT);
        digitalWrite(PINS[i], LOW);
    }
}

void initializeADC() {
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db);  // Full-scale voltage range
}