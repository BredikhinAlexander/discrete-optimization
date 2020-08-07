import numpy as np
from numpy import sqrt

A = []
X = []
Y = []
BASE = []

with open("dataset_328552_2.txt") as f:
    s = f.readline()
    n, p, k, m = map(int, s.split(' '))
    l = f.readline()
    BASE = list(map(int, l.split(' ')))
    for line in f:
        A.append(list(map(float, line.split(' '))))

val = 0
n = n - 1
for i in range(n):
    X.append(A[i][0])
    Y.append(A[i][1])
    val

X = np.asarray(X)
Y = np.asarray(Y)

S_S = []
L_W = []



M = np.zeros([n, n])
for i in range(n):
    for j in range(n):
        if i != j:
            M[i, j] = sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
        else:
            M[i, j] = float('inf')
print("tyt")
print(n)
for ib in range(n):
    M_1 = np.zeros([n, n], dtype=float)
    M_1 = M_1 + M
    way = []
    way.append(ib)
    for i in range(1, n):
        s = []
        for j in range(n):
            s.append(M_1[way[i - 1], j])
        way.append(s.index(min(s)))
        for j in range(i):
            M_1[way[i], way[j]] = float('inf')
    S = sum([sqrt((X[way[i]] - BASE[0]) ** 2 + (Y[way[i]] - BASE[1]) ** 2) + sqrt(
        (X[way[i]] - X[way[i + 1]]) ** 2 + (Y[way[i]] - Y[way[i + 1]]) ** 2) for i in range(n - 1)]) + sqrt(
        (X[way[n - 1]] - BASE[0]) ** 2 + (Y[way[n - 1]] - BASE[1]) ** 2)
    S_S.append(S)
    L_W.append(way)
    print("tyt", ib)

print("tyt")
print("")
way = L_W[S_S.index(min(S_S))]

s = ""
for item in way:
    s += str(item + 2) + ' '
print(s[:-1])