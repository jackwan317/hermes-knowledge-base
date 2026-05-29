# Hermes Knowledge Base Sync

Procedure for syncing Hermes Agent's active memory and skills to the `jackwan317/hermes-knowledge-base` GitHub repository.

## When to Run

- Cron job or on-demand sync of all Hermes memories and skills
- After significant memory updates or skill changes

## Source Files (Hermes → Repo direction)

| Source (Hermes active) | Destination (repo) |
|---|---|
| `~/.hermes/memories/MEMORY.md` | `~/hermes-knowledge-base/MEMORY.md` |
| `~/.hermes/memories/USER.md` | `~/hermes-knowledge-base/USER_PROFILE.md` |
| `~/.hermes/skills/*/SKILL.md` | `~/hermes-knowledge-base/skills/*/SKILL.md` |

## Procedure

### 1. Compare memory files

```bash
# Read Hermes active memory
cat ~/.hermes/memories/MEMORY.md
cat ~/.hermes/memories/USER.md

# Read repo versions
cat ~/hermes-knowledge-base/MEMORY.md
cat ~/hermes-knowledge-base/USER_PROFILE.md
```

The Hermes memory files use a terse paragraph format (sections separated by `§`). The repo files use richer markdown with headers, tables, and structured formatting. When syncing, the repo format should be preserved — merge new Hermes content into the repo's formatting, not the other way around.

### 2. Compare skill files

```bash
# List Hermes skills
find ~/.hermes/skills -name "SKILL.md" | sort

# List repo skills
find ~/hermes-knowledge-base/skills -name "SKILL.md" | sort

# Diff individual skills
diff ~/hermes-knowledge-base/skills/<path>/SKILL.md ~/.hermes/skills/<path>/SKILL.md
```

### 3. Update changed files

Only update files that actually differ. Use `patch` tool for targeted edits; use `write_file` for full rewrites (memory files typically need full rewrites since the formats differ).

### 4. Update SKILLS.md index

If any skill references change (new pitfalls, updated metadata), update `~/hermes-knowledge-base/SKILLS.md` to reflect it.

### 5. Git commit and push

```bash
cd ~/hermes-knowledge-base
git add -A
git commit -m "sync: 自动同步记忆和技能 $(date -I)"
git push origin main
```

## GitHub Auth Gotcha

The `GITHUB_TOKEN` environment variable is often **stale/expired**. The working token is stored in `~/.hermes/.env`:

```bash
# Working token
TOKEN=$(grep GITHUB_TOKEN ~/.hermes/.env | cut -d= -f2)

# Set remote with auth
git remote set-url origin "https://jackwan317:${TOKEN}@github.com/jackwan317/hermes-knowledge-base.git"
```

The token works for `curl` with `Authorization: Bearer` header, but for `git push` it must be used in the `username:token@host` URL format. If push fails with "Invalid username or token", the env var `GITHUB_TOKEN` is likely wrong — read directly from `.env`.

## Pitfalls

- **Remote ahead of local**: `git pull --rebase` before pushing if remote has new commits
- **Token expiry**: Always read from `~/.hermes/.env`, not from the shell env
- **Network restrictions**: Current server is in China with no outbound GitHub access. If push hangs, the server may still be restricted
- **Memory format drift**: Hermes memory is compact (`§` delimited), repo is rich markdown. Don't overwrite the rich format with the compact one — merge new facts into the rich structure
- **Built-in vs custom skills**: Most skills in `~/.hermes/skills/` are Hermes built-ins. Only sync skills that have been customized by the user (check with `diff`). Built-in skills change with Hermes updates and shouldn't be mirrored
