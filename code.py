from time import sleep
from timeutils import JustTime
from network import connect_to_wifi
from clock import rtc, update_clock, switch_dst, current_day_type
from alarms import show_alarm, set_alarm, get_alarm
from display import display_blank
from peripherals import keys, KEY_A, KEY_B, KEY_C, press_duration, led_power
from wakeup import update_wakeup, wakeup_in_progress, confirm_wakeup


connect_to_wifi()
update_clock()
print(f'started at {rtc.datetime}')
led_power.value = 0

while True:
    sleep(0.005)
    update_clock()
    alarm_nr = current_day_type()
    alarm: JustTime = get_alarm(alarm_nr)
    clock: JustTime = JustTime.now()
    update_wakeup(alarm, clock)
        
    event = keys.events.get()
    if event and event.pressed:
        
        if event.key_number == KEY_A or event.key_number == KEY_B:
            if wakeup_in_progress():
                confirm_wakeup()
            else:
                show_alarm(alarm_nr)
        
        if event.key_number == KEY_C:
            if press_duration(event) < 500:
                set_alarm(alarm_nr)
            else:
                switch_dst()
