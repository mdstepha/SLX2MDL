#!/usr/bin/python3 

import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns
import numpy as np 
from sklearn.metrics import r2_score 
from numpy.polynomial import Polynomial
from statistics import mean 
from matplotlib import style
from pylab import rcParams 





line_time = [
(1443, 1142),
(3798, 2931),
(2835, 2148),
(1953, 1464),
(9593, 11216), #
(2459, 1865),
(1517, 1253),
(2592, 1972),
(3359, 2809),
(3816, 2929),
(2624, 1927),
(2197, 1618),
(1635, 1494),
(1578, 1280),
(1836, 1455),
(2586, 2137),
(1632, 1317),
(1498, 1114),
(4007, 3802),
(3180, 2542),
(2409, 1930),
(3889, 3360),
(1350, 1103),
(1825, 1515),
(2197, 1525),
(4606, 3523),
(1662, 1262),
(1871, 1542),
(7946, 8136),  # 
(4924, 4688),
(2578, 1899),
(2352, 1723),
(4594, 4159),
(3500, 2954),
(1750, 1382),
(1598, 1259),
(2018, 1515),
(1702, 1419),
(5189, 3907),
(10590, 12541),  # 
(3814, 3052),
(2135, 1494),
]

lines = [] 
times = [] 
for l, t in line_time:
    lines.append(l)
    times.append(t)

plt.figure(figsize=(10, 5))

plt.xlabel('Model Size (number of source lines in MDL file)')
plt.ylabel('Execution Time (ms)')
# plt.title('Time taken for SLX2MDL transformation vs. model size')


xs = np.array(lines)
ys = np.array(times)

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

m, c = best_fit_slope_and_intercept(xs, ys)

# compute r-squared value of the line of best fit 
def predict(x, m, c): 
    return m * x + c
r_squared = r2_score(ys, predict(xs, m, c))
r_squared_percent = r_squared * 100 
print("r_squared : ", r_squared* 100, "%")


regression_line = [(m*x)+c for x in xs]

style.use('ggplot')

plt.plot(xs,ys, '.', color='#003F72')
eqn = f"y = {m:.2f}x - {-c:.2f}" if c < 0 else f"{m:.2f}x + {c:.2f}"
plt.plot(xs, regression_line, label=f'line of best fit: {eqn}; r\N{SUPERSCRIPT TWO} = {r_squared_percent:.2f}%')
plt.legend(loc=2)












print(f"average execution time : {np.mean(xs)} seconds")

plt.show()










