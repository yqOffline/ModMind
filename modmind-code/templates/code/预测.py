# -*- coding: utf-8 -*-
"""
预测.py —— 预测类模型模板
覆盖：时间序列（ADF 平稳性检验 + ARIMA）/ 灰色预测 GM(1,1)

铁律：
  - 时间序列先验平稳性（ADF p<0.05），不平稳做差分。
  - GM(1,1) 适用于小样本、单调趋势；必须检验精度（C、P 值）。
"""
import numpy as np
import pandas as pd


# ---------- 1. 时间序列：平稳性 + ARIMA ----------
def adf_test(series):
    """ADF 平稳性检验。p<0.05 表示平稳。"""
    from statsmodels.tsa.stattools import adfuller
    r = adfuller(series, autolag='AIC')
    print("ADF 统计量:", round(r[0], 4), " p 值:", round(r[1], 4))
    print("平稳" if r[1] < 0.05 else "不平稳，需差分")
    return r[1]


def arima_forecast(series, order=(1, 1, 1), steps=5):
    """ARIMA 拟合 + 预测。order=(p,d,q)。返回 (拟合值, 预测值, 模型)。"""
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(series, order=order).fit()
    fitted = model.fittedvalues
    forecast = model.forecast(steps=steps)
    print(model.summary())
    return fitted, forecast, model


# ---------- 2. 灰色预测 GM(1,1) ----------
def gm11(x0, predict_n=3):
    """x0: 原始序列（list/array，非负、单调更佳）。返回 (拟合值, 预测值, C, P, a, b)。"""
    x0 = np.array(x0, float)
    x1 = x0.cumsum()                      # 一次累加 AGO
    z1 = 0.5 * (x1[1:] + x1[:-1])         # 紧邻均值（背景值）
    B = np.column_stack([-z1, np.ones_like(z1)])
    Y = x0[1:]
    a, b = np.linalg.lstsq(B, Y, rcond=None)[0]   # 最小二乘求 a,b
    # 时间响应式
    def x1_hat(k):
        return (x0[0] - b / a) * np.exp(-a * k) + b / a
    fit_x1 = x1_hat(np.arange(len(x0)))
    fit_x0 = np.concatenate([[x0[0]], np.diff(fit_x1)])   # 还原：首值=x0[0]
    pred = x1_hat(np.arange(len(x0), len(x0) + predict_n))
    pred_x0 = np.diff(pred, prepend=fit_x1[-1])           # 预测还原：首值=末拟合差值
    # 精度检验：后验差比 C 与 小误差概率 P
    e = x0 - fit_x0
    S1 = x0.std(ddof=1)
    S2 = e.std(ddof=1)
    C = S2 / S1 if S1 > 0 else np.inf
    P = (np.abs(e - e.mean()) < 0.6745 * S1).mean() if S1 > 0 else 0
    print(f"GM(1,1) a={a:.4f} b={b:.4f}")
    print(f"C={C:.4f}（<0.35 好，<0.5 合格） P={P:.4f}（>0.95 好，>0.8 合格）")
    return fit_x0, pred_x0, C, P, a, b


# ---------- 自测 ----------
if __name__ == "__main__":
    # GM(1,1) 自测：单调增长序列
    x0 = [3.2, 3.6, 4.1, 4.6, 5.2, 5.9]
    fit, pred, C, P, a, b = gm11(x0, predict_n=2)
    print("拟合值:", fit.round(3))
    print("预测值:", pred.round(3))
