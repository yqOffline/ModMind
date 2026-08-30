# -*- coding: utf-8 -*-
"""
机理.py —— 机理分析类模型模板（A 题专属）
覆盖：常微分方程 ODE（SIR / Logistic / 牛顿冷却）/ 偏微分方程 PDE（一维热传导）

铁律：
  - ODE 每个状态量要写清 d/dt 方程 + 参数 + 初值；逐条核对流入/流出符号。
  - PDE 显式差分要满足稳定性：α*dt/dx² <= 0.5，否则数值爆炸。
"""
import numpy as np
from scipy.integrate import solve_ivp


# ---------- 1. ODE 通用求解 ----------
def solve_ode(fun, t_span, y0, args=(), t_eval=None, method='RK45'):
    """fun(t, y, *args) 返回 dy/dt；y0 为初值。返回 (t, y)。"""
    sol = solve_ivp(fun, t_span, y0, args=args, t_eval=t_eval, method=method)
    return sol.t, sol.y


def sir(t, y, beta, gamma):
    """SIR 传染病模型 dy/dt = [-βSI, βSI-γI, γI]。"""
    S, I, R = y
    return [-beta * S * I, beta * S * I - gamma * I, gamma * I]


def logistic(t, N, r, K):
    """Logistic 增长 dN/dt = rN(1-N/K)。"""
    return r * N * (1 - N / K)


def newton_cooling(t, T, T_env, k):
    """牛顿冷却 dT/dt = -k(T - T_env)。"""
    return -k * (T - T_env)


# ---------- 2. PDE：一维热传导（显式差分）----------
def heat_1d(u0, alpha, L, T_total, nx=50, nt=5000):
    """∂u/∂t = α ∂²u/∂x²，u0 为初始温度分布（长度 nx 数组）。
    返回 (x, u_final)。dt 自动取满足稳定性的最大值。"""
    dx = L / (nx - 1)
    dt = 0.45 * dx ** 2 / alpha      # 稳定性系数 < 0.5
    n_steps = int(T_total / dt)
    u = u0.copy()
    for _ in range(n_steps):
        u_new = u.copy()
        u_new[1:-1] = u[1:-1] + alpha * dt / dx**2 * (
            u[2:] - 2 * u[1:-1] + u[:-2])
        u = u_new
    x = np.linspace(0, L, nx)
    return x, u


# ---------- 自测 ----------
if __name__ == "__main__":
    # SIR
    t, y = solve_ode(sir, (0, 50), [0.99, 0.01, 0.0], args=(0.3, 0.1),
                     t_eval=np.linspace(0, 50, 200))
    print("SIR 终态 S,I,R:", y[:, -1].round(3))

    # 一维热传导
    u0 = np.zeros(50); u0[:10] = 100.0   # 左端高温
    x, u = heat_1d(u0, alpha=0.01, L=1.0, T_total=0.5)
    print("热传导终态两端温度:", round(u[0], 2), round(u[-1], 2))
