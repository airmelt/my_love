#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 聚类分析
@file_name: cluster_method.py
@project: my_love
@version: 1.0
@date: 2019/06/24 21:38
@author: air
"""

__author__ = 'air'
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import pandas as pd

# price = [1.1,1.2,1.3,1.4,10,11,20,21,33,34]
# increase = [1 for i in range(10)]
# X = np.array([price,increase],dtype='float32')
# X = X.T#这里必须使得输入的矩阵行代表样本，列代表维度
#
# d = sch.distance.pdist(X)#计算样本距离矩阵
#
# Z = sch.linkage(d, method='complete')#进行层级聚类，这里complete代表层级聚类中的最长距离法
#
# sch.dendrogram(Z)#显示树状聚类图
for year in range(2009, 2018):
    df_year = pd.read_excel(r'result' + str(year) + '.xlsx', encoding='utf-8', index_col=0)
    file_name = ['经济', '文化', 'D']
    df_economy = pd.DataFrame(df_year, columns=[r'经济得分'])
    df_culture = pd.DataFrame(df_year, columns=[r'文化得分'])
    df_result = pd.DataFrame(df_year, columns=[r'D2'])
    variables = ['Guangzhou', 'Shaoguan', 'Shenzhen', 'Zhuhai', 'Shantou', 'Foshan', 'Jiangmen', 'Zhanjiang', 'Maoming',
                 'Zhaoqing', 'Huizhou', 'Meizhou', 'Shanwei', 'Heyuan', 'Yangjiang', 'Qingyuan', 'Dongguan', 'Zhongshan',
                 'Chaozhou', 'Jieyang', 'Yunfu']
    link_economy = linkage(df_economy.values)
    link_culture = linkage(df_culture.values)
    link_result = linkage(df_result.values)
    dendrogram(link_economy, labels=variables)
    plt.savefig(str(year) + file_name[0] + ".png")
    dendrogram(link_culture, labels=variables)
    plt.savefig(str(year) + file_name[1] + ".png")
    dendrogram(link_result, labels=variables)
    plt.savefig(str(year) + file_name[2] + ".png")
# plt.show()
# x = np.array([df.iloc[0], df.iloc[1]])
# x = x.T
# d = sch.distance.pdist(x)
# z = sch.linkage(d, method='complete')
# sch.dendrogram(z)
# plt.show()
