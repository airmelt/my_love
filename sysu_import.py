#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: import file
@file_name: sysu_import.py
@project: my_love
@version: 1.0
@date: 2020/12/14 11:47
@author: Air
"""

__author__ = 'Air'

import time
import pandas as pd


def import_file(input_file: str) -> None:
    df1 = pd.read_excel(input_file)
    df1 = df1[-df1['贷方发生额（收入）'].isin(['0.00'])]
    df = pd.DataFrame(columns=['业务日期', '来款单位', '摘要', '暂存科目', '金额'])
    new_row = pd.DataFrame(index=['0'], columns=['业务日期', '来款单位', '摘要', '暂存科目', '金额'])
    for i in range(df1.shape[0]):
        new_row['业务日期'] = time.strftime('%Y/%m/%d %H:%M:%S', time.strptime(df1.iloc[i, 2], "%Y%m%d %H:%M:%S"))
        new_row['来款单位'] = df1.iloc[i, 7]
        new_row['摘要'] = '款' if df1.iloc[i, 12] == '电子汇入' else df1.iloc[i, 12]
        cost = format(df1.iloc[i, 4], ',')
        if cost.find('.') == len(cost) - 2:
            cost += '0'
        new_row['金额'] = cost
        df = df.append(new_row, ignore_index=True)
    df.to_excel('导入' + input_file, index=False, encoding='utf-8')


if __name__ == '__main__':
    import_file('')
