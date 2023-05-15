#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: secret training for 2023
@file_name: secret_training.py
@project: my_love
@version: 1.0
@date: 2023/5/15 17:00
@author: air
"""

import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def training(token: str):
    options = webdriver.EdgeOptions()
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    browser = webdriver.Edge(options=options)
    with open(r'class_list.json', 'r', encoding='utf-8') as f:
        class_list = json.load(f)['data']['listdata']
        for item in class_list:
            time_length = item['timeLength']
            total_time = 60 * int('0' + time_length[3:5]) + int('0' + time_length[-2:])
            resource_id = item['resourceID']
            resource_directory_id = item['SYS_UUID']
            url = f'http://www.baomi.org.cn/portal/api/v2/studyTime/saveCoursePackage.do?' \
                  f'courseId=897ed48c-b420-4b43-844b-280147eb422a&resourceId={resource_id}&' \
                  f'resourceDirectoryId={resource_directory_id}&resourceLength={total_time}&studyLength={total_time}&' \
                  f'studyTime={total_time}&token={token}'
            browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
            browser.get(url)
        