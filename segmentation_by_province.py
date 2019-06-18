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
    :param province_list: 传入省份列表
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
    """
    按照文件分割Excel
    :param file_list: 传入文件列表
    :return:
    """
    columns = [file[:file.find('.')] for file in file_list]
    columns.insert(0, '年份')
    columns.insert(0, '英文城市名')
    columns.insert(0, '城市名')
    df = pd.DataFrame(columns=columns)
    new = pd.DataFrame(index=['0'], columns=columns)
    df_list = []
    for file in file_list:
        df_list.append(pd.read_excel(file, index_col=2))
    city = int(df_list[0].shape[0])
    for i in range(city):
        for j in range(9):
            new.iloc[0, 0] = df_list[0].iloc[i, 0]
            new.iloc[0, 1] = df_list[0].iloc[i, 1]
            new.iloc[0, 2] = 2009 + j
            new.iloc[0, 3] = df_list[0].iloc[i, j + 2]
            new.iloc[0, 4] = df_list[1].iloc[i, j + 2]
            new.iloc[0, 5] = df_list[2].iloc[i, j + 2]
            new.iloc[0, 6] = df_list[3].iloc[i, j + 2]
            new.iloc[0, 7] = df_list[4].iloc[i, j + 2]
            new.iloc[0, 8] = df_list[5].iloc[i, j + 2]
            new.iloc[0, 9] = df_list[6].iloc[i, j + 2]
            new.iloc[0, 10] = df_list[7].iloc[i, j + 2]
            new.iloc[0, 11] = df_list[8].iloc[i, j + 2]
            new.iloc[0, 12] = df_list[9].iloc[i, j + 2]
            df = df.append(new, ignore_index=True)
    df.to_excel('area.xlsx', index=False, encoding='utf-8')


def segmentation_by_city(file_list):
    """
    按照城市分割Excel
    :param file_list: 传入城市列表
    :return:
    """
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


def segmentation_by_area(file_list):
    """
    按照地区分割Excel
    :param file_list: 传入地区列表
    :return:
    """
    df_gdp = pd.read_excel(file_list[0], index_col=1)
    df_middle_student = pd.read_excel(file_list[1], index_col=1)
    df_middle_school = pd.read_excel(file_list[2], index_col=1)
    df_middle_teacher = pd.read_excel(file_list[3], index_col=1)
    df_bus = pd.read_excel(file_list[4], index_col=1)
    df_suburb_income = pd.read_excel(file_list[5], index_col=1)
    df_bed = pd.read_excel(file_list[6], index_col=1)
    df_hospital = pd.read_excel(file_list[7], index_col=1)
    df_fai = pd.read_excel(file_list[8], index_col=1)
    df_city_income = pd.read_excel(file_list[9], index_col=1)
    df_fdi = pd.read_excel(file_list[10], index_col=1)
    df_primary_student = pd.read_excel(file_list[11], index_col=1)
    df_primary_school = pd.read_excel(file_list[12], index_col=1)
    df_primary_teacher = pd.read_excel(file_list[13], index_col=1)
    df_industry = pd.read_excel(file_list[14], index_col=1)
    df_people = pd.read_excel(file_list[15], index_col=1)
    df_resident = pd.read_excel(file_list[16], index_col=1)
    df_consume = pd.read_excel(file_list[17], index_col=1)
    df_life = pd.read_excel(file_list[18], index_col=1)
    df_electric = pd.read_excel(file_list[19], index_col=1)
    df_finance = pd.read_excel(file_list[20], index_col=1)
    df = pd.DataFrame(columns=['城市名', '英文城市名', '年份', 'GDP', '中学在校生数', '中学学校数', '中学教师数',
                               '公共交通车辆拥有量', '农村人均可支配收入', '医院、卫生院床位数', '医院、卫生院数',
                               '固定资产投资', '城镇人均可支配收入', '外商直接投资', '小学在校生数', '小学学校数',
                               '小学教师数', '工业固体废物综合利用率', '常住人口', '户籍人口', '消费品零售',
                               '生活垃圾无害化处理率', '电力消费', '财政支出'])
    new_row = pd.DataFrame(index=['0'], columns=['城市名', '英文城市名', '年份', 'GDP', '中学在校生数', '中学学校数',
                                                 '中学教师数', '公共交通车辆拥有量', '农村人均可支配收入', '医院、卫生院床位数',
                                                 '医院、卫生院数', '固定资产投资', '城镇人均可支配收入', '外商直接投资',
                                                 '小学在校生数', '小学学校数', '小学教师数', '工业固体废物综合利用率',
                                                 '常住人口', '户籍人口', '消费品零售', '生活垃圾无害化处理率', '电力消费',
                                                 '财政支出'])
    for i in range(21):
        for j in range(10):
            new_row.iloc[0, 0] = str(df_gdp.iloc[i, 0])[str(df_gdp.iloc[i, 0]).rfind(':') + 1:]
            new_row.iloc[0, 1] = df_gdp.iloc[i, 1]
            new_row.iloc[0, 2] = 2009 + j
            new_row.iloc[0, 3] = df_gdp.iloc[i, j + 4]
            new_row.iloc[0, 4] = df_middle_student.iloc[i, j + 4]
            new_row.iloc[0, 5] = df_middle_school.iloc[i, j + 4]
            new_row.iloc[0, 6] = df_middle_teacher.iloc[i, j + 4]
            new_row.iloc[0, 7] = df_bus.iloc[i, j + 4]
            new_row.iloc[0, 8] = df_suburb_income.iloc[i, j + 4]
            new_row.iloc[0, 9] = df_bed.iloc[i, j + 4]
            new_row.iloc[0, 10] = df_hospital.iloc[i, j + 4]
            new_row.iloc[0, 11] = df_fai.iloc[i, j + 4]
            new_row.iloc[0, 12] = df_city_income.iloc[i, j + 4]
            new_row.iloc[0, 13] = df_fdi.iloc[i, j + 4]
            new_row.iloc[0, 14] = df_primary_student.iloc[i, j + 4]
            new_row.iloc[0, 15] = df_primary_school.iloc[i, j + 4]
            new_row.iloc[0, 16] = df_primary_teacher.iloc[i, j + 4]
            new_row.iloc[0, 17] = df_industry.iloc[i, j + 4]
            new_row.iloc[0, 18] = df_people.iloc[i, j + 4]
            new_row.iloc[0, 19] = df_resident.iloc[i, j + 4]
            new_row.iloc[0, 20] = df_consume.iloc[i, j + 4]
            new_row.iloc[0, 21] = df_life.iloc[i, j + 4]
            new_row.iloc[0, 22] = df_electric.iloc[i, j + 4]
            new_row.iloc[0, 23] = df_finance.iloc[i, j + 4]
            df = df.append(new_row, ignore_index=True)
    df.to_excel('area.xlsx', index=False, encoding='utf-8')


def segmentation_by_year(input_file, start, end):
    """
    通用按照年份分割列表
    :param input_file: 传入文件名
    :param start: 开始年份
    :param end: 结束年份
    :return:
    """
    df = pd.read_excel(input_file, index_col=2)
    columns = list(df.columns)
    years = end - start
    for year in range(start, end):
        df_year = pd.DataFrame(columns=columns)
        for city in range(int(df.shape[0]) // years):
            new = pd.DataFrame(index=['0'], columns=columns)
            for i in range(len(columns)):
                new.iloc[0, i] = df.iloc[city * years + (year - start), i]
            df_year = df_year.append(new, ignore_index=True)
        df_year.to_excel('area' + str(year) + '.xlsx', index=False, encoding='utf-8')


if __name__ == '__main__':
    # p_list = ['云南.xls', '内蒙古.xls', '吉林.xls', '四川.xls', '宁夏.xls', '安徽.xls', '山东.xls', '黑龙江.xls',
    #           '广东.xls', '广西.xls', '新疆.xls', '江苏.xls', '江西.xls', '河北.xls', '河南.xls', '浙江.xls', '海南.xls',
    #           '湖北.xls', '湖南.xls', '甘肃.xls', '福建.xls', '贵州.xls', '辽宁.xls', '陕西.xls', '青海.xls', '山西.xls']
    # e_list = ['GDP.xls', '实际利用外资金额.xls', '年末总人口.xls', '社会消费品零售额.xls', '财政支出.xls']
    # f_list = ['人口.xlsx', '城镇人均可支配收入.xlsx', '城镇人均消费支出.xlsx', '外商直接投资（实际使用）.xlsx',
    #           '消费品零售.xlsx', '行政区域土地面积.xlsx', '财政支出.xlsx', 'GDP.xlsx']
    # f_list = ['GDP.xlsx', '中学在校生数.xlsx', '中学学校数.xlsx', '中学教师数.xlsx', '公共交通车辆拥有量.xlsx',
    #           '农村人均可支配收入.xlsx', '医院、卫生院床位数.xlsx', '医院、卫生院数.xlsx', '固定资产投资.xlsx',
    #           '城镇人均可支配收入.xlsx', '外商直接投资.xlsx', '小学在校生数.xlsx', '小学学校数.xlsx', '小学教师数.xlsx',
    #           '工业固体废物综合利用率.xlsx', '常住人口.xlsx', '户籍人口.xlsx', '消费品零售.xlsx', '生活垃圾无害化处理率.xlsx',
    #           '电力消费.xlsx', '财政支出.xlsx']
    f_list = ['养老保险.xlsx', '医疗保险.xlsx', '卫生技术人员.xlsx', '卫生机构数.xlsx', '图书馆.xlsx', '失业保险.xlsx',
              '年末登记失业人员.xlsx', '床位数.xlsx', '文化人员.xlsx', '邮电总量.xlsx']
    # segmentation_by_province(p_list)
    # segmentation_by_program(e_list)
    # segmentation_by_file(f_list)
    # segmentation_by_file(f_list)
    segmentation_by_year(r'area20190611.xlsx', 2009, 2018)
