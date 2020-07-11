import pgzrun
import pgzero as pg
import math
import random
import time
import numpy as np

WIDTH = 600
HEIGHT = 1000

bubbleColor = ['red', 'yellow', 'green', 'dblue']

bubblePos = [["" for _ in range(20)] for _ in range(10)]

activeBubble = {}

explodeList = []

movingLine = False
bubbleFlying = False
bubbleFlyX = 0.0
bubbleFlyY = 0.0
bubbleNowX = 0.0
bubbleNowY = 0.0
totalCount = 0

epoch = 0
bubHitNum = 0
mark = 0
musicCount = 0
bubbleExping = False


class bubble():
    def __init__(self, x, y, color=''):
        if color:
            self.color = color
        else:
            self.color = random.choice(bubbleColor)
        self.indx = x
        self.indy = y
        self.pic = Actor(self.color)
        posx, posy = index2pos(x, y)
        self.pic.center = (posx, posy)

        activeBubble[(x, y)] = self
        bubblePos[x][y] = self.color


def index2pos(indx, indy):
    rad = 30.0
    dy = rad * math.sqrt(3)
    posy = rad + dy * indy
    if epoch % 2 == 0:
        if indy % 2 == 0:
            posx = rad + 2 * rad * indx
        else:
            posx = 2 * rad + 2 * rad * indx
    else:
        if indy % 2 == 1:
            posx = rad + 2 * rad * indx
        else:
            posx = 2 * rad + 2 * rad * indx
    return (posx, posy)


def pos2index(posx, posy):
    '''主要用于bubble碰撞到别的bubble时看应该要塞到哪个位置，位置可能不是准确位置，在一个范围内都要映射到一个位置'''
    rad = 30.0
    dy = rad * math.sqrt(3)
    indy_esm = [int(posy / dy) - 1, int(posy / dy), int(posy / dy) + 1]
    indx_esm = [
        int(posx / (2 * rad)) - 1,
        int(posx / (2 * rad)),
        int(posx / (2 * rad)) + 1
    ]
    for x in indx_esm:
        for y in indy_esm:
            if x in range(10) and y in range(15):
                posx1, posy1 = index2pos(x, y)
                dist = math.sqrt((posx - posx1) * (posx - posx1) +
                                 (posy - posy1) * (posy - posy1))
                if dist <= rad:
                    return (x, y)
    return (int(posx / (2 * rad)), int(posy / dy))


def judgeConnect(A_indx, A_indy, B_indx, B_indy):
    if A_indx in range(10) and A_indy in range(15):
        if A_indy == B_indy:
            if abs(A_indx - B_indx) == 1:
                return 1
        elif abs(A_indy - B_indy) == 1:
            if epoch % 2 == 0:
                if A_indy % 2 == 0:
                    if A_indx == B_indx or A_indx - 1 == B_indx:
                        return 1
                else:
                    if A_indx == B_indx or A_indx + 1 == B_indx:
                        return 1
            else:
                if A_indy % 2 == 1:
                    if A_indx == B_indx or A_indx - 1 == B_indx:
                        return 1
                else:
                    if A_indx == B_indx or A_indx + 1 == B_indx:
                        return 1
    return 0


def explodeSearch(bubbleA):
    res = [(bubbleA.indx, bubbleA.indy)]
    global vis
    vis[bubbleA.indx][bubbleA.indy] = 1
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x = dx + bubbleA.indx
            y = dy + bubbleA.indy
            if judgeConnect(x, y, bubbleA.indx, bubbleA.indy):
                if vis[x][y] == 0:
                    vis[x][y] = 1
                    if (x, y) in activeBubble:
                        bubbleB = activeBubble[(x, y)]
                        if bubbleB.color == bubbleA.color:
                            res += explodeSearch(bubbleB)
    return res


def findExplode(bubbleA):
    '''bubbleA是撞击上的球所在位置的index值，是一个二元元组
    找到哪些球球需要爆炸，返回爆照球的下标列表。不包含爆炸后掉落的球，只考虑相同颜色的连通分量'''
    '''先传入新的球bubbleA,函数返回所有需要爆炸球的下标二元组列表.若不需爆炸则返回空表'''
    global vis
    vis = [[0 for _ in range(20)] for _ in range(10)]
    res = explodeSearch(bubbleA)
    if len(res) < 3:
        return []
    else:
        return res


def connectSearch(bubbleA):
    res = [(bubbleA.indx, bubbleA.indy)]
    global vis
    vis[bubbleA.indx][bubbleA.indy] = 1
    mk = 0
    if bubbleA.indy == 0:
        mk = 1
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x = dx + bubbleA.indx
            y = dy + bubbleA.indy
            if judgeConnect(x, y, bubbleA.indx, bubbleA.indy):
                if vis[x][y] == 0:
                    vis[x][y] = 1
                    if (x, y) in activeBubble:
                        bubbleB = activeBubble[(x, y)]
                        resB, mkB = connectSearch(bubbleB)
                        res += resB
                        mk = mk or mkB
    return [res, mk]


def findFallBubble():
    '''找到球爆炸后需要掉下来的其他球，返回值同上'''
    fallList = []
    global vis
    vis = [[0 for _ in range(20)] for _ in range(10)]
    for bubble in activeBubble.values():
        if vis[bubble.indx][bubble.indy] == 0:
            res, mk = connectSearch(bubble)
            if mk == 0:
                fallList += res
    return fallList


def explodeBubbles():
    global mark
    mark += len(explodeList)**2
    print(explodeList)

    for pos in explodeList:
        name = activeBubble[pos].color
        name += 'exp1'
        activeBubble[pos].pic.image = name
    bubbleExpStep = 1
    clock.schedule(explodeBub1, 0.1)


def explodeBub1():
    #print(explodeList)
    for pos in explodeList:
        name = activeBubble[pos].color
        name += 'exp2'
        activeBubble[pos].pic.image = name
    clock.schedule(explodeBub2, 0.1)


def explodeBub2():
    #print(explodeList)
    for pos in explodeList:
        name = activeBubble[pos].color
        name += 'exp3'
        activeBubble[pos].pic.image = name
    clock.schedule(explodeBub3, 0.1)


def explodeBub3():
    global explodeList
    #print(explodeList)
    for pos in explodeList:
        del activeBubble[pos]
    explodeList.clear()
    explodeList = findFallBubble()
    if explodeList:
        explodeBubbles()
    else:
        global bubbleFlying, bubbleExping
        bubbleFlying = False
        bubbleExping = False


def game_end():
    for x in range(10):
        for y in range(15):
            if (x, y) in activeBubble:
                return 1
    return 0


def generateLine():

    global activeBubble, epoch
    if epoch % 2:
        lineNum = 10
    else:
        lineNum = 9
    epoch += 1

    dic = {}
    for orgKey in activeBubble.keys():
        newKey = list(orgKey)
        newKey[1] += 1
        newKey = tuple(newKey)
        newValue = activeBubble[orgKey]
        dic[newKey] = newValue

    activeBubble = dic
    for val in dic.values():
        val.indy += 1
        posx, posy = index2pos(val.indx, val.indy)
        val.pic.center = (posx, posy)

    for i in range(lineNum):
        activeBubble[(i, 0)] = bubble(i, 0)

    if epoch == 10:
        bubbleColor.append('orange')

    if epoch == 25:
        bubbleColor.append('lblue')

    if epoch == 45:
        bubbleColor.append('purple')

    return False


def draw():
    screen.clear()
    screen.fill((0, 100, 0))

    newBub.draw()
    for bubble in activeBubble.values():
        bubble.pic.draw()


updating = 0
bubbleLock = 0


def update():
    rad = 30
    global bubbleFlying, bubbleExping, totalCount, updating
    if bubbleExping:
        return
    if updating:
        return
    updating = 1
    totalCount += 1
    #print(totalCount)
    if bubbleFlying:
        global bubbleFlyX, bubbleFlyY, bubbleNowX, bubbleNowY, newBub, newBubColor, bubbleLock
        bubbleNowX -= bubbleFlyX
        bubbleNowY -= bubbleFlyY
        if bubbleNowX < 30 or bubbleNowX > 570:
            bubbleFlyX = -bubbleFlyX

        newBub.center = (bubbleNowX, bubbleNowY)
        if bubbleNowY < 950:
            idxX, idxY = pos2index(bubbleNowX, bubbleNowY)
            neiborList = []
            for i in range(-1, 2):
                for j in (-1, 0):
                    if judgeConnect(idxX + i, idxY + j, idxX, idxY):
                        if (idxX + i, idxY + j) in activeBubble:
                            neiborList.append((idxX + i, idxY + j))

            if neiborList:
                minOne = neiborList[0]
                x0, y0 = index2pos(minOne[0], minOne[1])
                minDis = (bubbleNowX - x0)**2 + (bubbleNowY - y0)**2
                for neighbor in neiborList[1:]:
                    x0, y0 = index2pos(neighbor[0], neighbor[1])
                    Dis = (bubbleNowX - x0)**2 + (bubbleNowY - y0)**2
                    if Dis < minDis:
                        minDis = Dis

                if not bubbleLock and math.sqrt(minDis) <= 2 * rad:
                    bubbleLock = 1
                    a = bubble(idxX, idxY, newBubColor)
                    newBubColor = random.choice(bubbleColor)
                    del newBub
                    newBub = Actor(newBubColor)
                    newBub.center = (300, 950)
                    bubbleNowX = 300
                    bubbleNowY = 950
                    bubbleFlying = 0

                    global explodeList
                    explodeList = findExplode(a)
                    if len(explodeList) >= 3:
                        bubbleExping = True
                        explodeBubbles()
                        updating = 0
                        bubbleLock = 0
                    else:
                        explodeList.clear()
                    global bubHitNum
                    bubHitNum += 1
                    if bubHitNum % 4 == 0:
                        generateLine()
                    bubbleLock = 0
    updating = 0
    #print(totalCount)


def on_mouse_down(pos):
    posx, posy = pos
    global bubbleFlying
    if posy < 920 and bubbleFlying == False and bubbleExping == False:
        posx -= 300
        posy = 950 - posy
        global bubbleFlyX, bubbleFlyY, bubbleNowX, bubbleNowY
        bubbleFlyX = -math.sin(math.atan(posx / posy)) * 20
        bubbleFlyY = math.cos(math.atan(posx / posy)) * 20
        bubbleNowX = 300.0
        bubbleNowY = 950.0
        bubbleFlying = True


def on_music_end():
    global musicCount
    musicCount += 1
    if musicCount % 3 == 1:
        music.play_once('background2')

    elif musicCount % 3 == 2:
        music.play_once('background3')

    else:
        music.play_once('background1')


music.play_once('background1')

for j in range(3):
    for i in range(9):
        a = bubble(i, j)
        a.pic.center = index2pos(i, j)
    if j % 2 == 0:
        a = bubble(9, j)
        a.pic.center = index2pos(9, j)

for i in range(9):
    if random.randint(0, 3):
        a = bubble(i, 3)
        a.pic.center = index2pos(i, 3)

startTime = time.time()
newBubColor = random.choice(bubbleColor)
newBub = Actor(newBubColor)
newBub.pos = (300, 950)
bubbleNowX = 300
bubbleNowY = 950
pgzrun.go()
