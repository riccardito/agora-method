# CLAUDE.md — units

## Project overview

`units` converts between measurement units from the command line
(`units 3 ft m` → `0.9144`). Python 3.11, one module, the unit table as data in
`units.yaml`.

## How work runs here

The Agora method, copied from `agora-method`: sessions are bracketed by
`/agora --start` and `/agora --end`, the skills live in `.claude/skills/`, the
rules in `.claude/policies/`, the state in `.claude/sessions/`. The full policy
text is read from those files; this child mirrors no TL;DR yet.

## Checks

`python -m agora_checks all` from the repository root.
