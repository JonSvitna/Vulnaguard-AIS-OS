# Decisions Log

Append-only record of meaningful decisions and why they were made. `/level-up` Phase 2 (Method interview) writes scoped automation specs here. You can also append manually whenever you decide something worth remembering.

**Format per entry:**

```
## YYYY-MM-DD — Short title

**Decision:** what was decided.

**Why:** the reasoning, constraints, and what would change your mind.

**Alternatives considered:** what else was on the table.

**Owner:** who's accountable.
```

Keep it terse. Future-you will thank present-you for capturing the *why*, not just the *what*.

---

## 2026-06-18 — Wire Microsoft 365 via Graph app-only auth, not delegated/MCP

**Decision:** Connected Calendar + mailbox (`seanmurrill@vulnaguard.com`) using a Graph API client-credentials (app-only) flow in a stdlib-only Python script (`scripts/microsoft365_api.py`), instead of an MCP server or delegated OAuth.

**Why:** App-only auth runs unattended (no user sign-in step, no token refresh UI needed) — fits an AIOS that should reach data without Sean re-authenticating. Stdlib-only avoids adding `requests`/`msal` as dependencies for a single script. No MCP server existed for this at the time.

**Alternatives considered:** Delegated OAuth (rejected — needs a human in the loop to refresh); Microsoft Graph MCP server (rejected — adds a dependency for what's currently 3 read/write calls).

**Owner:** Sean.

## 2026-06-18 — Lowered qualifier_min_score 6→4 and pinned qualifier/copywriter to Claude

**Decision:** In `vulnaguard-seo-agent`, dropped `qualifier_min_score` from 6 to 4 and overrode the `qualifier`/`copywriter` agents to use Claude (`claude-sonnet-4-6`) instead of inheriting the OpenAI `gpt-4o` default, via `ai_provider_config`.

**Why:** 728 sales leads from the 2026-06-17 bulk CSV import were stuck at `status='discovered'` — 753 of 920 qualifier calls failed with OpenAI 429 rate-limit errors (30k TPM / 500 RPM tier) during the import, and nothing retried them afterward (no cron/recurring trigger calls `pipeline/run`). Separately, the imported leads are structurally thin — 0/718 have `cmmc_level_sought` or `employee_count`, only 319/718 have `org_type` — so even a working qualifier scores most at ~3/10 against a min score of 6, mostly producing `disqualified`, not outreach. Lowering the threshold to 4 lets thinner-but-plausible leads (named contact + HUBZone/WOSB designation) reach drafting. Safe because sending still requires manual approval (`sequences.status='approved'`, set only via `/api/marketing/approval/approve`) — lowering the qualifier threshold only changes what reaches the review queue, not what gets sent.

**Alternatives considered:** Enriching all 718 leads with missing fields before qualifying (rejected — too slow against the 90-day client-acquisition clock, for an unproven list); leaving the backlog stuck and fixing only future sourcing (rejected — doesn't recover the leads already paid-for/imported).

**Owner:** Sean. Revisit `qualifier_min_score` back up once a higher-quality lead source replaces this CSV batch — 4 is a deliberate, temporary loosening, not the new permanent baseline.

## 2026-06-18 — Personas stored in Postgres, not as markdown files

**Decision:** The marketing-agents persona system (`new-startup-intro`, `cmmc-specialist`) lives in a `personas` DB table in `vulnaguard-seo-agent`, seeded idempotently in `ensureSchema()`, not as `.md` files in a `personas/` folder as an earlier design doc described.

**Why:** The design doc (`docs/superpowers/specs/2026-06-16-bulk-import-personas-ai-provider-design.md`) called for file-based personas, but the actual implementation pivoted to DB-backed storage — found while trying to locate `vulnaguard-marketing-agents/personas/new-startup-intro.md`, which doesn't exist anywhere on disk. The DB seed already matches the spec's intended content.

**Alternatives considered:** Creating the file-based persona doc as originally specced (rejected — would diverge from what the running app actually reads).

**Owner:** Sean.

## 2026-06-19 — Lead-triage run failed: M365 auth env vars missing

Scheduled lead-triage run failed before pulling mail — `scripts/microsoft365_api.py` errored with `KeyError: 'MS365_USER_UPN'` (consistent with the SessionStart hook's `MS365_TENANT_ID` warning); no leads pulled, `leads/inbox.md` untouched. Not retried.
