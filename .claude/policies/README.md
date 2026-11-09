# Agora — the policy layer

Cross-cutting rules that any skill or any direct edit must respect live here as
focused markdown files; their TL;DR sections are mirrored into
[`CLAUDE.md`](../../CLAUDE.md) so the critical lines are always in context, with the
full text on demand.

Policies sit above skills: a policy is applied *by* skills, never the other way
around. In the Athenian Agora's map this is the Stoa Basileios, where the laws of
the city were inscribed on stone, visible to every citizen who passed through.

## Why we have a separate folder

Rules that span multiple skills (`/agora`, `/learn`, `/document`, `/level`) used to live in three places at
once: CLAUDE.md, the relevant skill SKILL.md files, and memory feedback
entries. Over time those copies drifted. Policies are the single source
of truth for each rule:

- **Skills are about workflow** — how to do a task end-to-end.
- **Policies are about rules of engagement** — invariants any task must respect.
- **Wiki seeds are about features** — what something is and how it works.

A skill *invokes* a policy by name; a policy is never *invoked* — it's
*applied*.

## Loading model

Three tiers, by where each piece of the policy ends up:

| Tier | Location | What's there |
|------|----------|-------------|
| 1 (always loaded, no Read) | `CLAUDE.md` → `## Policies` section | Each policy's TL;DR, mirrored verbatim |
| 2 (always available, Read on demand) | `.claude/policies/policy-*.md` | Full policy text — the "why", examples, mistakes |
| 3 (situational) | Skill SKILL.md cross-references | `Apply policy-X.md` lines that load the full file when relevant |

Critical rules are in Tier 1 so Claude never violates them by surprise.
Detail and rationale live in Tier 2 so Claude can deepen its
understanding when a skill says "see policy-X". Tier 3 is the explicit
hook from skill workflows.

## File pattern

```
.claude/policies/
├── README.md          ← this file
└── policy-<slug>.md   ← one per active policy
```

Slug is kebab-case and topic-focused: `policy-documentation`,
`policy-four-eyes`, `policy-spawns`, `policy-commit-discipline`.
Don't pluralise (`policy-spawn` ✓ would be wrong too — name the
topic, not the object: `policy-spawns` is the discipline of spawning).

## Authoring

Use [`/document --policy <slug>`](../skills/document/SKILL.md) (the
repurposed document skill). It walks through the same steps a manual
author would: start from an existing policy's shape, fill in the TL;DR, write the rules
with what/why/where-enforced, mirror the TL;DR into CLAUDE.md.

After writing or updating a policy:

1. Mirror the TL;DR into `CLAUDE.md` under `## Policies` (verbatim, with
   a link back to the policy file).
2. Update each related skill's SKILL.md to reference the policy at the
   point in the workflow where it applies (`Apply policy-<slug>.md`).
3. Run the checks — `make check` — the record-consistency check confirms
   the mirror and the frontmatter lint confirms the shape.

## Status field

Every policy carries a `status:` in its frontmatter:

| Status | Meaning |
|--------|---------|
| `draft` | Written but not yet referenced by any skill or mirrored into CLAUDE.md. Not yet active. |
| `active` | Mirrored into CLAUDE.md and referenced by at least one skill. Live. |
| `deprecated` | Superseded by another policy or moved into a stronger enforcement layer (lint rule, hook). Kept for historical reference; not active. |

A policy moves `draft → active` only when the CLAUDE.md sync and the
skill cross-references are in place. Don't leave half-applied policies
in the active state.

## Enforcement layers

A policy's rules can be enforced by one or more mechanisms:

- **Lint rule** — failing CI build. Strongest. Here: the `agora_checks` checks.
- **CI step** — non-lint check (e.g. ruff, pytest, type-check).
- **Pre-commit hook** — local guard before push.
- **Skill prompt** — the relevant SKILL.md tells Claude to follow the rule. Procedural; depends on the AI obeying.
- **Self** — the human author is expected to follow the rule. Weakest.

Each rule in a policy lists its enforcement layer in the
"Where enforced" line. A rule with only `self` enforcement is a
candidate for promotion to a lint rule when patterns stabilise.

## Active policies

Generated from each file's frontmatter (record-consistency fact `policy-table`).

<!-- rc:policy-table -->
| Policy | Domain | Status | Title |
|---|---|---|---|
| [`policy-commit-discipline`](policy-commit-discipline.md) | discipline | active | Commit discipline — one concern per commit, properly documented, clean tree at session boundaries |
| [`policy-documentation`](policy-documentation.md) | authoring | active | Documentation |
| [`policy-four-eyes`](policy-four-eyes.md) | discipline | active | Four-eye principle — propose, nod, then act at transition gates |
| [`policy-issue-templates`](policy-issue-templates.md) | authoring | active | GitHub Issue templates — agora:type:* axis labels at create-time |
| [`policy-shoulder-glance`](policy-shoulder-glance.md) | discipline | active | Shoulder-glance — the Schulterblick reflex (glance back before moving on) |
| [`policy-skill-authoring`](policy-skill-authoring.md) | authoring | active | Skill authoring — the static shape of a SKILL.md |
| [`policy-skill-progression`](policy-skill-progression.md) | leveling | active | Skill progression — leveling, metrics, promotion, regression |
| [`policy-skill-routing`](policy-skill-routing.md) | discipline | active | Skill routing — route work to skills, inline is the justified exception |
| [`policy-spawns`](policy-spawns.md) | discipline | active | Spawn discipline — when, how, and with what authorization |
<!-- /rc:policy-table -->

## See also

- [`../skills/README.md`](../skills/README.md) — the skill layer
- [`../sessions/README.md`](../sessions/README.md) — the session layer
