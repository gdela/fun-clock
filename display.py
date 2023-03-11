import time, board
import digitalio
from supervisor import ticks_ms

data_a = digitalio.DigitalInOut(board.GP13)
data_b = digitalio.DigitalInOut(board.GP15)
data_c = digitalio.DigitalInOut(board.GP2)
data_d = digitalio.DigitalInOut(board.GP3)

data_a.direction = digitalio.Direction.OUTPUT
data_b.direction = digitalio.Direction.OUTPUT
data_c.direction = digitalio.Direction.OUTPUT
data_d.direction = digitalio.Direction.OUTPUT

strobe = [
    digitalio.DigitalInOut(board.GP14),
    digitalio.DigitalInOut(board.GP11),
    digitalio.DigitalInOut(board.GP6),
    digitalio.DigitalInOut(board.GP4)
]
blanking = [
    digitalio.DigitalInOut(board.GP12),
    digitalio.DigitalInOut(board.GP10),
    digitalio.DigitalInOut(board.GP5),
    digitalio.DigitalInOut(board.GP1)
]

for i in range(0, 4):
    strobe[i].direction = digitalio.Direction.OUTPUT
    blanking[i].direction = digitalio.Direction.OUTPUT
    strobe[i].value = True
    blanking[i].value = False


def set_digit(position, digit):
    if digit == None:
        blanking[position].value = True
        return
    data_a.value = digit & (1 << 0)
    data_b.value = digit & (1 << 1)
    data_c.value = digit & (1 << 2)
    data_d.value = digit & (1 << 3)
    strobe[position].value = False
    strobe[position].value = True


def display_dec(value):
    set_digit(0, value // 1000 % 10)
    set_digit(1, value // 100 % 10)
    set_digit(2, value // 10 % 10)
    set_digit(3, value // 1 % 10)
    
    
def display_hex(value):
    set_digit(0, value // 0x1000 % 0x10)
    set_digit(1, value // 0x100 % 0x10)
    set_digit(2, value // 0x10 % 0x10)
    set_digit(3, value // 0x1 % 0x10)


blinking_position = None
def blink_digit(position):
    global blinking_position
    if blinking_position != None:
        blanking[blinking_position].value = False
    blinking_position = position


last_flip_ticks = ticks_ms()
def update_display():
    global last_flip_ticks
    ticks_elapsed = ticks_ms() - last_flip_ticks
    if blinking_position == None:
        return
    is_blank = blanking[blinking_position].value
    if ticks_elapsed < 0 or ticks_elapsed >= (20 if is_blank else 100):
        blanking[blinking_position].value = not is_blank
        last_flip_ticks = ticks_ms()


if __name__ == '__main__':
    for i in range(0, 100):
        display_dec(i * 100 + i)
        time.sleep(0.01)
    time.sleep(0.5)
    
    display_hex(0xcafe)
    time.sleep(0.5)
    display_hex(0xbabe)
    time.sleep(0.5)
    display_hex(0x0ff0)
    
    blink_digit(1)
    for i in range(0, 666):
        update_display()
        time.sleep(0.001)
    
    blink_digit(2)
    for i in range(0, 666):
        update_display()
        time.sleep(0.001)
        
    blink_digit(None)
    for i in range(0, 666):
        update_display()
        time.sleep(0.001)
        
    set_digit(1, None)
    set_digit(2, None)
