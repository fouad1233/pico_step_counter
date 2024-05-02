#Shows Pi is on by turning on LED when plugged in
from imu import MPU6050
from time import sleep
import time
import machine
from machine import Pin, I2C , Timer

LED = machine.Pin("LED", machine.Pin.OUT)
LED.on()





i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

def tick(timer):
    print("ax",imu.accel.x,"\t","ay",imu.accel.y,"\t","az",imu.accel.z,"\t","gx",imu.gyro.x,"\t","gy",imu.gyro.y,"\t","gz",imu.gyro.z,"\t","Temperature",imu.temperature,"        ",end="\n")


Timer().init(freq=100, mode=Timer.PERIODIC, callback=tick)

while True:
    sleep(1)

	
	
