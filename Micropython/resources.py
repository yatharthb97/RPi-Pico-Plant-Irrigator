import time

def update_ds_rtc(ds_obj):
    # Read compilation time
    year, month, mday, hour, minute, second, weekday, yearday = time.localtime()
    ds_obj.date_time([year, month, mday, weekday, hour, minute, second])
    
class Relay:
    '''Set constants for controlling relay.'''
    on = 0
    off = 1

def clac_yearday(dd, mm, yyyy):
    c = 20 # Century
    h = dd + (13(mm+1)/5) + yyyy + (yyyy/4) + (c/4) + 5*c
    return int(h)

def interconvert(tstruct):
    """
    Interconvert between the datetime structure returned by the on-chip RTC and the DS1302 External RTC.
    """
    if len(tstruct) == 8:
        # On-chip RTC struct
        year, month, mday, hour, minute, second, weekday, yearday = tstruct
        return [year, month, mday, weekday, hour, minute, second]
    elif len(tstruct) == 7:
        year, month, mday, weekday, hour, minute, second = tstruct
        return (year, month, mday, hour, minute, second, weekday, clac_yearday(mday, month, year))
        

def ds_rtc_time_check(dsobj, watering_time, last_pump):
    pass    



def on_chip_time_check(watering_time, last_pump):
    """
    Returns True if it is time to run the pump by using the on-chip RTC.
    watering_time & last_pump has the format:
    (0:year, 1:month, 2:mday, 3:hour, 4:minute, 5:second, 6:weekday, 7:yearday)
    """
    # Read Current Time
    now = time.localtime()
    diff3 = now[3] - watering_time[3]
    diff4 = now[4] - watering_time[4]
    
    # Check if it's time to water
    if diff3 == 0 and abs(diff4) < 5: #Tolerance of 5 min
        if last_pump[7] != now[7]:
            return True
    return False
            