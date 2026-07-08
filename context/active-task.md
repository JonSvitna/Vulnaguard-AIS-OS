# Active task

Updated whenever Sean switches coding agents mid-task (Claude Code ↔ Codex ↔ Cursor) so the next agent can pick up cold. If this file says "none," there's nothing in flight — read CLAUDE.md and proceed normally.

**Status:** in progress
**Switched from:** Codex → Cursor (manual switch)
**Updated:** 2026-07-01

## Cross-agent reminder (Content Intelligence)

- If resuming Stage 3 in Claude environment, start with references/content-intelligence-return-setup.md.
- Main pipeline spec: references/content-intelligence-pipeline.md.
- Stage 3 contract: references/content-intelligence-stage3-contract.md.
- Workflow scaffold: references/n8n/workflows/content-intelligence-pipeline-v1.json.
- Schema draft: references/sql/content-intelligence-pipeline.sql.

## What we're doing

SAM.gov contract scanner hardening + gov lead strategy. Scanner fixes done. USASpending scraper refocused on **small contract reverse-engineering** — individual awards in the $5k–$100k range that a startup could replicate to build past performance (not big-prime awardee lists).

## Done so far

- **Rate limiting added** (`scripts/sam_gov_api.py:184`): `time.sleep(3)` before every API call — scanner was bursting 21 requests with no delay, triggering the SAM.gov IP block
- **Dry-run bug fixed**: contacts CSV and seen-IDs cache were being written even with `--dry-run`. Now fully read-only in dry-run mode (`scripts/sam_gov_api.py:537-575`)
- **Scoring tightened** (`scripts/sam_gov_api.py:262`): NAICS code alone no longer clears the threshold — opportunity must have cyber keywords in the title OR be PSC D310 (Cyber Security). Previously any DoD contract with NAICS 541512 scored 40, pulling in rubber gaskets, engines, janitorial services, etc.
- **CSV deduped and cleaned** (`leads/sam_gov_contacts.csv`): was 221 rows of mostly hardware procurement contacts → now 1 row (effectively empty/reset). Will rebuild clean with new scoring rules.
- **Slack bot confirmed working**: bot is a member of `#gov-contracts` (channel ID `C0BF5NSMMCY`), `.env` has correct `SLACK_GOV_CONTRACTS_CHANNEL` value. First scan ran at 2:40 UTC before the bot was in the channel, which is why no messages appeared.
- **Strategic decision made**: gov POC contacts from SAM.gov are NOT the right outreach targets for Sentinel CMMC. They're Contracting Officers, not defense contractors needing certification. The play for Sentinel CMMC prospects is USASpending.gov awardee data (who won cybersecurity contracts).
- **USASpending scraper refocused** (`scripts/usaspending_api.py`): default mode finds individual small awards ($5k–$100k) with cyber service descriptions — reverse-engineer what agencies bought and who won. Output: `leads/usaspending_opportunities.csv`. First run: 92 opportunities (all agencies, 12mo lookback). `--mode companies` kept for legacy big-awardee view.

## Next step

1. Review `leads/usaspending_opportunities.csv` — filter `replicability=high`, pick 5–10 awards Sean could actually deliver. Cross-reference awardees (who won similar work) and agencies (who's buying).
2. When SAM.gov IP block clears, run opportunity scanner for active solicitations (complements spending data — what's being bought vs. what's open now).
```
python3 scripts/sam_gov_api.py --reset
python3 scripts/sam_gov_api.py --dry-run --days 7
```
Confirm cyber-relevant titles, then run live for Slack `#gov-contracts` monitoring (separate from awardee outreach).

## Key files

- `scripts/sam_gov_api.py` — opportunity scanner (Slack alerts, not outreach targets)
- `scripts/usaspending_api.py` — small contract opportunity reverse-engineering (default)
- `leads/usaspending_opportunities.csv` — individual awards to replicate
- `leads/usaspending_awardees.csv` — legacy big-company list (`--mode companies`)
- `leads/sam_gov_contacts.csv` — contracting officer POCs (monitoring only, not for blast outreach)
- `leads/sam_gov_seen.json` — SAM.gov seen-IDs cache; run `--reset` before first post-fix scan

## Watch out for

- SAM.gov API is currently unreachable (TLS handshake timeout from IP block). Do NOT try to run the scanner yet.
- USASpending default mode is **award-level** (what work got bought), not company totals. Use `replicability` column: `high` = services you could bid, `intel_only` = software/license buys.
- `sam_gov_contacts.csv` POCs are contracting officers — separate from this play.

<!--
Template for an in-flight task:

**Status:** in progress
**Switched from:** Claude Code → Codex (hit usage limit)
**Updated:** 2026-06-19 14:30

## What we're doing
One or two sentences on the goal.

## Done so far
- Bullet list of concrete completed steps, with file paths.

## Next step
The single next action to take. Be specific — file, function, what to change.

## Key files
- path/to/file.ts — why it matters
- path/to/other.py — why it matters

## Watch out for
Anything non-obvious the next agent would otherwise rediscover the hard way.
-->
