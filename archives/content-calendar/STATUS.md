# content-calendar — archived 2026-07-23

Retired, not deleted, per repo archive convention. Both copies (`.claude/skills`,
`.agents/skills`) moved here so neither surface triggers it anymore.

**Why:** The "expand a picked idea into full drafts" half of this skill
calls `vulnaguard-seo-agent`'s `POST /api/content-pipeline/generate`. That
API was deleted from `main` on 2026-07-16 (commit `74deeb5`, "Strip SEO
agent, content pipeline, and video tooling"). The idea-generation half
(the calendar itself) still works fine in isolation, but the skill as
written promises a drafting step that no longer exists — archived whole
rather than left half-functional. `connections.md` had drifted out of
sync with the strip and still described this as "degraded" — corrected
2026-07-23.

**To restore:** decide what replaces content-pipeline for drafting
full platform copy, re-point the "expand idea" step at it, move both
`SKILL.md` copies back to `.claude/skills/content-calendar/` and
`.agents/skills/content-calendar/`.
