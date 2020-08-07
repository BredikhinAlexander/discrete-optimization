from itertools import combinations
from math import sqrt



def TSP(points, AA):
    n = len(points)

    def euclidean_distance(point1, point2):
        return sqrt((points[point1][0] - points[point2][0]) ** 2 + (points[point1][1] - points[point2][1]) ** 2)

    # находим кратчайшее ребро
    edges = list(combinations(AA, 2))
    min_edge_i, min_edge_j = min(edges, key=lambda edge: euclidean_distance(edge[0], edge[1]))
    order = [min_edge_i, min_edge_j]

    def addition_to_perimeter(vertex):
        return euclidean_distance(vertex, min_edge_i) + euclidean_distance(vertex, min_edge_j)

    vertexes = set(AA) - set(order)
    min_perimeter_i = min(vertexes, key=addition_to_perimeter)
    order.append(min_perimeter_i)

    # print(order)

    # в цикле среди всех пар (<вершина не из цикла>, <ребро для удаления>) находим такую, которая минимально увеличит вес цикла
    def addition_of(pair):
        i = pair[0]
        #print(i)
        order_i = pair[1]
        u = order[order_i]
        v = order[(order_i + 1) % len(order)]
        return euclidean_distance(i, u) + euclidean_distance(i, v) - euclidean_distance(u, v)

    while len(order) < n:
        pairs = [(i, order_i) for i in AA if i not in order for order_i in range(len(order))]
        #print(pairs)
        i, order_i = min(pairs, key=addition_of)
        order.insert(order_i + 1, i)
    return order

n = int(input())


points = dict()
AA = []
for i in range(n):
    p, x, y = map(float, input().split())
    p = int(p)
    AA.append(p)
    points[p] = [x,y]

order = TSP(points, AA)
order.append(order[0])

for el in order:
    print(el, end = ' ')