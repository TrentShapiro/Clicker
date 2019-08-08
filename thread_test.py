import math
import time
import multiprocessing
import pyautogui as pag
import numpy as np
from random import randrange as rrange
from pynput import keyboard


def rotate_x(x, y, xo, yo, theta):
    xr = math.cos(theta) * (x - xo) - math.sin(theta) * (y - yo) + xo
    return xr


def rotate_y(x, y, xo, yo, theta):
    yr = math.sin(theta) * (x - xo) - math.cos(theta) * (y - yo) + yo
    return yr


def mouse_square():
    #print(1)
    print(pag.position())
    time.sleep(1)


def run_mouse():
    while True:
        mouse_square()
        time.sleep(1)


def on_press(key):
    try:
        press = key.char
    except AttributeError:
        press = key

    if press == '[':
        if not processes[-1].is_alive():
            try:
                processes[-1].start()
            except AssertionError:
                if processes[-1] is not None:
                    print('Restarting')
                    processes[-1].terminate()
                    new_process = multiprocessing.Process(target=run_mouse, args=())
                    processes[-1] = new_process
                    new_process.start()


def on_release(key):
    try:
        press = key.char
    except AttributeError:
        press = key

    if press == ']':
        print('Stop')
        if processes[-1].is_alive():
            processes[-1].terminate()

    if press == keyboard.Key.esc:
        print('Exit')
        return False


process1 = multiprocessing.Process(target=run_mouse, args=())

processes = [process1]

print(processes[-1])


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# process1 = multiprocessing.Process(target=run_add1, args=())
# process1.start()

# process1.terminate()[][

# process2 = multiprocessing.Process(target=run_add2, args=())
# process2.start()
# process1.join()

# while process1.is_alive():
#     time.sleep(2)
#     print('running...')

# if not process1.is_alive():
#     process1.terminate()
#     process1 = multiprocessing.Process(target=run_add1, args=())
#     process1.start()


