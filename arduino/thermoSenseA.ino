// thermoSenseA.ino

#include "pins.h"
#include "pressure_sensor.h"
#include "thermistor.h"
#include "serial_handler.h"
#include "heater_control.h"
#include "ph_sensor.h"

// Create thermistor instance
Thermistor thermistor(THERMISTOR_PIN);

// Create a global pH sensor instance
PHSensor phSensor(PH_SENSOR_PIN, 0.00); // Use your calibration offset if needed

// More balanced PID values:
// - Moderate Kp for reasonable response
// - Much lower Ki to prevent integral windup
// - Higher Kd to brake earlier
HeaterControl heater(15, 12.0f, 0.1f, 6.0f);

void setup() {
    initializePins();
    initializeADC();
    initializeSerial();
    
    // More smoothing to reduce oscillations
    thermistor.setSmoothing(0.1f);
    
    // Configure heater parameters
    heater.setTemperatures(80.0f, 100.0f);
    heater.setStabilizationTime(20.0f);  // Longer stabilization time
    heater.setStabilizationThreshold(2.0f);  // Wider threshold to prevent oscillation
    
    // More conservative limits
    heater.setMaxRate(40.0f);     // Slower changes
    heater.setIntegralLimit(30.0f);  // Less integral accumulation
}

void loop() {
    static unsigned long lastReadTime = 0;
    const unsigned long READ_INTERVAL = 100;
    
    if (millis() - lastReadTime < READ_INTERVAL) {
        delay(1);
        return;
    }
    
    if (!checkSerialConnection()) {
        return;
    }
    
    float voltage = readPressureSensor();
    float pressure = convertToPressure(voltage);
    float temperature = thermistor.readTemperature();
    float pH = phSensor.readPH();
    
    heater.update(temperature);
    
    // Use updated sendSensorData function
    int currentHeaterState = heater.getState();
    sendSensorData(voltage, pressure, temperature, pH, currentHeaterState);
    
    lastReadTime = millis();
}