#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 分割Excel/Excel segmentation
@file_name: segmentation_excel.py
@project: my_love
@version: 1.0
@date: 2019/04/21 17:08
@author: air
"""

__author__ = 'air'

import pandas as pd
import time


def segmentation_by_year(file_name, length=332, years=8):
    """
    按年份分割Excel
    :param file_name: 传入待分割的文件名
    :param length: 总长度
    :param years: 年份数
    :return:
    """
    input_file = file_name + '.xlsx'
    df1 = pd.read_excel(input_file)
    # 新建DataFrame, 相当于新建了一个excel文件
    df2 = pd.DataFrame(columns=['证券代码', '证券简称', '总市值/元', '所属行业名称', '每股收益EPS-扣除/基本(元)',
                                '净资产收益率ROE(扣除/加权)(%)', '总资产报酬率ROA(%)', '资产负债率(%)', '市净率PB(LF)(倍)',
                                '年份'])
    new = pd.DataFrame(index=['0'], columns=['证券代码', '证券简称', '总市值/元', '所属行业名称', '每股收益EPS-扣除/基本(元)',
                                             '净资产收益率ROE(扣除/加权)(%)', '总资产报酬率ROA(%)', '资产负债率(%)',
                                             '市净率PB(LF)(倍)', '年份'])
    for i in range(length):
        for j in range(years):
            # 插入新行, 忽略索引
            df2 = df2.append(new, ignore_index=True)
            df2.iloc[8 * i + j, 0] = df1.iloc[i, 0]             # 证券代码
            df2.iloc[8 * i + j, 1] = df1.iloc[i, 1]             # 证券简称
            df2.iloc[8 * i + j, 2] = df1.iloc[i, 2]             # 总市值/元
            df2.iloc[8 * i + j, 3] = df1.iloc[i, 59]            # 所属行业名称
            df2.iloc[8 * i + j, 4] = df1.iloc[i, 3 + j]         # 每股收益EPS-扣除/基本(元)
            df2.iloc[8 * i + j, 5] = df1.iloc[i, 12 + j]        # 净资产收益率ROE(扣除/加权)(%)
            df2.iloc[8 * i + j, 6] = df1.iloc[i, 21 + j]        # 总资产报酬率ROA(%)
            df2.iloc[8 * i + j, 7] = df1.iloc[i, 30 + j]        # 资产负债率/%
            df2.iloc[8 * i + j, 8] = df1.iloc[i, 39 + j]        # 市净率PB(LF)(倍)
            df2.iloc[8 * i + j, 9] = 2010 + j                   # 年份
    # 写出数据到excel, 忽略索引
    df2.to_excel(file_name + time.strftime("%Y-%m-%d", time.localtime()) + '.xlsx', index=False, encoding='utf-8')


def industry(input_file, output_file, years=8):
    """
    按产业分割Excel
    :param input_file: 传入待分割的文件名
    :param output_file: 传出待分割的文件名
    :param years: 年份数
    :return:
    """
    df1 = pd.read_excel(input_file)
    df2 = pd.read_excel(output_file)
    # 采掘
    for i in range(3):
        for j in range(years):
            df2.iloc[3 * j + i, 11] = df1.iloc[0, 1 + j]
            df2.iloc[3 * j + i, 14] = 3
    # 传媒
    for i in range(15):
        for j in range(years):
            df2.iloc[15 * j + i + 24, 11] = df1.iloc[1, 1 + j]
            df2.iloc[15 * j + i + 24, 14] = 15
    # 电气设备
    for i in range(19):
        for j in range(years):
            df2.iloc[19 * j + i + 144, 11] = df1.iloc[2, 1 + j]
            df2.iloc[19 * j + i + 144, 14] = 19
    # 电子
    for i in range(35):
        for j in range(years):
            df2.iloc[35 * j + i + 296, 11] = df1.iloc[3, 1 + j]
            df2.iloc[35 * j + i + 296, 14] = 35
    # 房地产
    for i in range(28):
        for j in range(years):
            df2.iloc[28 * j + i + 576, 11] = df1.iloc[4, 1 + j]
            df2.iloc[28 * j + i + 576, 14] = 28
    # 纺织服装
    for i in range(5):
        for j in range(years):
            df2.iloc[5 * j + i + 800, 11] = df1.iloc[5, 1 + j]
            df2.iloc[5 * j + i + 800, 14] = 5
    # 非银金融
    for i in range(1):
        for j in range(years):
            df2.iloc[1 * j + i + 840, 11] = df1.iloc[6, 1 + j]
            df2.iloc[1 * j + i + 840, 14] = 1
    # 钢铁
    for i in range(1):
        for j in range(years):
            df2.iloc[1 * j + i + 848, 11] = df1.iloc[7, 1 + j]
            df2.iloc[1 * j + i + 848, 14] = 1
    # 公用事业
    for i in range(13):
        for j in range(years):
            df2.iloc[13 * j + i + 856, 11] = df1.iloc[8, 1 + j]
            df2.iloc[13 * j + i + 856, 14] = 13
    # 国防军工
    for i in range(5):
        for j in range(years):
            df2.iloc[5 * j + i + 960, 11] = df1.iloc[9, 1 + j]
            df2.iloc[5 * j + i + 960, 14] = 5
    # 化工
    for i in range(22):
        for j in range(years):
            df2.iloc[22 * j + i + 1000, 11] = df1.iloc[10, 1 + j]
            df2.iloc[22 * j + i + 1000, 14] = 22
    # 机械设备
    for i in range(17):
        for j in range(years):
            df2.iloc[17 * j + i + 1176, 11] = df1.iloc[11, 1 + j]
            df2.iloc[17 * j + i + 1176, 14] = 17
    # 计算机
    for i in range(24):
        for j in range(years):
            df2.iloc[24 * j + i + 1312, 11] = df1.iloc[12, 1 + j]
            df2.iloc[24 * j + i + 1312, 14] = 24
    # 家用电器
    for i in range(8):
        for j in range(years):
            df2.iloc[8 * j + i + 1504, 11] = df1.iloc[13, 1 + j]
            df2.iloc[8 * j + i + 1504, 14] = 8
    # 建筑材料
    for i in range(7):
        for j in range(years):
            df2.iloc[7 * j + i + 1568, 11] = df1.iloc[14, 1 + j]
            df2.iloc[7 * j + i + 1568, 14] = 7
    # 建筑装饰
    for i in range(11):
        for j in range(years):
            df2.iloc[11 * j + i + 1624, 11] = df1.iloc[15, 1 + j]
            df2.iloc[11 * j + i + 1624, 14] = 11
    # 交通运输
    for i in range(6):
        for j in range(years):
            df2.iloc[6 * j + i + 1712, 11] = df1.iloc[16, 1 + j]
            df2.iloc[6 * j + i + 1712, 14] = 6
    # 农林牧渔
    for i in range(11):
        for j in range(years):
            df2.iloc[11 * j + i + 1760, 11] = df1.iloc[17, 1 + j]
            df2.iloc[11 * j + i + 1760, 14] = 11
    # 汽车
    for i in range(9):
        for j in range(years):
            df2.iloc[9 * j + i + 1848, 11] = df1.iloc[18, 1 + j]
            df2.iloc[9 * j + i + 1848, 14] = 9
    # 轻工制造
    for i in range(7):
        for j in range(years):
            df2.iloc[7 * j + i + 1920, 11] = df1.iloc[19, 1 + j]
            df2.iloc[7 * j + i + 1920, 14] = 7
    # 商业贸易
    for i in range(7):
        for j in range(years):
            df2.iloc[7 * j + i + 1976, 11] = df1.iloc[20, 1 + j]
            df2.iloc[7 * j + i + 1976, 14] = 7
    # 食品饮料
    for i in range(7):
        for j in range(years):
            df2.iloc[7 * j + i + 2032, 11] = df1.iloc[21, 1 + j]
            df2.iloc[7 * j + i + 2032, 14] = 7
    # 通信
    for i in range(10):
        for j in range(years):
            df2.iloc[10 * j + i + 2088, 11] = df1.iloc[22, 1 + j]
            df2.iloc[10 * j + i + 2088, 14] = 10
    # 休闲服务
    for i in range(3):
        for j in range(years):
            df2.iloc[3 * j + i + 2168, 11] = df1.iloc[23, 1 + j]
            df2.iloc[3 * j + i + 2168, 14] = 3
    # 医药生物
    for i in range(42):
        for j in range(years):
            df2.iloc[42 * j + i + 2192, 11] = df1.iloc[24, 1 + j]
            df2.iloc[42 * j + i + 2192, 14] = 42
    # 有色金属
    for i in range(13):
        for j in range(years):
            df2.iloc[13 * j + i + 2528, 11] = df1.iloc[26, 1 + j]
            df2.iloc[13 * j + i + 2528, 14] = 13
    # 综合
    for i in range(3):
        for j in range(years):
            df2.iloc[3 * j + i + 2632, 11] = df1.iloc[27, 1 + j]
            df2.iloc[3 * j + i + 2632, 14] = 3
    df2.to_excel(output_file, index=False, encoding='utf-8')


def calculate_iaroa(input_file):
    """
    计算IAROA
    :param input_file: 传入待计算的文件名
    :return:
    """
    df1 = pd.read_excel(input_file)
    for i in range(332):
        n = df1.iloc[i, 14]

        if n == 1:
            df1.iloc[i, 12] = df1.iloc[i, 10]
            df1.iloc[i, 13] = df1.iloc[i, 11]
        else:
            for j in range(8):
                roa = df1.iloc[8 * i + j, 6]
                iaroa = df1.iloc[8 * i + j, 10]
                df1.iloc[8 * i + j, 12] = roa - (iaroa - roa) / (n - 1)
                iaroa = df1.iloc[8 * i + j, 11]
                df1.iloc[8 * i + j, 13] = roa - (iaroa - roa) / (n - 1)
            for j in range(5):
                df1.iloc[8 * i + j + 3, 12] = (df1.iloc[8 * i + j + 2, 15] + df1.iloc[8 * i + j + 1, 15]
                                               + df1.iloc[8 * i + j, 15]) / 3
                df1.iloc[8 * i + j + 3, 13] = (df1.iloc[8 * i + j + 2, 16] + df1.iloc[8 * i + j + 1, 16]
                                               + df1.iloc[8 * i + j, 16]) / 3
            for j in range(3):
                df1.iloc[8 * i + j, 12] = None
                df1.iloc[8 * i + j, 13] = None
    df1.to_excel(input_file, index=False, encoding='utf-8')
