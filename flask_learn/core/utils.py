#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/23 15:56
# @Author  : LYF
# @File    : utils.py
# @Description : 其他工具类
import json
from json import JSONEncoder
import datetime
import uuid
from decimal import Decimal


# sql查询结果类型处理 Fixme 可能有遗漏
def sql_type_hand(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    else:
        return obj


# 序列化查询结果
def to_json(obj):
    res = {}
    for i in obj.__table__.columns.keys():
        res[i] = obj.__getattribute__(i)
    return res


def to_json2(objs):
    objs = objs if isinstance(objs, list) else [objs]
    res = []
    for item in objs:
        temp = {}
        for key in item.__table__.columns.keys():
            temp[key] = sql_type_hand(getattr(item, key))
        res.append(temp)
    return res
    # return json.dumps(res, cls=DataEncoder, ensure_ascii=False)


# json转码时 处理date datetime类型的数据
class DataEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        else:
            return JSONEncoder.default(self, obj)
