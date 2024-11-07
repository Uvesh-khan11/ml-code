import numpy as np
import matplotlib.pyplot as plt

x = np.array([10,20,30,40,50])
y = np.array([13,24,35,48,57])
mylabels = ["Apples", "Bananas", "Cherries", "Dates",'Pineapples']
myexplode = [0.2, 0, 0, 0,0]
mycolors = ["black", "hotpink", "b", "#4CAF50","red"]
plt.pie(y, labels=mylabels,startangle = 180,explode=myexplode,shadow = True,colors=mycolors)
plt.legend(title="My Fruits:")
plt.show()