#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 创建股票excel/Create excel for stock
@file_name: create_stock_excel.py
@project: my_love
@version: 1.0
@date: 2019/1/21 23:30
@author: air
"""

__author__ = 'air'


import pandas as pd
import xlwt
import xlrd


def get_row(input_file):
    """
    获取需要的股票
    :param input_file: 传入csv文件
    :return:
    """
    df1 = pd.read_csv(input_file)
    return df1.shape[0]


def create_excel(input_file, stock_file, row, output_file):
    """
    获取新智认知股票数据
    :param input_file: 传入excel文件
    :param stock_file: 传入股票数据文件
    :param row: 行数
    :param output_file: 输出结果文件
    :return:
    """
    df1 = pd.read_excel(input_file)
    df2 = pd.read_csv(stock_file)
    closing_share_price = df2.iloc[row][3]
    stock_quote_change = '%.2f' % df2.iloc[row][9]
    df1.iloc[2, 0] = '1'
    df1.iloc[2, 1] = '603869'
    df1.iloc[2, 2] = '新智认知'
    df1.iloc[2, 3] = '新奥控股投资有限公司'
    df1.iloc[2, 4] = closing_share_price
    insurance = (closing_share_price * (1000.5002 + 0) + 2000) / 13300
    df1.iloc[2, 5] = '%.2f' % (insurance * 100) + '%'
    df1.iloc[2, 6] = stock_quote_change + '%'
    alert_stock_price = '%.2f' % ((1.15 * 13300 - 2000) / (1000.5002 + 0))
    df1.iloc[2, 7] = alert_stock_price
    df1.iloc[2, 8] = '%.2f' % (((closing_share_price / float(alert_stock_price)) - 1) * 100) + '%'
    df1.iloc[2, 9] = ''
    df1.iloc[2, 10] = '50%'
    df1.iloc[2, 11] = '115%'
    df1.iloc[2, 12] = ''
    price_without_cost = '%.2f' % ((13300 - 0 - 2000) / (1000.5002 + 0))
    df1.iloc[2, 13] = price_without_cost
    cost_percent_deviation = (closing_share_price / float(price_without_cost)) - 1
    df1.iloc[2, 14] = '%.2f' % (cost_percent_deviation * 100) + '%'
    df1.iloc[2, 15] = '1,000.5002'
    df1.iloc[2, 16] = '0'
    df1.iloc[2, 17] = '0'
    df1.iloc[2, 18] = '0'
    df1.iloc[2, 19] = '2,000'
    df1.iloc[2, 20] = '13,300'
    df1.iloc[2, 21] = '1187天'
    df1.iloc[2, 22] = '7.050%'
    df1.iloc[2, 23] = '2016/10/17'
    df1.iloc[2, 24] = '2020/01/17'
    output_file = output_file.replace('time', df2.iloc[row][0])
    df1.to_excel(output_file, header=None, index=None)
    return output_file


def change_color(input_file):
    """
    按照结果改变字体颜色
    :param input_file: 传入文件
    :return:
    """
    workbook = xlrd.open_workbook(input_file)
    sheet = workbook.sheet_by_index(0)
    stock_quote_change = sheet.cell(2, 6).value
    style = "font:colour_index red;"
    red_style = xlwt.easyxf(style)
    style = "font:colour_index green;"
    green_style = xlwt.easyxf(style)
    # 新建一个excel文件
    file = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 新建一个sheet
    out_sheet = file.add_sheet('data')
    for i in range(sheet.nrows):
        for j in range(sheet.ncols):
            if i == 2 and j == 6:
                if stock_quote_change.find('-') > -1:
                    out_sheet.write(2, 6, sheet.cell(i, j).value, green_style)
                    continue
                else:
                    out_sheet.write(2, 6, sheet.cell(i, j).value, red_style)
                    continue
            out_sheet.write(i, j, sheet.cell(i, j).value)
    file.save(input_file.replace('xlsx', 'xls'))


if __name__ == '__main__':
    for i in range(get_row('603869.csv')):
        out_file = '场外质押盯市数据(time).xlsx'
        out_file = create_excel('场外质押盯市数据（1月04日收盘）.xlsx', '603869.csv', i, out_file)
        change_color(out_file)
