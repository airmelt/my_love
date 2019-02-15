#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 按证券代码分割excel/Excel segmentation by stocks
@file_name: segmentation_excel_by_stocks.py
@project: my_love
@version: 1.0
@date: 2018/11/15 09:14
@author: air
"""

import pandas as pd

df1 = pd.read_excel('300家数据.xlsx')
# 新建DataFrame, 相当于新建了一个excel文件
df2 = pd.DataFrame(columns=['搜索数'])
# 新建一行空数据
new = pd.DataFrame(index=['0'], columns=['搜索数'])
for i in range(332):
  for j in range(8):
    # 插入新行, 忽略索引
    df2 = df2.append(new, ignore_index=True)
    df2.iloc[8 * i + j, 0] = df1.iloc[i, 24 + j]                      # 证券代码
# 写出数据到excel, 忽略索引
df2.to_excel('year3.xlsx', index=False, encoding='utf-8')
