# ModMind · 数学建模竞赛 AI 辅助技能族

> 7 个 Claude Code Skill，覆盖数模竞赛「审题 → 建模 → 代码 → 质检 → 画图 → 论文」全流程。
> 纯文本文件夹，**复制即迁移**，无需安装。

## 1. 技能清单

| 技能 | 文件夹 | 角色 | 触发词（说这些会命中） |
|------|--------|------|------------------------|
| 主控 | `modmind` | 总指挥，按 6 步调度、每步确认 | 数模 / 国赛 / CUMCM / ModMind / 开始做题 |
| 审题 | `modmind-read` | 剥噪声、提变量、做假设（禁推导） | 审题 / 读题 / 提取变量 / 做假设 / 符号表 |
| 建模 | `modmind-model` | 选方法、建方程与约束（禁代码） | 建模 / 选模型 / 目标函数 / 约束 / 微分方程 |
| 代码 | `modmind-code` | 模型转代码（不运行） | 写代码 / 求解代码 / 编程 / Python 实现 |
| 质检 | `modmind-test` | 烟雾测试 / 手算对照 / 收敛检查 | 验证 / 质检 / 测试 / 手算对照 / 报错排查 |
| 画图 | `modmind-plot` | 学术规范图 + 趋势解读 | 画图 / 绘图 / 折线图 / 热力图 / 等高线 |
| 论文 | `modmind-write` | 摘要 + LaTeX 模型章节 + 图表分析 | 论文 / 摘要 / 写作 / LaTeX / 优缺点 |

## 2. 迁移 / 复制到比赛环境（VS Code + Claude Code）

Claude Code 的 Skill 是纯文本文件夹，复制即可。两种放置位置：

- **用户级（推荐）**：`%USERPROFILE%\.claude\skills\`（如 `C:\Users\25154\.claude\skills\`）
  → **任何** VS Code 打开的文件夹都能用，适合比赛时换项目目录。
- **项目级**：`<竞赛项目文件夹>\.claude\skills\` → 仅该文件夹可用。

### 迁移步骤（PowerShell）

```powershell
# 源：当前 vault 里的 skills
$src = "C:\Users\25154\Documents\Obsidian Vault\.claude\skills"

# 1) 建用户级目录
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null

# 2) 复制 7 个技能文件夹
Copy-Item -Recurse `
  "$src\modmind", "$src\modmind-read", "$src\modmind-model", `
  "$src\modmind-code", "$src\modmind-test", "$src\modmind-plot", `
  "$src\modmind-write" "$env:USERPROFILE\.claude\skills\"
```

3. **重启 VS Code**（或重启 Claude Code 会话）让 skill 被发现。
4. **验证**：对 Claude 说「用 ModMind，帮我判这道题的题型」→ 应命中 `modmind-read`。

### 注意事项

- 复制时**文件夹名不能改**（`modmind-read` 改名后与 `SKILL.md` 里的 `name` 字段对不上）。
- 每个技能内 `SKILL.md` 顶部 4 行是 YAML（`name` + `description`），description 是触发词，**别删别改错**。
- `modmind/SKILL.md`「兜底」一节指向旧 vault 的绝对路径，换机器后这几行失效但**无害**——7 个技能本身自包含（references + 代码模板都跟着走）。
- 代码模板依赖 Python 环境，比赛机器上先装好：
  `py -m pip install numpy scipy pandas scikit-learn statsmodels matplotlib networkx`

## 3. 使用教程

### 3.1 完整流程（主控驱动）

对 Claude 说「**开始做这道数模题**」→ 主控 `modmind` 按 6 步顺序推进，**每步产出后暂停向你确认**再走下一步：

```
① 读懂题目    → modmind-read    产出：问题重述 + 符号表 + 假设
② 建立数学模型 → modmind-model   产出：选型理由 + 目标函数/方程 + 约束
③ 编写求解代码 → modmind-code    产出：可执行代码（不运行）
④ 验证代码正确性 → modmind-test  产出：质检合格 / 错误定位
⑤ 结果画图    → modmind-plot    产出：学术规范图 + 趋势解读
⑥ 论文排版与摘要 → modmind-write 产出：摘要 + LaTeX 模型章节 + 图表分析
```

### 3.2 单点模式（跳过其余步骤）

只做某一步时，直接说触发词即可命中对应子技能，主控会自动跳转：

| 想做什么 | 说 | 命中 |
|---------|-----|------|
| 只审题 | 「帮我审这道题」 | modmind-read |
| 只建模 | 「这题用什么模型」 | modmind-model |
| 只写代码 | 「把这模型写成代码」 | modmind-code |
| 只验证 | 「帮我质检这段代码」 | modmind-test |
| 只画图 | 「把结果画成图」 | modmind-plot |
| 只写论文 | 「帮我写摘要」 | modmind-write |

### 3.3 分工铁律（红线）

- 读题、建模、写论文 = **用户主导**（评分核心，AI 辅助 ≠ 代写）
- 写代码、画图、质检 = AI 执行
- 论文禁出现学校/姓名/学号/队号以外个人信息；查重 ≤ 20%

## 4. 自检清单

- 7 个文件夹都在 `.claude\skills\` 下，每个含 `SKILL.md`
- `SKILL.md` 前 4 行 YAML 的 `name` 与文件夹名一致
- 重启后说触发词能命中（见 2.4）
- 代码模板能跑：`cd modmind-code\templates\code && py 优化.py`（应输出 LP max 313.33 / 0-1 8.0 / NLP 0.0）
