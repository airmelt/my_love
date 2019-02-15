#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: iaROA数据生成/Calculate iaROA
    公式为 IAROA(i, t) = 1/3∑(k = 1, 3)[ROA(i, t - k) - (∑(N, j = 1)ROA(j, t - k) - ROA(i, t - k)) / (N - 1)]
    IAROA = 最近三年平均值(ROA - （行业∑ROA - ROA) / (N - 1)), 其中N表示行业数量
@file_name: calculate_IAROA.py
@project: my_love
@version: 1.0
@date: 2018/11/14 09:11
@author: air
"""


import pandas as pd

# 定义一个字典用来存储行业名称
# industries = {'采掘': 1, '化工': 2, '钢铁': 3, '有色金属': 4, '建筑材料': 5, '建筑装饰': 6, '电气设备': 7, '机械设备': 8, '国防军工': 9, '汽车': 10, '家用电器': 11, '纺织服装': 12, '轻工制造': 13,
#               '商业贸易': 14, '农林牧渔': 15, '食品饮料': 16, '休闲服务': 17, '医药生物': 18, '公用事业': 19, '交通运输': 20, '房地产': 21, '电子': 22, '计算机': 23, '传媒': 24, '通信': 25, '非银金融': 26, '综合': 27}
df1 = pd.read_excel(r'行业300家.xlsx')
# df2 = pd.read_excel(r'iaROA.xlsx')
# 相当于新建excel表
output = pd.DataFrame(columns=['证券代码', '证券简称', '行业', '总资产报酬率IAROA2013', '总资产报酬率IAROA2014', '总资产报酬率IAROA2015', '总资产报酬率IAROA2016',
                               '总资产报酬率IAROA2017', '总资产净利率IAROA2013', '总资产净利率IAROA2014', '总资产净利率IAROA2015', '总资产净利率IAROA2016', '总资产净利率IAROA2017'])
new = pd.DataFrame(index=['0'], columns=['证券代码', '证券简称', '行业', '总资产报酬率IAROA2013', '总资产报酬率IAROA2014', '总资产报酬率IAROA2015', '总资产报酬率IAROA2016',
                                         '总资产报酬率IAROA2017', '总资产净利率IAROA2013', '总资产净利率IAROA2014', '总资产净利率IAROA2015', '总资产净利率IAROA2016', '总资产净利率IAROA2017'])

for i in range(332):
    # 行业数量
    N = df1.iloc[i, 6]
    # 用来存放∑ROA的列表
    ROAs1 = [df1.iloc[i, 32], df1.iloc[i, 33], df1.iloc[i, 34], df1.iloc[i, 35],
             df1.iloc[i, 36], df1.iloc[i, 37], df1.iloc[i, 38], df1.iloc[i, 39]]
    ROAs2 = [df1.iloc[i, 48], df1.iloc[i, 49], df1.iloc[i, 50], df1.iloc[i, 51],
             df1.iloc[i, 52], df1.iloc[i, 53], df1.iloc[i, 54], df1.iloc[i, 55]]

    output = output.append(new, ignore_index=True)

    # 证券代码
    output.iloc[i, 0] = df1.iloc[i, 0]
    # 证券简称
    output.iloc[i, 1] = df1.iloc[i, 1]
    # 行业
    output.iloc[i, 2] = df1.iloc[i, 7]
    # 处理行业内只有1家机构的情况
    if int(N) == 1:
        for j in range(5):
            output.iloc[i, 3 + j] = ROAs1[3 + j]
            output.iloc[i, 8 + j] = ROAs2[3 + j]
    else:
        # 用来存放ROA(t - k)的列表
        ROAt1 = [df1.iloc[i, 40], df1.iloc[i, 41], df1.iloc[i, 42], df1.iloc[i, 43],
                 df1.iloc[i, 44], df1.iloc[i, 45], df1.iloc[i, 46], df1.iloc[i, 47]]
        ROAt2 = [df1.iloc[i, 56], df1.iloc[i, 57], df1.iloc[i, 58], df1.iloc[i, 59],
                 df1.iloc[i, 60], df1.iloc[i, 61], df1.iloc[i, 62], df1.iloc[i, 63]]
        for j in range(5):
            ROA11 = ROAt1[j] - (ROAs1[j] - ROAt1[j]) / (N - 1)
            ROA12 = ROAt1[j + 1] - (ROAs1[j + 1] - ROAt1[j + 1]) / (N - 1)
            ROA13 = ROAt1[j + 2] - (ROAs1[j + 2] - ROAt1[j + 2]) / (N - 1)
            ROA1 = (ROA11 + ROA12 + ROA13) / 3
            ROA21 = ROAt2[j] - (ROAs2[j] - ROAt2[j]) / (N - 1)
            ROA22 = ROAt2[j + 1] - (ROAs2[j + 1] - ROAt2[j + 1]) / (N - 1)
            ROA23 = ROAt2[j + 2] - (ROAs2[j + 2] - ROAt2[j + 2]) / (N - 1)
            ROA2 = (ROA21 + ROA22 + ROA23) / 3
            output.iloc[i, 3 + j] = ROA1
            output.iloc[i, 8 + j] = ROA2

# 写出数据到excel, 忽略索引
output.to_excel('IAROA300.xlsx', index=False, encoding='utf-8')
