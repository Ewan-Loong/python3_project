#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/30 10:00
# @Author  : LYF
# @File    : ctrl_p.py
# @Software: IntelliJ IDEA
''' 敌人角色 e_player '''
import random

from .G_item import Plan


class e_plan(Plan):
    def __init__(self, screen):
        super().__init__(random.randint(0, 350), 0, screen, 'computer')
        self.direction = random.choice([-1, 1])  # -1左 1右

    def move(self, **kwargs):
        self.y += 1
        # 随机改变方向
        if random.randint(0, 100) == 1:
            self.direction *= -1
        # 撞墙改变方向
        move_x = self.x + 1 * self.direction
        if move_x > 350:
            self.direction = -1
            self.x = self.x + 1 * self.direction
        elif move_x < 0:
            self.direction = 1
            self.x = self.x + 1 * self.direction
        else:
            self.x = move_x

        # 1/50 的概率自动发射子弹
        if random.randint(0, 50) == 1:
            self.fire(19, 40, 1)
