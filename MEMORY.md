# MEMORY — Live State

Durable working facts about "what's true right now." This is not history — that lives in `decisions/log.md`. When a fact here goes stale, update or remove it. Keep entries short and current.

_Last updated: 2026-07-12_

## Who / What

- **Operator:** Sean Murrill (seanmurrill@gmail.com). Solo developer/entrepreneur. Serious/intense persona is "Jon Svitna."
- **Business:** Vulnaguard LLC. Three active lines — Sentinel CMMC (flagship), the SEO agent (outreach + traffic), client website dev.
- **No paying clients yet.** Landing the first is a Q priority.

## This Quarter's Priorities (90 days)

1. **Ship Sentinel CMMC certification** — hard deadline, driven by a government-agency contract requirement.
2. **Land up to 10 clients** via the SEO platform's automated outreach.
3. **Drive consistent website traffic** via the SEO optimization agent.
- Standing theme: any automation that removes workload is welcome, not limited to the above.

## Active Threads / Open Blockers

- **Svitna (fitness app, separate repo `JonSvitna/Svitna`):** builds, backend live on Railway, Jon Svitna coach voice shipped (2026-06-23). Open next step = live simulator walkthrough (onboarding → coach → missed-day nudge) before an App Store **soft test of 10–20 users**. Push notifications (APNs) and nutrition triggers explicitly deferred.
- **SeanBuilds SMB outreach vs Contract Hunter:** fix is a `microfrontends.json` routing change — PR [JonSvitna/seanbuilds#2](https://github.com/JonSvitna/seanbuilds/pull/2) open, needs Sean's merge (touches live domain routing).
- **Content Intelligence Pipeline (n8n):** live and verified end-to-end Stage 1–4. Stage 1 Tavily seed query needs tuning (surfaced blog/tool pages instead of YouTube channels) before Stage 2 shows real video data.

## Environment / Access State

- **M365 daily brief hook is failing** — `MS365_TENANT_ID` not set in this environment. Fix to restore the SessionStart brief.
- **Stripe: not yet configured** (revenue tier-1 domain not reachable). `references/stripe-api.md` exists; keys + `scripts/stripe_api.py` still needed. Mercury Bank is the invoicing fallback.
- **No task-tracking tool wired** as system of record (Linear reference + MCP exist but not adopted).
- **Remote AIOS:** DigitalOcean droplet `vulnaguard-aios` (NYC1, 143.244.148.90), Claude Code CLI via `tmux attach -t claude`. GitHub `gh` authed as `JonSvitna`.
- **Second brain:** Obsidian vault at `~/Documents/Obsidian Vault` — mirror business-level decisions there, not purely technical ones.

## Standing Preferences

- Voice: casual but professional, short sentences, no em dashes, bullets over paragraphs. Never publish external content in Sean's voice without showing a draft first.
- Documentation is mandatory — nothing is "done" until documented (`references/documentation-standard.md`).
- Default Shift: for any new task, first ask "to what extent could AI be leveraged here?"
