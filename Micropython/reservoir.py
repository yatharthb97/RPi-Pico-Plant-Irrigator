from machine import Pin

class Reservoir:
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.pumps = []


class Pump(Pin):
     
    __ch__ = 0
     
    def __init__(self, pin):
        #super().__init__(pin, Pin.OUT, value=1)
        self.pin = Pin(pin, Pin.OUT, value=1)
        self.ch =  self.__ch__
        self.__ch__ = self.__ch__ + 1
        self.buzz = Pin(4, Pin.OUT)
        
    def on(self):
        self.pin.off()
        self.buzz.on()
        
    def off(self):
        self.pin.on()
        self.buzz.off()
        
    def toggle(self):
        self.pin.toggle()
        self.buzz.toggle()
        
