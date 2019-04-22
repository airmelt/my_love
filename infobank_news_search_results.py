#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 爬取infobank新闻搜索数/Spider for news searching results from infobank.cn
@file_name: infobank_news_search_results.py
@project: my_love
@version: 1.0
@date: 2019/04/20 23:21
@author: air
"""

__author__ = 'air'


import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_news_search_results(length):
    try:
        # 伪装头部信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                          'Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        # df1 = pd.read_excel(r'C:\Users\air\Desktop\300家数据.xlsx', usecols = '1, 3')
        # df1打开数据的第B列(公司名称), df2打开数据的第E列(CEO姓名)
        df1 = pd.read_excel(r'筛选数据20190418.xlsx')
        df2 = pd.read_excel(r'筛选数据20190418.xlsx', usecols=[4])

        # 共2656条数据
        a = 0
        for i in range(length, 2656):
            a = i
            # 读取公司名称和CEO姓名
            group_name = df1.iat[i, 1]
            name = df2.iat[i, 0]
            year = str(df1.iat[i, 2])
            # 防止封IP, 休息1秒钟
            time.sleep(1)
            # 将字符串转换为编码urllib.parse.quote(name)
            # http://www.bjinfobank.com/DataList.do?method=DataList&db=HK&iw=%E8%B4%B5%E5%B7%9E%E8%8C%85%E5%8F%B0+%E8%A2%81%E4%BB%81%E5%9B%BD&query=all&rl=2&pageSize=25&starTime=2010-01-01&endTime=2010-12-31&myorder=SUTM
            url = 'http://www.bjinfobank.com/DataList.do?method=DataList&db=HK&iw=' + \
                  urllib.parse.quote(name) + '+' + urllib.parse.quote(group_name) + '&query=all&rl=2&pageSize=25&' + \
                  'starTime=' + year + '-01-01&endTime=' + year + '-12-31&myorder=SUTM'
            req = urllib.request.Request(url, None, headers, None, False)
            response = urllib.request.urlopen(req)
            soup = BeautifulSoup(response.read(), 'lxml')
            result = soup.find_all(name='span', attrs={"class": "mlgreen"})[0].string.replace(',', '').strip()
            print(result)
            df1.iloc[i, 17] = result
            df1.to_excel(r'筛选数据20190420.xlsx', index=False, header=False, encoding='utf-8')
    except:
        print('a: ' + str(a))
        get_news_search_results(a)


if __name__ == "__main__":
    get_news_search_results(0)
