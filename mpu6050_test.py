#Shows Pi is on by turning on LED when plugged in
from imu import MPU6050
from time import sleep
import time
import machine
from machine import Pin, I2C

LED = machine.Pin("LED", machine.Pin.OUT)
LED.on()





i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)


while True:
    #measure time 
	start_time = time.ticks_us()
	
	print("ax",imu.accel.x,"\t","ay",imu.accel.y,"\t","az",imu.accel.z,"\t","gx",imu.gyro.x,"\t","gy",imu.gyro.y,"\t","gz",imu.gyro.z,"\t","Temperature",imu.temperature,"        ",end="\r")
 
	#measure time
	stop_time = time.ticks_us()
	#calculate time
	delta_time = time.ticks_diff(stop_time, start_time)
	
	#display time in seconds
	print("Time: ", delta_time/1000, "ms\n")
	
	
