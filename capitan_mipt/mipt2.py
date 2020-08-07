import numpy as np
from numpy import exp, sqrt

X = []
Y = []
M = []

start = True
with open('dataset_328552_3.txt') as input:
    for line in input:
        if (start):
            [n, p, k, m] = list(map(int, line.split()))
            start = False
        else:
            X.append(float(line.split()[0]))
            Y.append(float(line.split()[1]))
            M.append(float(line.split()[2]))

distances = np.zeros([n, n])
for i in range(n):
    for j in range(n):
        if (i != j):
            distances[i, j] = sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
        else:
            distances[i, j] = float('inf')

path = [1]
for i in range(n):
    path.append(np.argmin(distances[path[i] - 1]) + 1)
    for j in range(n):
        distances[path[i] - 1][j] = float('inf')
        distances[j][path[i] - 1] = float('inf')

print(' '.join(map(str, path)))