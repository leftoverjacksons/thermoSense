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
            self.temperature_data = deque(maxlen=window_size)
            self.ph_data = deque(maxlen=window_size)  # Add this line
            self.heater_states = deque(maxlen=window_size)
            self.timestamps = deque(maxlen=window_size)
            self.window_size = window_size
            self.ser = None
            self.max_voltage = 5.0
            self.max_pressure = 0.0
            self.max_temperature = 0.0
            self.min_temperature = 100.0
            self.max_ph = 14.0  # Add this line
            self.min_ph = 0.0   # Add this line
            self.connection_attempts = 0
            self.last_connection_time = 0
            self.connect_serial()
            self.initialized = True
            print("Initialization complete")

    def connect_serial(self):
        """Attempt to connect to the serial port with enhanced error handling."""
        current_time = time.time()
        
        if current_time - self.last_connection_time < 5:
            print("Too soon to retry connection. Waiting...")
            return
                
        self.connection_attempts += 1
        print(f"\nAttempting to connect (Attempt {self.connection_attempts})...")
        
        if self.ser is not None:
            try:
                print("Closing existing serial connection...")
                self.ser.close()
                time.sleep(1)
            except Exception as e:
                print(f"Warning while closing serial port: {e}")
        
        try:
            print(f"Opening serial port {SERIAL_CONFIG['port']}...")
            self.ser = serial.Serial()
            self.ser.port = SERIAL_CONFIG['port']
            self.ser.baudrate = SERIAL_CONFIG['baudrate']
            self.ser.timeout = SERIAL_CONFIG['timeout']
            self.ser.writeTimeout = SERIAL_CONFIG['write_timeout']
            
            # Add these lines to prevent bootloader mode
            self.ser.dtr = False
            self.ser.rts = False
            
            self.ser.open()
            time.sleep(0.5)
            
            # Toggle DTR to reset ESP32 properly
            self.ser.dtr = True
            time.sleep(0.5)
            self.ser.dtr = False
            time.sleep(0.5)
            
            print(f"Successfully connected to {self.ser.name}")
            print(f"Port settings: {self.ser.get_settings()}")
            
            # Clear any bootloader messages
            time.sleep(1)
            if self.ser.in_waiting:
                self.ser.reset_input_buffer()
            
            self.last_connection_time = current_time
            self.connection_attempts = 0
            
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            print("Common causes:")
            print(" - Port is in use by another program")
            print(" - Incorrect port name")
            print(" - Device not connected")
            self.ser = None

    def read_serial(self):
        """Read from serial port with enhanced debugging."""
        if not self.ser:
            print("No serial connection established")
            self.connect_serial()
            return
            
        if not self.ser.is_open:
            print("Serial port not open")
            self.connect_serial()
            return
            
        if not self.ser.in_waiting:
            print("No data waiting in buffer")
            return
            
        try:
            data = self.ser.read(self.ser.in_waiting).decode('ascii')
            print(f"\nReceived {len(data)} bytes of raw data:")
            print("Raw data:", data.replace('\n', '\\n'))
            
            for line in data.split('\n'):
                if not line.strip():
                    continue
                    
                if "DATA:" in line:
                    print("\nProcessing line:", line)
                    try:
                        parts = line.strip().split(':')
                        print(f"Split parts: {parts}")
                        
                        if len(parts) >= 6:  # Expecting 6 parts with pH and heater state
                            try:
                                _, voltage_str, pressure_str, temp_str, ph_str, heater_state = parts[:6]
                                print(f"Parsing - Voltage: {voltage_str}, Pressure: {pressure_str}, "
                                    f"Temp: {temp_str}, pH: {ph_str}, Heater: {heater_state}")
                                
                                voltage = float(voltage_str)
                                pressure = float(pressure_str)
                                temperature = float(temp_str)
                                ph = float(ph_str)
                                heater_state = int(heater_state)
                                
                                self.max_voltage = max(self.max_voltage, voltage)
                                self.max_pressure = max(self.max_pressure, pressure)
                                self.max_temperature = max(self.max_temperature, temperature)
                                self.min_temperature = min(self.min_temperature, temperature)
                                self.max_ph = max(self.max_ph, ph)
                                self.min_ph = min(self.min_ph, ph)
                                
                                self.voltage_data.append(voltage)
                                self.pressure_data.append(pressure)
                                self.temperature_data.append(temperature)
                                self.ph_data.append(ph)
                                self.heater_states.append(heater_state)
                                self.timestamps.append(time.time())
                                print(f"Successfully added data point - V:{voltage:.3f}, "
                                    f"P:{pressure:.2f}, T:{temperature:.2f}, pH:{ph:.2f}, H:{heater_state}")
                            except ValueError as e:
                                print(f"Error parsing values: {e}")
                            
                        else:
                            print(f"Warning: Unexpected number of parts in data line ({len(parts)})")
                            
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing line '{line}': {e}")
                else:
                    print(f"Ignoring non-data line: {line}")
                    
        except Exception as e:
            print(f"\nError reading serial: {str(e)}")
            print("Attempting to reconnect...")
            self.connect_serial()

    def cleanup(self):
        """Clean up serial connection on shutdown."""
        if self.ser:
            try:
                print("\nClosing serial connection...")
                if self.ser.is_open:
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                    time.sleep(0.1)
                    self.ser.close()
                    print("Serial connection closed properly")
            except Exception as e:
                print(f"Error during cleanup: {e}")
        else:
            print("No serial connection to clean up")