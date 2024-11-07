import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 6, 8])
y = np.array([3, 8, 1, 10])

# plt.plot(y,'o:b',ms=20,mec='red',mfc='k') # ms for marker size nd mec is markedgecolor nd mfc is markerfacecolor

# you can also set color , linewidth and linestyle
# plt.plot(y,linewidth=20,linestyle='dashed',color='red')
plt.plot(x)
plt.plot(y)
# you can also change font and color of the font of label and title
font1 = {'family':'serif','color':'blue','size':20}
plt.xlabel('number',fontdict=font1,loc='center')
plt.ylabel('price',loc='bottom')
plt.title('ese',loc = 'left') # you can change location of the title
plt.grid() # you can also give style, color and width to the grid line
plt.show()