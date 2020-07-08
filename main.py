import pgzrun
import pgzero
import math
import random

WIDTH = 600
HEIGHT = 1200


BubbleColor = ['red', 'yellow', 'green', 'blue']

epoch = 0

def draw():
    screen.clear()
    screen.fill((128,0,0))



class bubble():
    color = random.choice(BubbleColor)
    posx = 0
    posy = 0



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


sounds.background1.play()
pgzrun.go()
