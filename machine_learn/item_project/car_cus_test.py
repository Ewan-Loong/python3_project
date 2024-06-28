#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/31 15:15
# @Author  : LYF
# @File    : car_cus_test.py
# @Description : 汽车销售客户数据分类
# 数据：dataset_ori/car_cus_class fixme 垃圾数据集；训练模型、参数调整只能拿到[0.5±0.01]的训练和测试分数
# 一家汽车公司计划利用其现有产品（P1、P2、P3、P4 和 P5）进入新市场。经过深入的市场研究，他们推断出新市场的行为与现有市场相似
# 在他们现有的市场中，销售团队将所有客户分为4个细分市场（A、B、C、D）。然后，他们针对不同的客户细分进行了细分的外展和沟通。
# 这种策略对他们来说非常有效。他们计划在新市场上使用相同的策略，并确定了2627个新的潜在客户
# 该数据集根据购买历史和相应的细分市场提供了公司现有(tran)和潜在客户(test)的详细信息
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import LinearSVC
import itertools


def data_handling():
    # 加载数据
    car_train = pd.read_csv("../dataset_ori/car_cus_class/train-set.csv")
    # print(car_train.columns)

    # 列是否存在空 ['Married', 'Graduated', 'Profession', 'WorkExperience', 'FamilySize', 'Category']
    # col_null = []
    # for col in car_train.columns:
    #     if pd.isna(car_train[col]).any():
    #         col_null.append(col)
    # print(col_null)

    # print(pd.isna(car_train['FamilySize']).any())
    # inplace 原视图修改
    car_train['FamilySize'].fillna(1, inplace=True)
    # print(pd.isna(car_train['FamilySize']).any())

    # 条件补充
    car_train['Married'].mask(car_train['Married'].isnull() & car_train['FamilySize'] > 1, 'Yes', inplace=True)
    car_train['Married'].mask(car_train['Married'].isnull() & car_train['FamilySize'] == 1, 'No', inplace=True)
    # = np.where(car_train['Married'].empty and car_train['FamilySize'] > 1, 'Yes', 'No')

    # 均值补充
    m = car_train['WorkExperience'].mean()  # 取均值
    car_train['WorkExperience'].fillna(m, inplace=True)
    car_train['WorkExperience'] = car_train['WorkExperience'].round(2)  # 四舍五入小数点后n位，输入负数指小数点前n位

    # 空值补充默认值
    car_train['Graduated'].fillna("Nil", inplace=True)  # 是否毕业

    # col_avg = data["列"].mean() # 使用均值补充
    # data["列"].fillna(col_avg, inplace=True)

    # 空值删除 pass

    # 将文件的True/False 改为01
    car_train_one_hot = car_train
    car_train_one_hot['Married'] = car_train_one_hot['Married'].replace({'Yes': 1, 'No': 0})
    # 修改分类为数值 否则会报错 fixme 待研究
    # car_train_one_hot['Segmentation'] = car_train_one_hot['Segmentation'].replace({'A': 0, 'B': 1, 'C': 2, 'D': 3})

    # 特征处理 - one-hot编码 使用0/1编码，默认是True/False
    dum_col = ['Gender', 'Graduated', 'Profession', 'SpendingScore', 'Category']  # 编码列指定
    car_train_one_hot = pd.get_dummies(car_train_one_hot, columns=dum_col, dtype=float)

    # 保存处理后文件 index 不生成行号
    car_train.to_csv('../dataset_after/car_cus_class/train-set.csv', index=False)
    car_train_one_hot.to_csv('../dataset_after/car_cus_class/train-set-decode.csv', index=False)
    print("ori hand", car_train.columns)
    print("one-hot hand", car_train_one_hot.columns)


def data_look():
    car_data = pd.read_csv("../dataset_after/car_cus_class/train-set-decode.csv")
    car_data['Segmentation'] = car_data['Segmentation'].replace({'A': 0, 'B': 1, 'C': 2, 'D': 3})
    x_col = list(car_data.columns)
    x_col.remove('Segmentation')
    x_col.remove('CustomerID')

    x_train, x_test, y_train, y_test = \
        train_test_split(car_data.loc[:, x_col], car_data.loc[:, 'Segmentation'], random_state=0)

    # 通过itertools.combinations 生产n*n的不重复的散点矩阵
    x_col_2 = list(itertools.combinations(x_col, 2))
    # print(len(x_col_2))
    pd.plotting.scatter_matrix(x_train.loc[:, x_col_2[0]], c=y_train, marker='.', alpha=.8, )
    plt.show()


def tran_model():
    car_data = pd.read_csv("../dataset_after/car_cus_class/train-set-decode.csv")
    x_col = list(car_data.columns)
    x_col.remove('Segmentation')
    x_col.remove('CustomerID')

    # 数据行列处理
    # print(car_data.loc[1, x_col])
    # print(car_data.loc[1, 'Segmentation'])
    args = [(0.01, 10000)]
    for c, i in args:
        lass_1 = LinearSVC(C=c, max_iter=i, penalty='l1', dual='auto')  # 默认l2 参数模型
        lass = LogisticRegression(C=c, max_iter=i)  # 默认l1 参数模型
        lass_2 = BernoulliNB(alpha=100) # BernoulliNB MultinomialNB
        lass_3 = GaussianNB()

        x_train, x_test, y_train, y_test = \
            train_test_split(car_data.loc[:, x_col], car_data.loc[:, 'Segmentation'], random_state=0)

        lass.fit(x_train, y_train)
        print("特征个数使用比:{}/{}".format(np.sum(lass.coef_[0] != 0), len(lass.coef_[0])))
        print(lass.coef_)
        print("参数({},{})训练分数:{}".format(c, i, lass.score(x_train, y_train)))
        print("参数({},{})测试分数:{}".format(c, i, lass.score(x_test, y_test)))


if __name__ == '__main__':
    # data_handling()

    # data_look()

    tran_model()

    # col = ['Gender', 'Graduated', 'Profession', 'SpendingScore', 'Category']
    # l = list(itertools.combinations(col, 2))
    # print(l)
    pass
