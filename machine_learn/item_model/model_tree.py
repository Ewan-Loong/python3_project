#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/7 9:34
# @Author  : LYF
# @File    : model_tree.py
# @Description : 决策树模型

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split


class TreeModel:
    cla = None  # 用于分类的模型变量
    reg = None  # 用于回归的模型变量

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__transform()

    # 生成训练集和测试集3:1
    def __transform(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, random_state=0)

    # RandomForestRegressor 用于回归的随机森林决策树
    # n_estimators 书的个数
    # max_features 每次划分考虑特征的个数
    def rf_reg(self, n_estimators=100, random_state=None):
        self.reg = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        pass

    # RandomForestClassifier 用于分类的随机森林决策树
    def rf_cla(self, n_estimators=100, random_state=None):
        self.cla = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        pass

    pass
