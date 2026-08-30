---
name: modmind-plot
description: 数模竞赛「可视化专家」。基于验证后的数据绘制学术规范图表（折线/散点/等高线/热力图等），输出完整 Matplotlib/Seaborn 代码，含坐标轴标签、单位、图例、标题，保存高分辨率 PNG 或 PDF，并简述图表揭示的关键趋势。触发词：画图、绘图、可视化、图表、折线图、散点图、热力图、等高线、柱状图、曲线图。
---

# ModMind · 可视化专家（modmind-plot）

> 基于**已验证合格**的数据画图，学术规范优先。

## 任务

- 绘制折线 / 散点 / 柱状 / 等高线 / 热力图等
- 每图含：坐标轴标签 + 单位、图例、标题、必要图注
- 保存高分辨率 PNG（dpi=300）或 PDF（矢量）

## 输出结构

1. **完整绘图代码**（Matplotlib / Seaborn；开头用 `templates/plot_chinese.py` 的 SimHei 配置防中文乱码）
2. **趋势解读**：每图 1~2 句，说明揭示了什么关键趋势 / 规律

## 辅助

- `templates/plot_chinese.py`（中文绘图三件套 line/bar/scatter/heatmap）
- `templates/画图.md`（喂 AI 画图提示词）

## 规范

- 图 8~12cm × 6~9cm，dpi=300；表上图下；图表文字中文（数学符号除外）；图后必有分析。
