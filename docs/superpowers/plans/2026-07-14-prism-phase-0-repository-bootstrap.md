# Prism Phase 0 Repository Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a private, independent Prism repository from the approved Sentinel CMMC snapshot, add Prism's Builder AIOS, import only approved local development credentials into ignored configuration, and prove that Sentinel cannot backflow into Prism.

**Architecture:** Prism starts from a clean working-tree snapshot of Sentinel commit `a1af8a5f1ff1a5f29744b2f592b866782b2cdf25`, without Sentinel Git history or remotes. Phase 0 preserves the application baseline while adding repository-isolation guards, a separate AIOS operating layer, and explicit credential boundaries. Customer credentials are not part of this phase and will live in customer-owned Azure Key Vault instances.

**Tech Stack:** Git, GitHub CLI, Python 3.11/3.12, FastAPI, SQLAlchemy, pytest, Next.js 16, React 19, TypeScript, shell verification commands

---

## Scope decomposition

The approved Prism design covers multiple independently testable systems. They will receive separate implementation plans in this order:

1. **Phase 0 — Repository bootstrap:** independent repository, AIOS, credential boundary, isolation verification, inherited baseline.
2. **Phase 1 — Compliance kernel:** canonical objectives, framework requirements, mappings, and framework-neutral readiness.
3. **Phase 2 — Azure customer data plane:** deployment template, identity, Key Vault, storage, database, control-plane contract, and teardown.
4. **Phase 3 — Evidence engine migration:** Azure-backed artifacts, extraction, provenance, reviews, connectors, and deterministic degraded operation.
5. **Phase 4 — Customer compliance brain:** Azure knowledge graph, GraphRAG indexing, relationship provenance, and source-backed retrieval.
6. **Phase 5 — Communications autonomy:** evidence requests, three-attempt cadence, delivery tracking, responses, and manager escalation.
7. **Phase 6 — Prism workspace and pilot:** cross-framework experience, reports, operational dashboard, end-to-end pilot verification, and offboarding.

This document implements Phase 0 only. It deliberately leaves Sentinel application behavior unchanged until the inherited baseline is captured.

## File map

### Source repository

- Read: `/Users/seanm/Documents/GitHub/Sentinel-CMMC/**`
- Source commit: `a1af8a5f1ff1a5f29744b2f592b866782b2cdf25`

### New Prism repository

- Create repository root: `/Users/seanm/Documents/GitHub/Prism-OS`
- Create: `PROVENANCE.md` — one-time Sentinel snapshot record and independence guarantee.
- Modify: `.gitignore` — exclude every local secret, environment, cache, and generated artifact.
- Create: `.env.example` — Prism local-development configuration contract with blank secret values.
- Create: `scripts/import_dev_env.py` — allowlisted secret importer that never prints values.
- Create: `tooling/tests/test_import_dev_env.py` — importer unit tests.
- Create: `scripts/assert_repo_isolation.py` — validates remotes, submodules, package links, and sync workflows.
- Create: `tooling/tests/test_repo_isolation.py` — isolation-guard unit tests.
- Create: `scripts/check_tracked_secrets.py` — rejects recognizable credential material in tracked files.
- Create: `tooling/tests/test_tracked_secrets.py` — secret-scanner unit tests.
- Create: `.github/workflows/repository-isolation.yml` — runs isolation and credential-safety tests on every push and pull request.
- Replace: `CLAUDE.md` — Prism Builder AIOS source-of-truth operating manual.
- Generate: `AGENTS.md` — generated copy of `CLAUDE.md` for Codex.
- Create: `context/about-product.md` — Prism mission, users, and boundaries.
- Create: `context/priorities.md` — ordered implementation priorities.
- Create: `context/active-task.md` — cross-agent handoff state.
- Create: `connections.md` — separate Prism connection registry.
- Create: `decisions/log.md` — append-only Prism decisions.
- Create: `references/credential-boundaries.md` — provisioning, builder, and customer credential rules.
- Create: `docs/migration/sentinel-source-inventory.md` — inherited capability and baseline record.
- Copy: `.agents/skills/{onboard,audit,level-up,handoff}/**` — independent Builder AIOS skills.
- Copy: `references/3ms-framework.md` — internal operating framework used by the Builder AIOS.
- Copy: `scripts/sync_agent_manuals.py` — keeps `AGENTS.md` synchronized from `CLAUDE.md`.

## Credential decisions established by this plan

### Provisioning-only credential

`GITHUB_APP_TOKEN` from `/Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.env` is valid for the `JonSvitna` GitHub account. It is used only as an ephemeral `GH_TOKEN` while creating and verifying the private repository. It is never copied into Prism.

### Allowlisted local-development credentials

The importer may copy these values from `/Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.env` into Prism's ignored root `.env`:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `RESEND_API_KEY`
- `STRIPE_SECRET_KEY`
- `MS365_TENANT_ID`
- `MS365_CLIENT_ID`
- `MS365_CLIENT_SECRET`
- `MS365_USER_UPN`

These credentials support Builder AIOS work and controlled development demonstrations. They are not deployed into customer environments.

### Customer credentials

Customer Microsoft, Google, Azure, messaging, graph, and storage credentials are never copied from another local repository. Each customer supplies them to resources inside that customer's Azure subscription, with secrets stored in that customer's Key Vault.

## Task 1: Create a clean local Prism snapshot

**Files:**
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/**`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/PROVENANCE.md`
- Modify: `/Users/seanm/Documents/GitHub/Prism-OS/.gitignore`

- [ ] **Step 1: Verify the Sentinel source is clean and pinned**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Sentinel-CMMC
git status --short
git rev-parse HEAD
git remote -v
```

Expected:

```text
# git status prints nothing
a1af8a5f1ff1a5f29744b2f592b866782b2cdf25
origin  https://github.com/JonSvitna/Sentinel-CMMC.git (fetch)
origin  https://github.com/JonSvitna/Sentinel-CMMC.git (push)
```

- [ ] **Step 2: Copy the working tree without Git identity or generated state**

Run:

```bash
mkdir -p /Users/seanm/Documents/GitHub/Prism-OS
rsync -a \
  --exclude='.git/' \
  --exclude='.env' \
  --exclude='.env.local' \
  --exclude='.env.*.local' \
  --exclude='.venv/' \
  --exclude='venv/' \
  --exclude='node_modules/' \
  --exclude='.next/' \
  --exclude='dist/' \
  --exclude='build/' \
  --exclude='__pycache__/' \
  --exclude='.pytest_cache/' \
  --exclude='*.tsbuildinfo' \
  --exclude='.DS_Store' \
  /Users/seanm/Documents/GitHub/Sentinel-CMMC/ \
  /Users/seanm/Documents/GitHub/Prism-OS/
```

Expected: the command exits `0`, and `/Users/seanm/Documents/GitHub/Prism-OS/backend/app/main.py` exists.

- [ ] **Step 3: Initialize new Git history with no remote**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
git init -b main
git remote -v
git log --oneline --all
```

Expected: both `git remote -v` and `git log --oneline --all` print nothing.

- [ ] **Step 4: Write the provenance document**

Create `PROVENANCE.md` with exactly:

```markdown
# Prism source provenance

Prism began as a one-time clean working-tree snapshot of Sentinel CMMC.

- Source repository: `JonSvitna/Sentinel-CMMC`
- Source commit: `a1af8a5f1ff1a5f29744b2f592b866782b2cdf25`
- Snapshot date: `2026-07-14`
- Git history inherited: no
- Runtime dependency on Sentinel: no
- Automated synchronization with Sentinel: prohibited

Sentinel and Prism are independent products. Changes in either repository must not enter the other automatically. Any future manual code reuse requires a documented decision, explicit review, and a normal Prism commit.
```

- [ ] **Step 5: Harden `.gitignore` before creating local configuration**

Ensure `.gitignore` contains this secret section:

```gitignore
# Environment and secrets
.env
.env.*
!.env.example
*.pem
*.key
*.pfx
*.p12
credentials.json
secrets.json

# Azure local deployment state
.azure/
*.parameters.local.json

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Node and Next.js
node_modules/
.next/
out/
dist/
build/
.turbo/
*.tsbuildinfo
*.log

# Editor and operating system
.vscode/
.idea/
.DS_Store
Thumbs.db
```

- [ ] **Step 6: Verify inherited secret files are absent**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
find . -type f \( -name '.env' -o -name '.env.local' -o -name '*.pem' -o -name '*.pfx' -o -name 'credentials.json' \) -print
```

Expected: no output.

## Task 2: Build the allowlisted development credential importer

**Files:**
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/scripts/import_dev_env.py`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/tooling/tests/test_import_dev_env.py`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/.env.example`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/references/credential-boundaries.md`

- [ ] **Step 1: Write failing importer tests**

Create `tooling/tests/test_import_dev_env.py`:

```python
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from scripts.import_dev_env import ALLOWED_KEYS, import_env, parse_env


class DevEnvImportTests(unittest.TestCase):
    def test_parse_env_ignores_comments_and_invalid_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / ".env"
            source.write_text(
                "# comment\nOPENAI_API_KEY=alpha\nINVALID\nRESEND_API_KEY='beta'\n",
                encoding="utf-8",
            )
            self.assertEqual(
                parse_env(source),
                {"OPENAI_API_KEY": "alpha", "RESEND_API_KEY": "beta"},
            )

    def test_import_env_writes_only_allowlisted_nonempty_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.env"
            target = Path(tmp) / "target.env"
            source.write_text(
                "OPENAI_API_KEY=alpha\nGITHUB_APP_TOKEN=never-copy\nRESEND_API_KEY=\n",
                encoding="utf-8",
            )
            written = import_env(source, target)
            self.assertEqual(written, ["OPENAI_API_KEY"])
            self.assertEqual(target.read_text(encoding="utf-8"), "OPENAI_API_KEY=alpha\n")
            self.assertEqual(os.stat(target).st_mode & 0o777, 0o600)
            self.assertNotIn("GITHUB_APP_TOKEN", ALLOWED_KEYS)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
python3 -m unittest tooling.tests.test_import_dev_env -v
```

Expected: `ModuleNotFoundError: No module named 'scripts.import_dev_env'`.

- [ ] **Step 3: Implement the importer**

Create `scripts/import_dev_env.py`:

```python
from __future__ import annotations

import argparse
import os
from pathlib import Path


DEFAULT_SOURCE = Path.home() / "Documents/GitHub/Vulnaguard-AIS-OS/.env"
DEFAULT_TARGET = Path(__file__).resolve().parents[1] / ".env"

ALLOWED_KEYS = (
    "ANTHROPIC_API_KEY",
    "MS365_CLIENT_ID",
    "MS365_CLIENT_SECRET",
    "MS365_TENANT_ID",
    "MS365_USER_UPN",
    "OPENAI_API_KEY",
    "RESEND_API_KEY",
    "STRIPE_SECRET_KEY",
)


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if key:
            values[key] = value
    return values


def import_env(source: Path, target: Path) -> list[str]:
    source_values = parse_env(source)
    selected = {
        key: source_values[key]
        for key in ALLOWED_KEYS
        if source_values.get(key)
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(f"{key}={selected[key]}\n" for key in sorted(selected))
    target.write_text(payload, encoding="utf-8")
    os.chmod(target, 0o600)
    return sorted(selected)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import allowlisted Prism development credentials without printing values."
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    args = parser.parse_args()
    written = import_env(args.source, args.target)
    print("Imported keys: " + ", ".join(written))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests and verify they pass**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
python3 -m unittest tooling.tests.test_import_dev_env -v
```

Expected: two tests pass.

- [ ] **Step 5: Create the public environment contract**

Replace `.env.example` with:

```dotenv
# Local application
ENV=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=/api/backend

# Legacy Sentinel baseline; removed when Phase 2 migrates the data plane to Azure
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_JWT_SECRET=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=

# Prism AI services
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_API_KEY=

# Development communications and billing
RESEND_API_KEY=
ALERT_FROM_EMAIL=alerts@vulnaguard.com
STRIPE_SECRET_KEY=

# Development Microsoft tenant only; customer credentials belong in customer Key Vault
MS365_TENANT_ID=
MS365_CLIENT_ID=
MS365_CLIENT_SECRET=
MS365_USER_UPN=

# Azure deployment identity; use local Azure CLI or workload identity instead of committed secrets
AZURE_SUBSCRIPTION_ID=
AZURE_TENANT_ID=
AZURE_LOCATION=eastus
```

- [ ] **Step 6: Document the credential boundary**

Create `references/credential-boundaries.md`:

```markdown
# Prism credential boundaries

## Provisioning credentials

GitHub and Azure provisioning credentials are supplied to the provisioning command at runtime. They are not stored in Prism `.env` files.

## Builder development credentials

`scripts/import_dev_env.py` copies an explicit allowlist from Vulnaguard AIS OS into Prism's ignored local `.env`. The script prints key names only. It never imports GitHub, DigitalOcean, Supabase, database, Slack, Buffer, YouTube, or customer credentials.

## Customer credentials

Customer connection secrets are created or supplied inside the customer's Azure subscription and stored in that customer's Key Vault. They must not enter the Prism control plane, Builder AIOS, source repository, logs, analytics, or Sean's Obsidian vault.

## Rotation

Reusing a builder credential is permitted for local development only. Production services receive Prism-specific credentials before deployment. A compromised or retired source credential is rotated at its provider, not copied again.
```

- [ ] **Step 7: Import the approved keys and verify names without values**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
python3 scripts/import_dev_env.py
awk -F= '/^[A-Z][A-Z0-9_]*=/{print $1}' .env
git check-ignore -v .env
```

Expected:

- The importer prints only the eight allowlisted key names that exist.
- `awk` prints key names only.
- `git check-ignore` identifies the `.env` ignore rule.

- [ ] **Step 8: Commit the credential tooling**

Run:

```bash
git add .gitignore .env.example scripts/import_dev_env.py tooling/tests/test_import_dev_env.py references/credential-boundaries.md
git commit -m "chore: establish Prism credential boundaries"
```

Expected: commit succeeds and `.env` is not staged.

## Task 3: Install the Prism Builder AIOS

**Files:**
- Replace: `/Users/seanm/Documents/GitHub/Prism-OS/CLAUDE.md`
- Generate: `/Users/seanm/Documents/GitHub/Prism-OS/AGENTS.md`
- Generate: `/Users/seanm/Documents/GitHub/Prism-OS/.cursor/rules/aios.mdc`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/context/about-product.md`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/context/priorities.md`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/context/active-task.md`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/connections.md`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/decisions/log.md`
- Copy: `/Users/seanm/Documents/GitHub/Prism-OS/.agents/skills/{onboard,audit,level-up,handoff}/**`
- Copy: `/Users/seanm/Documents/GitHub/Prism-OS/references/3ms-framework.md`
- Copy: `/Users/seanm/Documents/GitHub/Prism-OS/scripts/sync_agent_manuals.py`

- [ ] **Step 1: Copy the independent AIOS skills and framework**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
mkdir -p .agents/skills context decisions references scripts
rsync -a /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.agents/skills/onboard/ .agents/skills/onboard/
rsync -a /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.agents/skills/audit/ .agents/skills/audit/
rsync -a /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.agents/skills/level-up/ .agents/skills/level-up/
rsync -a /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.agents/skills/handoff/ .agents/skills/handoff/
cp /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/references/3ms-framework.md references/3ms-framework.md
cp /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/scripts/sync_agent_manuals.py scripts/sync_agent_manuals.py
```

Expected: all four `SKILL.md` files exist under `.agents/skills/`.

- [ ] **Step 2: Write the product context**

Create `context/about-product.md`:

```markdown
# About Prism

Prism is Vulnaguard's AI-native operating system for continuous compliance readiness. It collects evidence once, converts it into source-backed claims, maps those claims to canonical security objectives, and applies the objectives across SOC 2, ISO/IEC 27001, and CMMC Level 1.

Prism is not a SIEM, incident-response system, vulnerability scanner, auditor, or certification body. It coordinates evidence, readiness work, communications, escalation, and reporting. Customer data remains in a customer-owned Azure data plane.

The product promise is: **Collect once. Map once. Prove many.**
```

Create `context/priorities.md`:

```markdown
# Prism priorities

1. Preserve a clean, testable Sentinel baseline without repository coupling.
2. Replace CMMC-specific assumptions with canonical objectives and framework modules.
3. Deploy each customer data plane into the customer's Azure subscription.
4. Preserve provenance and deterministic behavior before adding AI autonomy.
5. Demonstrate cross-framework evidence reuse and autonomous communication escalation.
```

Create `context/active-task.md`:

```markdown
# Active task

**Status:** none

## Objective

No task is currently active.

## Last verified

2026-07-14
```

- [ ] **Step 3: Write the Builder AIOS operating manual**

Replace `CLAUDE.md` with:

```markdown
# Prism Builder AIOS

You are Prism's product and engineering operating system. Help Sean design, build, verify, document, and ship Prism without contaminating Sentinel CMMC or customer data.

## Mission

Build Prism into an AI-native operating system for SOC 2, ISO/IEC 27001, and CMMC Level 1 readiness. Preserve the promise: collect once, map once, prove many.

## Non-negotiable boundaries

- Sentinel CMMC is read-only source material. Never add a Sentinel remote, submodule, package dependency, or automated sync.
- Original evidence and relational records are authoritative. Graph and AI outputs are derived and retain provenance.
- Customer data stays in the customer's Azure subscription.
- Customer secrets stay in the customer's Key Vault.
- No customer data enters this repository, Builder AIOS memory, product analytics, or Sean's Obsidian vault.
- Prism does not issue certifications, investigate incidents, or modify customer infrastructure without explicit authorization.

## Operator brain

Read `references/3ms-framework.md` once. Prefer deterministic operations, the lowest sufficient autonomy, narrow permissions, validation chains, audit trails, and reversible changes.

## Context and records

- `context/about-product.md` — product mission and boundaries
- `context/priorities.md` — current build order
- `context/active-task.md` — cross-agent handoff state
- `connections.md` — every external system Prism can reach
- `decisions/log.md` — append-only technical and product decisions
- `references/` — researched-once technical and framework guidance
- `docs/superpowers/specs/` — approved designs
- `docs/superpowers/plans/` — executable implementation plans

## Required working style

- Be direct and evidence-backed.
- Use tests before changing inherited behavior.
- Keep units small and interfaces explicit.
- Record provenance for automated conclusions.
- Never print or commit secret values.
- Run repository-isolation checks before every push.
- Do not claim success without current verification.

## Four Cs

- **Context:** product scope, customer boundaries, framework knowledge, and decisions
- **Connections:** Azure, Microsoft, Google, communications, billing, and approved developer services
- **Capabilities:** evidence collection, mapping, readiness, task routing, communications, reports, and deployment
- **Cadence:** syncs, freshness checks, follow-ups, escalation, audits, releases, and weekly improvement

Run `/audit` after Phase 0 and weekly thereafter. Run `/level-up` when recurring manual work appears three or more times.
```

- [ ] **Step 4: Create connection and decision registries**

Create `connections.md`:

```markdown
# Prism connections

| Domain | Tool | Environment | Mechanism | Credential location | Status |
|---|---|---|---|---|---|
| Source control | GitHub | Builder | CLI/API | runtime provisioning token, not Prism env | verified for repository creation |
| AI reasoning | OpenAI | Builder | API | ignored local `.env` | available for development |
| AI reasoning | Anthropic | Builder | API | ignored local `.env` | available for development |
| Communications | Resend | Builder | API | ignored local `.env` | available for development |
| Billing | Stripe | Control plane | API | ignored local `.env`; production key separated before deployment | live key verified 2026-07-14 |
| Microsoft demo tenant | Microsoft Graph | Builder | app-only API | ignored local `.env` | available for controlled development |
| Customer data plane | Azure | Customer | deployment + managed identity | customer subscription and Key Vault | not provisioned in Phase 0 |
| Customer knowledge | Azure graph and GraphRAG | Customer | customer data-plane services | customer subscription | not provisioned in Phase 0 |
| Google sources | Google Workspace and GCP | Customer | OAuth/service account | customer Key Vault | not provisioned in Phase 0 |
```

Create `decisions/log.md`:

```markdown
# Prism decision log

Append decisions. Do not rewrite prior entries.

## 2026-07-14 — Create Prism as an independent compliance operating system

**Decision:** Build Prism in a new private repository from a one-time clean snapshot of Sentinel CMMC. Do not use GitHub's Fork function and do not retain any automated relationship with Sentinel.

**Why:** Prism needs Sentinel's proven evidence foundation without allowing either product's changes to backflow into the other.

## 2026-07-14 — Use a split control-plane and customer-owned Azure data-plane model

**Decision:** Vulnaguard operates the Prism control plane. Each customer owns the Azure subscription or resource group containing documents, authoritative records, graph indexes, credentials, logs, backups, and runtime services.

**Why:** Customers retain control, portability, revocation, retention, and destruction authority over their compliance data.
```

- [ ] **Step 5: Generate `AGENTS.md` and verify synchronization**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
python3 scripts/sync_agent_manuals.py
python3 -c 'from pathlib import Path; from scripts.sync_agent_manuals import HEADER; body=Path("CLAUDE.md").read_text(); assert Path("AGENTS.md").read_text() == HEADER + "\n" + body'
```

Expected: the sync script succeeds, creates `AGENTS.md` and `.cursor/rules/aios.mdc`, and the assertion exits `0`.

- [ ] **Step 6: Run a structural Four-Cs baseline**

Run the local `/audit` skill against `/Users/seanm/Documents/GitHub/Prism-OS` and save its first report to `audits/audit-2026-07-14.md`.

Expected: Context and Capabilities recognize the new manual, context, references, decisions, and four skills. Connections and Cadence may score lower because customer Azure deployment and runtime schedules are outside Phase 0; the report must state those gaps honestly.

- [ ] **Step 7: Commit the Builder AIOS**

Run:

```bash
git add CLAUDE.md AGENTS.md .cursor/rules/aios.mdc context connections.md decisions references/3ms-framework.md scripts/sync_agent_manuals.py .agents/skills audits/audit-2026-07-14.md
git commit -m "feat: establish Prism Builder AIOS"
```

Expected: commit succeeds without staging `.env`.

## Task 4: Enforce repository independence

**Files:**
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/scripts/assert_repo_isolation.py`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/tooling/tests/test_repo_isolation.py`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/scripts/check_tracked_secrets.py`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/tooling/tests/test_tracked_secrets.py`
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/.github/workflows/repository-isolation.yml`

- [ ] **Step 1: Write failing isolation tests**

Create `tooling/tests/test_repo_isolation.py`:

```python
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.assert_repo_isolation import find_isolation_problems


class RepositoryIsolationTests(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q", str(root)], check=True)

    def test_clean_prism_remote_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            subprocess.run(
                ["git", "-C", str(root), "remote", "add", "origin", "https://github.com/JonSvitna/Prism-OS.git"],
                check=True,
            )
            self.assertEqual(find_isolation_problems(root), [])

    def test_sentinel_remote_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            subprocess.run(
                ["git", "-C", str(root), "remote", "add", "upstream", "https://github.com/JonSvitna/Sentinel-CMMC.git"],
                check=True,
            )
            problems = find_isolation_problems(root)
            self.assertTrue(any("Sentinel remote" in problem for problem in problems))

    def test_sentinel_submodule_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            (root / ".gitmodules").write_text(
                '[submodule "sentinel"]\n\tpath = vendor/sentinel\n\turl = https://github.com/JonSvitna/Sentinel-CMMC.git\n',
                encoding="utf-8",
            )
            problems = find_isolation_problems(root)
            self.assertTrue(any("Sentinel submodule" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:

```bash
python3 -m unittest tooling.tests.test_repo_isolation -v
```

Expected: `ModuleNotFoundError: No module named 'scripts.assert_repo_isolation'`.

- [ ] **Step 3: Implement the isolation guard**

Create `scripts/assert_repo_isolation.py`:

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SENTINEL_MARKER = "github.com/jonsvitna/sentinel-cmmc"
LINK_FILES = (
    ".gitmodules",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
)


def git_output(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def find_isolation_problems(root: Path) -> list[str]:
    problems: list[str] = []
    remotes = git_output(root, "remote", "-v").lower()
    if SENTINEL_MARKER in remotes:
        problems.append("Sentinel remote is prohibited")

    modules = root / ".gitmodules"
    if modules.exists() and SENTINEL_MARKER in modules.read_text(encoding="utf-8").lower():
        problems.append("Sentinel submodule is prohibited")

    for relative in LINK_FILES[1:]:
        path = root / relative
        if path.exists() and SENTINEL_MARKER in path.read_text(encoding="utf-8").lower():
            problems.append(f"Sentinel package dependency is prohibited: {relative}")

    workflow_root = root / ".github/workflows"
    if workflow_root.exists():
        for path in workflow_root.glob("*.y*ml"):
            text = path.read_text(encoding="utf-8").lower()
            if SENTINEL_MARKER in text or "repository: jonsvitna/sentinel-cmmc" in text:
                problems.append(f"Sentinel workflow synchronization is prohibited: {path.name}")
    return problems


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    problems = find_isolation_problems(root)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    print("Repository isolation verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the tests and verify they pass**

Run:

```bash
python3 -m unittest tooling.tests.test_repo_isolation -v
python3 scripts/assert_repo_isolation.py
```

Expected: three unit tests pass and the script prints `Repository isolation verified.`

- [ ] **Step 5: Write failing tracked-secret scanner tests**

Create `tooling/tests/test_tracked_secrets.py`:

```python
from __future__ import annotations

import unittest

from scripts.check_tracked_secrets import scan_text


class TrackedSecretTests(unittest.TestCase):
    def test_blank_example_values_pass(self) -> None:
        self.assertEqual(scan_text(".env.example", "OPENAI_API_KEY=\nSTRIPE_SECRET_KEY=\n"), [])

    def test_openai_key_is_detected(self) -> None:
        value = "sk-" + "proj-" + "abcdefghijklmnopqrstuvwxyz123456"
        findings = scan_text("settings.txt", f"OPENAI_API_KEY={value}")
        self.assertEqual(findings, ["settings.txt: OpenAI API key"])

    def test_github_and_stripe_keys_are_detected(self) -> None:
        github = "ghp_" + "abcdefghijklmnopqrstuvwxyz123456"
        stripe = "sk_" + "live_" + "abcdefghijklmnopqrstuvwxyz"
        text = (
            f"GITHUB_TOKEN={github}\n"
            f"STRIPE_SECRET_KEY={stripe}\n"
        )
        findings = scan_text("leak.env", text)
        self.assertEqual(
            findings,
            ["leak.env: GitHub token", "leak.env: Stripe live secret"],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 6: Run the scanner tests and verify they fail**

Run:

```bash
python3 -m unittest tooling.tests.test_tracked_secrets -v
```

Expected: `ModuleNotFoundError: No module named 'scripts.check_tracked_secrets'`.

- [ ] **Step 7: Implement the tracked-secret scanner**

Create `scripts/check_tracked_secrets.py`:

```python
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


PATTERNS = (
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("Stripe live secret", re.compile(r"\b(?:sk_live|rk_live)_[A-Za-z0-9]{16,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("Private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


def scan_text(name: str, text: str) -> list[str]:
    return [f"{name}: {label}" for label, pattern in PATTERNS if pattern.search(text)]


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [root / item.decode() for item in result.stdout.split(b"\0") if item]


def scan_repository(root: Path) -> list[str]:
    findings: list[str] = []
    for path in tracked_files(root):
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text(str(path.relative_to(root)), text))
    return findings


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    findings = scan_repository(root)
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}", file=sys.stderr)
        return 1
    print("Tracked secret scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 8: Run all tooling tests and both guards**

Run:

```bash
python3 -m unittest discover -s tooling/tests -p 'test_*.py' -v
python3 scripts/assert_repo_isolation.py
python3 scripts/check_tracked_secrets.py
```

Expected: all tooling tests pass, followed by `Repository isolation verified.` and `Tracked secret scan passed.`

- [ ] **Step 9: Add the CI guard**

Create `.github/workflows/repository-isolation.yml`:

```yaml
name: Repository isolation

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 1
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Verify repository isolation
        run: python3 scripts/assert_repo_isolation.py
      - name: Reject recognizable tracked secrets
        run: python3 scripts/check_tracked_secrets.py
      - name: Verify tooling tests
        run: python3 -m unittest discover -s tooling/tests -p 'test_*.py' -v
      - name: Reject tracked environment files
        run: |
          if git ls-files | grep -E '(^|/)\.env($|\.)' | grep -vE '(^|/)\.env\.example$'; then
            echo "Tracked environment file detected" >&2
            exit 1
          fi
```

- [ ] **Step 10: Commit the isolation and secret guards**

Run:

```bash
git add scripts/assert_repo_isolation.py scripts/check_tracked_secrets.py tooling/tests/test_repo_isolation.py tooling/tests/test_tracked_secrets.py .github/workflows/repository-isolation.yml
git commit -m "test: enforce Prism repository safety"
```

Expected: commit succeeds.

## Task 5: Capture the inherited baseline before stripping code

**Files:**
- Create: `/Users/seanm/Documents/GitHub/Prism-OS/docs/migration/sentinel-source-inventory.md`
- Verify: `/Users/seanm/Documents/GitHub/Prism-OS/backend/tests/**`
- Verify: `/Users/seanm/Documents/GitHub/Prism-OS/frontend/**`

- [ ] **Step 1: Create isolated dependency environments**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
uv venv --python 3.12 backend/.venv
uv pip install --python backend/.venv/bin/python -r backend/requirements.txt pytest
cd frontend
npm ci
```

Expected: Python and Node dependencies install successfully without modifying lockfiles.

- [ ] **Step 2: Run the inherited backend suite**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS/backend
PYTHONPATH=. .venv/bin/python -m pytest -q
```

Expected: the inherited Sentinel baseline passes with `130 passed` or a higher passing count if the pinned source contains additional tests. Any variance must be recorded with the exact failing test and error before proceeding.

- [ ] **Step 3: Run the inherited frontend checks**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS/frontend
npm run lint
npm run build
```

Expected: lint and production build both exit `0`.

- [ ] **Step 4: Record the source inventory and verification evidence**

Create `docs/migration/sentinel-source-inventory.md`:

```markdown
# Sentinel source inventory

## Snapshot

- Source: `JonSvitna/Sentinel-CMMC`
- Commit: `a1af8a5f1ff1a5f29744b2f592b866782b2cdf25`
- Imported as Git history: no
- Imported secret files: no

## Inherited foundations

- FastAPI and SQLAlchemy backend
- Next.js and React workspace
- Evidence CRUD, signed access, review, provenance, and freshness
- PDF and DOCX extraction
- Content-aware evidence suggestions
- Finding normalization and deterministic mapping rules
- Readiness, reports, POA&M-style work tracking, and audit events
- Scheduled syncs and connector adapter contract
- GitHub, Entra ID, Okta, AWS, Azure, Google Drive, and SharePoint adapters
- AI command preview and confirmation flow

## Sentinel-only behavior retained temporarily for baseline comparison

- CMMC and NIST control identifiers
- Contract eligibility and revenue-risk logic
- CMMC-specific labels, reports, and dashboard behavior
- Supabase authentication and storage
- Railway deployment configuration

These remain unchanged in Phase 0 so later Prism changes can be tested against a known baseline. Their removal or replacement requires a later approved plan.

## Verification

- Backend test command: `cd backend && PYTHONPATH=. .venv/bin/python -m pytest -q`
- Frontend lint command: `cd frontend && npm run lint`
- Frontend build command: `cd frontend && npm run build`
- Repository isolation command: `python3 scripts/assert_repo_isolation.py`
```

Append the exact current test count and build result after running the commands.

- [ ] **Step 5: Commit the verified baseline record**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
git add docs/migration/sentinel-source-inventory.md
git commit -m "docs: record Prism source baseline"
```

Expected: commit succeeds and generated dependency directories remain ignored.

## Task 6: Create and verify the private GitHub repository

**Files:**
- Verify: `/Users/seanm/Documents/GitHub/Prism-OS/.git/config`
- Remote: `https://github.com/JonSvitna/Prism-OS`

- [ ] **Step 1: Run pre-push safety checks**

Run:

```bash
cd /Users/seanm/Documents/GitHub/Prism-OS
python3 scripts/assert_repo_isolation.py
python3 scripts/check_tracked_secrets.py
python3 -m unittest discover -s tooling/tests -p 'test_*.py' -v
git diff --check
git status --short
git ls-files | grep -E '(^|/)\.env($|\.)' | grep -vE '(^|/)\.env\.example$' && exit 1 || true
```

Expected:

- Isolation verification passes.
- All tooling tests pass.
- `git diff --check` prints nothing.
- `.env` does not appear as tracked or staged.

- [ ] **Step 2: Create the initial snapshot commit if copied files remain uncommitted**

Run:

```bash
git add .
git status --short
python3 scripts/check_tracked_secrets.py
git ls-files | grep -E '(^|/)\.env($|\.)' | grep -vE '(^|/)\.env\.example$' && exit 1 || true
git commit -m "chore: bootstrap independent Prism codebase"
```

Expected: the staged-tree secret scan passes. The commit contains the clean Sentinel snapshot plus Phase 0 files, but no secret files or generated dependency state. If earlier task commits already captured every file, `git status --short` is empty and this commit is skipped.

- [ ] **Step 3: Create the private GitHub repository with the verified provisioning token**

Run from `/Users/seanm/Documents/GitHub/Prism-OS`:

```bash
export GH_TOKEN="$(awk -F= '$1 == "GITHUB_APP_TOKEN" {print substr($0, index($0, "=") + 1); exit}' /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.env)"
gh repo create JonSvitna/Prism-OS --private --source=. --remote=origin --push
unset GH_TOKEN
```

Expected: GitHub creates `JonSvitna/Prism-OS` as a private, non-fork repository, configures `origin`, and pushes `main`.

- [ ] **Step 4: Prove the remote is independent**

Run:

```bash
export GH_TOKEN="$(awk -F= '$1 == "GITHUB_APP_TOKEN" {print substr($0, index($0, "=") + 1); exit}' /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.env)"
gh api repos/JonSvitna/Prism-OS --jq '{name: .name, private: .private, fork: .fork, parent: .parent}'
unset GH_TOKEN
git remote -v
python3 scripts/assert_repo_isolation.py
```

Expected:

```json
{"fork":false,"name":"Prism-OS","parent":null,"private":true}
```

`git remote -v` must list only `https://github.com/JonSvitna/Prism-OS.git`, and the isolation guard must pass.

- [ ] **Step 5: Verify the pushed branch and CI**

Run:

```bash
export GH_TOKEN="$(awk -F= '$1 == "GITHUB_APP_TOKEN" {print substr($0, index($0, "=") + 1); exit}' /Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS/.env)"
gh run list --repo JonSvitna/Prism-OS --limit 5
unset GH_TOKEN
git status --short
```

Expected: the Repository isolation workflow appears and completes successfully. Local `git status --short` prints nothing except intentionally untracked local files that are covered by `.gitignore` and therefore normally remain invisible.

## Phase 0 completion gate

Phase 0 is complete only when all of the following are true:

- `JonSvitna/Prism-OS` exists as a private GitHub repository with `fork: false` and `parent: null`.
- The local repository has no Sentinel remote, submodule, dependency, or sync workflow.
- The source commit is recorded in `PROVENANCE.md` and the migration inventory.
- No secret file or credential value is tracked.
- The allowlisted developer credentials exist only in ignored local `.env`.
- The GitHub provisioning token is not copied into Prism.
- Prism has its own operating manual, context, connections, decisions, skills, and Four-Cs baseline.
- The inherited backend tests, frontend lint, and frontend build have current recorded results.
- The repository-isolation CI workflow passes on `main`.

After this gate passes, write the Phase 1 compliance-kernel implementation plan from the approved Prism design before modifying inherited framework behavior.
