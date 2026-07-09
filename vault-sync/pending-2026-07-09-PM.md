# Pending vault updates — 2026-07-09 PM

**Coverage window:** Since the 2026-07-08 PM note (which found nothing). Covers 4 commits from overnight/this morning.

---

## AIS-OS architecture locked: master/specialist model confirmed (decisions/log.md, 2026-07-08)

**Decision:** `Vulnaguard-AIS-OS` is the root master AIOS. Peer repos (`creative-os`, `vulnaguard-capture-os`, `vulnaguard-seo-agent`) are called specialists — they pull from AIS-OS, not the other way around.

Practical consequences committed in `874fc4a`:
- `content-bank.md` is frozen/historical. Drafting moves into `vulnaguard-seo-agent`'s `content-pipeline` (DB-backed, multi-brand, generates all platform variants + video brief in one call).
- `social-post-queue` now sources and marks posts via DB endpoints (`GET /api/content-pipeline/next-unposted`, `PATCH /api/content-pipeline/<id>/posted`) instead of editing a markdown file.
- `seanbuilds-voice` persona added to the content-pipeline's personas table so SeanBuilds-domain content routes through the same engine as Vulnaguard-domain content.
- Dead duplicate skills in `vulnaguard-capture-os` cleaned up.
- Two live Creative OS handoff points documented: `social-post-queue` calls in for Instagram graphics; `content-pipeline` calls in for video composition.

**Vault action:** Log under `wiki/domains/vulnaguard-aios/` (architecture decision). This is the clearest statement of the cross-repo hierarchy to date.

---

## Content Intelligence Pipeline accepted and scaffolded (decisions/log.md, 2026-07-08; commits `1490864`, `7117426`)

**Decision:** Accepted a staged pipeline for making format decisions from what's winning in the AI/automation creator space, rather than guessing.

Stage order locked:
1. Stage 1 — Tavily API discovery + YouTube Data API metadata fetch (via n8n cron)
2. Stage 2 — Supabase: raw metadata + embeddings stored (title/caption/engagement/hashtags)
3. Stage 3 — Claude (primary) / GPT (fallback) classification: format type, topic, engagement tier, repeatable patterns. Output is strict JSON only.
4. Stage 4 — Write recommendations to a Notion "Content Playbook" consumed by `content-calendar` for format selection. **Notion integration scaffolded** (commit `7117426`).
5. Stage 5 — Feedback loop feeding first-party SeanBuilds performance data back to adapt the playbook. **Scaffold committed** (commit `7117426`); deferred until enough data exists.

Ownership locked: AIS-OS = orchestration, queue state, approvals. `creative-os` = asset production only. `vulnaguard-capture-os` = out of scope for this pipeline.

`connections.md` row 18 updated from placeholder to implementation-scoped. Workflow scaffold (`references/n8n/workflows/content-intelligence-pipeline-v1.json`) and SQL schema (`references/sql/content-intelligence-pipeline.sql`) committed.

Immediate next step: Stage 1 → Stage 2 implementation and data quality validation before adding model judgment layers.

**Vault action:** New page or note under `wiki/domains/seo-agent/content-intelligence/` (or similar). This is a multi-week implementation bet on a new content strategy infrastructure. Worth a dedicated page.

---

## No lead or context changes

No new entries in `leads/inbox.md` or `context/` files since the prior note.
