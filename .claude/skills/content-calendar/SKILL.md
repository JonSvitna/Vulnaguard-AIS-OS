---
name: content-calendar
description: Generate and maintain a 30-day content idea calendar across SeanBuilds and Vulnaguard, then expand picked ideas into full drafts for content-bank.md. Use for "build my content calendar", "generate this month's content ideas", "what should I post about", "expand calendar idea N", or "regenerate the calendar".
---

> Personal accountability tool. Not for sale, not client-facing. Two domains only: **SeanBuilds** and **Vulnaguard**.

## What this closes

Sean's recurring blocker: drafts exist in `references/content-bank.md` and `social-post-queue`
posts them, but nothing generates *what to write about* on a schedule — so the bank runs dry
and posting stalls on "I don't know what to talk about today." This skill is the idea engine
that feeds the bank; `social-post-queue` remains the only thing that actually posts.

```
content-calendar  →  references/content-calendar.md (30 days of one-line hooks)
       │ expand picked rows
       ▼
references/content-bank.md (full drafts, seanbuilds-voice)
       │
       ▼
social-post-queue (per-platform adapt → Buffer / IndieHackers)
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

## CTA rule (non-negotiable, per CLAUDE.md)

Every row in the calendar AND every expanded draft must name a CTA. Fixed per domain,
not improvised per post:

- **Vulnaguard** → `vulnaguard.com` (point people at the site; use a specific path
  instead of the root only if Sean gives one for that post)
- **SeanBuilds** → soft CTA — "comment '<keyword>'" or "DM me" (no live landing
  page yet; do not invent one)

## Generating the calendar

1. Read `context/priorities.md` and `context/about-business.md` for anything currently
   load-bearing (e.g. a CMMC deadline crunch) that should bias which pillar gets
   emphasis that month — don't just round-robin blindly if something's clearly hot.
2. Build a 30-row table in `references/content-calendar.md`: Day | Domain | Pillar |
   Hook (one line, specific, in Sean's actual voice/register — see `seanbuilds-voice`)
   | CTA. Alternate domain by day; cycle pillars 1→4→1→4 within each domain's run.
3. Hooks must be specific enough to write from without further research — a real
   claim, number, mistake, or feature name, not "talk about compliance." Pull real
   detail from `context/about-business.md`, `decisions/log.md`, or recent repo/commit
   activity (`git log --oneline -30` across this repo and the Sentinel/SEO-agent repos
   if accessible) rather than generic prompts.
4. Show Sean the full table before writing it — this is a planning artifact, not a
   posting action, but still cheap to get wrong for a month if pillars are off.
5. Write the approved table to `references/content-calendar.md`, replacing any
   previous month's table (move the old one to the bottom under a `## Archive`
   heading with its date range — don't delete history).

## Expanding an idea into a draft

Triggered by "expand calendar idea N" or "expand today's idea" or as part of the
weekly `social-post-queue` cadence when the bank runs low (per that skill's step 1).

1. Find the row in `references/content-calendar.md`.
2. Write the full draft via the `seanbuilds-voice` register — same length/style as
   existing `content-bank.md` entries (one paragraph + a `CTA:` line).
3. Append it to the correct domain section in `content-bank.md` (create the section
   if needed — currently the bank's sections are Vulnaguard/Sentinel CMMC, Web Dev,
   SEO Agent, Builder Philosophy; map SeanBuilds pillars to "Builder Philosophy" and
   Vulnaguard pillars to "Vulnaguard/Sentinel CMMC" or "SEO Agent" by content).
4. Mark the calendar row `[expanded YYYY-MM-DD]` so it's not expanded twice.
5. Show Sean the draft — same review-before-anything-external rule as
   `social-post-queue`. This skill never posts anything itself.

## What this skill is NOT

- Not a publisher — `social-post-queue` owns posting, this owns ideas only.
- Not market-facing — this calendar and its hooks are never shown to anyone outside
  Sean; if an idea is good enough to publish, it gets expanded into the bank first.
- Not a third-domain generator — SeanBuilds and Vulnaguard only, per Sean's explicit
  scope. Mectofitness/BlueAlamo are out of scope unless he says otherwise.

## KPI

Bucket: **more customers** (top-of-funnel, ties to `context/priorities.md` #2/#3).
Metric: **bank never runs below 3 unexpanded ideas per domain** — the calendar's whole
job is making sure `social-post-queue` step 1 never has to stall and ask Sean to think
of something on the spot.
