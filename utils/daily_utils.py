#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/26 14:04
# @Author  : LYF
# @File    : daily_utils.py
# @Software: IntelliJ IDEA

__doc__ = """日常工具类"""

from datetime import datetime, timedelta

from chinese_calendar import *


def solar_terms_count():
    """节气计算器"""
    base_count(get_solar_terms)
    return


def workdays_count():
    """工作日计算器"""
    base_count(get_workdays)
    return


def holidays_count():
    """假期计算器"""
    base_count(get_holidays)
    return


def date_mark():
    """工作日/节假日判断"""
    str_date = input("请输入日期,例{}\n".format(datetime.now().date()))
    dt = datetime.strptime(str_date, '%Y-%m-%d').date()

    if is_holiday(dt):
        print('{}是假期'.format(dt))
    if is_workday(dt):
        print('{}是工作日'.format(dt))


def date_diff():
    """日期区间天数计算"""
    str_date = input("请输入空格分割日期区间(开始日期缺省默认当天)\n").split(' ')
    dt_date = [datetime.strptime(i, '%Y-%m-%d').date() for i in str_date]
    if len(dt_date) == 1:
        dt_date.insert(0, datetime.today().date())
    if len(dt_date) > 2:
        print('输入错误,输入例如 {}[ {}]'.format(datetime.now().date(),
                                         datetime.now().replace(month=datetime.now().month + 3).date()))
    delta = dt_date[1] - dt_date[0] + timedelta(days=1)

    print("{}至{}共计{}天".format(dt_date[0], dt_date[1], delta.days))


def base_count(method):
    """base计算器"""

    while 1:
        str_date = input("请输入空格分割日期区间(截止日期缺省默认当天)\n")
        if str_date == '':
            print('格式输入错误,请重新输入,例如 {}[ {}]'.format(datetime.now().date(),
                                                   datetime.now().replace(month=datetime.now().month + 3).date()))
        else:
            dt_date = [datetime.strptime(i, '%Y-%m-%d').date() for i in str_date.split(' ')]
            if len(dt_date) == 2:
                break
            elif len(dt_date) == 1:
                dt_date.append(datetime.today().date())
                break
            else:
                print('日期区间个数错误,请重新输入,例如 {}[ {}]'.format(datetime.now().date(),
                                                         datetime.now().replace(month=datetime.now().month + 3).date()))

    days = method(dt_date[0], dt_date[1])
    out_info = {
        get_workdays: "{}至{}共计工作日:{}天,分别是:",
        get_holidays: "{}至{}共计假期:{}天,分别是:",
        get_solar_terms: "{}至{}共计节气:{}个,分别是:",
    }

    print(out_info[method].format(dt_date[0], dt_date[1], len(days)))

    if method == get_solar_terms:
        for i in range(len(days)):
            print(days[i][0], days[i][1], sep='_', end=' ') \
                if (i + 1) % 5 != 0 else print(days[i][0], days[i][1], sep='_')
    else:
        for i in range(len(days)):
            print(days[i], end=' ') if (i + 1) % 5 != 0 else print(days[i])
    print()
    return


def inter():
    while 1:
        count_type = input("请选择:1.工作日计算器 2.假期计算器 3.节气计算器 4.工作日判断 5.区间天数计算 0.退出\n")
        if count_type == '1':
            workdays_count()
        elif count_type == '2':
            holidays_count()
        elif count_type == '3':
            solar_terms_count()
        elif count_type == '4':
            date_mark()
        elif count_type == '5':
            date_diff()
        elif count_type == '0':
            print("EXIT")
            break
        else:
            print("选项错误,请重新输入")


if __name__ == '__main__':
    inter()
    pass
