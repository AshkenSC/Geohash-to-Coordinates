import numpy as np
import matplotlib.pyplot as plt

'''����ָ���ƶ�ƽ����'''

# ����Ȩ������weights
x = np.arange(5)
N = 5
weights = np.exp(np.linspace(-1.,0.,N))
weights /= weights.sum()

# ������Դ��ȡ���̼�close
close = np.loadtxt("petro_china.csv", delimiter=',', usecols=(3, ), unpack=True, skiprows=1)

# ����ָ���ƶ�ƽ����ema
ema = np.convolve(weights, close)[N-1:-N+1]

# ������
t = np.arange(N-1, len(close))

# ��ͼ
plt.plot(t, close[N-1:], lw=1.0)                # �������̼�
plt.plot(t, ema, lw=2.0)                        # ����ema
plt.legend(loc='best', labels=['close', 'ema']) # ����ͼ��
plt.grid()                                      # ��������
plt.show()