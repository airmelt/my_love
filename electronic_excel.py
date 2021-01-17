#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: get the information of some companies
@file_name: electronic_excel.py
@project: my_love
@version: 1.0
@date: 2021/01/11 13:17
@author: Air
"""

__author__ = 'Air'

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import time


def add_introduction(input_file: str):
    df = pd.read_excel(input_file)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    e = []
    for i in range(df.shape[0]):
        try:
            company = df.iloc[i, 1].replace(' ', '+')
            url = 'https://zh.wikipedia.org/w/index.php?search='
            url += company
            url += '&title=Special%3A%E6%90%9C%E7%B4%A2&go=%E5%89%8D%E5%BE%80&wprov=acrw1_-1'
            req = urllib.request.Request(url, None, headers, None, False)
            response = urllib.request.urlopen(req)
            soup = BeautifulSoup(response.read(), 'lxml')
            result = soup.find_all("p")
            if len(result) > 1:
                p1 = remove_brackets(str(result[0]))
                p2 = remove_brackets(str(result[1]))
                p = p1 + p2
            else:
                p = remove_brackets(str(result[0]))
            link = soup.find("span", attrs={"id": "外部連結"})
            s = str(link)
            if not link or not s.strip():
                link = soup.find("span", attrs={"id": "外部链接"})
                s = str(link)
            link = link.parent
            s = str(link)
            while not link.find("li") or not s.strip():
                link = link.next_sibling
                s = str(link)
            link = str(link.li.a['href'])
            title = str(soup.title.text)
            title = title[:title.find(' ')]
            df.iloc[i, 2] = title + '(' + p + link + ')'
            print(df.iloc[i, 2])
            time.sleep(5)
        except (AttributeError, urllib.error.URLError):
            e.append((i, df.iloc[i, 1]))
    print(e)
    df.to_excel('result.xlsx', index=False, encoding='utf-8')


def remove_brackets(s: str) -> str:
    while s.find('<') != -1:
        s = s[:s.find('<')] + s[s.find('>') + 1:]
    while s.find('[') != -1:
        s = s[:s.find('[')] + s[s.find(']') + 1:]
    return s
