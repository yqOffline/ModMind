# -*- coding: utf-8 -*-
"""
评价.py —— 综合评价类模型模板
覆盖：AHP 层次分析 / 熵权法 / TOPSIS / 灰色关联 GRA

铁律：
  - 先正向化（成本类指标取倒数或取反），再标准化，再赋权。
  - AHP 必算一致性 CR<0.1；熵权 ln(0) 加小量；权重和为 1。
  - 指标方向：本文件统一约定「越大越好」的正向指标，负向指标请在调用前先正向化。
"""
import numpy as np


# ---------- 1. AHP 层次分析法 ----------
def ahp(judge):
    """judge: 判断矩阵（n×n，a_ij = i 相对 j 的重要性）。
    返回 (权重, λmax, CI, CR)。CR<0.1 才通过一致性。"""
    RI = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32,
          8: 1.41, 9: 1.45, 10: 1.49}
    A = np.array(judge, float)
    n = A.shape[0]
    # 几何平均法求权重
    w = A.prod(axis=1) ** (1 / n)
    w = w / w.sum()
    lam = (A @ w) / w
    lam_max = lam.mean()
    CI = (lam_max - n) / (n - 1)
    CR = CI / RI[n] if n > 2 else 0.0
    return w, lam_max, CI, CR


# ---------- 2. 熵权法 ----------
def entropy_weight(X):
    """X: m×n 正向化指标矩阵。返回权重 w（和=1）。"""
    X = np.array(X, float)
    # min-max 归一化到 [0,1]，再平移避免 ln(0)
    xmin, xmax = X.min(axis=0), X.max(axis=0)
    Xn = (X - xmin) / (xmax - xmin + 1e-12) + 1e-6
    p = Xn / Xn.sum(axis=0)
    m = X.shape[0]
    e = -(p * np.log(p)).sum(axis=0) / np.log(m)
    d = 1 - e
    w = d / d.sum()
    return w


# ---------- 3. TOPSIS ----------
def topsis(X, w):
    """X: m×n 正向化指标矩阵；w: 权重。返回贴近度 C（越大越优）。"""
    X = np.array(X, float)
    w = np.array(w, float)
    # 向量归一化
    r = X / np.sqrt((X ** 2).sum(axis=0))
    v = r * w
    v_best = v.max(axis=0)
    v_worst = v.min(axis=0)
    d_best = np.sqrt(((v - v_best) ** 2).sum(axis=1))
    d_worst = np.sqrt(((v - v_worst) ** 2).sum(axis=1))
    C = d_worst / (d_best + d_worst)
    return C


# ---------- 4. 灰色关联分析 GRA ----------
def gray_relation(X, ref=None, rho=0.5):
    """X: m×n 比较序列矩阵（每行一个对象）。
    ref: 参考序列（默认取各列最优，即越大越优）。
    返回各对象的关联度 r_i（越大越优）。"""
    X = np.array(X, float)
    if ref is None:
        ref = X.max(axis=0)  # 越大越优的参考序列
    # 初值化归一化
    Xn = X / ref
    refn = ref / ref
    delta = np.abs(refn - Xn)
    dmin, dmax = delta.min(), delta.max()
    xi = (dmin + rho * dmax) / (delta + rho * dmax)
    r = xi.mean(axis=1)
    return r


# ---------- 5. 组合赋权（主客观） ----------
def combined_weight(w_sub, w_obj, alpha=0.5):
    """w_sub: 主观权重（AHP）；w_obj: 客观权重（熵权）。
    alpha: 主观权重占比（默认 0.5，需在论文里说明取值依据）。"""
    return alpha * np.array(w_sub) + (1 - alpha) * np.array(w_obj)


# ---------- 自测 ----------
if __name__ == "__main__":
    # AHP：3 个指标两两比较
    judge = [[1, 2, 4],
             [1/2, 1, 3],
             [1/4, 1/3, 1]]
    w, lam, CI, CR = ahp(judge)
    print("AHP 权重:", w.round(3), "λmax:", round(lam, 3), "CR:", round(CR, 3))

    # 熵权 + TOPSIS：4 方案 3 指标（已正向化，越大越好）
    X = np.array([[9, 8, 9],
                  [7, 9, 6],
                  [8, 7, 7],
                  [5, 6, 6]])
    w_e = entropy_weight(X)
    C = topsis(X, w_e)
    print("熵权权重:", w_e.round(3))
    print("TOPSIS 贴近度 C:", C.round(3), "排名:", np.argsort(-C) + 1)

    # 灰色关联
    r = gray_relation(X)
    print("灰色关联度:", r.round(3))
