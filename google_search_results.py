#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 爬虫爬取Google搜索结果数
@file_name: google_search_results.py
@project: my_love
@version: 1.0
@date: 2018/11/22 11:28
@author: air
"""

import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

# 伪装头部信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
# df1 = pd.read_excel(r'C:\Users\air\Desktop\year5.xlsx', usecols = '1, 4')
# df1打开数据的第B列(公司名称), df2打开数据的第E列(CEO姓名)
df1 = pd.read_excel(r'year5.xlsx', usecols=[1])
df2 = pd.read_excel(r'year5.xlsx', usecols=[4])
keywords = ['魅力', '幻想', '浮夸', '传奇', '身材', '个性', '明星', '传教士', '鼓舞人心', '关心员工',
            '关心顾客', '使命感', '理智', '敬业', '合作', '正确的经营理念', '解决就业', '关心环境', '合作精神', '热心公益慈善事业']
with open(r'output.txt', 'w') as f:

    # 共334条数据
    for i in range(5):
        # 读取公司名称和CEO姓名
        group_name = df1.iat[i, 0]
        name = df2.iat[i, 0]
        for j in range(len(keywords)):
            keyword = keywords[j]
            for year in range(2010, 2018):
                # 防止google封IP, 休息1秒钟
                time.sleep(1)
                # 将字符串转换为编码
                # url: https://www.google.com/search?q=%E8%B4%B5%E5%B7%9E%E8%8C%85%E5%8F%B0+%E8%A2%81%E4%BB%81%E5%9B%BD+%E9%AD%85%E5%8A%9B&newwindow=1&source=lnt&tbs=cdr%3A1%2Ccd_min%3A20100101%2Ccd_max%3A20101231&tbm=
                # url: https://www.google.com/search?q=%E8%B4%B5%E5%B7%9E%E8%8C%85%E5%8F%B0+%E8%A2%81%E4%BB%81%E5%9B%BD+%E9%AD%85%E5%8A%9B&newwindow=1&source=lnt&tbs=cdr%3A1%2Ccd_min%3A20110101%2Ccd_max%3A20111231&tbm=
                url = 'https://www.google.com/search?q=' + \
                    urllib.parse.quote(group_name) + '+' + urllib.parse.quote(group_name) + \
                    '+' + urllib.parse.quote(keyword) + '&newwindow=1&source=lnt&tbs=cdr%3A1%2Ccd_min%3A' + str(
                        year) + '0101%2Ccd_max%3A' + str(year) + '1231&tbm='
                req = urllib.request.Request(url, None, headers, None, False)
                response = urllib.request.urlopen(req)
                soup = BeautifulSoup(response.read())
                # 如果搜索数不足1000个, 下面的正则将输出None
                # 找到约 917 条结果
                pattern1 = r'找到约 (\d+,)+\d+ 条结果'
                # result1: '百度为您找到相关结果约###,###,###个'
                result1 = re.search(pattern1, str(soup))
                if result1 is not None:
                    pattern = r'(\d+,)+\d+'
                    result = re.search(pattern, result1.group(0)).group(0)
                    result = ''.join(result.split(','))
                else:
                    pattern1 = r'找到约 (\d+) 条结果'
                    result1 = re.search(pattern1, str(soup))
                    pattern = r'(\d+)'
                    result = re.search(pattern, result1.group(0)).group(0)
                    result = ''.join(result.split(','))
                # result: '###,###,###'
                f.write(result + '\n')
