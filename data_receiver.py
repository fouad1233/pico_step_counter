import serial
import time

# Serial port configuration
serial_port = '/dev/cu.usbmodem12301'  # Change this to the appropriate port
baud_rate = 9600

# File path
file_path = 'esra_cevrede_yuruyor.txt'  # Change this path as needed

try:
    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    # Open the file in write mode
    with open(file_path, 'w') as file:
        while True:
            # Read data from serial port
            data = ser.readline().decode().strip()  # Decode bytes to string and strip newline characters
            print(data)
            if data:
                # Write data to the file
                file.write(data + '\n')
                file.flush()  # Ensure data is written immediately

            time.sleep(0.005)  # Adjust sleep time as needed
except Exception as e:
    print("Error:", e)
finally:
    # Close the serial port
    ser.close()
