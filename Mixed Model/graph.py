# import matplotlib
# import math as m
# import numpy as np

# def sig(x):
#     return 1/(1+m.exp(x))

# def sig2(x):
#     return m.exp(x)/(1+m.exp(x))

# x = np.linspace(-100, 100)
# sigma = np.linspace(-100, 100)
# y=[]
# y = sig2(sigma) + sig(-x)

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

init = np.random.normal(size=1, loc = 3)
e = np.random.normal(size=1000, scale = 3)

y = np.zeros(1000)
z = np.zeros(1000)
y[0] = init
print(len(y))
z[0] = init
print(len(z))

for t in range(1,1000):
    y[t] = 3 + 1 * y[t-1] + e[t] # beta1 = 1 단위근 모형
    z[t] = 3 + 0.1*z[t-1] + e[t] # beta1 = 0.1

fig,ax = plt.subplots(1,2)
ax[0].plot(y)
ax[0].set_title("Non-Stationary")
ax[1].plot(z)
ax[1].set_title("Stationary")
plt.show()    