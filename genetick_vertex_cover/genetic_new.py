from scipy.optimize import linprog
import numpy as np
import time

precision = 10^-10



Mut_const = 7
def Mutation(vertex_cover, s: dict, n_rows: int, n_colums: int)->list:
    away = np.random.randint(0, n_rows, size=Mut_const)
    new_vertex_cover = [el for el in vertex_cover if el not in away]
    in_set = set()
    #print(s)
    for el in new_vertex_cover:
        for i in range(1,len(s[el])):
            in_set.add(s[el][i])
    # print(in_set)
    # жадный алгоритм

    my_struct = dict()
    for el in vertex_cover:
        cur_num = 0
        if el not in new_vertex_cover:
            for i in range(1, len(s[el])):
                if s[el][i] not in in_set:
                    cur_num += 1
            my_struct[el] = cur_num

    sort_my_struct = sorted(my_struct.items(), key=lambda x: x[1], reverse=True)
    #print(sort_my_struct)

    # proverka = set(i for i in range(n_colums))
    for el in sort_my_struct:
        for i in range(1, len(s[el[0]])):
            in_set.add(s[el[0]][i])
        new_vertex_cover.append(el[0])
        if len(in_set) == n_colums:
            break

    if len(in_set) == n_colums:
        return new_vertex_cover
    else:
        return vertex_cover


    # print(new_vertex_cover)
    # return new_vertex_cover


def crossing (vertex_cover_1: list, vertex_cover_2: list, n_colums: int)->list:
    v_1 = set(vertex_cover_1)
    v_2 = set(vertex_cover_2)

    common = v_1.intersection(v_2)

    non_v1 = []
    for el in vertex_cover_1:
        if el not in common:
            non_v1.append(el)

    non_v2 = []
    for el in vertex_cover_2:
        if el not in common:
            non_v2.append(el)

    # print(common)
    flag = 0

    while Is_vertex_cover_new(list(common), s, n_colums) != 1:
        if flag == 0 and len(non_v1) != 0:
            common.add(non_v1[0])
            non_v1 = non_v1[1:]
            flag = 1
        elif flag == 1 and len(non_v2) != 0:
            common.add(non_v2[0])
            non_v2 = non_v2[1:]
            flag = 0
        else:
            if flag == 0:
                flag = 1
            else:
                flag = 0

    return list(common)


def Is_vertex_cover_new(X, s, n_colms: int):
    vert_cov = set()
    for el in X:
        for i in s[el][1:]:
            vert_cov.add(i)
    if len(vert_cov) == n_colms:
        return 1
    else:
        return 0

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

def Threshold_rounding(X, matrix_non_trans, porog, n_colms, n_rows): # функция порогового округления
    porog = 1. / porog
    vertex_cover = []

    for i in range(n_rows):
        if X[i] >= porog:
            vertex_cover.append(i)
            if Is_Vertex_Cover(matrix_non_trans, vertex_cover, n_colms):
                break
    return vertex_cover


n_colms, n_rows = map(int,input().split())
s = dict((i, []) for i in range(0,n_rows))
s1 =  dict((i, []) for i in range(1,n_rows+1))
A = []
for i in s.keys():
    a = list(map(int,input().split()))
    s[i] = a
    s1[i+1] = a
    A.append(a[1:])

if n_rows < 100:
    s = s1
    matrix = []  # матрица коэффициентов
    for i in range(n_rows):
        matrix.append([0] * n_colms)

    for i in range(n_rows):
        for j in range(n_colms):
            if (j in s[i + 1][1:]):
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

    c = []  # коэффициенты задачи оптимизации
    b_ub = []  # правые части неравенств

    for i in range(n_colms):
        b_ub.append(-1)

    for i in s.keys():
        c.append(s[i][0])

    matrix_non_trans = matrix

    matrix = np.array(matrix)
    matrix = matrix.transpose()

    cor = []
    for i in range(n_rows):
        cor.append(tuple((0, 1)))
    cor = tuple(cor)

    res_lin_solv = linprog(c, A_ub=matrix, b_ub=b_ub, bounds=cor)
    X = res_lin_solv.x
    # print(res_lin_solv)

    vertex_cover_porog = Threshold_rounding(X, matrix_non_trans, porog, n_colms, n_rows)
    # vertex_cover_probl = Probability_rounding(res_lin_solv.x, matrix_non_trans, n_colms, n_rows)

    # if len(vertex_cover_porog) < len(vertex_cover_probl):
    #     vertex_cover = vertex_cover_porog
    # else:
    #     vertex_cover = vertex_cover_probl
    vertex_cover = vertex_cover_porog
    for i in vertex_cover:
        print(i + 1, end=' ')

else:


    vertex_cover = [i for i in range(n_rows)]
    # for i in vertex_cover:
    #     print(i+1, end= ' ')
    # print(vertex_cover)



    # -------------------------------///////////////////////---------------------------------------



    v_c1 = Mutation(vertex_cover, s, n_rows, n_colms)
    # v_c2 = Mutation(vertex_cover,matrix_non_trans, s, n_rows, n_colms)

    cr_1 = crossing(v_c1, vertex_cover, n_colms)


    A = [v_c1, vertex_cover, cr_1]
    opt = 10**10
    for i in A:
        # print(len(i))
        if len(i) < opt:
            opt = len(i)


    # start_t = time.time()


    FLAG = 0
    depth = 25

    start_t = time.time()
    while FLAG != depth and time.time() - start_t < 27:
        new_buf = A
        for i in range(4):
            new_buf.append(Mutation(new_buf[i],  s, n_rows, n_colms))

        for i in range(4):
            new_buf.append(crossing(new_buf[i], new_buf[6-i], n_colms))

        new_generation = sorted(new_buf, key=lambda x: len(x))
        A = new_generation[:3]
        if len(A[0]) == opt:
            FLAG += 1
        elif len(A[0]) < opt:
            FLAG = 0
            opt = len(A[0])
        # print(new_generation)

    # print(A)
    for i in A[0]:
        print(i+1, end= ' ')


