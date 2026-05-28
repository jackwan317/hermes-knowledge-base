# Memory（Hermes 持久记忆）

> 以下是 Hermes Agent 在与用户 jackwan317 交互过程中积累的持久记忆。
> 新 Agent 应将这些信息加载到自己的 memory 中，以便无缝接续工作。
> 最后同步时间：2026-05-29

---

## 飞书文档体系

### 默认文件夹
- **Token**: `WYvrfJEuflZtMQdgUcjcc2HlnLX`
- **规则**: 除非用户特别指定，所有新建飞书文档都放在此文件夹下。

### 每日复盘 Bitable
- **URL**: https://my.feishu.cn/base/VsL5b9zSRaO3A7sPBdWcye49nBb
- **app_token**: `VsL5b9zSRaO3A7sPBdWcye49nBb`
- **table_id**: `tblM2sYDIMnGvINr`
- **字段映射（记录操作用字段名）**:
  - 今日亮点 (Text) — 今日做得好的事/重点完成的事
  - 日期 (DateTime) — 复盘日期 (Unix ms)
  - 今日不足 (Text) — 今天的不足之处
  - 明日计划 (Text) — 明天计划完成的事
- **添加记录**: `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records`
- **模板脚本**: feishu-api skill 的 `templates/daily-review.py`

### 感悟记录飞书文档
- **URL**: https://my.feishu.cn/docx/MnQRd4rNUoctsVxM4rPcLcRRn04
- **document_id**: `MnQRd4rNUoctsVxM4rPcLcRRn04`
- **标题**: 感悟记录
- **格式**: 先加日期标题（block_type=2，加粗日期时间），再加内容段落（block_type=2）
- **处理规则**: 仅做口头禅/啰嗦句的清理，保留原始行文结构
- **追加方式**: GET 获取 token → POST `/open-apis/docx/v1/documents/{doc_id}/blocks/{page_id}/children?document_revision_id=N`
- **注意**: 需要先 GET 文档获取最新 revision_id

### 想法记录 Bitable
- **app_token**: `WSyEbu2EhavajVsQBVRcYbKenWb`
- **table_id**: `tblvSu7Bv3yQw7oH`
- **字段映射**:
  - 编号
  - 记录时间
  - 想法
  - 期待结果
  - 执行情况
  - 调研与思考
  - 投产比评估 (单选：⭐绝佳点子 / 👍一般 / ❌不靠谱 / 🤔待评估)
  - 投入成本
  - 技术可行性 (单选：✅高 / 🟡中 / 🔴低 / 🚫不可行)
- **工作流**: 记录想法 → 调研评估 → 填写投产比和可行性 → 简单任务直接执行，复杂任务等待用户确认

---

## 飞书 API 要点

- 每次操作前获取新 token：`POST /open-apis/auth/v3/tenant_access_token/internal`
- App ID: `cli_a92fa611b5b9dbc2`
- POST 操作用 `fields` 传入字段（使用字段名而非 field_id）
- 日期字段需要 Unix 时间戳（毫秒）
- 飞书文档追加前必须先 GET 获取最新 `document_revision_id`

---

## GitHub

- **用户名**: jackwan317
- **认证方式**: `GITHUB_TOKEN` 环境变量 + `gh auth setup-git`
- Token 具有 `repo` + `workflow` 权限，持久化在 `~/.hermes/.env`
- **知识库仓库**: jackwan317/hermes-knowledge-base — 本地路径 `~/hermes-knowledge-base/`
- **报告库仓库**: jackwan317/hermes-reports — 本地路径 `~/hermes-reports/`
- **当前状态**: 国内服务器网络不通 GitHub，无法 push。迁移到海外服务器后恢复。

---

## 用户目标

- **3 个月目标**: 睡后月入过万的产品或商业模式
- **6 个月目标**: 累计赚 50 万
- **工作方式**:
  1. 用户发「生财有术」帖子 → 重构为 AI Agent 可执行的 SOP（整条链路，非单步提效）
  2. 定期搜索 skills 仓库找赚钱相关 skill/skill 组合，搜到先给用户审，不擅自安装
  3. 搜索方向：低成本获客、商机发现、产品选品上线售卖等

---

## 双 Agent 对抗性 Idea 评审系统

用户搭建了双 Hermes Agent 对抗性 Idea 评审系统：
- **本 Agent**（二代-hermes / DeepSeek V4 Pro）= Agent 1 猎手+辩手
- **战友**（Mac-hermes / GPT-5.5）= Agent 2/3/4 魔鬼代言人+裁判+执行
- **飞书群「赛博团队」**: chat_id=`oc_29e92db56abde591c072120e72958de5`（工作沟通 @Mac-hermes 用）
- **用户与我的主通道**: 本 DM 会话
- **GitHub pipeline 协作**: proposal.md → questions.md → defense.md → judgment.md
- **阶段流转**: proposal_ready → questions_ready → defense_ready → judged
- **仓库**: https://github.com/jackwan317/hermes-knowledge-base/tree/main/pipeline

---

## Idea 筛选标准（硬门槛 + 偏好）

### 硬门槛（缺一不可）
1. 搜索趋势/社区热度高
2. 技术成熟可做

### 偏好与原则
- 不预设 B2B/B2C——B2C 更容易验证市场，不毙掉
- 唯一一票否决：重依赖单一封闭平台 API + 自建双边冷启动

### 用户反馈（纠正过的错误假设）
1. API 价格趋势是越来越便宜，10 倍涨价不是合理假设
2. 大厂 6 个月跟进不是风险——是 6 个月的赚钱窗口期，且大厂更可能收购而非竞争
3. 「用户为什么不自己做」是伪命题——花钱省时间是市场常态
4. B2C 不应被毙掉，可以跑——用户也考虑 B2C 业务

---

## 其他

- 用户在 2026-05-27 复盘中的"KITOP"是 GitHub 的拼写错误，不是独立工具名
- 环境：当前国内服务器外网全不通（GitHub/Google/Reddit 全部超时），迁移海外后恢复
