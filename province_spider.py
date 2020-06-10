#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 爬取省份地级市县级市
@file_name: province_spider.py
@project: my_love
@version: 1.0
@date: 2020/06/09 20:05
@author: air
"""
import re
import time
import json
import urllib
import pandas as pd
from bs4 import BeautifulSoup

__author__ = 'air'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                  'Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
# 国家统计局
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html'
req = urllib.request.Request(url, None, headers, None, False)
response = urllib.request.urlopen(req)
soup = BeautifulSoup(response.read(), 'lxml')
china, province_names, province_urls = {}, [], []
# 省份
for item in soup.find_all('tr', 'provincetr'):
    time.sleep(3)
    for detail in item.find_all('a'):
        if detail:
            province_names.append(detail.get_text())
            province_urls.append(detail['href'])
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'
tr, a, lxml, href = 'tr', 'a', 'lxml', 'href'

for province_name, province_url in zip(province_names[29:], province_urls[29:]):
    time.sleep(3)
    province_url = url + province_url
    req = urllib.request.Request(province_url, None, headers, None, False)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), lxml)
    province, city_names, city_urls, clazz = [], [], [], 'citytr'
    # 省份对应的城市
    for item in soup.find_all(tr, clazz):
        for detail in item.find_all(a):
            if detail:
                if detail.get_text().isdigit():
                    continue
                city_names.append(detail.get_text())
                city_urls.append(detail[href])
    province += city_names
    china[province_name] = {}
    # 城市对应的区/县
    for city_name, city_url in zip(city_names, city_urls):
        time.sleep(3)
        city_url = url + city_url
        req = urllib.request.Request(city_url, None, headers, None, False)
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response.read(), lxml)
        county_names, county_urls, clazz = [], [], 'countytr' if soup.find_all(class_=re.compile('countytr')) else 'towntr'
        for item in soup.find_all(tr, clazz):
            for detail in item.find_all(a):
                if detail:
                    if detail.get_text().isdigit():
                        continue
                    county_names.append(detail.get_text())
                    county_urls.append(detail[href])
        province += county_names
        china[province_name][city_name] = county_names
        print('{}爬取完成'.format(city_name))
    print(china)
# 保存为json文档
china = json.dumps(china)
with open('china_province_data.json', 'w') as f:
    f.write(china)
# 保存为Excel文档
china_province_data = open('./china_province_data.json', encoding="utf-8").read()
china_province_data = json.loads(china_province_data)
df = pd.DataFrame(columns=['省份', '地级市', '县/县级市'])
new = pd.DataFrame(index=['0'], columns=['省份', '地级市', '县/县级市'])
index = 0
for province in china_province_data.keys():
    for city in china_province_data[province].keys():
        for county in china_province_data[province][city]:
            df = df.append(new, ignore_index=True)
            df['省份'][index], df['地级市'][index], df['县/县级市'][index] = province, city, county
            index += 1
df1 = df
for i in range(df1.shape[0]):
    if df1.iloc[i, 1] == '市辖区':
        df1.iloc[i, 1] = df1.iloc[i, 0]
    if '自治区' in df1.iloc[i, 0]:
        if '内蒙古' in df1.iloc[i, 0]:
            df1.iloc[i, 0] = '内蒙古'
        else:
            df1.iloc[i, 0] = df1.iloc[i, 0][:2]
df1.to_excel('china_religious_data.xlsx', index=False, encoding='utf-8')
df.to_excel('china_province_data.xlsx', index=False, encoding='utf-8')

