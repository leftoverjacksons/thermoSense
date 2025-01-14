import serial
import time
from collections import deque
from config import SERIAL_CONFIG

class PressureMonitor:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, window_size=100):
        if not hasattr(self, 'initialized'):
            print("Starting initialization...")
            self.voltage_data = deque(maxlen=window_size)
            self.pressure_data = deque(maxlen=window_size)
            self.timestamps = deque(maxlen=window_size)
            self.window_size = window_size
            self.ser = None
            self.max_voltage = 5.0
            self.max_pressure = 0.0
            self.connect_serial()
            self.initialized = True
            print("Initialization complete")

    def connect_serial(self):
        if self.ser is None or not self.ser.is_open:
            try:
                self.ser = serial.Serial()
                self.ser.port = SERIAL_CONFIG['port']
                self.ser.baudrate = SERIAL_CONFIG['baudrate']
                self.ser.timeout = SERIAL_CONFIG['timeout']
                self.ser.writeTimeout = SERIAL_CONFIG['write_timeout']
                self.ser.open()
                
                print(f"Connected to {self.ser.name}")
                print(f"Port settings: {self.ser.get_settings()}")
                
                time.sleep(2)
                self.ser.reset_input_buffer()
                
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")
                self.ser = None

    def read_serial(self):
        if self.ser and self.ser.is_open and self.ser.in_waiting:
            try:
                data = self.ser.read(self.ser.in_waiting).decode('ascii')
                for line in data.split('\n'):
                    if "DATA:" in line:
                        try:
                            _, voltage_str, pressure_str = line.strip().split(':')
                            voltage = float(voltage_str)
                            pressure = float(pressure_str)
                            
                            self.max_voltage = max(self.max_voltage, voltage)
                            self.max_pressure = max(self.max_pressure, pressure)
                            
                            self.voltage_data.append(voltage)
                            self.pressure_data.append(pressure)
                            self.timestamps.append(time.time())
                            
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing line '{line}': {e}")
            except Exception as e:
                print(f"Error reading serial: {e}")
                self.connect_serial()

    def cleanup(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed")