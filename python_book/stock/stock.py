import numpy as np
close, volume = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3,5), unpack=True, skiprows=1)
# skiprows=1 设置跳过开头的行数（不是行号）

# 1. 计算成交量加权平均价
vwap = np.average(close,weights=volume)
print('成交量加权平均价 vwap=',vwap)

# 2. 计算收盘时算术平均价
mean = np.mean(close)
print('收盘时算术平均价 mean=',mean)

# 3. 计算收盘时加权平均价（时间与现在越近，权重越大）
t = np.arange(len(close))
twap = np.average(close,weights=t)
print('收盘时加权平均价 twap=',twap)

# 4. 获取最高价、最低价
high,low = np.loadtxt('petro_china.csv', delimiter=',',usecols=(2,4),unpack=True, skiprows=1)
print('该时段每日最高价：')
print(high)     # 输出最高价
print('该时段每日最低价：')
print(low)      # 输出最低价

highest = np.max(high)
print('时段内历史最高价 highest=', highest)
lowest = np.min(low)
print('时段内历史最低价 lowest=', lowest)
average = (highest+lowest)/2
print('均值 average = ',average)

# 5. 计算最大值和最小值的波动范围
print('最大值波动范围=',np.ptp(high))
print('最小值波动范围=',np.ptp(low))


'''计算中位数和方差'''
# 6.1 计算中位数方法一
median = np.median(close)
print('median = ',median)

# 6.2 计算中位数方法二
sorted = np.msort(close)
print('sorted = ',sorted)
N = len(close)
middle = sorted[int((N-1)/2)]
print('middle = ',middle)
average_mid = (sorted[int(N/2)] + sorted[int((N-1)/2)])/2
print('average_middle = ',average_mid)
