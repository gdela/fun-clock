import board
import keypad
from display import display_hex, set_digit, blink_digit, update_display
from peripherals import keys, KEY_A, KEY_B, KEY_C, encoder
from supervisor import ticks_ms


def decInHex(dec):
    h1 = (dec // 1000 % 10) * 0x1000
    h2 = (dec // 100 % 10) * 0x100
    h3 = (dec // 10 % 10) * 0x10
    h4 = (dec // 1 % 10) * 0x1
    return h1 + h2 + h3 + h4


def hexInDec(hex):
    h1 = (hex // 0x1000 % 0x10) * 1000
    h2 = (hex // 0x100 % 0x10) * 100
    h3 = (hex // 0x10 % 0x10) * 10
    h4 = (hex // 0x1 % 0x10) * 1
    return h1 + h2 + h3 + h4


def pick_dec_digits(min_digits_dec, max_digits_dec, initial_dec=None, stop_dec=None, timeout_seconds=None):
    min_digits_hex = decInHex(min_digits_dec)
    max_digits_hex = decInHex(max_digits_dec)
    initial_hex = None if initial_dec == None else decInHex(initial_dec)
    stop_hex = None if stop_dec == None else decInHex(stop_dec)
    result_hex = pick_hex_digits(min_digits_hex, max_digits_hex, initial_hex, stop_hex, timeout_seconds)
    return hexInDec(result_hex)


def pick_hex_digits(min_digits_hex, max_digits_hex, initial_hex=None, stop_hex=None, timeout_seconds=None):
    start_time = ticks_ms()
    min_digits = [
        min_digits_hex // 0x1000 % 0x10,
        min_digits_hex // 0x100 % 0x10,
        min_digits_hex // 0x10 % 0x10,
        min_digits_hex // 0x1 % 0x10
    ]
    max_digits = [
        max_digits_hex // 0x1000 % 0x10,
        max_digits_hex // 0x100 % 0x10,
        max_digits_hex // 0x10 % 0x10,
        max_digits_hex // 0x1 % 0x10
    ]
    if initial_hex != None:
        display_hex(initial_hex)
    else:
        set_digit(0, None)
        set_digit(1, None)
        set_digit(2, None)
        set_digit(3, None)
        initial_hex = min_digits_hex
    digits = [
        initial_hex // 0x1000 % 0x10,
        initial_hex // 0x100 % 0x10,
        initial_hex // 0x10 % 0x10,
        initial_hex // 0x1 % 0x10
    ]
    current_position = 0
    max_position = 0
    encoder.position = digits[current_position] - min_digits[current_position]
    blink_digit(current_position)
    while True:
        digits[current_position] = encoder.position % (1 + max_digits[current_position] - min_digits[current_position]) + min_digits[current_position]
        set_digit(current_position, digits[current_position], True)
        update_display()
        event = keys.events.get()
        if event and event.pressed:
            
            if event.key_number == KEY_A:
                current_position = current_position - 1 if current_position > 0 else 3
            if event.key_number == KEY_B:
                current_position = current_position + 1 if current_position < 3 else 0
            max_position = max(max_position, current_position)
                
            if event.key_number == KEY_A or event.key_number == KEY_B:
                encoder.position = digits[current_position] - min_digits[current_position]
                blink_digit(current_position)
                
            if event.key_number == KEY_C:
                break
            
        value = digits[0] * 0x1000 + digits[1] * 0x100 + digits[2] * 0x10 + digits[3] * 0x1
        if value == stop_hex and max_position == 3:
            break
        
        current_time = ticks_ms()
        if timeout_seconds != None and current_time - start_time > timeout_seconds * 1000:
            break
            
    blink_digit(None)
    return value


if __name__ == '__main__':
    #result = pick_hex_digits(0x0000, 0x2359, initial_hex=0x1234, timeout_seconds=30)
    #print(result, ' / ', hex(result))
    #result = pick_hex_digits(0xAAAA, 0xFFFF, stop_hex=0xCAFE)
    #print(result, ' / ', hex(result))
    
    #print(str(1234) + ' / ' + hex(decInHex(1234)))
    #print(hex(0x4321) + ' / ' + str(hexInDec(0x4321)))
    result = pick_dec_digits(1001, 5995, initial_dec=2112, stop_dec=3333)
    print(result, ' / ', hex(result))
    