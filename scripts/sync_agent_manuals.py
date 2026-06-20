#!/usr/bin/env python3
"""Regenerate Codex/Cursor operating manuals from CLAUDE.md.

CLAUDE.md is canonical. Codex CLI reads AGENTS.md, Cursor reads
.cursor/rules/aios.mdc — neither reads CLAUDE.md natively. This script
copies CLAUDE.md's content into both, wrapped with a generated-file
header, so all three coding agents operate from the same manual with
no manual drift.

Run any time CLAUDE.md changes. Idempotent.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "CLAUDE.md"

HEADER = """<!-- GENERATED FILE — do not edit directly.
Source of truth is CLAUDE.md at the repo root.
Edit CLAUDE.md, then run: python3 scripts/sync_agent_manuals.py -->

"""

TARGETS = {
    ROOT / "AGENTS.md": HEADER,
    ROOT / ".cursor" / "rules" / "aios.mdc": (
        "---\n"
        "description: AIOS operating manual (mirrors CLAUDE.md)\n"
        "alwaysApply: true\n"
        "---\n\n"
        + HEADER
    ),
}


def main():
    content = SOURCE.read_text()
    for path, header in TARGETS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(header + content)
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
