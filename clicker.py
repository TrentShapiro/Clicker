import pyautogui as pag
import numpy as np
from random import randrange as rrange
import math
import multiprocessing
from pynput import keyboard
# import multiprocessing
# import time
# import pyHook, pyautogui, pythoncom
# import queue

# Setup pyautogui constants
pag.MINIMUM_DURATION = 0  # Default: 0.1
pag.MINIMUM_SLEEP = 0  # Default: 0.05
pag.PAUSE = 0  # Default: 0.1


class Clicker(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            try:
                task = self.queue.get(block=False)
                if task == "Start":
                    print("moving")
                    mouse_square()

            except task == "Exit":
                print("ending")
                self.queue.task_done()
                break
        return


def rotate_x(x, y, xo, yo, theta):
    xr = math.cos(theta) * (x - xo) - math.sin(theta) * (y - yo) + xo
    return xr


def rotate_y(x, y, xo, yo, theta):
    yr = math.sin(theta) * (x - xo) - math.cos(theta) * (y - yo) + yo
    return yr


def mouse_square():
    x_rel = 500
    y_rel = 0

    x1, y1 = pag.position()  # Starting position
    x2, y2 = x1 + x_rel, y1 + y_rel  # Destination

    x_mid = x1 + 250
    y_mid = y1 + 250

    p_size = int(np.floor((abs(x_rel) + abs(y_rel))/4))
    p_x = np.linspace(x1, x2, p_size)
    p_y = np.linspace(y1, y2, p_size)

    rand_max = 20
    p_y_rand = []
    for a in range(0, len(p_y)):
        if a % 2 == 0:
            p_y_rand.append(p_y[a] + rrange(-rand_max, 0, 1))

        if a % 2 == 1:
            p_y_rand.append(p_y[a] + rrange(0, rand_max, 1))

    z = np.polyfit(p_x, p_y_rand, 10)
    f = np.poly1d(z)

    p_x_smooth = p_x
    p_y_smooth = f(p_x_smooth)

    # top right to top left
    p_x_1 = p_x
    p_y_1 = p_y_smooth

    p_x_2 = []
    p_y_2 = []
    for p in range(0, len(p_x_1)):
        p_x_2.append(rotate_x(p_x_1[p], p_y_1[p], x_mid, y_mid, math.pi / 2))
        p_y_2.append(rotate_y(p_x_1[p], p_y_1[p], x_mid, y_mid, math.pi / 2))

    p_x_3 = np.flip(p_x_1)
    p_y_3 = p_y_1 + 500
    p_x_4 = np.array(p_x_2) - 500
    p_y_4 = np.flip(p_y_2)

    # corner smoothing
    smooth_points = 2
    p_x_1_5 = np.linspace(p_x_1[-1], p_x_2[0], smooth_points)
    p_x_2_5 = np.linspace(p_x_2[-1], p_x_3[0], smooth_points)
    p_x_3_5 = np.linspace(p_x_3[-1], p_x_4[0], smooth_points)
    p_x_4_5 = np.linspace(p_x_4[-1], p_x_1[0], smooth_points)
    p_y_1_5 = np.linspace(p_y_1[-1], p_y_2[0], smooth_points)
    p_y_2_5 = np.linspace(p_y_2[-1], p_y_3[0], smooth_points)
    p_y_3_5 = np.linspace(p_y_3[-1], p_y_4[0], smooth_points)
    p_y_4_5 = np.linspace(p_y_4[-1], p_y_1[0], smooth_points)

    p_x_total = np.concatenate((p_x_1, p_x_1_5, p_x_2, p_x_2_5, p_x_3, p_x_3_5, p_x_4, p_x_4_5))
    p_y_total = np.concatenate((p_y_1, p_y_1_5, p_y_2, p_y_2_5, p_y_3, p_y_3_5, p_y_4, p_y_4_5))

    # top left to bottom left
    for r in range(0, len(p_x_total)):
        pag.moveTo(p_x_total[r]
                   , p_y_total[r]
                   , 0
                   , pag.easeInCubic)


def on_press(key):
    if key.char == '[':
        print('[ key read')
        # queue.put("Start")
        # queue.join()


def on_release(key):
    if key.char == ']':
        # queue.put("Exit")
        # queue.join()
        # Stop listener
        return False


if __name__ == '__main__':
    # Establish communication queues
    queue = multiprocessing.JoinableQueue()
    # create a hook manager]
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

Clicker.run(self)
