# Agora — the skill layer

A skill is a packaged workflow an agent invokes by name (`/agora --start`). Each
lives in `.claude/skills/<name>/SKILL.md` with an `experience.md` sidecar, and
carries a level:

| Level | The claim |
|---|---|
| `draft` | written, not yet proven in use |
| `used` | invoked across real sessions; has a role and an experience log |
| `hardened` | names its boundaries (`## When NOT to use`) and three or more claims other skills rely on; has an epithet |
| `reference` | its claims read like rules other skills cite; opens with `## Identity` |

Promotion is human-confirmed through `/level`; the frontmatter lint holds the
shape each level requires ([`policy-skill-progression`](../policies/policy-skill-progression.md),
[`policy-skill-authoring`](../policies/policy-skill-authoring.md)).

## The skills

These are the eight meta-skills: the ones that run the method itself. A child
project adds its own build and doctor skills beside them. Generated from each
skill's frontmatter (record-consistency fact `skill-table`).

<!-- rc:skill-table -->
| Skill | Level | Role | Epithet |
|---|---|---|---|
| [`/agora`](agora/SKILL.md) | hardened | the mayor | Socrates — the dialectician |
| [`/design`](design/SKILL.md) | used | the Themelion conductor — red-flag code-design review, Arc phase-③ cleanup conducting, post-cleanup QC |  |
| [`/document`](document/SKILL.md) | used | the scribe |  |
| [`/inspect-pipeline`](inspect-pipeline/SKILL.md) | hardened | the registrar | Diogenes — the iconoclast with the lamp |
| [`/learn`](learn/SKILL.md) | reference | the tutor | Theophrastus — the careful classifier |
| [`/level`](level/SKILL.md) | reference | the assessor | Solon — the lawgiver who ranks the citizens |
| [`/plaza`](plaza/SKILL.md) | used | the reformer |  |
| [`/write`](write/SKILL.md) | used | the artefact author — gather · brief · produce · measured style pass |  |
<!-- /rc:skill-table -->

## How they fit

```
/agora --start ── plan ── (the child's own build skills) ── /agora --end
      │                                                          │
      │                    /inspect-pipeline --session ◄─────────┤
      │                    /learn --from-session      ◄──────────┤
      │                    /level --xp                ◄──────────┘
      │
/plaza (a self-improvement round) ── /document --policy · /learn · /level
/write  (any artefact to a named form and voice)
/design (code-design review and cleanup conducting)
```

Skill names other than these eight appear in the corpus (`/fixbug`,
`/implement-story`, `/check-page`, …). They are the parent project's build and
doctor skills, left as provenance; a child writes its own.
