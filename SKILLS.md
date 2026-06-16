# 自定义技能 (Custom Skills)

> 以下是 Hermes Agent 在与用户 jackwan317 交互过程中创建的自定义技能。
> 这些技能不是 Hermes 内置的，而是根据用户特定需求和工作流演化而来。

---

## 1. 对抗性 Idea 评审系统 (`idea-adversarial-review`)

**Skill 文件**: [skills/.archive/idea-adversarial-review/SKILL.md](skills/.archive/idea-adversarial-review/SKILL.md) (已归档)

### 用途
通过 4-Agent 对抗性辩论流水线，系统性评估商业/产品 Idea 的可行性。

### 核心设计
- **Agent 1（猎手+辩手）**: 搜索信息、生成 idea、回答质疑
- **Agent 2（魔鬼代言人）**: 提出 10 个尖锐质疑（固定 10 维度）
- **Agent 3（独立裁判）**: 审查辩论记录、核实事实、定性分级
- **Agent 4（执行者）**: 拿到 SOP 后落地执行（仅强力推荐时触发）

### 评级体系
| 等级 | 含义 |
|------|------|
| ⭐ 强力推荐 | 值得立即投入执行 |
| 👍 值得探索 | 有潜力但需进一步验证 |
| 🤔 观望 | 方向有趣但条件不成熟 |
| ❌ 不推荐 | 存在致命缺陷或事实捏造 |

### 实战经验
- 已运行两轮完整实战
- 子 Agent 迭代次数有限（DeepSeek 约 3-5 轮），搜索+提案需分离
- 竞品死亡记录是最强负面信号
- 三个经典风险假设（API 涨价、大厂跟进、用户 DIY）已被实战验证失效
- B2C/B2B 不应预设偏好——聚焦付费意愿和竞争信号
- 详细日志见 skill 的 `references/` 目录
- 最新更新(2026-05-29)：新增第 13-14 条实战注意事项

---

## 2. 商业自动化工作协议 (`business-automation`)

**Skill 文件**: [skills/productivity/business-automation/SKILL.md](skills/productivity/business-automation/SKILL.md)

### 用途
AI-native 商业自动化工作协议，涵盖 SOP 重构、Skills 猎头、Idea 评审、MVP 先行判断、报告归档、目标追踪。

### 核心目标
| 时间 | 目标 |
|------|------|
| 3 个月 | 一个睡后月入过万的产品或商业模式 |
| 6 个月 | 累计赚 50 万 |

### 五大工作模式
1. **生财有术帖子 → AI Agent SOP 重构**：将人工 SOP 改造为 AI Agent 可执行的全自动链路
2. **Skills 猎头**：定期搜索 GitHub/MCP marketplace 的赚钱相关 Skill/Skill 组合（搜到先审，不擅自安装）
3. **每日复盘（飞书）**：飞书 Bitable + 文档记录复盘和感悟
4. **对抗性 Idea 评审**：多 Agent 辩论 + 独立裁判评估商业可行性
5. **MVP 先行判断**：任何 idea 先输出 ≤4h 的 MVP 验证方案

### 基础设施
- `jackwan317/hermes-reports`：报告和分析的输出仓库
- `jackwan317/hermes-knowledge-base`：记忆和技能备份（cron 每 2 天自动同步）
- 定时任务 `ebd1b672b71a`：自动将 memory + skills 推送到 knowledge-base

### 参考资源
- `references/money-tools-index.md` — 首轮 Skills 猎头报告精华索引（60+ 工具）
- `references/adversarial-review-protocol.md` — 对抗性评审完整协议
- `references/adversarial-review-collab.md` — 双 Hermes 跨设备协作指南
- `references/adversarial-review-first-run-log.md` — 首次实战日志
- `references/adversarial-review-second-run-log.md` — 第二轮实战日志

---

## 3. 飞书知识管理工作流

这不是一个独立的 Skill 文件，而是一套内化在记忆中的工作模式：

### 每日复盘流程
1. 用户口述今日亮点/不足/明日计划
2. Agent 写入飞书 Bitable (`VsL5b9zSRaO3A7sPBdWcye49nBb` → `tblM2sYDIMnGvINr`)

### 感悟记录流程
1. 用户口述一段感悟
2. Agent 清理口头禅/啰嗦句（保留原始行文结构）
3. Agent 追加到飞书文档 (`MnQRd4rNUoctsVxM4rPcLcRRn04`)，附加日期标题

### 想法管理流程
1. 用户提出一个想法
2. Agent 写入想法记录 Bitable (`WSyEbu2EhavajVsQBVRcYbKenWb` → `tblvSu7Bv3yQw7oH`)
3. Agent 自动调研并填写：
   - 投产比评估（⭐绝佳点子 / 👍一般 / ❌不靠谱 / 🤔待评估）
   - 技术可行性（✅高 / 🟡中 / 🔴低 / 🚫不可行）
   - 投入成本估算
   - 调研与思考
4. 简单任务直接执行，复杂任务等待用户确认

---

## 已归档技能

- **MVP 先行判断** (`mvp-first`)：[skills/.archive/mvp-first/SKILL.md](skills/.archive/mvp-first/SKILL.md) — 已整合到 `business-automation` 的模式五中
- **对抗性 Idea 评审** (`idea-adversarial-review`)：[skills/.archive/idea-adversarial-review/SKILL.md](skills/.archive/idea-adversarial-review/SKILL.md) — 已整合到 `business-automation` 的模式四中
