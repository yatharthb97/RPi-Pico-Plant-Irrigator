# Options ▬ ↓ ▬

sch_pump_duration_min = 2
sch_pump_time = (17, 10, 00) # 5:10 PM
sch_pump_day_freq = 1
sch_check_poll_freq_min = 15
sync_ds1302 = False

####################################################
from machine import Pin, RTC
import utime
from resource import *
from pump import *
#from pyb import RTC -> ImportError

# Peripherals ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
led = Pin(25, Pin.OUT)
b1 = Pin(15, Pin.IN)
b2 = Pin(16, Pin.IN)
buzzer = Pin(9, Pin.OUT, value=Relay.off)
pump = Pin(8, Pin.OUT, value=Relay.off)

ds_rtc = ds1302.DS1302()
if sync_ds1302:
    ds_rtc = set_ds1302(ds_rtc)
rtc = build_rtc(ds_rtc)



# Interrupts ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
b1.irq(handler=man_pump_isr, trigger=Pin.IRQ_RISING, hard=True)
b2.irq(handler=man_pump_counter, trigger=Pin.IRQ_FALLING, hard=True)

# RTC periodic alarm & alarm interrupt ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
rtc.alarm(int(sch_check_poll_freq_min*60*1000), repeat=True)
rtc.irq(trigger=RTC.ALARM0, handler=rtc_isr, wake=machine.IDLE)

man_act_flag = False
rtc_alarm_flag = False

start_dt = interconvert(ds_rtc.datetime())

# Check & create Files to Prevent Crashes
CheckAndCreate("last_pump_yearday.txt", start_dt[7]-1)
CheckAndCreate("pumptime.txt", 0)

# Event Loop
while True:
    
    # Sleep for power-saving
    utime.sleep(0.5)

    
    # >----- Timeout based reset -----<
    now = time.ticks_ms()
    timeout_ = time.ticks_diff(now, last_b2_time) > 20000
    if timeout_ and man_pump_time > 0:
        man_pump_time = 0
        led.value(0)
    # >------ Timeout based reset -----<
    

    # >---- Manual Pump Activation ----<
    if man_act_flag:
        #--
        buzzer.value(Relay.on)
        utime.sleep(1)
        buzzer.value(Relay.off)
        
        # >---- Maybe Reset man_pump_time ----<
        if b1.value() == 0:
            man_pump_time = 0
            led.value(man_pump_time > 0)
            
        if longpress(b1):
            # 3 beeps
            for i in range(6):
                buzzer.toggle()
                utime.sleep(0.5)
            buzzer.value(Relay.off)
            
            # Run Pump
            if man_pump_time > 0 and WaterAvailable():
                pumptime = man_pump_time*man_pump_min_unit*60
                run_pump(pump_time)
        else:
            man_pump_time = 0
        man_act_flag = False
    # >---- Manual Pump Activation ----<
    
    
    # >---- Scheduled Pump Activation ----<
    if rtc_alarm_flag:
        for _ in range(6):
            utime.sleep(0.25)
            buzzer.toggle()
        buzzer.value(Relay.off)
        
        dt_now = interconvert(ds_rtc.datetime())
        if WaterAvailable() and time_check(dt_now, sch_pump_time, Read('last_pump_yearday.txt')):
            run_pump(sch_pump_duration_min * 60)      # Run Pump
            Write('last_pump_yearday.txt', dt_now[7]) # Update Yearday
        rtc_alaram_flag = False
    # >---- Scheduled Pump Activation ----<

# >-------------------- While Loop Ends --------------------<
    

    

        
    
