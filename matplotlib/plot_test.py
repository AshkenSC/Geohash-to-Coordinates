import numpy as np
import matplotlib.pyplot as plt

input_values = [1, 2, 3, 4, 5]
squares = [1, 4, 6, 9, 16, 25]
plt.plot(input_values, squares, linewidth = 5)

# set caption and label axes
plt.title("Square numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)

# set tick size
plt.tick_params(axis='both', labelsize=14)

plt.show()