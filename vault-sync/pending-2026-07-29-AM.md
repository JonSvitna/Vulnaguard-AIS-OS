# Pending vault updates — 2026-07-29 AM

**Coverage window:** Since `pending-2026-07-28-AM.md` — commits `00a70de`, `913dab5`, `29cacd5`, `0d8b330` (2026-07-28 evening through 2026-07-29 AM UTC).

---

## New items to consider for Obsidian

### 1. "AI Is a Shovel" video published to OfficialSeanBuilds — 2026-07-28
- Long-form video live at `https://www.youtube.com/watch?v=qXsc6UORWnE` (public).
- Publishing pipeline extended: `youtube_api.py` now handles resumable upload, thumbnail set, and comment posting (PNG→JPEG re-encode to clear YouTube's undocumented ~2MB thumbnail limit). `connections.md` row 16 updated.
- **No API for comment pinning** — confirmed no endpoint exists in YouTube Data API v3. Stays a manual Studio step.
- Skill renamed: `seanbuilds-video-edit` → `video-creation` (now covers full raw-clips-to-live pipeline, not just edit).
- Decision log notes this as technical/dev — **no vault mirror needed per the log**. Flag here as a content milestone if you want it tracked in `wiki/domains/seanbuilds/`.
- Commit: `29cacd5`

### 2. Slack guest-access audit script scoped (`/level-up` 2026-07-27) — Brickline
- Root cause: wrong Slack guest had access → incorrect billing charge this week.
- `scripts/slack_guest_check.py` built: cross-references live Slack channel membership against SharePoint Excel "Approved" column; flags mismatches for Sean to act on (no auto-remove).
- **Blocking:** SharePoint site URL and guest sheet file path still needed from Sean. Script not yet real-world tested.
- **Also blocking:** MS365 env vars (`MS365_TENANT_ID`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET`, `MS365_USER_UPN`) not configured in remote/scheduled sessions — affects this script and anything else using Graph auth.
- Decision log flags this as business-level (Brickline, cost-control) — mirror to vault only if Brickline tracking is confirmed in scope there.
- Commit: `00a70de`

### 3. Lead triage still failing — day 4 (2026-07-29)
- Same `KeyError: 'MS365_USER_UPN'` failure in the scheduled session. 4th consecutive day.
- No new leads added. Any solicitation emails since 2026-07-20 are unreviewed.
- Fix is the same: set the MS365 env vars in Claude Code on the web environment settings.
- Commit: `0d8b330`

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **SeanBuilds site: real lead capture live** — Resend Audiences wired, all dead-end CTAs converted to inquiry modal. Commit `6e196f7` (2026-07-24). Vault target: `wiki/domains/seanbuilds/`.
- **SeanBuilds "AI Won't Replace You" — first social batch live** — LinkedIn + Instagram + YouTube Shorts. Brand/content milestone. Commit `ce606a5`. Vault target: `wiki/decisions/` or `wiki/domains/seanbuilds/`.
- **Clay → n8n → SEO agent cutover / Origami now owns Vulnaguard B2B pipeline** — outreach architecture change. Commits `5fe4c6d`, `42a2ac1`, `28f0063` (2026-07-21); `connections.md` row 21 added 2026-07-23. Vault target: `wiki/decisions/`.
- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut. Commit `74deeb5`. Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning. Commit `4b0197e`. Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-29 AM. Next check: 2026-07-30 AM.*
