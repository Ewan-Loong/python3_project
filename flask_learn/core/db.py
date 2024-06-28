#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/26 14:03
# @Author  : LYF
# @File    : db.py
# @Software: IntelliJ IDEA
import types

from sqlalchemy import create_engine, Table
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from settings import flask_config

engine = create_engine(flask_config.DB_URI)
# 自动刷新和提交 False,使用 db_session.commit() 提交, 使用db_session.close() 关闭
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


# def new_method(self, filters):
#     query = self.query  # 获取查询对象
#     for field, value in filters.items():
#         # 动态添加过滤条件
#         query = query.filter(getattr(self, field) == value)
#     print("This is a new method.")
#     return query.all()
#
#
# Base.query_by_filter = types.MethodType(new_method, None)


def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    import models.hrms
    Base.metadata.create_all(bind=engine)

# 以下内容暂未搞懂
# click.command 定义一个名为 init-db 命令行,类似于用代码编写脚本

# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """清除现有数据并创建新表。"""
#     init_db()
#     click.echo('Initialized the database.')

# 把close_db 和 init_db_command 注册到app
# app.cli.add_command() 添加一个新的 可以与 flask 一起工作的命令；直接使用 flask init-db

# def init_app(app):
#     app.cli.add_command(init_db_command)
