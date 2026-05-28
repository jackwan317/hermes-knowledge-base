---
name: business-automation
description: AI-native 商业自动化工作协议 — SOP 重构、Skills 猎头、报告归档、目标追踪。当用户讨论赚钱项目、商业变现、或让 Agent 协助搭建自动化赚钱系统时使用。
---

# AI-Native 商业自动化工作协议

用 AI Agent 搭建自动化赚钱系统的完整工作流。核心理念：**AI 不应只是单步提效工具，而应思考、设计、执行整条商业链路。**

## 核心目标

| 时间 | 目标 |
|------|------|
| 3 个月 | 一个睡后月入过万的产品或商业模式 |
| 6 个月 | 累计赚 50 万 |

## 工作模式

### 模式一：生财有术帖子 → AI Agent SOP 重构

用户发送生财有术等来源的帖子（通常是别人拆解好的人工主导 SOP），Agent 的工作不是简单总结，而是：

1. **理解整条商业链路**：输入 → 处理 → 输出 → 变现
2. **重构为 AI Agent 可执行的 SOP**：将每一步替换为 AI 工具/Skill/MCP 可调用的操作
3. **识别可全自动化的环节**：哪些步骤可以完全不需要人类参与
4. **设计验证闭环**：如何判断 Agent 执行的每一步是否正确

输出格式：Markdown 文档，推送到 `jackwan317/hermes-reports` 仓库。

### 模式二：Skills 猎头（定期执行）

定期搜索 GitHub、MCP marketplace、技能仓库中与赚钱相关的 Skill 或 Skill 组合。

**搜索方向**：
- 低成本获客引流
- 商机发现 / 市场调研
- 产品选品与自动上架
- 自动化销售
- 内容变现

**铁律：搜到后先展示给用户，不擅自安装。** 用户审核通过后才安装。

**组合思维**：不只搜单个 Skill，要发现哪些 Skill 组合起来可以形成完整的赚钱流水线。

输出：推送到 `jackwan317/hermes-reports`，文件名格式 `ai-money-making-<主题>.md`。

### 模式三：每日复盘（飞书）

每天通过飞书 Bitable + 文档记录复盘和感悟。详见 `feishu-api` skill 的 `templates/daily-review.py`。

## 基础设施

### GitHub 仓库

| 仓库 | 用途 |
|------|------|
| `jackwan317/hermes-reports` | 所有报告、分析、清单的输出目的地 |
| `jackwan317/hermes-knowledge-base` | 记忆和技能的备份，cron 每 2 天自动同步 |

### 自动化同步

定时任务 `ebd1b672b71a`：每 2 天凌晨 2:00 自动将 memory + skills 推送到 `hermes-knowledge-base`。

## 用户画像速览

- 编程背景（C#、Python、单片机、网络运维）
- 生财有术信息源
- 强烈赚钱欲望（为家庭提供物质保障）
- 探索欲和求知欲是武器，不是目的
- 当前主线：用 AI 发现需求 → 验证商业模式 → 自动化变现
- 偏好：诚实面对现实，不粉饰状态

## Pitfalls

### 不要偏离赚钱主线

用户已明确纠正：不要过度关注"穷尽未知/探索欲"，当前核心是**赚钱**。探索欲是赚钱的武器和路上的风景，不是独立目标。

### KITOP 是 GitHub 的拼写错误

用户曾把 GitHub 误打为 KITOP。在复盘记录中遇到此词时理解为 GitHub。

## 参考资源

- `references/money-tools-index.md` — 首轮 Skills 猎头报告的精华索引（60+ 工具，四大组合）
