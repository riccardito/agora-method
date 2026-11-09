---
name: inspect-pipeline
description: "Skill-system meta-audit — list skills by declared category, flag mismatches between front-matter and behaviour, detect knowledge that should be in a policy, surface under-referenced policies (drift risk), check cross-reference health between skills and policies. Periodic dry-run inspection of the .claude/ directory itself; NOT for per-feature work. The --session mode audits the skill system through the lens of one lived /agora session. Read-only: it surfaces the gaps (including the pipeline diagram's consistency in the skills README); fixes go through /learn and /document."
argument-hint: "[--audit (default) | --policies | --drift | --session <file>]"
level: hardened
promoted_at: 2026-06-20
role: "the registrar"
epithet: "Diogenes — the iconoclast with the lamp"
---

> **Journal-at-source** (policy-skill-progression Rule 6): when you finish a unit of work in a session, append ONE unrated stub to [`experience.md`](experience.md) `## Unrated journal` — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`. One line, lighter than the session Log; `/agora --end` 2.3b grades it.

# Skill-System Meta-Audit

Audits **the skill system itself** — `.claude/skills/`, `.claude/policies/`, the cross-references between them, and the consistency between what skills *claim* (front-matter description) and what they *do* (SKILL.md body). Run periodically when the system has accumulated drift, e.g. after a wave of skill cleanups, before a "are we ready to commit to this setup?" review, or when something feels off.

This is a **meta** doctor — its scope is the `.claude/` directory, not any feature or entity. Modes 1–3 audit the system **statically** (the files as they sit on disk); Mode 4 audits it **dynamically** — through one lived `/agora` session, where the gap between what a skill claims and what it does shows up as something the user had to correct by hand.

## When NOT to use this skill

| Need | Use instead |
|------|-------------|
| Audit one entity's UI surface | `/check-ui-entity` |
| Audit Python test coverage | `/check-coverage` |
| A test plan or feedback triage for **one story** | `/iterate` — the loop's manager; this skill audits the pipeline through a session's lens (`--session`), never one story's loop (the three-sided grain, US-AGORA-061) |
| Patch a misbehaving skill (after this audit surfaces one) | [`/learn`](../learn/SKILL.md) |
| Author a missing policy (after this audit surfaces one) | [`/document`](../document/SKILL.md) `--policy` |

`/inspect-pipeline` **surfaces gaps**; the fixes go through the right tool above.

---

## MODE 1 — `--audit` (default)

Full system audit. Produces a structured report with green / yellow / red verdict.

**The audit's lens is the Agora declaration** —
`docs/references/agora/agora-declaration.md`
§0 (the seven statements) and §3 (the record's seven red flags). Every finding names the
statement it violates as `AGORA-DECL §<n>`; a finding that names none is either a new
statement or a new flag, and is reported as such rather than filed under taste
(US-AGORA-054; the declaration's §5.3 binds this mode).

### 1.1 — Skill inventory

Walk `.claude/skills/<name>/SKILL.md`. For each, parse:

- `name` (frontmatter)
- `description` (frontmatter)
- `argument-hint` (frontmatter)
- The body's section headings (extract `^## ` and `^### ` from the markdown)

The static file-shape contract a SKILL.md must satisfy (frontmatter fields + body sections by level, quoting) is [`policy-skill-authoring`](../../policies/policy-skill-authoring.md), enforced by `scripts/checks/validate_skill_frontmatter.py --levels`. A structural mismatch this audit surfaces that the lint *should* have caught is a finding against the lint, not just the skill.

### 1.2 — Categorize each skill

The skills fall into four categories. Tag each one:

| Category | Examples | Trait |
|----------|----------|-------|
| **Per-feature** | `new-story`, `implement-story`, `fixbug`, `deploy` | Used during the build of a specific feature |
| **Cross-cutting / doctor** | `check-coverage`, `check-ui-entity`, `selenium`, `manage-translations` | Periodic health checks; audit + drill modes; outside per-feature pipeline |
| **Meta** | `learn`, `document`, `iterate`, `inspect-pipeline` | Operates on the skill system or iteration loop |
| **Specific** | `update-story`, `feature-plan` | Specific narrow purpose; not pipeline-stage but not doctor either |

Use the description's "When NOT to use" table (if present) and the body's mode list as primary signal. If a skill has 3+ modes (`--audit / --add / --run`-shape), it's almost certainly a doctor.

### 1.3 — Description-vs-behaviour cross-check

For each skill, ask:

1. **Does the description claim a category?** ("doctor", "manager", "auditor" → cross-cutting; "build", "scaffold" → per-feature; "patch", "captures" → meta).
2. **Does the body match?** A skill described as a doctor should have multiple modes and a "When NOT to use" table. A skill described as per-feature should have phases (Phase 1, Phase 2, …) and a clear sequence.
3. **Mismatch?** Flag it: "skill X is described as Y but body looks like Z".

Common mismatches to surface:
- Description says "doctor / manager" but body has only one mode → either rename the skill or actually add modes.
- Description says "use during build" but body is a static reference → consider moving the content to a policy.
- Description has long "Use when..." prose but body is much narrower → the description over-promises.

### 1.4 — Pipeline placement check

The pipeline is:

```
Per-feature:   /new-story → /implement-story → /fixbug → /deploy
                                  └── /iterate (test plan, feedback)
Cross-cutting: /learn · /document · /check-coverage · /check-ui-entity
               · /selenium · /manage-translations
Meta:          /inspect-pipeline (this skill)
```

Check `.claude/skills/README.md`:
- Does the workflow diagram match the categorization above?
- Do the "Cross-cutting skills" list and the table descriptions agree on category?
- Are skills cross-referenced in next-steps from the right side of the boundary? (E.g. `/check-coverage` should NOT be in `/implement-story` Phase 5 next-steps as a per-feature step — it belongs in the cross-cutting block.)

Surface drift: skills listed in two categories, skills missing from the pipeline diagram entirely, etc.

### 1.4b — Dormancy read (the wire registry, US-AGORA-061)

Read `docs/stats.yaml` `agora.skills.records[]` — `callers` (the registry's
declared call sites, verified in the caller's text by Check 10 of the frontmatter
validator) and `called_by` / `called_by_steps` (the Log-mention proxy, window 30).
A skill with registered callers and `called_by` 0 is **the dormancy finding,
caller named** ("`check-coverage` — 4 registered callers, 0 sessions: `compass:#461
C9` is the wire that should fire first"); a skill with `callers: []` is a routing
question (`policy-skill-routing`), not a wire. A `type: plaza` session runs `/plaza`
without a Log heading, so its 0 is the proxy's blind spot until US-AGORA-062's
Evidence lines replace the count.

### 1.5 — Verdict

| Status | Trigger |
|--------|---------|
| 🟢 Green | All skills' descriptions match their bodies; pipeline diagram is up-to-date; cross-cutting / per-feature boundaries are clean. |
| 🟡 Yellow | 1–2 description mismatches OR the README diagram is stale OR a skill is in two categories. |
| 🔴 Red | 3+ skills mis-categorised, OR a skill prompts behaviour that contradicts its description, OR pipeline diagram doesn't reflect actual skill cross-references. |

Output a one-paragraph summary, then the per-skill table, then the
fix list (each item dispatchable to `/learn` for skill content,
direct edit for README, or `/document` for new policies).

---

## MODE 2 — `--policies`

Policy-side audit. Different scope from skill audit — focuses on the
policy lifecycle, cross-references, and CLAUDE.md mirror health.

### 2.1 — Policy inventory

Walk `.claude/policies/policy-*.md`. For each:

- Parse frontmatter: `name`, `title`, `status`, `related_skills`, `related_lint_rules`
- Read the body's TL;DR

### 2.2 — Reference count

For each policy, count how many `.claude/skills/<name>/SKILL.md` files
reference it (search for `policy-<slug>` in skill prompts). Compare
to the policy's `related_skills:` list:

- **Symmetric** (skill is in `related_skills:` AND skill references the policy): healthy
- **Asymmetric A** (skill is in `related_skills:` but no reference in skill body): policy claims a relationship the skill doesn't carry — fix by adding the reference to the skill
- **Asymmetric B** (skill references the policy but isn't in `related_skills:`): missing reciprocity — fix by updating the policy's frontmatter

**This is Check 11 of `scripts/checks/validate_skill_frontmatter.py` (US-AGORA-061):**
direction A fails the lint, direction B warns and `--fix` appends — this step reads
the check's output rather than re-counting by hand.

### 2.3 — CLAUDE.md mirror check

Read CLAUDE.md `## Policies` section. For each active policy:

- Is the TL;DR mirror present?
- Is the mirrored TL;DR **verbatim** from the policy file? (line-by-line text match — the framework requires this)
- Are deprecated policies still mirrored? (should have been removed)

A drifted mirror is the most common silent failure: the policy's TL;DR
gets edited, the mirror doesn't, and the always-loaded version (CLAUDE.md)
no longer matches the on-disk file. Surface every drift.

### 2.4 — Under-referenced policies (drift risk)

Policies with **0–1 skill references** are at risk:
- 0 references → why does the policy exist? Either delete or wire up.
- 1 reference → only one skill cares; consider whether the rule is actually cross-cutting (the bar for a policy) or whether it should live inside that skill's prompt.

Surface every under-referenced policy. Don't auto-delete — surface for user decision.

### 2.5 — Status enum check

Every policy has `status: draft | active | deprecated`. Check:
- `draft` policies that have been mirrored into CLAUDE.md (shouldn't be — only `active` mirrors)
- `active` policies that have NOT been mirrored or referenced (the framework's "active is a commitment" rule)
- `deprecated` policies still in the `## Active policies` section of `.claude/policies/README.md`

---

## MODE 3 — `--drift`

Looks for **knowledge duplication** across skill SKILL.md files —
candidates for extraction to a new policy.

### 3.1 — Scan for repeated rules

For every skill, extract bullet lists, numbered lists, and tables.
Look for content that appears in 2+ skills with high text similarity:

- **Identical paragraphs** across 2+ skills → high-confidence candidate
- **Same rule, different wording** ("never use _ as discard" vs "don't shadow `_`") → medium-confidence candidate
- **Same example code** across 2+ skills → low-confidence candidate (might be intentional reference)

Use grep + a similarity heuristic (shared phrases of 5+ words). For
small skill systems (~15 files), a manual scan is feasible too.

### 3.2 — Surface candidates

```markdown
## Drift Candidates — Knowledge Duplicated Across Skills

### High-confidence (identical paragraph in 2+ skills)

1. **"Never @click.stop on #modal-box"** — appears in:
   - `/fixbug` SKILL.md L26 (`#modal` tag)
   - `/check-ui-entity` Layer 3.2
   - `/implement-story` Phase 3.3

   Already in `policy-frontend-conventions` Rule 4. ✓ — but the
   text in fixbug isn't a reference, it's a paraphrase. Should
   collapse to a one-line `Apply policy-frontend-conventions Rule 4`
   reference.

2. ...

### Medium-confidence (same rule, different wording)

1. **i18n discard target rule** — `_` shadow gotcha
   - `/implement-story` SKILL.md mentions Python and Jinja
   - `/fixbug` doesn't but probably should

   Already in `policy-i18n` Rule 2. Check that fixbug `#i18n` tag
   references it.

2. ...
```

### 3.3 — Suggest fixes

Each duplication candidate gets a recommendation:

- **Already in a policy** → trim the skill to a `Apply policy-X Rule N` reference
- **Should be in a policy** → propose a new policy via `/document --policy <slug>`
- **Intentional repetition** (e.g. shared example code) → mark as "OK, just keep an eye"

Don't auto-extract policies. Surface the candidates; the user decides
which warrant the abstraction.

---

## MODE 4 — `--session <file>`

Audits the skill system **through one lived session**. Where Modes 1–3
read the `.claude/` files statically, this mode reads a closed (or
closing) `/agora` session protocol file and asks: *given what actually
happened, where is the skill system drifting?*

This is the mode [`/agora --end`](../agora/SKILL.md) invokes at step
2.3. It can also be run by hand on any session file in
`.claude/sessions/`.

### 4.1 — Read the session

`$0` is a path to a `.claude/sessions/<id>.md` file (or a bare session
id — resolve it under `.claude/sessions/`). Read:

- frontmatter — `type`, `skills_invoked`, `stories_touched`, `commits`
- the **Session plan** — what was queued vs what got ticked
- the **Log** — the running record of what each skill did
- the **Agora findings** — the user/conversation already flagged these
- the **Open threads** — what didn't finish

### 4.2 — Cross-check each invoked skill against its SKILL.md

For every skill in `skills_invoked` (and every `/skill` mention in the
Log), open its `SKILL.md` and ask the questions below. **`/agora` is
always one of them** — it brackets every session, so it is always in
scope here; this cross-check *is* the Agora self-audit that
`/agora --end` step 2.4 relies on. A meta skill with no doctor above it
gets audited by being treated as just another invoked skill.

Open the skill's `SKILL.md` and ask:

1. **Did it behave as written?** The Log says `/implement-story` did X;
   the SKILL.md says it should do Y. Match or drift?
2. **Did the user have to correct it?** Search the Log for "had to",
   "instead", "manually", "the skill didn't" — every manual correction
   is a candidate `/learn`.
3. **Was it invoked at the right time?** A skill used out of pipeline
   order, or skipped where it applied, points at either a usage problem
   (coaching — `/agora` does that) or a description that doesn't make
   the trigger obvious (a skill-description fix).
4. **Did the queue hold?** Plan items queued but never ticked, or work
   done that was never queued — surfaces planning gaps or scope creep.

### 4.3 — Surface the findings

Same three buckets as the static modes, but sourced from the session:

- **Skill drift** — a skill that needed manual correction this session →
  `/learn --from-session <file>` (it reads the finding straight from the
  file).
- **Policy gap** — a rule the conversation stated from memory more than
  once, or a cross-cutting correction → `/document --policy <slug>`.
- **Missing-skill candidate** — a repeatable procedure done ad-hoc this
  session with no skill to carry it → propose a new skill via `/learn`.
- **Description / categorisation mismatch** — usage this session
  contradicted the skill's declared category or "When NOT to use"
  table → direct edit or `/learn`.

### 4.4 — Verdict + dispatch list

| Status | Trigger |
|--------|---------|
| 🟢 Green | The session ran on-rails — skills behaved as written, no manual corrections, the queue held. |
| 🟡 Yellow | 1–2 manual corrections OR a plan item silently dropped OR one skill used out of order. |
| 🔴 Red | 3+ manual corrections, OR a skill behaved opposite to its SKILL.md, OR a repeatable procedure was done entirely by hand. |

Output: a one-paragraph summary, the per-skill cross-check table, then
the dispatch list — each item routed to `/learn --from-session`,
`/document --policy`, or a direct edit. This list is what
`/agora --end` step 2.5 hands to the user for confirmation.

The boundary with Mode 1: Mode 1 finds drift by **reading the files**;
Mode 4 finds drift by **watching the files get used**. A skill can pass
Mode 1 (description matches body) and fail Mode 4 (the body, when
followed, didn't actually work) — that gap is the high-value catch.

### 4.5 — Vocabulary sweep (grow the cheatsheet per-session)

WS4 (US-AGORA-013 /
RP-AGORA-003). A controlled vocabulary decays without a maintenance cadence — so
every `--session` run also sweeps the session record for **new Agora vocabulary**:

1. **Scan** the session Log + retro (Close-out) for terms used *as if* they were
   vocabulary but **absent** from `docs/references/agora/vocabulary-cheatsheet.md`:
   capitalised coinages, `x · y` pairings (the `bones · meat` shape), terms in
   scare-quotes, repeated domain phrases. Grep the cheatsheet to confirm absence.
2. **Surface** the candidates as a **4-eye gate** per
   [`policy-four-eyes`](../../policies/policy-four-eyes.md) — propose each term +
   the one-line definition it would carry + the cheatsheet group it belongs to.
3. **On the nod**, add the confirmed terms to the cheatsheet (correct group); a
   term that warrants a full definition is also flagged for
   `docs/wiki/feature-agora-vocabulary.md` (path config).
4. **Silent when empty** — when no vocabulary-shaped term surfaced, the sweep
   prints nothing (no ceremony when there's nothing to add).
5. **Incorporation (US-AGORA-042 — the lifecycle's declared last step).** The
   sweep also checks terms ALREADY in the cheatsheet against the frequency
   threshold: a term mentioned in **≥5 of the newest-30 session files** (the
   adoption surface's own window) that still has only a table description is
   proposed for **incorporation** — a spec, a structural home, and (where it
   has a boundary moment) an `EVENTS.md` chapter — at the same 4-eye gate.
   Coined → adopted → circulating → **incorporated**: promotion is a call,
   not luck (even *north star*, the good case, got its COMPASS entry by luck
   of the moment). Arc, AVOR and close-out were the first three walked
   through (US-AGORA-042). Silent when nothing crosses.

The `bones · meat` coinage (2026-05-19, adopted by hand) is the worked precedent —
this sub-step makes that loop a per-session cadence. (An ad-hoc `--vocab` mode for
sweeping outside a session is a possible future addition; the per-session sub-step
is the must-have.) `/agora --end` 2.4 already prepends the
`### Step 2.4 — /inspect-pipeline --session` heading, so this sweep's M1 is counted.

---

## Mode dispatch

Parse `$ARGUMENTS`:

| User says | Mode |
|-----------|------|
| (nothing) / "audit" / "health" | **Mode 1** (skill-system audit) |
| `--policies` / "policy health" | Mode 2 |
| `--drift` / "duplication" / "extract candidates" | Mode 3 |
| `--session <file>` / a `.claude/sessions/` path or id | Mode 4 (session-driven audit) |

---

## Notes

- This skill is **read-only** — it audits and reports. Fixes go through `/learn` (skill content), direct edit (README), `/document` (new policy), or `/document --update <slug>` (policy mirror).
- **Modes 1–3 run periodically** — once every few rounds of skill cleanup, before a "are we ready to commit?" review, or when the system feels off. NOT after every feature. **Mode 4 runs per session** — it is invoked by `/agora --end` (step 2.4) on the closing session file, and is the only mode meant to fire on a regular cadence.
- The audit's verdict is meant to surface what to look at next, not to grade. A 🔴 result usually has 1–2 actionable fixes that bring it back to 🟢; the skill system is small enough that drift catches up fast once surfaced.

---

## Initialisation

**What this skill reads before acting** (US-AGORA-041): Modes 1–3 read the
`.claude/` tree statically — every SKILL.md's frontmatter + headings, the
policies' TL;DRs + `related_skills:`, the README roster; Mode 4 reads the
named session file whole plus every invoked skill's SKILL.md (with `/agora`
always in scope). The audit's evidence is what is on disk, never an
impression.

**Self-model:** the lamp — Diogenes looking for the honest skill. It
surfaces and routes; it never patches (Claim 1). A gap noticed mid-audit (a
surface its modes do not read but should) lands as a 🟡 journal stub in
[`experience.md`](experience.md).

## Claims at this level

The invariants other skills and the user depend on `/inspect-pipeline` to hold
(the `hardened`-tier commitments; each is the unit `/learn` checks for
contradiction per `policy-skill-progression` Rule 4).

1. **The audit is read-only — it surfaces, it never patches.** Across all four modes `/inspect-pipeline` produces a verdict and a dispatch list; it never edits a SKILL.md, policy, or README itself — fixes route to `/learn`, `/document`, or a direct edit.
2. **Every `--session` run produces a verdict and a fully-routed dispatch list — no un-actioned finding.** Mode 4 always emits a 🟢/🟡/🔴 verdict plus a per-skill cross-check where every finding is routed to `/learn --from-session`, `/document --policy`, or a direct edit; that list is what `/agora --end` step 2.5 hands the user.
3. **Every `--session` run audits `/agora` itself — the orchestrator is always in scope.** Because `/agora` brackets every session, Mode 4 treats it as an always-present invoked skill; this cross-check *is* the Agora self-audit that `/agora --end` step 2.4 depends on, so a meta-skill with no doctor above it never goes unaudited.
4. **Mode 4 fires per session; Modes 1–3 fire periodically — the cadences do not blur.** Mode 4 (`--session`) is the only per-session mode (invoked by `/agora --end` 2.4); Modes 1–3 run only periodically, never after every feature.
5. **The drift-detection contract is to nominate, not to extract.** Mode 3 (`--drift`) and Mode 2's under-referenced-policy check surface duplication and zero/one-reference candidates for user decision; they never auto-create, auto-delete, or auto-collapse a policy.
