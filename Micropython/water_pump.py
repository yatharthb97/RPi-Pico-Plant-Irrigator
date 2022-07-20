# Control Constants
pump_running_time_s = 120 # 2 minutes
watering_time = (0, 0, 0, 17, 15, 0, 0, 0) #(0:year, 1:month, 2:mday, 3:hour, 4:minute, 5:second, 6:weekday, 7:yearday)
sleep_time_min = 15
debounce_ms = 50




###############################################################################################

# Imports
import utime
import time
from machine import Pin
import _thread
from resource import update_ds_rtc, Relay


# Resources
TempSensor = machine.ADC(4)
WaterPump = machine.Pin(0, Pin.OUT, value=Relay.off)
Buzzer = machine.Pin(0, Pin.OUT, value=Relay.off)
Switch = machine.Pin(0, Pin.IN)
RTC = ds1302.DS1302(Pin(18),Pin(17),Pin(16))


sleep_time_s = sleep_time_min * 60
last_hit = time.ticks_ms()
irq_run_pump = False



# Run Pump Definations
def run_pump(time_s=2):
    '''Run Water Pump.'''
    Buzzer.value(Relay.on)
    WaterPump.value(Relay.on)
    utime.sleep(time_s)
    WaterPump.value(Relay.off)
    Buzzer.value(Relay.off)



while True:    
    
    run_pump(time_s=pump_running_time_s)
    last_pump = time.localtime()
            
    # Sleep for some time
    utime.sleep(sleep_time_s)
        
#(0:year, 1:month, 2:mday, 3:hour, 4:minute, 5:second, 6:weekday, 7:yearday)


        

    
