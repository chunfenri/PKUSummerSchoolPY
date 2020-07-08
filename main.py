import pgzrun
import pgzero
import math
import random

WIDTH = 600
HEIGHT = 1200
newBubbleIdx = 1

bubbleColor = ['red', 'yellow', 'green', 'blue']

bubblePos = [[] for i in range(20)]

activeBubble = {}


print(bubblePos)

epoch = 0


def draw():
    screen.clear()
    screen.fill((128, 0, 0))


def update():
    pass


def on_mouse_down(pos):
    pass


class bubble():
    def __init__(self, x, y):
        self.color = random.choice(bubbleColor)
        self.posx = x
        self.posy = y
        self.index = newBubbleIdx
        newBubbleIdx += 1
        activeBubble[self.index] = self

    


def init():
    pass


def traceBubble():
    pass


def BubbleHitPosition(bubble):
    pass


def judgeBubbleBoom(bubble):
    pass


def bubbleExplode(bubbleList):
    pass


sounds.background3.play()
pgzrun.go()
