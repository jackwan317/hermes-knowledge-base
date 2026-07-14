---
name: policy-pipeline
description: 政策信息自动化流水线 — 官方信源采集→去重→AI评分→事实提取→飞书审核→小红书图文生成。当用户提到政策解读、新闻监控、小红书内容自动化、政府信息分析时使用。
---

# 政策信息自动化流水线

六阶段流水线：**官方信源定时采集 → 规则去重 → AI筛选评分 → AI事实化总结 → 飞书人工审核 → 自动生成小红书图文**

## 核心原则

1. **不要外部 API key**：Agent 本身就是模型（DeepSeek V4 Pro），AI 评分和事实提取直接由 Agent 在上下文中完成。`ai_pipeline.py` 需要独立 API key 是多余的——Agent 读 SQLite 数据 → 在脑中打分 → 写回 SQLite，无需 HTTP 调用。
2. **不要一开始就全自动发小红书**：政策和国际时事一旦总结错误，损失比省下来的几分钟更大。前期飞书保留人工审核列（审核状态：待审核/通过/退回/已发布）。
3. **采集是确定性任务交给脚本；AI 只处理需要判断的部分。**
4. **外交部记者会默认给 45-52 分基线，读正文后必须上调**——标题看起来是"例行答问"，但正文经常包含重磅政策信号。

## 项目位置

```
~/projects/policy-pipeline/
├── crawlers/         采集器（6个，5个可用）
│   ├── base.py       基类 + 三层次去重 + SQLite 操作
│   ├── mfa.py        外交部例行记者会 ✓
│   ├── xinhua.py     新华网国际频道 ✓
│   ├── gov_policy.py 国务院政策文件库 — Vue SPA，需 Playwright
│   ├── ndrc.py       发改委网上直播 — ⚠️ 只抓到预告，实录在 china.com.cn
│   ├── stats.py      国家统计局数据发布 ✓
│   └── un_news.py    联合国中文新闻 — ⚠️ 详情页 news.un.org 重定向 404
├── db/               SQLite（6表，去重+评分+提取+发布日志）
├── ai_pipeline.py    AI 评分+事实提取脚本（需独立 API key，不推荐直接用）
├── feishu_sync.py    飞书多维表格创建/字段配置/同步
├── run_crawler.py    采集器统一入口
├── .env.example      环境变量模板
└── output/           生成的小红书图片（待建）
```

## 运行环境

- Python: `/usr/bin/python3`（系统 3.12，有 bs4/requests/lxml）
- 不要用 venv 的 python3（3.11，没 pip）
- 需要 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 环境变量
- **不需要 DEEPSEEK_API_KEY**：Agent 直接处理评分和提取

## 信源状态

| 信源 | 状态 | 采集方式 | 关键问题 |
|------|------|---------|---------|
| 外交部 | ✅ | 静态 HTML, `ul.list1 li a` | 标题无信息量，必须读正文评分 |
| 新华网国际 | ✅ | 静态 HTML，多选择器容错 | 混有文化娱乐内容，需 AI 过滤 |
| 发改委 | ⚠️ | `ul.u-list li > a + span` | 列表页只有预告通知（122字），实录链接到 china.com.cn |
| 统计局 | ✅ | 静态 HTML | 纯数据内容，质量最高 |
| 联合国 | ⚠️ | 列表页可抓 | 详情页链接从 ungeneva.org 重定向到 news.un.org，直接拼接 404 |
| 国务院政策库 | ❌ | Vue SPA (`<div id="app">`) | 需 Playwright |
| 国新办 | ❌ | JS 反爬 cookie 挑战 | `curl -k` 可过 TLS 但被 JS challenge 拦截 |

## 数据库

6 张表：`raw_articles`, `ai_scores`, `fact_extracts`, `publish_log`, `crawl_log`, `event_groups`

去重三层次：

1. **URL 完全相同** → 直接去重，update crawl_count + 1
2. **body_hash 相同**（SHA-256 全文）→ 标记重复
3. **summary_256 相同**（前 256 字符 SHA-256）→ 大概率转载，AI 判断是否为同一事件

来源优先级：国务院(1) > 国新办(2) > 部委(3) > 新华社(4) > 其他(5+)

## AI 评分（Agent 直接在上下文中完成）

公式：

```
总分 = 公共影响范围×30% + 普通人相关度×25% + 政策新颖性×20% + 可解释性×15% + 时效性×10%
```

阈值：
- ≥80：优先单独做（publish_advice=special）
- 65-79：放进日报/周报合集（daily/weekly）
- 50-64：仅入资料库，不推飞书
- <50：忽略

排除项（直接 skip）：
- 领导人礼节性外事活动（会见、出访、致电祝贺等）
- 纯内部分工/人事任免
- 文化娱乐活动报道（音乐会、体育赛事等）
- 纯预告通知无实质内容（如发改委每月新闻发布会预告）
- 过于专业的行业技术细节

**外交部记者会特殊处理**：标题永远是"X月X日外交部发言人XXX主持例行记者会"，但正文经常包含重磅内容。例如"7月13日记者会"实际包含「习近平将出席世界AI大会发表主旨讲话」。**默认给 45-52 分基线，读完正文后必须上调。**

## 事实提取规则（三层分离！）

必须输出结构化 JSON，三个数组严格分离：

- **facts[]**：原文明确陈述的内容（可引用为事实）
- **inferences[]**：基于事实的判断，以"这可能意味着"的确定性级别表达
- **uncertainties[]**：尚未明确的信息

**推断不能写成确定事实。不能补充材料中不存在的数字、原因和结论。**

每个 key_numbers 后保留来源编号。避免官话、口号和情绪化表达。

## 飞书多维表格

候选审核表 17 字段：事件标题、发布时间、来源机构、原文链接、内容分类（单选:经济/就业/科技/外交/民生/产业/国际）、重要性评分、普通人相关度、新颖性、影响对象、关键数字、政府具体行动、AI事实摘要、AI趋势判断、发布建议（单选:日报/专题/周报/放弃）、审核状态（单选:待审核/通过/退回/已发布）、入库时间、文章ID。

### 创建和同步命令

```bash
# 创建表格
/usr/bin/python3 feishu_sync.py create

# 配置字段
/usr/bin/python3 feishu_sync.py setup-fields <app_token> <table_id>

# 同步文章到飞书
/usr/bin/python3 feishu_sync.py sync <app_token> <table_id>
```

### Pitfalls

- **folder_token 可能失效**：`DriveNodeNotExist` 错误表示文件夹 token 不再有效。回退方案：不传 folder_token 在根目录创建。
- **飞书 API PUT vs POST**：重命名字段需要 `PUT`，添加字段需要 `POST`。`feishu_post` 函数已改为支持 `method` 参数。
- **字段重命名后检查**：重命名一个字段可能导致其他字段消失，操作后务必重新 list fields 确认。
- **sqlite3.Row 不支持 .get()**：使用 `row["key"]` 方括号语法。execute_code 沙箱中 `row_factory` 可能不生效。
- **只推送高分文章**：默认 min_score=65，低于此的不进飞书。

## 采集器开发经验

### 判断页面是否需要 Playwright

```bash
curl -s --connect-timeout 5 --max-time 10 "$URL" | grep -c "id=.app"
# > 0 → SPA，需要 Playwright
```

### 常见采集问题

- **国新办**：JS 生成的 cookie challenge，设置 cookie 后 location.href 重定向。即使 `curl -k` 过 TLS 也不行。
- **发改委**：`ul.u-list li > a + span`，结构清晰。但内容是"预告通知"而非实录——实际发布会实录链接到 china.com.cn。正文仅 122 字，AI 应标记为 skip。
- **联合国**：列表页 `ungeneva.org/zh/news-media/news-list`，链接格式 `/zh/news-media/news/2026/07/120654/...`，但详情页实际在 `news.un.org/feed/view/zh/story/...`，需要额外一步解析来获取正确链接。
- **新华网时间解析**：页面可能没有明确的日期 DOM 元素，需要从标题文字中提取（如"新华社华盛顿7月13日电"）。

## 工作流：Agent 处理评分和提取

正确的流程是 Agent 直接在上下文中完成——不需要 `ai_pipeline.py`：

1. `execute_code` 查询 `raw_articles` 中未评分的文章（含 body_text 前 500 字符预览）
2. Agent 阅读内容，按五维公式打分，用 `execute_code` 写入 `ai_scores` 表
3. 对 ≥65 分的文章做事实提取（读完整 body_text）
4. 用 `execute_code` 写入 `fact_extracts` 表
5. 最后运行 `feishu_sync.py sync` 推送到飞书

`ai_pipeline.py` 仅作为备选方案（需要独立 API key 时使用）。

## 定时频率（待配置 CRON）

| 时间 | 任务 |
|------|------|
| 09:00 | 抓取前一晚及早间政策 |
| 12:30 | 抓取国新办、部委动态 |
| 18:30 | 抓取外交部记者会及当日更新 |
| 21:00 | 当日去重、AI评分、生成候选日报 |
| 周一 08:00 | 生成上周国家行动总结 |

## 参考文件

- `references/architecture.md` — 用户原始方案全文（含信源清单、评分公式、字段设计、栏目安排）
- `references/schema.sql` — 完整数据库表结构
- `references/scoring-prompt.md` — AI 评分 system/user prompt 模板
- `references/extraction-prompt.md` — 事实提取 + 小红书生成 + 校验规则 prompt 模板
