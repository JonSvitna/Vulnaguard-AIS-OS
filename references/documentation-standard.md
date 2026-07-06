# Documentation Standard (Mandatory)

Documentation is not optional. Nothing is "done" until it is documented. This applies to internal AIOS work, delivery process changes, decisions, and every client engagement.

For federal and CMMC work this is not just good practice — the documentation *is* the deliverable, and auditors, contracting officers, and past-performance records all depend on it existing.

Updated: 2026-07-06

---

## The rule

**Definition of Done includes documentation.** A task, decision, tool choice, or engagement step is not complete until its record exists in the right place below. If it isn't written down, it didn't happen.

No exceptions for "small" items. The whole point of a paper trail is that you can't predict which small thing an auditor, a CO, or future-Sean will need to reconstruct.

---

## What gets documented, and where it lives

| What | Where it goes | When |
|---|---|---|
| A decision (product, tooling, client handling, direction) | `decisions/log.md` | At the moment the decision is made |
| Business-level decision (product direction, positioning, client/lead handling) | Also mirror to the Obsidian vault `wiki/decisions/` | Same session |
| Delivery process / methodology / tooling standards | `playbook/` (the runbook or `methodology/` file it belongs to) | When the process is set or changed |
| Progress on a multi-step initiative | The initiative's progress log in `references/` (e.g. `references/gov-contract-progress-log.md`) | As each item completes |
| In-flight task handoff (switching agents mid-task) | `context/active-task.md` | When work is paused or handed off |
| Client engagement work, evidence, deliverables | `playbook/engagements/{client-slug}/` | Throughout the engagement |
| Outreach sent | `references/outreach-log.md` | When outreach goes out |

If a piece of work spans two of these, it gets recorded in each relevant place. A tooling decision, for example, lands in both `decisions/log.md` (the decision) and the `playbook/` standard it changes.

---

## Standard for a good record

Every entry answers, at minimum:

- **What** was done or decided.
- **Why** — the reasoning, so future-you doesn't relitigate it.
- **When** — the date.
- **Where** — file paths touched, so the record is traceable.
- For decisions: **alternatives considered** and the **owner**.

Follow the existing `decisions/log.md` entry format — it already models this well.

---

## Client engagement documentation (federal / CMMC — non-negotiable)

For any client-facing assessment or compliance engagement, the following must exist and be retained per the playbook's Data Handling rules:

- Signed SOW, MSA, and Rules of Engagement **before** any billable or technical work begins.
- Scope confirmed in writing (authorized IP ranges / URLs, testing window).
- Raw scanner output preserved, unmodified, with scanner version and plugin/update date recorded.
- Evidence for every Critical/High finding, referenced by exhibit/filename in the technical report.
- Findings mapped to the relevant control framework (NIST 800-171 / 800-53 / CMMC).
- Deliverables (Technical Report, Executive Summary, POA&M as applicable) in the engagement folder.
- Closeout record and, where requested, documented data destruction.

Engagement artifacts are retained for **3 years post-closeout** (see `playbook/methodology/technical-standards.md` → Data Handling).

This is what turns each small win into documented past performance — the asset that unlocks the next, larger contract.

---

## How the AIOS enforces this

When any task in this repo is completed, the corresponding record above is created or updated **in the same session, as part of the task** — not deferred, not left for later. Treat "and document it" as an implicit final step of every request, whether or not it was spelled out.
