#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/21 10:09
# @Author  : Ewan
# @File    : user_auth.py
# @Description : 用户认证

from flask import Blueprint, request
from core.db import db_session, select_by_where, insert_by_obj
from core.api_token import required_token, generate_token, verify_token

bp = Blueprint('user_auth', __name__, url_prefix='/UserAuth', template_folder='/templates')


@bp.route('/login', methods=['POST'])
def login():
    res = {'msg': '错误输入'}
    data = request.json
    if data and data['name'] and data['id']:
        user = select_by_where('user', data)
        if len(user) == 1:
            res['token'] = generate_token(user[0]['id'])
            res['msg'] = '登录成功'
        else:
            res['msg'] = '用户名或密码错误'
    return res


@bp.route('/refresh_token', methods=['POST'])
@required_token
def refresh_token():
    # TOKEN检查刷新
    new_token = verify_token(request.headers['Token'])
    return {'code': 0, 'msg': '更新成功', 'Token': new_token.get('Token')}


@bp.route('/create_user', methods=['POST'])
@required_token
def create_user():
    res = {'msg': '错误输入'}
    data = request.json
    if data:
        user = insert_by_obj('user', [data] if isinstance(data, dict) else data)
        if len(user) == len(data):
            res['msg'] = '创建成功'
    return res
