# Memory & User Profile Backup
> 迁移备份 | 日期: 2026-05-28 | 迁移前状态

---

## MEMORY（Agent 个人笔记）

### Feishu / 飞书

- **每日复盘 Bitable**：app_token=VsL5b9zSRaO3A7sPBdWcye49nBb，table_id=tblM2sYDIMnGvINr，URL=https://my.feishu.cn/base/VsL5b9zSRaO3A7sPBdWcye49nBb
- 字段（记录操作用字段名，非 field_id）：
  - 今日亮点 (Text)
  - 日期 (DateTime) — Unix ms
  - 今日不足 (Text)
  - 明日计划 (Text)
- 添加记录用 POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records
- 模板脚本: feishu-api skill 的 templates/daily-review.py

- **感悟记录飞书文档**：document_id=MnQRd4rNUoctsVxM4rPcLcRRn04，标题=感悟记录，URL=https://my.feishu.cn/docx/MnQRd4rNUoctsVxM4rPcLcRRn04，位于默认文件夹
- 追加新感悟时：GET 获取token → POST /open-apis/docx/v1/documents/{doc_id}/blocks/{page_id}/children?document_revision_id=N
- 格式：先加日期标题（block_type=2，加粗日期时间），再加内容段落（block_type=2）
- 仅做口头禅/啰嗦句的清理，保留原始行文结构

### 用户行为理解

- 用户 2026-05-27 复盘中的"KITOP"是 GitHub 的拼写错误，不是独立工具名。"熟悉 KITOP 操作"应理解为"熟悉 GitHub 操作"

### 用户目标与工作方式

- **3 个月目标**：睡后月入过万的产品或商业模式
- **6 个月目标**：累计赚 50 万
- **工作方式**：
  1. 用户发生财有术帖子 → 我重构为 AI Agent 可执行的 SOP（整条链路，非单步提效）
  2. 定期搜索 skills 仓库找赚钱相关 skill/skill 组合，搜到先给用户审，不擅自安装
  3. 搜索方向：低成本获客、商机发现、产品选品上线售卖等

### GitHub

- **知识库仓库**：jackwan317/hermes-knowledge-base — 存储 memory、user profile、skills。本地路径 ~/hermes-knowledge-base/
- **报告仓库**：jackwan317/hermes-reports — 存储 Agent 输出的研究报告和文档。本地路径 ~/hermes-reports/
- GitHub 账号：jackwan317，已通过 GITHUB_TOKEN 认证

---

## USER PROFILE（用户信息）

### 飞书文档体系

默认飞书文档创建位置：文件夹「WYvrfJEuflZtMQdgUcjcc2HlnLX」，内含：
- 📊 每日复盘 Bitable：VsL5b9zSRaO3A7sPBdWcye49nBb
- 📄 感悟记录 Doc：MnQRd4rNUoctsVxM4rPcLcRRn04
- 💡 想法记录 Bitable：WSyEbu2EhavajVsQBVRcYbKenWb，table_id=tblvSu7Bv3yQw7oH
  字段：编号/记录时间/想法/期待结果/执行情况/调研与思考/投产比评估/投入成本/技术可行性
  投产比选项：⭐绝佳点子/👍一般/❌不靠谱/🤔待评估
  可行性选项：✅高/🟡中/🔴低/🚫不可行

### 当前主线任务

1. 发现可上站机会 → 做 SaaS 站或工具
2. 发现有用的 skill → 学习沉淀
3. 发现不错的商业模式 → 自动化

### 协作信息（新增 2026-05-28）

- **飞书群「赛博团队」**：chat_id=oc_29e92db56abde591c072120e72958de5
- 本 Agent 名称：**二代-hermes**（DeepSeek V4 Pro）
- 战友 Agent 名称：**Mac-hermes**（GPT-5.5）
- 协作项目：AgentMint 对抗性 Idea 评审系统
- 协作模式：GitHub pipeline（proposal.md → questions.md → defense.md → judgment.md）
- 阶段流转：proposal_ready → questions_ready → defense_ready → judged
- GitHub 协作路径：https://github.com/jackwan317/hermes-knowledge-base/tree/main/pipeline
