from time import sleep
from timeutils import JustTime
from display import display_dec
from peripherals import drive_led
from picker import pick_dec_digits


alarms = [JustTime(6, 59), JustTime(6, 59)]


def to_dec(alarm:JustTime) -> int:
    return alarm.hour * 100 + alarm.minute


def set_dec(alarm:JustTime, setting:dec):
    alarm.hour = setting // 100
    alarm.minute = setting % 100


def load_alarms():
    with open('alarms.txt', 'r') as file:
        contents = file.read()
        items = contents.split('\n')
        for i in range(0, len(items)-1):
            set_dec(alarms[i], int(items[i]))
            print(f'loaded alarm {i}: {alarms[i]}')


def store_alarms():
    with open('alarms.txt', 'w') as file:
        for alarm in alarms:
            file.write(f'{to_dec(alarm)}\n')


try:
    load_alarms()
except Exception as e:
    print('cannot load alarms: ' + str(e))


def show_alarm(alarm_nr:int):
    alarm = alarms[alarm_nr]
    drive_led(alarm_nr, 1.0)
    display_dec(to_dec(alarm))
    sleep(2)


def set_alarm(alarm_nr:int):
    drive_led(alarm_nr, 1.0)
    alarm = alarms[alarm_nr]
    result = pick_dec_digits(0000, 2959, initial_dec=to_dec(alarm))
    set_dec(alarm, result)
    print(f'set alarm {alarm_nr} to: {alarm}')
    store_alarms()


def get_alarm(alarm_nr:int) -> JustTime:
    return alarms[alarm_nr]


if __name__ == '__main__':
    alarm_nr = 0
    
    print('showing')
    show_alarm(alarm_nr)
    display_dec(0000)
    drive_led(alarm_nr, 0.0)
    sleep(1)
    
    print('setting')
    set_alarm(alarm_nr)
    display_dec(0000)
    drive_led(alarm_nr, 0.0)
    sleep(1)
    
    print(f'current alarm set to {alarms[alarm_nr]}')
    display_dec(to_dec(alarms[alarm_nr]))
    