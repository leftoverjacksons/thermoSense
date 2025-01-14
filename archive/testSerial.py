import serial
import time

def test_serial():
    try:
        # Open serial port
        ser = serial.Serial()
        ser.port = 'COM4'
        ser.baudrate = 115200
        ser.timeout = 0.1
        ser.writeTimeout = 0.1
        ser.open()
        
        print(f"Opened {ser.name}")
        print(f"Settings: {ser.get_settings()}")
        
        # Give the serial connection time to establish
        time.sleep(2)
        print("Serial port ready")
        
        # Clear any existing data
        ser.reset_input_buffer()
        print("Buffer cleared")
        
        # Read for 10 seconds
        start_time = time.time()
        count = 0
        
        while (time.time() - start_time) < 10:
            try:
                # Alternative reading method
                if ser.is_open:
                    bytes_waiting = ser.in_waiting
                    if bytes_waiting > 0:
                        print(f"Bytes waiting: {bytes_waiting}")
                        data = ser.read(bytes_waiting)
                        text = data.decode('ascii')
                        print(f"Received: {text}")
                        count += 1
            except Exception as e:
                print(f"Error during read: {type(e).__name__} - {str(e)}")
            
            time.sleep(0.01)
            
    except Exception as e:
        print(f"Error: {type(e).__name__} - {str(e)}")
    finally:
        if 'ser' in locals():
            if ser.is_open:
                ser.close()
                print("\nSerial port closed")
            print(f"Total reads with data: {count}")

if __name__ == "__main__":
    print("Starting Serial Test...")
    print(f"Python version: {serial.VERSION}")
    print("Opening serial port...")
    test_serial()