import board
import time
import digitalio
import rotaryio
import pwmio
import keypad
from display import display_dec
from rtc import RTC
from peripherals import keys, KEY_A, KEY_B, KEY_C

rtc = RTC()

while True:
    event = keys.events.get()
    
    datetime = rtc.datetime
    display_dec(datetime[4] * 100 + datetime[5])
    
    if event and event.pressed:
        print(event.key_number)
        if event.key_number == KEY_C:
            break
    
    time.sleep(0.005)