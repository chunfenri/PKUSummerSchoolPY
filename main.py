import pgzrun
import pgzero as pg
import math
import random
import time

WIDTH = 600
HEIGHT = 1200


bubbleColor = ['red', 'yellow', 'green', 'dblue']

bubblePos = [["" for _ in range(10)] for _ in range(20)]

activeBubble = {}

movingLine = False


class bubble():
    def __init__(self, x, y):
        self.color = random.choice(bubbleColor)
        self.indx = x
        self.indy = y
        self.pic = Actor(self.color)

        activeBubble[(y, x)] = self
        bubblePos[y][x] = self.color


def index2pos(indx, indy):
    rad = 30
    dx = rad * math.sqrt(3)
    x_pixel = rad + dx * indx
    if indx % 2 == 0:
        y_pixel = rad + 2 * rad * indy
    else:
        y_pixel = 2 * rad + 2 * rad * indy
    posx = x_pixel / 1200
    posy = y_pixel / 600
    return (posx, posy)


def index2pos_pixel(indx, indy):
    rad = 30
    dx = rad * math.sqrt(3)
    x_pixel = rad + dx * indx
    if indx % 2 == 0:
        y_pixel = rad + 2 * rad * indy
    else:
        y_pixel = 2 * rad + 2 * rad * indy
    return (x_pixel, y_pixel)


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


def generateLine():
    for i in bubblePos[19]:
        if i != '':
            return False

    for i in range(19):
        for j in range(10):
            bubblePos[i + 1][j] = bubblePos[i][j]

    key, value = [], []
    for keys in activeBubble:
        newkey = list(key)
        newkey[0] += 1
        newkey = tuple(newkey)
        key.append(newkey)
        value.append(activeBubble[keys])

    activeBubble.clear()
    activeBubble.fromkeys(key, value)

    global epoch
    if epoch % 2:
        lineNum = 9
    else:
        lineNum = 10
    epoch += 1

    for i in range(lineNum):
        bubble(i, 0)
    return True


def draw():
    screen.clear()
    screen.fill((128, 0, 0))
    actor.draw()
    for bubble in activeBubble.values():
        bubble.pic.draw()

    if(time.time()-startTime < 1):
        global epoch
        print(bubblePos, epoch)
        print(activeBubble)
        epoch += 1


def update():
    global movingLine
    if movingLine:
        for bubbles in activeBubble.values():
            


def on_mouse_down(pos):
    pass


epoch = 0
sounds.background3.play()
a = bubble(0, 0)
a.pic.topleft = index2pos(0, 0)
startTime = time.time()
pgzrun.go()
