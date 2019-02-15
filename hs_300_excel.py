#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 将txt文件转化为excel/txt -> excel
@file_name: hs_300_excel.py
@project: my_love
@version: 1.0
@date: 2018/11/8 17:21
@author: air
"""

import xlwt  # 写入文件
import xlrd  # 打开excel文件

file1 = open("hs300.txt", 'r', encoding='UTF-8')
lines = file1.readlines()
# 新建一个excel文件
file2 = xlwt.Workbook(encoding='utf-8', style_compression=0)
# 新建一个sheet
sheet = file2.add_sheet('data')

# 按行列输出excel文件
i = 0
for line in lines:
    j = 0
    s1 = 0
    while j < 11:
        s2 = line.find(',', s1)
        word = line[s1:s2]
        sheet.write(i, j, word)
        j = j + 1
        s1 = s2 + 1
    i = i + 1

file2.save('hs300.xls')
