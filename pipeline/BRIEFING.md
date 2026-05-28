# 协作情况说明 — 致二代-hermes

## 项目概述

大哥搭建了一个**双 Hermes Agent 对抗性 Idea 评审系统**。两个 Agent 各有分工，通过飞书群聊 + GitHub 仓库协作，完成商业 Idea 的搜索提案、质询答辩、裁判评估的全流程。

---

## 分工

| Agent | 模型 | 角色 | 职责 |
|-------|------|------|------|
| **你（二代-hermes）** | DeepSeek V4 Pro | Agent 1 — 猎手+辩手 | 1) 搜索信息生成 Idea 提案 2) 回答我的质询（答辩） |
| **我（Hermes-GPT）** | GPT-5.5 | Agent 2/3/4 — 魔鬼代言人+裁判+执行 | 1) 对你的提案提出 10 个尖锐质询 2) 审查答辩，给出评级 3) 强力推荐时执行落地 |

---

## 沟通方式

**飞书群聊**：`oc_29e92db56abde591c072120e72958de5`（群名：二代-hermes）

- 你完成一个阶段 → 在群里 @我，告知完成
- 我完成 → 在群里 @你，告知下一步
- 紧急/简要沟通直接在群里完成

---

## 协作仓库

**GitHub**：`https://github.com/jackwan317/hermes-knowledge-base/tree/main/pipeline`

### 文件结构

| 文件 | 写入方 | 说明 |
|------|--------|------|
| `pipeline/state.json` | 双方 | 阶段状态（phase 字段） |
| `pipeline/proposal.md` | 你（Agent 1） | Idea 提案全文 |
| `pipeline/questions.md` | 我（Agent 2） | 10 个质询问题 |
| `pipeline/defense.md` | 你（Agent 1） | 你对质询的答辩 |
| `pipeline/judgment.md` | 我（Agent 3） | 裁判评估与评级 |
| `pipeline/BRIEFING.md` | — | 本文件 |

### 阶段流转（state.json 的 phase 字段）

```
proposal_ready  → 你写完了提案，通知我质询
questions_ready → 我写完了质询，通知你答辩
defense_ready   → 你写完了答辩，通知我裁判
judged          → 我评完了，流程结束
```

---

## 你的技能

你已经具备 `idea-adversarial-review` 技能。你负责其中 **Agent 1（猎手+辩手）** 的部分。

### Phase 1：生成提案

大哥会给你一个 idea 方向。你需要：
1. 搜索信息（市场规模、竞品、技术可行性、用户痛点等）
2. 生成结构化 Idea 提案（11 部分，详见 skill）
3. 将提案写入 `pipeline/proposal.md`
4. 将 `pipeline/state.json` 的 `phase` 改为 `proposal_ready`
5. 在飞书群里 @我

### Phase 3：答辩（在我完成质询后）

1. 读取 `pipeline/questions.md` 中我的 10 个质询问题
2. 按照 skill 中「辩手」的答辩原则逐一回答
3. 将答辩写入 `pipeline/defense.md`
4. 将 `pipeline/state.json` 的 `phase` 改为 `defense_ready`
5. 在飞书群里 @我

---

## 第一个任务

大哥的第一个评审方向是：**「AI Agent 自动赚钱系统」— 让 Agent 自己去发现、验证、执行赚钱方案**。

我已经让一个 cron job（DeepSeek V4 Pro）跑了第一版提案，写在了 `pipeline/proposal.md` 中。请你：

1. 阅读 `pipeline/proposal.md` 和 `pipeline/state.json`
2. **暂时跳过质询阶段**（我已经在做这步）
3. 准备好进入答辩阶段

后续任务由大哥在群里分发。

---

## 关键规则

- 所有文件写入后立即 `git push`
- 读取文件前先 `git pull`
- 数据必须标注来源，不编造
- 提案/答辩自包含，不依赖上下文
- 有不确定的地方标「待验证」+ 验证方法
