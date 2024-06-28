#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/23 13:58
# @Author  : LYF
# @File    : app.py
# @Software: IntelliJ IDEA
import importlib
import logging
from pathlib import Path
from flask import Flask, render_template
from flask.logging import default_handler

from core.db import init_db
from werkzeug.exceptions import HTTPException
from services import *
from settings.flask_config import config
from settings.flask_logger import file_handler, api_format

app = Flask(__name__)


def create_app(conf="dev"):
    # instance_relative_config :  告诉应用配置文件是相对于 instance folder 的相对路径。
    app.config.from_object(config.get(conf))
    # print(app.config)

    # 中文返回
    # app.json.ensure_ascii = False

    # 日志记录器调整 重置默认日志输出格式
    # app.logger.handlers[0].setFormatter(api_format)
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(file_handler)

    # 测试路由
    @app.route('/')
    def hello():
        return render_template('/test/index.html')

    @app.before_request
    def log_quest():
        app.logger.info(None)

    # @app.before_request
    # def req_test():
    #     request.json = json.loads(request.bp)

    # 注册蓝图 改用配置文件
    # app.register_blueprint(bp)

    # 获取蓝图 注册
    route_list = ['services', 'services/hrms']
    for r in route_list:
        route_files = [f.stem for f in Path(r).glob('*.py') if f.stem != '__init__']

        for route_file in route_files:
            module = importlib.import_module(f"{r.replace('/', '.')}.{route_file}")
            router = getattr(module, "bp", None)
            if router is not None:
                app.register_blueprint(router)

    # 初始化数据库
    init_db()

    # 结束app时断开数据库
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # 通用错误处理
    @app.errorhandler(Exception)
    def error_handling(e):
        app.logger.error(e)
        if isinstance(e, HTTPException):
            return e
        return e, 500

    return app


if __name__ == '__main__':
    create_app()
    # print('路由:', [str(url) for url in app.url_map.iter_rules()])
    app.run(host='0.0.0.0', port=5000)

# 设置环境变量
# set PYTHONPATH=G:\py_workspace\flask_learn;
# 手动启动
# flask --app app:create_app() run -h 0.0.0.0 -p 5000

# 这种方式为动态的添加路由 一般不用 常采用构建蓝图工厂的形式
# def add_route(func):
#     url = os.path.abspath(__file__) + '/' + func.__name__
#     print('正在添加路由:{}'.format(url))
#
#     def inner():
#         create_app().add_url_rule(url, view_func=func, methods=['POST'])
#
#     return inner
