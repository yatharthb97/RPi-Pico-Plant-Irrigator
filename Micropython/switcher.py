from machine import Pin, Timer
import machine
from time import sleep
import time

class TwoStateSwitch:
    
    def __init__(self, pin1, pin2):
        self.pin1 = Pin(pin1, Pin.IN)
        self.pin2 = Pin(pin2, Pin.IN)
        
        self.value = -1
        self.flag = False
        
        self.debounce_ms = 300
        self._next_call = time.ticks_ms()
        
        self.pin1.irq(handler=self.counter, trigger= Pin.IRQ_RISING, hard=False)
        self.pin2.irq(handler=self.clear, trigger= Pin.IRQ_RISING, hard=False)

        #self.timer = Timer(period=10000, mode=Timer.PERIODIC, callback=self.autoclear)
        
    def counter(self, pin):
        self.value = self.value + 1
        self.flag = True
        
    def clear(self, pin):
        self.value = 0
        self.flag = True
        
    def autoclear(self, timer):
        print("Timer cleared buffer state.")
        self.value = 0
        self.flag = True
            
        
    def read(self, pin):
        if time.ticks_ms() > self._next_call:
            self.debounce_ms = time.ticks_ms() + self.debounce_ms
            print("IRQ init")
            sleep(0.3)
            self.value =  (self.pin1() * 2) + (self.pin2() * 1)
            self.flag = True
            print("IRQ exit")