import machine
import utime
import sys
import uos
# Configure I2C
i2c = machine.I2C(0,freq=400000, sda=machine.Pin(0), scl=machine.Pin(1))
#uart = machine.UART(0, baudrate=115200)  # Assuming UART0, adjust the UART number as needed
#uos.dupterm(uart)

#uart.init(baudrate=115200)  # Set baud rate to 115200 bps or adjust to your desired value


class MPU6050():
	# MPU6050 I2C address
	MPU6050_ADDR = 0x68

	# Register addresses
	MPU6050_REG_PWR_MGMT_1 = 0x6B
	MPU6050_REG_SMPLRT_DIV = 0x19
	MPU6050_REG_ACCEL_CONFIG = 0x1C
	MPU6050_REG_GYRO_CONFIG = 0x1B
	MPU6050_REG_ACCEL_XOUT_H = 0x3B
	def __init__(self, i2c):
		self.i2c = i2c
		self.addr = MPU6050.MPU6050_ADDR
		self.accel_x = 0
		self.accel_y = 0
		self.accel_z = 0
		self.gyro_x = 0
		self.gyro_y = 0
		self.gyro_z = 0
		# Initialize MPU6050
		self.i2c.writeto_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_PWR_MGMT_1, b'\x00')  # Wake up MPU6050
		self.i2c.writeto_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_SMPLRT_DIV, b'\x00')  # Sample rate divider (1kHz)
		self.i2c.writeto_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_ACCEL_CONFIG, b'\x00')  # Accelerometer scale (+/- 2g)
		self.i2c.writeto_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_GYRO_CONFIG, b'\x00')  # Gyroscope scale (+/- 250deg/s)

		
	def read_sensor_data(self):
		data = self.i2c.readfrom_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_ACCEL_XOUT_H, 14)
		self.accel_x = (data[0] << 8) | data[1]
		self.accel_y = (data[2] << 8) | data[3]
		self.accel_z = (data[4] << 8) | data[5]
		self.gyro_x = (data[8] << 8) | data[9]
		self.gyro_y = (data[10] << 8) | data[11]
		self.gyro_z = (data[12] << 8) | data[13]
		

MPU6050_Sensor = MPU6050(i2c)  

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(5, machine.Pin.OUT)
 
# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(2),
                  mosi=machine.Pin(3),
                  miso=machine.Pin(4))
 

 
# Open the file we just created and read from it
#with open("/sd/test01.txt", "r") as file:
#    data = file.read()
#    print(data)


def timer1_callback(timer):
	#start_time = time.ticks_us()
	MPU6050_Sensor.read_sensor_data()
	print('ax', MPU6050_Sensor.accel_x, 'ay', MPU6050_Sensor.accel_y, 'az', MPU6050_Sensor.accel_z, 'gx', MPU6050_Sensor.gyro_x, 'gy', MPU6050_Sensor.gyro_y, 'gz', MPU6050_Sensor.gyro_z)

	#try:
		#file.write(str(MPU6050_Sensor.accel_x) + '\t' + str(MPU6050_Sensor.accel_y) + '\t' + str(MPU6050_Sensor.accel_z) + '\t' + str(MPU6050_Sensor.gyro_x) + '\t' + str(MPU6050_Sensor.gyro_y) + '\t' + str(MPU6050_Sensor.gyro_z) + '\n')
	#except:
		#print("File not found")
	#measure time
	#stop_time = time.ticks_us()
	#calculate time
	#delta_time = time.ticks_diff(stop_time, start_time)
	
	#display time in seconds
	#print("Time: ", delta_time/1000, "ms\n")

#def timer2_callback(timer):
#	print('ax', MPU6050_Sensor.accel_x, 'ay', MPU6050_Sensor.accel_y, 'az', MPU6050_Sensor.accel_z, 'gx', MPU6050_Sensor.gyro_x, 'gy', MPU6050_Sensor.gyro_y, 'gz', MPU6050_Sensor.gyro_z)


# Set PLL to maximum frequency (250 MHz)
machine.freq(250000000)

# Print current CPU frequency
cpu_frequency = machine.freq()
print("CPU Frequency:", cpu_frequency, "Hz")



timer1 = machine.Timer()
timer1.init(period=5, mode=machine.Timer.PERIODIC, callback=timer1_callback)

#timer2 = machine.Timer()
#timer2.init(period=10, mode=machine.Timer.PERIODIC, callback=timer2_callback)
# Main loop


while True:
	utime.sleep(1)