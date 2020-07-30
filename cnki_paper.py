#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 爬取知网文章数据
@file_name: cnki_paper.py
@project: my_love
@version: 1.0
@date: 2020/07/16 16:54
@author: air
"""

__author__ = 'air'

import time
from typing import List
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def find_by_name(year: str, main_author: str, second_author: str='') -> str:
    from_time, to_time = year + '-01-01', year + '-12-31'
    now = time.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0800 (中国标准时间)'
    first_url = "https://kns.cnki.net/kns/request/SearchHandler.ashx"
    first_headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/29.0.1547.66 Safari/537.36',
        'Referer': "http://kns.cnki.net/kns/brief/default_result.aspx",
        'Cookie': 'Ecp_ClientId=2190704232702209793	; cnkiUserKey=eaf9a3b9-3143-a1b4-d005-52f7e51dbca0; '
                  'Ecp_IpLoginFail=20071636.157.3.135; ASP.NET_SessionId=zlfi5d2twco23dak2rpjcwih; SID_kns=123109; '
                  'SID_klogin=125143; SID_kns_new=kns123117; KNS_SortType=; RsPerPage=20; SID_krsnew=125131; '
                  '_pk_ref=%5B%22%22%2C%22%22%2C1594887932%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D; '
                  '_pk_ses=*; SID_kinfo=125102; ASPSESSIONIDQABTATSR=MOIFBCHDILGIKNKBFDHAGMAF',
    }
    data = {'action': '44',
            'gt': '1',
            'NaviCode': '*',
            'ua': '1.21',
            'isinEn': '1',
            'PageName': 'ASP.brief_result_aspx',
            'DbPrefix': 'SCDB',
            'DbCatalog': '中国学术文献网络出版总库',
            'ConfigFile': 'SCDB.xml',
            'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
            'publishdate_from': from_time,
            'publishdate_to': to_time,
            'CKB_extension': 'ZYW',
            'au_1_sel': 'AU',
            'au_1_sel2': 'AF',
            'au_1_value1': main_author,
            'au_1_special1': '=',
            'au_1_special2': '%',
            'au_4_sel': 'AU',
            'au_4_sel2': 'AF',
            'au_4_value1': second_author,
            'au_4_logical': 'and',
            'au_4_special1': '=',
            'au_4_special2': '%',
            'his': '0',
            '__': now}
    first_response = requests.get(first_url, headers=first_headers, data=data).text

    second_headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/29.0.1547.66 Safari/537.36',
        'Referer': "http://kns.cnki.net/kns/brief/default_result.aspx?code=SCDB",
        'Cookie': 'Ecp_ClientId=2190704232702209793	; cnkiUserKey=eaf9a3b9-3143-a1b4-d005-52f7e51dbca0; '
                  'Ecp_IpLoginFail=20071636.157.3.135; ASP.NET_SessionId=zlfi5d2twco23dak2rpjcwih; SID_kns=123109; '
                  'SID_klogin=125143; SID_kns_new=kns123117; KNS_SortType=; RsPerPage=20; SID_krsnew=125131; '
                  '_pk_ref=%5B%22%22%2C%22%22%2C1594887932%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D; '
                  '_pk_ses=*; SID_kinfo=125102; ASPSESSIONIDQABTATSR=MOIFBCHDILGIKNKBFDHAGMAF',
    }
    second_url = "https://kns.cnki.net/kns/brief/brief.aspx?pagename=" + \
        str(first_response) + "&S=1&sorttype=(被引频次,'INTEGER')+desc"
    response = requests.get(second_url, headers=second_headers).text
    soup = BeautifulSoup(response, "lxml")
    a = soup.find("a", class_="fz14")
    # title = a.get_text()
    now_timestamp, href = str(int(datetime.now().timestamp() * 1000)), 'href'
    if not a:
        return '未查询到相关结果' + '---' + year + ' ' + main_author + ' ' + second_author
    url = a[href]
    db_name = re.search(r'(?<=DbName=)(.*?)&', url, re.I).group(1)
    file_name = re.search(r'(?<=FileName=)(.*?)&', url, re.I).group(1)
    cur_rec = re.search(r'(?<=CurRec=)(.*?)&', url, re.I).group(1)
    query_id = re.search(r'(?<=QueryID=)(.*?)&', url, re.I).group(1)
    third_url = "https://kns.cnki.net/kns/ViewPage/viewsave.aspx?t=" + now_timestamp + '&formfilenames=' + db_name + \
                '!' + file_name + '!' + cur_rec + '!' + query_id
    third_headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 '
                      'Safari/537.36',
        'Referer': "http://kns.cnki.net/kns/brief/default_result.aspx?code=SCDB",
        'Cookie': 'Ecp_ClientId=2190704232702209793; cnkiUserKey=eaf9a3b9-3143-a1b4-d005-52f7e51dbca0; '
                  'ASP.NET_SessionId=zlfi5d2twco23dak2rpjcwih; SID_kns=123109; SID_klogin=125143; '
                  'SID_kns_new=kns123117; RsPerPage=20; SID_krsnew=125131; SID_kinfo=125102; '
                  'ASPSESSIONIDQABTATSR=MOIFBCHDILGIKNKBFDHAGMAF; SID_kcms=124119; SID_crrs=125133; '
                  'KNS_SortType=SCDB%21%28%25e8%25a2%25ab%25e5%25bc%2595%25e9%25a2%2591%25e6%25ac%25a1%252c%2527'
                  'INTEGER%2527%29+desc; Ecp_IpLoginFail=20071736.157.15.1; '
                  '_pk_ref=%5B%22%22%2C%22%22%2C1594976764%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D; DisplaySave=21',
    }
    third_response = requests.get(third_url, headers=third_headers).text
    soup = BeautifulSoup(third_response, "lxml")
    message = soup.find('td', class_='CurContentID').get_text().strip()[3:]
    print(message)
    return message


def get_name_year(file_name: str) -> List[tuple]:
    df1 = pd.read_excel(file_name)
    result = list()
    for i in range(df1.shape[0]):
        year, main_author, second_author = str(df1.iloc[i, 2]), df1.iloc[i, 0], df1.iloc[i, 1]
        if df1.iloc[i, 1] != df1.iloc[i, 1]:
            second_author = ''
        result.append(tuple((year, main_author, second_author)))
    return result


if __name__ == '__main__':
    # get_name_year('参考文献作者名与年份.xlsx')
    find_by_name('2012', '丁美芹', '')
