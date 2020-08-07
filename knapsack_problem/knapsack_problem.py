from scipy.optimize import linprog
import sys

precision = 10^-5

sys.setrecursionlimit(1500)

def comparison(a1: float, a2: float):
    if abs(a1-a2) <= precision:
        return 0
    else:
        return 1


def LP_solution(items: dict, V: int, number_of_items: int) -> float:
    cor = []
    for i in range(number_of_items):
        cor.append(tuple((0, 1)))
    cor = tuple(cor)

    values  = [-items[i][1] for i in items.keys()]
    volumes = [[items[i][0] for i in items.keys()]]

    res_lin_solv = linprog(c=values, A_ub=volumes, b_ub=V, bounds=cor, method='interior-point')
    # print(res_lin_solv)
    return -res_lin_solv.fun


def Greedy_algorithm_mean(items: dict, optimal_items: list, total_knapsack_volume: int) -> int: # жадный алгоритм по средниму показателю
    unit_price = dict((i, items[i][1] / items[i][0]) for i in items.keys())
    sort_price = (sorted(unit_price.items(), key=lambda item: item[1]))
    sort_price.reverse()
    # print(sort_price)

    #optimal_items = []
    opt = 0
    cur_volume = 0
    for index in range(len(items)):
        if cur_volume + items[sort_price[index][0]][0] <= total_knapsack_volume:
            cur_volume += items[sort_price[index][0]][0]
            optimal_items.append(sort_price[index][0])
            opt += items[sort_price[index][0]][1]

    for el in sort_price:
        if el[0] not in optimal_items:
            optimal_items.append(el[0])

    # print(opt, end='\n')
    # print(optimal_items)
    return opt

def Greedy_algorithm_volume(items: dict, optimal_items: list, total_knapsack_volume: int) -> int: # жадный алгоритм по размеру
    sort_volume = sorted(items.items(), key= lambda item: item[1], reverse=False)
    # print(sort_volume)
    opt = 0
    cur_volume = 0
    for i in range(len(items)):
        if cur_volume + sort_volume[i][1][0] <= total_knapsack_volume:
            cur_volume += sort_volume[i][1][0]
            optimal_items.append(sort_volume[i][0])
            opt += sort_volume[i][1][1]

    for el in sort_volume:
        if el[0] not in optimal_items:
            optimal_items.append(el[0])

    return opt



def Greedy_algorithm_value(items: dict, optimal_items: list, total_knapsack_volume: int) -> int: # жадный алгоритм по цене
    sort_value = sorted(items.items(), key= lambda item: item[0], reverse=True)
    # print(sort_volume)
    opt = 0
    cur_volume = 0
    for i in range(len(items)):
        if cur_volume + sort_value[i][1][0] <= total_knapsack_volume:
            cur_volume += sort_value[i][1][0]
            optimal_items.append(sort_value[i][0])
            opt += sort_value[i][1][1]

    for el in sort_value:
        if el[0] not in optimal_items:
            optimal_items.append(el[0])
    return opt



def Pruning(items: dict, n_items: int, path: list, price: int, opt: int, V: int):
    if len(items) == 0:
        return price

    index = number_of_items - n_items
    new_price = 0

    items_right = items.copy()
    items_right.pop(optimal_items[index])
    #print("eeeeeeeeeeeee   ", items[optimal_items[index]][0])
    if len(items_right) != 0:
        OPT_right = LP_solution(items_right, V - items[optimal_items[index]][0], n_items-1)
    else:
        OPT_right = 0
    if price + OPT_right + items[optimal_items[index]][1] >= opt and V-items[optimal_items[index]][0] >= 0:
        path_right = path.copy()
        path_right.append(items[optimal_items[index]][1])
        #price += items[optimal_items[index]][1]
        price = sum(path_right)
        # if price != sum(path_right):
        #     print("Waaaarning", price, sum(path_right))
        new_price = Pruning(items_right, n_items-1, path_right, price, opt, V-items[optimal_items[index]][0])
        # return new_price

    if new_price > opt:
        opt = new_price
# ---------------------------------------------------------------------------
    items_left = items.copy()
    items_left.pop(optimal_items[index])
    if len(items_left) != 0:
        OPT_left = LP_solution(items_left, V, n_items-1)
    else:
        OPT_left = 0
    if price + OPT_left >= opt:
        path_left = path.copy()
        path_left.append(0)
        new_price = Pruning(items_left, n_items-1, path_left, price, opt, V)
        # return new_price


    if new_price > opt:
        opt = new_price
    # ---------------------------------------------------------------------------
    print(opt)
    print(path)
    if opt == 12248:
        print("aaaaaaaaaaaa", path)
        exit(0)

    return opt



total_knapsack_volume = int(input())
number_of_items = int(input())

items = dict((i,[]) for i in range(number_of_items))
for i in items.keys():
    item_volume_value = list(map(int,input().split()))
    items[i] = item_volume_value

# удвлим элементы, которые не смогут войти в рюкзак
new_items = items.copy()
for i in items.keys():
    if items[i][0] > total_knapsack_volume:
        new_items.pop(i)
items = new_items
number_of_items = len(items)
# print(items)
# print(number_of_items)

optimal_items_mean, optimal_items_value, optimal_items_volume= [], [], []
opt_mean   = Greedy_algorithm_mean(items,optimal_items_mean, total_knapsack_volume)
opt_value  = Greedy_algorithm_value(items, optimal_items_value, total_knapsack_volume)
opt_volume = Greedy_algorithm_volume(items, optimal_items_volume, total_knapsack_volume)

optimal_items = []
opt = max(opt_mean, opt_value, opt_volume)
if opt == opt_mean:
    optimal_items = optimal_items_mean
elif opt == opt_volume:
    optimal_items = optimal_items_volume
else:
    optimal_items = optimal_items_value


# my_path = dict((i,[items[i][0], items[i][1]]) for i in optimal_items)
#print(optimal_items)

path = []
price = 0

print(Pruning(items, number_of_items, path, price, opt, total_knapsack_volume))
# print(LP_solution(items, total_knapsack_volume, number_of_items))




