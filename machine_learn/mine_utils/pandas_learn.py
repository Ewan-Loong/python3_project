#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 16:30
# @Author  : LYF
# @File    : pandas_learn.py
# @Description : pandas学习以及工具

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_path = '../dataset_after/nyc_crime/nyc_crime.csv'

if __name__ == '__main__':
    df = pd.read_csv(csv_path)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # print(red_wine)
    # print(red_wine.describe())

    # 数据按值排序
    # red_wine.sort_values(by='pH', inplace=True)

    # 重置行索引 drop代表丢弃之前的行索引
    # red_wine.reset_index(drop=True, inplace=True)

    # 不同时间犯罪事件发生数
    # df['dt'] = pd.to_timedelta(df['发生时间'], errors='coerce').seconds / 60 / 60
    # df['dt'] = df.apply(lambda x: int(pd.to_timedelta(x['发生时间'], errors='coerce').seconds / 60 / 60), axis=1)
    #
    # t1 = df.groupby('dt')['ID'].count()
    # t1.plot()
    #
    # plt.xticks(np.arange(0, 24, 1))  # 设置x轴0-24小时
    # plt.show()

    # 不同犯罪地点事件发生数
    t2 = df.groupby('发生行政区')['ID'].count()
    # t2.plot(kind='pie', autopct='%.2f%%') # pie饼图
    t2.plot(kind='bar', rot=0, xticks=t2.index.values)
    # plt.xticks(t2.index.values)
    # plt.xticks(ticks=np.arange(0, len(t2.index.values), 1), labels=t2.index.values)
    plt.show()

    # 不同犯罪类型事件持续均值
    # t3 = df.groupby(['精确犯罪类型代码'])['持续时间'].mean()
    # t3.plot()
    # plt.xticks(rotation=90)
    # plt.show()

    pass
