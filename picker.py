import board
import keypad
from display import display_hex, set_digit, blink_digit, update_display
from peripherals import keys, KEY_A, KEY_B, KEY_C, encoder


def pick_digits(min_digits_hex, max_digits_hex, initial_hex=None, stop_hex=None):
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
    encoder.position = digits[current_position] - min_digits[current_position]
    blink_digit(current_position)
    while True:
        digits[current_position] = encoder.position % (1 + max_digits[current_position] - min_digits[current_position]) + min_digits[current_position]
        set_digit(current_position, digits[current_position])
        update_display()
        event = keys.events.get()
        if event and event.pressed:
            
            if event.key_number == KEY_A:
                current_position = current_position - 1 if current_position > 0 else 3
            if event.key_number == KEY_B:
                current_position = current_position + 1 if current_position < 3 else 0
                
            if event.key_number == KEY_A or event.key_number == KEY_B:
                encoder.position = digits[current_position] - min_digits[current_position]
                blink_digit(current_position)
                
            if event.key_number == KEY_C:
                break
            
        value = digits[0] * 0x1000 + digits[1] * 0x100 + digits[2] * 0x10 + digits[3] * 0x1
        if value == stop_hex:
            break
            
    blink_digit(None)
    return value


if __name__ == '__main__':
    result = pick_digits(0x0000, 0x2359, initial_hex=0x1234)
    print(result, ' / ', hex(result))
    result = pick_digits(0xAAAA, 0xFFFF, stop_hex=0xCAFE)
    print(result, ' / ', hex(result))
    