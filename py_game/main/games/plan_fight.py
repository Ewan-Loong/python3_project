#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/13 14:45
# @Author  : LYF
# @File    : plan_fight.py
# @Software: IntelliJ IDEA
import sys

import pygame

from main.pojo.G_item import Plan
from main.pojo.e_player import e_plan

'''飞机大战'''


def game_run():
    pygame.init()  # 初始化
    # 定义游戏窗口 像素*像素 可改变大小的窗口
    screen = pygame.display.set_mode((400, 600), pygame.RESIZABLE)
    # 设置窗口的标题/游戏名称
    pygame.display.set_caption('飞机大战')

    # 帧率 / 游戏时间
    clock = pygame.time.Clock()

    # 背景图加载
    back_y = 0
    image_back = pygame.image.load('../run_resource/background.png').convert_alpha()

    p1 = Plan(175, 500, screen)
    e1 = e_plan(screen)

    # 固定代码：监听游戏时间并刷新画面 点X退出界面
    while True:
        # 30帧
        clock.tick(30)

        if 0 <= back_y <= 600:
            back_y += 2
        else:
            back_y = 0

        # 背景图滚动 原理：两张图拼接 向下滚动
        screen.blit(image_back, (0, back_y))
        screen.blit(image_back, (0, back_y - 600))

        p1.display()
        e1.display()

        # 循环获取事件，监听事件状态
        for event in pygame.event.get():
            # 判断用户是否点了"X"关闭按钮,并执行if代码段
            if event.type == pygame.QUIT:
                # 卸载所有模块 终止程序
                pygame.quit()
                sys.exit()

            # elif event.type == pygame.MOUSEMKEYDOWNOTION:
            #    p1.mou_move(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    p1.move(event.key)
                elif event.key == pygame.K_SPACE:
                    p1.fire(20, -10, -1)

        e1.move()
        if e1.y > 600:
            e1.y = 0

        pygame.display.flip()  # 更新屏幕内容
        pygame.display.update()
