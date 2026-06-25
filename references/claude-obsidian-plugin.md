# claude-obsidian (plugin)

Transport layer connecting this AIOS to Sean's second brain — the Obsidian vault at
`~/Documents/Obsidian Vault`. Not an API with endpoints; it's a Claude Code
skill/plugin bundle that reads and writes vault notes directly (via the Obsidian CLI
where available, falling back to filesystem Read/Write/Edit).

## What it is

A set of `claude-obsidian:*` skills (this session lists `wiki`, `wiki-cli`, `wiki-ingest`,
`wiki-query`, `wiki-lint`, `wiki-fold`, `wiki-mode`, `wiki-retrieve`, `save`, `canvas`,
`autoresearch`, plus `verifier` and `wiki-ingest`/`wiki-lint` sub-agents). Together they
turn the Obsidian vault into a structured, queryable knowledge base rather than a flat
folder of markdown files — domain-first wiki spanning Sentinel CMMC, the SEO Agent, and
client work (per the vault's own `wiki/overview.md`).

## Mechanism (no API key/OAuth — it's a transport, not a service)

1. **Preferred transport**: the Obsidian CLI (Obsidian 1.12+) — `wiki-cli` skill wraps
   it for read/write/search/daily-note operations. No MCP server, no REST API plugin,
   no TLS workarounds needed.
2. **Fallback transport**: direct filesystem Read/Write/Edit against the vault path
   when the CLI is unavailable.
3. Per `connections.md` row 6, this was wired and the domain-first wiki scaffolded
   2026-06-19, with existing notes ingested at that time.

There's nothing to rotate or store in `.env` — it's local filesystem/CLI access, not a
remote credential.

## Key skills and what they do

- **`wiki`** — bootstrap/setup entry point; scaffolds vault structure from a one-line
  description, routes to the right sub-skill.
- **`wiki-cli`** — the actual read/write/search transport (Obsidian CLI wrapper).
- **`save`** — saves the current conversation or a specific insight into the vault as a
  structured note (this is the one CLAUDE.md's "Second brain" section points to for
  mirroring business decisions).
- **`wiki-ingest`** — ingest external sources (files, URLs, batches) into the vault:
  extracts entities/concepts, files pages, cross-references, logs the operation.
- **`wiki-query`** — answers questions using the vault: hot cache → index → relevant
  pages, in that read order (or hybrid BM25+rerank if `wiki-retrieve` is opted in).
  Supports quick/standard/deep modes.
- **`wiki-lint`** — health check: orphan pages, dead wikilinks, stale claims, missing
  cross-refs, frontmatter gaps.
- **`wiki-fold`** — rolls up `wiki/log.md` entries into summary "fold" pages.
- **`wiki-mode`** — lets the vault declare an organizational methodology (LYT/PARA/
  Zettelkasten/Generic); defaults to generic.
- **`canvas`** — adds images/text/PDFs/wiki pages to Obsidian `.canvas` visual files.
- **`autoresearch`** — autonomous web research loop that files findings into the wiki.

## Usage in this repo's context

Per `CLAUDE.md`'s "Second brain" section, this repo treats the vault as the place
business-relevant decisions and lead activity should leave a trace, separate from
this repo's own `decisions/log.md`:

- **Business decisions**: when a decision is logged to `decisions/log.md` here and it's
  business-level (product direction, client/lead handling, market positioning — not
  pure refactors/bug fixes), it also gets mirrored as a page/note under the vault's
  `wiki/decisions/`. Purely technical/dev decisions stay local only.
- **Leads**: the `lead-triage` agent writes synthesized solicitation summaries into the
  vault's `wiki/domains/sentinel-cmmc/comms/`, in addition to the staging table in this
  repo's `leads/inbox.md`.
- **Read-before-assume**: read `wiki/hot.md` then `wiki/index.md` in the vault before
  assuming a domain lacks context — check there before re-deriving from scratch.
- **What doesn't get ingested**: routine file edits, in-progress code, anything not yet
  decided. Bar is "would future-Sean want to find this browsing the wiki," not "did
  something happen."

## Gotchas

- This is a **plugin/skill bundle that runs inside this Claude Code session**, not a
  remote API — there's no endpoint list to document the way Buffer/Slack/GSC have one.
  The "API surface" is the skill set above.
- Per the memory note on Obsidian update cadence: the vault should sync at least daily
  for every project this AIOS touches, not just at noteworthy moments — don't treat
  vault-writing as optional/occasional.
- Vault-sync also runs via 2 separate cloud routines (7am/8pm ET) that stage
  `vault-sync/pending-*.md` files on `main` in this repo for manual pull into Obsidian —
  that's a distinct mechanism from the live `claude-obsidian` skills described here, see
  the `project_vault_sync_cloud_routines` memory note.
- Per `feedback_obsidian_update_cadence` memory: cadence is "daily minimum," not yet
  fully automated — still something Sean/the AIOS needs to actively do, not a fire-and-
  forget background sync.
