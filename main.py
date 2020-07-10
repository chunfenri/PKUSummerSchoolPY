import pgzrun
import pgzero as pg
import math
import random
import time
import numpy as np

WIDTH = 600
HEIGHT = 1300


bubbleColor = ['red', 'yellow', 'green', 'dblue']

bubblePos = [["" for _ in range(10)] for _ in range(20)]

activeBubble = {}

movingLine = False
bubbleFlying = False
bubbleFlyX = 0.0
bubbleFlyY = 0.0
bubbleNowX = 0.0
bubbleNowY = 0.0

epoch = 0
bubHitNum = 0
mark = 0


class bubble():
    def __init__(self, x, y, color=''):
        if color:
            self.color = color
        else:
            self.color = random.choice(bubbleColor)
        self.indx = x
        self.indy = y
        self.pic = Actor(self.color)
        pixy, pixx = index2pos(y, x)
        self.pic.pos = (-60, pixx)

        activeBubble[(y, x)] = self
        bubblePos[y][x] = self.color


def index2pos(indx, indy):
    rad = 30
    dy = rad * math.sqrt(3)
    y_pixel = rad + dy * indy
    if indy % 2 == 0:
        x_pixel = rad + 2 * rad * indx
    else:
        x_pixel = 2 * rad + 2 * rad * indx
    posy = y_pixel / 1200
    posx = x_pixel / 600
    return (posx, posy)


def index2pos_pixel(indx, indy):
    rad = 30
    dy = rad * math.sqrt(3)
    y_pixel = rad + dy * indy
    if indy % 2 == 0:
        x_pixel = rad + 2 * rad * indx
    else:
        x_pixel = 2 * rad + 2 * rad * indx
    return (x_pixel, y_pixel)


def pos2index(posy, posx):
    '''主要用于bubble碰撞到别的bubble时看应该要塞到哪个位置，位置可能不是准确位置，在一个范围内都要映射到一个位置'''
    rad = 30
    dy = rad * math.sqrt(3)
    y_pixel = posy * 1200
    x_pixel = posx * 600
    indy_esm = [
        int(y_pixel / dy) - 1,
        int(y_pixel / dy),
        int(y_pixel / dy) + 1
    ]
    indx_esm = [
        int(x_pixel / (2 * rad)) - 1,
        int(x_pixel / (2 * rad)),
        int(x_pixel / (2 * rad)) + 1
    ]
    for x in indx_esm:
        for y in indy_esm:
            if x in range(10) and y in range(23):
                x1_pixel, y1_pixel = index2pos_pixel(x, y)
                dist = math.sqrt((x_pixel - x1_pixel) * (x_pixel - x1_pixel) +
                                 (y_pixel - y1_pixel) * (y_pixel - y1_pixel))
                if dist <= rad:
                    return (x, y)


def judgeConnect(A_indx, A_indy, B_indx, B_indy):
    if A_indy == B_indy:
        if abs(A_indx - B_indx) == 1:
            return 1
    elif abs(A_indy - B_indy) == 1:
        if A_indy % 2 == 0:
            if A_indx == B_indx or A_indx - 1 == B_indx:
                return 1
        else:
            if A_indx == B_indx or A_indx + 1 == B_indx:
                return 1


def explodeSearch(vis, bubbleA):
    res = [(bubbleA.indx, bubbleA.indy)]
    vis[bubbleA.indx][bubbleA.indy] = 1
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x = dx + bubbleA.indx
            y = dy + bubbleA.indy
            if vis[x][y] == 0 and judgeConnect(x, y, bubbleA.indx,
                                               bubbleA.indy):
                if (x, y) in activeBubble:
                    bubbleB = activeBubble[(x, y)]
                    if bubbleB.color == bubbleA.color:
                        res += explodeSearch(vis, bubbleB)
    if len(res) >= 3:
        return res
    else:
        return []


def findExplode(bubbleA):
    '''bubbleA是撞击上的球所在位置的index值，是一个二元元组
    找到哪些球球需要爆炸，返回爆照球的下标列表。不包含爆炸后掉落的球，只考虑相同颜色的连通分量'''
    '''先传入新的球bubbleA,函数返回所有需要爆炸球的下标二元组列表.若不需爆炸则返回空表'''
    vis = [[0 for _ in range(10)] for _ in range(20)]
    return explodeSearch(vis, bubbleA)


def connectSearch(vis, bubbleA):
    res = [(bubbleA.indx, bubbleA.indy)]
    vis[bubbleA.indx][bubbleA.indy] = 1
    mark = 0
    if bubbleA.indy == 0:
        mark = 1
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x = dx + bubbleA.indx
            y = dy + bubbleA.indy
            if vis[x][y] == 0 and judgeConnect(x, y, bubbleA.indx,
                                               bubbleA.indy):
                if (x, y) in activeBubble:
                    bubbleB = activeBubble[(x, y)]
                    resB, markB = explodeSearch(vis, bubbleB)
                    res += resB
                    mark = mark or markB
    return [res, mark]


def findFallBubble():
    '''找到球爆炸后需要掉下来的其他球，返回值同上'''
    fallList = []
    vis = [[0 for _ in range(10)] for _ in range(20)]
    for bubble in activeBubble.values():
        if vis[bubble.indx][bubble.indy] == 0:
            res, mark = connectSearch(vis, bubble)
            if mark == 0:
                fallList += res
    return fallList


def explodeBubbles(explodeList):
    pass

def generateLine():
    for i in bubblePos[19]:
        if i:
            return True

    for i in range(19):
        for j in range(10):
            bubblePos[i + 1][j] = bubblePos[i][j]

    key, value = [], []

    for keys in activeBubble:
        newKey = list(key)
        newKey[0] += 1
        newKey = tuple(newKey)
        key.append(newKey)

        newValue = activeBubble[keys]
        newValue.indy += 1
        value.append(newValue)

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

    global movingLine
    movingLine = True

    if epoch == 5:
        bubbleColor.append('purple')

    if epoch == 15:
        bubbleColor.append('orange')

    if epoch == 35:
        bubbleColor.append('lblue')

    return False


def draw():
    screen.clear()
    screen.fill((128, 255, 0))

    newBub.draw()
    for bubble in activeBubble.values():
        bubble.pic.draw()

    if time.time() - startTime < 1:
        global epoch
        print(bubblePos, epoch)
        print(activeBubble)
        epoch += 1


def update():
    global movingLine, bubbleFlying
    if movingLine:
        for bubbles in activeBubble.values():
            bubbles.pic.down += 5
        if activeBubble.values[0].posy == activeBubble.values[0].down:
            movingLine = False

    if bubbleFlying:
        global bubbleFlyX, bubbleFlyY, bubbleNowX, bubbleNowY
        bubbleNowX += bubbleFlyX
        bubbleNowY += bubbleFlyY
        if bubbleNowX < 30 or bubbleNowX > 150:
            bubbleFlyX = -bubbleFlyX

        newBub.left += bubbleNowX - newBub.left
        newBub.up += bubbleNowY - newBub.up
        idxX, idxY = pos2index(bubbleNowX, bubbleNowY)
        neiborList = []
        for i in range(-1, 2):
            for j in (-1, 0):
                if bubblePos[idxY+j][idxX+i]:
                    neiborList.append((idxY+j, idxX+i))

        if neiborList:
            minOne = neiborList[0]
            x0, y0 = index2pos(minOne)
            minDis = (bubbleNowX - x0) ** 2 + (bubbleNowY - y0) ** 2
            for neighbor in neiborList[1:]:
                x0, y0 = index2pos(neighbor)
                Dis = (bubbleNowX - x0) ** 2 + (bubbleNowY - y0) ** 2
                if Dis < minDis:
                    minOne = neighbor
                    minDis = Dis

            a = bubble(minOne[0], minOne[1], newBubColor)
            explodeList = findExplode(a)
            if explodeList:
                explodeBubbles(explodeList)

            bubbleFlying = False
            bubHitNum += 1

            if bubHitNum % 4 == 0:
                if generateLine():
                    game_end()
                

            


def on_mouse_down(pos):
    posx, posy = pos
    global bubbleFlying
    if posy < 1240 and bubbleFlying == False:
        posx -= 300
        posy = 1250 - posy
        global bubbleFlyX, bubbleFlyY
        bubbleFlyX = math.cos(math.atan(posy/posx)) * 10
        bubbleFlyY = -math.sin(math.atan(posy/posx)) * 10
        bubbleNowX = 300.0
        bubbleNowY = 1250.0
        bubbleFlying = True


sounds.background3.play()
for i in range(10):
    a = bubble(i, 0)
    a.pic.topleft = index2pos(i, 0)

startTime = time.time()
newBubColor = random.choice(bubbleColor)
newBub = Actor(newBubColor)
newBub.pos = (300, 1250)
pgzrun.go()
