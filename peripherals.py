import board, time
import digitalio
import rotaryio
import keypad

led_power = digitalio.DigitalInOut(board.LED)
led_power.direction = digitalio.Direction.OUTPUT
led_power.value = True

led_x = digitalio.DigitalInOut(board.GP17)
led_y = digitalio.DigitalInOut(board.GP0)
led_x.direction = digitalio.Direction.OUTPUT
led_y.direction = digitalio.Direction.OUTPUT
led_x.value = False
led_y.value = False

encoder = rotaryio.IncrementalEncoder(board.GP21, board.GP22)

keys = keypad.Keys((board.GP18, board.GP19, board.GP20), value_when_pressed=False, pull=True)
KEY_A = 0
KEY_B = 1
KEY_C = 2

if __name__ == '__main__':
    while True:
        event = keys.events.get()
        if event and event.pressed:
            
            if event.key_number == KEY_A:
                led_x.value = not led_x.value
                
            if event.key_number == KEY_B:
                led_y.value = not led_y.value
                
            if event.key_number == KEY_C:
                led_power.value = False
                print(encoder.position)
                time.sleep(0.1)
                led_power.value = True
                
            if led_x.value and led_y.value and event.key_number == KEY_C:
                break

    led_x.value = False
    led_y.value = False
    led_power.value = True