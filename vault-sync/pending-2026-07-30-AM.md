# Pending vault updates — 2026-07-30 AM

**Coverage window:** Since `pending-2026-07-29-AM.md` — commits `68f74f4`, `3502bbc`, `803a469` (2026-07-29 evening through 2026-07-30 AM UTC).

---

## BLOCKING: decisions/log.md has an unresolved merge conflict

Commit `68f74f4` (Sean, 00:43 today) left a raw `<<<<<<< / =======/ >>>>>>>` conflict in `decisions/log.md`. The file is currently broken — automated appends will corrupt it further. **Resolve manually before the next scheduled run.**

The two conflicting entries are:
- `Updated upstream` side: Lead triage failed (day 4) — already in yesterday's note.
- `Stashed changes` side: STOP-reply false-positive bug fixed in vulnaguard-seo-agent (see item 1 below).

---

## New items to consider for Obsidian

### 1. STOP-reply false-positive bug fixed in vulnaguard-seo-agent — 2026-07-29
- **What happened:** `checkStopReplies` (`lib/check-stop-replies.ts`) polled Sean's real working mailbox and never flipped a lead out of `sent` status on a real reply — so 747 leads sat in `sent` forever, getting rescanned on every run. Ordinary words in live conversations eventually matched the STOP regex, silently auto-unsubscribing active prospects, emailing them an unwanted "removed from outreach" notice, and flooding Slack.
- **Fix deployed:** Now only leads still in pure `sent` status are evaluated; the first non-STOP reply flips to `replied` so the thread is never rescanned again. Pushed to `main`, Railway auto-deployed. Verified a same-day legitimate unsubscribe (Hillcrest Pharmacy & Compounding of Elkton) had processed correctly before the fix.
- **Why vault-relevant:** Active prospects were damaged by an outreach system error. Business-level context for the SEO pipeline's reliability.
- **Source:** `decisions/log.md` (stash side of conflict), commit `68f74f4` (Sean), vulnaguard-seo-agent commit `78a77aa`.
- **Vault target:** `wiki/decisions/` or `wiki/domains/seo-agent/`.

### 2. Hermes flagged the stop-word bug as a content opportunity
- Hermes staged `references/hermes-pending/pending-2026-07-30-1785383624076.md` — pitching the bug-and-fix story as a "lesson from a mistake" pillar piece for SeanBuilds.
- Run `/hermes` to review and decide whether to merge it into `references/hermes-opportunities.md`.
- **Vault target:** Not needed unless you want to track SeanBuilds content strategy there.

### 3. Lead triage failing — day 5 (2026-07-30)
- Same `KeyError: 'MS365_USER_UPN'` failure. **Fifth consecutive day.** No solicitation emails have been reviewed since 2026-07-20.
- Fix: set `MS365_TENANT_ID`, `MS365_USER_UPN`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET` in Claude Code on the web environment settings.
- **Vault target:** None — tracking already in `decisions/log.md`. Mirror only if you want a "persistent blocker" note in the vault.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **SeanBuilds site: real lead capture live** — Resend Audiences wired, all dead-end CTAs converted to inquiry modal. Commit `6e196f7` (2026-07-24). Vault target: `wiki/domains/seanbuilds/`.
- **SeanBuilds "AI Won't Replace You" — first social batch live** — LinkedIn + Instagram + YouTube Shorts. Brand/content milestone. Commit `ce606a5`. Vault target: `wiki/decisions/` or `wiki/domains/seanbuilds/`.
- **Clay → n8n → SEO agent cutover / Origami now owns Vulnaguard B2B pipeline** — outreach architecture change. Commits `5fe4c6d`, `42a2ac1`, `28f0063` (2026-07-21); `connections.md` row 21 added 2026-07-23. Vault target: `wiki/decisions/`.
- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut. Commit `74deeb5`. Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning. Commit `4b0197e`. Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-30 AM. Next check: 2026-07-31 AM.*
