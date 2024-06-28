#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/13 15:03
# @Author  : LYF
# @File    : snake.py
# @Software: IntelliJ IDEA


'''贪吃蛇'''
import sys

import pygame

from main.pojo.snake_item import head


def game_run():
    pygame.init()  # 初始化
    # 定义游戏窗口 像素*像素 可改变大小的窗口
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    # 除去边框8px 可移动范围[8-492,8-492]

    # 设置窗口的标题/游戏名称
    pygame.display.set_caption('贪吃蛇')
    # 帧率 / 游戏时间
    clock = pygame.time.Clock()
    # 背景图加载
    image_back = pygame.image.load('../run_resource/snake_bg.png').convert_alpha()

    s_head = head(250, 250, screen)

    # 固定代码：监听游戏时间并刷新画面 点X退出界面
    while True:
        clock.tick(5)  # 帧数
        screen.blit(image_back, (0, 0))

        s_head.display()

        # 循环获取事件，监听事件状态
        for event in pygame.event.get():
            # 判断用户是否点了"X"关闭按钮,并执行if代码段
            if event.type == pygame.QUIT:
                # 卸载所有模块 终止程序
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    s_head.turn(event.key)

        pygame.display.flip()  # 更新屏幕内容
        pygame.display.update()
