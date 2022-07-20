def fn_core1():
    
    def irq_water():
        now = time.ticks_ms()
        if time.ticks_diff(now, last_hit) < debounce_ms:
            irq_run_pump = True
            last_hit = now
    
    while True:
        global irq_run_pump
        if irq_run_pump:
            run_pump()
            irq_run_pump = False



# Setup the irq and thread for inerrupt
#Switch.irq(handler=irq_water, trigger=Pin.IRQ_RISING, hard=True)
_thread.start_new_thread(fn_core1, ())

