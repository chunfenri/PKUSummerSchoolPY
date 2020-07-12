import pgzrun
import pgzero as pg
import math
import random
import numpy as np

WIDTH = 600
HEIGHT = 1000

bubbleColor = ['red', 'yellow', 'green', 'dblue']


activeBubble = {}

activeBubbleCnt = {}

explodeList = []

explodeListCnt = []

bubbleFlyX = 0.0
bubbleFlyY = 0.0
bubbleNowX = 0.0
bubbleNowY = 0.0



epoch = 0
bubHitNum = 0
mark = 0
newmark = 0
musicCount = 0

updating = False
bubbleLock = False
movingLine = False
bubbleFlying = False
bubbleExping = False
gameEnd = False
gameEndFinish = False

bubbleCnt = 0


class bubble():
    def __init__(self, x, y, color=''):
        global bubbleCnt
        if color:
            self.color = color
        else:
            self.color = random.choice(bubbleColor)
        self.indx = x
        self.indy = y
        self.pic = Actor(self.color)
        posx, posy = index2pos(x, y)
        self.pic.center = (posx, posy)
        self.cnt = bubbleCnt
        activeBubbleCnt[bubbleCnt] = self
        bubbleCnt += 1
        activeBubble[(x, y)] = self


def index2pos(indx, indy):
    '''
    坐标转换函数,将行列坐标转换为窗口位置坐标
    不同epoch下第一行可能有9个或10个泡泡,因此转换过程不一定相同
    '''
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
    '''
    坐标转换函数,将一定范围内的窗口位置坐标转换为行列坐标
    主要用于bubble碰撞到别的bubble时看应该要塞到哪个位置，位置可能不是准确位置，在一个范围内都要映射到一个位置
    '''
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
    '''
    给定两对行列坐标(A_indx, A_indy)和(B_indx, B_indy),判断两个泡泡是否相邻.
    与之前的坐标转换函数一样,不同epoch下判断程序不同
    '''
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
    '''
    深度优先搜索,把全体泡泡看出一个节点染色图,寻找颜色相同且连通的节点.
    '''
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
    '''
    找到哪些球球需要爆炸,返回会爆炸球的下标列表.不包含爆炸后掉落的球.
    参数为新的球bubbleA,函数返回所有需要爆炸球的坐标二元组列表.若不需爆炸则返回空表.
    '''
    global vis
    vis = [[0 for _ in range(20)] for _ in range(10)]
    res = explodeSearch(bubbleA)
    if len(res) < 3:
        return []
    else:
        return res


def connectSearch(bubbleA):
    '''
    深度优先搜索,把全体泡泡看成一个图,枚举其连通分量,并标记这个连通分量是否有在第0行的节点.
    返回值res是连通分量内节点的坐标列表,mk是一个标记,mk==1当且仅当这个连通分量有在第0行的节点.
    '''
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
    '''
    找到球爆炸后需要掉落的球,返回值同上.
    '''
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
    '''
    球爆炸开始时的逻辑与动画效果（第一帧）
    '''
    global newmark, explodeListCnt, explodeList
    newmark = len(explodeList) ** 2
    if newmark >= 64:
        sounds.bonus1.play()
    sounds.eliminate2.play()
    for ct in explodeListCnt:
        name = activeBubbleCnt[ct].color
        name += 'exp1'
        activeBubbleCnt[ct].pic.image = name
    bubbleExpStep = 1
    clock.schedule(explodeBub1, 0.1)


def explodeBub1():
    '''
    球爆炸的动画效果（第二帧）
    '''
    global explodeListCnt
    for ct in explodeListCnt:
        name = activeBubbleCnt[ct].color
        name += 'exp2'
        activeBubbleCnt[ct].pic.image = name
    clock.schedule(explodeBub2, 0.1)


def explodeBub2():
    '''
    球爆炸的动画效果（第三帧）
    '''
    global explodeListCnt
    for ct in explodeListCnt:
        name = activeBubbleCnt[ct].color
        name += 'exp3'
        activeBubbleCnt[ct].pic.image = name
    clock.schedule(explodeBub3, 0.1)


def explodeBub3():
    '''
    球爆炸的结束逻辑与音效
    '''
    global explodeList, explodeListCnt, mark, newmark
    sounds.eliminate3.play()
    mark += newmark
    for ct in explodeListCnt:
        de = activeBubbleCnt[ct]
        del activeBubble[(de.indx, de.indy)]
        del de

    explodeList.clear()
    explodeListCnt.clear()
    explodeList = findFallBubble()
    for item in explodeList:
        explodeListCnt.append(activeBubble[item].cnt)
    if explodeList:
        sounds.eliminate4.play()
        explodeBubbles()
    else:
        global bubbleExping
        bubbleExping = False


def game_end():
    '''
    游戏结束开始时的逻辑用户音效，以及动画效果（第一帧）
    '''
    global bubbleFlying, gameEnd
    bubbleFlying = False
    gameEnd = True
    music.pause()
    sounds.explode.play()
    for item in activeBubble.values():
        name = item.color
        name += 'exp1'
        item.pic.image = name

    name = newBubColor
    name += 'exp1'
    newBub.image = name
    clock.schedule(game_end1, 0.2)


def game_end1():
    '''
    游戏结束动画效果（第二帧）
    '''
    for item in activeBubble.values():
        name = item.color
        name += 'exp2'
        item.pic.image = name

    name = newBubColor
    name += 'exp2'
    newBub.image = name
    clock.schedule(game_end2, 0.3)


def game_end2():
    '''
    游戏结束动画效果（第三帧）
    '''
    for item in activeBubble.values():
        name = item.color
        name += 'exp3'
        item.pic.image = name

    name = newBubColor
    name += 'exp3'
    newBub.image = name
    clock.schedule(game_end3, 0.4)


def game_end3():
    '''
    游戏结束完成时的逻辑与音效
    '''
    global gameEndFinish
    gameEndFinish = True
    global activeBubble
    del activeBubble
    sounds.gg.play()


def generateLine():
    '''
    生成新的行,所有现有的泡泡下移一列,并在第0行生成一行新的泡泡.
    主要涉及到全局字典activeBubble元素的更新.
    '''
    global activeBubble, epoch
    for i in range(10):  # 若在没生成球时，最下面一行已经有球，则直接返回true,被update函数捕获执行游戏结束。
        if (i, 14) in activeBubble:
            return True

    if epoch % 2:  # 由于球是密堆积，相邻行球数不一样，所以按照行数来确定生成10个或9个新球
        lineNum = 10
    else:
        lineNum = 9
    epoch += 1

    dic = {}
    for orgKey in activeBubble.keys():  # 每个已有球下移一格
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

    for i in range(lineNum):  # 生成新球
        activeBubble[(i, 0)] = bubble(i, 0)

    if epoch == 10:  # 根据游戏进行情况加入新球色
        bubbleColor.append('orange')

    if epoch == 25:
        bubbleColor.append('lblue')

    if epoch == 45:
        bubbleColor.append('purple')

    return False


def draw():
    screen.clear()
    screen.blit('3', (0, 0))  # 一共有三张背景图，分别为'1','2','3'，可以更换背景
    screen.draw.text('score:', (380, 940), color='#FFAAAA', fontsize=40)
    screen.draw.text(str(mark), (480, 935),
                     color='#FFAAFF', gcolor='#FFFFAA', fontsize=60)  # 显示得分

    screen.draw.filled_circle(
        (150, 950), 20, switchColor(nextBubColor))  # 画提示球

    if gameEndFinish == False:
        newBub.draw()
        for bubble in activeBubble.values():
            bubble.pic.draw()
    else:
        screen.draw.text('GAME OVER', (95, 450), color='#FF6600', fontsize=100)


def switchColor(name):
    '''
    颜色名称到RGB值的映射
    '''
    if name == 'red':
        return (255, 40, 40)
    if name == 'yellow':
        return (255, 255, 0)
    if name == 'dblue':
        return (0, 0, 255)
    if name == 'green':
        return (60, 255, 60)
    if name == 'orange':
        return (255, 150, 0)
    if name == 'lblue':
        return (150, 150, 255)
    return (255, 50, 255)


def update():
    rad = 30
    global bubbleFlying, bubbleExping, updating, gameEnd
    if bubbleExping or updating or gameEnd:  # 在异步调用的函数没有返回前，或上一个update函数没有返回前不进行下一步update逻辑
        return  # 避免因为多线程竞争（不同的线程修改对象的参数）导致的程序逻辑问题
    updating = True

    if bubbleFlying:
        global bubbleFlyX, bubbleFlyY, bubbleNowX, bubbleNowY, newBub, newBubColor, nextBubColor, bubbleLock, bubHitNum
        bubbleNowX -= bubbleFlyX  # 利用两个全局浮点数来存储泡泡的准确位置，防止舍入误差的累积
        bubbleNowY -= bubbleFlyY

        if bubbleNowX < 30:  # 实现触边反弹效果，在触边时改变x轴飞行速度分量的方向
            bubbleFlyX = -bubbleFlyX
            bubbleNowX = 60 - bubbleNowX
        if bubbleNowX > 570:
            bubbleFlyX = -bubbleFlyX
            bubbleNowX = 1140 - bubbleNowX

        newBub.center = (bubbleNowX, bubbleNowY)
        if bubbleNowY < 950:  # 进入网格部分后每次更新位置都查看此位置周围是否有其他泡泡
            idxX, idxY = pos2index(bubbleNowX, bubbleNowY)
            neiborList = []
            for i in range(-1, 2):
                for j in (-1, 0):
                    if judgeConnect(idxX + i, idxY + j, idxX, idxY):
                        if (idxX + i, idxY + j) in activeBubble:
                            neiborList.append((idxX + i, idxY + j))

            if idxY == 0 and len(neiborList) == 0:  # 防止球从全图的最上方的空白部分飞出去
                a = bubble(idxX, idxY, newBubColor)
                newBubColor = nextBubColor
                nextBubColor = random.choice(bubbleColor)
                del newBub
                newBub = Actor(newBubColor)
                newBub.center = (300, 950)
                bubbleNowX = 300
                bubbleNowY = 950
                bubbleFlying = False

                bubHitNum += 1
                if bubHitNum % 4 == 0:
                    generateLine()
                bubbleLock = False
                updating = False
                return

            if neiborList:
                if bubbleNowY > 910:  # 若邻接有球且球的位置很靠下则游戏结束
                    game_end()
                    return
                minOne = neiborList[0]  # 寻找相邻球中最进的球
                x0, y0 = index2pos(minOne[0], minOne[1])
                minDis = (bubbleNowX - x0)**2 + (bubbleNowY - y0)**2
                for neighbor in neiborList[1:]:
                    x0, y0 = index2pos(neighbor[0], neighbor[1])
                    Dis = (bubbleNowX - x0)**2 + (bubbleNowY - y0)**2
                    if Dis < minDis:
                        minDis = Dis

                if (not bubbleLock and math.sqrt(minDis) <= 2 * rad) or idxY == 0:  # 判断本球与距离最近球是否碰撞
                    bubbleLock = True
                    # 在碰撞位置生成一个一模一样的bubble对象
                    a = bubble(idxX, idxY, newBubColor)
                    newBubColor = nextBubColor  # 更新newBub对象与提示颜色
                    nextBubColor = random.choice(bubbleColor)
                    del newBub
                    newBub = Actor(newBubColor)
                    newBub.center = (300, 950)
                    bubbleNowX = 300
                    bubbleNowY = 950
                    bubbleFlying = False

                    global explodeList, explodeListCnt, epoch
                    explodeList = findExplode(a)
                    for item in explodeList:
                        explodeListCnt.append(activeBubble[item].cnt)

                    if len(explodeList) >= 3:  # 若碰撞点颜色一样的球超过三个就爆炸
                        bubbleExping = True
                        orgEpoch = epoch
                        explodeBubbles()
                        updating = False
                        bubbleLock = False
                    else:
                        explodeList.clear()  # 若无则清空列表

                    bubHitNum += 1
                    if bubHitNum % 5 == 0:  #每打5个球生成一行新球
                        if generateLine():  #若生成球之前最下面的行已经有球就结束游戏
                           game_end()

                    bubbleLock = False
    updating = False


def on_mouse_down(pos):
    posx, posy = pos
    global bubbleFlying, bubbleExping, gameEnd
    if posy < 920 and bubbleFlying == False and bubbleExping == False and gameEnd == False:
        sounds.eliminate1.play()
        posx -= 300
        posy = 950 - posy
        global bubbleFlyX, bubbleFlyY, bubbleNowX, bubbleNowY
        bubbleFlyX = -math.sin(math.atan(posx / posy)) * 20  # 允许情况下的鼠标点击会设置飞行速度，并设置标志变量
        bubbleFlyY = math.cos(math.atan(posx / posy)) * 20
        bubbleNowX = 300.0
        bubbleNowY = 950.0
        bubbleFlying = True


def on_music_end():
    global musicCount  # 三首歌轮播
    musicCount += 1
    if musicCount % 3 == 1:
        music.play_once('background2')

    elif musicCount % 3 == 2:
        music.play_once('background3')

    else:
        music.play_once('background1')


music.play_once('background1')

for j in range(3):  # 生成三行满球和一行随机球作为初始
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
        
newBubColor = random.choice(bubbleColor)
newBub = Actor(newBubColor)
nextBubColor = random.choice(bubbleColor)
newBub.pos = (300, 950)
bubbleNowX = 300
bubbleNowY = 950
pgzrun.go()
