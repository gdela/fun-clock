import os, rtc
from micropython import const
from time import struct_time
from network import get_socket_pool
from adafruit_ntp import NTP
from display import display_dec
from peripherals import drive_led

rtc = rtc.RTC()

WEEKDAY = const(0)
WEEKEND = const(1)
day_type = WEEKDAY
time_zone_offset = 1
last_synchronization_day = -1


def current_day_type():
    return day_type


def update_clock(now:struct_time = None):
    if now == None:
        now = rtc.datetime
    determine_day_type(now)
    global last_synchronization_day
    if last_synchronization_day != now.tm_mday:
        synchronize_clock()
        last_synchronization_day = now.tm_mday
    display_dec(now.tm_hour * 100 + now.tm_min)


def determine_day_type(now:struct_time):
    global day_type
    if now.tm_wday < 4 or (now.tm_wday == 4 and now.tm_hour <= 15):  # up to friday 15:59
        day_type = WEEKDAY
    elif now.tm_wday == 6 and now.tm_hour > 15:  # since sunday 16:00
        day_type = WEEKDAY
    else:
        day_type = WEEKEND
    drive_led(day_type, 0.2)


def load_time_zone_offset():
    global time_zone_offset
    with open('offset.txt', 'r') as file:
        contents = file.read()
        time_zone_offset = int(contents)
    print(f'loaded time zone offset: {time_zone_offset}')


def store_time_zone_offset():
    with open('offset.txt', 'w') as file:
        file.write(str(time_zone_offset))


try:
    load_time_zone_offset()
except Exception as e:
    print('cannot load time zone offset: ' + str(e))


def switch_dst():
    global time_zone_offset
    time_zone_offset = 2 if time_zone_offset == 1 else 1
    store_time_zone_offset()
    print(f'changed time zone offset to: {time_zone_offset}')
    synchronize_clock()


def synchronize_clock():
    try:
        ntp = NTP(get_socket_pool(), tz_offset=time_zone_offset, socket_timeout=10)
        now = rtc.datetime = ntp.datetime
        print(f'synchronized to: {now.tm_year}-{now.tm_mon:02d}-{now.tm_mday:02d} {now.tm_hour:02d}:{now.tm_min:02d}')
    except Exception as e:
        print('cannot synchronize: ' + str(e))


def now_with(**modifications) -> struct_time:
    source = rtc.datetime
    target = {}
    for a in [a for a in dir(source) if a.startswith('tm_')]:
        target[a] = getattr(source, a)
        if a in modifications:
            target[a] = modifications[a]
    return struct_time([
        target['tm_year'],
        target['tm_mon'],
        target['tm_mday'],
        target['tm_hour'],
        target['tm_min'],
        target['tm_sec'],
        target['tm_wday'],
        target['tm_yday'],
        target['tm_isdst']
    ])

        
if __name__ == '__main__':
    #switch_dst()
    #synchronize_clock()
    update_clock()  # will trigger auto synchronization
    update_clock()  # will skip auto synchronization in the same day
    update_clock(now_with(tm_mday=0))  # will synchronize again in new day
    print(f'current rtc datetime = {rtc.datetime}')
    
    determine_day_type(rtc.datetime)
    print(f'day type currently: {day_type}')
    determine_day_type(now_with(tm_wday=0, tm_hour=00))  # monday midnight
    print(f'day type currently: {day_type} [0 expected]')
    determine_day_type(now_with(tm_wday=4, tm_hour=12))  # friday noon
    print(f'day type currently: {day_type} [0 expected]')
    determine_day_type(now_with(tm_wday=4, tm_hour=22))  # friday evening
    print(f'day type currently: {day_type} [1 expected]')
    determine_day_type(now_with(tm_wday=2, tm_hour=12))  # wednesday noon
    print(f'day type currently: {day_type} [0 expected]')
    determine_day_type(now_with(tm_wday=5, tm_hour=12))  # saturday noon
    print(f'day type currently: {day_type} [1 expected]')
    determine_day_type(now_with(tm_wday=6, tm_hour=22))  # sunday evening
    print(f'day type currently: {day_type} [0 expected]')
    determine_day_type(now_with(tm_wday=6, tm_hour=12))  # sunday noon
    print(f'day type currently: {day_type} [1 expected]')
    
    