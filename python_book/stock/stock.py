import numpy as np
c, v = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3,5), unpack=True, skiprows=1)
# skiprows=1 设置跳过开头的行数（不是行号）
print(c)
print(v)