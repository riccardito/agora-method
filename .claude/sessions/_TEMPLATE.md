---
session_id: YYYY-MM-DD-<slug>
date: YYYY-MM-DD
closed_date: ""
type: pipeline
mode: normal
plan_ref: ""
intent: "<one-line statement of what this session is for>"
goal: "<Goal name from COMPASS.md, or 'Filler' -- a session that advances no Goal (La Paz's records say 'exploration')>"
era: "<the current Era's slug from COMPASS ## Eras (agora:era:<slug>), e.g. la-paz>"
milestone_target: "<Milestone slug + which Goal criteria close, or 'none — parking'>"
status: open
repo_plan:
  branch: "<main | feat/<slug> — a feature branch by default for non-trivial build work; ONE branch per Milestone>"
  groupings: []
  push: "<at close | at the Milestone only | none — local park>"
agent: "<terminal / worktree / purpose label — distinguishes concurrent agents>"
skills_invoked: []
stories_touched: []
commits: []
milestone_outcome: ""
outcome: ""
---

<!--
  The frontmatter fields (US-AGORA-106: no inline comments in the block -- a
  `status: open  # ...` line made a copied file invisible to `find_open_session`,
  T058 T088). `flask agora open` writes the block from fields; `flask agora write
  close` flips `status: closed`. What each field holds:

  date: the day the session OPENED
  closed_date: the day the session CLOSED (filled by --end); empty while open. Sessions often span >1 day — keep both for the timeline.
  type: pipeline | doctor | fix | meta | mixed | plaza (plaza = a /plaza self-improvement round; use _TEMPLATE-plaza.md)
  mode: normal | planning | blind  (US-AGORA-037) — ORTHOGONAL to `type:`, which is untouched.
  planning — produces a plan, builds nothing. Emits one or more PLANS.md entries.
  blind    — executes a plan, composes nothing. MUST declare plan_ref: below.
  plan_ref: blind: the P-NNN loaded via `flask agora plan --load`. planning: the P-NNN(s) emitted.
  This field is also how a plan's status is DERIVED — never written back into PLANS.md.
  era: US-AGORA-067: INDEX.md carries the newest session's Era; `flask agora write era`
  status: open | closed
  repo_plan: declared at --start 1.4c (US-AGORA-036); --end 2.1 compares actual vs declared
  groupings: expected commit concerns, one line each — a forecast, not a contract
  skills_invoked: filled as the session runs: [implement-story, iterate, fixbug]
  stories_touched: [US-XXX-NNN, ...]
  commits: short shas + subjects, filled by the commit-tree triage
  milestone_outcome: filled by --end step 2.2: tag + green run id + push (Path A), or which criteria advanced (Path B)
  outcome: the ONE-line outcome --end 2.8 writes through `flask agora write outcome`; `write index` renders it as the INDEX line (US-AGORA-067). Empty while open -> `<intent> — in progress`.
-->

<!--
  Agora session protocol file. Created by `/agora --start` from this
  template, appended to during the session, compacted + closed by
  `/agora --end`. See `.claude/sessions/README.md` for the full model.

  This is a STRUCTURED SUMMARY, not a transcript. Keep the Log dense.
-->

# Session YYYY-MM-DD — <slug>

## Intent

<2–4 sentences. What this session sets out to do, and why now. If it
continues an open thread from a prior session, link it:
`Continues [[YYYY-MM-DD-<prior-slug>]]`.>

## Session plan

<The skill pipeline `/agora --start` reasoned from the goal (step 1.4) —
a checklist, ticked as each step completes. `/agora` lays it out; the
conversation drives it. Most real sessions are MULTI-PHASE — they cross
type boundaries. Base examples:

- pipeline:  [ ] /new-story or /feature-plan → [ ] /implement-story → [ ] /iterate → [ ] /fixbug (as needed)
- doctor:    [ ] enumerate targets → [ ] /check-page <slug> --finish ×N
- fix:       [ ] /fixbug <item> ×N (from /iterate --feedback or the bugs collection)
- meta:      [ ] /inspect-pipeline → [ ] /learn / /document per finding

Common multi-phase shape — "feature + rollout":
  [ ] /feature-plan → [ ] /new-story ×N → [ ] /implement-story
  → [ ] ui tweaks → [ ] /check-page --finish ×N (roll out to siblings)
  → [ ] /wiki (seed the feature)

For a CONTINUATION session, add the new goal's steps as a new phase
below the existing ones — don't erase the prior phase's checklist.
-->

- [ ] <step 1>
- [ ] <step 2>

## Log

<Running summary. One entry per meaningful unit of work. Each entry:
what was done, which skill (if any), key decisions, surprises, and the
docs/stories/code touched. Append as you go — do not wait for the end.>

### <skill or topic> — <one-line what>

- <decision / surprise / reference>

## Open threads

<DELTAS ONLY against [`THREADS.md`](THREADS.md) — the central registry is the
single home for carried threads (2026-06-12). Record: new threads born this
session (`T-NNN born — <text>`), threads resolved/promoted this session
(`T-NNN resolved/promoted → #NN`). Never copy the full carried list here;
`--start` reads THREADS.md whole. Empty is fine.>

- <T-NNN born/resolved/promoted — one line>

## Agora findings

<The feedback loop into Agora itself. Anything that surfaced about the
SKILL system during this session — a skill that needed manual
correction, a rule stated from memory more than once, a repeatable
procedure done ad-hoc. Each is a `/learn` / `/document` /
`/inspect-pipeline` candidate. `/agora --end` dispatches these. Empty is
fine.>

- <finding> → candidate: `/learn <skill>` | `/document --policy <slug>` | discuss

## Evidence

<!--
  THE ONE REGISTRY-SHAPED BLOCK in this narrative file (US-AGORA-062, AGORA-DECL §5):
  evidence with a definite shape is written as a FIELD at the moment it becomes true,
  never parsed from the Log afterwards. Written ONLY through

      flask agora write evidence --kind <kind> --value "<value>"

  (anchored on this heading, refusing a malformed line, a duplicate, or an older file
  without the block). The seams write it: the triage's commit step (`commit <sha>
  <subject>`), the seam chain (`suite <passed>/<failed> <scope>` · `gate <name>
  <verdict>`), the phase gate's nod (`phase-gate <phase> fired <ref>`), `write
  journal-stub` (`skill <name> invoked <step>`), `write milestone-record`
  (`milestone <tag> fired`), every `flask agora` command (`mechanism agora <cmd>
  fired`). `flask agora retro-context` reads these FIRST at --end 2.0 and labels
  anything it still has to parse `[PROXY]`. `cost <tokens> <minutes>` is reserved
  (§M, open question 7) -- nothing writes it yet. Do not edit by hand.
-->

## Handoff checklist

<!--
  BLIND RUNS ONLY (`mode: blind`) — delete this section on a normal session.

  A numbered, walkable item per verifiable outcome (US-AGORA-038). This is a
  first-class DELIVERABLE of a blind run, not a courtesy: it is what lets the
  user verify a whole unattended session in one pass instead of discovering it
  piecemeal.

  GENERATED, not composed at the end of a long run:
      flask agora handoff --draft .claude/sessions/<this-session>.md
  seeds one item per scope member of the loaded plan. Edit and extend it.

  DEEP-LINK a step wherever you can — `flask agora devlink "<path>"` — because
  a step that can be clicked is a step that gets tested.

  The NEXT `--start` 1.1 reads this back with `flask agora handoff` and
  surfaces every unchecked item as open. That read-back is the point: a
  checklist nobody reads is the state this section replaced. The user ticks
  items as they verify them.
-->

1. [ ] <verifiable outcome> — <deep link>

---

<!-- Everything below is written by `/agora --end`. -->

## Close-out

<!--
  THE CLOSE-OUT PAPER — `--end`'s deliverable (US-AGORA-034), assembled at
  step 2.10 and presented at ONE gate. Which sections appear depends on the
  SHAPE classified at 2.0 (`flask agora retro-context`):

    simple      — summary · commits · Issue comment · unresolved · baton
    substantive — + XP · dispatch · audit verdict · drafted retro
    milestone   — + the Goal retro (its own gate at 2.2.5)

  Delete the sections the shape does not carry; do not leave them empty.
-->

**Shape:** <simple | substantive | milestone — as classified at 2.0, with its one-line reason>

**Compacted summary:** <3–6 sentences — what the session actually
accomplished, distilled from the Log.>

**Commits this session:** <list, or "see frontmatter `commits:`". Note any
DIVERGENCE from the `repo_plan:` declared at `--start`.>

**Milestone outcome:** <if reached (Path A): tag name + green CI run id
+ push. If parked (Path B): which Goal success criteria advanced this
Session, which remain.>

**`/inspect-pipeline --session` verdict:** <🟢 / 🟡 / 🔴 + one line>

**Dispatched:** <what went to `/learn`, `/document`, `flask agora capture`,
`/fixbug`, or a new story — each with its `mechanism | prose | judgment`
disposition (US-AGORA-029)>

**Issues updated:** <every Issue the session worked, with the comment posted —
this half ALWAYS runs. Closed Issues listed separately.>

### Touched and unresolved

<!--
  `policy-shoulder-glance`'s CATCH half, made an artifact (US-AGORA-034).
  Everything the session touched that did not reach a resolved state, each
  with a NAMED disposition: resolved · thread · Issue · deliberately dropped.
  "Deliberately dropped" is a legitimate answer; absent from the list is not.
  `flask agora retro-context` produces the raw list — this is where each item
  gets its disposition.
-->

- <item> → <resolved | thread T-NNN | Issue #NN | deliberately dropped: why>

### Baton — what the next session inherits

<!--
  An INDEX, not a copy: the Issues/comments/files/COMPASS entries the next
  session should open against, so `--start` begins already holding what it
  needs rather than re-deriving it.

  DRAFTED, not composed (US-AGORA-035):
      flask agora baton --draft .claude/sessions/<this-session>.md
  proposes the bullets from the open Goal criterion, the stories short of
  `tested`, carried plan items, open threads, the Issues worked, the stubs the
  next --end grades, and the branch. Edit them; it is raw material.

  The next `--start` 1.1 reads this section back with `flask agora baton` and
  VERIFIES every pointer it names. So WRITE THE POINTERS PLAINLY -- `#184`,
  `US-AGORA-035`, `T-063`, a backticked `feat/…` branch, a backticked path or a
  markdown link. Prose around them passes through untouched; a pointer only
  gets checked if it is written in a shape the reader can see.
-->

- <pointer>

<!--
  ### Milestone retrospective — <milestone-slug>
  Inserted by `--end` step 2.2.5 — one per Milestone fired (Path A
  only). Omit entirely at Path B (parking sessions). When two
  Milestones fire in one session, two `### Milestone retrospective —
  <slug>` sections appear back-to-back in firing order, each
  Goal-scoped. Three prompts per Milestone:
    1. What does closing this Goal change?
    2. What was hardest about this Goal?
    3. What should the next Goal in this Mission cycle look like?
  Do NOT pre-draw an empty section here — the actual block is inserted
  at run time by --end, never as a template scaffold. Discipline added
  2026-05-23 by US-AGORA-005; rationale per IMPROVEMENTS.md 2026-05-23 (d)
  Finding 4a (template stickiness drift).
-->

### Retrospective

<!--
  Filled by `--end` step 2.6 — a section of the close-out paper.
  SKIPPED ENTIRELY on a `simple` shape (delete this block).

  DRAFTED, never solicited (US-AGORA-034 D2): the agent writes all three
  answers from the session record — grounded by `flask agora retro-context`,
  not from a conversation that may already be compacted — and the user nods,
  corrects, or adds. A blank three-question form at the end of a long session
  is the exact shape that was removed.

  Draft from EVIDENCE, not impression: a redirect the user actually made, a
  phase that overran, a gate that didn't fire, a test that caught something
  late. "The session went well" is filler, not a retro.

  Anything the USER says goes in VERBATIM — the agent writes the structure and
  the evidence, never a paraphrase of their words.

  Session-scoped (sprint-retro analogue — the Goal-scoped retro is at 2.2.5).
  Exactly ONE `### Retrospective` heading per file; never append a second.
-->

**What worked:**

-

**What didn't:**

-

**What to change next session:**

-
