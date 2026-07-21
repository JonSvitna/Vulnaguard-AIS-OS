# Prism OS — manager boundary

Prism is Vulnaguard's multi-framework compliance operating system (SOC 2, ISO/IEC 27001, CMMC Level 1). Repo: `~/Documents/GitHub/Prism-OS` (`JonSvitna/Prism-OS`, private).

## Role of Vulnaguard AIS OS

This AIOS is the **head manager**, not the implementation home.

Allowed here:

- Track Prism as a connection and active product line
- Prioritize, schedule, and hand off Prism work
- Route Prism product history into the Obsidian vault (non-customer)
- Coach capture/commercial context when Prism affects client pipeline

Not allowed here:

- Edit Prism application code, catalogs, migrations, or Builder AIOS files
- Copy Sentinel fixes into Prism (or the reverse) without an explicit decision recorded in Prism
- Store customer evidence, claims, or Key Vault material in this repo or the personal vault

## Where Prism work happens

- Product and engineering changes: open `~/Documents/GitHub/Prism-OS` and use Prism's Builder AIOS (`CLAUDE.md` / `AGENTS.md` there)
- Design and plans: Prism `docs/superpowers/`
- Product history: Obsidian `wiki/domains/prism-os/`

## Credential boundary

Local builder credentials may be imported into Prism's ignored `.env` via Prism's allowlisted importer. Provisioning tokens and customer secrets stay out of both repos' tracked trees. See Prism `references/credential-boundaries.md`.
