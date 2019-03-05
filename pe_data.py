#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 爬虫爬取清科研究中心Excel/Spider for creating excel from pedata.com
@file_name: pe_data.py
@project: my_love
@version: 1.0
@date: 2018/12/13 00:56
@author: air
"""


import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import xlwt
import os
import time


def html2txt(url_enter, num, file_name):
    """
    输入页码返回一个txt文档
    :param url_enter: 三级地址
    :param num: 页码
    :param file_name: 输出的文件名路径，文本文件
    :return: txt"""
    url_dict = {'投资': 'invest', '并购': 'ma', '退出': 'exit',
                '投资事件': 'invest', '并购事件': 'ma', '退出事件': 'exit',
                'invest': 'invest', 'ma': 'ma', 'exit': 'exit'}
    # 伪装头部信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    with open(file_name, 'w', encoding='utf-8') as f:
        url_head = 'https://' + url_dict[url_enter] + '.pedata.cn/list_'
        for i in range(num):
            url = url_head + str(i + 1) + '_0_0_0_0.html'
            req = urllib.request.Request(url, None, headers, None, False)
            response = urllib.request.urlopen(req)
            soup = BeautifulSoup(response.read(), 'lxml')
            row = soup.find_all('tr')
            for j in range(1, len(row)):
                col = row[j].find_all('td')
                for k in range(len(col)):
                    if k == 0:
                        if len(col[k].find_all('a')) == 0:
                            f.write(col[k].text.strip() + '\n')
                        else:
                            names = []
                            for name in col[k].find_all('a'):
                                names.append(name.text)
                                name = ', '.join(names)
                            f.write(name + '\n')
                        continue
                    if k == 1:
                        f.write(col[k].find('a').text + '\n')
                        continue
                    if k == (len(col) - 1):
                        url = col[k].find('a')['href']
                        f.write(url + '\n')
                        continue
                    col[k] = ''.join(col[k].text.strip().split())
                    if k == 5 and url_dict[url_enter] != 'exit':
                        if col[k] != '--':
                            col[k] = col[k].replace('RMB', '').replace('M', '')
                            if len(col[k]) > 5:
                                col[k] = col[k][0:-5] + '.' + col[k][-5:-3] + col[k][-2:] + '亿'
                            else:
                                col[k] = col[k][0:-3] + col[k][-2:] + '万'
                    if k == 3 and url_dict[url_enter] == 'exit':
                        if col[k] != '--':
                            col[k] = col[k].replace('RMB', '').replace('M', '')
                            if len(col[k]) > 5:
                                col[k] = col[k][0:-5] + '.' + col[k][-5:-3] + col[k][-2:] + '亿'
                            else:
                                col[k] = col[k][0:-3] + col[k][-2:] + '万'
                    f.write(col[k] + '\n')


def txt2excel(input_file, out_file):
    """
    文本文件转化为Excel文件
    :param input_file: 输入的文件路径, 文本文件
    :param out_file: 输出的文件路径, Excel文件
    :return:
    """

    file1 = open(input_file, 'r', encoding='UTF-8')
    lines = file1.readlines()
    # 新建一个excel文件
    file2 = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 新建一个sheet
    sheet = file2.add_sheet('data')

    # 按行列输出excel文件
    i = 0
    j = 0
    font = xlwt.Font()  # Create Font
    font.colour_index = 4  # 蓝色字体
    font.underline = True
    style = xlwt.XFStyle()
    style.font = font
    for line in lines:
        line = line.strip()
        if j == 7:
            # '"test" & HYPERLINK("http://google.com")'
            # sheet.write(i, j, xlwt.Formula('HYPERLINK("%s";"Link")' % line))
            # sheet.write(i, j, xlwt.Formula('HYPERLINK(' + line + ')'))
            # 详情 -> url
            sheet.write(i, j, xlwt.Formula('HYPERLINK("' + line + '";"' + '详情' + '")'), style)
            sheet.write(i, j + 1, line)
            i += 1
            j = 0
            continue
            # sheet.write_url(i, j, line)
        sheet.write(i, j, line)
        j += 1
    # 输出文件带上时间
    out_file = out_file + time.strftime("%Y-%m-%d", time.localtime()) + '.xls'
    file2.save(out_file)
    # 返回文件名
    return out_file


def delete(input_file):
    """
    删除中间文件
    :param input_file: 输入文件路径
    :return:
    """
    if os.path.exists(input_file):
        os.remove(input_file)


def get_equity(input_file):
    """
    点击详情获取股权
    :param input_file: 输入文件
    :return:
    """
    df1 = pd.read_excel(input_file, header=None)
    df2 = pd.read_excel(input_file, header=None)
    # 伪装头部信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    for i in range(len(df1[8])):
        # req = urllib.request.Request('https://ma.pedata.cn/236860833.html', None, headers, None, False)
        time.sleep(1)
        req = urllib.request.Request(df1[8][i], None, headers, None, False)
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response.read(), 'lxml')
        result = soup.find_all(name='table', attrs={"class": "table_squre"})
        result = result[0].find_all('td')[2].find_all('p')[0].string.strip()
        print(result)
        df2.iloc[i, 7] = result
    df2.to_excel('equity' + input_file, index=False, header=False, encoding='utf-8')


if __name__ == '__main__':
    # html2txt('invest', 1, 'invest.txt')
    # txt2excel('invest.txt', 'invest')
    # delete('invest.txt')
    # html2txt('ma', 1, 'ma.txt')
    # txt2excel('ma.txt', 'ma')
    # delete('ma.txt')
    # html2txt('exit', 3, 'exit.txt')
    # txt2excel('exit.txt', 'exit')
    # delete('exit.txt')
    get_equity('ma' + time.strftime("%Y-%m-%d", time.localtime()) + '.xls')
