import pgzrun
import pgzero
import math
import random

'''数组0，0是左上角，往下一个是1，0；往右一个是0，1.要求是第一次第一行有10个，下一行9个
下一行10个，下一行9个，呈现六边形密堆积，其中10个球的直径正好填满横排'''

def index2pos(indx,indy):
    return (0.0,0.0)

def pos2index(posx,posy): 
‘’'主要用于bubble碰撞到别的bubble时看应该要塞到哪个位置，位置可能不是准确位置，在一个范围内都要映射到一个位置'''
    
    return (0,0)

def findExplode(bubbleA):
'''bubbleA是撞击上的球所在位置的index值，是一个二元元组
找到哪些球球需要爆炸，返回爆照球的下标列表。不包含爆炸后掉落的球，只考虑相同颜色的连通分量'''
    return [(0,0),(1,0),(1,1)]

def findFallbubble():
    '''找到球爆炸后需要掉下来的其他球，返回值同上'''
    return [(0,0),(1,0),(1,1)]
