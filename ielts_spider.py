#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: spider of IELTS speaking and writing test
@file_name: ielts_spider.py
@project: my_love
@version: 1.0
@date: 2022/5/25 10:59
@author: airmelt
"""
import urllib.request
from bs4 import BeautifulSoup


def extract(url: str) -> None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    req = urllib.request.Request(url, None, headers, None, False)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')
    table = soup.table
    for a in table.find_all('a', text=['查看', '范文']):
        part_one = a.get('href')
        a_req = urllib.request.Request(part_one, None, headers, None, False)
        a_response = urllib.request.urlopen(a_req)
        a_soup = BeautifulSoup(a_response.read(), 'lxml')
        core = a_soup.find('div', class_='xqy_core_text')
        file_name = core.find('strong').text.replace('/', '或者')
        with open(file_name + '.txt', 'w', encoding='utf-8') as f:
            for item in core.find_all('p'):
                text = item.text
                if text.find('新东方') != -1 or text.find('Part 1') != -1 or text.find('雅思') != -1:
                    continue
                f.write(item.text)
                f.write('\n\n')
