# Origami: Vulnaguard's B2B Sourcing + Outreach Pipeline

Updated: 2026-07-23

## Why

Clay was cut over 2026-07-21 to source Vulnaguard's commercial B2B leads,
feeding `vulnaguard-seo-agent`'s draft/approve/send pipeline. Two days
later Sean started using Origami.chat instead and, after evaluating it,
decided Origami should own the **whole loop** for Vulnaguard — sourcing,
enrichment, campaign drafting, and sending — not just sourcing into SEO
Agent. Clay's trial stays active and wired, but only for a separate
business (property skip-tracing, different repo — out of scope here).
`vulnaguard-seo-agent` and Clay are untouched and still fully live for
that use.

An earlier version of this doc had Origami feeding SEO Agent's intake
endpoint (mirroring Clay's old role, source-generalized SEO Agent code —
see `decisions/log.md` 2026-07-23). That's superseded: the n8n workflow
built for it (`Origami Lead Intake to SEO Agent`) was deleted. SEO Agent's
`source` generalization was left in place (harmless, tested) in case a
future source ever needs it, but nothing currently uses it for Vulnaguard.

## Why not run both SEO Agent and Origami sending on the same leads

Origami has its own native campaign/send feature (`create-campaign` /
`launch-campaign`), not just sourcing. Routing Origami leads into SEO
Agent's Resend pipeline *and* letting Origami's own campaigns run would
risk double-emailing the same prospects from two systems with two
different voices, no shared suppression list. Decision: Origami owns
outreach for Vulnaguard end to end; SEO Agent's send path stays reserved
for Brickline leads via Clay.

## Architecture (all inside Origami, no n8n)

1. **Source + enrich** — an Origami agent (`POST /agents` or a scheduled
   agent) works a table from a plain-English ICP brief. Live example:
   agent id `2a6afd7a-cf30-45e7-895e-5d498bafaa4f`, table "Vulnaguard
   Prospects" (id `5f5e3528-01d0-47d2-8ea7-87dcdcde1dd5`). First run
   (2026-07-23): 30 candidate rows, 12 qualified (5 compliance_cmmc, 4
   cybersecurity, 3 systems_automation, 0 website_design — website_design
   is deliberately excluded from the brief, it's already covered by the
   AIOS's own yellowpages-based `website-design-lead-finder`).
2. **Draft a campaign** — `POST /tables/{tableId}/campaigns` with a
   free-form `instructions` string. This only drafts — it never sends.
   Voice is injected here (see below).
3. **Human review** — Sean reviews the drafted sequences in Origami's UI
   (`GET /tables/{tableId}/campaigns`, or the workspace URL). Nothing
   sends until an explicit `launch-campaign` call.
4. **Launch** — `POST /campaigns/{id}/launch` (alias `/send`). Runs a
   "sender gate" check; blocked with `missingChannels` if no sending
   mailbox/LinkedIn account is connected for that channel. **This is a
   manual, human step for now** — nothing built here calls `launch`.

## Real cell schema (confirmed live, 2026-07-23)

Table rows use generic `cells` keyed by column slug, not fixed field
names:

| Slug | Shape |
| --- | --- |
| `company-name` | scalar string |
| `domain` | scalar string |
| `location` | scalar `"City, State"` |
| `decision-maker` | `{ first_name, last_name, title, reasoning, linkedin_url }` or fields null |
| `email` | `{ email, reasoning }` — `email` can be null (not verified) |
| `best-fit-service` | `{ service, fit_score, fit_reason, reasoning, confidence, source_url }` — `service`/`fit_score` null when excluded (e.g. Fortune 1000) |
| `score` | the built-in score column — **left null by the agent**, real fit score lives in `best-fit-service.value.fit_score` instead |

A data-quality flag from the first run: one decision-maker resolved as
"John Johnny" — an obvious scraping artifact. Spot-check drafts before
trusting volume, same discipline Clay's rollout used (see
`decisions/log.md` 2026-07-19 entries on ICP/volume ramp).

## Voice

Campaign `instructions` are built from `references/vulnaguard-bd-voice.md`
(Vulnaguard's existing cold/BD email voice doc — opening formula, tone
rules, calibration table, self-check list) plus channel-specific rules:
email under 150 words, no em dashes/buzzwords, tailored per
`best-fit-service` (CMMC framing only for compliance_cmmc rows, etc.);
LinkedIn touches are shorter and connection-request-first — the
connection note itself carries no pitch, only a specific one-line reason
tied to the company.

## Scheduling

Origami supports native scheduled agents (`create-scheduled-agent`,
account has `canRunScheduledTasks: true`) — no n8n hop needed. **Not yet
enabled.** Per Sean's own volume-ramp discipline with Clay, run a few more
manual rounds and spot-check quality (see the "John Johnny" flag above)
before automating a daily unattended schedule. When enabled, the
scheduled brief should source + draft only, and must never call `launch`.

## Blocking prerequisite — Sean's manual step

`launch-campaign` needs a connected sending mailbox **and** a connected
LinkedIn account (Sean chose email + LinkedIn) inside Origami's own
dashboard settings (origami.chat) — there is no API to do this, it's an
OAuth-style connection only Sean can complete. Until both are connected,
drafts can be created and reviewed, but nothing can actually send.

## Account

Org "Vulnaguard", Starter plan (`plan_29_monthly`), API key stored as an
n8n credential (bearer auth, scoped to `origami.chat` only — id
`5CNVRzJWxv5U3YnN`, name "Origami API") even though nothing in n8n calls
it yet; kept there since it's the same pattern Clay's secrets used and
it's readily available if a Slack-notify or approval layer gets added
later.

## Status — 2026-07-23

- [x] Agent/table built and sourcing proven live (12 qualified leads)
- [x] Campaign draft created and completed: "Vulnaguard Defense & Ops Outreach" (id `b3279d11-d956-4ba7-b93d-d841a487f70b`, slug `vulnaguard-defense-ops-outreach-shaky-crimson-owl`), status `draft`, 12 leads / 4-step sequences each (email → email +3d → LinkedIn connect → LinkedIn DM). Spot-checked one full sequence against `references/vulnaguard-bd-voice.md`'s self-check list — passes (situation-specific opening, no em dashes/banned phrases, under 150 words, low-pressure close, follow-up offers something new rather than "checking in", LinkedIn connect note left blank/no pitch).
- [x] Stale n8n workflow (`Origami Lead Intake to SEO Agent`, posted into SEO Agent) deleted
- [x] Sean connected a sending mailbox in Origami's settings (2026-07-23)
- [ ] Sean connects a LinkedIn account (planned 2026-07-24) — until then, launching this campaign will likely hit the sender-gate `missingChannels` check since every sequence includes LinkedIn steps
- [ ] Sean reviews the full 12-lead draft (one spot-checked above by Claude; not yet reviewed in full by Sean)
- [ ] Launch (manual, human-triggered — not automated). Recommend waiting until LinkedIn is connected to avoid a partial/blocked launch.
- [ ] Minor: `peopleCount` shows 11 vs. 12 total sequences returned by the sequences list — not yet investigated, low priority
- [ ] Scheduled agent for recurring sourcing+drafting (built later, left disabled at first, after a few more manual quality spot-checks — first run already surfaced one data-quality artifact, "John Johnny" as a decision-maker name)
