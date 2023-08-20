from micropython import const
import board, time
import digitalio
import rotaryio
import pwmio
import keypad

led_power = digitalio.DigitalInOut(board.LED)
led_power.direction = digitalio.Direction.OUTPUT
led_power.value = True

led_left = pwmio.PWMOut(board.GP17, frequency=1000)
led_right = pwmio.PWMOut(board.GP0, frequency=1000)

lights = digitalio.DigitalInOut(board.GP16)
lights.direction = digitalio.Direction.OUTPUT
lights.value = False

encoder = rotaryio.IncrementalEncoder(board.GP21, board.GP22)

keys = keypad.Keys((board.GP18, board.GP19, board.GP20), value_when_pressed=False, pull=True)
KEY_A = const(0)
KEY_B = const(1)
KEY_C = const(2)


def drive_led(led_nr: int, power: float):
    led_left.duty_cycle = 0
    led_right.duty_cycle = 0
    led = led_left if led_nr == 0 else led_right
    led.duty_cycle = int(0xffff * power)
    
    
def lights_on():
    print('lights on')
    lights.value = True
    
    
def lights_off():
    print('lights off')
    lights.value = False


def press_duration(press_event):
    if not press_event.pressed:
        raise ValueError("measuring duration must start with a press")
    while True:
        release_event = keys.events.get()
        if release_event:
            return release_event.timestamp - press_event.timestamp


if __name__ == '__main__':
    led_nr = 0
    power = 0.1
    while True:
        event = keys.events.get()
        if event and event.pressed:
            
            if event.key_number == KEY_A:
                led_nr = 1 - led_nr
                drive_led(led_nr, power)
                
            if event.key_number == KEY_B:
                power = 1 - power
                drive_led(led_nr, power)
                
            if event.key_number == KEY_C:
                led_power.value = False
                print(encoder.position)
                time.sleep(0.1)
                led_power.value = True
                break

    drive_led(0, 0.0)
    drive_led(0, 0.0)
    led_power.value = True
    
    lights_on()
    time.sleep(1)
    lights_off()