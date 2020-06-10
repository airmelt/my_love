#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 爬取国家宗教事务局数据
@file_name: religious_data.py
@project: my_love
@version: 1.0
@date: 2020/06/10 11:44
@author: air
"""

import json
import time
import urllib
import pandas as pd

__author__ = 'air'

df = pd.read_excel('city.xlsx', encoding='utf-8')
cache = {}
headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
           'Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8'
           }
url = 'http://www.sara.gov.cn/api/front/zj/query'
page, page_size = 1, 15
for i in range(0, df.shape[0]):
    address = df.iloc[i, 2] + df.iloc[i, 1]
    types = ['佛教', '道教']
    cities = {'北京市北京市', '天津市天津市', '上海市上海市', '重庆市重庆市'}
    if address in cities:
        address = address[:2]
    if address in cache.keys():
        df.iloc[i, 3] = cache[address]
        print(df.iloc[i, 2], df.iloc[i, 1], df.iloc[i, 3])
        df.to_excel('city.xlsx', index=False, encoding='utf-8')
        continue
    result = 0
    for item in types:
        time.sleep(3)
        data_json = {'address': address,
                     'faction': '',
                     'type': item,
                     'keywords': '',
                     'page': page,
                     'pageSize': page_size,
                     }
        data_json = bytes(urllib.parse.urlencode(data_json), 'utf-8')
        req = urllib.request.Request(
            url=url,
            data=data_json,
            headers=headers,
            method='POST')
        response = urllib.request.urlopen(req)
        response = json.loads(response.read().decode('utf-8'))
        total_page = int(response['totalPage'])
        total_page = 1 if not total_page else total_page
        data_json = {'address': address,
                     'faction': '',
                     'type': item,
                     'keywords': '',
                     'page': total_page,
                     'pageSize': page_size,
                     }
        data_json = bytes(urllib.parse.urlencode(data_json), 'utf-8')
        req = urllib.request.Request(
            url=url,
            data=data_json,
            headers=headers,
            method='POST')
        response = urllib.request.urlopen(req)
        response = json.loads(response.read().decode('utf-8'))
        result += len(response['data']) + (total_page - 1) * page_size
    df.iloc[i, 3] = result
    cache[address] = result
    print(df.iloc[i, 2], df.iloc[i, 1], df.iloc[i, 3])
    df.to_excel('city.xlsx', index=False, encoding='utf-8')
