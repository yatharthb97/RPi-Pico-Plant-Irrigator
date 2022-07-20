from machine import Pin
import time
import utime
import ds1302

#def get_yearday(dd, mm, yyyy):
#    from datetime import date
#    d0 = date(yyyy, 1, 1)
#    d1 = date(yyyy, mm, dd)
#    delta = d1 - d0
#    return delta

set_rtc = False

ds = ds1302.DS1302(Pin(18),Pin(17),Pin(16))
# [self.year(), self.month(), self.day(), self.weekday(), self.hour(), self.minute(), self.second()]
# (0:year, 1:month, 2:mday, 3:hour, 4:minute, 5:second, 6:weekday, 7:yearday)
        
if set_rtc:
    # Read compilation time
    year, month, mday, hour, minute, second, weekday, yearday = time.localtime()
    ds.date_time([year, month, mday, weekday, hour, minute, second])

while True:
    on_chip_rtc = time.localtime()
    ds_rtc = ds.date_time()
    #print("(0:year, 1:month, 2:mday, 3:hour, 4:minute, 5:second, 6:weekday, 7:yearday)")
    print("On-chip: ", on_chip_rtc)
    print("DS RTC:  ", ds_rtc)
    #print("Yearday: ", get_yearday(ds_rtc[2], ds_rtc[1], ds_rtc[0]))
    utime.sleep(1)