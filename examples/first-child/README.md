# first-child — a toy Agora child

A pretend product, `units`, a small command-line unit converter, used only to show
the method running. It carries no code: what it shows is the record a project
keeps around its code.

`make demo` (from the repository root) builds a working copy of this child in a
temporary directory: the method layer from the parent (`.claude/skills`,
`.claude/policies`, the session template, `agora/`) plus the files here. Then it
runs one session start to end and runs every check over the result.

What is here:

- `CLAUDE.md` — the child's own operating brief
- `agora/record-consistency.yaml` — the child's registry of duplicated facts
- `.claude/sessions/COMPASS.md` — one Era, one Goal with three success criteria
- `.claude/sessions/THREADS.md` — one open thread
- `.claude/sessions/2026-01-05-units-kickoff.md` — the session before, closed,
  with the baton the demo's session opens from
