#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/13 15:16
# @Author  : LYF
# @File    : snake_itme.py
# @Software: IntelliJ IDEA

'''贪吃蛇实体类'''
import random

import pygame

image_type = {
    'head': '../run_resource/s_head.png',
    'body': '../run_resource/s_body.png'
}


class head:
    '''蛇头'''

    def __init__(self, x, y, screen):
        self.screen = screen
        self.image = pygame.image.load(image_type.get('head')).convert_alpha()
        self.point = (x, y)  # 图像点 左上角
        self.center = (x + 5, y - 5)  # 图像中心点
        self.move_to = (1, 0)  # 移动方向 (1,0) (0,1) (-1,0) (0,-1) 二维坐标系
        self.body_list = [body(x, y, screen), body(x, y, screen)]
        self.food = None

    def display(self):
        if self.food is None:
            self.food = body(random.randint(8, 482), random.randint(8, 482), self.screen)

        # 碰撞判断
        if pow(self.food.center[0] - self.center[0], 2) + pow(self.food.center[1] - self.center[1], 2) <= 100:
            self.body_list.append(self.food)
            self.food = body(random.randint(8, 482), random.randint(8, 482), self.screen)

        self.food.display(self.food.point)
        self.body_list[0].display(self.point)
        for i in range(1, self.body_list.__len__()):
            self.body_list[i].display(self.body_list[i - 1].last_point)

        self.move()
        self.screen.blit(self.image, self.point)

    def move(self):
        x = self.point[0] + self.move_to[0] * 10
        y = self.point[1] + self.move_to[1] * 10
        if x > 482 or x < 8 or y > 482 or y < 8:
            pass  # 超出边界
        else:
            self.point = (x, y)
            self.center = (x + 5, y - 5)

    def turn(self, key):
        if key == pygame.K_LEFT:
            self.move_to = (self.move_to[1], self.move_to[0] * -1)  # 顺时针90° (x,y) > (y,-x)
            self.image = pygame.transform.rotate(self.image, 90)
        elif key == pygame.K_RIGHT:
            self.move_to = (self.move_to[1] * -1, self.move_to[0])  # 逆时针90° (x,y) > (-y,x)
            self.image = pygame.transform.rotate(self.image, -90)


class body:
    '''蛇身体/奖励点'''

    def __init__(self, x, y, screen):
        self.screen = screen
        self.image = pygame.image.load(image_type.get('body')).convert_alpha()
        self.point = (x, y)  # 图像点 左上角
        self.center = (x + 5, y - 5)  # 图像中心点
        self.last_point = None

    def display(self, xy):
        self.last_point = self.point
        self.point = xy
        self.center = (xy[0] + 5, xy[1] - 5)
        self.screen.blit(self.image, self.point)
        # print(xy)

    pass
