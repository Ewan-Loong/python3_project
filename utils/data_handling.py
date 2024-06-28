#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/6 17:34
# @Author  : LYF
# @File    : data.py
# @Software: IntelliJ IDEA

import hashlib
import re

__doc__ = '数据处理工具'


def get_str_enc(message, mode='md5', salt=None):
    """
    返回文本的加密值
    :param message: 加密文本
    :param mode: 加密方法
    :param salt: 加盐文本
    :return:结果值
    """
    message = message if isinstance(message, str) else str(message)
    if mode in hashlib.algorithms_available:
        en_message = hashlib.new(mode, message.encode('utf-8'))
    else:
        raise KeyError('加密算法{}未找到'.format(mode))

    # 加盐处理:在原明文后面添加n位随机数,再加密 提高密文等级
    if salt:
        salt = salt if isinstance(salt, str) else str(salt)
        en_message.update(salt.encode('utf-8'))

    return en_message.hexdigest()


rex_dict = {
    'Email': r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$',
    'MobilePhone': r'^((\(\d{2,3}\))|(\d{3}\-))?(\(0\d{2,3}\)|0\d{2,3}-)?[1-9]\d{6,7}(\-\d{1,4})?$',
    'LinePhone': r'^((\(\d{2,3}\))|(\d{3}\-))?13\d{9}$',
    'Chinese': r'^[\u0391-\uFFE5]+$',
    'IP_Address': r'(\d+)\.(\d+)\.(\d+)\.(\d+)',
    'IDNumber': r'^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$'
}


def get_str_match(message, rex_name=None, rex=None):
    """
    正则匹配
    :param message: 待匹配数据
    :param rex_name: 匹配规则名
    :param rex: 自定义匹配规则
    :return: 匹配结果
    """
    result = None
    # rex = "^[1-9]\\d{5}(18|19|20)\\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$"
    if not (rex or rex_name):
        print("请输入校验规则")
        return result
    elif rex_name:
        result = re.match(rex_dict[rex_name], message)
    elif rex:
        result = re.match(rex, message)

    if result:
        print('匹配结果', result.group())
    else:
        print("未匹配成功")
    return result


def get_str_hide(message, hide_args, hide_sub='*'):
    """
    字符串隐藏脱敏
    :param message: 隐藏的字符串
    :param hide_args: 隐藏字符参数 [规则,参1,参2]
    :param hide_sub: 替换的字符 默认*
    :return:脱敏后结果
    """
    # message = "四川省成都市武侯区12345有限公司"
    # hide1 = [1, 3, 3]  # 前后隐藏
    # hide2 = [2, 9, 9]  # 中间隐藏
    # hide_args = hide2
    message = message if isinstance(message, str) else str(message)
    en_message = message
    if hide_args[0] == 1:
        en_message = re.sub('^.{' + str(hide_args[1]) + '}', hide_sub * hide_args[1], message)
        en_message = re.sub('.{' + str(hide_args[2]) + '}$', hide_sub * hide_args[2], en_message)
    elif hide_args[0] == 2:
        en_head = message[0:hide_args[1]]
        if hide_args[2] > len(message[hide_args[1]:]):
            en_end = len(message[hide_args[1]:]) * hide_sub
        else:
            en_end = re.sub('^.{' + str(hide_args[2]) + '}', hide_sub * hide_args[2], message[hide_args[1]:])
        en_message = en_head + en_end
    else:
        pass
    print(en_message)
    return en_message


if __name__ == '__main__':
    # get_str_hide(13890711287, [2, 3, 4])
    get_str_match("123456789123456789", 'IDNumber')
    pass
