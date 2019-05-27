#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 根据省份分割列表/Segmentation by province
@file_name: segmentation_by_province.py
@project: my_love
@version: 1.0
@date: 2019/05/16 22:35
@author: air
"""

__author__ = 'air'

import pandas as pd


def segmentation_by_province(province_list):
    """
    根据省份分割列表
    :param province_list:
    :return:
    """
    df_total = pd.DataFrame(columns=['城市名', '收入', '支出', '年份'])
    new_row = pd.DataFrame(index=['0'], columns=['城市名', '收入', '支出', '年份'])
    for province_file in province_list:
        province = province_file[:province_file.find('.')]
        df = pd.read_excel(province_file)
        rows = df.shape[0]
        columns = df.shape[1] // 2
        for j in range(columns):
            j += 1
            city = df.iloc[0, j]
            city = province + '-' + city[city.rfind(':') + 1:]
            for i in range(1, rows):
                new_row.iloc[0, 0] = city
                new_row.iloc[0, 1] = str(df.iloc[i, j])
                new_row.iloc[0, 2] = str(df.iloc[i, j + columns])
                new_row.iloc[0, 3] = str(2008 + i)
                df_total = df_total.append(new_row, ignore_index=True)
    df_total.to_excel('total.xlsx', index=False, encoding='utf-8')


def segmentation_by_program(excel_list):
    """
    按照项目分割Excel
    :param excel_list: 传入项目Excel文件列表
    :return:
    """
    df_gdp = pd.read_excel(excel_list[0], index_col=0)
    df_foreign = pd.read_excel(excel_list[1], index_col=0)
    df_people = pd.read_excel(excel_list[2], index_col=0)
    df_consume = pd.read_excel(excel_list[3], index_col=0)
    df_cost = pd.read_excel(excel_list[4], index_col=0)
    df_total = pd.DataFrame(columns=['城市名', '年份', 'GDP', '实际利用外资金额', '年末总人口', '社会消费品零售额', '财政支出'])
    new_row = pd.DataFrame(index=['0'], columns=['城市名', '年份', 'GDP', '实际利用外资金额', '年末总人口', '社会消费品零售额', '财政支出'])
    for i in range(284):
        for j in range(8):
            new_row.iloc[0, 0] = df_gdp.iloc[i, 0]
            new_row.iloc[0, 1] = 2010 + j
            new_row.iloc[0, 2] = df_gdp.iloc[i, j + 1]
            new_row.iloc[0, 3] = df_foreign.iloc[i, j + 1]
            new_row.iloc[0, 4] = df_people.iloc[i, j + 1]
            new_row.iloc[0, 5] = df_consume.iloc[i, j + 1]
            new_row.iloc[0, 6] = df_cost.iloc[i, j + 1]
            df_total = df_total.append(new_row, ignore_index=True)
    df_total.to_excel('city.xlsx', index=False, encoding='utf-8')


def segmentation_by_file(file_list):
    df_people = pd.read_excel(file_list[0], index_col=0)
    df_income = pd.read_excel(file_list[1], index_col=0)
    df_consume = pd.read_excel(file_list[2], index_col=0)
    df_fdi = pd.read_excel(file_list[3], index_col=0)
    df_retail = pd.read_excel(file_list[4], index_col=0)
    df_area = pd.read_excel(file_list[5], index_col=0)
    df_finance = pd.read_excel(file_list[6], index_col=0)
    df_gdp = pd.read_excel(file_list[7], index_col=0)
    df_total = pd.DataFrame(columns=['城市名', '英文城市名', '年份', '人口', '城镇人均可支配收入', '城镇人均消费支出', '外商直接投资（实际使用）',
                                     '消费品零售', '行政区域土地面积', '财政支出', 'GDP'])
    new_row = pd.DataFrame(index=['0'], columns=['城市名', '英文城市名', '年份', '人口', '城镇人均可支配收入', '城镇人均消费支出', '外商直接投资（实际使用）',
                                                 '消费品零售', '行政区域土地面积', '财政支出', 'GDP'])
    for i in range(284):
        for j in range(9):
            new_row.iloc[0, 0] = df_gdp.iloc[i, 0]
            new_row.iloc[0, 1] = df_gdp.iloc[i, 1]
            new_row.iloc[0, 2] = 2010 + j
            new_row.iloc[0, 3] = df_people.iloc[i, j + 2]
            new_row.iloc[0, 4] = df_income.iloc[i, j + 2]
            new_row.iloc[0, 5] = df_consume.iloc[i, j + 2]
            new_row.iloc[0, 6] = df_fdi.iloc[i, j + 2]
            new_row.iloc[0, 7] = df_retail.iloc[i, j + 2]
            new_row.iloc[0, 8] = df_area.iloc[i, j + 2]
            new_row.iloc[0, 9] = df_finance.iloc[i, j + 2]
            new_row.iloc[0, 10] = df_gdp.iloc[i, j + 2]
            df_total = df_total.append(new_row, ignore_index=True)
    df_total.to_excel('program.xlsx', index=False, encoding='utf-8')


if __name__ == '__main__':
    # p_list = ['云南.xls', '内蒙古.xls', '吉林.xls', '四川.xls', '宁夏.xls', '安徽.xls', '山东.xls', '黑龙江.xls',
    #           '广东.xls', '广西.xls', '新疆.xls', '江苏.xls', '江西.xls', '河北.xls', '河南.xls', '浙江.xls', '海南.xls',
    #           '湖北.xls', '湖南.xls', '甘肃.xls', '福建.xls', '贵州.xls', '辽宁.xls', '陕西.xls', '青海.xls', '山西.xls']
    # e_list = ['GDP.xls', '实际利用外资金额.xls', '年末总人口.xls', '社会消费品零售额.xls', '财政支出.xls']
    f_list = ['人口.xlsx', '城镇人均可支配收入.xlsx', '城镇人均消费支出.xlsx', '外商直接投资（实际使用）.xlsx',
              '消费品零售.xlsx', '行政区域土地面积.xlsx', '财政支出.xlsx', 'GDP.xlsx']
    # segmentation_by_province(p_list)
    # segmentation_by_program(e_list)
    segmentation_by_file(f_list)
