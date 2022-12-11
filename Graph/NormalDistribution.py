import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 

x = np.arange(-5,5,0.01)

def gaussian(x,mean,sigma):
    return (1 / np.sqrt(2*np.pi * sigma**2)) * np.exp(-(x-mean)**2 / (2*sigma**2))

# legend=[]

# for i in range (1,5):
#     legend.append(f'N(0,{i})')
    
plt.plot(x,gaussian(x,0,1))
plt.xlabel('x')
plt.ylabel('density')
#plt.legend(legend)

cum = np.arange(-1.96, 1.96, 0.01) #1
plt.fill_between(cum, norm.pdf(cum), alpha=0.5, color='g')

plt.savefig('normal.png', dpi=72, bbox_inches='tight')

plt.show()