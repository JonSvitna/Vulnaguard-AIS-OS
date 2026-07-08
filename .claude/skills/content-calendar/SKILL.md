---
name: content-calendar
description: Generate and maintain a 30-day content idea calendar across SeanBuilds and Vulnaguard, then expand picked ideas by calling vulnaguard-seo-agent's content-pipeline to generate full platform-ready drafts. Use for "build my content calendar", "generate this month's content ideas", "what should I post about", "expand calendar idea N", or "regenerate the calendar".
---

> Personal accountability tool. Not for sale, not client-facing. Two domains only: **SeanBuilds** and **Vulnaguard**.

## What this closes

Sean's recurring blocker: nothing generated *what to write about* on a schedule, so posting
stalled on "I don't know what to talk about today." This skill is the idea engine.

As of 2026-07-08, drafting itself is fused into `vulnaguard-seo-agent`'s `content-pipeline`
(a real generation engine with DB + multi-brand voice support) instead of hand-writing drafts
into `references/content-bank.md` — that file is now historical/frozen (see its header).
`content-calendar` still owns *what to write about*; `content-pipeline` now owns turning that
into platform-ready drafts; `social-post-queue` still owns the only posting step.

```
hermes agent (scans commits for real moments)
       │
       ▼
references/hermes-opportunities.md (staged real entries, unused/used)
       │ pulled first when generating/refilling the month
       ▼
content-calendar  →  references/content-calendar.md (30 days of one-line hooks)
       │ expand picked rows
       ▼
vulnaguard-seo-agent POST /api/content-pipeline/generate
  (voiceSkillSlug: seans-voice-vulnaguard | seanbuilds-voice)
       │ generates linkedin/instagram/facebook/youtube + video_brief in one call
       ▼
social-post-queue (pulls via GET /api/content-pipeline/next-unposted → Buffer / IndieHackers)
```

## Domains and pillars

Two domains only, alternating day by day so neither goes silent. Each domain rotates
through 4 fixed pillars so ideas don't repeat or drift generic.

**SeanBuilds** (personal brand, builder-in-public):
1. Build log — what shipped or broke this week, and why
2. Lesson from a mistake — what went wrong, what changed after
3. A tool/automation actually in use — practical, not hype
4. Contrarian take — pushback on AI/productivity hype from someone actually building

**Vulnaguard** (Sentinel CMMC + the SEO agent — both ship under the Vulnaguard name):
1. CMMC myth or pain point contractors actually hit
2. Behind Sentinel — one real feature and the reason it exists
3. SEO agent in action — a specific thing it caught or automated
4. Credibility — PenTest+/forensics background applied to a real scenario

Do not invent a third domain or sub-brand. If an idea doesn't fit one of these 8
pillars cleanly, it's generic — discard it and write a different one.

## Hook rule (non-negotiable)

Every hook — hand-written or pulled from `hermes-opportunities.md` — must state the
measurable result of the change, not just that something was broken and got fixed.
"Found and fixed a bug" is not a hook. State what's concretely better now as a result:
a number, a before/after, a capability that didn't exist a moment ago. Bad: "Sentinel's
evidence extraction had a bug capping it at 5 pages." Good: "Raised Sentinel's evidence
cap from 5 to 12 pages — every control suggestion on a real policy doc now reads the
whole thing instead of silently grading off half of it." If a hermes-opportunities.md
entry's hook only describes the bug with no stated effect, rewrite it to state the
effect before slotting it into the calendar or expanding it into the bank.

## CTA rule (non-negotiable, per CLAUDE.md)

Every row in the calendar AND every expanded draft must name a CTA. Fixed per domain,
not improvised per post:

- **Vulnaguard** → `vulnaguard.com` (point people at the site; use a specific path
  instead of the root only if Sean gives one for that post)
- **SeanBuilds** → soft CTA — "comment '<keyword>'" or "DM me" (no live landing
  page yet; do not invent one)

## Generating the calendar

1. Read `references/hermes-opportunities.md` if it exists. Every `[unused]` entry
   there is a real, already-sourced moment (commit-backed hook + talking points +
   pillar guess).
   - **Detect shared themes before slotting.** If multiple unused entries trace to
     the same root cause, sub-product, or effort (e.g. several fixes from one audit
     pass on the same repo), sequence them as a mini-arc instead of scattering them
     across the rotation: an opening frame, the fixes in escalating/logical order,
     and a closing wrap that names what they had in common. Still respect the
     domain's pillar rotation for which slots they land in.
   - **Never merge across sub-products.** Sentinel CMMC and the SEO agent are
     separate products that both ship under the Vulnaguard name — they get separate
     arcs even when entries from both are unused at the same time. Don't build one
     story that blends a Sentinel fix with an SEO agent fix.
   - Entries with no shared theme just slot individually into the next matching
     pillar rotation spot, same as before.
   - Mark each entry consumed `[used YYYY-MM-DD]` in `hermes-opportunities.md` once
     it's placed in the calendar. If an unused entry duplicates a story already told
     in a previous month's calendar (check for it before assuming it's new), mark it
     `[used YYYY-MM-DD — duplicate, not slotted]` instead of giving it a fresh day.
2. Read `context/priorities.md` and `context/about-business.md` for anything currently
   load-bearing (e.g. a CMMC deadline crunch) that should bias which pillar gets
   emphasis that month — don't just round-robin blindly if something's clearly hot.
3. Build 30 per-day blocks in `references/content-calendar.md` — not a flat table.
   Each day: `### Day N — date — Domain — Pillar`, a **Hook** (the headline claim),
   **3 talking points** (the specific things to actually say, in order — concrete
   enough to record or write from without rambling, not a script to read verbatim),
   and a **CTA** line. Alternate domain by day; cycle pillars 1→4→1→4 within each
   domain's run.
4. For any day slot not already filled from `hermes-opportunities.md`, hooks and
   talking points must still be specific enough to use without further research —
   a real claim, number, mistake, or feature name, not "talk about compliance." Pull
   real detail from `context/about-business.md`, `decisions/log.md`, or recent
   repo/commit activity (`git log --oneline -30` across this repo and the
   Sentinel/SEO-agent repos if accessible) rather than generic prompts. If
   `hermes-opportunities.md` is running low (fewer than 3 unused entries per domain),
   say so in the summary — that's the cue to run the `hermes` agent.
5. Show Sean the full set before writing it — this is a planning artifact, not a
   posting action, but still cheap to get wrong for a month if pillars are off.
6. Write the approved set to `references/content-calendar.md`, replacing any
   previous month's content (move the old one to the bottom under a `## Archive`
   heading with its date range — don't delete history).

## Expanding an idea into a draft

Triggered by "expand calendar idea N" or "expand today's idea" or as part of the
weekly `social-post-queue` cadence when the queue runs low (per that skill's step 1).

1. Find the row in `references/content-calendar.md`.
2. Call `POST /api/content-pipeline/generate` on `vulnaguard-seo-agent` with:
   - `rawInput`: the hook + 3 talking points, concatenated
   - `captureMode`: `"type"`
   - `brand`: `"vulnaguard"` for Vulnaguard-pillar rows, `"seanbuilds"` for
     SeanBuilds-pillar rows (keeps the two queues separable in `next-unposted`)
   - `voiceSkillSlug`: `"seans-voice-vulnaguard"` or `"seanbuilds-voice"` to match
   This returns a `content_pipeline_records` row with linkedin/instagram/facebook/
   youtube_desc/youtube_short + a `video_brief` already generated — no separate
   per-platform drafting step needed.
3. Mark the calendar row `[expanded YYYY-MM-DD]` so it's not expanded twice.
4. Show Sean the generated record — same review-before-anything-external rule as
   `social-post-queue`. This skill never posts anything itself.

## What this skill is NOT

- Not a publisher — `social-post-queue` owns posting, this owns ideas only.
- Not a drafting tool itself anymore — `content-pipeline` (vulnaguard-seo-agent) does
  the actual writing now; this skill picks *what* to write about and hands off the
  raw idea.
- Not market-facing — this calendar and its hooks are never shown to anyone outside
  Sean; if an idea is good enough to publish, it gets expanded via content-pipeline first.
- Not a third-domain generator — SeanBuilds and Vulnaguard only, per Sean's explicit
  scope. Mectofitness/BlueAlamo are out of scope unless he says otherwise.

## KPI

Bucket: **more customers** (top-of-funnel, ties to `context/priorities.md` #2/#3).
Metric: **at least 3 unexpanded calendar ideas per domain at all times** — the
calendar's whole job is making sure `social-post-queue` step 1 never has to stall and
ask Sean to think of something on the spot.
