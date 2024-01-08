from reservoir import Reservoir, Pump
from switcher import TwoStateSwitch
from time import sleep
from machine import Pin, RTC
from ds1302 import DS1302
import math
from _thread import start_new_thread
from resource import set_ds1302, sync_rtc, build_rtc

global rtc, rrtc
led = Pin(25, Pin.OUT)
res = Reservoir(5)
rrtc = DS1302(Pin(19), Pin(18), Pin(20))
#rtc = build_rtc(rrtc)
#sync_rtc(rtc, rrtc)

rtc = RTC()

#------- RTC is synchronised
global poll_wait, trigger_time, last_trigger_time, water_time_s
poll_wait = 1.5 
trigger_time = [11, 22]
last_trigger_time = [0,0]
water_time_s = 10


#-------



p1 = Pump(14)
res.pumps.append(p1)

p2 = Pump(13)
res.pumps.append(p2)

p3 = Pump(12)
res.pumps.append(p3)
    
p4 = Pump(11)
res.pumps.append(p4)

sw = TwoStateSwitch(15, 16)


def sec_diff(t1, t2):
    t1_ = t1[0]*3600 + t1[1]*60
    t2_ = t2[0]*3600 + t2[1]*60
    return math.fabs(t1_ - t2_)

def processor2():
    while True:
        led.on()
        sleep(poll_wait)
        led.off()
        sleep(0.1)
        
        if sw.flag:
            sw.flag = False
            print("Switch value:", sw.value)
            if sw.value == 0:
                for p in res.pumps:
                    p.off()
            else:
                res.pumps[0].toggle()
                sw.value = 0
                
        now = rrtc.datetime()
        now = [now[4], now[5]]
        print(now)
        global last_trigger_time
        #print(last_trigger_time)
        sd_ = sec_diff(last_trigger_time, now)
        if (now == trigger_time) and (sd_ > 2*poll_wait):
            print("Its time!!!")
            p1.on()
            sleep(water_time_s)
            p1.off()
            last_trigger_time = now
            
start_new_thread(processor2, ())
#processor2()