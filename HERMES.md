# Hermes Agent 知识库 —— 新 Agent 接入指南

> 如果你是一个新创建的 Hermes Agent，正在阅读这个文件，请按以下步骤操作。

---

## 欢迎，新 Hermes！

你的前任已经为你准备好了所有必要的知识。你不需要从头学习，也不需要再问用户同样的问题。

### 第 1 步：加载用户画像

读取 [USER_PROFILE.md](USER_PROFILE.md)，用 `memory` 工具保存关键信息：
- 用户的身份、技术栈、兴趣领域
- 用户的交互偏好（语言、风格、确认方式）
- 用户常用的工具平台

### 第 2 步：学习持久记忆

读取 [MEMORY.md](MEMORY.md)，用 `memory` 工具逐条保存：
- 飞书文档体系（文件夹、Bitable、文档 ID 和字段映射）
- 飞书 API 调用要点
- GitHub 账号和认证方式

**重要**：这些是用户花时间配置好的，请确保你的 memory 中包含这些内容。这样下次用户说「帮我记一条今天的复盘」，你不需要问「哪个表？」。

### 第 3 步：了解已有技能

读取 [SKILLS.md](SKILLS.md)，了解前任创建了哪些自定义技能。

如果用户提到「评审一个 idea」，你应该加载 `idea-adversarial-review` 技能（完整文件在 `skills/autonomous-ai-agents/idea-adversarial-review/SKILL.md`），而不是从头发明评审流程。

### 第 4 步：安装自定义技能（可选）

如果你有文件系统访问权限，可以将 `skills/` 目录下的技能文件复制到你的 `~/.hermes/skills/` 目录中：

```bash
cp -r skills/autonomous-ai-agents/idea-adversarial-review ~/.hermes/skills/autonomous-ai-agents/
```

这样 Hermes 的技能系统会自动识别它，你可以用 `skill_view('idea-adversarial-review')` 直接加载。

---

## 仓库结构

```
hermes-knowledge-base/
├── README.md              ← 你在看这
├── HERMES.md              ← 新 Agent 接入指南（本文件）
├── MEMORY.md              ← 持久记忆（飞书配置、GitHub、工作流）
├── USER_PROFILE.md        ← 用户画像（身份、偏好、技术栈）
├── SKILLS.md              ← 自定义技能索引
└── skills/
    └── autonomous-ai-agents/
        └── idea-adversarial-review/   ← 完整技能文件
            ├── SKILL.md
            └── references/
```

---

## 用户的话

> 「我不想把我告诉过的事情再教一遍。」

这个仓库存在的意义就是：**一次教，永远记住**。请认真阅读以上内容，确保你能无缝接续工作。
