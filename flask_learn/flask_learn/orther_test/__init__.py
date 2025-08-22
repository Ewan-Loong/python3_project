#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/21 16:22
# @Author  : LYF
# @File    : __init__.py.py
# @Software: IntelliJ IDEA

import xml.etree.ElementTree as ET


def query_by_filters(model_class, filters):
    """
    根据传入的过滤条件字典动态构建查询
    :param model_class: ORM模型类
    :param filters: 查询条件字典，键为字段名，值为过滤条件
    :return: 查询结果
    """
    query = model_class.query  # 获取查询对象
    for field, value in filters.items():
        # 动态添加过滤条件
        query = query.filter(getattr(model_class, field) == value)

    return query.all()


# 读取xml文件
def iterate_over_xml(node):
    """递归遍历XML节点"""
    # 处理当前节点的标签和文本内容（如果存在）
    print(f"Node 标签: {node.tag}, Node 内容: {node.text.strip() if node.text else 'None'}")

    # 遍历当前节点的所有属性
    for attr_name, attr_value in node.attrib.items():
        print(f"属性: {attr_name} = {attr_value}")

    # 递归遍历子节点
    for child in node:
        iterate_over_xml(child)


if __name__ == '__main__':
    filters = {"name": "Alice", "age": 30}
    # ss = query_by_filters(Student, filters)
    # for s in ss:
    #     print(s.name, s.age)

    # 解析XML文件
    # tree = ET.parse('example.xml')
    # root = tree.getroot()
    # iterate_over_xml(root)

    # print(f'{12:0>3}')
    pass
