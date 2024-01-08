from machine import Pin
from time import sleep

sw1 = Pin(15, Pin.IN)
sw2 = Pin(16, Pin.IN)

while True:
    print(sw1.value(), sw2.value())
    sleep(0.2)