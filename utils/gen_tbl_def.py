#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/24 17:16
# @Author  : LYF
# @File    : gen_tbl_def.py
# @Description : 自动化生成sqlalchemy的表声明定义
import os
import re

from sqlalchemy import create_engine, MetaData

# 模板 template
class_tmpl = """# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.types import *
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class {table_name}(Base):  
    __tablename__ = '{table_name}'  
  
{fields}
"""

col_tmpl = "    {0} = Column('{1}', {2},{3} comment='{4}')\n"


def gen_sql(url, out_dir, schema, table=None):
    '''
    :param url: 数据库连接的完整路径
    :param out_dir: 输出目录 如果不存在会自动创建
    :param schema: 指定导出的库名 str
    :param table: 可选 指定导出的表列表 [str,...]
    :return: None
    '''

    # 获取文件路径的目录部分
    directory = os.path.dirname(out_dir + '/' + schema + '/')
    # 如果目录不存在，则创建目录
    if not os.path.exists(directory):
        print(f'dir: {directory} Created')
        os.makedirs(directory)

    engine = create_engine(url, echo=True)
    metadata = MetaData()
    # 加载表 表很多的时候执行时间会变长
    metadata.reflect(bind=engine, schema=schema, only=table)
    tables = metadata.tables

    # 遍历 tables 来查看表结构
    # for table_name, table in tables.items():
    #     print("Table: {}".format(table_name))
    #     print(table.columns.keys())

    # 遍历表，生成代码
    for table_name, table in tables.items():
        fields = ''
        for col in table.columns:
            col_type = str(col.type)
            # 简单处理字段类型 该处请根据需求调整
            # FIXME 对不同数据库类型可能存在问题 -> 如oracle NUMBER类型
            #  没有对数据类型做统一映射,若跨数据库建表会存在问题
            if ')' in col_type:
                col_type = re.findall(r'.*\)', col_type)[0]

            # FIXME 如果字段名为中文(MySQL支持),会输出变量名为中文的变量
            field = col_tmpl.format(col.name, col.name, col_type,
                                    ' primary_key=True,' if col.primary_key else '', col.comment if col.comment else '')

            fields += field

        class_code = class_tmpl.format(table_name=table.name, fields=fields)
        # print(class_code)

        # 写入文件
        with open(f'{directory}/{table.name}.py', 'w', encoding='utf-8') as file:
            file.write(class_code)
            print(f'{directory}/{table.name}.py write done')


if __name__ == '__main__':
    # Mysql8
    # gen_sql("mysql+pymysql://root:root@localhost:3306", '../models', 'py3_dev')

    # oracle19c PDB
    # gen_sql("oracle+cx_oracle://system:oracle@192.168.2.136:1521/?service_name=p_dev", '../models', 'DEV_DB')
    pass
