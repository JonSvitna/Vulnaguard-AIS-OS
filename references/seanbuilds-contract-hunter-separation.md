# SeanBuilds ↔ Contract Hunter Separation Playbook

**Date:** 2026-07-09
**Status:** Diagnosis complete, fix pending (Sean executing on his Mac)
**Owner:** Sean

Two distinct products got tangled. This is the map for pulling them apart so the SMB
outreach site can launch cleanly at `officialseanbuilds.com/outreach`.

---

## The two products (must stay distinct)

| Product | Repo | What it is | Brand / domain |
|---|---|---|---|
| **Contract Hunter** | `JonSvitna/Contract-Hunter` | "Local Contract Hunter AI" — gov-contract discovery (EMMA / SAM.gov / CivicEngage scrapers, opportunity scoring, dashboard). FastAPI backend + Next.js frontend. Railway app `contract-hunter-production`. | **Vulnaguard LLC** |
| **SMB Outreach** | `JonSvitna/vulnaguard-smb-automation` | SMB outreach tool — its own landing page. | **SeanBuilds** → `officialseanbuilds.com/outreach` |

These are different products, different brands, different domains. The SMB outreach site
is **not** a page inside Contract Hunter, and Contract Hunter is **not** a page under
SeanBuilds.

---

## Diagnosis (verified 2026-07-09)

`JonSvitna/Contract-Hunter` was cloned and inspected end to end. **It is clean.** Every
tracked file was grepped for `smb`, `outreach`, `officialseanbuilds`, `seanbuilds`, `n8n`
— **zero hits.** Its frontend metadata reads "Local Contract Hunter AI / Vulnaguard LLC,"
there is no `/outreach` route, and no SeanBuilds branding anywhere.

**Conclusion:** there is nothing SeanBuilds/SMB to remove *from* Contract Hunter's git.
The mess lives on the SMB side. Symptom reported by Sean: hitting
`officialseanbuilds.com/outreach` loads a **broken/wrong SMB page** — i.e. Contract Hunter
code/pieces got copied *into* `vulnaguard-smb-automation`, so the SMB repo is the one that
needs cleaning.

> Note: `local_contract_hunter.db` (~248 KB SQLite) is committed in Contract-Hunter even
> though `.gitignore` lists it — it was force-added at some point. Unrelated to this
> separation, but worth `git rm --cached` later so the DB isn't tracked.

---

## Contract-Hunter signature — anything matching this inside the SMB repo is the blend

Clean Contract-Hunter layout (this is what should **not** appear in the SMB repo):

```
Contract-Hunter/
  local-contract-hunter-ai/
    backend/            # FastAPI: app/main.py, app/routes/*, app/scrapers/*, app/services/*
    frontend/           # Next.js: app/page.tsx (title "Local Maryland Contract Intelligence")
    config/             # sources.yaml, keywords.yaml, scoring_rules.yaml, scheduler.yaml
    docs/
  docs/superpowers/
  local_contract_hunter.db
  railway.json          # startCommand: uvicorn app.main:app (cd local-contract-hunter-ai/backend)
  nixpacks.toml
  requirements.txt
```

Distinctive strings to grep for in the SMB repo — each hit is Contract-Hunter code that
does not belong there:

- `local-contract-hunter-ai`
- `Local Contract Hunter AI`
- `Local Maryland Contract Intelligence`
- `local_contract_hunter.db`
- `emma_scraper` / `samgov_scraper` / `civicengage_bid_scraper`
- `app.main:app` (Contract Hunter's uvicorn entrypoint)
- `Vulnaguard LLC` (as a page/brand header — SMB site is SeanBuilds-branded)

---

## Separation steps (run on the Mac, where you have repo access)

### 1. Get both repos locally

```bash
git clone https://github.com/JonSvitna/vulnaguard-smb-automation.git
git clone https://github.com/JonSvitna/Contract-Hunter.git   # reference for what to strip
cd vulnaguard-smb-automation
git checkout -b claude/sean-builds-contract-hunter-separation   # work on a branch
```

### 2. Find the blend

```bash
# From inside vulnaguard-smb-automation:
grep -rniE 'local-contract-hunter-ai|Local Contract Hunter|local_contract_hunter\.db|emma_scraper|samgov_scraper|civicengage|app\.main:app|Vulnaguard LLC' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git .

# Also list top-level dirs — a stray `local-contract-hunter-ai/` or a whole backend/
# scraper tree that belongs to Contract Hunter is the giveaway.
git ls-files | awk -F/ '{print $1"/"$2}' | sort -u
```

### 3. Remove the Contract-Hunter pieces from the SMB repo

For each file/dir the grep flags as Contract-Hunter:

```bash
git rm -r <path-that-belongs-to-contract-hunter>
```

Keep only what the SMB outreach landing page actually needs. If unsure whether a file is
SMB's or Contract-Hunter's: if the identical file exists in the `Contract-Hunter` clone,
it's Contract-Hunter's — remove it from the SMB repo.

### 4. Confirm the SMB repo is a standalone landing page

The SMB repo should build and serve **only** the SeanBuilds SMB outreach landing page.
After removal:

```bash
grep -rniE 'contract.?hunter|local_contract_hunter|emma_scraper|samgov' . \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git
# → expect ZERO hits. If any remain, they're still blended.
```

Update branding so it reads SeanBuilds, not Vulnaguard/Contract Hunter (page `<title>`,
header, metadata).

### 5. Wire the `/outreach` path under officialseanbuilds.com

The SMB site is its own landing page served at `officialseanbuilds.com/outreach`. Two ways:

- **basePath (cleanest if it's a standalone Next.js app on its own deployment):** in
  `next.config.mjs` set `basePath: '/outreach'` so all routes/assets resolve under
  `/outreach`, then point the `officialseanbuilds.com` domain's `/outreach` at this
  deployment (Vercel domain + rewrite/path, or a reverse proxy).
- **Rewrite from the main SeanBuilds site:** if `officialseanbuilds.com` is one main
  deployment, add a rewrite so `/outreach` (and `/outreach/:path*`) proxies to the SMB
  deployment's URL. Keep the SMB app as a separate Vercel project — do **not** fold its
  source into the main site repo (that's how things blend again).

Confirm the SMB deployment's own env/config does not point at Contract-Hunter's Railway
backend — it should have its own backend/data or be static.

### 6. Verify

- `officialseanbuilds.com/outreach` → the SeanBuilds SMB outreach landing page, correct
  branding, no Contract Hunter UI.
- `contract-hunter-production-…up.railway.app` (Contract Hunter) → still the Vulnaguard
  "Local Contract Hunter AI" dashboard, untouched.
- The two deployments share no source and no repo.

### 7. Commit + document

```bash
git commit -am "Separate SMB outreach landing page from Contract Hunter; brand under SeanBuilds"
git push -u origin claude/sean-builds-contract-hunter-separation
```

Then log it in `decisions/log.md` here (business-level → also mirror to the Obsidian vault
per CLAUDE.md).

---

## Guardrail to stop re-blending

- Contract Hunter = **Vulnaguard** product, Railway. Its repo stays `JonSvitna/Contract-Hunter`.
- SMB Outreach = **SeanBuilds** product, `officialseanbuilds.com/outreach`. Its repo stays
  `JonSvitna/vulnaguard-smb-automation`.
- Never copy one app's source into the other's repo. Cross-link between the two live URLs;
  don't share source trees.
- The n8n flow that used to hang off Contract Hunter already lives in its own repo — keep
  it there too. Three separate concerns, three separate repos.
