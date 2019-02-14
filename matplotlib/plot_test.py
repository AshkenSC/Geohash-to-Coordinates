import numpy as np

# 每隔200毫秒等时距取样
t = np.arange(0., 5., 0.2)

# 红色虚线，蓝色方块，绿色三角
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.show()