#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 15:37
# @Author  : LYF
# @File    : model_knn.py
# @Description : KNN k近邻模型

from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split


class KnnModel:
    cla = None  # 用于分类的模型变量
    reg = None  # 用于回归的模型变量

    def __init__(self, data, target):
        self.data = data
        self.target = target
        self.__transform()

    # 生成训练集和测试集3:1
    def __transform(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.data, self.target, random_state=0)

    # 用于分类的knn
    def by_cla(self, n):
        self.cla = KNeighborsClassifier(n_neighbors=n)
        self.cla.fit(self.x_train, self.y_train)
        return self.cla

    # 用于回归的knn
    def by_reg(self, n):
        self.reg = KNeighborsRegressor(n_neighbors=n)
        self.reg.fit(self.x_train, self.y_train)
        return self.reg

    # 记录泛化精度
    def test_score(self):
        s = self.cla if self.cla else self.reg
        return s.score(self.x_test, self.y_test)

    # 记录训练集精度
    def train_score(self):
        s = self.cla if self.cla else self.reg
        return s.score(self.x_train, self.y_train)
