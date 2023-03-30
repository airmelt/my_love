#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: correct bank from bank excel
@file_name: correct_bank.py
@project: my_love
@version: 1.0
@date: 2023/3/13 10:17
@author: air
"""

import pandas as pd


def correct_bank():
    # df_bank = pd.read_excel(r'银行开户行信息.xlsx')
    df_bank = pd.read_excel(r'开户行信息.xlsx')
    banks = set()
    n = df_bank.shape[0]
    for i in range(n):
        banks.add((df_bank.iloc[i, 1], df_bank.iloc[i, 2]))
    df_company = pd.read_excel(r'学校往来单位信息.xlsx')
    m = df_company.shape[0]
    for i in range(m):
        open_bank = str(df_company.iloc[i, 5])
        open_bank = open_bank[-6:]
        bank_name = str(df_company.iloc[i, 7])
        bank_name = bank_name[-4:]
        if '汇丰银行' in open_bank or not open_bank:
            for bank in banks:
                if bank[0][-5:] == open_bank and bank[1][-4:] == bank_name:
                    df_company.iloc[i, 6] = bank[0]
                    df_company.iloc[i, 8] = bank[1]
                    print(i, bank)
                    break
    df_company.to_excel('bank.xlsx')
