# Hermes 多 Agent 评审流水线

## 角色
- **Agent 1 (二代-hermes)**: DeepSeek V4 Pro — 猎手+辩手
- **Agent 2/3/4 (Hermes-GPT)**: GPT-5.5 — 魔鬼代言人+裁判+执行

## 文件说明
| 文件 | 写入方 | 说明 |
|------|--------|------|
| `state.json` | 双方 | 阶段状态 |
| `proposal.md` | Agent 1 | idea 提案 |
| `questions.md` | Agent 2 | 10 个质询问题 |
| `defense.md` | Agent 1 | 答辩 |
| `judgment.md` | Agent 3 | 裁判评估 |

## 阶段流转
```
init → proposal_ready → questions_ready → defense_ready → judged
```
每个阶段完成后，更新 state.json.phase。
通过飞书群 @mention 通知对方进入下一步。
