#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 将数据处理成300行的数据/Data progressing
@file_name: hs_300_lines.py
@project: my_love
@version: 1.0
@date: 2018/10/27 18:36
@author: air
"""

file1 = open('hs300s2.txt', 'r', encoding='UTF-8')
file2 = open('hs300s3.txt', 'w')
list1 = []

while True:
    line = file1.readline()
    s = line.find(',')
    if s > 0:
        file2.write(line)
    if not line:
        break

file1.close()
file2.close()
