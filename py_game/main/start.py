#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/29 16:40
# @Author  : LYF
# @File    : __init__.py.py
# @Software: IntelliJ IDEA
''' 游戏主程序 '''

from games.snake import game_run


# 开始游戏
def start():
    game_run()


if __name__ == '__main__':
    start()
