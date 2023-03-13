#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: spider for extracting duolingo words
@file_name: duolingo_words.py
@project: my_love
@version: 1.0
@date: 2023/3/8 10:17
@author: air
"""

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import time

from pandas import DataFrame


def generate_excel():
    columns = ['Base Word', 'Guideword', 'Level', 'Part of Speech', 'Topic', 'Details', 'Length']
    df = pd.DataFrame(columns=columns)
    for i in range(0, 15400, 20):
        time.sleep(1)
        df = generate_row(i, df)
        print(i, df.iloc[-1, 0])
    df.to_excel('duolingo_words.xlsx', index=False)
    
    
def generate_row(start: int, df: DataFrame) -> DataFrame:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    url = 'http://www.englishprofile.org/american-english'
    if start:
        url += '?start=' + str(start)
    req = urllib.request.Request(url, None, headers, None, False)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')
    row = soup.find_all('tr')
    new_row = pd.DataFrame(index=['0'], columns=df.columns)
    for r in row[1:]:
        col = r.find_all('td')
        for j, c in enumerate(col):
            new_row.iloc[0, j] = c.text
        new_row.iloc[0, -1] = len(col[0].text)
        df = pd.concat([df, new_row], ignore_index=True)
    return df
