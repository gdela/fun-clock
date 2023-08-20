from time import sleep
from random import randint
from timeutils import JustTime
from display import set_digit, display_dec, display_blank
from picker import pick_hex_digits, pick_dec_digits
from sound import start_sound, stop_sound, set_current_sound, get_current_sound, play_single_sound
from peripherals import lights_on, lights_off


MODE_NORMAL = const(0)
MODE_WAKING_UP = const(1)
MODE_WOKE_UP = const(2)

current_mode = MODE_NORMAL


def update_wakeup(alarm: JustTime, clock: JustTime):
    global current_mode
    diff = alarm.diff_seconds_to(clock) / 60

    if diff <= 0:
        _handle_normal_period()
        
    elif diff <= 1:
        _handle_wakeup_period('alarm')
        
    elif diff <= 5:
        _handle_wakeup_period('strong')
        
    elif diff <= 9:
        _handle_wakeup_period('gentle')
        
    else:
        _handle_normal_period()
        

def wakeup_in_progress():
    global current_mode
    return current_mode == MODE_WAKING_UP


def _handle_wakeup_period(sound):
    global current_mode
    set_current_sound(sound)
    if current_mode == MODE_NORMAL:
        current_mode = MODE_WAKING_UP
        start_sound()
        lights_on()
        

def _wakeup_confirmed():
    global current_mode
    current_mode = MODE_WOKE_UP


def _handle_normal_period():
    global current_mode
    if current_mode == MODE_WOKE_UP:
        current_mode = MODE_NORMAL
        stop_sound()
        lights_off()


def confirm_wakeup():
    print('confirming wakeup')
    enter_password()
    stop_sound()
    
    try:
        successes = 0
        failures = 0
        while successes < 3 and failures < 5:
            result = memory_game()
            if result:
                successes += 1
            else:
                failures += 1
            print(f'successes {successes}, failures {failures}')
        
        if successes == 3:
            print('wakeup confirmed')
            _wakeup_confirmed()
        else:
            start_sound()
        
    except GameNotPlayed as e:
        start_sound()
    


def enter_password():
    guess = None
    for word in [0xCAFE, 0xBABE]:
        while guess != word:
            guess = pick_hex_digits(0xAAAA, 0xFFFF, stop_hex=word)
        sleep(1)
    display_blank()


def memory_game():
    display_blank()
    secret = randint(1, 9999)
    secret_str = f'{secret:04d}'
    digits = random_digits_order()
    for digit in digits:
        set_digit(digit, int(secret_str[digit]))
        sleep(0.5)
        set_digit(digit, None)
    guess = pick_dec_digits(0, 9999, stop_dec=secret, timeout_seconds=15)
    display_dec(guess)
    play_single_sound('good' if guess == secret else 'bad')
    sleep(1)
    display_blank()
    print(f'guessed {guess} while secret was {secret}')
    if guess == 0:
        raise GameNotPlayed()
    return guess == secret


def random_digits_order():
    result_list = []
    while len(result_list) < 4:
        next_digit = randint(0,3)
        if not next_digit in result_list:
            result_list.append(next_digit)
    return result_list


class GameNotPlayed(Exception):
    pass


if __name__ == '__main__':
    def simulate_confirm_wakeup():
        stop_sound()
        _wakeup_confirmed()
    
    #enter_password()
    #result = memory_game()
    #print(f'memory game success: {result}')
    #confirm_wakeup()
    
    update_wakeup(JustTime(8,30), JustTime(8,00))
    print(f'at -30 min, mode: {current_mode}, sound: {get_current_sound()}')
    update_wakeup(JustTime(8,30), JustTime(8,20))
    print(f'at -10 min, mode: {current_mode}, sound: {get_current_sound()}')
    update_wakeup(JustTime(8,30), JustTime(8,25))
    print(f'at  -5 min, mode: {current_mode}, sound: {get_current_sound()}')
    update_wakeup(JustTime(8,30), JustTime(8,29))
    print(f'at  -1 min, mode: {current_mode}, sound: {get_current_sound()}')
    
    simulate_confirm_wakeup()
    
    update_wakeup(JustTime(8,30), JustTime(8,30))
    print(f'at   0 min, mode: {current_mode}, sound: {get_current_sound()}')
    update_wakeup(JustTime(8,30), JustTime(8,31))
    print(f'at  +1 min, mode: {current_mode}, sound: {get_current_sound()}')
    
    