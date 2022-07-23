import utime
import time

start_t = time.ticks_ms()
lst =[]
while time.ticks_diff(time.ticks_ms(), start_t) < 4000:
    utime.sleep(1)
    lst.append(time.ticks_ms())
    #print("Hello")
print(lst)