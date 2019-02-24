import numpy as np
import matplotlib.pyplot as plt

names = ['sub_a', 'sub_b', 'sub_c']
values = [5, 25, 125]

plt.figure(num='hello', figsize=(9, 3))

plt.subplot(1,3,2)
plt.bar(names, values)
plt.subplot(1,3,1)
plt.scatter(names, values)
plt.subplot(1,3,3)
plt.plot(names, values, marker=',', visible=False)
plt.suptitle('Subplots')
plt.show()

