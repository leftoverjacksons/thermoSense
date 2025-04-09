// serial_handler.cpp

#include "serial_handler.h"

void initializeSerial() {
    delay(500);
    Serial.begin(115200);
    delay(1000);
    
    int timeout = 0;
    while (!Serial && timeout < 100) {
        delay(100);
        timeout++;
    }
    
    Serial.flush();
    Serial.println("ESP32 Starting...");
    delay(100);
    Serial.println("Setup Complete");
    Serial.println("Format: DATA:voltage:pressure:temperature");
}

bool checkSerialConnection() {
    if (!Serial) {
        delay(100);
        Serial.end();
        delay(100);
        Serial.begin(115200);
        delay(100);
        return false;
    }
    return true;
}

// serial_handler.cpp - Update the sendSensorData function
void sendSensorData(float voltage, float pressure, float temperature, float ph, int heaterState) {
    Serial.print("DATA:");
    Serial.print(voltage, 3);
    Serial.print(":");
    Serial.print(pressure, 2);
    Serial.print(":");
    Serial.print(temperature, 2);
    Serial.print(":");
    Serial.print(ph, 2);
    Serial.print(":");
    
    // Include heater state
    Serial.println(heaterState);
}