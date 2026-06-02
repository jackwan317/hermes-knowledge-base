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

### 模式四：对抗性 Idea 评审

通过多 Agent 对抗性辩论 + 独立裁判机制，系统评估一个商业/产品 Idea 的可行性。4 个 Agent 角色：猎手+辩手、魔鬼代言人、独立裁判、执行者。支持三种触发模式（纯自主搜索 / 用户播种 / 纯用户输入），输出飞书文档含完整辩论记录和定性评级。

**两种部署模式**：
- **双 Hermes 协作**（跨设备）：通过 GitHub + 飞书群，详见 `references/adversarial-review-collab.md`
- **单 Hermes 编排**（delegate_task）：导演调度 4 个子 Agent，详见 `references/adversarial-review-protocol.md`（含完整 Agent Prompt、8 阶段工作流、14 条 Pitfalls、编排参考代码）

首次和第二次实战执行日志见 `references/adversarial-review-first-run-log.md` 和 `references/adversarial-review-second-run-log.md`。

### 模式五：MVP 先行判断

当用户描述任何 idea 或新项目时，先输出 MVP 验证方案，再讨论可行性分析。

**核心原则**：
1. MVP 必须 ≤ 4 小时完成。超过 4 小时的「第一步」不叫 MVP，叫打外围
2. MVP 的终点必须是「验证性结果」（如「AI 能识别 SOP」），不是「产出物」（如「爬了 2000 篇文章」）
3. 如果当前行为偏离 MVP，直接指出——不要附和不批判

**输出格式**：最小验证步骤、预计耗时、验证通过/不通过标准、当前行为判定

## Idea 筛选标准

当 Agent 主动搜索/筛选赚钱 Idea 时，遵守以下标准（经用户纠正后的最终版本）：

### 硬门槛（缺一不可）

1. **搜索热度**：Google Trends 在涨 / 社区有真实讨论热度
2. **技术成熟度**：依赖的技术和 API 已可用，项目可实际开发

两条都不满足 = 坏项目，直接毙掉。

### 一票否决（真正致命的）

- 重度依赖单一封闭平台 API（Reddit/X 那种随时可能关的）
- 需要自建双边市场（冷启动地狱）

### 不禁的（被纠正过的错误偏见）

- ❌ ~~"API 涨价 10 倍怎么办"~~ — API 价格趋势是越来越便宜
- ❌ ~~"大厂 6 个月跟进怎么办"~~ — 6 个月是有效窗口期，做起来了更可能被收购
- ❌ ~~"用户凭什么不自己做"~~ — 花钱省时间是成熟消费行为，不是伪命题
- ❌ ~~"拒掉所有 B2C"~~ — B2C 可以更快验证市场，不要一刀切

### 优选信号（加分项）

- B2B 或 B2C 均可，重要是有真实付费意愿
- 2-4 周可出 MVP
- 能用 Hermes Agent 编排能力做出差异化
- 有竞品在赚钱（证明需求真实）
- 单人可执行

## Pitfalls

### 不要偏离赚钱主线

用户已明确纠正：不要过度关注"穷尽未知/探索欲"，当前核心是**赚钱**。探索欲是赚钱的武器和路上的风景，不是独立目标。

### KITOP 是 GitHub 的拼写错误

用户曾把 GitHub 误打为 KITOP。在复盘记录中遇到此词时理解为 GitHub。

## 参考资源

- `references/money-tools-index.md` — 首轮 Skills 猎头报告的精华索引（60+ 工具，四大组合）
- `references/adversarial-review-collab.md` — 双 Hermes 跨设备协作模式的操作指南
- `references/adversarial-review-protocol.md` — 对抗性评审完整协议（Agent Prompt、Workflow、Pitfalls、编排代码）
- `references/adversarial-review-first-run-log.md` — 首次实战执行日志（SaaS Clone AI，含故障和 Workarounds）
- `references/adversarial-review-second-run-log.md` — 第二轮实战日志（Reddit Pulse，含 Prompt 升级前后对比）
