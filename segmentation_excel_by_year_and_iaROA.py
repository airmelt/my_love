#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 按年份和iaROA分割excel/Excel segmentation by year and iaROA
@file_name: segmentation_excel_by_year_and_iaROA.py
@project: my_love
@version: 1.0
@date: 2018/11/15 09:25
@author: air
"""

import pandas as pd

df1 = pd.read_excel('300家.xlsx')
df = pd.read_excel('IAROA300.xlsx')
# 新建DataFrame, 相当于新建了一个excel文件
df2 = pd.DataFrame(columns=['证券代码', '证券简称', '年份', '总市值/元', '董事长', '公司年龄', '所属行业名称',
                            '市净率PB(LF)/倍', '资产负债率/%', '净资产收益率ROE(平均)/%', '总资产报酬率ROA/%', '总资产净利率ROA/%', '每股收益EPS-基本/元', '总资产/元', '总资产报酬率IAROA', '总资产净利率IAROA'])
# 新建一行空数据
new = pd.DataFrame(index=['0'], columns=['证券代码', '证券简称', '年份', '总市值/元', '董事长', '公司年龄', '所属行业名称',
                                         '市净率PB(LF)/倍', '资产负债率/%', '净资产收益率ROE(平均)/%', '总资产报酬率ROA/%', '总资产净利率ROA/%', '每股收益EPS-基本/元', '总资产/元', '总资产报酬率IAROA', '总资产净利率IAROA'])
for i in range(332):
  for j in range(8):
    # 插入新行, 忽略索引
    df2 = df2.append(new, ignore_index=True)
    df2.iloc[8 * i + j, 0] = df1.iloc[i, 0]                      # 证券代码
    df2.iloc[8 * i + j, 1] = df1.iloc[i, 1]                      # 证券简称
    df2.iloc[8 * i + j, 2] = 2010 + j                            # 年份
    df2.iloc[8 * i + j, 3] = df1.iloc[i, 2]                      # 总市值/元
    df2.iloc[8 * i + j, 4] = df1.iloc[i, 3]                      # 董事长
    df2.iloc[8 * i + j, 5] = df1.iloc[i, 5] - 7 + j              # 公司年龄
    df2.iloc[8 * i + j, 6] = df1.iloc[i, 6]                      # 所属行业名称
    df2.iloc[8 * i + j, 7] = df1.iloc[i,
                                      7 + j]                     # 市净率PB(LF)/倍
    df2.iloc[8 * i + j, 8] = df1.iloc[i, 15 + j]                 # 资产负债率/%
    df2.iloc[8 * i + j, 9] = df1.iloc[i, 23 +
                                      j]                         # 净资产收益率ROE(平均)/%
    df2.iloc[8 * i + j, 10] = df1.iloc[i,
                                       31 + j]                   # 总资产报酬率ROA/%
    df2.iloc[8 * i + j, 11] = df1.iloc[i,
                                       39 + j]                   # 总资产净利率ROA/%
    df2.iloc[8 * i + j, 12] = df1.iloc[i,
                                       47 + j]                   # 每股收益EPS-基本/元
    df2.iloc[8 * i + j, 13] = df1.iloc[i, 55 + j]                # 总资产/元
    if (j > 2):
      df2.iloc[8 * i + j, 14] = df.iloc[i, 0 + j]
      df2.iloc[8 * i + j, 15] = df.iloc[i, 5 + j]
# 写出数据到excel, 忽略索引
df2.to_excel('year2.xlsx', index=False, encoding='utf-8')
