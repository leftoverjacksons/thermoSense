// serial_handler.h

#ifndef SERIAL_HANDLER_H
#define SERIAL_HANDLER_H

#include <Arduino.h>

void initializeSerial();
bool checkSerialConnection();
void sendSensorData(float voltage, float pressure, float temperature, float ph, int heaterState);

#endif