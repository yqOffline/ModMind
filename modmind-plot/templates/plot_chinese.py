# -*- coding: utf-8 -*-
"""
plot_chinese.py —— 中文绘图通用模板（每个画图脚本开头复制这几行，或 import 本文件）

解决：matplotlib 默认字体显示中文变成方框 □□、负号显示异常的问题。
用法：
    from plot_chinese import setup_chinese
    setup_chinese()
    # 之后正常 plt.plot / plt.bar / ...
"""
import matplotlib.pyplot as plt


def setup_chinese():
    """全局配置中文显示，调用一次即可。"""
    plt.rcParams['font.sans-serif'] = ['SimHei']   # 黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False     # 正常显示负号
    plt.rcParams['figure.dpi'] = 300               # 论文图 300dpi


def style_axis(ax, xlabel="", ylabel="", title=""):
    """统一坐标轴：加单位、标题。论文图表文字用中文（数学符号除外）。"""
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, alpha=0.3, linestyle='--')
    return ax


# ---------- 常用图模板 ----------

def line_plot(x, y, xlabel="", ylabel="", title="", label=""):
    """折线图：趋势、随时间变化。"""
    setup_chinese()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, marker='o', label=label or ylabel)
    style_axis(ax, xlabel, ylabel, title)
    if label:
        ax.legend()
    fig.tight_layout()
    return fig, ax


def bar_plot(labels, values, xlabel="", ylabel="", title="", color='steelblue'):
    """柱状图：对比、排名。"""
    setup_chinese()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, values, color=color, edgecolor='black', alpha=0.8)
    style_axis(ax, xlabel, ylabel, title)
    for i, v in enumerate(values):
        ax.text(i, v, f'{v:.3g}', ha='center', va='bottom', fontsize=9)
    fig.tight_layout()
    return fig, ax


def scatter_plot(x, y, xlabel="", ylabel="", title="", c=None):
    """散点图：分布、相关性、聚类结果。"""
    setup_chinese()
    fig, ax = plt.subplots(figsize=(8, 5))
    sc = ax.scatter(x, y, c=c, cmap='viridis', s=40, alpha=0.8)
    style_axis(ax, xlabel, ylabel, title)
    if c is not None:
        fig.colorbar(sc, ax=ax)
    fig.tight_layout()
    return fig, ax


def heatmap(mat, xlabel="", ylabel="", title=""):
    """热力图：相关性矩阵、权重分布。"""
    setup_chinese()
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(mat, cmap='Blues', aspect='auto')
    style_axis(ax, xlabel, ylabel, title)
    fig.colorbar(im, ax=ax)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f'{mat[i, j]:.2f}', ha='center', va='center', fontsize=8)
    fig.tight_layout()
    return fig, ax


if __name__ == "__main__":
    setup_chinese()
    import numpy as np
    # 自测：画一张带中文的图，确认中文/负号正常
    x = np.linspace(-3, 3, 50)
    line_plot(x, -x**2, xlabel="变量 x", ylabel="目标值 y", title="示例：中文与负号测试")
    plt.show()
