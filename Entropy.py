import numpy as np
import math


def entropy(in_csv, title): #define a function to calculate Entropy weight
    """the array of xij"""
    m = len(open(in_csv, 'r+').readlines()) - 1  # number of rows
    value = np.loadtxt(open(in_csv, "rb"), dtype='str', delimiter=",", skiprows=1)
    value = np.delete(value, 0, axis=1)
    value = value.astype(np.float64)
    value2 = value  # for yij
    value3 = value  # for pij
    n = len(value[0, :])  # number of cloumns
    '''the array of yij'''
    Xmax=[]
    Xmin=[]
    for i in range(n):
        xmax = np.max(value[:, i])
        xmin = np.min(value[:, i])
        Xmax.append(xmax)
        Xmin.append(xmin)
    count = 0
    while count < m:
        for i in range(n):
            value2[count, i] = (value[count, i] - Xmin[i]) / (Xmax[i] - Xmin[i])
        count += 1
    '''the array of pij'''
    count = 0
    Sum = []
    for k in range(n):
        sum = 0
        for j in range(m):
            sum += (0.0001 + value2[j, k])
        Sum.append(sum)
    while count < m:
        for i in range(n):
            value3[count, i] = (0.0001 + value2[count, i]) / Sum[i]
        count += 1
    '''list ej'''
    e = []
    for j in range(n):
        sum = 0
        for i in range(m):
            sum += value3[i, j] * math.log(value3[i, j])
        e.append(float(-(1 / math.log(m)) * sum))

    '''calculate wj'''
    wj = []
    sum = 0
    for i in range(n):
        sum += (1 - e[i])
    for j in range(n):
        s = float((1 - e[j]) / sum)
        wj.append('%.3f' % s)
    OutputData = open("output-Entropy.txt", 'a')
    print(title, file=OutputData)
    for i in range(len(wj)):
        s = str(wj[i]).replace('[', '').replace(']', '')  # convert the format to str
        print(s, end='   	', file=OutputData)  # output wj
    OutputData.close()


OutputData = open("output-Entropy.txt", 'r+')
OutputData.truncate()  # empty the file before recording
entropy(in_csv='input-Entropy-bp.csv', title="pH	BOD	DO	Ss	Cha-a	COD	S")
entropy(in_csv='input-Entropy-nut.csv', title='\n' + '\n' + "NO3	NH4	NO2	PO3")
entropy(in_csv='input-Entropy-hm.csv', title='\n' + '\n' + "Zn	Cd	Hg	Pb	Cu")
