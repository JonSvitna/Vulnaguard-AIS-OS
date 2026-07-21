# Pending vault updates — 2026-07-19 AM

**Coverage window:** Since `pending-2026-07-18-AM.md` — commit `68bf73d` (2026-07-19 01:56 EDT).

---

## New items to consider for Obsidian

### Retired website-design-lead-finder agent (business direction)
- **What:** Archived both `.claude/agents/` and `.codex/agents/` copies of the `website-design-lead-finder` agent to `archives/website-design-lead-finder/`. `leads/website-design-inbox.md` left as-is (data, not automation).
- **Why:** Sean judged the website-dev lead line wasn't earning its keep. Part of a broader pass cutting automations that drain resources without pulling weight.
- **Note:** Agent was never scheduled (no cron, no Railway service) — only ran on manual trigger. Archive removes the suggestion surface, not a running cost.
- **Commit:** `68bf73d` | **Decisions log entry:** 2026-07-19
- **Vault target:** `wiki/decisions/` — product/automation retirement decision worth recording.

### Paused n8n content workflows + creative-os-render-worker already gone
- **What:** Deactivated two live n8n workflows via API: `Content Intake Pipeline v1` and `Content Intelligence Pipeline v1` (both confirmed `active: false`). Stops 5-min polling and Claude/Slack calls. n8n server stays running; workflows only are off.
- **Surprise finding:** `creative-os-render-worker` isn't there — not in Railway project list, URL returns edge 404. It was documented as live since 2026-07-10 but is already gone.
- **Follow-ups flagged (not yet acted on):**
  - `content_intake_video_queue` may have a backlog of unprocessed videos from whenever the worker died — worth checking the table before deciding to redeploy or fully retire.
  - n8n workflows are deactivated, not deleted — reactivate via `/activate` endpoint or n8n UI when content pipeline is wanted back.
- **Commit:** `68bf73d` | **Decisions log entry:** 2026-07-19
- **Vault target:** `wiki/decisions/` or `wiki/domains/seo-agent/` — resource-drain cleanup + infrastructure gap discovery.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — massive product direction cut (`commit 74deeb5`, flagged in `pending-2026-07-18-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **Approve now sends immediately** — workflow fix unblocking lead backlog (`commit 1dca53f`, flagged in `pending-2026-07-18-AM.md`). Vault target: process note.

---

*Check ran: 2026-07-19 AM. Next check: 2026-07-19 PM.*
