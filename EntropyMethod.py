#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 熵值法/EntropyMethod
@file_name: EntropyMethod.py
@project: my_love
@version: 1.0
@date: 2019/06/08 11:15
@author: air
"""

__author__ = 'air'

import pandas as pd
import numpy as np


class EntropyMethod:
    def __init__(self, index, positive, negative, row_name):
        """
        初始化熵值法类
        :param index: 指标
        :param positive: 正向指标
        :param negative: 负向指标
        :param row_name: 行名称
        """
        if len(index) != len(row_name):
            raise Exception('数据指标行数与行名称数不符')
        if sorted(index.columns) != sorted(positive + negative):
            raise Exception('正项指标加负向指标不等于数据指标的条目数')

        self.index = index.copy().astype('float64')
        self.positive = positive
        self.negative = negative
        self.row_name = row_name
        self.uniform_mat = None
        self.p_mat = None
        self.entropy_series = None
        self.d_series = None
        self.weight = None
        self.score = None

    def uniform(self):
        """
        均一化
        :return:
        """
        uniform_mat = self.index.copy()
        min_index = {column: min(uniform_mat[column]) for column in uniform_mat.columns}
        max_index = {column: max(uniform_mat[column]) for column in uniform_mat.columns}
        for i in range(len(uniform_mat)):
            for column in uniform_mat.columns:
                if column in self.positive:
                    uniform_mat[column][i] = (uniform_mat[column][i] - min_index[column]) / (
                            max_index[column] - min_index[column])
                else:
                    uniform_mat[column][i] = (max_index[column] - uniform_mat[column][i]) / (
                            max_index[column] - min_index[column])

        self.uniform_mat = uniform_mat
        return self.uniform_mat

    def calc_probability(self):
        """
        计算权重
        :return:
        """
        try:
            p_mat = self.uniform_mat.copy()
        except AttributeError:
            raise Exception('你还没进行归一化处理，请先调用uniform方法')
        for column in p_mat.columns:
            sigma_x_1_n_j = sum(p_mat[column])
            p_mat[column] = p_mat[column].apply(
                lambda x_i_j: x_i_j / sigma_x_1_n_j if x_i_j / sigma_x_1_n_j != 0 else 1e-6)

        self.p_mat = p_mat
        return p_mat

    def calc_entropy(self):
        """
        计算熵值
        :return:
        """
        try:
            self.p_mat.head(0)
        except AttributeError:
            raise Exception('你还没计算比重，请先调用calc_probability方法')

        e_j = -(1 / np.log(len(self.p_mat))) * np.array(
            [sum([pij * np.log(pij) for pij in self.p_mat[column]]) for column in self.p_mat.columns])
        ejs = pd.Series(e_j, index=self.p_mat.columns, name='指标的熵值')

        self.entropy_series = ejs
        return self.entropy_series

    def calc_entropy_redundancy(self):
        """
        计算冗余度
        :return:
        """
        try:
            self.d_series = 1 - self.entropy_series
            self.d_series.name = '信息熵冗余度'
        except AttributeError:
            raise Exception('你还没计算信息熵，请先调用calc_entropy方法')

        return self.d_series

    def calc_weight(self):
        """
        计算权值
        :return:
        """
        self.uniform()
        self.calc_probability()
        self.calc_entropy()
        self.calc_entropy_redundancy()
        self.weight = self.d_series / sum(self.d_series)
        self.weight.name = '权值'
        return self.weight

    def calc_score(self):
        """
        计算得分
        :return:
        """
        self.calc_weight()

        self.score = pd.Series(
            [np.dot(np.array(self.p_mat[row:row + 1])[0], np.array(self.weight)) for row in range(len(self.p_mat))],
            index=self.row_name, name='得分'
        )
        return self.score


if __name__ == '__main__':
    for year in range(2009, 2018):
        df = pd.read_excel('area' + str(year) + '.xlsx', encoding='utf-8')
        cities = df['城市名']
        economic_items = ['人均GDP/元', '城镇人均可支配收入/元', '人均消费品零售/元', '人均固定资产投资/元', '人均外商直接投资/美元', '人均财政支出/元']
        cultural_items = ['每千名中学生均教师数/人', '人均公共交通车辆拥有量/辆', '每千名小学生均教师数/人', '工业固体废物综合利用率/%', '生活垃圾无害化处理率/%', '人均电力消费/千瓦时',
                          '每千人卫生技术人员/人', '每千人卫生机构数/个', '失业率/%', '每千人床位数/张', '文化人员/人', '人均邮电总量/元', '失业保险基金/万元',
                          '城镇基本养老保险基金/万元']
        cultural_positive = cultural_items[:]
        cultural_positive.remove('失业率/%')
        cultural_negative = ['失业率/%']
        cultural_index = df[cultural_items]
        economic_positive = economic_items[:]
        economic_negative = []
        economic_index = df[economic_items]
        cultural_em = EntropyMethod(cultural_index, cultural_positive, cultural_negative, cities)
        cultural_em.calc_score().to_excel('cultural' + str(year) + '.xlsx', encoding='utf-8')
        economic_em = EntropyMethod(economic_index, economic_positive, economic_negative, cities)
        economic_em.calc_score().to_excel('economic' + str(year) + '.xlsx', encoding='utf-8')

    for year in range(2009, 2018):
        columns = ['城市名', '经济得分', '文化得分', 'C', 'T', 'D']
        df_result = pd.DataFrame(columns=columns)
        df_economic = pd.read_excel('economic' + str(year) + '.xlsx')
        df_cultural = pd.read_excel('cultural' + str(year) + '.xlsx')
        df_result['城市名'] = df_economic['城市名']
        df_result['经济得分'] = df_economic['得分']
        df_result['文化得分'] = df_cultural['得分']
        df_result['C'] = ((df_economic['得分'] * df_cultural['得分']) / (df_economic['得分'] + df_cultural['得分']) ** 2) ** 0.5
        df_result['T'] = (df_economic['得分'] + df_cultural['得分']) * 0.5
        df_result['D'] = (df_result['C'] * df_result['T']) ** 0.5
        df_result.to_excel('result' + str(year) + '.xlsx', index=False, encoding='utf-8')
