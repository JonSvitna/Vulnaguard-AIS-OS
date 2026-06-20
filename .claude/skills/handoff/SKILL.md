---
name: handoff
description: Use when Sean says he's hit a usage limit and needs to switch to Codex or Cursor mid-task, or says "handoff", "switch agents", "continue this in Codex/Cursor". Snapshots the in-progress task to context/active-task.md and syncs the operating manual so the next agent picks up cold with full context.
---

## What this skill does

Manual agent switching, made seamless. Sean codes across Claude Code, Codex CLI, and Cursor. When he hits a limit on one, this skill writes down exactly what's in flight so whichever agent picks it up next doesn't have to re-derive context.

Two things make this work:

1. **One operating manual, three formats.** `CLAUDE.md` is canonical. `AGENTS.md` (Codex) and `.cursor/rules/aios.mdc` (Cursor) are generated copies — same content, different filename each tool expects natively.
2. **One handoff file.** `context/active-task.md` is the in-flight task snapshot. Any agent reads it first.

## Execution

### Step 1: Sync the manuals (always, no judgment call needed)

```
python3 scripts/sync_agent_manuals.py
```

Run this every time `CLAUDE.md` changed since the last handoff — keeps Codex/Cursor's view of the AIOS from drifting out of sync. Cheap to run even if nothing changed.

### Step 2: Write the handoff snapshot

Overwrite `context/active-task.md` using the template comment already in that file. Fill in, based on the actual current conversation:

- **Status:** in progress
- **Switched from / to:** which agent, and why (usage limit, just prefer the other tool, etc.)
- **What we're doing:** 1-2 sentences, the actual goal — not "fix bug" but what bug, where
- **Done so far:** concrete completed steps with file paths, not vibes
- **Next step:** the single next concrete action — be specific enough that a cold agent doesn't have to guess
- **Key files:** paths plus *why* each matters
- **Watch out for:** anything non-obvious — a gotcha, a partial edit, a decision already made and why

Be concrete. "Working on auth" is useless to the next agent. "Added JWT middleware in `api/auth.ts:40`, still need to wire it into `api/routes.ts` — don't touch the session cookie logic above line 20, that's intentionally legacy" is useful.

### Step 3: Tell Sean how to resume

Report back, don't just silently write files. Tell him:

- The snapshot is saved at `context/active-task.md`
- For **Codex**: `cd` into this repo and run `codex` — it reads `AGENTS.md` automatically, and the active task lives in `context/active-task.md`
- For **Cursor**: open this repo — it reads `.cursor/rules/aios.mdc` automatically; tell the agent in chat to read `context/active-task.md` first (Cursor rules don't auto-chain reads, the agent needs the nudge)

### Step 4: When the task is finished or handed back

Whoever finishes the task (could be a different agent than who started it) should reset `context/active-task.md` back to `**Status:** none` so it doesn't get stale and mislead the next handoff. If the decision/approach was non-trivial, log it via `decisions/log.md` per normal AIOS practice.

## Notes

- This is a **manual** switch, by design — Sean decides when he's hit a limit, not an auto-detector watching for rate-limit errors. Simpler, no brittle detection logic tied to each tool's specific error format.
- If `CLAUDE.md` changes and this skill isn't run, `AGENTS.md` / `.cursor/rules/aios.mdc` drift stale. There's no hook auto-running the sync — re-run Step 1 whenever the manual changes, not just at handoff time.
