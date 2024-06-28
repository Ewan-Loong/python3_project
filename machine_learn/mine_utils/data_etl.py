#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/25 16:27
# @Author  : LYF
# @File    : data_etl.py
# @Description : 一个通用的ETL工具类，利用Pandas进行数据处理。包含数据清洗、整合、转换和计算等功能。数据读取、转换、加载工具

# 项目常用的包
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re


# import mglearn
# 非重点,附加代码下载 https://github.com/amueller/introduction_to_ml_with_python

# - 数据清洗：去除重复数据、处理缺失值、处理异常值等。
# - 数据整合：将多个数据源的数据进行合并或关联。
# - 数据转换：对数据进行格式转换、数据类型转换、单位转换等。
# - 数据计算：进行数据聚合、计算指标、创建衍生字段等。x`


def check_data_validity(df, column, value_range=None, string_pattern=None):
    '''
    检查DataFrame中指定列的数据是否符合要求

    :param df: Pandas DataFrame 需要检查的数据集
    :param column: str 需要检查的列名
    :param value_range: tuple or list, 对于数值类型，预期的最小值和最大值范围，例如(0, 100) 如果为None，则不进行数值范围检查
    :param string_pattern: str, 对于字符串类型，正则表达式模式，用于匹配字符串是否符合命名规范。如果为None，则不进行字符串模式检查
    :return: list, 失败的检查详情列表 为空则全部通过
    '''

    # 初始化失败详情列表
    failed_checks = []

    # 检查列是否存在
    if column not in df.columns:
        failed_checks.append(f"列 '{column}' 不存在于DataFrame中")
        return failed_checks

    # 数值范围检查
    if value_range is not None and pd.api.types.is_numeric_dtype(df[column]):
        min_val, max_val = value_range
        if not (df[column] >= min_val).all() or not (df[column] <= max_val).all():
            failed_checks.append(f"列 '{column}' 中的值超出了预期范围 {value_range}")

    # 字符串命名规范检查
    if string_pattern is not None and pd.api.types.is_string_dtype(df[column]):
        pattern = re.compile(string_pattern)
        if not all(pattern.match(str(val)) for val in df[column]):
            failed_checks.append(f"列 '{column}' 中的部分字符串不符合命名规范 '{string_pattern}'")

    # 如果没有失败的检查，则表示所有检查都通过
    return failed_checks


def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    '''
    去除DataFrame中的重复数据。

    :param df: 输入的DataFrame
    :param subset: 指定考虑重复性的列，默认为None，考虑所有列
    :return: 去重后的DataFrame
    '''
    return df.drop_duplicates(subset=subset)


def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop', columns: list = None) -> pd.DataFrame:
    '''
    处理缺失值

    :param columns: 需要处理的列 可选 默认全部
    :param df: 输入的DataFrame
    :param strategy: 缺失值处理策略，可选'drop'删除、'mean'填充均值、'median'填充中位数
    :return: 处理后的DataFrame
    '''

    if strategy == 'drop':
        df = df.dropna() if columns is None else df.dropna(subset=columns)
    elif strategy == 'mean':
        if columns is None:
            df = df.fillna(df.mean())
        else:
            df[columns] = df[columns].fillna(df[columns].mean())
    elif strategy == 'median':
        if columns is None:
            df = df.fillna(df.median())
        else:
            df[columns] = df[columns].fillna(df[columns].median())
    else:
        raise ValueError('缺失值处理策略无效')

    return df


def merge_data(dfs: list, on: str = None, how: str = 'inner') -> pd.DataFrame:
    '''
    合并多个DataFrame; on为空上下连接,on不为空左右连接

    :param dfs: DataFrame列表
    :param on: 合并键，默认为None，此时需确保DataFrame可以按行自动对齐
    :param how: 合并方式，如'left', 'right', 'outer', 'inner'
    :return: 合并后的DataFrame
    '''
    res = dfs[0]
    if on is None:
        res = pd.concat(dfs, axis=0, join=how, ignore_index=True)
    else:
        for df in dfs[1:]:
            res = pd.merge(res, df, on=on, how=how)
    return res


def convert_data_type(df: pd.DataFrame, columns: list = None, new_type: type = str) -> pd.DataFrame:
    '''
    转换指定列的数据类型。

    :param df: 输入的DataFrame
    :param columns: 需要转换类型的列名列表 默认全部
    :param new_type: 新的数据类型 默认字符串
    :return: 转换类型后的DataFrame
    '''
    if columns is None:
        df = df.astype(new_type)
    else:
        df[columns] = df[columns].astype(new_type)
    return df


def perform_aggregation(df: pd.DataFrame, group_by: str or list, agg_func: dict) -> pd.DataFrame:
    '''
    对数据进行聚合计算。

    :param df: 输入的DataFrame
    :param group_by: 分组依据的列名或列名列表
    :param agg_func: 聚合函数字典，如{'column_name': 'sum'}
    :return: 聚合后的DataFrame
    '''
    return df.groupby(group_by).agg(agg_func)


def sample_extract(df: pd.DataFrame, columns: list = None, part: float = 0.1) -> pd.DataFrame:
    '''
    对数据进行样品抽样

    :param df: 输入的DataFrame
    :param columns: 需要抽取的数据列,默认全部
    :param part: 抽取比例 默认0.1,即10%
    :return: 抽样后的DataFrame
    '''
    return df.sample(frac=part) if columns is None else df[columns].sample(frac=part)


if __name__ == '__main__':
    # data1 = {'A': [1, 2, 3, 4, 10, -10], 'B': [4, 5, 6, 7, 10, -10], 'C': [1, 2, 3, 4, 10, -10]}
    # data2 = {'A': [3, 4, 5, 6], 'C': [7, 8, 9, 10]}
    # df1 = pd.DataFrame(data1)
    # df2 = pd.DataFrame(data2)

    # # 数据清洗：去除重复数据
    # cleaned_df = remove_duplicates(df1)
    #
    # # 数据整合：合并数据
    # merged_df = merge_data([df1, df2], on='A')
    #
    # # 数据转换：转换数据类型
    # converted_df = convert_data_type(merged_df, ['A'], str)
    #
    # # 数据计算：进行聚合
    # aggregated_df = perform_aggregation(converted_df, group_by='A', agg_func={'B': 'sum', 'C': 'mean'})
    #
    # print(aggregated_df)

    pass
