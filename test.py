# Toggle a led
from machine import Pin
from time import sleep
pin = Pin("LED", Pin.OUT)

while True:
    pin.toggle()
    print("LED is ON" if pin.value() == 1 else "LED is OFF")
    sleep(1)
    
    