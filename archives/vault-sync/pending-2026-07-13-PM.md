# Pending vault updates — 2026-07-13 PM

**Coverage window:** Since the 2026-07-12 AM vault-sync (commit `b0e0e9b`). That check said "nothing new" — two PRs landed after it ran.

---

## Items to pull into Obsidian

### 1. MEMORY.md created — closes top Four-Cs audit gap
*Commit `07c716d`, PR #8 merged `23c3e2e`*

New live-state file (`MEMORY.md`) added to this repo as a durable "what's true right now" layer, separate from the append-only `decisions/log.md`. Surfaced by the Four-Cs audit as the top gap.

Key facts it documents (for vault: cross-check these are current):
- No paying clients yet. Q priority = land the first.
- Active blockers: Svitna App Store soft test gated on APNs/simulator walkthrough; SeanBuilds PR #2 open waiting on Sean's merge (live domain routing); M365 daily brief broken (MS365_TENANT_ID not set in cloud env).
- Stripe not yet configured; Mercury Bank is invoicing fallback.

**Vault target:** `wiki/domains/vulnaguard-ais-os/` — add or update a MEMORY note there if you want this findable from the shared vault.

---

### 2. Token discipline: drafting router + video consolidation
*Commit `2fadbba`, PR #9 merged `5176512` — logged in `decisions/log.md` entry 2026-07-12*

Three decisions made to stop burning personal API keys and avoid rebuilding paid infrastructure:

- **Drafting router (process change):** Any repeatable "write me X" routes to the seo-agent copywriter pipeline, the content-pipeline generate API, or the AIOS voice skills. Personal Claude/ChatGPT tabs reserved for one-off exploration only. Wired into `CLAUDE.md`.
- **Video consolidation (architecture):** creative-os Remotion is the single video spine going forward. HyperFrames `template-composer` (video-website-agent) and seo-agent `captureMode:"video"` are to be retired/frozen. Execution pending — needs access to those repos. The lever for better video output is the existing storyboard + `design_concepts` feedback loop, not new machinery.
- **URL intake Flow B (product spec):** Designed a ~5-change path to route videos dropped as external URLs (e.g. YouTube) to the render worker's existing yt-dlp path, not just Slack file uploads. SQL migration staged at `references/sql/content-intake-url-asset.sql`. Execution pending (needs `.env` / creative-os).

**Vault target:** `wiki/decisions/` — these are product architecture + cost decisions, not purely dev-level housekeeping.

---

*Check ran: 2026-07-13 PM. Next check: 2026-07-14 AM.*
