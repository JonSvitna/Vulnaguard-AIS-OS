---
name: social-post-queue
description: Pull the next unposted draft from vulnaguard-seo-agent's content-pipeline (already generated per-platform), show Sean for review/edit, then queue to Buffer (Facebook/Instagram/LinkedIn) or hand off to IndieHackers manually. Use for "post to social", "what's next in the content queue", "queue this week's posts", "post to IndieHackers", or as a standing cadence to hit 5 posts/week minimum.
bike-method-phase: 1
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

> *Phase 1 — Training wheels. Run manually first. Advance phase only by explicit edit.*

## What this skill does

Closes the gap between "drafts exist in `content-bank.md`" and "posts actually go out" —
the most disliked recurring task on record (see `context/about-me.md`), currently stuck
at zero `[posted]` entries despite 5+ drafts sitting ready.

Target cadence: **5 posts/week minimum**, across Facebook, Instagram, and LinkedIn,
via Buffer (see `references/buffer-api.md` — Buffer is the broker so this skill never
needs direct Meta/LinkedIn API access).

Also drafts for **IndieHackers** on a weekly cadence (separate from the 5/week social
quota — IndieHackers has no posting API, so this branch stops at a reviewed draft and
hands off to Sean for manual copy/paste/submit).

## What this skill is NOT

- Not an auto-publisher. Sean reviews and edits every post before it's queued — this is
  a hard rule from `AGENTS.md` ("don't fake my voice on external content... without
  showing me a draft first"), not a preference. Autonomy level is locked at L2 (Drafted).
- Not a drafting-from-scratch tool by default. It pulls from the existing content bank
  first; only writes new drafts (via `seanbuilds-voice`) once the bank runs low.

## Execution

1. **`GET /api/content-pipeline/next-unposted?brand=<vulnaguard|seanbuilds>` on
   vulnaguard-seo-agent.** Call it once per domain — this returns the oldest record still
   missing at least one of linkedin/facebook/instagram. If it returns `record: null` for a
   domain, that domain's queue is dry — trigger `content-calendar`'s "expand an idea" step
   for that domain before continuing.
2. **The per-platform variants are already generated** (`record.linkedin`,
   `record.instagram`, `record.facebook`) — no adapting step needed here anymore. For
   Instagram, if the post needs a graphic, hand off to Creative OS
   (`~/Documents/GitHub/creative-os`) to produce the asset from `record.video_brief` or the
   post copy, then bring the result back here to attach before queuing.
3. **Show Sean all three platform variants together.** Wait for explicit approval or edits
   before continuing. Do not queue anything unapproved.
4. **Queue approved posts into Buffer:**
   ```
   python3 scripts/buffer_api.py queue --profile-id $BUFFER_PROFILE_ID_<PLATFORM> --text "<approved text>"
   ```
   If `record.recommended_post_window` is set (populated by the Content Intake
   Pipeline's playbook lookup — see `references/content-intake-pipeline.md`), use it
   for `--scheduled-at` instead of even weekly spacing. Otherwise, space posts across
   the week to land on different days and hit the 5/week cadence evenly, not in a burst.
5. **Mark each queued platform posted** via `PATCH /api/content-pipeline/<record.id>/posted`
   with `{ "platform": "linkedin" | "facebook" | "instagram", "postedAt": "<ISO timestamp>" }`
   — one call per platform, right after that platform's Buffer queue call succeeds.
6. **Log progress** — if this closes out a week's 5-post quota, note it in `decisions/log.md`
   only if something changed about the approach; routine weeks don't need a log entry.

### IndieHackers branch (weekly, separate from the steps above)

1. **Pick a record suited to IndieHackers' audience** from recent `content-pipeline`
   history (`GET /api/content-pipeline/generate` history endpoint, or ask Creative
   for the recent list) — build-in-public, technical, lessons-learned. Not every
   record qualifies; generic promo content doesn't fit this audience and should be
   skipped rather than forced.
2. **Rewrite into IndieHackers' register** (one AI step): longer-form, conversational,
   build-log voice — no hashtags, no CTA-style social copy. This is a different register
   from the Facebook/Instagram/LinkedIn variants `content-pipeline` already generated,
   not a trim of them.
3. **Show Sean the draft.** Wait for explicit approval or edits.
4. **Hand off — do not attempt to post it.** IndieHackers has no posting API. Once
   approved, tell Sean the draft is ready for him to copy, paste, and submit manually.
5. **Mark it posted** via `PATCH /api/content-pipeline/<record.id>/posted` with
   `{ "platform": "indiehackers", "postedAt": "<ISO timestamp>" }` once Sean confirms
   he's posted it (separate field from the Buffer-platform tracking, since the same
   record can run on both tracks independently).

## Setup required before first real run

`BUFFER_ACCESS_TOKEN` and the three `BUFFER_PROFILE_ID_*` vars in `.env` must be filled in
(Sean connects Facebook/Instagram/LinkedIn inside Buffer's own UI first, then pulls profile
IDs via `python3 scripts/buffer_api.py profiles`). Until then, this skill can still draft and
get approval — it just can't execute the queue step.

## KPI

Bucket: **more customers** (top-of-funnel traffic, ties to `context/priorities.md` #3).
Metric: **posts/week sustained at ≥5** (Buffer platforms).

IndieHackers branch tracks separately — bucket: **more customers** (outreach/brand
awareness, ties to `context/priorities.md` #2). Metric: **IndieHackers posts/week**
(proxy metric for now; revisit once seanbuilds.com has its own domain and signup
tracking, so this can trace to actual signups instead of post count).
