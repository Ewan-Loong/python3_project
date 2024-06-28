#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 12:13
# @Author  : LYF
# @File    : generate_data.py
# @Description : 生成随机数据

from random_data import *

if __name__ == '__main__':
    print("正在生成数据中...")

    filepath = 'E:/tmp/sr_test.csv'
    f1 = open(filepath, 'w')
    clos = ['v_vin', 'v_send_time', 'v_date', 'v_time', 'v_speed', 'v_atmospheric_pressure', 'v_output_torque',
            'v_friction_torque', 'v_engine_speed', 'v_engine_fuel_flow', 'v_scr_up_nox', 'v_scr_down_nox',
            'v_reagent_margin', 'v_intake_air_volume', 'v_scr_inlet_temperature', 'v_scr_outlet_temperature', 'v_dpf',
            'v_engine_coolant_temperature', 'v_oil_tank_level', 'v_positioning_status', 'v_lng', 'v_lat',
            'v_accumulated_mileage', 'v_year', 'v_month', 'v_day', 'v_type', 'flag']
    f1.write(','.join(clos) + '\n')
    n = 2018
    dt = {}
    for i in range(1, 1101):
        v_vin = mk_uuid()
        v_send_time = mk_time2('{}-01-01'.format(n), '{}-12-31'.format(n), out_str='datetime')
        v_date = parse(v_send_time).strftime("%Y-%m-%d")
        v_time = v_send_time
        v_speed = str(mk_num())
        v_year = parse(v_send_time).strftime("%Y")
        v_month = parse(v_send_time).strftime("%m")
        v_day = parse(v_send_time).strftime("%d")

        line = [v_vin, v_send_time, v_date, v_time, v_speed, '97.0', '43', '7', '1296', '5.05', '425.75', '-0.5',
                '57.2', '98.5', '298.512350', '266.43750', '1.40', '83', '48.4', '1', '106.29195', '29.522', '65.600',
                v_year, v_month, v_day]
        f1.write(','.join(line) + '\n')
        if i % 100 == 0:
            f1.flush()
            print('{} make done'.format(n))
            n += 1
        i += 1

    print("all done")
    pass
