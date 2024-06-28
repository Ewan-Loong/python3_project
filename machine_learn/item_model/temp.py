#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/25 16:35
# @Author  : LYF
# @File    : temp.py
# @Description : 临时学习文件
from pandas.plotting import scatter_matrix
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def iris():
    # 加载数据
    iris_dataset = load_iris()

    # 打乱数据 默认将训练集和测试集分为3:1(75:25)
    # 指定随机数种子 random_state 以保证每次打乱的后的数据集一致
    X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)

    # 上述沿用数学中 f(x)=y 的习惯 x为输入的数据 y为结果;
    # 该处 x>花的基本数据 y>花的种类

    # 利用X_train中的数据创建DataFrame
    # 利用iris_dataset.feature_names中的字符串对数据列进行标记(即数据表的表头)
    iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
    # 利用DataFrame创建散点图矩阵，按y_train着色
    grr = pd.plotting.scatter_matrix(iris_dataframe, c=y_train, figsize=(15, 15), marker='o',
                                     hist_kwds={'bins': 20}, s=60, alpha=.8)
    # plt.show()

    knn = KNeighborsClassifier(n_neighbors=1)
    # 训练模型 fit(数据,标签)
    knn.fit(X_train, y_train)

    # 新数据测试 是按行测试的
    X_new = np.array([[5, 2.9, 1, 0.2]])
    prediction = knn.predict(X_new)
    # 返回的是标签序列号 如果是一组测试数据 返回的是列表
    # print("Predicted target name: {}".format(iris_dataset['target_names'][prediction]))

    # 评估模型
    y_pred = knn.predict(X_test)
    # print("Test set predictions:\n {}".format(y_pred))

    # 两个方法等价 输出的是测试的精度 如0.97 > 指97%预测的结果正确
    print("Test set score: {:.2f}".format(np.mean(y_pred == y_test)))
    print("Test set score: {:.2f}".format(knn.score(X_test, y_test)))


def cancer():
    from sklearn.datasets import load_breast_cancer

    cancer = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        cancer.data, cancer.target, stratify=cancer.target, random_state=6)
    training_accuracy = []
    test_accuracy = []

    # k近邻的个数 取值从1到10
    neighbors_settings = range(1, 11)

    for n_neighbors in neighbors_settings:
        # 构建模型
        clf = KNeighborsClassifier(n_neighbors=n_neighbors)
        clf.fit(X_train, y_train)
        # 记录训练集精度
        training_accuracy.append(clf.score(X_train, y_train))
        # 记录泛化精度
        test_accuracy.append(clf.score(X_test, y_test))

    plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
    plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("n_neighbors")
    plt.legend()
    plt.show()


def test():
    # 测试
    iris_dataset = load_iris()

    from item_model.model_knn import KnnModel

    kn = KnnModel(iris_dataset['data'], iris_dataset['target'])

    train = []
    test = []

    for n in range(1, 11):
        kn.by_cla(n)
        print("n={}".format(n))
        s1 = kn.test_score()
        print("test_score {:.2f}".format(s1))
        test.append(s1)
        s2 = kn.train_score()
        print("train_score {:.2f}".format(s2))
        train.append(s2)

    # 绘图解决中文乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
    # plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    plt.plot([i for i in range(1, 11)], train, label="training accuracy")
    plt.plot([i for i in range(1, 11)], test, label="test accuracy")
    plt.ylabel("准确度 Accuracy")
    plt.xlabel("近邻数 n")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    pass
