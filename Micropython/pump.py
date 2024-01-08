from resource import Relay
import time
import utime


last_b2_time = None
b1_flag = False
b2_flag = False


def run_pump(pump_time):
    pump_is_running = True
    pump.value(Relay.on)
                
    # Record time
    utime.sleep(pumptime)
    pump.value(Relay.off)
                
    pump_is_running = False
    # Record time and time correction is needed
                
    #RegisterPumpTime(pumpduration)


def rtc_isr(what):
    global rtc_alarm_flag, debug
    rtc_alarm_flag = True
    if debug:
        print("RTC alaram!")

def man_pump_isr(pin):
    global b1_flag, debug
    b1_flag = True
    if debug:
        print("B1 ISR!")

def man_pump_counter(pin):
    """
    ISR for recording manual pump time.
    """
    global man_pump_time, last_b2_time, led, debug
    man_pump_time += 1
    last_b2_time = time.ticks_ms()
    led.value(man_pump_time > 0)
    if debug:
        print("B2 ISR! -> {}".format(man_pump_time))


def stop_pump(pin):
    """
    ISR to stop the pump midway.
    """
    global pump_is_running, pump
    if pump_is_running:
        pump.value(Relay.off)
        pump_is_running = False


### Pump and filesystem #### 
class Tank:
    
    # Pump object
    pump_is_running = False
    pumps_litre_per_min = 1
    max_tank_cap_litre = 45
    
    
    # Manual Pump Varaibles
    man_pump_time     = 0
    man_pump_min_unit = 0.5
    
    def water_available():
        return True
        
        pump_time = Tank.min_operated()
        used_water = pump_time * pumps_litre_per_min
        return (Tank.max_tank_cap_litre - used_water) > 0

    def register_pump(time_min, log=False, datetime=None):
        """
        Add the `time_min` to the pumping time.
        """
        pump_time = Tank.min_operated()
            
        with open("pumptime.txt", 'w') as file:
            file.write("{:.2f}".format(str(pump_time + time_min)))
        
        if log:
            with open("pumplogs.txt", 'a') as logger:
               logger.write("{}") 
        
    def min_operated():
        """
        The time in minutes for whcih the pump was run.
        """
        pump_time = None
        with open("pumptime.txt", 'r') as file:
            pump_time = float(file.read())
        return pump_time

    def reset():
        """
        When called, the function restores the `water-remaining` value to `max-capacity`.
        """
        with open("pumptime.txt", 'w') as file:
            file.write(Tank.max_tank_cap_litre)
