#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 从所有上市公司筛选300家上市公司数据/Data filter
@file_name: 300_file_filter.py
@project: my_love
@version: 1.0
@date: 2018/11/11 15:15
@author: air
"""

import pandas as pd


def select(from_file, filter_file):
    """
    根据传入文件筛选数据
    :param from_file: 选择该文件中出现的公司
    :param filter_file: 从该文件筛选公司
    :return:
    """
    df1 = pd.read_excel(from_file)
    df2 = pd.read_excel(filter_file)
    # writer = pd.ExcelWriter('C:\Users\air\Desktop\筛选数据.xlsx')
    # 选择df2中证券代码与df1中相同的
    index = df1[u'证券代码'].isin(df2[u'证券代码'])
    # 取得相同内容并输出为excel文件
    outfile = df1[index]
    outfile.to_excel(r'筛选数据.xlsx', index=False, encoding='utf-8')


if __name__ == '__main__':
    file1 = r'最最最后的指标.xlsx'
    file2 = r'300家.xlsx'
    select(file1, file2)
