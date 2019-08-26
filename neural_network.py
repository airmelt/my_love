#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 神经网络
@file_name: neural_network.py
@project: my_love
@version: 1.0
@date: 2019/08/08 22:55
@author: air
"""

__author__ = 'air'
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt


def load_data(filename, sheetname):
    """导入数据
    input:  file_path(string):训练数据
    output: feature(mat):特征
            label(mat):标签
    """
    df = pd.read_excel(filename, sheet_name=sheetname)
    feature = df.iloc[:, 0:6]
    label = df.iloc[:, -2]
    maxminz = [
        [
            0, 0, 0], [
            0, 0, 0], [
                0, 0, 0], [
                    0, 0, 0], [
                        0, 0, 0], [
                            0, 0, 0]]
    for i in range(6):
        maxminz[i][0] = df.iloc[0:5500, i].max()  # 国企5500 非国企6000
        maxminz[i][1] = df.iloc[0:5500, i].min()
        maxminz[i][2] = df.iloc[0:5500, i].mean()

    return np.mat(feature), np.mat(label).T, maxminz


def distance(X, Y):
    """计算两个样本之间的距离
    """
    return np.sqrt(np.sum(np.square(X - Y), axis=1))


def distance_mat(trainX, testX):
    """计算待测试样本与所有训练样本的欧式距离
    input:trainX(mat):训练样本
          testX(mat):测试样本
    output:Euclidean_D(mat):测试样本与训练样本的距离矩阵
    """
    m, n = np.shape(trainX)
    p = np.shape(testX)[0]
    Euclidean_D = np.mat(np.zeros((p, m)))
    for i in range(p):
        for j in range(m):
            Euclidean_D[i, j] = distance(testX[i, :], trainX[j, :])[0, 0]
    return Euclidean_D


def Gauss(Euclidean_D, sigma):
    """测试样本与训练样本的距离矩阵对应的Gauss矩阵
    input:Euclidean_D(mat):测试样本与训练样本的距离矩阵
          sigma(float):Gauss函数的标准差
    output:Gauss(mat):Gauss矩阵
    """
    m, n = np.shape(Euclidean_D)
    # print('Euclidean_D',Euclidean_D)
    Gauss = np.mat(np.zeros((m, n)))
    for i in range(m):
        for j in range(n):
            Gauss[i, j] = math.exp(- Euclidean_D[i, j] / (2 * (sigma ** 2)))
    # print("gauss:::",Gauss)
    return Gauss


def sum_layer(Gauss, trY):
    """求和层矩阵，列数等于输出向量维度+1,其中0列为每个测试样本Gauss数值之和
    """
    m, l = np.shape(Gauss)
    # print('Gauss:',m,l)
    n = np.shape(trY)[1]
    sum_mat = np.mat(np.zeros((m, n + 1)))
    # 对所有模式层神经元输出进行算术求和
    for i in range(m):
        # sum_mat的第0列为每个测试样本Gauss数值之和
        sum_mat[i, 0] = np.sum(Gauss[i, :], axis=1)
    # 对所有模式层神经元进行加权求和
    for i in range(m):
        for j in range(n):
            total = 0.0
            for s in range(l):
                total += Gauss[i, s] * trY[s, j]
            sum_mat[i, j + 1] = total  # sum_mat的后面的列为每个测试样本Gauss加权之和
    return sum_mat


def output_layer(sum_mat):
    """输出层输出
    input:sum_mat(mat):求和层输出矩阵
    output:output_mat(mat):输出层输出矩阵
    """
    m, n = np.shape(sum_mat)
    # print("m,n",m,n)
    # print('sum_mat:', sum_mat[99][0])
    output_mat = np.mat(np.zeros((m, n - 1)))
    for i in range(n - 1):
        output_mat[:, i] = sum_mat[:, i + 1] / sum_mat[:, 0]
    # print("sum_mat[:, 0]",np.shape(sum_mat[:, 0]))
    # print("sum_mat[:, 0]:",np.reshape(sum_mat[:, 0],(1,m)))
    # print("sum_mat[:, 1]:", np.reshape(sum_mat[:, 1], (1, m)))
    return output_mat


def genarateM(n, maxminz):  # 取100
    arr = np.linspace(maxminz[n][1], maxminz[n][0], 100)
    xgfeature = []
    for i in range(6):
        if i != n and i != 5:
            xgfeature.append([maxminz[i][2]] * 100)
        else:
            if i != 5 and n != 5:
                xgfeature.append(arr)
        if i == 5 and n != 5:
            xgfeature.append([0] * 100)
        if i == 5 and n == 5:
            xgfeature.append([0] * 50 + [1] * 50)
    return np.mat(xgfeature).T


def genarateM1(n, maxminz, data):
    arr = np.linspace(maxminz[n][1], maxminz[n][0], 100)
    xgfeature = []
    for i in range(6):
        if i != n and i != 5:
            xgfeature.append([data[0, i]] * 100)
        else:
            if i != 5 and n != 5:
                xgfeature.append(arr)
        if i == 5 and n != 5:
            xgfeature.append([0] * 100)
        if i == 5 and n == 5:
            xgfeature.append([0] * 50 + [1] * 50)
    return np.mat(xgfeature).T


def baifen(output_mat):
    minz = 1000000000
    q = 0
    sk = 0
    output_arr = np.array(output_mat.T)
    # print(type(output_arr[0][1]))
    for i in range(len(output_arr[0])):
        if not np.isnan(output_arr[0][i]):
            if minz > output_arr[0][i]:
                minz = output_arr[0][i]
            q += 1
    # print(minz)
    for i in range(len(output_arr[0])):
        if not np.isnan(output_arr[0][i]):
            sk = sk + (output_arr[0][i] - minz)
    print('sk=', sk, 'q=', q)
    if q == 0:
        print('buduile')
        return 0
    return sk / q


def RMSE(out_mat, teY):
    rmse = 0
    for i in range(len(out_mat)):
        rmse += (out_mat[i] - teY[i]) * (out_mat[i] - teY[i]) / len(out_mat)
    return rmse


def Mr(Tex):
    n = np.shape(teX)[0]
    guoqi = [-0.0623732, 0.0000254, 1.625355, -0.0938985, 0.0988323, 2.355644]
    guoqicons = [-9.111716]

    feiguoqi = [-0.0832964, 0.0526446, 3.229266, -0.0993228, 0.1933707, 4.1525]
    feiguoqicons = [-27.69735]

    zong = [-0.0515938, 0.0003216, 2.326571, -0.0979011, 0.1407304, 3.167704]
    zongcons = [-17.53259]
    pram = np.mat(np.reshape(guoqi, (6, 1)))
    cons = np.mat(np.reshape(guoqicons * n, (n, 1)))
    pre = Tex * pram + cons
    return pre


def calsix(trX, tex, trY):
    output_mat = output_layer(
        sum_layer(
            Gauss(
                distance_mat(
                    trX,
                    tex),
                0.95),
            trY))
    for i in range(np.shape(tex)[0]):
        if tex[i, 5] == 1:
            tex[i, 5] = 0
        if tex[i, 5] == 0:
            tex[i, 5] = 1
    output_mat1 = output_layer(
        sum_layer(
            Gauss(
                distance_mat(
                    trX,
                    tex),
                0.95),
            trY))
    return sum(abs(output_mat - output_mat1)) / np.shape(tex)[0]


if __name__ == '__main__':
    # 1.导入数据
    print('------------------------1. Load Data----------------------------')
    feature, label, maxminz = load_data('国企20190826.xlsx', 'Sheet1')  # 改要读的文件
    print(maxminz)
    print(feature)
    # 2.数据集和测试集
    print('--------------------2.Train Set and Test Set--------------------')
    trX = feature[0:5500, :]  # 国企5500 非国企6000   测试点取200
    trY = label[0:5500, :]
    teX = feature[5500:5700, :]
    teY = label[5500:5700, :]

    """
    这里是测试比重
    """
    # sk = []
    # data = feature[4100,:]
    # print('dada',data)
    # for i in range(6):
    #
    #     # Xgf = genarateM(i,maxminz)
    #     Xgf = genarateM1(i, maxminz,data)
    #     print(i)
    #     print()
    #     # print(Xgf)
    #     if i ==5:
    #         print('input:',Xgf[0,:])
    #
    #     output_matx = output_layer(sum_layer(Gauss(distance_mat(trX, Xgf), 0.95), trY))
    #
    #     a = baifen(output_matx)
    #     sk.append(a)
    #     print(a)
    #
    # for i in range(6):
    #     print(i,':',sk[i]/sum(sk))

    """
    单个测试
    """
    # output_mat = output_layer(sum_layer(Gauss(distance_mat(trX, teX), 0.9), trY))  #从这里找我要的 国企1.1，非国企 0.9
    # mrpre = Mr(teX)
    # print(np.reshape(output_mat,(1,len(output_mat))))
    # print(np.reshape(mrpre,(1,len(mrpre))))
    # print(np.reshape(teY,(1,len(teY))))
    # rmse = RMSE(output_mat,teY)
    # rmse1 = RMSE(mrpre, teY)
    # print('GRNN:',rmse)
    # print('MR:',rmse1)

    """
    下面这段是画图
    """
    sigma = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
    rmse = []
    for sig in sigma:
        output_mat = output_layer(
            sum_layer(
                Gauss(
                    distance_mat(
                        trX,
                        teX),
                    sig),
                trY))
        rmse.append(RMSE(output_mat, teY)[0, 0])  # 矩阵要用[0,0]

    plt.figure(figsize=(8, 4))
    plt.plot(sigma, rmse, label="", color="red", marker='*')
    plt.xlabel("sigam value")
    plt.ylabel("RMSE")
    plt.title("PyPlot RMSE in different sigma")
    # plt.ylim(-1.2, 1.2)
    plt.show()
