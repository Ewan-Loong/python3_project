#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/6 15:52
# @Author  : LYF
# @File    : nyc_crime_test.py
# @Description : 纽约市犯罪数据
from datetime import datetime

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import pearsonr, spearmanr

def check_time_format(time_str, date_type=None, date_format=None):
    type_dit = {'D': '%Y-%m-%d', 'T': '%H:%M:%S', 'DT': '%Y-%m-%d %H:%M:%S'}

    if date_format is None and date_type in ['D', 'T', 'DT']:
        format = type_dit[date_type]
    else:
        raise NameError("参数错误,date_type可选项为D,T,DT")

    try:
        datetime.strptime(time_str, format)
        return True
    except ValueError:
        return False


# 数据处理
def data_handling():
    # 加载数据
    nyc_crime = pd.read_csv("../dataset_ori/nyc_crime/NYPD_Complaint_Data_Historic.csv")

    # 日期处理 mm/dd/yyyy
    to_dt_list = ['CMPLNT_FR_DT', 'CMPLNT_TO_DT', 'RPT_DT']
    for col in to_dt_list:
        # errors 无法解析数据如何处理：默认raise 抛出异常;coerce 置NaT;ignore 返回原值
        nyc_crime[col] = pd.to_datetime(nyc_crime[col], format='%m/%d/%Y', errors='coerce')

    # 时间处理 fixme
    # to_datetime(,format='%H:%M:%S',errors='coerce') 转换后为 1900-01-01 %H:%M:%S
    # to_timedelta(,errors='coerce') 转换后为 0 days %H:%M:%S

    # to_tm_list = ['CMPLNT_FR_TM', 'CMPLNT_TO_TM']
    # for col in to_tm_list:
    #     nyc_crime[col] = pd.to_datetime(nyc_crime[col], format='%H:%M:%S', errors='coerce')

    # 时间日期合并生成新字段 axis=0默认按列操作,1按行操作
    # 日期和时间组合需要把时间转成 Timedelta
    def ex_col(df):
        fr_datetime = df['CMPLNT_FR_DT'] + pd.to_timedelta(df['CMPLNT_FR_TM'], errors='coerce')
        to_datetime = df['CMPLNT_TO_DT'] + pd.to_timedelta(df['CMPLNT_TO_TM'], errors='coerce')
        ft_to_time = (to_datetime - fr_datetime) if (to_datetime - fr_datetime) is None \
            else (to_datetime - fr_datetime).seconds / 60 
        sub_time = (df['RPT_DT'] - df['CMPLNT_FR_DT']).days
        return fr_datetime, to_datetime, ft_to_time, sub_time

    # apply添加多列:func返回多列 映射到对应位置 ps:持续时间(分钟) 与报警时间差(天)
    nyc_crime[['发生详细时间', '结束详细时间', '持续时间', '与报警时间差']] = nyc_crime.apply(ex_col, axis=1, result_type='expand')

    # nyc_crime['发生详细时间'] = nyc_crime.apply(
    #     lambda x: x['CMPLNT_FR_DT'] + pd.to_timedelta(x['CMPLNT_FR_TM'], errors='coerce'), axis=1)
    #
    # nyc_crime['结束详细时间'] = nyc_crime.apply(
    #     lambda x: x['CMPLNT_TO_DT'] + pd.to_timedelta(x['CMPLNT_TO_TM'], errors='coerce'), axis=1)
    #
    # nyc_crime['持续时间'] = nyc_crime.apply(lambda x: x['结束详细时间'] - x['发生详细时间'], axis=1)
    #
    # nyc_crime['与报警时间差'] = nyc_crime.apply(lambda x: (x['结束详细时间'] - x['RPT_DT']).days, axis=1)

    # 列名替换
    col_zh = {'CMPLNT_NUM': 'ID',
              'CMPLNT_FR_DT': '发生日期', 'CMPLNT_FR_TM': '发生时间',
              'CMPLNT_TO_DT': '结束日期', 'CMPLNT_TO_TM': '结束时间',
              'RPT_DT': '报警日期', 'KY_CD': '犯罪类型代码',
              'OFNS_DESC': '犯罪类型描述', 'PD_CD': '精确犯罪类型代码',
              'PD_DESC': '精确犯罪类型描述', 'CRM_ATPT_CPTD_CD': '犯罪未遂标志',
              'LAW_CAT_CD': '犯罪级别', 'JURIS_DESC': '事件司法管辖区',
              'BORO_NM': '发生行政区', 'ADDR_PCT_CD': '发生辖区',
              'LOC_OF_OCCUR_DESC': '具体场所位置', 'PREM_TYP_DESC': '发生地点类型',
              'PARKS_NM': '发生标志地名', 'HADEVELOPT': '发生住房区',
              'X_COORD_CD': '长岛区X坐标', 'Y_COORD_CD': '长岛区Y坐标',
              'Latitude': '纬度', 'Longitude': '经度', 'Lat_Lon': '经纬度', }

    nyc_crime.rename(columns=col_zh, inplace=True)

    print(nyc_crime.head(5))

    # 更具数据观查 数据主要集中在2013(86162) 2014(490363) 2015(468576) 99.67%
    nyc_crime = nyc_crime[nyc_crime['发生日期'] >= '2014-01-01']

    # 保存处理后文件 index 不生成行号
    nyc_crime.to_csv('../dataset_after/nyc_crime/nyc_crime.csv', index=False)


if __name__ == '__main__':
    # data_handling()

    # nyc_crime = pd.read_csv("../dataset_after/nyc_crime/nyc_crime.csv")
    # sa = nyc_crime.sample(frac=0.01) # 随机抽取 1%的数据
    # sa.to_csv('../dataset_after/nyc_crime/nyc_crime_sample.csv', index=False)

    # nyc_crime = pd.read_csv("../dataset_after/nyc_crime/nyc_crime.csv")
    # nyc_crime['事件发生日期'] = pd.to_datetime(nyc_crime['事件发生日期'], errors='coerce')
    # nyc_crime['事件发生时间'] = pd.to_timedelta(nyc_crime['事件发生日期'], errors='coerce')

    # # 中文乱码 负号显示解决
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 以时间列为x轴，id列为y轴作图
    # dt_id = nyc_crime.loc[:, ['主键ID', '事件发生日期']]
    # dt_id.plot(x='事件发生日期',y='主键ID')
    # plt.show()

    # 时间序列按不同区间统计 - resample 重新采样 on以什么字段为时间参数
    # m = nyc_crime.resample("M",on='事件发生日期').count()
    # 直接对数据进行count 是按时间区间分别统计每一列的非空个数

    # 以时间列为分组计算发事件集中发生的条数
    # t1 = nyc_crime.groupby(['事件发生日期']).count()

    # df = pd.DataFrame({'a': [1, 2, 3, 4, 5],
    #                    'b': ['aaa', 'bbb', 'ccc', 'ddd', 'eee'],
    #                    'c': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']})
    #
    # # 同时添加多列测试
    # def ex_col(df):
    #     c = df['a'] + 1
    #     d = df['b'] + '_str'
    #     return c, d
    #
    # df[['c', 'd']] = df.apply(ex_col, axis=1, result_type='expand')
    # print(df)
    pass
