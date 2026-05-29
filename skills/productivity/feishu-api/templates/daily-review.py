#!/usr/bin/env python3
"""每日复盘 + 感悟记录：写 Bitable 记录 + 追加飞书文档。

环境变量: FEISHU_APP_ID, FEISHU_APP_SECRET

Bitable 字段映射（用字段名，非 field_id）：
  日期 (DateTime)     — 复盘日期 (Unix ms)
  今日亮点 (Text)      — 今日做得好的事
  今日不足 (Text)      — 今天的不足之处
  明日计划 (Text)      — 明天计划完成的事

感悟文档：标题=感悟记录，追加日期标题（粗体）+ 感悟内容段落。
"""

import os, subprocess, json
from datetime import datetime, timezone, timedelta

APP_ID = os.environ["FEISHU_APP_ID"]
APP_SECRET = os.environ["FEISHU_APP_SECRET"]

# ----- 配置区 -----
APP_TOKEN = "VsL5b9zSRaO3A7sPBdWcye49nBb"
TABLE_ID = "tblM2sYDIMnGvINr"
DOC_ID = "MnQRd4rNUoctsVxM4rPcLcRRn04"

TODAY = datetime(2026, 5, 26, tzinfo=timezone(timedelta(hours=8)))

HIGHLIGHT = "今日亮点内容"
WEAKNESS = "今日不足内容"
PLAN = "明日计划内容"

REFLECTION_DATE = "2026年5月26日 星期二"
REFLECTION_TEXT = "感悟正文..."
# ----- 配置区结束 -----


def get_token():
    resp = subprocess.run([
        "curl", "-s", "-X", "POST",
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET})
    ], capture_output=True, text=True, timeout=10)
    return json.loads(resp.stdout)["tenant_access_token"]


token = get_token()

# 1. 写 Bitable 复盘记录（字段名，非 field_id！）
ts_ms = int(TODAY.timestamp() * 1000)
body = {
    "fields": {
        "日期": ts_ms,
        "今日亮点": HIGHLIGHT,
        "今日不足": WEAKNESS,
        "明日计划": PLAN,
    }
}
url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
resp = subprocess.run([
    "curl", "-s", "-X", "POST", url,
    "-H", f"Authorization: Bearer {token}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps(body, ensure_ascii=False)
], capture_output=True, text=True, timeout=10)
result = json.loads(resp.stdout)
if result.get("code") == 0:
    print(f"OK 复盘记录已添加: {result['data']['record']['record_id']}")
else:
    print(f"ERR Bitable: {result.get('msg')}")

# 2. 追加感悟到文档
resp = subprocess.run([
    "curl", "-s", "-X", "GET",
    f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}",
    "-H", f"Authorization: Bearer {token}",
], capture_output=True, text=True, timeout=10)
rev = json.loads(resp.stdout)["data"]["document"]["revision_id"]

children = [
    {
        "block_type": 2,
        "text": {
            "elements": [{"text_run": {"content": REFLECTION_DATE, "text_element_style": {"bold": True}}}],
            "style": {}
        }
    },
    {
        "block_type": 2,
        "text": {
            "elements": [{"text_run": {"content": REFLECTION_TEXT, "text_element_style": {}}}],
            "style": {}
        }
    }
]
url2 = f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}/blocks/{DOC_ID}/children?document_revision_id={rev}"
resp = subprocess.run([
    "curl", "-s", "-X", "POST", url2,
    "-H", f"Authorization: Bearer {token}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"children": children, "index": -1}, ensure_ascii=False)
], capture_output=True, text=True, timeout=10)
result2 = json.loads(resp.stdout)
if result2.get("code") == 0:
    print(f"OK 感悟已追加 (revision: {result2['data']['document_revision_id']})")
else:
    print(f"ERR 文档: {result2.get('msg')}")
