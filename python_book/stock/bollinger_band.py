'''绘制布林带'''

import numpy as np
import matplotlib.pyplot as plt

# 计算权重数组weights
N = 5
weights = np.ones(N)/N

# 从数据源获取收盘价close
close = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3, ), unpack=True, skiprows=1)

# 计算简单移动平均线sma
sma = np.convolve(weights, close)[N-1:-N+1]

# 计算标准差
deviation = []
C = len(close)
for i in range(N-1,C):
    if i+N < C:
        dev = close[i:i+N]
    else:
        dev = close[-N:]
    averages = np.zeros(N)
    averages.fill(sma[i-N-1])
    dev = dev - averages
    dev = dev ** 2
    dev = np.sqrt(np.mean(dev))
    deviation.append(dev)

deviation = 2 * np.array(deviation)   # 计算两倍标准差

# 计算上轨线和下轨线
upperBB = sma + deviation
lowerBB = sma - deviation

c_slice = close[N-1:]
between_bands = np.where((c_slice<upperBB)&(c_slice>lowerBB))

# 显示下轨线、收盘价和上轨线数据
print(lowerBB[between_bands])
print(close[between_bands])
print(upperBB[between_bands])

# 横坐标
t = np.arange(N-1,C)

# 绘图
plt.plot(t, c_slice, lw=1.0)    # 绘制
plt.plot(t, sma, lw=2.0)        # 绘制sma
plt.plot(t, upperBB, lw=3.0)    # 绘制下轨线
plt.plot(t, lowerBB, lw=4.0)    # 绘制上轨线
plt.legend(loc='best', labels=['c_slice', 'sma', 'upperBB', 'lowerBB']) # 绘制图例
plt.show()