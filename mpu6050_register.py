import machine
import utime

# MPU6050 I2C address
MPU6050_ADDR = 0x68

# Register addresses
MPU6050_REG_PWR_MGMT_1 = 0x6B
MPU6050_REG_SMPLRT_DIV = 0x19
MPU6050_REG_ACCEL_CONFIG = 0x1C
MPU6050_REG_GYRO_CONFIG = 0x1B
MPU6050_REG_ACCEL_XOUT_H = 0x3B
MPU6050_REG_TEMP_OUT_H = 0x41
MPU6050_REG_GYRO_XOUT_H = 0x43

# Configure I2C
i2c = machine.I2C(0,freq=400000, sda=machine.Pin(0), scl=machine.Pin(1))

# Initialize MPU6050
i2c.writeto_mem(MPU6050_ADDR, MPU6050_REG_PWR_MGMT_1, b'\x00')  # Wake up MPU6050
i2c.writeto_mem(MPU6050_ADDR, MPU6050_REG_SMPLRT_DIV, b'\x00')  # Sample rate divider (1kHz)
i2c.writeto_mem(MPU6050_ADDR, MPU6050_REG_ACCEL_CONFIG, b'\x00')  # Accelerometer scale (+/- 2g)
i2c.writeto_mem(MPU6050_ADDR, MPU6050_REG_GYRO_CONFIG, b'\x00')  # Gyroscope scale (+/- 250deg/s)

# Function to read sensor data
def read_sensor_data():
    data = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_REG_ACCEL_XOUT_H, 14)
    accel_x = (data[0] << 8) | data[1]
    accel_y = (data[2] << 8) | data[3]
    accel_z = (data[4] << 8) | data[5]
    gyro_x = (data[8] << 8) | data[9]
    gyro_y = (data[10] << 8) | data[11]
    gyro_z = (data[12] << 8) | data[13]
    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z


# Set PLL to maximum frequency (250 MHz)
machine.freq(250000000)

# Print current CPU frequency
cpu_frequency = machine.freq()
print("CPU Frequency:", cpu_frequency, "Hz")
# Main loop
while True:
    start_time = utime.ticks_us()  # Get current time
    accel_x, accel_y, accel_z,  gyro_x, gyro_y, gyro_z = read_sensor_data()
    # Process sensor data as required
    end_time = utime.ticks_us()  # Get current time
    execution_time = utime.ticks_diff(end_time, start_time)  # Calculate execution time
    if execution_time < 10:  # Maintain 1 ms interval
        utime.sleep_ms(1 - execution_time)
    print('Time:', execution_time, 'us')
    print('ax', accel_x, 'ay', accel_y, 'az', accel_z, 'gx', gyro_x, 'gy', gyro_y, 'gz', gyro_z)
