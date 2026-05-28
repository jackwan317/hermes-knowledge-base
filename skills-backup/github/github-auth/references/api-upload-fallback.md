# API Upload Fallback — When `git push` Is Blocked

Some environments (firewalls, corporate networks, restricted cloud VMs) block outbound HTTPS to `github.com:443` while allowing `api.github.com:443`. When this happens, `git push` hangs or times out, but the GitHub REST API still works.

## Quick Diagnosis

```bash
# Test which endpoints are reachable
curl -s --connect-timeout 5 https://api.github.com 2>&1 | head -3
curl -s --connect-timeout 5 https://github.com 2>&1 | head -3
```

If `api.github.com` responds but `github.com` times out, use the API fallback.

## Python Recipe: Upload Files via Contents API

This script walks a local repo directory and uploads every file via `PUT /repos/{owner}/{repo}/contents/{path}`:

```python
import os
import base64
import requests

token = "<GITHUB_TOKEN>"
owner = "<owner>"
repo = "<repo>"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

repo_dir = "/path/to/local/repo"

for root, dirs, filenames in os.walk(repo_dir):
    dirs[:] = [d for d in dirs if d != '.git']
    for filename in filenames:
        filepath = os.path.join(root, filename)
        relpath = os.path.relpath(filepath, repo_dir)

        with open(filepath, 'rb') as f:
            content = f.read()

        encoded = base64.b64encode(content).decode('utf-8')
        payload = {
            "message": f"Add {relpath} via API",
            "content": encoded
        }

        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{relpath}"
        resp = requests.put(url, headers=headers, json=payload)

        if resp.status_code == 201:
            print(f"OK: {relpath}")
        elif resp.status_code == 422:
            # File already exists — use SHA to update instead
            # Skip for simplicity; see full update flow if needed
            print(f"SKIP (exists): {relpath}")
        else:
            print(f"FAIL {resp.status_code}: {relpath} - {resp.text[:200]}")
```

## Notes

- Files are uploaded one at a time; each creates its own commit.
- If a file already exists, the API returns 422. To update existing files, you must first GET the file to obtain its `sha`, then include that in the PUT payload.
- This method goes through `api.github.com`, not `github.com` — useful when only the API subdomain is reachable.
- The local `.git` directory is skipped in the walk.

## When to Use

- `git push` times out repeatedly (30s+)
- `GIT_TRACE=1 git push` shows "Trying <IP>:443..." and hangs
- You've confirmed `api.github.com` is reachable via curl
- You need to get files onto GitHub NOW and can't wait for network changes
