#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 按年龄分割excel/Excel segmentation by age
@file_name: segmentation_excel_by_age.py
@project: my_love
@version: 1.0
@date: 2018/11/19 21:52
@author: air
"""

import pandas as pd


def age(input_file, output_file):
    """
    按年龄分割excel文件
    :param input_file: 传入文件
    :param output_file: 输出文件
    :return:
    """
    df1 = pd.read_excel(input_file)
    df2 = pd.DataFrame(columns=['年龄'])
    new = pd.DataFrame(index=['0'], columns=['年龄'])
    for i in range(332):
        for j in range(8):
            df2 = df2.append(new, ignore_index=True)
            df2.iloc[8 * i + j, 0] = df1.iloc[i, 15 - j]
    df2.to_excel(output_file, index=False, encoding='utf-8')


if __name__ == '__main__':
    file1 = '改了年龄的数据.xlsx'
    file2 = '筛选数据.xlsx'
    age(file1, file2)
