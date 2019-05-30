import numpy as np
import matplotlib.pyplot as plt

'''绘制简单移动平均线'''

N = 5      # 绘制5天移动平均线，因此N取5
weights = np.ones(N) / N

# 从数据源获取收盘价
close = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3, ), unpack=True, skiprows=1)

# 简单移动平均线
sma = np.convolve(weights,close)[N-1:-N+1]

# 横坐标
t = np.arange(N - 1, len(close))

plt.plot(t, close[N - 1:], lw=1.0, color='red')  # 绘制收盘价
plt.plot(t, sma, lw=2.0, color='blue')           # 绘制SMA
plt.legend(loc='best', labels=['close', 'sma'])  # 绘制图例
plt.show()