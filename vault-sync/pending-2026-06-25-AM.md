# Pending vault updates — 2026-06-25 AM

Staged by the morning vault-sync check, covering commits since the last note (`a4e201b`, archived in `4c7b28f`).

- **`vulnaguard-website-creation-tool` Phase 1 closed out — website-dev product line now has all four planned AI capabilities shipped.** Logged in `decisions/log.md` (2026-06-24, commit `b0338d1`): image generation/editing (`lib/image-client.ts`, OpenAI `gpt-image-1`) was the last of the four Phase 1 capabilities (code suggestions, design suggestions, token iteration, image gen) — closes Phase 1 as scoped on 2026-06-24. Verified end-to-end against the real OpenAI API, not just type-checked.
  - Supporting feature work same day, also worth noting if this gets a vault page: first real in-app page (`/project/[id]`, design history timeline) and the tool's own UI skinned with SeanBuilds brand tokens (`decisions/log.md` commits in `b0338d1`/`4c7b28f`).
  - This is the first concrete deliverable for the **client website dev** line (one of the three active business lines) — worth a `wiki/domains/` page or an update to wherever the website-creation-tool scaffolding (already staged in the prior PM note) landed.

- **Flag, not yet resolved:** `decisions/log.md` has a contradiction worth checking before this propagates anywhere. Commit `a47a357` (22:11 EDT, 6/24) deployed the mail-to-Slack poller as a **Railway cron job** (`railway.json` is live in the repo right now, confirmed at HEAD). Commit `b0628bb` (22:56 EDT, same night) then logged a *different* decision claiming the poller was deployed on the **DigitalOcean droplet instead, explicitly rejecting Railway** as redundant. Both can't be true — worth a quick check on which one is actually running before this matters for lead-routing reliability (the SEO agent's mail-to-lead path depends on this poller).

No new leads in `leads/inbox.md` since the last sync (all rows still dated 2026-06-20), and no `context/` changes in this window.
