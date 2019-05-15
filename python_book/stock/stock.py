import numpy as np
close, volume = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3,5), unpack=True, skiprows=1)
# skiprows=1 设置跳过开头的行数（不是行号）

# 1. 计算成交量加权平均价
vwap = np.average(close,weights=volume)
print('vwap=',vwap)

# 2. 计算收盘时算术平均价
mean = np.mean(close)
print('mean=',mean)

# 3. 计算收盘时加权平均价（时间与现在越近，权重越大）
t = np.arange(len(close))
twap = np.average(close,weights=t)
print('twap=',twap)