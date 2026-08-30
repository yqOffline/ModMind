# -*- coding: utf-8 -*-
"""
图论.py —— 图与网络模型模板
覆盖：最短路（Dijkstra）/ 最大流 / TSP 旅行商（最近邻 + 2-opt）

铁律：
  - 建图前分清有向/无向、边权含义。
  - TSP 是 NP 难，用启发式（最近邻/2-opt/GA），别硬求精确解。
"""
import numpy as np
import networkx as nx


# ---------- 1. 最短路（Dijkstra）----------
def shortest_path(edges, source, target, directed=False):
    """edges: [(u, v, weight), ...]；返回 (路径, 总权)。"""
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_weighted_edges_from(edges)
    path = nx.dijkstra_path(G, source, target, weight='weight')
    length = nx.dijkstra_path_length(G, source, target, weight='weight')
    return path, length


# ---------- 2. 最大流 ----------
def max_flow(edges, source, sink):
    """edges: [(u, v, capacity), ...]（有向）。返回 (最大流量, 流量字典)。"""
    G = nx.DiGraph()
    for u, v, cap in edges:
        G.add_edge(u, v, capacity=cap)
    val, flow = nx.maximum_flow(G, source, sink)
    return val, flow


# ---------- 3. TSP（最近邻 + 2-opt）----------
def tsp(dist, start=0):
    """dist: n×n 距离矩阵。返回 (路径, 总距离)。"""
    n = len(dist)
    unvisited = set(range(n)); unvisited.remove(start)
    route = [start]
    cur = start
    while unvisited:                     # 最近邻构造初始解
        nxt = min(unvisited, key=lambda j: dist[cur][j])
        route.append(nxt); unvisited.remove(nxt); cur = nxt
    route.append(start)
    def total(r):
        return sum(dist[r[i]][r[i+1]] for i in range(len(r)-1))
    improved = True                      # 2-opt 优化
    while improved:
        improved = False
        for i in range(1, n-1):
            for j in range(i+1, n):
                new = route[:i] + route[i:j+1][::-1] + route[j+1:]
                if total(new) < total(route):
                    route = new; improved = True
    return route, total(route)


# ---------- 自测 ----------
if __name__ == "__main__":
    edges = [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)]
    print("最短路 0->4:", shortest_path(edges, 0, 4))

    # 最大流
    fe = [(0, 1, 16), (0, 2, 13), (1, 2, 10), (1, 3, 12), (2, 1, 4),
          (2, 4, 14), (3, 2, 9), (3, 5, 20), (4, 3, 7), (4, 5, 4)]
    print("最大流:", max_flow(fe, 0, 5)[0])

    # TSP：随机 6 个点
    rng = np.random.default_rng(0)
    pts = rng.uniform(0, 10, (6, 2))
    d = np.linalg.norm(pts[:, None] - pts[None, :], axis=2)
    print("TSP 路径与距离:", tsp(d))
