#"""
#Code that doesn't have another home (file).
#"""

import time
from jeanmeeus import yearday
from ds1302 import DS1302


    
class Relay:
    """
    Set constants for controlling relay.
    """
    on = 0
    off = 1
    
    def to_bool(state):
        return (state == Relay.on)*(True) + \
               (state == Relay.off)*(False)
        
    def to_state(boolean):
        return (boolean == False)*(Relay.off) + \
               (boolean == True)*(Relay.on)

def Read(filename):
    with open(filename, 'r') as file:
        val = file.read()
        return float(val)
    
def Write(filename, value):
    with open(filename, 'w') as file:
        file.write(value)
        
def CheckAndCreate(filename, default_value):
    pass

def interconvert(tstruct):
    """
    Interconvert between the datetime structure returned by the on-chip RTC and the DS1302 External RTC.
    """
    if len(tstruct) == 8:
        # On-chip RTC struct
        year, month, mday, hour, minute, second, weekday, yearday_ = tstruct
        return [year, month, mday, weekday, hour, minute, second]
    elif len(tstruct) == 7:
        # DS1302 RTC struct
        year, month, mday, weekday, hour, minute, second = tstruct
        return (year, month, mday, hour, minute, second, weekday, yearday(mday, month, year))
    else:
        return
        

def time_check(dt_now, sch_time_tuple, last_pump_yearday, tolerance_min=5):
    """
    Returns True if it is time to run the pump by using the on-chip RTC.
    watering_time & last_pump has the format:
    time_now: tuple → (0:year, 1:month, 2:mday, 3:hour, 4:minute, 5:second, 6:weekday, 7:yearday)
    sch_time_tuple : tuple → (hh,mm,ss)
    """
    global sch_pump_day_freq
    
    # Compare time
    hour_diff = dt_now[3] - sch_time_tuple[0]
    min_diff = dt_now[4] - sch_time_tuple[1]
    
    # Check if it's time to water
    if hour_diff == 0 and abs(min_diff) < tolerance_min:
        if dt_now[7] >= last_pump_yearday + sch_pump_day_freq:
            return True
    return False


# >-----------<•>-----------<••• Other functions •••>-----------<•>-----------<

def longpress(button):
    """
    Long press activation check - returns true if b1 is called for 3 straight seconds.
    """
    utime.sleep(3)
    if button.value() == 1:
        return True
    else:
        return False
    
# >-----------<•>-----------<••• RTC Objects •••>-----------<•>-----------<

def build_rtc(DS1302):
    """
    Construct an RTC object and initalize it with an DS1032
    """
    from machine import RTC
    rtc = RTC()
    rtc.datetime(interconvert(DS1302.datetime()))
    return rtc

def sync_rtc(rtc, ds_rtc):
    """
    Sync time from DS1302 to Machine RTC object if the time is 2 minutes out of sync.
    """
    ds_rtc_time = interconvert(ds_rtc.datetime())
    rtc_time = rtc.datetime()
    
    #(0:year, 1:month, 2:mday, 3:hour, 4:minute, 5:second, 6:weekday, 7:yearday)
    ds_rtc_sec = (ds_rtc_time[0]-1) * 365 +  (ds_rtc_time[7] * 24 * 3600)
    rtc_sec = (rtc_time[0]-1) * 365 +  (rtc_time[7] * 24 * 3600)
    
    #if ds_rtc_sec -  rtc_sec > 120: # 2 minutes out of sync
        # Set Machine RTC to DS1302 RTC time
    rtc.datetime(ds_rtc_time)
    
    return rtc

def set_ds1302(ds1302):
    # Read compilation time
    year, month, mday, hour, minute, second, weekday, yearday = time.localtime()
    ds1302.date_time([year, month, mday, weekday, hour, minute, second])
    return ds1302