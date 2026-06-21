---
name: social-post-queue
description: Pull the next unposted draft from references/content-bank.md, adapt it per platform (Facebook/Instagram/LinkedIn), show Sean for review/edit, then queue the approved version into Buffer. Use for "post to social", "what's next in the content queue", "queue this week's posts", or as a standing cadence to hit 5 posts/week minimum.
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

## What this skill is NOT

- Not an auto-publisher. Sean reviews and edits every post before it's queued — this is
  a hard rule from `CLAUDE.md` ("don't fake my voice on external content... without
  showing me a draft first"), not a preference. Autonomy level is locked at L2 (Drafted).
- Not a drafting-from-scratch tool by default. It pulls from the existing content bank
  first; only writes new drafts (via `seanbuilds-voice`) once the bank runs low.

## Execution

1. **Read `references/content-bank.md`.** Find the next entry without a `[posted YYYY-MM-DD]` tag.
   If the bank has fewer than 3 unposted drafts left, flag it and offer to write more
   via the `seanbuilds-voice` skill before continuing.
2. **Adapt per platform** (one AI step — this is the only judgment call in the pipeline):
   - LinkedIn: post as-is, long-form is fine.
   - Facebook: trim to ~2-3 sentences + CTA.
   - Instagram: trim to caption length, and call out that an image/graphic is needed
     (this skill doesn't generate images — flag it, don't silently skip Instagram).
3. **Show Sean all three platform variants together.** Wait for explicit approval or edits
   before continuing. Do not queue anything unapproved.
4. **Queue approved posts into Buffer:**
   ```
   python3 scripts/buffer_api.py queue --profile-id $BUFFER_PROFILE_ID_<PLATFORM> --text "<approved text>"
   ```
   Use `--scheduled-at` to spread posts across the week rather than dumping all 5 at once —
   space them to land on different days to hit the 5/week cadence evenly, not in a burst.
5. **Mark the source draft `[posted YYYY-MM-DD]`** in `content-bank.md` once all platform
   variants for it are queued.
6. **Log progress** — if this closes out a week's 5-post quota, note it in `decisions/log.md`
   only if something changed about the approach; routine weeks don't need a log entry.

## Setup required before first real run

`BUFFER_ACCESS_TOKEN` and the three `BUFFER_PROFILE_ID_*` vars in `.env` must be filled in
(Sean connects Facebook/Instagram/LinkedIn inside Buffer's own UI first, then pulls profile
IDs via `python3 scripts/buffer_api.py profiles`). Until then, this skill can still draft and
get approval — it just can't execute the queue step.

## KPI

Bucket: **more customers** (top-of-funnel traffic, ties to `context/priorities.md` #3).
Metric: **posts/week sustained at ≥5.** Revisit later whether GSC referral data shows
this channel actually driving site traffic, once volume is steady — that's a follow-on
check, not part of this build.
