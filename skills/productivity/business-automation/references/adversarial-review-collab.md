# 对抗性评审：双 Hermes 协作模式

## 角色分工

| Agent | 模型 | 角色 | 职责 |
|-------|------|------|------|
| 二代-hermes（我们） | DeepSeek V4 Pro | Agent 1 — 猎手+辩手 | 搜索信息生成 Idea 提案；回答质询 |
| Mac-hermes | GPT-5.5 | Agent 2/3/4 — 质询+裁判+执行 | 提出 10 个尖锐质询；审查答辩评级；强力推荐时执行 |

## 沟通渠道

- **飞书群「赛博团队」**：`oc_29e92db56abde591c072120e72958de5`
  - 群公告为空（2026-05-28）
  - 完成一个阶段 → @对方通知
  - 工作沟通只在这个群
- **用户主通道**：本会话的 DM（`oc_572b918e82afdb05a360b866ee607e57`）

## 协作仓库

**GitHub**：`https://github.com/jackwan317/hermes-knowledge-base/tree/main/pipeline`

### 文件结构

| 文件 | 写入方 | 说明 |
|------|--------|------|
| `pipeline/state.json` | 双方 | 阶段状态（phase 字段） |
| `pipeline/proposal.md` | 我们（Agent 1） | Idea 提案全文 |
| `pipeline/questions.md` | Mac-hermes | 10 个质询问题 |
| `pipeline/defense.md` | 我们（Agent 1） | 对质询的答辩 |
| `pipeline/judgment.md` | Mac-hermes | 裁判评估与评级 |

### 阶段流转

```
proposal_ready  → 我们写完了提案，通知 Mac 质询
questions_ready → Mac 写完了质询，通知我们答辩
defense_ready   → 我们写完了答辩，通知 Mac 裁判
judged          → Mac 评完了，流程结束
```

### 协作规则

- 所有文件写入后立即 `git push`
- 读取文件前先 `git pull`
- 数据必须标注来源，不编造
- 不确定处标「待验证」+ 验证方法
- 提案/答辩自包含，不依赖上下文

## 详细操作步骤

详见 `idea-adversarial-review` skill。
