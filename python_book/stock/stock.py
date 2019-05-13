import numpy as np
c, v = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3,5), unpack=True)
print(c)
print(v)