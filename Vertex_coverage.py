from scipy.optimize import linprog
import numpy as np

precision = 10^-10

def Is_Vertex_Cover(matrix, X, n_colums): # проверяет образует ли набор X Vertex Cover matrix
    cover_colum = set()
    for i in X:
        for j in range(n_colums):
            if matrix[i][j] != 0:
                cover_colum.add(j)
    if len(cover_colum) == n_colums:
        return 1
    else:
        return 0


def Is_more(x1, x2): # сравнивает числа
    if x1 - x2 >= precision:
        return 1
    else:
        return 0


def Threshold_rounding(X, matrix_non_trans, porog, n_colms, n_rows): # функция порогового округления
    porog = 1 / porog
    vertex_cover = []

    for i in range(n_rows):
        if Is_more(X[i], porog):
            vertex_cover.append(i)
            if Is_Vertex_Cover(matrix_non_trans, vertex_cover, n_colms):
                break
    return vertex_cover

def Probability_rounding(X, matrix_non_trans, n_colms, n_rows): # вероятностное округление
    vertex_cover = []

    flag = 1
    my_rows = dict((i, X[i]) for i in range(n_rows))

    while flag:
        for i in vertex_cover:
            if i in my_rows.keys():
                my_rows.pop(i)

        for i in my_rows.keys():
            el = np.random.choice([1, 0], size=None, replace=False, p=[my_rows[i], 1 - my_rows[i]])
            if el != 0:
                vertex_cover.append(i)
        if Is_Vertex_Cover(matrix_non_trans, vertex_cover, n_colms):
            flag = 0
            break

    return vertex_cover


n_colms, n_rows = map(int,input().split())
s = dict((i, []) for i in range(1,n_rows+1))
for i in s.keys():
    a = list(map(int,input().split()))
    s[i] = a

matrix = [] # матрица коэффициентов
for i in range(n_rows):
    matrix.append([0] * n_colms)

for i in range(n_rows):
    for j in range(n_colms):
        if (j in s[i+1][1:]):
            matrix[i][j] = -1
        else:
            matrix[i][j] = 0

# for i in range(n_rows):
#     print(matrix[i], end="\n")

porog = 0
cur_max = 0
for i in range(n_colms):
    cur_max = 0
    for j in range(n_rows):
        if matrix[j][i] != 0:
            cur_max += 1
    if cur_max > porog:
        porog = cur_max

# print("porog = ",porog)


c    = [] # коэффициенты задачи оптимизации
b_ub = [] # правые части неравенств

for i in range(n_colms):
    b_ub.append(-1)

for i in s.keys():
    c.append(s[i][0])

matrix_non_trans = matrix

matrix = np.array(matrix)
matrix = matrix.transpose()


cor = []
for i in range(n_rows):
     cor.append(tuple((0,1)))
cor = tuple(cor)


res_lin_solv = linprog(c, A_ub= matrix, b_ub= b_ub, bounds= cor)
X = res_lin_solv.x
# print(res_lin_solv)


vertex_cover_porog = Threshold_rounding(res_lin_solv.x, matrix_non_trans, porog,n_colms, n_rows)
vertex_cover_probl = Probability_rounding(res_lin_solv.x, matrix_non_trans, n_colms, n_rows)

if len(vertex_cover_porog) < len(vertex_cover_probl):
    vertex_cover = vertex_cover_porog
else:
    vertex_cover = vertex_cover_probl

# for i in vertex_cover:
#     print(i+1, end= ' ')
# print(vertex_cover)






