#!/usr/bin/env python3
"""Regenerate AGENTS.md and .cursor/rules/aios.mdc from CLAUDE.md."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = ROOT / "CLAUDE.md"
AGENTS = ROOT / "AGENTS.md"
CURSOR_RULE = ROOT / ".cursor" / "rules" / "aios.mdc"

HEADER = """<!-- GENERATED FILE — do not edit directly.
Source of truth is CLAUDE.md at the repo root.
Edit CLAUDE.md, then run: python3 scripts/sync_agent_manuals.py -->
"""

CURSOR_FRONTMATTER = """---
description: AIOS operating manual (mirrors CLAUDE.md)
alwaysApply: true
---
"""


def main() -> None:
    body = CLAUDE.read_text(encoding="utf-8")

    AGENTS.write_text(HEADER + "\n" + body, encoding="utf-8")
    CURSOR_RULE.parent.mkdir(parents=True, exist_ok=True)
    CURSOR_RULE.write_text(CURSOR_FRONTMATTER + "\n" + HEADER + "\n" + body, encoding="utf-8")

    print(f"Synced {AGENTS.relative_to(ROOT)}")
    print(f"Synced {CURSOR_RULE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
