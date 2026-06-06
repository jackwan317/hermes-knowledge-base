每日复盘 Bitable：app_token=VsL5b9zSRaO3A7sPBdWcye49nBb，table_id=tblM2sYDIMnGvINr，URL=https://my.feishu.cn/base/VsL5b9zSRaO3A7sPBdWcye49nBb
字段（记录操作用字段名，非 field_id！field_id 仅供字段管理如 rename/delete）：
- 今日亮点 (Text) — 今日做得好的事/重点完成的事
- 日期 (DateTime) — 复盘日期 (Unix ms)
- 今日不足 (Text) — 今天的不足之处
- 明日计划 (Text) — 明天计划完成的事
添加记录时用 POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records，fields 中用字段名如 {"日期": ts_ms, "今日亮点": "..."}。模板脚本: feishu-api skill 的 templates/daily-review.py。
§
感悟记录飞书文档：document_id=MnQRd4rNUoctsVxM4rPcLcRRn04，标题=感悟记录，URL=https://my.feishu.cn/docx/MnQRd4rNUoctsVxM4rPcLcRRn04，位于默认文件夹。
追加新感悟时：GET 获取token → 用 POST /open-apis/docx/v1/documents/{doc_id}/blocks/{page_id}/children?document_revision_id=N 追加子块。格式：先加日期标题（block_type=2，加粗日期时间），再加内容段落（block_type=2）。需要先 GET 文档获取最新 revision_id。仅做口头禅/啰嗦句的清理，保留原始行文结构。
§
用户在 2026-05-27 复盘中的"KITOP"是 GitHub 的拼写错误，不是独立工具名。今日计划中"熟悉 KITOP 操作"应理解为"熟悉 GitHub 操作"。
§
用户 3 个月目标：睡后月入过万的产品或商业模式。6 个月目标：累计赚 50 万。工作方式：① 用户发生财有术帖子 → 我重构为 AI Agent 可执行的 SOP（整条链路，非单步提效）；② 定期搜索 skills 仓库找赚钱相关 skill/skill 组合，搜到先给用户审，不擅自安装。搜索方向：低成本获客、商机发现、产品选品上线售卖等。
§
当前国内服务器网络不稳定：GitHub.com 和 API 可通但 raw.githubusercontent.com 仍超时，git push/pull 时好时坏（knowledge-base 可 push，reports 偶断连），Reddit/Google 等仍不通。迁移海外后恢复。
§
用户搭建了双 Hermes Agent 对抗性 Idea 评审系统：
- 本 Agent：二代-hermes（DeepSeek V4 Pro）= Agent 1 猎手+辩手
- 战友：Mac-hermes（GPT-5.5）= Agent 2/3/4 魔鬼代言人+裁判+执行
- 飞书群「赛博团队」chat_id=oc_29e92db56abde591c072120e72958de5（工作沟通@Mac-hermes用）
- 用户与我的主通道：本 DM 会话
- GitHub pipeline 协作：proposal.md → questions.md → defense.md → judgment.md
- 阶段流转：proposal_ready → questions_ready → defense_ready → judged
- 仓库：https://github.com/jackwan317/hermes-knowledge-base/tree/main/pipeline
§
用户对 Idea 风险评审的反馈（纠正了我之前的提问）：
1. API 价格趋势是越来越便宜，10 倍涨价不是合理假设
2. 大厂 6 个月跟进不是风险——是 6 个月的赚钱窗口期，且大厂更可能收购而非竞争
3. 「用户为什么不自己做」是伪命题——花钱省时间是市场常态
4. B2C 不应被毙掉，可以跑——用户也考虑 B2C 业务
§
Idea 筛选标准：① 搜索趋势/社区热度高 ② 技术成熟可做。不预设 B2B/B2C，B2C 可跑。唯一一票否决：重依赖单一封闭平台 API + 自建双边冷启动。
§
行为约定：用户描述 idea 时先给 MVP 验证方案再评价（MVP≤4h，终点是验证性结果）。已固化 skill：productivity/mvp-first。
§
用户2026-06-01确立纪律：①已删所有色情视频/小说；②再刷擦边/无意义视频则卸载APP；③无聊空虚时只读书/运动/冥想；④保持正念，不被情绪想象牵引；⑤每晚11点前睡觉（目标10点上床）；⑥主动社交减无效社交；⑦给想认识的人一次拒绝你的机会，不纠结；⑧让每次被拒绝有价值；⑨回到当下不为结果耿耿于怀。
