import numpy as np
import matplotlib.pyplot as plt

'''绘制指数移动平均线'''

# 计算权重数组weights
x = np.arange(5)
N = 5
weights = np.exp(np.linspace(-1.,0.,N))
weights /= weights.sum()

# 从数据源获取收盘价close
close = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3, ), unpack=True, skiprows=1)

# 计算指数移动平均线ema
ema = np.convolve(weights, close)[N-1:-N+1]

# 横坐标
t = np.arange(N-1, len(close))

# 绘图
plt.plot(t, close[N-1:], lw=1.0, color='red')   # 绘制收盘价
plt.plot(t, ema, lw=2.0, color='blue')          # 绘制ema
plt.legend(loc='best', labels=['close', 'ema']) # 绘制图例
plt.grid()                                      # 绘制网格
plt.show()