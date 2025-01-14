import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime
import time

class PressureMonitor:
    def __init__(self):
        print("Starting initialization...")
        self.voltage_data = np.array([])
        self.pressure_data = np.array([])
        self.connect_serial()
        self.setup_plot()
        print("Initialization complete")

    def connect_serial(self):
        try:
            # Open serial port with explicit settings
            self.ser = serial.Serial()
            self.ser.port = 'COM4'
            self.ser.baudrate = 115200
            self.ser.timeout = 0.1
            self.ser.writeTimeout = 0.1
            self.ser.open()
            
            print(f"Connected to {self.ser.name}")
            print(f"Port settings: {self.ser.get_settings()}")
            
            time.sleep(2)  # Wait for connection to establish
            self.ser.reset_input_buffer()
            
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            raise

    def setup_plot(self):
        plt.style.use('dark_background')
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Voltage plot
        self.line_v, = self.ax1.plot([], [], 'b-', linewidth=2)
        self.ax1.set_xlim(0, 100)
        self.ax1.set_ylim(0, 5)
        self.ax1.set_xlabel('Samples')
        self.ax1.set_ylabel('Voltage (V)')
        self.ax1.set_title('Raw Voltage Reading')
        self.ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Pressure plot
        self.line_p, = self.ax2.plot([], [], 'r-', linewidth=2)
        self.ax2.set_xlim(0, 100)
        self.ax2.set_ylim(0, 100)
        self.ax2.set_xlabel('Samples')
        self.ax2.set_ylabel('Pressure (PSI)')
        self.ax2.set_title('Calculated Pressure')
        self.ax2.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()

    def update_plot(self, frame):
        if self.ser.is_open:
            bytes_waiting = self.ser.in_waiting
            if bytes_waiting > 0:
                data = self.ser.read(bytes_waiting)
                text = data.decode('ascii')
                
                # Process each complete line
                for line in text.split('\n'):
                    if "DATA:" in line:
                        try:
                            _, voltage_str, pressure_str = line.strip().split(':')
                            voltage = float(voltage_str)
                            pressure = float(pressure_str)
                            
                            # Update voltage data
                            self.voltage_data = np.append(self.voltage_data, voltage)
                            if len(self.voltage_data) > 100:
                                self.voltage_data = self.voltage_data[-100:]
                            
                            # Update pressure data
                            self.pressure_data = np.append(self.pressure_data, pressure)
                            if len(self.pressure_data) > 100:
                                self.pressure_data = self.pressure_data[-100:]
                                
                            # Update line data
                            x_data = np.arange(len(self.voltage_data))
                            self.line_v.set_data(x_data, self.voltage_data)
                            self.line_p.set_data(x_data, self.pressure_data)
                            
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing line '{line}': {e}")
        
        return self.line_v, self.line_p

    def run(self):
        print("Starting animation")
        self.ani = FuncAnimation(
            self.fig, 
            self.update_plot,
            interval=50,
            blit=True,
            cache_frame_data=False
        )
        plt.show()

    def cleanup(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed")

if __name__ == "__main__":
    print("Starting Pressure Monitor...")
    
    monitor = PressureMonitor()
    
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        monitor.cleanup()