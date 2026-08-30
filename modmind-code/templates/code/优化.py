# -*- coding: utf-8 -*-
"""
优化.py —— 优化类模型模板
覆盖：线性规划 LP / 整数规划 IP / 0-1 规划 / 非线性规划 NLP / 多目标加权 / 遗传算法 GA

铁律：
  - max 问题：把目标函数系数取负，转成 min 再喂 linprog/milp/minimize。
  - NLP 单起点易陷局部最优：多起点跑对比。
  - 多目标先归一化再加权，否则量纲不同失公平。
"""
import numpy as np
from scipy.optimize import linprog, milp, minimize, LinearConstraint, Bounds


# ---------- 1. 线性规划 LP ----------
def solve_lp(c, A_ub, b_ub, A_eq=None, b_eq=None, bounds=None, maximize=False):
    """线性规划。c/A_ub/b_ub 对应 c·x，A_ub x <= b_ub。
    maximize=True 表示求最大值（内部取负）。返回 (最优解, 最优值)。"""
    c_arr = np.array(c, dtype=float)
    if maximize:
        c_arr = -c_arr
    res = linprog(c_arr, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method='highs')
    x = res.x
    z = np.array(c, dtype=float) @ x   # c·x 即最优值（max 时 c_arr 已取负转 min）
    return x, z


# ---------- 2. 整数 / 0-1 规划 ----------
def solve_ip(c, A_ub, b_ub, integrality, lb=None, ub=None, maximize=False):
    """整数/0-1 规划（scipy>=1.9 的 milp）。
    integrality: 与 x 等长的数组，1=整数，0=连续。
    0-1 规划：integrality 全 1 且 lb=0、ub=1。"""
    c_arr = np.array(c, dtype=float)
    if maximize:
        c_arr = -c_arr
    n = len(c_arr)
    lb = np.zeros(n) if lb is None else np.asarray(lb, float)
    ub = np.full(n, np.inf) if ub is None else np.asarray(ub, float)
    constraints = [LinearConstraint(np.array(A_ub, float), -np.inf,
                                    np.array(b_ub, float))]
    res = milp(c_arr, integrality=np.asarray(integrality),
               bounds=Bounds(lb, ub), constraints=constraints)
    x = res.x
    z = np.array(c, dtype=float) @ x
    return x, z


# ---------- 3. 非线性规划 NLP ----------
def solve_nlp(fun, x0, bounds=None, ineq_cons=None, eq_cons=None,
              maximize=False, starts=None):
    """非线性规划（SLSQP）。fun 为 Python 函数；x0 为初始点。
    starts：多个初点列表（可选，防局部最优，如 [[0,0],[5,5]]）。
    ineq_cons/eq_cons：{'type':'ineq'/'eq','fun':g} 列表，g(x)>=0 或 g(x)=0。"""
    sign = -1.0 if maximize else 1.0
    def obj(x):
        return sign * fun(x)
    cons = []
    for g in (ineq_cons or []):
        cons.append({'type': 'ineq', 'fun': g})
    for h in (eq_cons or []):
        cons.append({'type': 'eq', 'fun': h})
    candidates = starts if starts is not None else [x0]
    best, best_val = None, np.inf
    for x0i in candidates:
        res = minimize(obj, np.array(x0i, float), method='SLSQP',
                       bounds=bounds, constraints=cons)
        if res.success and res.fun < best_val:
            best, best_val = res.x, res.fun
    return best, sign * best_val


# ---------- 4. 多目标（加权法）----------
def solve_multi(funs, weights, x0, bounds=None, ineq_cons=None):
    """多目标线性加权。funs: 目标函数列表；weights: 权重（和=1）。
    注意：各目标先各自归一化到同量纲，再加权（示例里假设已归一化）。"""
    def combined(x):
        return sum(w * f(x) for w, f in zip(weights, funs))
    return solve_nlp(combined, x0, bounds=bounds, ineq_cons=ineq_cons)


# ---------- 5. 遗传算法 GA（组合/非线性全局优化）----------
def ga(fitness, n_var, bounds, n_pop=50, n_gen=100, p_cross=0.8, p_mut=0.1,
       minimize=True, seed=None):
    """实数编码遗传算法。fitness(x) 返回适应度；求最大传 minimize=False。"""
    rng = np.random.default_rng(seed)
    lo = np.array([b[0] for b in bounds], float)
    hi = np.array([b[1] for b in bounds], float)
    pop = rng.uniform(lo, hi, size=(n_pop, n_var))
    def score(x):
        return fitness(x) if not minimize else -fitness(x)  # 内部统一求最大
    for _ in range(n_gen):
        fits = np.array([score(ind) for ind in pop])
        fits = fits - fits.min() + 1e-9
        prob = fits / fits.sum()
        new_pop = []
        for _ in range(n_pop // 2):
            p1 = pop[rng.choice(n_pop, p=prob)]
            p2 = pop[rng.choice(n_pop, p=prob)]
            c1, c2 = p1.copy(), p2.copy()
            if rng.random() < p_cross:  # 算术交叉
                a = rng.random()
                c1, c2 = a*p1 + (1-a)*p2, (1-a)*p1 + a*p2
            for c in (c1, c2):  # 变异
                if rng.random() < p_mut:
                    j = rng.integers(n_var)
                    c[j] = rng.uniform(lo[j], hi[j])
            new_pop += [c1, c2]
        pop = np.array(new_pop)
    fits = np.array([score(ind) for ind in pop])
    best = pop[np.argmax(fits)]
    return best, fitness(best)


# ---------- 自测 ----------
if __name__ == "__main__":
    # LP：max Z = 3x1 + 5x2，s.t. 2x1+x2<=100, x1+2x2<=120, x>=0
    x, z = solve_lp([3, 5], [[2, 1], [1, 2]], [100, 120],
                    bounds=[(0, None), (0, None)], maximize=True)
    print("LP max:", x, z)  # 期望 ≈ x1=26.67, x2=46.67, Z=313.33

    # 0-1 规划示例：从 3 个物品选，价值 [4,3,5]，重量 [2,1,3]，容量 4
    x, z = solve_ip([4, 3, 5], [[2, 1, 3]], [4],
                    integrality=[1, 1, 1], lb=[0, 0, 0], ub=[1, 1, 1],
                    maximize=True)
    print("0-1 max:", x, z)  # 期望选 [0,1,1]，总价值 8

    # NLP：min (x1-2)^2 + (x2-3)^2, x1,x2 in [0,10]
    x, v = solve_nlp(lambda x: (x[0]-2)**2 + (x[1]-3)**2,
                     [0, 0], bounds=[(0, 10), (0, 10)])
    print("NLP min:", x, v)  # 期望 (2,3), 0

    # GA：min (x-2)^2, x in [-10, 10]
    x, v = ga(lambda x: (x[0]-2)**2, 1, [(-10, 10)], n_gen=50, seed=1)
    print("GA min:", x, v)  # 期望 ≈2
