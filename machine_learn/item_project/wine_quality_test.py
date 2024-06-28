#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/6 10:21
# @Author  : LYF
# @File    : wine_quality_test.py
# @Description : 葡萄酒质量分类
# 数据：dataset_ori/wine_quality_class
# 通过各项物理化学指标对红/白葡萄酒进行质量分类 特征11个 输出质量[1,10] -- 多分类问题
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

red_path = '../dataset_ori/wine_quality_class/winequality-red.csv'
white_path = '../dataset_ori/wine_quality_class/winequality-white.csv'


def data_look():
    r_d = pd.read_csv(red_path)
    x_col = list(r_d.columns)
    x_col.remove('quality')

    x_train, x_test, y_train, y_test = train_test_split(r_d.loc[:, x_col], r_d.loc[:, 'quality'], random_state=0)
    # x_train.loc[:, ['',]]
    # print(r_d.columns)
    # ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
    #        'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
    #        'pH', 'sulphates', 'alcohol', 'quality']

    pd.plotting.scatter_matrix(x_train.loc[:,
                               ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides',
                                'free sulfur dioxide', ]],
                               c=y_train, cmap='rainbow', marker='.', alpha=.8,
                               figsize=(20.48, 10.8), s=10)
    plt.axis('tight')

    plt.show()


def data_tran():
    r_d = pd.read_csv(red_path)
    x_col = list(r_d.columns)
    x_col.remove('quality')

    x_train, x_test, y_train, y_test = train_test_split(r_d.loc[:, x_col], r_d.loc[:, 'quality'], random_state=0)

    args = [(0.1, 1000)]
    for c, i in args:
        mdl = LinearSVC(C=c, max_iter=i, penalty='l1', dual='auto')  # 默认l2 参数模型
        mdl1 = LogisticRegression(C=c, max_iter=i)  # 默认l1 参数模型

        mdl.fit(x_train, y_train)
        print("特征个数使用比:{}/{}".format(np.sum(mdl.coef_[0] != 0), len(mdl.coef_[0])))
        print(mdl.coef_)
        print("参数({},{})训练分数:{}".format(c, i, mdl.score(x_train, y_train)))
        print("参数({},{})测试分数:{}".format(c, i, mdl.score(x_test, y_test)))


if __name__ == '__main__':
    # 数据预处理 pass 所有特征均为连续数值数据
    # 可视化
    # data_look()
    # 模型训练

    # data_tran()

    # r_d = pd.read_csv(white_path)
    # # 计算皮尔逊相关系数和p值
    # pearson_corr, pearson_p_value = pearsonr(r_d['pH'], r_d['quality'])
    # print(f"皮尔逊相关系数: {pearson_corr}, p值: {pearson_p_value}")
    #
    # # 计算斯皮尔曼等级相关系数和p值
    # spearman_corr, spearman_p_value = spearmanr(r_d['pH'], r_d['quality'])
    # print(f"斯皮尔曼等级相关系数: {spearman_corr}, p值: {spearman_p_value}")

    pass
