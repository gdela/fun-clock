import board
import time
import digitalio
import rotaryio
import pwmio

weekdayAlarm = 0
weekendAlarm = 0
nextAlarm = weekdayAlarm

blink = True
val = 1
val_change = time.monotonic()
while encoder.position >= 0 and encoder.position < 16:
    i = encoder.position
    curr = time.monotonic()
    if blink and (curr - val_change) > 0.2:
        val = 1 - val
        blanking.value = val
        val_change = curr
    if btn_a.value == False:
        blink = False
        blanking.value = 0
    if btn_b.value == False:
        blink = True
        
blanking.value = 1


