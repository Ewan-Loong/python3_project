#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/21 15:35
# @Author  : Ewan
# @File    : api_Token.py
# @Description : Token令牌工具
import functools
from datetime import timedelta, datetime
import time

import pytz
from flask import request
from itsdangerous import TimedSerializer, SignatureExpired, BadSignature
from settings.flask_config import config

# app密钥
SECRET_KEY = getattr(config, "SECRET_KEY", 'DEFAULT_SECRET_KEY')
EXPIRES_IN = getattr(config, "PERMANENT_SESSION_LIFETIME", timedelta(minutes=10))  # 过期时间默认10min
# EXPIRES_IN = timedelta(seconds=5)  # 测试用


def get_system_timezone():
    """获取当前系统时区"""
    # 尝试获取系统时区
    try:
        return pytz.timezone(time.tzname[time.localtime().tm_isdst])
    except:
        #  fallback: 使用本地时区
        return pytz.utc.localize(datetime.utcnow()).astimezone().tzinfo


def utc_to_local(utc_time):
    """将UTC时间转换为当地时间"""
    if not isinstance(utc_time, datetime):
        raise TypeError("输入必须是datetime对象")

    # 如果UTC时间没有时区信息，手动添加UTC时区
    if utc_time.tzinfo is None:
        utc_time = pytz.utc.localize(utc_time)

    # 获取系统时区
    local_tz = get_system_timezone()

    # 转换为当地时间
    return utc_time.astimezone(local_tz)


# 生成密钥 并补充过期时间
def generate_token(data, secret_key=SECRET_KEY):
    # , expires_in=EXPIRES_IN):
    s = TimedSerializer(secret_key)
    # expire = (datetime.now() + EXPIRES_IN).timestamp()
    # data.update({"exp": expires_in.seconds})
    return s.dumps(data)


# 校验Token / Token更新
def verify_token(t, secret_key=SECRET_KEY):
    resp = {'code': 0, 'msg': "Token处理成功", 'data': {}}
    s = TimedSerializer(secret_key)
    try:
        data, exp = s.loads(t, return_timestamp=True)
        resp['data'] = data
        now = datetime.now(pytz.timezone('UTC')).replace(microsecond=0)
        seconds = (now - exp).total_seconds()  # 剩余时间秒数
        # print(seconds, EXPIRES_IN.total_seconds())
        if seconds > EXPIRES_IN.total_seconds():
            raise SignatureExpired('Token过期')
        if seconds < EXPIRES_IN.total_seconds() / 2:  # 剩余有效时间小于过期时间的1/2重新生成
            resp['Token'] = generate_token(data, secret_key=secret_key)
            resp['msg'] = "Token更新成功"
    except Exception as e:
        raise e
    return resp


# 定义装饰器验证Token
def required_token(func):
    # flask的装饰器一定需要带上 @functools.wraps(func) 以保证最外层的函数名不变 且装饰器需要放置再最外层
    @functools.wraps(func)
    def required_inner(*arg, **kwargs):
        try:
            res = verify_token(request.headers['Token'])
            print('Token校验通过')
        except SignatureExpired:
            return {'code': -501, 'msg': "Token过期"}
        except BadSignature:
            return {'code': -502, 'msg': "Token校验失败"}
        except Exception as e:
            return {'code': -509, 'msg': str(e)}
        return func(*arg, **kwargs)

    return required_inner


if __name__ == '__main__':
    # 生成令牌
    Token = generate_token({'user': 'A01'})
    print("生成令牌:", Token)
    time.sleep(1)
    # 验证令牌
    res = verify_token(Token)
    print("验证令牌:", res)

    # # 示例用法
    # # 创建一个UTC时间（带时区信息）
    # utc_now = pytz.utc.localize(datetime.utcnow())
    # print(f"UTC时间: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    #
    # # 转换为当地时间
    # local_time = utc_to_local(utc_now)
    # print(f"当地时间: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    # print(f"系统时区: {local_time.tzinfo.zone}")
    pass
