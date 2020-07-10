import pgzrun
import pgzero as pg
import math
import random
import time
import numpy as np

HEIGHT = 200
WIDTH = 200


def draw():
    screen.clear()
    screen.fill((128, 255, 0))


def on_mouse_down(pos):

    print(pos)


pgzrun.go()
