from itertools import combinations
from math import sqrt



def TSP(points, cons):
    n = len(points)

    def find_distance(point1, point2):
        return sqrt((points[point1][0] - points[point2][0]) ** 2 + (points[point1][1] - points[point2][1]) ** 2)

    edges = list(combinations(cons, 2))
    min_edge_i, min_edge_j = min(edges, key=lambda edge: find_distance(edge[0], edge[1]))
    cycle = [min_edge_i, min_edge_j]

    def find_base(vertex):
        return find_distance(vertex, min_edge_i) + find_distance(vertex, min_edge_j)

    vertices = set(cons) - set(cycle)
    min_perimeter_i = min(vertices, key=find_base)
    cycle.append(min_perimeter_i)

    def add_vertex(pair):
        i = pair[0]
        order_i = pair[1]
        u = cycle[order_i]
        v = cycle[(order_i + 1) % len(cycle)]
        return find_distance(i, u) + find_distance(i, v) - find_distance(u, v)

    while len(cycle) < n:
        pairs = [(i, order_i) for i in cons if i not in cycle for order_i in range(len(cycle))]
        i, order_i = min(pairs, key=add_vertex)
        cycle.insert(order_i + 1, i)
    return cycle

n = int(input())


points = dict()
cons = []
for i in range(n):
    p, x, y = map(float, input().split())
    p = int(p)
    cons.append(p)
    points[p] = [x,y]

cycle = TSP(points, cons)
cycle.append(cycle[0])

for el in cycle:
    print(el, end = ' ')