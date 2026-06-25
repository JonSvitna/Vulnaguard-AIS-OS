# Linear

Connects the AIOS to Sean's Linear workspace for project/task tracking via the
`claude.ai Linear` MCP connector — no API key or `.env` entry, the connector is wired
into the Claude environment directly. Sentinel-CMMC is tracked under the
"Sentinel-CMMC Pilot Readiness Gap Closure" project; SEO Agent has its own project
for `vulnaguard-seo-agent` repo changes.

## Auth flow

No manual auth — the MCP connector (`claude.ai Linear`) handles OAuth to the Vulnaguard
Linear workspace at the platform level. Tools just show up as `mcp__claude_ai_Linear__*`
in any session where the connector is enabled. Nothing to rotate or store in `.env`.

## Key tools

Issues:
- `list_issues` — filter by assignee (`"me"` for Sean), team, project, state, label,
  cycle, priority, query (title/description search), createdAt/updatedAt windows.
- `get_issue` — full detail by ID/identifier (e.g. `LIN-123`), optionally including
  relations, releases, customer needs.
- `save_issue` — create (needs `title` + `team`) or update (pass `id`) an issue;
  sets state, assignee, project, labels, priority, due date, parent/blocking relations.
  Relation fields (`blockedBy`, `blocks`, `relatedTo`) are append-only — they never remove
  existing relations, use the `remove*` variants for that.

Projects / teams / milestones:
- `list_projects`, `get_project` — project name/ID/slug lookup, optional members/milestones/resources.
- `list_teams`, `get_team` — team lookup by name/key/UUID.
- `list_milestones`, `get_milestone`, `save_milestone` — project milestones.
- `list_cycles` — team's sprint/cycle list (current/previous/next).

Comments & docs:
- `list_comments`, `save_comment` — top-level threads or inline (anchored) comments on
  issues/projects/initiatives; pass `parentId` to reply to an existing thread.
- `delete_comment` — can't delete inline-anchored root comments, only replies.
- `list_documents`, `get_document`, `save_document` — Linear docs attached to a
  project/issue/initiative/cycle/team.
- `get_status_updates`, `save_status_update`, `delete_status_update` — project/initiative
  health updates (`onTrack`/`atRisk`/`offTrack`).

Labels & users:
- `list_issue_labels`, `create_issue_label`, `list_project_labels` — label management.
- `list_users`, `get_user` — workspace users (`"me"` resolves to Sean).
- `list_issue_statuses`, `get_issue_status` — per-team workflow states.

Attachments & diffs (GitHub PR integration):
- `prepare_attachment_upload` → PUT raw bytes → `create_attachment_from_upload` — the
  correct flow for attaching files to an issue (the older `create_attachment` base64
  path is deprecated, tiny-files-only).
- `get_attachment`, `delete_attachment`, `extract_images` (pulls images out of markdown
  for viewing).
- `list_diffs`, `get_diff`, `get_diff_threads` — Linear's PR/diff review surface, looked
  up by GitHub PR URL, Linear review URL, or identifier.

Docs search:
- `search_documentation` — searches Linear's own help docs, not the workspace data.

## Common usage patterns in this repo

**Check open work on Sentinel-CMMC before a planning session:**
```
list_issues(project: "Sentinel-CMMC Pilot Readiness Gap Closure", state: "...")
```

**Pull a specific issue's full context:**
```
get_issue(id: "LIN-123", includeRelations: true)
```

**Log a new task discovered mid-session:**
```
save_issue(title: "...", team: "...", project: "SEO Agent", priority: 3)
```

**Add a status note after a work session:**
```
save_comment(issueId: "LIN-123", body: "...")
```

## Gotchas

- IDs/slugs/names are all accepted as lookup keys for most `query`/`team`/`project`
  params — Linear's MCP resolves fuzzy matches, but a tight name match is safer than a
  loose keyword when there are multiple similarly-named projects.
- Markdown content fields (`description`, comment `body`, document `content`) want
  literal newlines, not `\n` escape sequences, per the MCP server's own instructions.
- This doc was written from tool descriptions/schemas only — **no live calls were made**
  against the real workspace to avoid touching real state. Treat field-level behavior
  (e.g. exact filter semantics, what "include archived" returns) as accurate-per-schema
  but unverified against actual Vulnaguard workspace data.
- No `scripts/linear_api.py` — this is MCP-only, there's no REST/script layer like
  Buffer or Slack have.

## Rotating access

Nothing to rotate locally. If the connector needs to be reauthorized or disconnected,
that happens in the claude.ai connector settings (not this repo), since there's no
locally stored token.
