#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/1 16:48
# @Author  : LYF
# @File    : plan.py
# @Software: IntelliJ IDEA
''' 基础实体'''
import pygame

plan_type = {
    'player': '../run_resource/player1.png',
    'computer': '../run_resource/enemy1.png'
}


class Plan:
    def __init__(self, x, y, screen, type='player'):
        self.screen = screen
        self.image = pygame.image.load(plan_type.get(type)).convert_alpha()
        self.x = x
        self.y = y
        self.bullet_list = []

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for i in self.bullet_list:
            i.display()
            i.move()
            if i.y < 0:
                self.bullet_list.remove(i)

    def move(self, key):
        if key == pygame.K_LEFT:
            self.x -= 10
        elif key == pygame.K_RIGHT:
            self.x += 10

    def fire(self, x, y, direction):
        n_bullet = Bullet(self.x + x, self.y + y, self.screen, direction)
        self.bullet_list.append(n_bullet)


class Bullet:
    def __init__(self, x, y, screen, direction):
        self.screen = screen
        self.image = pygame.image.load('../run_resource/bullet.png').convert_alpha()
        self.x = x
        self.y = y

        self.direction = direction  # 子弹方向 默认向上-1,向下+1
        # 根据方向重设图片
        if direction == 1:
            self.image = pygame.transform.rotate(self.image, 180)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += 2 * self.direction
