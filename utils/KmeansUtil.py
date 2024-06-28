#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 9:53
# @Author  : LYF
# @File    : KmeansUtil.py
# @Software: IntelliJ IDEA

import random
import sys

import numpy as np


class KMeansClusterer:
    def __init__(self, data_array, K_cluster=0, KMeansPlus=True):
        """
        :param data_array: 数据点 list/array
        :param K_cluster: 分簇数(可选) 默认使用手肘法(SEE)输出最佳分簇数K
        :param KMeansPlus: 使用KMeans++算法
        """
        self.data_array = data_array
        self.K_cluster = K_cluster
        self.KMeansPlus = KMeansPlus
        self.points = self.__pick_start_point(data_array, K_cluster)

    def __center(self, list):
        """计算每一列的平均值 计算某簇所有坐标的平均值"""
        return np.array(list).mean(axis=0)

    def __distance(self, p1, p2):
        """欧式距离计算 坐标平方和开方"""
        tmp = 0
        for i in range(len(p1)):
            tmp += pow(p1[i] - p2[i], 2)
        return pow(tmp, 0.5)

    def __pick_start_point(self, data_array, K_cluster):
        """选择初始点坐标"""
        if K_cluster < 0 or K_cluster > data_array.shape[0]:
            raise Exception("簇数设置有误")

        # 随机点的下标
        indexes = random.sample(np.arange(0, data_array.shape[0], step=1).tolist(), K_cluster)
        points = []
        for index in indexes:
            points.append(data_array[index].tolist())
        return np.array(points)

    def __KMeans(self):
        result = []
        for i in range(self.K_cluster):
            result.append([])

        for item in self.data_array:
            distance_min = sys.maxsize
            index = -1
            for i in range(self.K_cluster):
                distance = self.__distance(item, self.points[i])
                if distance < distance_min:
                    distance_min = distance
                    index = i
            result[index] = result[index] + [item.tolist()]
        new_center = []
        for item in result:
            new_center.append(self.__center(item).tolist())
        # 中心点未改变，说明达到稳态，结束递归
        if (self.points == new_center).all():
            return result

        self.points = np.array(new_center)
        return self.__KMeans()

    def __KMeansPlus(self):
        pass

    def cluster(self):
        """输出分簇"""

        algorithm = self.__KMeansPlus if self.KMeansPlus else self.__KMeans
        # 手肘法判断
        if self.K_cluster <= 0:
            self.K_cluster = self.data_array.shape[0] - 1
            print('SSE 手肘法')
        else:
            return algorithm()

    def mapping(self):
        pass


if __name__ == '__main__':
    # array = np.random.rand(50, 2)
    #
    # item = KMeansClusterer(array, KMeansPlus=False)
    # kc = item.cluster()
    # print(len(kc))
    # print(kc[0])
    # print(kc[1])
    # print(kc[2])

    # df = pd.DataFrame(kc, columns=['x', 'y'])
    # df.plot(kind='scatter', x='x', y='y')
    # plt.show()
    seq = ['A', 'B', 'C', 'D']
    seqw = [1, 2, 3, 4]
    res = {
        'A': 0,
        'B': 0,
        'C': 0,
        'D': 0
    }
    for i in range(100):
        out = random.choices(list(res.keys()), seqw)[0]
        res[out] = res[out] + 1
    print(res)
    pass
