---
name: skill-progression
title: Skill progression — leveling, metrics, promotion, regression
status: active
domain: leveling
related_skills:
  - learn
  - inspect-pipeline
  - agora
  - level
  - design
  - document
  - plaza
  - write
related_lint_rules: []
---

# Skill progression policy

> **Authored:** 2026-05-17, session session 2026-05-17 Phase C. Thresholds + peer-framework grounding folded in from spawn `2026-05-17-skill-progression-research` (5-section synthesis: Anthropic Skills / Cursor / Cline / Copilot / AGENTS.md + game-design primitives + file-backed metrics). No peer framework has a formal level system — Agora is in genuine new territory; the prior art validates the *shape* (file-backed, frontmatter-resident, git-audited) but not the *content*.

## TL;DR

1. **Four levels — `draft / used / hardened / reference`.** Each level has a one-line capability claim, an **all-of metric gate**, and a **quest** (a deterministic file-checkable artifact that must exist for promotion). A skill is exactly one level at any time; the level lives in the SKILL.md frontmatter (`level:` + `promoted_at:` + at `used`+ `role:` + at `hardened`+ `epithet:`). New skills start at `draft`. Levels apply to **skills only**, never policies — policies have their separate `status:` enum (`draft / active / deprecated`).
2. **Five quantitative metrics + one qualitative trail.** Metrics are file-backed and deterministic — computed from `.claude/`, `docs/`, and Git history alone. **M1** invocation count (since last promotion-marker commit), **M2** correction load (`/learn` patches against SKILL.md since promotion), **M3** redo rate, **M4** reference depth (soft signal), **M5** cross-reference fan-in, **M6** last-update recency. **The qualitative trail is XP** — the per-skill experience log (Rule 6) carrying the *narrative* the metrics can't. Metrics gate; XP tells the story.
3. **Promotion is human-confirmed via `/level <skill> --promote`. No auto-promote, ever.** The system *surfaces* eligibility (computed "candidate-for-<next>" state at read time); the user confirms. The promotion-marker commit subject `level(skill): promote <name> <from> → <to>` is the immutable reference point for M1/M2's "since last promotion" computation. Every promotion + regression appends one entry to `IMPROVEMENTS.md`. Promotion `used → hardened` includes a **naming ceremony** (Rule 7) and requires a **`## Claims at this level` section** in the SKILL.md body (Rule 8).
4. **Regression is narrow — only on a `/learn` patch that contradicts a named claim the skill makes at its current level.** Threshold-based auto-regression is forbidden. High M2 surfaces as a `/level <skill>` audit finding ("3 patches since promotion — review for regression?") but never silently demotes. The contradicting-patch shape: `/learn` reads the `## Claims at this level` section of any `hardened`+ target and asks *per claim* whether the patch contradicts it. If any answer is yes, `/learn` calls `/level <skill> --regress --corrects <sha>`.
5. **`/level` is the only authorised writer.** Modes: `/level --board` (every skill ranked — the "character sheet" surface; without it the leveling system is invisible and dies), `/level <skill>` (audit one skill — "Holding tier" + "Reaching for next" two-column view), `/level <skill> --promote|--regress` (the level writes, including the naming ceremony), `/level <skill> --xp +<N> "<snippet>"` (append one XP entry — the granular writer, called by `/agora --end` and by hand). Direct edits to `level:` / `promoted_at:` / `epithet:` / experience.md bypass the audit trail and are a discipline violation.
6. **Each skill at `used`+ carries an append-only experience log at `.claude/skills/<name>/experience.md`** — markdown frontmatter (`xp_total`, `xp_by_level`, `last_xp_at`) + a `## Unrated journal` capture-at-source buffer + per-entry graded blocks (date · session · +XP · 🟢 success / 🟡 lesson · one-paragraph snippet). **Capture-at-source:** the invoked skill appends a one-line *unrated* stub to its own buffer when it finishes work in-session (a narrow carve-out from Rule 5 — unrated, so skill-writable). **Grade-at-end:** `/agora --end` step 2.3b reads the buffer, rates each stub as a 4-eye gate, and `/level <skill> --xp` converts + clears it. The `hardened → reference` gate adds `xp_total ≥ 200 across ≥ 15 sessions` (XP is the trajectory signal at the top tier; lower tiers gate on metrics alone). **The sidecar also holds `## Level history`** (US-AGORA-057, `AGORA-DECL §3`): every level transition `/level` writes and every `/learn` patch entry lands there, never in SKILL.md — whose own `## Level history`, where one still exists, is legacy and only shrinks, so the prose ratchet stays green on a lesson.
7. **Naming ceremony fires at `used → hardened`.** Three identity steps across the four levels: (i) at `draft → used`, the user sets a one-line `role:` frontmatter descriptor (*"the inspector"*, *"the doctor"*); (ii) at `used → hardened`, the **ceremony** — `/level` presents the skill with its capabilities + experience log + the Agora-philosophers catalog (Socrates / Aristotle / Euclid / Diogenes / Hero / Callimachus / Plato / Pythagoras / Heraclitus / Thales / Solon / Pericles / Anaxagoras / Theophrastus), the skill proposes ONE epithet + a one-sentence justification, user nods via 4-eye gate, `epithet:` is written; (iii) at `hardened → reference`, the epithet is canonicalized as a `## Identity` opening section that tells the story of why it fits.
8. **Hardened+ skills carry a `## Claims at this level` section in the SKILL.md body** — 3–5 explicit commitments the skill makes that other skills depend on. Each claim is one sentence naming an invariant. The section is a **quest requirement** for the `used → hardened` promotion (a skill that cannot enumerate 3 claims isn't yet hardened). At `hardened → reference`, the claims tighten — a `reference`-tier skill's claims read like rule statements that *other* skills cite. `/learn` reads the section per Rule 4: each named claim is the unit of the contradiction question.

## Why this exists

An early session (2026-05-16) evolved Agora's skills unevenly. `check-ui-entity` deepened into a reference tier (tier philosophy, plugin-zone rules, sticky icon-twin spec — ~3000 lines of detailed procedure). `fixbug` accumulated tag fragments — each a pointer to a single past incident, valuable but un-systematised. `agora` itself stayed mostly procedural. No mechanism existed to answer "which skill needs the next round of work?"

The user's retrospective phrasing (2026-05-17, parent session):

> Introduce a skill leveling system with levels, titles, abilities, and
> measurable signals. Define learning references and track them in skill
> passports. Strengthen the learning environment for abstract reasoning
> skills.
>
> We currently lack formal metrics for skill performance. We need
> definitions for reliability, consistency, correction load, artefact
> quality, and human confirmation load. Without metrics, leveling
> remains conceptual.

Two failure modes the policy guards against:

1. **Drift-blind investment.** Without a level signal, the conversation defaults to "the skill the user just used" for further refinement. Skills that should be retired or consolidated keep accruing patches; skills that should level up don't get the deeper procedural work that earns the next tier.
2. **Patches that contradict tier claims.** A `reference`-level skill claims procedural completeness; a `/learn` patch that materially changes its behaviour contradicts that claim. Without a regression mechanism, the level field rots into a self-flattering label.

The leveling system's deliberate design constraints:
- **File-backed** (no runtime DB) — Agora's whole architecture rule
- **Deterministic** — same inputs always produce the same level diagnosis
- **Git-auditable** — every promotion is a commit, every regression too
- **Useful at decision-time** — `/level --board` is the answer to "what should we work on next?"

## The vocabulary — four levels

A skill is exactly one of:

### `draft`

**Capability:** The skill exists, has frontmatter that parses, and has been used at least once. May be incomplete (missing modes, light on examples, unclear "When NOT to use").

**Constraint:** Not yet load-bearing. A session that depends critically on a `draft` skill is taking on risk. `draft` skills are candidates for either consolidation (does another skill do this?) or maturation.

**Criteria — the gate to `draft`:** frontmatter passes `validate_skill_frontmatter.py`. Body has at least one `## ` heading (i.e. has structure, not just a sentence).

### `used`

**Capability:** Invoked in at least one closed session and didn't require manual correction during that session. The skill works for its declared trigger.

**Constraint:** Cannot be the basis for cross-cutting claims. If two other skills both want to delegate the same sub-task to this skill, the duplication is a flag — at `used` we don't yet know the skill's contract is stable enough to be a dependency.

**Criteria — gate `draft → used`** (all-of):
- M1 ≥ 1 (one closed-session invocation)
- **Quest:** frontmatter validation passes; SKILL.md body has at least one `## ` heading

### `hardened`

**Capability:** Invoked across multiple sessions, has a "When NOT to use" table that has held up under fire, has been cross-referenced by ≥3 other skills or policies, and has weathered ≤1 correction since its `used` promotion. The contract is stable.

**Constraint:** Cannot claim "the canonical pattern" — that's the `reference` tier's job. Still subject to incremental patching as adjacent areas evolve.

**Criteria — gate `used → hardened`** (all-of, measured since the `used` promotion-marker commit):
- M1 ≥ 10 (invocations since promoted_at)
- M2 ≤ 1 (correction load since promoted_at)
- M5 ≥ 3 (cross-reference fan-in)
- **Quest (three artifacts must exist):**
  1. A `## When NOT to use` table OR equivalent boundary-statement section. Mode-shape skills (doctors with `--audit / --add / --run / …`) must list all modes.
  2. A `## Claims at this level` section with **at least 3** named claims (per Rule 8). A skill that cannot enumerate 3 invariants isn't hardened.
  3. An `epithet:` proposed via the naming ceremony (Rule 7), confirmed by the user, written into frontmatter.

> **XP gate at this tier is informational only** — the policy does not block this promotion on `xp_total`. The hardened tier is where XP *starts mattering* as a signal; the trajectory becomes load-bearing at the next tier.

### `reference`

**Capability:** The skill's body is the **doctrine** for its area — other skills cite *it* rather than re-stating the rules. Has authored or anchors at least one policy. Carries a **mastery marker** surfaced on `/level --board` (e.g. *"cited by N other skills"*, *"authored policy-page-zones"*). Patches since promotion are exceptional events.

**Constraint:** Cannot promote further. If the skill's scope outgrows the tier (more areas absorbed), the answer is *split into sibling reference skills* — never invent a `master` tier.

**Criteria — gate `hardened → reference`** (all-of, measured since the `hardened` promotion-marker commit):
- M1 ≥ 30
- M2 ≤ 1
- M5 ≥ 5 (with at least one being a *policy* listing this skill in `related_skills:`)
- M4 ≥ 300 lines (sanity check on doctrinal density, not a hard rule)
- **XP trajectory:** `xp_total ≥ 200 across ≥ 15 sessions` since `used` promotion (per Rule 6 — XP is the trajectory signal at the top tier)
- **Quest (two artifacts must exist):**
  1. The skill has authored OR is the primary entry in a `policy-*.md` file's `related_skills:`
  2. A `## Identity` opening section that tells the story of the epithet — canonicalizing the `epithet:` frontmatter into doctrine prose (per Rule 7 step iii). Other skills may then cite this skill *by epithet*.

**Worked example today (2026-05-17):** `check-ui-entity` is the closest `reference` candidate — tier philosophy, plugin-zone rules, sticky icon-twin spec, ~3000 lines. The mastery markers it would carry: *cited by ≥4 sibling skills*, *its structural pattern mirrored by check-page and fixbug*. Whether it's at the gate today is the first `/level --board` finding once the skill ships.

> **Thresholds are tentative — calibrate on real corpus.** The corpus is tiny (3 closed sessions as of 2026-05-17). First `/level --board` after 10 closed sessions surfaces "the threshold puts N skills at the gate; recalibrate?" as a self-finding.

## The rules

### 1. Levels are atomic — exactly one per skill, in frontmatter

**What:** Each SKILL.md frontmatter carries a `level:` field with one of the
four enum values. Plus a `promoted_at:` ISO date (`YYYY-MM-DD`) recording
when the current level was reached, and a `last_correction:` ISO date
recording the most recent `/learn` patch that touched the skill.

```yaml
---
name: check-ui-entity
description: "..."
argument-hint: "..."
level: hardened              # one of: draft | used | hardened | reference
promoted_at: 2026-04-12      # when current level was reached
last_correction: 2026-05-16  # most recent /learn patch
role: "the inspector"        # set at draft → used (one-line role descriptor)
epithet: "Aristotle — the categoriser"  # set at used → hardened (naming ceremony)
---
```

`role:` is mandatory at `used`+; `epithet:` is mandatory at `hardened`+. Both are written by `/level <skill> --promote` only — direct edits violate Rule 5.

**Why:** Co-location with the skill is the simplest passport — git-tracked
alongside the skill's own evolution, no sidecar files, no separate registry
file to merge-conflict on. The `/level --board` view computes
cross-skill ranking by reading all 18 frontmatters in one pass (same I/O as
`validate_skill_frontmatter.py`).

**Where enforced:** `/level` skill writes/reads these fields. `validate_skill_frontmatter.py --levels` enum-validates `level:` and checks the field/section requirements; a skill without `level:` defaults to `draft` at read time. The *static file-shape contract* these fields and sections must satisfy is [`policy-skill-authoring`](policy-skill-authoring.md) — **this policy owns the transitions between levels; that one owns the artifact at each level.**

### 2. Metrics are file-backed and deterministic

**What:** Six metrics, every one computable from `.claude/`, `docs/`, and Git
history alone. Reference point for M1/M2/M3: the most-recent **promotion-marker commit** (the commit with subject `level(skill): promote <name> <from> → <to>`; see Rule 3). Before the first promotion, the reference point is "all-time".

| # | Metric | Computation | Interpretation |
|---|---|---|---|
| **M1** | **Invocation count** | Count of `<skill>` in `skills_invoked:` lists across all `status: closed` `.claude/sessions/*.md` since the skill's last promotion-marker | Raw usage. **Lower bound on promotion eligibility** — a skill with M1=0 cannot promote past `draft`. |
| **M2** | **Correction load** | `git log --follow .claude/skills/<name>/SKILL.md` filtered to commits with `/learn` in the body OR subject prefix `docs(skill):` / `feat(learn):`, counted since the last promotion-marker — **minus the self-audit + cross-reference exclusions (see below)** | Patch frequency. **Low = stable. High = drifting.** A `reference`-tier skill with M2 > 1 since promotion is a regression candidate. |
| **M3** | **Redo rate** | Fraction of sessions where the skill is invoked AND the session Log has `^### .*\b/<skill>\b` heading appearing 2+ times | Proxy for "didn't work the first time". Imperfect (Log is prose); simple grep ratio is the first cut. |
| **M4** | **Reference depth** | `wc -l` of `SKILL.md` + count of `^## ` and `^### ` headings | Maturity proxy. Deep + many sections = `reference` candidate. Shallow + few = either `draft` or a deliberately narrow terminal skill (`/deploy` fine at its size forever). **Soft signal**, never a hard gate. |
| **M5** | **Cross-reference fan-in** | Count of other SKILL.md files containing `<skill>` outside their own frontmatter + count of `policy-*.md` files listing the skill in `related_skills:` | "How much does the system depend on this?" Fan-in ≥ 3 has earned an ecosystem place. Fan-in 0 fine for terminal skills (`/deploy`); a `reference` claim with fan-in 0 is a contradiction. |
| **M6** | **Last-update recency** | `git log -1 --format=%ci -- .claude/skills/<name>/SKILL.md`, days ago | Sanity check, not a gate. > 180 days untouched AND high M1 = either truly stable (good — `reference`) or being silently worked around (bad — surface as `/level <skill>` finding). |

**M2 self-audit exemption (WS-Meta, US-AGORA-015).** A skill that declares `self_audit_loop: true` in its frontmatter is patched by its **own** self-improvement loop *by design* — `/agora` is the canonical case: its `--end` steps 2.4–2.5 run an `/inspect-pipeline --session` self-audit that dispatches `/learn` patches *against `/agora` itself*. For such a skill, a high M2 is a sign of **health, not instability** — the exact opposite of what M2 is meant to catch (a skill that keeps needing fixes because it is *unstable*). So:

- **`/learn` adds a `Self-audit: <skill>` commit trailer** when the patch is dispatched by that skill's own `--end` self-audit (the dispatching session's audit subject equals the patched skill).
- **M2 for a `self_audit_loop: true` skill excludes commits carrying `Self-audit: <skill>`.** External `/learn` patches (a user correcting the skill from a normal session) still count — only the skill's *own loop* is exempt.
- This is a **precise** fix, not a blunt ceiling bump: it names *why* the orchestrator's M2 is high and exempts exactly that cause, leaving the `M2 ≤ 1` gate fully in force for genuinely-unstable skills. The exemption applies only to skills that *declare* the loop (today only `agora`).
- **Calibration case (first application):** `agora`'s patches since its 2026-05-17 `used` promotion are dominated by self-improvement of the orchestrator (the `--end` self-audit loop + feature work on its own session machinery). Those predate the trailer, so the first `used → hardened` audit classifies them by inspection as self-audit-originated → exempt M2 → gate met. The promotion-marker commit resets the M2 window, and future self-audit patches carry the trailer (deterministic from then on).

**M2 cross-reference exclusion (lived session 2026-06-20).** M2 is *correction* load, not *touch* count. A `/learn` / `docs(skill):` commit that only **adds a cross-reference** to the skill — a hand-off note, a "see also", a link emitted by *another* skill's `/learn` — does NOT count toward M2; only a commit that **corrects this skill's own contract** does. Judge by inspection at audit time (the same audit-time classification the self-audit exemption uses): read the commit's diff against the `SKILL.md`; an additive mention/link that leaves the skill's own behaviour unchanged is excluded, a genuine behaviour/contract change counts. **Driver:** `implement-story`'s `115bd306` led with a `check-page` patch and only *added* an implement-story hand-off note, yet M2 mechanically counted it as a correction and nearly blocked the `used → hardened` promotion — the 4-eye judgment call (cross-ref, not correction → M2=1) is now the codified rule. Unlike the self-audit exemption (gated on a declared `self_audit_loop:` + a trailer), this exclusion applies to **every** skill and is inherently inspection-based — there is no mechanical marker for "this commit only links me", so the audit-time diff read is the rule, not a fallback.

**Codification rate** (proposed initially as M4-alternate, rejected after spawn analysis): computing "fraction of invocations that produced a retrospective finding" requires parsing prose `Agora findings` blocks and matching each to a specific skill. Doable but fragile at corpus scale. **Skipped for first cut**; re-introduce when the corpus is large enough that the noise floor justifies the parsing cost.

**Why:** Deterministic + file-backed is the architectural constraint. No
runtime database, no user-rating, no LLM-judged "quality score" — all of
those break either the determinism or the file-backed rule. The six metrics
are the signals the level gates lean on (M1+M2+M5 are the load-bearing trio;
M3 is diagnostic; M4 is the soft `reference`-tier sanity check; M6 catches
stagnation).

**Where enforced:** `/level <skill>` and `/level --board` compute and report them. No CI gating today — metrics surface for human-in-the-loop decisions.

### 3. Promotion is human-confirmed; regression is narrow

**What — promotion:** A skill becomes "candidate-for-`<next>`" when all of its next-level criteria pass (all-of, not any-of: metric thresholds AND the quest). `/level --board` displays this candidate state as a computed view — it's NOT a stored level (no third intermediate frontmatter value). The user runs `/level <skill> --promote` to apply. Auto-promotion is forbidden.

The promotion event does five things in this order:

1. Re-runs the audit (`/level <skill>` internally) and refuses if any criterion no longer passes.
2. Edits SKILL.md frontmatter: bumps `level:`, sets `promoted_at: YYYY-MM-DD`.
3. Appends a `## Level history` block (or extends an existing one) at the bottom of SKILL.md:
   ```
   ## Level history
   - 2026-05-17 — promoted: used → hardened (M1=12, M2=0, M5=4; quest: When-NOT-to-use table present)
   - 2026-04-22 — promoted: draft → used (M1=3)
   ```
4. Commits with subject `level(skill): promote <name> <from> → <to>` — **the promotion-marker commit**. All subsequent M1/M2/M3 "since last promotion" computations reference this commit's date.
5. Appends a one-line entry to `IMPROVEMENTS.md`.

**What — regression:** Regression triggers ONLY when **a `/learn` patch contradicts a claim the skill makes at its current level**. This is judgment-heavy and explicit:

1. After `/learn` patches a skill, it asks the user: *"Does this patch contradict a claim the skill makes at its current level (`<level>`)? If yes, this is a regression event."*
2. If yes, `/learn` calls `/level <skill> --regress --corrects <new-commit-sha>` as the final step of its patch flow.
3. Regression bumps `level:` down one tier, appends a `regressed:` line in `## Level history` (with the contradicting commit sha), and commits with subject `level(skill): regress <name> <from> → <to> (corrects: <sha>)`.

**Threshold-triggered regression is forbidden.** A high M2 surfaces as a `/level <skill>` audit finding ("3 patches since promotion — review for regression?") but never silently demotes. The skill might be genuinely stable but evolving in scope. The "contradicts a claim" framing forces a qualitative judgment that prevents the spiral of auto-demotion churn.

**Why:** Promotion is a quality commitment — *"this skill is reliable enough to depend on at this level"*. Quality commitments belong with the human, not with auto-firing thresholds. The asymmetry between promotion (explicit gate) and regression (contradiction trigger) is deliberate: promotions advance with deliberate cost, regressions retreat with deliberate cause.

**Where enforced:** `/level <skill> --promote|--regress` writes the frontmatter + history block + IMPROVEMENTS.md entry. `/learn` integrates as its final step (the contradiction prompt + conditional `--regress --corrects <sha>` call).

### 4. `/level` is the only authorised writer; otherwise the field is read-only

**What:** `level:`, `promoted_at:`, `last_correction:` are managed by the
`/level` meta-skill and (for `last_correction:` only) by `/learn`. Direct
edits to these fields are a discipline violation — they bypass the
`IMPROVEMENTS.md` audit trail. Other skills may *read* the level (e.g.
`/learn` reads it to decide regression) but never write it directly.

**Why:** The audit trail is the integrity guarantee. Without
`IMPROVEMENTS.md` entries pairing every level change, the field is just a
self-flattering label.

**Where enforced:** Procedural — `/level` SKILL.md is explicit about being
the canonical writer. `/learn` SKILL.md only writes `last_correction:`. CI
could check for direct-edit violations (`git log -p` filter on
`level:` / `promoted_at:` outside `/level`-authored commits) but is not
gated today.

### 5. The leveling system is a discipline gate, not just a label — and applies to skills only

**What — skills only:** Levels apply only to `.claude/skills/<name>/SKILL.md`. Policies use their separate `status:` enum (`draft | active | deprecated`) — see [`.claude/policies/README.md`](README.md). Mirroring the leveling model onto policies is rejected: policies have no invocation counts (only lint-rule references), so the metrics don't transfer. A policy's promotion path is its lint-rule (`R0xx`) — when a policy's procedural rule becomes a hard CI gate, that's the policy "leveling up".

**What — discipline gate:** A skill's level changes how other skills interact with it:

- **`/learn`** integrates per Rule 3 — after patching a skill, asks the contradiction question, and on a "yes" calls `/level <skill> --regress --corrects <sha>`. This is the load-bearing integration; without it the leveling system is decorative.
- **`/inspect-pipeline --session`** Mode 4 dispatch list surfaces regression candidates: a `hardened`-or-higher skill whose session invocation needed manual correction is flagged alongside the `/learn` patch dispatch.
- **`/agora --start`** loads the skill board (or at minimum the skill-system state including `level:` values) so the user sees the current shape of the tools they're about to use.
- **`/agora --end`** 2.6 session retrospective surfaces promotion candidates ("`iterate` is now eligible for `hardened` — run `/level iterate --promote`?") as findings alongside the standard dispatch.

A skill's body cannot make claims above its level:
- A `used` skill cannot say *"always do X"* — must phrase as *"prefer X"*.
- `hardened` skills can prescribe.
- `reference` skills can be cited by other skills as the canonical rule source.

**Why:** A label that doesn't change downstream behaviour is decoration. Making the level shape `/learn` integration, dispatch findings, and audit framing is what turns leveling into discipline. The skills-only constraint preserves the existing policy lifecycle model — a separate, simpler concept that uses lint rules as its progression path.

**Where enforced:** `/learn` SKILL.md gains the contradiction-question integration as its final step. `/inspect-pipeline` Mode 4 includes the regression-candidate surface. `/agora --start` / `--end` integration is the recommendation in `/level` SKILL.md's "Integration points" section — the actual SKILL.md edits land in a follow-on session once the leveling system is exercised.

### 6. Each skill carries an append-only experience log (XP-with-knowledge)

**What:** Every skill at `used` or above maintains a sidecar file at `.claude/skills/<name>/experience.md` — an append-only markdown log of XP entries. Each entry carries: ISO date, session reference (`[[session-id]]`), `+N XP`, a 🟢 (success) or 🟡 (lesson) marker, and a one-paragraph knowledge snippet (the *why* — what was learned or what the skill did right).

The file's frontmatter rolls up:

```yaml
---
skill: check-ui-entity
xp_total: 175
xp_by_level:
  draft: 25
  used: 150
last_xp_at: 2026-05-18
---
```

XP value ranges:

| Marker | Award range | When |
|---|---|---|
| 🟢 **Success** | +20 to +30 XP | The skill did something materially right — delivered a non-trivial sub-goal without rework, validated a load-bearing pattern, earned a new cross-reference |
| 🟡 **Lesson** | +10 to +15 XP | The skill learned a lasting improvement — codified an edge case, surfaced a recurring trap, absorbed a `/learn` patch that strengthens the contract |

Both flavours build the trail; successes don't "outrank" lessons — a skill that learns earns its place too.

**Why:** Metrics are *counts*; XP is *narrative*. A skill at `hardened` isn't just "above the threshold" — it has earned its place across N specific moments, each of which can be re-read. The log doubles as the **mastery marker** at `reference` tier ("authored policy-X", "cited by N siblings" become category-tagged subsets of XP entries the user can scan).

The qualitative complement to the deterministic metric gate. Promotion to `reference` requires `xp_total ≥ 200 across ≥ 15 sessions` because at the top tier we want *trajectory*, not just *count*.

**Capture-at-source: the `## Unrated journal` buffer (WS1, US-AGORA-009).** XP has two
acts — *observe* what a skill did, and *grade* it. Bunching both at `--end` biases XP
toward the skills the orchestrator can see clearly (`agora`, `learn`) and risks the
award being forgotten. The fix splits the acts: **observe continuously, grade
periodically.**

- Every `used`+ `experience.md` carries a `## Unrated journal` section above its graded
  entries — a **capture-at-source buffer**.
- **The invoked skill writes its own stub** (a *standing instruction*, the same shape as
  the Log-before-checkbox-flip rule): when a skill finishes a unit of work in-session, it
  appends ONE line to its buffer — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`.
  The skill is the better observer of its own friction than the orchestrator. The stub is
  **strictly lighter than the session Log entry** (one line, no prose paragraph — no
  double-bookkeeping).
- **This is a narrow, explicit carve-out from Rule 5.** Rule 5 reserves `experience.md`
  for `/level`. The carve-out covers *only* the `## Unrated journal` buffer, and *only*
  because its contents are **unrated** — a journal stub is observation, not graded XP. The
  "single graded writer" invariant is preserved: graded entries (below the buffer) remain
  `/level`-exclusive. Writing a graded `## YYYY-MM-DD — … +N XP` block into the buffer (or
  anywhere by hand) is still a Rule 5 violation.

**Where enforced:**
- `/level <skill> --xp +<N> "<snippet>"` is the only writer of **graded** entries (appends to `experience.md`, updates the rollup frontmatter, updates the SKILL.md frontmatter `last_correction:`/`last_xp_at:` as appropriate). Direct edits to graded entries are a Rule 5 violation.
- **`/agora --end` step 2.3b is now *evaluate-the-stubs*, not reconstruct-from-Log** (US-AGORA-010): it reads the `## Unrated journal` buffer of **every `used`+ skill in the union of (a) this session's `skills_invoked:` and (b) skills with a non-empty buffer** — (b) catches orchestrator-inline stubs written *after* a prior session's 2.3b already ran (fix 2026-06-12; without the sweep, stubs rot ungraded across sessions). It rates each stub (+N XP, 🟢/🟡), presents the bundle as a **4-eye gate** per [`policy-four-eyes`](policy-four-eyes.md); on the nod, `/level <skill> --xp` converts each stub to a graded entry **and clears it from the buffer** (so a stub is never double-counted). Buffers are read **before** any Log distillation; a skill that wrote no stubs falls back to the Log-distillation path ("log-sourced award + surviving stub" is the named failure mode).
- Each `used`+ SKILL.md carries the one-line journal-at-source standing instruction (so the discipline is visible where the skill runs).
- `/level --board` shows `xp_total` as a column and renders the recent XP trail when auditing one skill.
- `experience.md` is git-tracked alongside SKILL.md — the audit trail.

### 7. Naming ceremony — identity earned at `used → hardened`

**What:** A skill's *identity* unfolds in three steps across the four levels — the game-design arc the metric gates alone don't provide.

**Step (i) — at `draft → used`: role descriptor.** The user proposes a one-line `role:` frontmatter value during `/level <skill> --promote`. Examples: *"the inspector"*, *"the doctor"*, *"the architect"*, *"the cartographer"*, *"the patcher"*. One short phrase that names what the skill *does* at its functional core. Set by the user, written by `/level`.

**Step (ii) — at `used → hardened`: the naming ceremony.** This is the core ceremony. `/level <skill> --promote` extends Mode 3 with the following sub-steps:

1. **Gather the skill's profile** — its `## When NOT to use` table, its mode list, its `## Claims at this level` section (Rule 8 quest), and its experience log to date.
2. **Present the philosophers catalog** — the Agora philosophers from `agora-naming.md`: Socrates (the dialectician), Aristotle (the categoriser), Euclid (the systematiser), Diogenes (the iconoclast), Hero of Alexandria (the engineer), Callimachus (the cataloguer), Plato (the form-seer), Pythagoras (the harmoniser), Heraclitus (the flux-seer), Thales (the first principle), Solon (the lawgiver), Pericles (the orator), Anaxagoras (the cosmologist), Theophrastus (the botanist / characterologist). The catalog is open — skills may propose an Agora philosopher not yet listed if the fit is strong.
3. **Issue the structured naming prompt** — the skill (Claude executing the prompt in the conversation) reads its own profile + the catalog and proposes ONE epithet + a one-sentence justification grounding it in the skill's actual behaviour (not poetic preference).
4. **4-eye gate** — present the proposal to the user per [`policy-four-eyes`](policy-four-eyes.md). Three options: accept (proceed), propose alternative (user names a different philosopher; the skill re-justifies against that one), cancel (promotion aborted; rerun later).
5. **On accept**, write `epithet: "<Philosopher> — <one-line domain>"` to SKILL.md frontmatter (e.g. `epithet: "Aristotle — the categoriser"`).

**Step (iii) — at `hardened → reference`: epithet canonicalized.** A `## Identity` opening section is added to the SKILL.md body — 1–3 paragraphs telling the story of why this epithet fits, citing 2–3 specific XP-log moments that prove the fit. Other skills may then *cite by epithet* in their own bodies: *"Apply Aristotle's classification"* reads as a recognised reference, not jargon.

**Why:** Without an identity arc, the level system is just a discipline gate dressed in game-design vocabulary. The philosopher epithet creates a *character* — a thing the user remembers, a name other skills can cite, a story the experience log can ground. Binding the ceremony to `hardened` (not `used`) ensures the name is **earned**, not handed out; ensures the skill has already accumulated XP entries the naming prompt can ground in; ensures regressions don't strip identity the skill never claimed.

The structured prompt + 4-eye gate guards against the AI's poetic preference overriding actual behaviour fit. The user can always redirect.

**Where enforced:** `/level <skill> --promote` extends Mode 3 with the ceremony sub-steps at the appropriate gate. `/level --board` renders the `role:` and `epithet:` columns. SKILL.md frontmatter writes are exclusive to `/level`.

### 8. Hardened+ skills carry a `## Claims at this level` section

**What:** Every skill at `hardened` or `reference` has a `## Claims at this level` section in its SKILL.md body — 3 to 5 explicit commitments the skill makes that other skills depend on. Each claim is one declarative sentence naming an invariant the skill guarantees.

**Worked example** (hypothetical, illustrative — not the actual /check-ui-entity claims):

```markdown
## Claims at this level (hardened)

1. Every audited entity is checked against all four registry layers (tag, type, permission, conftest); a missing layer is always a finding, never silent.
2. The audit is read-only — no SKILL.md or app/ edit happens outside `--finish` mode.
3. Findings are categorised R / Y / G; R findings block any subsequent promotion gate that depends on this audit.
4. The `--audit` default exit code is 0 unless an R finding is present; CI integration relies on this.
```

**Tightening at `reference`:** the same section evolves from 3–5 commitments to *rule statements other skills cite*. A `reference`-tier skill's claims read as imperatives the rest of the system depends on — they often graduate into policy lint rules.

**Why:** Today's contradiction question (Rule 4) is **abstract** — *"does this patch contradict a level claim?"* — easy to wave through because there's no specific text to point at. Named claims make it **concrete**. When `/learn` patches a `hardened` skill, it reads the 3–5 claims and asks per-claim: *"Does this patch contradict claim N: '<text>'?"*. A "yes" on any one is the trigger for `/level <skill> --regress --corrects <sha>`. This is the load-bearing teeth of the regression mechanism.

A skill that cannot enumerate 3 invariants isn't yet `hardened` — the gate keeps soft skills out.

**Where enforced:**
- `/level <skill> --promote` (`used → hardened`) refuses without a `## Claims at this level` section carrying ≥ 3 named claims. Quest requirement.
- `/learn` reads the section after patching a `hardened`+ skill and asks the contradiction question per claim (per Rule 4).
- `/level <skill>` audit mode displays the current claims as part of the "Holding tier" panel.

## The `/level` meta-skill — modes

Drafted here for the parent session to author the SKILL.md from.

### `/level --board`

The **skills-board view**. Read every `.claude/skills/*/SKILL.md` frontmatter
+ compute the six metrics. Output a single ranked table:

```
Skill                Level       Promoted    Last-update  Inv  Corr  Redo  Codif  Depth
─────────────────────────────────────────────────────────────────────────────────────
check-ui-entity      hardened    2026-04-12  2026-05-16   28   2     0.07  0.12   (3041L, 84H)
implement-story      hardened    2026-04-08  2026-05-15   47   1     0.04  0.09   (2814L, 71H)
agora                used        2026-05-14  2026-05-17   12   3     0.00  0.25   (598L, 41H)
fixbug               used        2026-04-01  2026-05-16   23   8     0.13  0.35   (1142L, 52H)
...
```

Sort modes: by level desc, by correction load desc, by invocation count
desc, by last-update asc (staleness). Default: by level desc, then by
correction load desc within tier.

### `/level <skill>`

Audit one skill against its current level's criteria. Report fit, propose
next promotion gate (or surface regression candidacy).

```
$ /level check-ui-entity
Skill: check-ui-entity
Current level: hardened (promoted 2026-04-12)

Metrics:
  invocation count: 28
  correction load (since promotion): 2
  redo rate: 0.07
  codification rate: 0.12
  last-update recency: 1 day
  reference depth: 3041 lines, 84 ## headings

Criteria for next level (reference):
  ✓ Invocation count ≥ 30: 28 (close — 2 more sessions)
  ✓ Zero behaviour-changing /learn patches since reaching hardened: 0
  ✓ Has vocabulary section: yes (tier philosophy)
  ✓ Has canonical audit defaults: yes (Layer 1-4 defaults)
  ✗ Other skills (3+) follow its structural pattern: 2 (check-page, fixbug)
  ✓ Has worked example: yes

Verdict: 5/6 criteria met. 2 sessions away from invocation count gate;
one more skill needs to mirror its pattern (candidate: feature-plan?).

Proposed action: park the promotion candidacy. Re-audit after one more
Session that invokes check-ui-entity.
```

### `/level <skill> --promote` / `--regress`

The only writers. Apply the level change, write the frontmatter, append the
`IMPROVEMENTS.md` entry. Refuse promotion if criteria are unmet (with the
gap listed); refuse regression if the criteria are still met (with the
metrics shown).

## Common mistakes

- **Hand-editing `level:` in frontmatter.** Bypasses the audit trail. Use `/level`.
- **Auto-promoting a skill that "feels ready".** Promotion is a quality commitment — the user makes it, not the metrics. Numeric readiness is necessary but not sufficient.
- **Counting non-behaviour-changing `/learn` patches as correction load.** A patch that adds a worked example, fixes a typo, or tightens cross-references is NOT a regression signal. Only patches that change what the skill does count.
- **Treating reference depth (line count) as a level gate.** Length is a heuristic; doctrine quality is what `reference` tier signals. A 5000-line skill that's never been invoked is `draft`, not `reference`.
- **Leveling new skills aggressively.** A skill at `used` after one session is rare. Most skills stay at `draft` for many sessions before they're invoked enough to justify `used`.
- **Forgetting to flip `level:` after a behaviour-changing `/learn` patch on `hardened`.** The whole discipline collapses if the integration between `/learn` and the leveling system breaks. `/learn` SKILL.md must enforce the level-check at patch time.

## See also

- [`policy-skill-authoring`](policy-skill-authoring.md) — the static counterpart: the file-shape contract (frontmatter fields, body sections, quoting) a SKILL.md must satisfy at each level, enforced by `validate_skill_frontmatter.py --levels`. This policy owns the transitions; that one owns the artifact.
- [`policy-skill-routing`](policy-skill-routing.md) — the demand side of M1/XP: a skill earns M1 (invocation count) and XP *only* when it appears in `skills_invoked:`, so routing real work to skills is the only thing that levels the corpus. That policy makes routing the agent's win condition; this one defines what the win unlocks.
- `.claude/skills/level/SKILL.md` — the canonical operator of this policy
- `.claude/skills/learn/SKILL.md` — the patcher; integration is the contradiction-question step that calls `--regress --corrects <sha>` when applicable
- `.claude/skills/inspect-pipeline/SKILL.md` — Mode 4 dispatch list surfaces regression candidates
- `.claude/skills/agora/SKILL.md` — `--start` loads the skill board; `--end` 2.6 surfaces promotion candidates as findings
- `.claude/sessions/IMPROVEMENTS.md` — durable promotion / regression audit trail
- `scripts/checks/validate_skill_frontmatter.py` — to be extended to enum-validate `level:` (follow-on)
- `.claude/sessions/spawns/2026-05-17-skill-progression-research.md` — the spawn supplying calibrated thresholds + peer-framework grounding
