#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/2 11:18
# @Author  : LYF
# @File    : model_naive_bayes.py
# @Description : 朴素贝叶斯分类器
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB


class NaiveBayesModel:
    # 训练速度更快 泛化能力较线性分类器较差；其假设所有变量之间不相关，实际应用中会有偏差
    cla = None  # 用于分类的模型变量

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__transform()

    # 生成训练集和测试集3:1
    def __transform(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, random_state=0)

    def mul_cla(self, alpha=1.0):
        # alpha:添加alpha个虚拟数据点，对所有值取正值，可以将数据平滑化；
        # alpha，调整该参数通常会使精度略有提高
        self.cla = MultinomialNB(alpha=alpha)
        self.cla.fit(self.x_train, self.y_train)
        return self.cla

    def ber_cla(self, alpha=1.0):
        # alpha:添加alpha个虚拟数据点，对所有值取正值，可以将数据平滑化；
        # alpha，调整该参数通常会使精度略有提高
        self.cla = BernoulliNB(alpha=alpha)
        self.cla.fit(self.x_train, self.y_train)
        return self.cla

    def gas_cla(self):
        self.cla = GaussianNB()
        self.cla.fit(self.x_train, self.y_train)
        return self.cla

    # 记录泛化精度
    def test_score(self):
        s = self.cla
        return s.score(self.x_test, self.y_test)

    # 记录训练集精度
    def train_score(self):
        s = self.cla
        return s.score(self.x_train, self.y_train)
