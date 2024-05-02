from machine import Pin, Timer

led = Pin("LED", Pin.OUT)

def tick(timer):
  led.toggle()

Timer().init(freq=10, mode=Timer.PERIODIC, callback=tick)