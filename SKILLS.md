# 自定义技能 (Custom Skills)

> 以下是 Hermes Agent 在与用户 jackwan317 交互过程中创建的自定义技能。
> 这些技能不是 Hermes 内置的，而是根据用户特定需求和工作流演化而来。

---

## 1. 对抗性 Idea 评审系统 (`idea-adversarial-review`)

**Skill 文件**: [skills/autonomous-ai-agents/idea-adversarial-review/SKILL.md](skills/autonomous-ai-agents/idea-adversarial-review/SKILL.md)

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
- 详细日志见 skill 的 `references/` 目录

---

## 2. 飞书知识管理工作流

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
