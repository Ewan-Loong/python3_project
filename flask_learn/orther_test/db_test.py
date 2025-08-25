#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/19 15:51
# @Author  : Ewan
# @File    : db_test.py
# @Description : 数据库操作测试

from core.db import *

if __name__ == '__main__':
    table = 'student'

    where = {
        'sex': "男",
        "department": ['计算机科学与技术学院', '艺术与设计学院']
    }

    in_objs = [
        {'id': '2022010202', 'name': '苏赴', 'birthday': '2004-06-16', 'speciality': '软件工程'},
        {'id': '2022020202', 'name': '陌石阡', 'birthday': '2004-05-08', 'speciality': '视觉传达设计'},
    ]

    up_objs = [
        {'id': '2022010202', 'sex': '女', 'department': '计算机科学与技术学院', 'height': 1.63, 'weight': 52},
        {'id': '2022020202', 'sex': '女', 'department': '艺术与设计学院', 'height': 1.64, 'weight': 51},
    ]

    de_objs = {'id': '2022030303'}

    # res = select_by_where(table, where)
    # res = insert_by_obj(table, in_objs)
    # res = update_by_obj(table, up_objs)
    # res = delete_by_obj(table, de_objs)

    # print(res)
    pass
