import board
from digitalio import DigitalInOut, Direction
from time import sleep

# controls to select mode work only within 60ms after powering on sound board
# but pico and python code is to slow to set the mode during boot, it's too late
con1 = DigitalInOut(board.GP28) 
con2 = DigitalInOut(board.GP27)
con3 = DigitalInOut(board.GP26)
#con1.direction = Direction.OUTPUT
#con2.direction = Direction.OUTPUT
#con3.direction = Direction.OUTPUT
#con1.value = 0
#con2.value = 0
#con3.value = 0

snd1 = DigitalInOut(board.GP9)
snd2 = DigitalInOut(board.GP8)
snd3 = DigitalInOut(board.GP7)
snd1.direction = Direction.OUTPUT
snd2.direction = Direction.OUTPUT
snd3.direction = Direction.OUTPUT
snd1.value = 1
snd2.value = 1
snd3.value = 1


sound_outputs = {
    'off':    (1, 1, 1),
    'silent': (1, 1, 0), # 1
    'good':   (1, 0, 1), # 2
    'bad':    (1, 0, 0), # 3
    'gentle': (0, 1, 1), # 4
    'strong': (0, 1, 0), # 5
    'alarm':  (0, 0, 1), # 6
}

def drive_outputs(sound):
    output = sound_outputs[sound]
    snd3.value = output[0]
    snd2.value = output[1]
    snd1.value = output[2]


current_sound = None
is_playing = False


def set_current_sound(sound):
    global current_sound
    if current_sound != sound:
        print(f'setting current sound to: {sound}')
        current_sound = sound
        if is_playing and current_sound != None:
            drive_outputs(current_sound)
        

def get_current_sound():
    global current_sound
    return current_sound


def start_sound():
    global current_sount, is_playing
    print(f'starting sound: {current_sound}')
    drive_outputs(current_sound)
    is_playing = True


def stop_sound():
    global current_sound, is_playing
    print(f'stoping sound: {current_sound}')
    drive_outputs('silent')
    sleep(0.020)
    drive_outputs('off')
    is_playing = False
    
    
def play_single_sound(sound):
    print(f'playing sound: {sound}')
    drive_outputs(sound)
    sleep(0.020)
    drive_outputs('off')
    

if __name__ == '__main__':
    set_current_sound('gentle')
    sleep(3)
    start_sound()
    sleep(10)
    set_current_sound('strong')
    sleep(10)
    set_current_sound('alarm')
    sleep(10)
    stop_sound()
    sleep(3)
    play_single_sound('good')
    sleep(3)
    play_single_sound('bad')
    sleep(3)
    start_sound()
    sleep(3)
    stop_sound()
    set_current_sound(None)
