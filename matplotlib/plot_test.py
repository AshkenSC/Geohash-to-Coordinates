import numpy as np
import matplotlib.pyplot as plt

data = [2, 4, 8, 16, 32]

plt.bar([0.3, 1.7, 4, 6, 7], data, width=0.6, bottom=[10, 0, 5, 0, 5], color='rgbrg')
plt.show()

