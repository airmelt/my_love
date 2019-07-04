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
import re


def find_name_author(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.readline().strip()
    pattern = re.compile(r'data-res-name="(.*?)" data-res-author="(.*?)"')
    music_list = pattern.findall(text)
    with open(r'music_list.txt', 'a', encoding='utf-8') as f:
        for song, author in music_list:
            f.write(song + '----' + author + '\n')
    

if __name__ == '__main__':
    find_name_author('music.txt')
