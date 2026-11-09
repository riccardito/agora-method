---
name: design
description: "Code-design doctor and Themelion-Arc conductor — red-flag design review of existing code (module boundaries, interfaces, dependencies, the canon's fourteen-flag vocabulary), cleanup conducting for Arc phase ③ where every sub-pass cites the Themelion Declaration, and post-cleanup quality control (ratchets, adoption tables, policy-rules-retired). NOT for page structure (/check-page), entity surfaces (/check-ui-entity), the skill system (/inspect-pipeline), pre-code feature design (/feature-plan), or doc placement and policy authoring (/document)."
argument-hint: "[--review <path-or-module> | --conduct <C-class-or-sub-pass> | --qc [<class>]]"
level: used
role: "the Themelion conductor — red-flag code-design review, Arc phase-③ cleanup conducting, post-cleanup QC"
promoted_at: "2026-08-16"
---

# Design — the code-design doctor and Themelion conductor

Working name: **the John-Skill** — the carrier the canon promised (canon §7.2), born
at `draft` inside Arc phase ① so the Declaration and its carrier ship together
(US-AGORA-046, the D2 ruling). The Greek epithet is deliberately absent: it arrives
at the used→hardened naming ceremony (`policy-skill-progression` Rule 7), never at
birth. Hippodamus of Miletus is noted as a candidate, not decided.

**The core this skill carries:**

- `themelion-declaration.md`
  — the normative core. Everything this skill plans, reviews or verifies cites it:
  principles **P1–P4**, class entries **C1–C14**, discipline rules **§5**.
- `themelion-canon.md` — the
  analytical ground. §2.3 holds the **fourteen red flags with definitions and
  codebase smells** — this skill's review vocabulary, referenced rather than
  duplicated so the table cannot drift.

Its Vision is the north star stated plainly: the perfect system design, never fully
achieved, always steered by (canon §7.2).

## When NOT to use this skill

| Territory | Owner — use instead |
|---|---|
| Page structure — zones, subtabs, per-page structure docs | `/check-page` |
| Entity surfaces — registries, modals, cards, story coverage | `/check-ui-entity` |
| The skill system — the `.claude/` tree itself | [`/inspect-pipeline`](../inspect-pipeline/SKILL.md) |
| Pre-code feature design — alternatives before anything exists | `/feature-plan` |
| Where a doc lives, policy authoring, CLAUDE.md mirrors | [`/document`](../document/SKILL.md) |
| A concrete bug with a symptom | `/fixbug` |

`/design` owns what none of them touch: **code design** — module boundaries,
interfaces, dependency structure, the red-flag read of *existing* code — plus the
Arc coordination the Declaration's execution discipline requires.

## MODE 1 — `--review <path-or-module>`

The red-flag design review. Read-only; the deliverable is a design note.

1. **Read the module AND its callers** — depth is a property of the interface seen
   from outside; a review that reads only the implementation cannot judge it.
   **Read the battle map on the way in** —
   `docs/references/agora/bug-battle-map.md`
   (`flask agora battle-map --check` first; regenerate if stale): the system's
   known defect classes + their trend are review context, and a flag that
   matches a named defect class **cites it** rather than re-deriving it
   (US-AGORA-052 — the map is this mode's named read).
2. **Walk the fourteen flags** — Shallow Module · Information Leakage · Temporal
   Decomposition · Overexposure · Pass-Through Method · Repetition ·
   Special-General Mixture · Conjoined Methods · Comment Repeats Code ·
   Implementation Contaminates Interface · Vague Name · Hard to Pick Name · Hard
   to Describe · Nonobvious Code. Definitions and per-codebase smells: canon §2.3.
   Verdicts carry **evidence** (a path, a grep count, a call-site list), never
   impressions. **When the module is Agora's substrate** (`app/commands/agora*.py`,
   `scripts/`, the git hooks, the state files' writers and readers), the
   Agora declaration is the
   canon's Agora sibling: its §3 seven record flags (the banner in the callee · the
   two-copies fact · the stale carry · the fold never closed · the one-way seam · the
   parsed log · the endured batch) join the fourteen, and a verdict on the substrate
   cites `AGORA-DECL §<n>` beside the canon section (US-AGORA-054; the declaration's
   §5.5 binds this mode).
3. **Ask the sharpest question per finding:** *which single module owns this
   knowledge?* (Ch 5 — the leakage probe.)
4. **State the interface/implementation split** — what the module hides, what it
   exposes, whether the interface is simpler than the implementation (the depth
   read, used comparatively, never as arithmetic — canon §3.4).
5. **Write the design note** to `docs/references/design/note-<slug>.md`: the split
   (step 4), the per-flag verdicts with evidence, recommendations framed as
   trade-offs citing the Declaration, and the **least-confident-decisions list**.
   This is C14's "recorded design reasoning" artifact — the check the Declaration
   names.

## MODE 2 — `--conduct <C-class-or-sub-pass>`

Phase ③ conducting. Plans a cleanup sub-pass; the session executes it.

**Target-less variant (`--conduct` with no argument — the lived
first-invocation shape, session 2026-08-16):** the
deliverable is the **phase agenda itself**, not a sub-pass plan. Read the
Declaration whole (P1–P4 · C1–C14 · §5) + the Arc ledger's phase-③ members +
their topic definitions in `la-paz-last-topics.md`, order the sub-passes by
leverage (§5.6) with a citation and its employed doctors per sub-pass, and
propose the phase's Goal/Issue home at the 4-eye gate (the #351 precedent:
a Goal Issue mirroring the #231 shape, batches opened up front, the ledger
staying the Arc index). Steps 1–5 below then run **per sub-pass**, each at
that sub-pass's own session, citing the agenda.

1. Read the Declaration entry for the target class (C-n) and the principles it
   cites; read the **audit matrix** for the class — if none exists, the matrix IS
   the first deliverable (§5.2, matrix-first).
2. Draft the sub-pass plan, each rule citing **P-n / C-n / §5** — a rule that
   cannot cite does not run (§5.1).
3. Enforce the discipline in the plan itself: the ratchet lands the same session
   the class burns to zero (§5.3) · no intended behaviour change (§5.4) · the
   three test-reconciliation grep axes at the matrix step (§5.5) · leverage orders
   the work (§5.6) · interfaces get design-it-twice and conversions get the
   Program Design gate + a tracer bullet (§5.7).

   **A config/descriptor conversion prices EVERY AXIS against its CONSUMER
   SURFACES.** When the converted thing is multi-axis (the leaf descriptors:
   columns · filters · plugins), the plan enumerates, per axis, *which
   surfaces consume it* — and a conversion is complete only when every named
   consumer is wired, not when the primary surface renders. The lived miss
   (session 2026-08-18 return round F1): SP-4's wave wired
   the LEAF surface (columns + filters) for ten entities while the plugins
   axis's consumer is the MODAL fragments — which had exactly one wired
   consumer (the SP-3 pilot), so the editor's plugin toggles silently
   no-opped on every wave entity through pricing, the conduct, and the blind
   run; the user's walk found it. Cheap check at step 2: a two-column
   axis × consumer-surface table in the sub-pass plan; an axis with zero (or
   "pilot-only") consumers named is the flag.
4. **Name the doctors the sub-pass employs — the conductor conducts, he does not
   re-implement their checks** (US-AGORA-040, the chief-doctor wiring). The
   verification half of every sub-pass is a STEP that calls the doctor that owns
   it and consumes its output — the wire lives here, in the caller, and is
   registered in `mechanisms.yaml` `skills:` (AGORA-DECL §4):

   | The doctor · call | When the sub-pass employs it | Its output the plan consumes |
   |---|---|---|
   | `/check-page` `<slug> --audit` / `--finish` | page zones + premium chrome on a touched leaf | the zone-findings table · the finish sweep's diff |
   | `/check-ui-entity` `<Entity>` / `--hub <hub>` | entity surfaces + the eight registries | the registry matrix (a named feed of the QM overview) |
   | `/check-coverage` `--diff` | a coverage ratchet (also MODE 3 step 1's executor) | the per-module delta against `main` |
   | `/wiki` `--audit` / `--surprises <slug>` | seed drift on a touched feature | the stale list · the surprises list |
   | `/selenium` `--run <test>` / `--add <feature>` | acceptance that is user-visible behaviour | the pin verdict (Goal #45 stays the suite's home) |
   | `/manage-translations` | i18n health after a string sweep | the fuzzy / missing table per locale |

   The chain is `/agora → /design --conduct → doctor → skill`; a sub-pass plan
   that hand-rolls a check one of these six owns is a routing breach, not
   thoroughness. **The QM overview** (scoped by US-AGORA-040: generated skeleton
   + authored judgment over the page registry · the hub registry · `docs/stats.yaml`
   · the modal-matrix scanner) is this mode's planned instrument — built
   matrix-first by the first phase-③ sub-pass that needs it, read here to pick
   targets and re-run by MODE 3 as the regrow check.
5. Present the plan at a 4-eye gate (`policy-four-eyes` — summarized,
   recommendation-with-default); the session runs it and the commits cite the plan.

## MODE 3 — `--qc [<class>]`

Post-cleanup quality control. For the named class (or all cleaned classes):

1. **Ratchet check** — the class's zero-tolerance gate exists, its baseline is
   current, and it fires (positive control) — a check that cannot fail is not a
   check. Coverage ratchets run through `/check-coverage`
   `--diff` (its output: the per-module delta against `main`), the executor this step
   employs rather than re-implementing. **And the control's planted regression is verified to have LANDED
   before its verdict is read** — a line count, a grep, a `git diff --stat` on
   the mutated file. A mutation that never reached the tree returns "nothing
   grew", which is indistinguishable from a passing control; the tell is a count
   sitting at *exactly* the baseline instead of rising (lived
   session 2026-09-03: a `sed` range matched nothing and the
   first control read as a pass — the retry checked `wc -l` first).
2. **Adoption check** — every mechanism the cleanup shipped sits in the *called*
   half of the adoption table (a mechanism only a human remembers is not shipped) —
   read off `docs/stats.yaml` `agora.mechanisms` and, for skills,
   `agora.skills.records[].callers` / `called_by` (US-AGORA-061);
   [`/inspect-pipeline`](../inspect-pipeline/SKILL.md) `--audit` 1.4b is the
   reader that names the dormant one.
3. **Rules-retired count** — for C8/C10-family work: which policy rules the new
   layer absorbed, proposed for deletion with citations. A shrinking policy is the
   success metric.
4. **Regrow check** — re-run the class's audit matrix; any count above baseline is
   a finding with a named owner, never a note. The matrices are the doctors'
   (`/check-page` `--audit` for zones,
   `/check-ui-entity` `--hub` for registries) —
   re-run through them; the output is the same table MODE 2 step 4 consumes.
5. **Consumer-config audit** — when the cleanup RETIRED a script-held config (a JS
   `elementMap`, a JSON block, a hand mount) in favour of a generated one, diff the
   retired config's KEYS against the generated one's, per surface, from the
   pre-conversion version (the introducing commit's parent). The capture-diff that
   proves the surface byte-equal cannot see this: the old map lived inside a deleted
   `<script>`, and a pin written from the new output pins the loss (lived
   session 2026-08-29: four leaves' saved-preset fields never
   reached the generated blob, fixed by `hand_kept.preset_id`). The audit is a script
   (**#413**, the `elmap_audit.py` shape under `scripts/`); until it lands, run it by
   hand.

## Initialisation (the US-AGORA-041 pilot — full self-model)

**What this skill reads before acting:** the Themelion Declaration + the canon
(`themelion-canon.md`) — no verdict leaves without a citation, so the sources
are read first, never recalled; the battle map
(`flask agora battle-map --check`, regenerate if stale) for the system's known
defect classes; for `--review`, the module AND its callers; for `--conduct`,
the target C-class entry + its audit matrix (building the matrix first when
none exists, §5.2); for `--qc`, the class's ratchet + the adoption table; the
QM overview (US-AGORA-040-scoped) once built.

**Self-model (the C3 pilot):** `/design` exists because cleanup without
recorded design reasoning re-accumulates — it is the Arc's conductor: it
cites (P-n / C-n / §5) or it does not clean, it employs the six doctors
rather than re-implementing their checks, and it plans sub-passes the session
executes. It is deliberately NOT another doctor and NOT a builder. **The
extension's test:** during Arc-③ sessions, every noticed context gap —
knowledge this skill needed and did not have, a read the list above missed —
lands as a 🟡 journal stub in [`experience.md`](experience.md) (the
journal-at-source channel); the r7 landscape reads those stubs as the
self-model extension's lived evidence.

## Working method (the canon's imports)

- **Design it twice at interfaces** (Ch 11) — two genuinely different sketches
  before committing any module boundary; an hour against days.
- **The Program Design gate** (canon §7.2, from the Software Factory Playbook) —
  before a conversion: types and signatures with **no bodies**, plus the
  least-confident-decisions list, so the risky calls are made at a gate instead of
  silently mid-implementation.
- **Tracer-bullet vertical slices** — one thin end-to-end slice proves a
  conversion's shape before the class rollout.
- **The comment-first canary** (Ch 15.3) — a method or variable that needs a long
  comment is flagging its own abstraction; the review reads comments as depth
  instruments, not as prose.

## Mode dispatch

| User says | Mode |
|---|---|
| `--review <path>` / "review this module's design" / "red-flag read" | MODE 1 |
| `--conduct <target>` / "plan the cleanup pass for X" | MODE 2 |
| `--qc [<class>]` / "is the cleaned class still clean?" | MODE 3 |
| No flag, during Arc phase ③ | MODE 2 (the conductor is the phase's default) |
| No flag, otherwise | MODE 1 |

## Key rules

- **Cites or it doesn't clean.** No plan, verdict or recommendation leaves this
  skill without its P-n / C-n / §5 citation. Taste gets re-cleaned.
- **Evidence over impression.** Every flag verdict carries a path, a count, or a
  call-site list.
- **The trade-off frame is the boundary** (Declaration §6): every principle has
  its *taking it too far*, and the tie-breaker is the book's — best information
  hiding, fewest dependencies, deepest interfaces.
- **Read-only by default.** MODE 1 and MODE 3 write nothing but their artifacts
  (design notes, QC reports); MODE 2 plans — the session executes.
