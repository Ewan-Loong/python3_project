#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/9 17:02
# @Author  : LYF
# @File    : random_data.py
# @Software: IntelliJ IDEA
import random
import time
import uuid
from datetime import timedelta

from dateutil.parser import parse

__doc__ = '随机数据生成工具'

import pandas as pd


def mk_category(k=None):
    categorys = "服装 运动 美妆 数码 家电 食品 厨房用品 书籍 教育用品 医药 饰品".split(' ')
    if not k:
        k = random.randint(1, 6)
    cs = random.sample(categorys, k=k)
    return cs


def mk_brand():
    with open('E:/pywork/wyhc/data_oracle/brand.txt', 'r') as file:
        brand = file.readlines()
    return random.choice(brand).replace('\n', '')


def mk_colors(k=None):
    colors = "白色 柠檬黄 淡黄 中黄 土黄 桔黄 桔红 肉色 朱红 大红 土红 桃红 " \
             "玫瑰红 深红 黄绿 粉绿 淡绿 浅绿 中绿 草绿 橄榄绿 翠绿 墨绿 湖蓝 " \
             "天蓝 钴蓝 群青 普蓝 紫罗兰 青莲 普兰 灰色 赭石 熟褐 黑色".split(' ')
    if not k:
        k = random.randint(1, 11)
    cs = random.sample(colors, k=k)
    c = random.choice(cs)
    return c, cs


def mk_series(s=2018, e=2020):
    years = [year for year in range(s, e)]
    season = ['-春', '-夏', '-秋', '-冬']
    return str(random.choice(years)) + random.choice(season)


def mk_edtype():
    return random.choice(['A', 'D', 'E'])


def mk_sizes():
    sizes = "s m l xl xxl".split(' ')
    k = random.randint(1, 5)
    ss = random.sample(sizes, k=k)
    s = random.choice(ss)
    return s, ss


def mk_s_age():
    ages = "baby children teenagers youth middle-aged old".split(' ')
    k = random.randint(1, 5)
    agess = random.sample(ages, k)
    sa = random.choice(agess)
    return sa, agess


def mk_s_sex():
    return random.choice(['man', 'woman', 'men&women'])


def mk_discount():
    is_d = mk_tf()
    d = 'No discount'
    if is_d:
        d = random.choice(['50% off', '60% off', '70% off', '80% off', '85% off', '90% off'])
    return str(is_d), d


def mk_price():
    p = random.randint(5, 1000)
    p_max = p + random.randint(5, 100)
    p_min = p
    if p > 100:
        p_min = p - random.randint(5, 100)
    return str(p), str(p_max), str(p_min)


def mk_shipping():
    s = mk_tf()
    f = 0 if s else random.choice([10.0, 15.0, 20.0, 25.0])
    return str(s), str(f)


def mk_tf():
    return random.choice([True, False])


# 输入可迭代对象 从里面选n个，范围可以是以分隔符分割的str
def mk_list_n(ranges, n=1, split=' '):
    ranges = ranges.split(split) if type(ranges) == str else ranges
    n = n if n < len(ranges) else len(ranges)
    return random.sample(ranges, n)


# 生成uuid 并去除 -
def mk_uuid():
    suid = ''.join(str(uuid.uuid4()).split('-'))
    return suid


# 从指定时间范围生成时间
def mk_time(s_time=None, e_time=None, str_f="%Y-%m-%d %H:%M:%S"):
    # 默认开始时间(当前时间减去365天) 结束时间
    s_time = int(time.mktime(time.strptime(s_time, '%Y-%m-%d %H:%M:%S'))) if s_time else int(time.time()) - 31536000
    # s_time = int(parse(s_time)) if s_time else int(time.time()) - 31536000
    # int强转是为了除去毫秒 即浮点位
    e_time = int(time.mktime(time.strptime(e_time, '%Y-%m-%d %H:%M:%S'))) if e_time else int(time.time())
    t = random.randint(s_time, e_time)
    date_tuple = time.localtime(t)  # 将时间戳生成时间元组
    date = time.strftime(str_f, date_tuple)  # 将时间元组转成格式化字符串
    return date


def mk_time2(start_t, end_t, out_str="date", format=None):
    dt_format = {"date": "%Y-%m-%d", "datetime": "%Y-%m-%d %H:%M:%S", "time": "%H:%M:%S"}
    if out_str not in dt_format.keys() and format is None:
        raise ValueError("输出日期格式化字符串非法")
    start_time = parse(start_t)
    end_time = parse(end_t)
    if start_time >= end_time:
        raise ValueError("结束时间必须晚于起始时间")
    time_diff = (end_time - start_time).total_seconds()  # 计算时间范围内的总秒数
    random_offset = timedelta(seconds=random.uniform(0, time_diff))  # 随机选择一个时间偏移量
    random_time = start_time + random_offset
    return random_time.strftime(format) if format else random_time.strftime(dt_format.get(out_str))


# 以开始结束范围生成数字 is_f 是否浮点数
def mk_num(s_range=0, e_range=100, is_f=False):
    method = random.uniform if is_f else random.randint
    return method(s_range, e_range)


# 洗牌
def mk_shuffle(ls):
    return random.shuffle(ls)


# 随机生成假身份证 注意校验位是真实的计算公式
def mk_id(st, et, sex=None):
    df = pd.read_csv('./行政区划代码.csv', dtype={'行政区划代码': str, '单位名称': str}, header=0)
    xz_list = df['行政区划代码'].dropna().tolist()
    sex_num = mk_num(0, 9)  # 男奇数 女偶数
    if sex == 'man':
        sex_num = (sex_num * 2 + 1) % 10
    elif sex == 'woman':
        sex_num = (sex_num * 2) % 10
    id17 = mk_list_n(xz_list)[0] + mk_time2(st, et, format="%Y%m%d") + str(mk_num(0, 9)) + str(
        mk_num(0, 9)) + str(sex_num)
    # 行政区 + 生日 + 00~99 + 0~9 + 校验码如下
    # [ 7 9 10 5 8 4 21 6 3 7 9 10 5 8 4 2 ] 求余 11
    id18 = 0
    for x, y in zip([x for x in id17], [7, 9, 10, 5, 8, 4, 21, 6, 3, 7, 9, 10, 5, 8, 4, 2]):
        id18 = id18 + int(x) * y
    id18 = id18 % 11
    return id17 + str(id18) if id18 != 10 else id17 + 'X'


# 随机生成手机号
def mk_phone(mac_type=None):
    mac_dict = {
        # 中国电信号段
        "dx": ['133', '153', '173', '177', '180', '181', '189', '190', '191', '193', '199'],
        # 中国联通号段
        "lt": ['130', '131', '132', '155', '156', '166', '167', '171', '175', '176', '185', '186', '196'],
        # 中国移动号段
        "yd": ['134', '135', '136', '137', '138', '139', '148', '150', '151', '152', '157', '158', '159',
               '172', '178', '182', '183', '184', '187', '188', '195', '197', '198'],
        "gd": ['192']  # 中国广电号段
    }
    if mac_type and mac_type in mac_dict.keys():
        mac = mk_list_n(mac_dict.get(mac_type))[0]
    else:
        mac = mk_list_n(mac_dict['dx'] + mac_dict['lt'] + mac_dict['yd'] + mac_dict['gd'])[0]
    phone8 = '{:0>8}'.format(mk_num(0, 9999999))
    return mac + phone8


# 按行写入数据 txt文件
def mk_to_txt(lines, path):
    print("数据写入路径:" + path)
    total = len(lines)
    with open(path, "w") as file:
        done = 1
        for item in lines:
            file.write(','.join(item) + '\n')
            done += 1
            if (done / total) * 100 % 10 == 0:
                print("进度:" + str((done / total) * 100) + "%")
    print("写入完成")


# 将数据写入文件
def mk_to_file(lines, name, path='E:/tmp', ftype='csv'):
    df = pd.DataFrame(lines[1:], columns=lines[0])
    if ftype == 'csv':
        df.to_csv(f'{path}/{name}.csv', index=False)
    elif ftype == 'xlsx':
        df.to_excel(f'{path}/{name}.xlsx', index=False)
    else:
        print('ftype 仅支持 csv xlsx')
    print("写入完成")


def mk_record():
    print("正在生成数据中...")
    filepath = 'E:/tmp/' + mk_uuid() + '.txt'
    f1 = open(filepath, 'w')
    num = 0
    while True:
        date_source = '测试--数据源'
        table_name = mk_brand()
        check_time = '2022-11-28'
        filed_name = mk_category(1)
        count = str(random.randint(1, 10000))

        line = [date_source, table_name, check_time, filed_name[0], filed_name[0], count]
        f1.write(','.join(line) + '\n')
        num += 1
        if num >= 1000:
            f1.flush()
            f1.close()
            break
    print("done")


if __name__ == '__main__':
    # mk_data(Queue())
    # print mk_uuid()
    # mk_record()

    # res = mk_list_n('a,b,c,d,e', 2, ',')
    # print(res)

    # lines = []
    # lines.append(['时间','机构','资产端金额','负债端金额','账上可用资金余额'])
    # for i in range(2000):
    #     op_time = mk_time(s_time='2023-05-15 00:00:00',e_time='2024-05-15 00:00:00')
    #     name = mk_list_n('交子新兴,金控租赁,金控典当,金控小贷,交子保理',1,',')[0]
    #     zcbal = mk_num(5000000,500000000,True)
    #     fzbal = mk_num(5000000,500000000,True)
    #     zsbal = mk_num(5000000,500000000,True)
    #
    #     line = [op_time, name, str(zcbal), str(fzbal), str(zsbal)]
    #     lines.append(line)
    #
    # mk_to_txt(lines, "E:/tmp/test1.txt")

    # lines = []
    # lines.append(['时间', '项目编号', '五级分类', '还款方式', '还本金额', '付息金额'])
    # while True:
    #     ac_time = mk_time(s_time='2023-01-01 00:00:00', e_time='2023-06-30 00:00:00')
    #     pro_id = mk_list_n('A01,A02,A03,B01,B02,B03,C01,C02,C03,D01,D02,D03', 1, ',')[0]
    #     risk = mk_list_n('正常,关注,次级,可疑,损失', 1, ',')[0]
    #     pay_type = mk_list_n('正常还款,逾期还款,提前还款,核销,核销后回收', 1, ',')[0]
    #     bj = mk_num(10000, 999999, True)
    #     lx = mk_num(1000, 99999, True)
    #
    #     line = [ac_time, pro_id, risk, pay_type, str(bj), str(lx)]
    #     lines.append(line)
    #
    #     if len(lines) > 10000:
    #         print('done')
    #         break
    #
    # mk_to_txt(lines, "E:/tmp/hk.csv")

    # for i in range(1, 10):
    #     print(mk_id('1980-01-01', '1985-12-31', 'woman'))

    for i in range(1, 10):
        print(mk_phone('lt'))

    pass
