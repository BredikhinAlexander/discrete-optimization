import numpy as np
import time

Mut_const = 7 # константа, которая показывает сколько строк в вершинном покрытии мы будем менять
def Mutation(vertex_cover, s: dict, n_rows: int, n_colums: int)->list: # функция мутации
    away = np.random.randint(0, n_rows, size=Mut_const) # выбираем рандомно строки, которые выбросим из vertex_cover
    new_vertex_cover = [el for el in vertex_cover if el not in away]
    in_set = set()

    for el in new_vertex_cover:  # строим множество столбцов, которое мы все равно покрываем даже после выбрасывания
        for i in range(1,len(s[el])):
            in_set.add(s[el][i])

    # жадный алгоритм

    my_struct = dict()  # смотрим, сколько столбцов покрывают те строки, которых нет в вершинном покрытии
    for el in vertex_cover:
        cur_num = 0
        if el not in new_vertex_cover:
            for i in range(1, len(s[el])):
                if s[el][i] not in in_set:
                    cur_num += 1
            my_struct[el] = cur_num

    sort_my_struct = sorted(my_struct.items(), key=lambda x: x[1], reverse=True) # сортируем по этому количеству, чтобы затем брать более выгодные

    for el in sort_my_struct: # добавляем, пока не получим вершинное покрытие
        for i in range(1, len(s[el[0]])):
            in_set.add(s[el[0]][i])
        new_vertex_cover.append(el[0])
        if len(in_set) == n_colums:
            break

    if len(in_set) == n_colums: # на всякий раз проверяем, что в итоге получили вершинное покрытие, а то вдруг я неправильно написал функцию)))
        return new_vertex_cover
    else:
        return vertex_cover



def crossing (vertex_cover_1: list, vertex_cover_2: list, n_colums: int)->list: # функция скрещивания
    v_1 = set(vertex_cover_1)
    v_2 = set(vertex_cover_2)

    common = v_1.intersection(v_2) # смотрим, какие строик есть в обоих вершинных покрытиях

    non_v1 = []
    for el in vertex_cover_1:  # смотрим, что разное
        if el not in common:
            non_v1.append(el)

    non_v2 = []
    for el in vertex_cover_2:
        if el not in common:
            non_v2.append(el)

    flag = 0

    while Is_vertex_cover_new(list(common), s, n_colums) != 1: # по очереди берём пока не появится вершинное покрытие
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


def Is_vertex_cover_new(X, s, n_colms: int): # функция которое по массиву строк проверяет образует он вершинное покрытие или нет
    vert_cov = set()
    for el in X:
        for i in s[el][1:]:
            vert_cov.add(i)
    if len(vert_cov) == n_colms:
        return 1
    else:
        return 0


n_colms, n_rows = map(int,input().split())
s = dict((i, []) for i in range(0,n_rows))
A = []
for i in s.keys():
    a = list(map(int,input().split()))
    s[i] = a
    A.append(a[1:])


vertex_cover = [i for i in range(n_rows)] # берём все строки сначала а затем запускаем наш генетический алгоритм

v_c1 = Mutation(vertex_cover, s, n_rows, n_colms) # делаем первого мутанта
cr_1 = crossing(v_c1, vertex_cover, n_colms) # скрещиваем его со всеми строками


A = [v_c1, vertex_cover, cr_1] # считаем оптимальный размер вершинного покрытия на данный момент
opt = 10**10
for i in A:
    if len(i) < opt:
        opt = len(i)



FLAG = 0
depth = 15 # переменная, котороая отвечает за глубину генетики: сколько раз мы должны получить одно и то же, чтобы прекратить и успокоиться

start_t = time.time()
while FLAG != depth and time.time() - start_t < 27:
    new_buf = A
    for i in range(3): # делаем для каждого вершинного покрытия по мутанту
        new_buf.append(Mutation(new_buf[i],  s, n_rows, n_colms))

    for i in range(3): # скрещиваем с полученными мутантами
        new_buf.append(crossing(new_buf[i], new_buf[5-i], n_colms))

    new_generation = sorted(new_buf, key=lambda x: len(x)) # сортируем по размеру вершинного покрытия
    A = new_generation[:3] # выкидываем слабых
    if len(A[0]) == opt:
        FLAG += 1
    elif len(A[0]) < opt: # меняем оптимум если нашли что-то лучше
        FLAG = 0
        opt = len(A[0])


for i in A[0]:
    print(i+1, end= ' ')