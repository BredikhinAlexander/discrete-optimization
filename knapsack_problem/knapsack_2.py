from scipy.optimize import linprog
import sys
import numpy as np
import time

def LP_new(p, v, V: int) -> int:
    max_div = np.argsort(-p/v)
    cur_v = 0
    cur_p = 0
    for i in max_div:
        if cur_v + v[i] > V:
            x = (V-cur_v)/v[i]
            cur_p += p[i]*x
            break
        else:
            cur_p += p[i]
            cur_v += v[i]
    return cur_p


def LP_solution(p, v , V: int) -> float: # долгая функция, лучший вариант выше (так как мы знаем, что в этой задаче будет решением NLP)
    cor = []
    n = p.size
    if n == 0:
        return 0
    for i in range(n):
        cor.append(tuple((0, 1)))
    cor = tuple(cor)

    values  = [-p[i] for i in range(n)]
    volumes = [[v[i] for i in range(n)]]

    res_lin_solv = linprog(c=values, A_ub=volumes, b_ub=V, bounds=cor, method='interior-point')
    # print(res_lin_solv)
    return -res_lin_solv.fun



def Greedy_algorithm_mean(items: dict,
                          total_knapsack_volume: int):  # жадный алгоритм по средниму показателю
    unit_price = dict((i, items[i][1] / items[i][0]) for i in items.keys())
    sort_price = (sorted(unit_price.items(), key=lambda item: item[1]))
    sort_price.reverse()
    # print(sort_price)

    optimal_items = []
    opt = 0
    cur_volume = 0
    for index in range(len(items)):
        if cur_volume + items[sort_price[index][0]][0] <= total_knapsack_volume:
            cur_volume += items[sort_price[index][0]][0]
            optimal_items.append(sort_price[index][0])
            opt += items[sort_price[index][0]][1]
    return opt, optimal_items

def greedy(p,v,V: int): # через nm массивы

    max_div = np.argsort(-p/v)

    cur_v = 0
    cur_p = 0

    vis = np.zeros(p.size)

    for el in max_div:
        if cur_v + v[el] <= V:
            vis[el] = 1
            cur_p += p[el]
            cur_v += v[el]

        elif v[el] <= V:
            cur_p = max(cur_p, p[el])
            if cur_p == p[el]:

                vis = np.zeros(p.size)
                vis[el] = 1
            break

    return cur_p, vis

start_t = time.time()
def pruning(p, v, V, curP, vis):
    global opt
    global n
    global start_t
    # if time.time() - start_t < 28:
    #     print(int(opt))
    #     exit()

    if p.size > 0 and time.time() - start_t < 27: # проходит +1 тест!!!!!
        if vis[0]:
            pruning(p[1:], v[1:], V - v[0], curP + p[0], vis[1:])

            lin_bnd = LP_new(p[1:], v[1:], V)
            lin_bnd += curP

            if lin_bnd > opt:
                greedy0, vis0 = greedy(p[1:], v[1:], V)

                if opt < greedy0 + curP:
                    opt = greedy0 + curP
                pruning(p[1:], v[1:], V, curP, vis0)
        else:
            pruning(p[1:], v[1:], V, curP, vis[1:])
            if v[0] <= V:
                lin_bnd = LP_new(p[1:], v[1:], V - v[0])
                lin_bnd += (curP + p[0])

                if lin_bnd > opt:
                    greedy1, vis1 = greedy(p[1:], v[1:], V - v[0])

                    if opt < greedy1 + curP + p[0]:
                        opt = greedy1 + curP + p[0]
                    pruning(p[1:], v[1:], V - v[0], curP + p[0], vis1)



V = int(input())
n = int(input())
sys.setrecursionlimit(2*n)

items = dict((i, []) for i in range(n))
for i in items.keys():
    item_volume_value = list(map(int, input().split()))
    items[i] = item_volume_value

# удлим элементы, которые не смогут войти в рюкзак
# new_items = items.copy()
# for i in items.keys():
#     if items[i][0] > V:
#         new_items.pop(i)
# items = new_items
# n = len(items)

# print(items)

# opt, opt_items = Greedy_algorithm_mean(items, V)
# print(opt)

p = np.zeros(n)
v = np.zeros(n)
print(type(p))
# vis = np.zeros(n)

ind = 0
for el in items.keys():
    v[ind], p[ind] = items[el][0], items[el][1]
    # if el in opt_items:
    #     vis[ind] = 1
    ind += 1

opt, vis = greedy(p,v,V)
# print(v)
# print(p)
# print(vis)

# print(LP_solution(p,v,V))

pruning(p,v,V,0,vis)


print(int(opt))


