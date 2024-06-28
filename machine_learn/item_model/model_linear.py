#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 16:41
# @Author  : LYF
# @File    : model_linear.py
# @Description : 线性模型
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split


class LinearModel:
    cla = None  # 用于分类的模型变量
    reg = None  # 用于回归的模型变量
    w = None
    b = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__transform()

    # 生成训练集和测试集3:1
    def __transform(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, random_state=0)

    # 线性回归 最小二乘法
    def line_reg(self):
        self.reg = LinearRegression()
        self.reg.fit(self.x_train, self.y_train)
        self.w = self.reg.coef_  # 斜率
        self.b = self.reg.intercept_  # 截距
        return self.reg

    # 岭回归 L2正则化 避免过拟合而进行的优化约束
    def ridge_reg(self, alpha=1.0):
        # alpha越大 会令系数更加趋向于0，从而降低训练集性能，但可能会提高泛化性能(即测试数据的准确性)
        self.reg = Ridge(alpha=alpha)
        self.reg.fit(self.x_train, self.y_train)
        self.w = self.reg.coef_  # 斜率 多个特征值返回list
        self.b = self.reg.intercept_  # 截距
        return self.reg

    # Lasso L1正则化 自动化特征选择 某些特征可能被忽略
    def lasso_reg(self, alpha=1.0, max_iter=1000):
        # alpha 同岭回归 越大会令系数越趋于0; 过大会欠拟合,过小时则会消除正则化结果(会得到与线性回归类似的结果)并出现过拟合
        # max_iter 最大迭代次数,对于lasso常把alpha减小并增大max_iter
        self.reg = Lasso(alpha=alpha, max_iter=max_iter)
        self.reg.fit(self.x_train, self.y_train)
        self.w = self.reg.coef_  # 斜率 多个特征值返回list
        self.b = self.reg.intercept_  # 截距

        print("特征个数使用比:{}/{}".format(np.sum(self.reg.coef_[0] != 0), len(self.reg.coef_[0])))

        return self.reg

    # LogisticRegression 该模型是用于分类的 默认l1 支持l2正则
    def log_reg(self, C=1.0, max_iter=100, penalty='l1'):
        # C类似于alpha C值越大,训练集拟合更好,泛化弱;C值越小,正则化越强,w系数更趋近于0
        self.cla = LogisticRegression(C=C, max_iter=max_iter, penalty=penalty)
        self.cla.fit(self.x_train, self.y_train)
        self.w = self.cla.coef_
        self.b = self.cla.intercept_  # 截距

        if penalty == 'l1':
            print("特征个数使用比:{}/{}".format(np.sum(self.cla.coef_[0] != 0), len(self.cla.coef_[0])))

        return self.cla

    # 同log_reg类似 默认l2 支持l1
    def svc_cls(self, C=1.0, penalty='l2'):
        if penalty == 'l1':
            self.cla = LinearSVC(C=C, penalty=penalty, dual='auto')
        else:
            self.cla = LinearSVC(C=C, penalty=penalty)

        self.cla.fit(self.x_train, self.y_train)
        self.w = self.cla.coef_
        self.b = self.cla.intercept_  # 截距

        if penalty == 'l1':
            print("特征个数使用比:{}/{}".format(np.sum(self.cla.coef_[0] != 0), len(self.cla.coef_[0])))

        return self.cla

    # 记录泛化精度
    def test_score(self):
        s = self.reg
        return s.score(self.x_test, self.y_test)

    # 记录训练集精度
    def train_score(self):
        s = self.reg
        return s.score(self.x_train, self.y_train)
