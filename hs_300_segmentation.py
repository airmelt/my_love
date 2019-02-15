#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 分割结果
@file_name: hs_300_segmentation.py
@project: my_love
@version: 1.0
@date: 2018/10/27 18:35
@author: air
"""

file1 = open('hs300origin.txt', 'r', encoding='UTF-8')
file2 = open('hs300s.txt', 'w')

line = file1.readlines()
list1 = line[0].split('"')
for item in list1:
    file2.write(item + "\n")

file1.close()
file2.close()
