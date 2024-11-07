import matplotlib.pyplot as plt
import numpy as np

x = np.array(["A", "B", "C", "D"])
y = np.array([3, 8, 1, 10])

# plt.bar(x,y)
plt.barh(x, y, height = 0.1) # h for horizontal bar
#if the bar is horizontal then height otherwise width applies
plt.show()