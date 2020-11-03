import numpy as np
import math


def ahp(in_txt, pN, title, Type):  # define a function to calculate ahp weight
    with open(in_txt, 'r+') as obj:
        a = obj.readlines()
    mid = a[2].replace("\n", "").split('\t', pN - 1)  # PN: the number of parameters
    ww = [float(i) for i in mid]
    '''use the weight to generate the judge matrix A'''
    value = np.zeros([pN, pN])
    for j in range(pN):
        for i in range(pN):
            value[i, j] = ww[i] / ww[j]
    with open('output-matrixA-AHP.txt', 'a+') as f:
        f.write('matrixA-%s' % Type + '\n')
        np.savetxt(f, value, fmt="%.3f", delimiter=" ")
    n = len(value[0, :])  # number of cloumns
    '''calculate Wi Mi'''
    Mi = []
    Wi = []
    for i in range(0, n):
        mi = 1
        for j in range(n):
            mi = mi * value[i, j]
        Mi.append(mi)
        wi = math.pow(mi, 1 / n)
        Wi.append(wi)
    '''calculate wi'''
    wi = []
    sum = 0
    for j in range(0, n):
        sum += Wi[j]
    for i in range(0, n):
        w = Wi[i] / sum
        w = ('%.3f' % w)
        wi.append(w)
    OutputData = open("output-AHP.txt", 'a')
    print(title, file=OutputData)
    for i in range(len(wi)):
        s = str(wi[i]).replace('[', '').replace(']', '')  # convert to str
        print(s, end='   	', file=OutputData)  # output wi
    OutputData.close()
    '''judge the rationality of the  weight vector'''
    value1 = np.array([Wi])
    value2 = value1.T  # Transpose Wi to the column matrix
    xc = np.dot(value, value2)  # the products of A and Wi
    sum = 0
    for i in range(0, n):
        xc2 = xc[i] / Wi[i]
        sum += xc2
    lamudamax = sum / n
    RI = 1.12
    CI = (lamudamax - n) / (n - 1)
    CR = CI / RI
    print("the consistency ratio CR of %s is %f" % (Type, CR))


with open("output-AHP.txt", 'r+') as a, open("output-matrixA-AHP.txt", 'r+') as b:
    a.truncate()  # empty the file before recording
    b.truncate()
ahp(in_txt='input-AHP-bp.txt', pN=7, title="pH	BOD	DO	Ss	Cha-a	COD	S", Type='bp')
ahp(in_txt='input-AHP-nut.txt', pN=4, title='\n' + '\n' + "NO3	NH4	NO2	PO3", Type='nut')
ahp(in_txt='input-AHP-hm.txt', pN=5, title='\n' + '\n' + "Zn	Cd	Hg	Pb	Cu", Type='hm')
