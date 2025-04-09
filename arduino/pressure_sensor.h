// pressure_sensor.h

#ifndef PRESSURE_SENSOR_H
#define PRESSURE_SENSOR_H

#include <Arduino.h>
#include "constants.h"  // Add this include

// PX3 Transducer Constants
extern const float V_MIN;
extern const float V_MAX;
extern const float P_MAX;

float readPressureSensor();
float convertToPressure(float voltage);

#endif