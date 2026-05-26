# Memory（Hermes 持久记忆）

> 以下是 Hermes Agent 在与用户 jackwan317 交互过程中积累的持久记忆。
> 新 Agent 应将这些信息加载到自己的 memory 中，以便无缝接续工作。

---

## 飞书文档体系

### 默认文件夹
- **Token**: `WYvrfJEuflZtMQdgUcjcc2HlnLX`
- **规则**: 除非用户特别指定，所有新建飞书文档都放在此文件夹下。

### 每日复盘 Bitable
- **URL**: https://my.feishu.cn/base/VsL5b9zSRaO3A7sPBdWcye49nBb
- **app_token**: `VsL5b9zSRaO3A7sPBdWcye49nBb`
- **table_id**: `tblM2sYDIMnGvINr`
- **字段映射**:
  - `fldxuvUGmS`: 今日亮点 (Text)
  - `fldghIeoEz`: 日期 (DateTime)
  - `fldyeFRWAQ`: 今日不足 (Text)
  - `fldoMCBBFr`: 明日计划 (Text)
- **添加记录**: `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records`

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
  - `fldqySoPi2`: 记录时间
  - `fldwSad4pJ`: 想法
  - `fldaA9cPrw`: 期待结果
  - `fldd3VOxvV`: 调研与思考
  - `fld9FqZE88`: 投产比评估 (单选：⭐绝佳点子 / 👍一般 / ❌不靠谱 / 🤔待评估)
  - `fldCIqI1bJ`: 投入成本
  - `fldF0FCZ0L`: 技术可行性 (单选：✅高 / 🟡中 / 🔴低 / 🚫不可行)
- **工作流**: 记录想法 → 调研评估 → 填写投产比和可行性 → 简单任务直接执行，复杂任务等待用户确认

---

## 飞书 API 要点

- 每次操作前获取新 token：`POST /open-apis/auth/v3/tenant_access_token/internal`
- App ID: `cli_a92fa611b5b9dbc2`
- POST 操作用 `fields` 传入字段
- 日期字段需要 Unix 时间戳（毫秒）
- 飞书文档追加前必须先 GET 获取最新 `document_revision_id`

---

## GitHub

- **用户名**: jackwan317
- **认证方式**: `GITHUB_TOKEN` 环境变量 + `gh auth setup-git`
- Token 具有 `repo` + `workflow` 权限，持久化在 `~/.hermes/.env`
- 本知识库仓库: https://github.com/jackwan317/hermes-knowledge-base
