'''import pgzrun
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


pgzrun.go()'''

import time
import itertools

# 导入pgzero的模块运行工具pgzrun，与模块最后的`pgzrun.go()`配合使用
# 效果相当于在命令行中运行`pgzrun intro.py`
# Mu和Thonny的`Pygame Zero模式`运行，即是执行`pgzrun intro.py`命令
import pgzrun
# pgzrun将自动引入
# * 类: Actor, Rect, ZRect
# * 对象: images, keyboard, screen, sounds
# * 枚举对象: keymods, keys, mouse
# * 函数: animate(), exit()
# * 模块: clock, music, pgzrun, tone
# 因此下面这些导入不是必须的，但显示导入可以方便编辑器补全、提示
from pgzero.actor import Actor
from pgzero.rect import Rect, ZRect
from pgzero.loaders import sounds, images
from pgzero import music, tone
from pgzero.clock import clock
from pgzero.builtins import keymods  # 似乎没有作用
# keymods属性有: LSHIFT, RSHIFT, SHIFT, LCTRL, RCTRL, CTRL, LALT, RALT, ALT, LMETA, RMETA, META, NUM, CAPS, MODE
# 可检测mod值，LCtrl: 64, RCtrl: 128, LAlt: 256, RAlt: 512, LShift: 1, RShift: 1, Capital: 8192
from pgzero.constants import mouse
from pgzero.animation import animate
from pgzero.keyboard import keys, Keyboard
from pgzero.screen import Screen
keyboard: Keyboard  # 类型标注
screen: Screen  # 类型标注


# 生成演员（Actor）实例alien
# Actor(image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs)
alien = Actor('alien')
# 演员定位，可以使用这些属性：
# bottom, bottom_left, bottom_right, center, left, mid_bottom, mid_left,
# mid_right, mid_top, pos, right, top, top_left, top_right, x, y
# 另有属性，锚点: anchor, 角度: angle
# 另有方法，测量相对距离: distance_to(), 测量相对角度: angle_to()
alien.pos = (0, 200)
alien2 = Actor('alien')

TITLE = 'api用法'  # 窗口标题
# 画布宽高
WIDTH = 800
HEIGHT = 400


def draw():
    """    绘制（显示钩子）;

    如果定义了update()，或者发出了定时器（clock）事件、输入事件，就会重绘画布;
    不要在这里更新数据，定义动画;
    """
    screen.clear()  # 屏幕清理，其后默认填充黑色
    screen.fill((128, 0, 128))  # 填充颜色

    screen.blit('alien_hurt',(WIDTH/2, 0))  # 绘制图像

    screen.draw.line((0,0),(WIDTH, HEIGHT),(0,128,128))  # 画线

    rect = Rect((0, 0), (200, 200))  # 画方形
    rect.center = WIDTH / 2, HEIGHT / 2
    screen.draw.rect(rect, (128,128,128))
    # screen.draw.filled_rect(rect, color)  # 画填充的方形

    # screen.draw.circle(pos, radius, color)  # 画圆形
    screen.draw.filled_circle((WIDTH/2, HEIGHT/2), 100, (0,0,200))  # 画填充的圆形

    # 画文本
    screen.draw.text(
        "Python\n和\nPygame Zero\n游戏学习",  # 要显示的文本
        midtop=(WIDTH / 2, 10),  # 定位，关键字：
        # top left bottom right
        # topleft bottomleft topright bottomright
        # midtop midleft midbottom midright
        # center centerx centery
        fontname="simkai",  # 请保证存在字体： fonts\simkai.ttf
        fontsize=64,
        align='center',  # 对齐方式：left, center, right
        color="#000000",  # 颜色
        # background="gray",  # 背景色
        alpha=0.3,  # 透明度
        gcolor="#0000ff", # 渐变色

        owidth=2,  # 外框
        ocolor='red',  # 外框色

        # shadow=(1.0,1.0),  # 阴影投射偏置，会覆盖owidth，被alpha覆盖
        # scolor="blue",  # 阴影颜色
    )
    # 画适配方框的文本
    # screen.draw.textbox(*args, **kwargs)

    # 画文本
    screen.draw.text(
        "用空白键停止/播放音乐",
        midtop=(WIDTH / 2, HEIGHT - 30),
        fontname="simkai",
        alpha=0.7
    )

    # 画演员
    alien.draw()
    alien2.draw()

# screen.surface: Surface  # 代表屏幕缓存


def update():
    """
    更新（显示钩子）;
    游戏的逐步逻辑，每秒重复60次;
    update()基于帧，间距不稳定；update(dt)基于实际时间，消耗大;
    """
    alien.left += 2
    if alien.left > WIDTH:
        alien.right = 0


# 合成音，'E4'指第4个八度的E，'A#5'指第5个八度的A升，'Bb3'指第3个八度的B降
beep = tone.create('A3', 0.5)
def on_mouse_down(pos):
    """ 当鼠标按下（事件钩子）"""
    if alien.collidepoint(pos):
        sounds.eep.play()  # sounds, images 可以用`.file_name`取得Surface或Sound实例
        alien.image = 'alien_hurt'
        time.sleep(0.1)
        alien.image = 'alien'
        set_alien_hurt()
        move_alien2()
    else:
        print("You missed me!")
        # beep.stop()  # 快速点击会导致杂音，不停止则有变音
        beep.play()
        # tone.play('A3', 0.5)  # 也可以不生成实例


def on_mouse_move(pos, rel, buttons):
    if mouse.LEFT in buttons and alien.collidepoint(pos):
        # 当鼠标拖动
        alien.pos = pos


def set_alien_hurt():
    """ 外星人被击中后的动作"""
    alien.image = 'alien_hurt'
    sounds.eep.play()
    clock.schedule_unique(set_alien_normal, 1.0)
    # clock的方法还有: schedule(), schedule_interval(), unschedule()


def set_alien_normal():
    """ 外星人复原"""
    alien.image = 'alien'


# alien2动画
# 位置数据
offset_x = alien2.width / 2
offset_y = alien2.height / 2
BLOCK_POSITIONS = [
    (WIDTH - offset_x, offset_y),
    (WIDTH - offset_x, HEIGHT - offset_y),
    (offset_x, HEIGHT - offset_y),
    (offset_x, offset_y),
]
alien2_positions = itertools.cycle(BLOCK_POSITIONS)
def move_alien2():
    """Move the ship to the target."""
    animate(
        alien2,
        tween='accel_decel',  # 可选: linear, accelerate, decelerate, accel_decel, end_elastic, 
        # start_elastic, both_elastic, bounce_end, bounce_start, bounce_start_end
        pos=next(alien2_positions),
        duration=1,
        # on_finished=next_ship_target,  # 结束时回调
    )
    # animate()会返回一个动画实例，可以使用方法: stop(complete=False)，属性: running, on_finished

# 控制背景音乐
music.set_volume(0.3)
music.play("handel")
is_pausing = False
def on_key_down(key, mod):
    if key == keys.SPACE:
        global is_pausing
        if is_pausing:
            music.unpause()
            is_pausing = False
        else:
            music.pause()
            is_pausing = True
# music的方法还有: play_once(name), queue(name), stop(), is_playing(), fadeout(duration), get_volume(), 
# 键盘和鼠标事件钩子还有：
# on_key_up()
# on_mouse_up()
# on_music_end()


pgzrun.go()  # 运行本脚本