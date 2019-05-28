import numpy as np
from matplotlib.pyplot import plot
from matplotlib.pyplot import show

# 简单移动平均线

N = 5      # 5天移动平均线
weights = np.ones(N) / N
print('权重 weights =',weights)

close = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3, ), unpack=True, skiprows=1)
sma = np.convolve(weights,close)[N-1:-N+1]     # 简单移动平均线
t = np.arange(N - 1, len(close))
plot(t, close[N - 1:], lw=1.0)
plot(t, sma, lw=2.0)
show()