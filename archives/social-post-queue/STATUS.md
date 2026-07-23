# social-post-queue — archived 2026-07-23

Retired, not deleted, per repo archive convention. Both copies (`.claude/skills`,
`.agents/skills`) moved here so neither surface triggers it anymore.

**Why:** This skill's entire job was pulling from `vulnaguard-seo-agent`'s
`content-pipeline` API (`GET /api/content-pipeline/next-unposted`,
`PATCH /api/content-pipeline/<id>/posted`). That API was deleted from `main`
on 2026-07-16 (commit `74deeb5`, "Strip SEO agent, content pipeline, and
video tooling") — the seo-agent repo now does one thing: qualify leads,
send outreach. The feeding n8n workflow (`Content Intake Pipeline v1`) was
separately deactivated 2026-07-19. `connections.md` had drifted out of
sync with both changes and still described this as "degraded" rather than
retired — corrected 2026-07-23.

**To restore:** decide what replaces content-pipeline for drafting
per-platform posts (revive the `feature/lead-email-filter-footer` branch's
content-pipeline code, or build fresh), re-point this skill's endpoints at
it, move both `SKILL.md` copies back to `.claude/skills/social-post-queue/`
and `.agents/skills/social-post-queue/`.
