#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: check bank account
@file_name: check_bank_account.py
@project: my_love
@version: 1.0
@date: 2021/01/11 15:22
@author: Air
"""

__author__ = 'Air'

import pandas as pd


def check(input_file: str, check_file: str) -> None:
    df1 = pd.read_excel(input_file)
    df2 = pd.read_excel(check_file)
    number_set = set()
    for i in range(df2.shape[0]):
        if not pd.isna(df2.iloc[i, 1]):
            number_set.add(str(df2.iloc[i, 2])[-5:])
    df = pd.DataFrame(columns=['出纳提交时间', '交易时间', '凭证日期', '凭证编号', '借方发生额（支取）',
                               '贷方发生额（收入）', '对方户名', '对方账号', '对方开户机构', '记账日期', '摘要', '备注'])
    for i in range(df1.shape[0]):
        number = str(df1.iloc[i, 3])[-5:]
        if number not in number_set:
            df = df.append(df1.iloc[i])
    df.to_excel('out.xls', index=False, encoding='utf-8')
    df1 = df1.drop(df.index)
    df1.to_excel('in.xls', index=False, encoding='utf-8')
