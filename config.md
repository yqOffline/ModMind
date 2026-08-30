# ModMind 全局配置（改这一处，别改各 SKILL.md）

> 换电脑 / 换队友 / 换投稿格式，**只改本文件**。各 skill 由 AI 读本文件取环境信息。

## 1. 投稿格式

- **格式：Word**（`modmind-write` 产出 Word 结构；公式用 Word 公式编辑器或 LaTeX 公式图）
- 若改用 LaTeX：把上一行改成 LaTeX，write 阶段改为产出 `.tex` 全文。
- 官方电子版要求：Word 或 PDF 之一（**建议 PDF**），≤20MB、不压缩、**第一页必须是摘要页**。

## 2. 队伍信息

- 队号：`（赛前填，只填队号，禁填学校/姓名/学号）`

## 3. Vault 兜底路径（子技能参考不够用时读原笔记）

- Vault 根：`C:\Users\25154\Documents\Obsidian Vault`（换电脑只改这一行）
- 模型库：`<根>\CSL\10-数学建模\02-模型库\`
- 论文写作：`<根>\CSL\10-数学建模\03-论文写作\数模论文写作指导.md`
- 真题与精读：`<根>\CSL\10-数学建模\04-真题与实战\`
- 真题数据：`<根>\CSL\10-数学建模\05-资源\真题\`

## 4. Python 环境速记

- 装包：`py -m pip install xxx`（`py` = Python 3.14 有 pip；裸 `python` 是 msys64 没 pip）
- 绘图中文：脚本开头加 `SimHei` + `axes.unicode_minus=False`
