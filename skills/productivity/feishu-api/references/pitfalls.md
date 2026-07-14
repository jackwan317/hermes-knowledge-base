# Pitfalls & Common Errors

## Browser Sandbox in Containers

The `browser` tool (Chrome/CDP) fails in container environments with sandbox errors:
```
FATAL:content/browser/zygote_host/zygote_host_impl_linux.cc:128] No usable sandbox!
```
**Workaround**: Use Feishu Open API via curl instead of trying to browse Feishu pages. The API gives programmatic access to all Drive/Docs/Bitable operations.

## Python3 F-String Backslash in Shell One-Liners

```bash
# WRONG — f-string backslash causes SyntaxError:
python3 -c 'import json,sys; d=json.load(sys.stdin); print(f"code={d[\"code\"]}")'

# RIGHT — use json.tool module instead:
python3 -m json.tool
```

Or extract a single value without f-string:
```bash
python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["code"], d["msg"])'
```

## Bash Variable Inside Single-Quoted JSON

The `'"'"$VAR"'"'` pattern is the reliable way to interpolate shell variables inside single-quoted JSON strings in bash:

```bash
-d '{"app_id": "'"$FEISHU_APP_ID"'", "app_secret": "'"$FEISHU_APP_SECRET"'"}'
-d '{"app_id": "'"$FEISHU_APP_ID"'", "app_secret": "'"$FEISHU_APP_SECRET"'"}'

This pattern: close single-quote, open double-quote, insert variable, close double-quote, open single-quote.

## Field IDs Become Stale After Rename

When you rename a Bitable field via PUT, other unmodified fields may silently disappear. The field IDs you captured before the rename can become stale — DELETE/PUT on them will return `FieldIdNotFound` (code 1254044).

**Always re-list fields** (`GET .../fields`) after ANY structural mutation (rename, add, delete) before using a field ID. Never assume field IDs persist across mutations.

## Record Creation/Update Uses Field Names, Not Field IDs

When creating or updating Bitable records, the `fields` object keys must be **field names** (e.g. `"日期"`, `"今日亮点"`), NOT `field_id` values (e.g. `"fldghIeoEz"`). Using field IDs returns `FieldNameNotFound` (code 1254045).

Field IDs are only valid for field management endpoints: rename (`PUT /fields/{field_id}`), delete (`DELETE /fields/{field_id}`), and listing. This is confusing because `GET /fields` returns `field_id` prominently, leading you to try using them in records.

```bash
# WRONG — uses field_id, returns 1254045
-d '{"fields": {"fldghIeoEz": 1779724800000, "fldxuvUGmS": "内容"}}'

# RIGHT — uses field names
-d '{"fields": {"日期": 1779724800000, "今日亮点": "内容"}}'
```

## Doc API Requires revision_id

When appending children to a doc via `POST .../blocks/{id}/children`, you MUST include `?document_revision_id=${REV}` in the URL. Omitting it causes `code: 1770001, invalid param` even when the request body is valid. Get the revision from `GET .../documents/{doc_id}` first.

## Folder Token Can Go Stale (DriveNodeNotExist)

A previously valid `folder_token` can return `DriveNodeNotExist` (code 1254702) if the folder was renamed, moved, or deleted. 

**Workaround**: Create the Bitable without a `folder_token` (in root), then manually move it to the target folder in the Feishu UI. The no-folder approach always works.

```bash
# Fallback: create in root
-d '{"name": "表格名称"}'
# Instead of:
-d '{"name": "表格名称", "folder_token": "WYvrf..."}'
```

## PUT vs POST for Field Operations

When using the Feishu Bitable API, different field operations need different HTTP methods:

- **Rename field**: `PUT /fields/{field_id}` with `{"field_name": "...", "type": N}`
- **Add field**: `POST /fields` with `{"field_name": "...", "type": N}`
- **Delete field**: `DELETE /fields/{field_id}`

Using `POST` for a rename will fail silently or return unexpected data. Always use `PUT` for renames.

When wrapping in a helper function, add a `method` parameter:

```python
def feishu_post(token, path, body, method="POST"):
    subprocess.run(["curl", "-s", "-X", method, path, ...])

# Usage:
feishu_post(token, rename_url, body, method="PUT")
feishu_post(token, add_url, body)  # default POST
```
