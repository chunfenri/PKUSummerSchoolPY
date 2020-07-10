#import pgzrun
#import pgzero
import math
import random
import numpy as np
'''数组0，0是左上角，往下一个是1，0；往右一个是0，1.要求是第一次第一行有10个，下一行9个
下一行10个，下一行9个，呈现六边形密堆积，其中10个球的直径正好填满横排'''
'''右下角下标为(9,22)'''


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
