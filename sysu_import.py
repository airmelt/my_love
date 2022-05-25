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
    key_dict = {'水费': '23072509', '电费': '23072509', '水电费': '23072509', '押金': '230720', '测试': '230503',
                '鉴定': '230503', '机时': '230503', '租金': '230503', '平台充值': '230503', '测试费': '230503',
                '鉴定费': '230503', '机时费': '230503', '机时服务费': '230503'}
    for i in range(df1.shape[0]):
        new_row['业务日期'] = time.strftime('%Y/%m/%d %H:%M:%S', time.strptime(df1.iloc[i, 2], "%Y%m%d %H:%M:%S"))
        new_row['来款单位'] = df1.iloc[i, 7]
        info = str(df1.iloc[i, 12])
        if info == '电子汇入':
            new_row['摘要'] = '款'
        elif info != 'nan':
            new_row['摘要'] = info
        else:
            new_row['摘要'] = ''
        if info in key_dict:
            new_row['暂存科目'] = key_dict[info]
        elif len(info) > 2 and info[-3:] in key_dict:
            new_row['暂存科目'] = key_dict[info[-3:]]
        elif len(info) > 2 and info[:3] in key_dict:
            new_row['暂存科目'] = key_dict[info[:3]]
        else:
            new_row['暂存科目'] = ''
        cost = format(df1.iloc[i, 4], ',')
        if cost.find('.') == len(cost) - 2:
            cost += '0'
        new_row['金额'] = cost
        df = df.append(new_row, ignore_index=True)
    df.to_excel('导入' + input_file, index=False, encoding='utf-8')


def check_file(file_name: str) -> None:
    df1 = pd.read_csv(file_name)
    df = pd.DataFrame(columns=['对账序号', '凭证日期', '凭证编号', '业务日期', '结算方式', '结算单号',
                               '摘要', '借方金额', '贷方金额', '对方单位', '说明'])
    for i in range(0, (df1.shape[0] >> 1), 2):
        if pd.isna(df1.iloc[i, 2]):
            num1 = str(df1.iloc[i + 1, 2])
            num2 = str(df1.iloc[i, 6])
        else:
            num1 = str(df1.iloc[i, 2])
            num2 = str(df1.iloc[i + 1, 6])
        if num1[-5:] != num2[1:6]:
            if pd.isna(df1.iloc[i, 5]) or df1.iloc[i + 1, 5] != df1.iloc[i, 5]:
                df = df.append(df1.iloc[i]).append(df1.iloc[i + 1])
    worse = pd.DataFrame(columns=['对账序号', '凭证日期', '凭证编号', '业务日期', '结算方式', '结算单号',
                                  '摘要', '借方金额', '贷方金额', '对方单位', '说明'])
    for i in range(0, (df.shape[0] >> 1), 2):
        num1, num2 = (str(df.iloc[i + 1, 2]), str(df.iloc[i, 6])) if pd.isna(df.iloc[i, 2]) \
            else (str(df.iloc[i, 2]), str(df.iloc[i + 1, 6]))
        if num2.startswith('南'):
            num2 = num2.replace('南', '', 1)
        if all(j.isdigit() for j in num2[:5]):
            if num1[-5:] != num2[:5]:
                worse = worse.append(df.iloc[i]).append(df.iloc[i + 1])
    df1 = df1.drop(df.index)
    df1.to_csv('right.csv', index=False, encoding='utf-8')
    worse.to_csv('worse.csv', index=False, encoding='utf-8')
    df = df.drop(worse.index)
    df.to_csv('wrong.csv', index=False, encoding='utf-8')
    add_csv_bom('wrong.csv')
    add_csv_bom('right.csv')
    add_csv_bom('worse.csv')


def add_csv_bom(input_file: str) -> None:
    with open(input_file, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('\ufeff' + content)


def filter_file(input_file: str) -> None:
    df1 = pd.read_excel(input_file, sheet_name='dgvTable', dtype=str)
    df = pd.DataFrame(columns=['凭证日期', '凭证字', '凭证编号', '摘要', '科目编号', '科目名称',
                               '借金额', '贷金额'])
    new_row = pd.DataFrame(index=['0'], columns=['凭证日期', '凭证字', '凭证编号', '摘要', '科目编号',
                                                 '科目名称', '借金额', '贷金额'])
    num_set = set()
    subject_set = {'10010101', '10020103', '1002010401', '1002010602', '100201250101', '101101',
                   '101102', '101103', '10020114'}
    fifty = 0
    hundred = 0
    fh = 0
    th = 0
    for i in range(df1.shape[0]):
        num = df1.iloc[i, 2]
        subject_num = df1.iloc[i, 9]
        if num in num_set:
            continue
        if subject_num not in subject_set:
            continue
        num_set.add(num)
        new_row['凭证日期'] = df1.iloc[i, 0]
        new_row['凭证字'] = df1.iloc[i, 1]
        new_row['凭证编号'] = df1.iloc[i, 2]
        new_row['摘要'] = df1.iloc[i, 6]
        new_row['科目编号'] = df1.iloc[i, 9]
        new_row['科目名称'] = df1.iloc[i, 10]
        new_row['借金额'] = df1.iloc[i, 15]
        new_row['贷金额'] = float(df1.iloc[i, 16])
        if float(df1.iloc[i, 16]) > 500000.00:
            fifty += 1
        if float(df1.iloc[i, 16]) > 1000000.00:
            hundred += 1
        if float(df1.iloc[i, 16]) > 1500000.00:
            fh += 1
        if float(df1.iloc[i, 16]) > 2000000.00:
            th += 1
        df = df.append(new_row, ignore_index=True)
    df.sort_values(by=['贷金额'], inplace=True)
    new_row['凭证编号'] = ''
    new_row['摘要'] = ''
    new_row['科目编号'] = ''
    new_row['科目名称'] = ''
    new_row['借金额'] = ''
    new_row['贷金额'] = ''
    new_row['凭证日期'] = '大于50万'
    new_row['凭证字'] = str(fifty)
    df = df.append(new_row, ignore_index=True)
    new_row['凭证日期'] = '大于100万'
    new_row['凭证字'] = str(hundred)
    df = df.append(new_row, ignore_index=True)
    new_row['凭证日期'] = '大于150万'
    new_row['凭证字'] = str(fh)
    df = df.append(new_row, ignore_index=True)
    new_row['凭证日期'] = '大于200万'
    new_row['凭证字'] = str(th)
    df = df.append(new_row, ignore_index=True)
    df.to_excel('过滤' + input_file, index=False, encoding='utf-8')


if __name__ == '__main__':
    import_file('')
