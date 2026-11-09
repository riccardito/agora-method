---
name: skill-authoring
title: Skill authoring — the static shape of a SKILL.md
status: active
domain: authoring
related_skills:
  - learn
  - level
  - agora
  - inspect-pipeline
  - document
related_lint_rules: []
---

# Skill authoring policy

> **Authored:** 2026-05-20, session session 2026-05-20 Phase A2 (GH #75). Consolidates skill-authoring rules that had drifted across `/agora`'s hygiene appendix, `/learn`'s frontmatter section, `policy-skill-progression`, and `validate_skill_frontmatter.py`. The split with `policy-skill-progression`: **that policy owns the *transitions* between levels; this one owns the *artifact* at each level.** The enforcement arm is `scripts/checks/validate_skill_frontmatter.py --levels` (default ON).

## TL;DR

1. **This policy owns the static shape of skill AND policy files; [`policy-skill-progression`](policy-skill-progression.md) owns the level transitions.** Every requirement on what a `SKILL.md` / `experience.md` / `policy-*.md` *contains* (frontmatter fields, body sections, quoting, categorization) lives here; how a skill *moves* between levels (metrics, gates, promotion, regression, ceremony) lives there. The enforcement arm is `scripts/checks/validate_skill_frontmatter.py` (`--levels`, default ON) — wired into `/agora --start` step 1.1, the pre-commit hook, and CI.
2. **Frontmatter prose scalars MUST be double-quoted** when the value contains `: ` (colon-space), whitespace-`#`, a leading `[`/`{`, a mid-string `|`/`>`, a `<`/`>` anywhere, or a leading reserved indicator (`& * ! ' " % @` backtick). Unquoted, they crash the VS Code extension's strict YAML parser with `Unhandled case: [object Object]` and block the user from seeing assistant responses — even though the harness's tolerant parser accepts them.
3. **Frontmatter fields gate by level** (lint-checked): `level:` ∈ `draft / used / hardened / reference` (missing → `draft`); `role:` required at `used`+; `epithet:` required at `hardened`+; a parsing `experience.md` sidecar (with `xp_total`) required at `used`+. Only `/level` writes `level:` / `promoted_at:` / `role:` / `epithet:` — direct edits violate `policy-skill-progression` Rule 5.
4. **Body sections gate by level** (lint-checked): every `SKILL.md` body has ≥1 `## ` heading; `hardened`+ adds a `## When NOT to use` (or equivalent boundary) section and a `## Claims at this level` section with ≥3 named invariants; `reference` adds a `## Identity` opening section. These are the deterministic, file-checkable artifacts the promotion quests require.
5. **A scattered rule earns its own policy when it lives in ≥3 places** (the consolidation threshold — recorded canonically in [`policy-documentation`](policy-documentation.md) Rule 3). This policy is the first application: the frontmatter-quoting rule had crossed four surfaces before being consolidated here.
6. **Policy frontmatter carries a `domain:` field** (lint-checked, added 2026-05-24 by US-AGORA-008) — one of the canonical enum values: `discipline` · `authoring` · `ui` · `i18n` · `testing` · `migration` · `leveling`. Categorizes policies for structural discovery (which set of cross-cutting rules a new contributor needs to learn for a given domain) and for observability (`/wiki/stats` renders a `by_domain` distribution chart). Required on every `.claude/policies/policy-*.md` file; the lint surfaces missing or invalid values. `_TEMPLATE.md` carries the placeholder.
7. **Cite a rule by its title, a step by its heading** — a `policy-<slug> Rule <n>` citation carries the rule's title beside the number (`Rule 8 (*form inputs use the canonical macros*)`), a skill step is cited by its heading, a command by the name the click registry carries. The consistency lint's citation mode (US-AGORA-087) resolves each against its source: a number whose quoted title is another rule's is a re-pointed citation and reds the push; a bare number is warned and counted against a ratchet that only falls. Added 2026-11-02 after T-116's renumbering of `policy-frontend-conventions` left thirteen citing lines in five skills pointing at the wrong rules.

## Why this exists

The frontmatter-quoting rule — the one that, when violated, blocks the user from seeing assistant responses (session session 2026-05-15 Finding #1) — lived in **four** places at once: the `/agora` SKILL.md hygiene appendix, the `/learn` SKILL.md frontmatter section, `scripts/checks/validate_skill_frontmatter.py`, and the pre-commit hook. The level-field and body-section requirements lived in `policy-skill-progression` — which is the *progression* policy, about levels and gates, not about file shape. When GH #74 extended the lint to enforce the level/body requirements, the same rule was about to cross a fifth surface.

Scattered authoring rules drift: the `/agora` appendix listed seven risky patterns, the `/learn` section listed six, and the script checked a slightly different set. Whoever read one surface didn't see the others. The fix is the same one `policy-documentation` Rule 3 prescribes for every cross-cutting rule: **one canonical home, mirrored into CLAUDE.md, referenced (not restated) by every skill that touches it.**

## The rules

### 1. Authoring owns the artifact; progression owns the transitions

**What:** Two policies govern skills, on a clean axis. `policy-skill-authoring` (this file) is the **static contract** — what a `SKILL.md` and its `experience.md` sidecar must *contain* to be valid at a given level. `policy-skill-progression` is the **dynamic model** — the metrics, gates, quests, promotion/regression events, naming ceremony, and XP awards that move a skill *between* levels. A field requirement ("`epithet:` exists at hardened+") is authoring; the ceremony that *produces* the epithet is progression.

**Why:** Progression is load-bearing and large (~400 lines); folding the file-shape checklist into it buried the lint's contract inside event prose. Separating the artifact from the transition gives the lint a single policy to cite and gives `policy-skill-progression` room to stay about levels.

**Where enforced:** `scripts/checks/validate_skill_frontmatter.py --levels` checks the artifact (this policy). `/level` enacts the transitions (`policy-skill-progression`). The two cross-reference each other; neither restates the other.

### 2. Frontmatter prose scalars must be quoted

**What:** Any prose scalar in `SKILL.md` / policy frontmatter (`description:`, `argument-hint:`, `name:`, `title:`, `role:`, `epithet:`) **MUST be double-quoted** if its value contains *any* of:

| Pattern | Why it bites |
|---------|--------------|
| `: ` (colon-space) mid-string | parsed as a nested mapping key — silent truncation or hard error |
| `#` preceded by whitespace | parsed as a comment — silent truncation |
| Leading `[` or `{` | opens a flow sequence/mapping |
| Mid-string `\|` or `>` | block-scalar indicators |
| `<` / `>` anywhere | reserved indicators — strict parsers reject |
| Leading `&` `*` `!` `'` `"` `%` `@` `` ` `` | reserved/anchor/tag indicators |

Prefer double quotes; use single quotes only when the value contains a literal `"`.

```yaml
description: "Reactive: surfaces gaps in EXISTING entities."
argument-hint: "[--start (default) | --end | --status | --spawn | --plaza]"
role: "the mayor"
```

**Why:** The Claude harness uses a tolerant YAML parser; the VS Code Claude Code extension uses a strict one. A risky unquoted scalar parses fine for the agent yet crashes the IDE with `Unhandled case: [object Object]`, which **blocks the user from seeing assistant responses**. The skill still works at runtime — the IDE is silently broken (session session 2026-05-15 Finding #1).

**Where enforced:** `scripts/checks/validate_skill_frontmatter.py` (YAML round-trip + the `value_needs_quoting` heuristic). `--fix` auto-quotes `description` / `argument-hint` / `name` / `title`. Defence in depth: `/agora --start` step 1.1 hard gate · pre-commit hook · CI `lint` job · `/learn` applies it reflexively when writing frontmatter.

### 3. Frontmatter fields gate by level

**What:** Each `SKILL.md` frontmatter carries a `level:` ∈ `draft / used / hardened / reference` (absent → `draft`) plus `promoted_at:`. Field requirements escalate with level:

| Field | Required at | Written by |
|-------|-------------|------------|
| `level:`, `promoted_at:` | always (default draft) | `/level` only |
| `role:` (one-line role descriptor) | `used`+ | `/level` only |
| `experience.md` sidecar (parses, has `xp_total`) | `used`+ | `/level --xp` only |
| `epithet:` (`"<Philosopher> — <domain>"`) | `hardened`+ | `/level` only |

**Why:** Co-locating the passport with the skill (no sidecar registry) is the simplest design; the lint reading all frontmatters in one pass is the same I/O as the quoting check. Escalating requirements keep `draft` skills cheap to create while making higher tiers prove their shape.

**Where enforced:** `validate_skill_frontmatter.py --levels` checks 1–4 (enum, `role:`, `experience.md`, `epithet:`). `--fix` scaffolds a missing `experience.md` from `_TEMPLATE_experience.md`; it never auto-writes `role:` / `epithet:` (those need judgment). `/level` is the exclusive writer per `policy-skill-progression` Rule 5.

### 4. Body sections gate by level

**What:** The `SKILL.md` *body* must contain, by level:

- **all** — at least one `## ` heading (structure, not a bare sentence).
- **`hardened`+** — a `## When NOT to use` table (or equivalent boundary section; mode-shape skills list every mode) **and** a `## Claims at this level` section with **≥3** named invariants (one declarative sentence each).
- **`reference`** — a `## Identity` opening section telling the story of the epithet.

**Why:** These are the deterministic, file-checkable artifacts the `policy-skill-progression` promotion quests require — a skill that cannot enumerate three claims isn't `hardened`; an unbounded skill with no "When NOT to use" hasn't proven its edges. Making them lint-checked means a promotion can't claim a quest artifact that isn't actually present.

**Where enforced:** `validate_skill_frontmatter.py --levels` checks 5–6 (`## Claims at this level` ≥3 bullets at hardened+, `## Identity` at reference). The `## When NOT to use` requirement is a `/level --promote` quest gate (procedural — not yet lint-checked).

### 5. The experience.md sidecar shape

**What:** Every `used`+ skill has `.claude/skills/<name>/experience.md` — frontmatter (`skill`, `xp_total`, `xp_by_level`, `last_xp_at`) + a `## Unrated journal` capture-at-source buffer + append-only graded XP entry blocks (under `## Graded XP entries`). New sidecars are scaffolded from `_TEMPLATE_experience.md`. **Graded entries** are written by `/level --xp` only; direct edits to them violate `policy-skill-progression` Rule 5. The **`## Unrated journal` buffer** is the one part the invoked skill may write to directly — a narrow, explicit Rule 5 carve-out, because its stubs are *unrated* (observation, not graded XP) per `policy-skill-progression` Rule 6.

**Why:** The sidecar is the qualitative trail the metrics can't carry (`policy-skill-progression` Rule 6). Keeping its *shape* defined here — and lint-checked for existence + `xp_total` — means the leveling system can rely on every `used`+ skill having a readable, parsing log. The `## Unrated journal` section separates cheap continuous observation from periodic graded review (WS1, US-AGORA-009).

**Where enforced:** `validate_skill_frontmatter.py --levels` check 3 (existence + parse + `xp_total`). `--fix` scaffolds it (including the `## Unrated journal` section). Graded content is written exclusively by `/level --xp` (driven by `/agora --end` step 2.3b *evaluate-the-stubs*); the unrated buffer is appended to by the invoked skill mid-session.

### 6. Policy frontmatter carries a domain attribute

**What:** Every `.claude/policies/policy-*.md` frontmatter carries a `domain:` field with one of seven canonical enum values:

| Domain | Covers | Example policies |
|--------|--------|------------------|
| `discipline` | Cross-cutting governance — when to commit, when to nod, how to spawn, how to route | `policy-commit-discipline`, `policy-four-eyes`, `policy-spawns`, `policy-skill-routing` |
| `authoring` | How to write skills / policies / Issues — frontmatter shape, documentation discipline, Issue templates | `policy-skill-authoring`, `policy-documentation`, `policy-issue-templates` |
| `ui` | Front-end conventions, wireframes, surface discipline, page zone vocabulary | `policy-frontend-conventions`, `policy-ui-wireframes`, `policy-ui-surface-discipline`, `policy-page-zones` |
| `i18n` | Translation pipeline + gettext discipline across 12 locales | `policy-i18n` |
| `testing` | Test-suite conventions (Selenium opt-in, page-objects, in-PR fix discipline) | `policy-selenium-coverage` |
| `migration` | Rewriting existing templates without silent regression (inventory + map + decide before delete) | `policy-migration-discipline` |
| `leveling` | The skill leveling system — levels, metrics, gates, ceremony, XP awards | `policy-skill-progression` |

`_TEMPLATE.md` carries the `domain:` placeholder so `/document --policy <slug>` includes it from creation.

**Why:** As the policy layer grew past 15 active policies, the lack of structural categorization made cross-policy patterns invisible. Browsing `.claude/policies/` required opening each file; "show me the UI-related policies" was a prose-grep through `README.md`. The `domain:` field makes the categorization machine-readable (aggregable in `docs/stats.yaml`, visualized on the observability dashboard, surfaced by `/level --board --policies` in the future per US-AGORA-006) and lint-enforced (a new policy cannot ship without explicit domain assignment). Originating session: session 2026-05-23 Phase D4, surfaced via the bidirectional gate per `policy-four-eyes` Rule 5.

**Where enforced:** `scripts/checks/validate_skill_frontmatter.py` extends its policy validation pass to require `domain:` + enum-check the value against the seven-value vocabulary. `--fix` does NOT auto-set the value (requires human judgment per the per-policy assignment table above) — surfaces as manual-fix-required. The README's `## Active policies` section is grouped by domain for human-facing browsing.

**Example:**

```yaml
---
name: skill-progression
title: "Skill progression — four levels with metric gates …"
status: active
domain: leveling          # ← required; one of the 7 canonical values
related_skills:
  - level
  - agora
related_lint_rules: []
---
```

### 7. Cite a rule by its title, a step by its heading

A reference inside prose is a third kind of copy — neither verbatim nor generated — and
until round 8 nothing held it to its source: T-116 renumbered `policy-frontend-conventions`
correctly and thirteen citing lines in five skills kept the old numbers, so they pointed at
the wrong rules while every lint stayed green. The citation mode of
`scripts/checks/check_record_consistency.py` (US-AGORA-087, `record_consistency.yaml`
`mode: citation`) resolves four kinds against their sources: a **rule** by the policy's
heading (the ids `policy-<slug>.R<n>` the ontology derives, US-AGORA-088), a **step** by the
skill's numbered heading, a **command** by the click registry, a **path** by the tree.

**Write the title beside the number** — `Rule 8 (*form inputs use the canonical macros*)` —
so the lint can prove the citation right or wrong; a bare `Rule 8` can only be warned, and
the bare count is a ratchet (`scripts/baselines/citation_baseline.json`) that only falls.
A quoted title that belongs to another rule of the same policy is a re-pointed citation and
fails `--check`. A command cited before it is built is named `planned:` with its story in
the registry; a retired thing is called retired on the line, which exempts it.
`python scripts/checks/check_record_consistency.py --census` lists every rule citation with
the heading it resolves to.

## Common mistakes

- **Restating the quoting rule in a skill prompt.** It now lives here; skills reference `policy-skill-authoring`, they don't re-enumerate the risky-char table. (This policy exists *because* four surfaces had diverged enumerations.)
- **Hand-editing `level:` / `role:` / `epithet:` to "fix" a lint failure.** Those are `/level`-only fields. A lint failure on them means the skill's actual level is wrong, or `/level` was bypassed — fix the cause, not the field.
- **Adding a `## Claims at this level` section with vague claims to pass the lint.** The lint counts bullets; the *quest* (a human gate) checks they're real invariants other skills depend on. Three bullets of fluff passes the script and fails the promotion.
- **Forgetting `experience.md` when promoting draft → used.** `--fix` scaffolds it, but the XP backfill is a `/level` concern — scaffolding gives an empty log, not a populated one.
- **Authoring a new policy without `domain:`.** The lint fails pre-commit; `--fix` won't auto-set the value because picking the right domain requires reading the policy's intent. Re-run `/document --policy` if scaffolding fresh, or hand-edit the frontmatter from the Rule 6 vocabulary table.

## See also

- [`policy-skill-progression`](policy-skill-progression.md) — the dynamic counterpart: levels, metrics, gates, promotion/regression, naming ceremony, XP awards. This policy owns the artifact; that one owns the transitions.
- [`policy-documentation`](policy-documentation.md) — Rule 3 carries the ≥3-places consolidation threshold that motivated this policy.
- `scripts/checks/validate_skill_frontmatter.py` — the enforcement arm (`--levels` default ON, `--fix` auto-quote + experience.md scaffold).
- `.claude/skills/_TEMPLATE_experience.md` — the experience.md scaffold source.
- `.claude/skills/level/SKILL.md` — the exclusive writer of leveling frontmatter fields.
- `.claude/skills/learn/SKILL.md`, `.claude/skills/agora/SKILL.md` — reference this policy for the frontmatter rule instead of restating it.
- Lint: enforced by the standalone `validate_skill_frontmatter.py` script, not a `requirements_lint` `Rxxx` rule (hence `related_lint_rules: []`).
