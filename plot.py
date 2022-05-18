import csv
import numpy as np
import matplotlib.pyplot as plt

with open('data.csv') as file:
    csvreader = csv.reader(file)
    x_vals = []
    y_vals = []
    for row in csvreader:
        x_vals.append(float(row[0]))
        y_vals.append(float(row[1]))
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    plt.plot(x_vals, y_vals)
    plt.figure()
    plt.plot(x_vals)
    plt.plot(y_vals)
    plt.show()