# noinspection PyUnresolvedReferences
# input: Wsi,Woi and λ
import numpy as np
import pandas as pd

in_txt = "input-weight-WQI.txt"
df = pd.read_table(in_txt, sep="	")  # split the input file by space
df = df.iloc[:, 1:5].values  # extract values
value = np.array(df)
'''calculate W1-i'''
i = 0
W1istorage = []
OutputData = open("output-W1i.txt", 'r+')
OutputData.truncate()  # empty the file when running again
print("pH	DO	BOD	Ss	CHa-a	COD	Sulfide	NO3	NH4	NO2	PO4	Zn	Cd	Hg	Pb	Cu	",
      file=OutputData)  # Write W1-i to the output file
for i in range(16):
    W1i = round(value[i, 2] * value[i, 0] + (1 - value[i, 2]) * value[i, 1], 3)  # calculate W1-i
    W1istorage.append(W1i)
    print(W1i, end='   	', file=OutputData)
OutputData.close()
'''calcaulte Vindicator-i'''
in_txt2 = 'input-indic_limit.txt'
df2 = pd.read_table(in_txt2, sep="	")
df2 = df2.iloc[:, 1:2].values
value2 = np.array(df2)


def compare(a, b):  # Define comparison function
    if a > b:
        c = b / a
    else:
        c = 1
    return c


value_lab = np.loadtxt(open('input-lab-WQI.csv', "rb"), dtype='str', delimiter=",",
                       skiprows=1)  # convert the lab values to array
value_lab = np.delete(value_lab, 0, axis=1)
value_lab = value_lab.astype(np.float64)
V_indicator1 = np.zeros((23, 16))
for i in range(23):
    V_indicator1[i, 1] = 1 / compare(value2[1], value_lab[i, 1]) # The V_indicaor of DO is obtained separately
    V_indicator1[i, 0] = 1
    for j in range(2, 16):
        V_indicator1[i, j] = (compare(value_lab[i, j], value2[j]))  # Get the V_indicaor of the remaining parameters
'''Judge whether the sum of W1-i is 3'''
sum = 0
for item in W1istorage:
    sum += item
if sum == 3:
    print('The sum of W1i is 3, meeting the requirements')
else:
    print('The sum of W1i is not 3, it is %f' % sum)
'''calculate WQI'''
WQI = []
for i in range(23):
    wqi = 0
    for j in range(16):
        wqi += W1istorage[j] * V_indicator1[i, j] * value[j, 3]
    WQI.append(wqi)
OutputData = open("output-WQI.txt", 'r+')
OutputData.truncate()  # empty the file when running again
for i in range(23):
    print('Y%d  %.3f' % (i+1, WQI[i]), file=OutputData)
