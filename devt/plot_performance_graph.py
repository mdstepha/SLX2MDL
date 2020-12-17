#!/usr/bin/python3 

# This script plots the performance-report data from (multiple) csv files (specified in var 'files') in a graph
# It does not save the graph. To save the graph, use GUI once the graph opens. 

import matplotlib.pyplot as plt 
import numpy as np 
from sklearn.metrics import r2_score 
from statistics import mean 
from matplotlib import style

WIDE = True

files = [
    '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/working-dir-github/performance-report.csv',
    '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/working-dir-matlab-central/performance-report.csv',
    '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/working-dir-other/performance-report.csv',
    '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/working-dir-source-forge/performance-report.csv',    
]

line_time = []  # each entry will be a tuple of (nlines, time)
lines_total = 0
time_total = 0
n = 0

for file in files:
    print()
    print(file) 
    print()
    with open(file, 'r') as f:
        f.readline()  # skip header 
        for line in f.readlines():
            line = line.strip()
            path, nlines, time = line.split(',')
            nlines = int(nlines)
            time = float(time)
            print(nlines, time)
            line_time.append((nlines, time))
            lines_total += nlines
            time_total += time 
            n += 1 

lines = [] 
times = [] 
for l, t in line_time:
    lines.append(l)
    times.append(t)

if WIDE:
    plt.figure(figsize=(10,5))

plt.xlabel('Model Size (number of source lines in MDL file)')
plt.ylabel('Execution Time (s)')
# plt.title('Time taken for SLX2MDL transformation vs. model size')

xs = np.array(lines)
ys = np.array(times)

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    b = mean(ys) - m * mean(xs)
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
eqn = f"y = {m:.4f}x - {-c:.2f}" if c < 0 else f"{m:.2f}x + {c:.2f}"
# plt.plot(xs, regression_line, label=f'line of best fit: {eqn}; r^sq : {r_squared_percent:.2f}%')

plt.plot(xs, regression_line, label=f'line of best fit: {eqn}; r\N{SUPERSCRIPT TWO} = {r_squared_percent:.2f}%')
plt.legend(loc=2)
print(f"average execution time : {np.mean(xs)} seconds")


print(f"\n\n# total models transformed: {n}")
print(f"# total time taken : {time_total} secs")
print(f"avg # lines per model : {lines_total / n}")
print(f"avg # time per model : {time_total / n} secs")


plt.show()













