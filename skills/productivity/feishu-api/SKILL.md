---
name: feishu-api
description: Interact with Feishu/Lark Open API via curl — auth, folder listing, Bitable CRUD, field management.
---

# Feishu / Lark Open API

Interact with Feishu (飞书) / Lark via the Open API using `curl` + `python3`. Credentials come from environment variables.

See `references/pitfalls.md` for common errors (browser sandbox, f-string backslash, bash quoting).

## Prerequisites

Env vars must be set:
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`

## Auth — Get Tenant Access Token

```bash
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id": "'"$FEISHU_APP_ID"'", "app_secret": "'"$FEISHU_APP_SECRET"'"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["tenant_access_token"])')
```

Token lasts ~2 hours. Use `-H "Authorization: Bearer ${TOKEN}"` on all subsequent calls.

**PITFALL**: The quoting pattern `'"'"$VAR"'"'` is required to embed bash vars inside single-quoted JSON strings. Do NOT use `"$VAR"` inside `'...'` — the dollar sign won't expand.

## List Folder Contents

```bash
curl -s -X GET "https://open.feishu.cn/open-apis/drive/v1/files?folder_token=${FOLDER_TOKEN}&page_size=50" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool
```

Returns files array with: `name`, `token`, `type`, `url`, `parent_token`.

## Create a Bitable (多维表格)

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/bitable/v1/apps' \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d "{\"name\": \"Table Name\", \"folder_token\": \"${FOLDER_TOKEN}\"}" \
  | python3 -m json.tool
```

Returns `app_token`, `default_table_id`, `url`. The default table comes with 4 fields: 文本 (Text), 单选 (SingleSelect), 日期 (DateTime), 附件 (Attachment).

## List Fields in a Table

```bash
curl -s -X GET "https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool
```

## Rename a Field

```bash
curl -s -X PUT "https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields/${FIELD_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{"field_name": "New Name", "type": 1}' | python3 -m json.tool
```

**PITFALL**: Renaming a field may cause other unchanged fields to disappear. Always re-list fields after renaming to confirm what remains.

## Add a Field

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{"field_name": "Field Name", "type": 1}' | python3 -m json.tool
```

## Delete a Field

```bash
curl -s -X DELETE "https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields/${FIELD_ID}" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool
```

## Rename a Table

```bash
curl -s -X PATCH "https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d "{\"name\": \"New Table Name\"}" | python3 -m json.tool
```

## Create a SingleSelect Field with Options

When adding a SingleSelect (type=3) field, include `property.options`:

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "field_name": "Status",
    "type": 3,
    "property": {
      "options": [
        {"name": "Option A", "color": 1},
        {"name": "Option B", "color": 2}
      ]
    }
  }' | python3 -m json.tool
```

Colors: 1=blue, 2=cyan, 3=red, 4=yellow, 6=gray, 13=orange. Options get auto-generated `id` values (e.g. `optPt0k2Hj`).

## Field Types Reference

| type | ui_type      | Description    |
|------|-------------|----------------|
| 1    | Text        | 文本           |
| 2    | Number      | 数字           |
| 3    | SingleSelect | 单选           |
| 5    | DateTime    | 日期           |
| 17   | Attachment  | 附件           |

## Add a Record to a Table

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "fields": {
      "日期": 1716681600000,
      "今日亮点": "完成了A、B、C"
    }
  }' | python3 -m json.tool
```

Date values are Unix timestamps in **milliseconds**.

## Create a Doc (文档)

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/docx/v1/documents' \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d "{\"title\": \"Doc Title\", \"folder_token\": \"${FOLDER_TOKEN}\"}" \
  | python3 -m json.tool
```

Returns `document_id` and `revision_id`. The document's page block shares the same ID as the document.

## Append Content to a Doc

First get the latest `revision_id`:

```bash
curl -s -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/${DOC_ID}" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["document"]["revision_id"])'
```

Then append children to the page block (which has the same ID as the doc):

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/${DOC_ID}/blocks/${DOC_ID}/children?document_revision_id=${REV}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "children": [
      {
        "block_type": 2,
        "text": {
          "elements": [
            {
              "text_run": {
                "content": "Hello world",
                "text_element_style": { "bold": false }
              }
            }
          ],
          "style": {}
        }
      }
    ],
    "index": -1
  }' | python3 -m json.tool
```

`block_type: 2` = paragraph. `index: -1` appends at end. Use `text_element_style.bold: true` for bold text (e.g. date headings). New blocks get auto-generated `block_id` values (e.g., `doxcnBVM7uSOd7QDNXafcqhcfiH`).

**PITFALL**: Must include `?document_revision_id=${REV}` in the URL — otherwise you get a `1770001 invalid param` error even when the body is correct.

## Pitfalls

### execute_code 没有环境变量

`execute_code` 工具运行在沙箱中，无法访问 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 环境变量。模板 `templates/daily-review.py` 依赖这两个变量，因此**不能直接在 execute_code 中运行**。

**正确做法**：在 terminal 中用 `curl` 执行，shell 可以正常展开环境变量。或者先用 `curl` 获取 token，再把 token 写进 Python 脚本后运行。

### 终端超时

Bitable 写入 API 有时响应较慢，单次 curl 超时属于正常现象。可以分步执行（先获取 token，再写 Bitable，最后追加文档），每步独立运行以避免超时。

## Design Pattern: Create Bitable with Custom Fields

1. Create the bitable in target folder
2. List default fields
3. Rename the primary text field to your first custom field
4. Delete unwanted default fields (单选, 附件)
5. Add remaining custom fields
6. Re-list to verify structure
