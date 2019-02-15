#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 按年份查找百度新闻搜索结果数/Spider for news results from baidu.com by years
@file_name: baidu_news_search_results_by_years.py
@project: my_love
@version: 1.0
@date: 2018/12/08 11:53
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
# df1 = pd.read_excel(r'C:\Users\air\Desktop\300家数据.xlsx', usecols = '1, 3')
# df1打开数据的第B列(公司名称), df2打开数据的第D列(CEO姓名)
df1 = pd.read_excel(r'CEO新闻数.xlsx', usecols=[1])
df2 = pd.read_excel(r'CEO新闻数.xlsx', usecols=[4])
with open(r'output.txt', 'w') as f:

    # 共334条数据
    for i in range(334):
        # 读取公司名称和CEO姓名
        group_name = df1.iat[i * 8, 0]
        name = df2.iat[i * 8, 0]
        time_stamp1 = 1262275200
        time_stamp2 = 1293811199
        for j in range(8):
            # 使用时间戳查找
            url = 'http://www.baidu.com/s?wd=' + urllib.parse.quote(group_name) + '%20' + urllib.parse.quote(name) + '&gpc=stf%3D' + \
                str(time_stamp1) + '%2C' + \
                str(time_stamp2) + '%7Cstftype%3D2'
            time_stamp1 = 31536000 + time_stamp1
            time_stamp2 = 31536000 + time_stamp2
            # 防止百度封IP, 休息1秒钟
            time.sleep(1)
            # 将字符串转换为编码
            # url = http://news.baidu.com/ns?from=news&cl=2&bt=1262275200&y0=2010&m0=1&d0=1&y1=2010&m1=12&d1=31&et=1293811199&q1=%E9%87%91%E9%A3%8E%E7%A7%91%E6%8A%80+%E6%AD%A6%E9%92%A2&submit=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B&q3=&q4=&mt=0&lm=&s=2&begin_date=2010-1-1&end_date=2010-12-31&tn=newsdy&ct1=1&ct=1&rn=20&q6=
            # http://www.baidu.com/s?wd=贵州茅台%20袁仁国&gpc=stf%3D1262275200%2C1293811199%7Cstftype%3D2
            # http://www.baidu.com/s?wd=贵州茅台%20袁仁国&gpc=stf%3D1293811200%2C1325347199%7Cstftype%3D2
            # http://www.baidu.com/s?wd=贵州茅台%20袁仁国&gpc=stf%3D1325347200%2C1356969599%7Cstftype%3D2
            # http://www.baidu.com/s?wd=贵州茅台%20袁仁国&gpc=stf%3D1356969600%2C1388505599%7Cstftype%3D2
            # http://www.baidu.com/s?wd=贵州茅台%20袁仁国&gpc=stf%3D1388505600%2C1420041599%7Cstftype%3D2
            # http://www.baidu.com/s?wd=贵州茅台%20袁仁国&gpc=stf%3D1420041600%2C1451577599%7Cstftype%3D2
            # http://www.baidu.com/s?wd=贵州茅台%20袁仁国&gpc=stf%3D1451577600%2C1483199999%7Cstftype%3D2
            # http://www.baidu.com/s?wd=贵州茅台%20袁仁国&gpc=stf%3D1483200000%2C1514735999%7Cstftype%3D2
            # url = 'http://news.baidu.com/ns?from=news&cl=2&bt=1262275200&y0=2010&m0=1&d0=1&y1=2010&m1=12&d1=31&et=1293811199&q1=' + \
            #     urllib.parse.quote(name) + '+' + urllib.parse.quote(group_name) + \
            #     '&submit=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B&q3=&q4=&mt=0&lm=&s=2&begin_date=2010-1-1&end_date=2010-12-31&tn=newsdy&ct1=1&ct=1&rn=20&q6='
            req = urllib.request.Request(url, None, headers, None, False)
            response = urllib.request.urlopen(req)
            soup = BeautifulSoup(response.read())
            # 如果搜索数不足1000个, 下面的正则将输出None
            pattern1 = r'百度为您找到相关结果约(\d+,)+\d+个'
            # result1: '百度为您找到相关结果约###,###,###个'
            result1 = re.search(pattern1, str(soup))
            if result1 is not None:
                pattern = r'(\d+,)+\d+'
                result = re.search(pattern, result1.group(0)).group(0)
                result = ''.join(result.split(','))
            else:
                pattern1 = r'百度为您找到相关结果约(\d+)个'
                result1 = re.search(pattern1, str(soup))
                pattern = r'(\d+)'
                result = re.search(pattern, result1.group(0)).group(0)
                result = ''.join(result.split(','))
            # result: '###,###,###'
            f.write(result + '\n')
