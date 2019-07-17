#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 网易云音乐正则
@file_name: cloud_music.py
@project: my_love
@version: 1.0
@date: 2019/07/04 10:04
@author: air
"""

__author__ = 'air'
import os
import re
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def find_name_author(filename):
    """
    获取歌名
    :param filename: 传入文件名
    :return:
    """
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.readline().strip()
    pattern = re.compile(r'data-res-name="(.*?)" data-res-author="(.*?)"')
    music_list = pattern.findall(text)
    with open(r'music_list.txt', 'a', encoding='utf-8') as f:
        for song, author in music_list:
            f.write(song + '----' + author + '\n')


class CloudMusic:
    """
    网易云音乐类
    """
    def __init__(self):
        """
        初始化
        """
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.main_url = 'https://music.163.com/'
        self.songs = []

    def get_songs(self, playlist_id):
        """
        获取歌单中所有的歌名&作者名&id
        :param playlist_id: 歌单id
        :return:
        """
        url = self.main_url + '#/playlist?id=' + str(playlist_id)
        self.browser.get(url)
        self.browser.implicitly_wait(5)
        self.browser.switch_to.frame('g_iframe')
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        table = soup.find_all('tr')
        for item in table:
            if item.a:
                spans = item.find_all('span')
                for span in spans:
                    share = '分享'
                    if span.get('title') == share:
                        song = (
                            span.get('data-res-id'),
                            span.get('data-res-author'),
                            span.get('data-res-name'))
                        self.songs.append(song)
        self.browser.close()

    def download_songs(self):
        """
        下载mp3
        :return:
        """
        url = self.main_url + 'song/media/outer/url?id='
        extension = '.mp3'
        work_dir = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))
        work_dir = os.path.join(work_dir, 'music')
        for item in self.songs:
            song_id = item[0]
            author = item[1].replace(r'?', '').replace(r'/', r'&').replace(r'*', '')
            name = item[2].replace(r'?', '').replace(r'/', r'&').replace(r'*', '')
            song_url = url + song_id + extension
            file_name = author + '-' + name + extension
            work_path = os.path.join(work_dir, file_name)
            try:
                urllib.request.urlretrieve(song_url, work_path)
            except OSError:
                print(file_name)
                pass
            time.sleep(1)


if __name__ == '__main__':
    # find_name_author('music.txt')
    c = CloudMusic()
    c.get_songs(382885157)
    c.download_songs()
