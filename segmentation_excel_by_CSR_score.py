#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 按csr得分分割excel/Excel segmentation by CSR score
@file_name: segmentation_excel_by_CSR_score.py
@project: my_love
@version: 1.0
@date: 2018/11/17 14:33
@author: air
"""
import pandas as pd


def csr(main_file, input_file, j):
    """
    按csr得分分割excel
    :param main_file: 分割文件
    :param input_file: 传入csr得分文件
    :param j: 年份参数
    :return:
    """
    df1 = pd.read_excel(main_file)
    df2 = pd.read_excel(input_file)
    name1 = list(df1['证券简称'])
    name2 = list(df2['股票名称'])
    for i in range(332):
        try:
            # 找出在CSR得分文件中对应的行
            row = name2.index(name1[8 * i])
            # 在CSR得分文件中找出对应的得分数据
            score = df2.iloc[row, 5]
            # 存入得分数据
            df1.iloc[8 * i + j, 2] = score
        # 防止找不到对应数据报错
        except ValueError:
            pass
    # 保存文件
    df1.to_excel('temp.xlsx', index=False, encoding='utf-8')


if __name__ == '__main__':
    # 共8年的数据
    for k in range(8):
        file1 = 'temp.xlsx'
        file2 = '筛选数据201' + str(j) + '.xlsx'
        csr(file1, file2, k)
