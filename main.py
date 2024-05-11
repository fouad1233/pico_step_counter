import machine
from machine import Pin, SPI
import utime
import time
import sdcard
import os
# Configure I2C
i2c = machine.I2C(0,freq=400000, sda=machine.Pin(0), scl=machine.Pin(1))
pin = machine.Pin("LED", machine.Pin.OUT)

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
        i2c.writeto_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_PWR_MGMT_1, b'\x00')  # Wake up MPU6050
        i2c.writeto_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_SMPLRT_DIV, b'\x00')  # Sample rate divider (1kHz)
        i2c.writeto_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_ACCEL_CONFIG, b'\x00')  # Accelerometer scale (+/- 2g)
        i2c.writeto_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_GYRO_CONFIG, b'\x00')  # Gyroscope scale (+/- 250deg/s)

        
    def read_sensor_data(self):
        data = i2c.readfrom_mem(MPU6050.MPU6050_ADDR, MPU6050.MPU6050_REG_ACCEL_XOUT_H, 14)
        self.accel_x = (data[0] << 8) | data[1]
        self.accel_y = (data[2] << 8) | data[3]
        self.accel_z = (data[4] << 8) | data[5]
        self.gyro_x = (data[8] << 8) | data[9]
        self.gyro_y = (data[10] << 8) | data[11]
        self.gyro_z = (data[12] << 8) | data[13]
        

MPU6050_Sensor = MPU6050(i2c)  


 
# Initialize the SD card
spi=SPI(1,baudrate=40000000,sck=Pin(10),mosi=Pin(11),miso=Pin(12))
# Initialize SD card
try:
    sd=sdcard.SDCard(spi,Pin(13))
except:
    print("SD card not found")

try:
    # Mount filesystem
    vfs = os.VfsFat(sd)
    os.mount(sd, "/sd")
except:
    print("File system not found")

test_num = 0
try:
    
    # Create / Open a file in write mode.
    # Write mode creates a new file.
    # If  already file exists. Then, it overwrites the file.
    file = open("/sd/test_num.txt","r")
    content = file.read()
    test_num = int(content)
    file.close()
    
    file = open("/sd/test_num.txt","w")
    file.write(str(test_num+1))
    file.close()
    

except:
    print("File not found")
try:
    
    # Create / Open a file in write mode.
    # Write mode creates a new file.
    # If  already file exists. Then, it overwrites the file.
    file = open("/sd/test" +str(test_num) +".txt","w")
    file.write("test"+str(test_num)+"\r\n")
    file.close()

except:
    print("File not found")
 
# Open the file we just created and read from it
#with open("/sd/test01.txt", "r") as file:
#    data = file.read()
#    print(data)
sdCardError = False

def timer1_callback(timer):
    global sdCardError
    #start_time = time.ticks_us()
    MPU6050_Sensor.read_sensor_data()
    try:
        timestmap = time.ticks_ms()
        file = open("/sd/test" +str(test_num) +".txt","a")
        file.write(str(timestmap)+ '\t' + str(MPU6050_Sensor.accel_x) + '\t' + str(MPU6050_Sensor.accel_y) + '\t' + str(MPU6050_Sensor.accel_z) + '\t' + str(MPU6050_Sensor.gyro_x) + '\t' + str(MPU6050_Sensor.gyro_y) + '\t' + str(MPU6050_Sensor.gyro_z) + '\n')
        file.close()
        sdCardError = False
    except:
        sdCardError = True
        
        #print("File not found")
    #measure time
    #stop_time = time.ticks_us()
    #calculate time
    #delta_time = time.ticks_diff(stop_time, start_time)
    
    #display time in seconds
    #print("Time: ", delta_time/1000, "ms\n")

def timer2_callback(timer):
    print('ax', MPU6050_Sensor.accel_x, 'ay', MPU6050_Sensor.accel_y, 'az', MPU6050_Sensor.accel_z, 'gx', MPU6050_Sensor.gyro_x, 'gy', MPU6050_Sensor.gyro_y, 'gz', MPU6050_Sensor.gyro_z)
    if sdCardError:
        pin.toggle()


# Set PLL to maximum frequency (250 MHz)
machine.freq(250000000)

# Print current CPU frequency
cpu_frequency = machine.freq()
print("CPU Frequency:", cpu_frequency, "Hz")



timer1 = machine.Timer()
timer1.init(period=100, mode=machine.Timer.PERIODIC, callback=timer1_callback)

timer2 = machine.Timer()
timer2.init(period=1000, mode=machine.Timer.PERIODIC, callback=timer2_callback)
# Main loop


while True:
    utime.sleep(1)