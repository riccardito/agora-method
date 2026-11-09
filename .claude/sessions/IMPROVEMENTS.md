# Agora improvements ledger

The durable memory of **how Agora itself gets better**. Per-session logs in this
folder get compacted and age out of relevance; this file does not. Every
[`/agora --end`](../skills/agora/SKILL.md) that produced a real lesson about the
pipeline appends one entry here.

This is distinct from:

- **auto-memory** (`~/.claude/projects/.../memory/`) — facts about the user,
  project, and environment
- **per-session files** (`YYYY-MM-DD-<slug>.md`) — what happened in one session
- **policies / skills** — the rules and workflows themselves

`IMPROVEMENTS.md` is the *changelog of Agora's evolution* — it answers "how has
the way we build the product changed, and why."

Format per entry:

```
## YYYY-MM-DD — <short title>

**Session:** YYYY-MM-DD-<slug>
**What changed:** <skill patched / policy authored / scaffolding added>
**Why:** <the finding from the session that drove it>
**Effect:** <what is different now>
```

<!-- Newest entries at the top. -->

<!-- Newest entries below this line. -->
