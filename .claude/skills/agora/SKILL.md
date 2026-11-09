---
name: agora
description: "session orchestrator for the Agora skill system. Brackets a work session with a start sequence (loads recent-session context + skill-system state + the product's story backlog, classifies the goal prompt as a new session or a continuation, commit-tree + open-PR triage, a reasoned skill-pipeline plan, the declared repo plan, the session protocol file) and an end sequence that produces ONE close-out paper at ONE gate (commit triage, log compaction, XP grading, a session-scoped /inspect-pipeline audit including an Agora self-audit, /learn + /document dispatch, a drafted retro, the touched-and-unresolved list, and the Issue update) plus a separate Milestone gate for push + CI-green. The lightweight conductor at the centre of Agora — it routes work and records it, it does not do the work itself."
argument-hint: "[--start (default) | --end | --status | --spawn | --plaza]"
level: hardened
promoted_at: 2026-05-31
role: "the mayor"
epithet: "Socrates — the dialectician"
self_audit_loop: true
---

> **Journal-at-source** (policy-skill-progression Rule 6): when you finish a unit of work in a session, append ONE unrated stub to [`experience.md`](experience.md) `## Unrated journal` — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`. One line, lighter than the session Log; `/agora --end` 2.3b grades it. **Orchestrator-inline dispatches are covered too:** the skills `--end` invokes inside its own machinery (`/level --xp` · `/inspect-pipeline --session` · `/learn --from-session` at steps 2.3b/2.4/2.5) have no self-journaling phase, so the orchestrator writes their stub *on their behalf* at the same step-heading prepend — see step 2.3b.

# Agora — the session orchestrator

`/agora` is the **centre of Agora** — the open plaza where the work happens.
The policy layer holds the rules, the skill layer holds the workflows, the
tools layer holds the CLIs; `/agora` is the layer above all of them that
**brackets a work session**: it opens with a start sequence, closes with an
end sequence, and in between keeps a structured record of what happened.

It is deliberately **lightweight**. It does not build features, fix bugs, or
audit pages — the other skills do that. `/agora` **plans, routes, records, and
reflects**. The conversation drives the queued skills; `/agora` lays out the
queue, ticks it off, and at the end turns the session into a lesson.

Apply [policy-commit-discipline](../../policies/policy-commit-discipline.md) —
the start and end sequences are where it is enforced; the working tree opens
and closes a session clean.

## When NOT to use this skill

| Need | Use instead |
|------|-------------|
| Build a feature | `/implement-story` (or `/new-story` first) |
| Run the iteration loop for one story | `/iterate` — test plan / feedback |
| Audit the static `.claude/` tree | [`/inspect-pipeline`](../inspect-pipeline/SKILL.md) `--audit` (no session needed) |
| Patch a misbehaving skill | [`/learn`](../learn/SKILL.md) |
| Author a cross-cutting policy | [`/document`](../document/SKILL.md) `--policy` |
| Just commit some changes | direct `git` — but if it's a session boundary, let `--start` / `--end` triage it |

`/agora` sits **one level above** `/iterate`: `/iterate` manages the loop
*within* building one story; `/agora` manages the *whole work session*, which
may contain several `/iterate` loops, a doctor sweep, or meta work on Agora
itself.

---

## Goal vocabulary

Agora structures work into six hierarchical tiers, one event, and two named
non-tiers — an **Arc** (a movement) and a **North star** (an orientation). This
is the vocabulary `/agora` operates in; every other clause in this skill refers
back to it. **The source is the ontology schema** (`docs/references/agora/ontology/schema.yaml`,
`vocabularies.tiers` — US-AGORA-088): this table, `CLAUDE.md`'s and `agora-harness.md`'s are
generated from it between markers and held by the record-consistency lint (AGORA-DECL §1).

<!-- rc:tier-table -->
| Tier | Granularity | Closes with |
|---|---|---|
| Vision → Mission | forever / multi-year | re-stated, never closed |
| **Era** | several Goals — a themed chapter | the `New Era` event |
| **Goal** | weeks–months | success criteria met → a Milestone |
| **Sub-goal** | hours–days | one conventional commit |
| **Session** | a work window | a two-way retro |
| **Milestone** *(an event, not a tier)* | when its Goals close | tag + push + CI-green (the Haleluja) |
| **Arc** *(a movement, not a tier)* | a named multi-session movement inside an Era — phases + a paper + a ledger Issue | the `Arc-close` event: its paper written, its ledger emptied — no tag of its own (its Goals fired their own Halelujas) |
| **North star** *(an orientation, not a tier)* | a named horizon for a topic / design line — never committed | never closed — orients decisions ("closer or farther?"); retired only by explicit ruling |
<!-- /rc:tier-table -->

Vision and Mission live in [`.claude/sessions/COMPASS.md`](../../sessions/COMPASS.md)
— durable, read by `--start` 1.4. **Eras** and Active Goals (with their success
criteria) also live there; a session opens *inside* the current Era, so
continuation is structural rather than inferred (US-AGORA-016 / RP-AGORA-004 T1).
Sub-goals are session-scoped — they live in the session plan and tick off as
commits land.

**An Era is a themed chapter above Goal** — a COMPASS chapter + an
`agora:era:<slug>` Issue label + an EVENTS.md `New Era` chapter, **not** a data
model. It groups several Goals into a coherent arc so the *boundaries between
Goals* (where drift lives — the round-4 thesis) have a home. Eras are
**forward-only** — a new Era is opened going forward, not retro-fitted over
history. **Backlog = an empty Era** (a not-yet-started chapter; the same object
with its `start`/Era-plan slot not yet filled).

**Era and Goal share one 6-part skeleton** (US-AGORA-017 / RP-AGORA-004 T3) —
`0 structure · 1 backlog · 2 start · 3 sections · 4 evaluation · 5 ending` — so both
feel identical to operate and every follow-up has a structural home. **The existing
COMPASS fields ARE the slots** (no per-object boilerplate — the skeleton is a lens,
not new prose): a Goal's `Era`/sub-goals = slot 0, its deferred follow-ups = slot 1,
its Intent + Success criteria = slot 2, the ticked criteria = slot 3, the
shoulder-glance = slot 4, the Milestone = slot 5. When `--start` opens a new Era or
Goal (1.4), fill the slots in order. Full convention + field-mapping:
[`COMPASS.md`](../../sessions/COMPASS.md) `## The fractal planning skeleton`;
rationale: `docs/references/agora/agora-planning-skeleton.md`.

**A Milestone is an event, not a tier.** It fires when a Goal's success
criteria are met — wherever in a session that happens. The push +
CI-green ceremony is bound to the **Milestone**, not to `--end`.

**A session is a clock-time window.** It may close N sub-goals; it may
or may not reach a Milestone. A session that didn't reach one parks
clean: commit pending sub-goals, retro, no push gate. The on-disk home
for session protocol files is [`.claude/sessions/`](../../sessions/) —
the directory name is historical; each file represents one session.

---

## The commit-tree triage

A shared subroutine — **both** `--start` and `--end` run it. It enforces
[policy-commit-discipline](../../policies/policy-commit-discipline.md).

1. **Read the working tree.** `git status --short` + `git diff --stat` +
   `git stash list`. Note the current branch (`git branch --show-current`).

2. **Group changes into coherent commits.** One commit = one concern
   (policy Rule 1). Group by feature / scope / layer — never by "everything
   touched". A group whose summary needs an "and" is two groups.

3. **Draft a message per group** in conventional-commit form (policy Rule 2):
   `type(scope): summary`, imperative, ≤72 chars, story id where one applies,
   co-author trailer (policy Rule 3).

4. **Surface the branch state — and for feature/build work, RECOMMEND a branch.** On `main`, non-trivial feature/build work gets a recommended feature branch with a proposed name (`feat/<slug>` / `fix/<slug>`); docs / chore / tiny fixes may go direct to `main` — say so. Never silently branch or refuse.

5. **Present the commit plan — summarized.** The grouped files +
   one-line subject per commit. **No full bodies yet.** Wait for the
   user's explicit "go" / "yes" / "commit" before drafting the full
   messages. Smoke tests passing, ruff clean, manual verification —
   none of these are user confirmation; they are *prerequisites* to
   asking. The summarized plan + "go" gate is a discipline of its own:
   a full commit body in the proposal turns the user's "go" into a
   rubber-stamp of text they may not have read carefully. This is a
   **4-eye gate** per
   [policy-four-eyes](../../policies/policy-four-eyes.md) rules 3
   (summarized) and 4 (smoke-test pass is a prerequisite, not consent).

6. **On "go", write the full bodies and commit.** Stage each group
   by explicit path (`git add <path>…`, never `git add -A`), write
   the full conventional-commit body (with "Why" line + co-author
   trailer per policy Rules 2-3), commit, repeat. (precedent)

   **Verify the INDEX before every commit — `git commit` commits the
   index, not the paths you just added.** Anything staged *earlier in
   the session* (a `git rm` from a doctor pass, a stray `git add`
   before a rethink) rides along silently into the next commit,
   producing a multi-concern commit that ruff, the hooks and CI all
   pass. Compare `git diff --cached --name-only` to the commit's own file
   list **before** each `git commit` — **as a test inside the chain**
   (`[ "$(git diff --cached --name-only | LC_ALL=C sort)" = "$expected" ] && git commit`,
   `$expected` in byte order — a bare `sort` collates by locale and refuses a correct
   index, runbook C6; lived
   session 2026-10-23, the shape this line prescribed until then),
   never as a print, which shows the rider and commits it anyway: *the plan's
   file list is a claim; the index is the fact* (lived
   session 2026-07-08: a doctor pass's `git rm` rode into
   an unrelated `feat(ui)` commit · session 2026-10-22: a printed
   index carried a staged `git mv` into an interview commit; #477). **Its blind side: it sees what IS staged,
   never what a drawn seam FORGOT** — the preflight lints the working tree, so an
   untracked source file passes every gate while later commits cite it; after the
   last build seam `git status --short` shows no `??` under `app/` · `scripts/` ·
   `tests/`, or it is a red (lived session 2026-09-11; #477).

   **When a change CHANGES a behavior an existing test ASSERTS, run the
   test file that asserts the OLD behavior before committing.** A build's
   own new-feature test passing is not enough — a feature that *reverses*
   a prior invariant will red the test that pinned the invariant, and that
   test usually lives in a *different* file. Before committing a
   behavior-changing build, grep the suite for tests asserting the
   behavior you changed (by the route, the class name, the assertion
   string) and run them (lived session 2026-07-10: T-039's
   Workouts "+add" reded `test_double_modal.py`, which the build never ran).

   **When a URL's rendered BODY changes meaning, also grep the tests that
   FETCH that URL** — a test asserting on rendered output contains *none* of
   your diff's symbols, so the symbol axis below never reaches it. Ask *"which
   URL's response did I change the meaning of?"* and grep `tests/` for that path
   (`grep -rn "get('/wiki')" tests/` finds the *class*, not the instance — lived
   session 2026-08-01). **When the change REMOVES content from that
   response, reconcile the fetchers that stay GREEN too** — a `not in` on a page that
   can no longer carry it is a *vacuous pass* (lived session 2026-09-20).

   **And a reconciliation grep is read WHOLE — never capped with `head -N`.**
   The axis can be right and the cap still defeats it: a truncated finding
   list is indistinguishable from a complete one, so the sweep proceeds
   believing it reconciled everything the grep found (lived
   session 2026-08-19: the T-075 grep carried `| head -12`).
   When the output might be long, write it to a file and read the file whole;
   a cap belongs on *exploration* greps, never on a grep whose output is a
   work list.

   **A capped grep is also how a DELETION proceeds on a false clearance — so a
   grep that licenses a deletion is never previewed, and you sort or bucket
   before you cut, or do not cut.** The cost of reading it whole is seconds;
   the cost of a false clearance is a revert plus everything downstream that
   trusted it. Uniform, uninteresting hits are exactly what hide the one ruling
   past the cut, and any grouping by file type would surface it (lived
   session 2026-08-30: `hits[:8]` were all `.po`
   breadcrumbs; four `home: reserve` templates deleted, R040 caught it). A
   session that had QUOTED this rule still capped, so prose is not the fix — the
   mechanism half is captured: a sweep-verify command that writes findings to a
   file and refuses to summarise.

   **Grep by the SYMBOL you changed, not by the FEATURE you were
   building** — the axis is the whole rule. A changed helper's test
   almost never lives beside the feature that made you change it: it
   lives beside the *helper*. Searching the files you were already
   working in feels like applying this rule and isn't (lived
   session 2026-07-26 · session 2026-07-26: the
   same shape twice — `_ascii()` grepped in the agora tests only; 2.7
   retired without grepping `coaching`). Ask *"what did I change?"*, not
   *"what was I working on?"* — then grep the answer across `tests/` (and,
   for a retired or renamed thing, across `.claude/` and `docs/` too). The
   full suite is the backstop; a one-line grep catches it first.

   **A path used as a DATA-STRUCTURE KEY is a symbol too — grep the retired
   KEYS, not only the retired identifiers.** The symbol axis asks *what did I
   change?* and is usually read as naming variables, functions and ids; a
   literal string used as a dict key does not look like an identifier, and so
   slips a sweep that is otherwise run correctly. It behaves like one in every
   way that matters: something elsewhere names it verbatim, and retiring it
   breaks that reader. The tell is mechanical — **you edited a literal-keyed
   map** (an exclusion map, a registry, a baseline, an allowlist) — so grep
   the retired keys across `tests/ scripts/` (lived
   session 2026-08-31: an exclusion map
   shrank; its ratchet test hard-coded one of the retired keys).

   **The same finding from the other side: a GUARD test must not hard-code a
   member of the thing it guards.** That test monkeypatches a sample exclusion
   to prove `--check` reds an untagged entry — so it had pinned *a value the
   ratchet exists to delete*, and it reded while the ratchet was perfectly
   healthy. Fix at the shape, not by renaming the sample to the next victim:
   **derive** it (`next(iter(chk.EXCLUDED))`). Any proof-of-failure test
   guarding a shrinking map has this shape — **and its fixtures never NAME a real member either**: a quoted `'deployment-guide.md'` in a test file is a bound name in a code file, so the path-pin gate reads the fixture as a READER of the deleted path and reds the seam (lived twice, session 2026-09-12); plant neutral stems. A hard-coded member is a
   time-bomb whose fuse is the map working as designed.

   **And when a sweep REWRITES a MARKUP SHAPE app-wide (attribute quoting,
   a macro's rendered pattern), grep `tests/` for the OLD shape before
   running the suite** — the third axis of this family. The symbol axis
   finds tests beside a changed helper; the URL axis finds tests fetching a
   changed page; neither reaches a test that asserts or PARSES the markup
   pattern itself (lived session 2026-08-09: the quoting sweep
   left 12 tests in 5 files pinning the old single-quote shape). Derive the
   grep from the sweep's own conversion rule (*what pattern is being
   retired?*), run it at the audit-matrix step, and schedule the test
   reconciliation as part of the sweep rather than as a suite surprise.

   **The fourth axis: a change to the RENDERING BASELINE of the default TEST locale
   (a catalogue minted for it) greps `tests/` for the SOURCE-LANGUAGE literals before
   the suite, and 1.4c forecasts the reconciliation seam** — such a pin carries none
   of the diff's symbols, URLs or markup, yet asserts exactly the rendering the change
   retires; a null test locale is not the fix, it hides the product's UI from the suite
   (lived session 2026-09-23: 117 pins, one class, unforecast).

   **The fifth axis: a ROUTING change -- a URL converter, a blueprint `before_request` -- is
   reconciled by a mechanical sweep, every literal test path matched against the changed rules
   (static siblings excluded), never by a grep built from a list of bad-value spellings** -- a
   spelling list cannot be complete, and a call split across lines escapes a line grep (lived
   [[2026-10-14-trigos-epF-part1]]: #843's list missed `not-valid-id` and a two-line call; the sweep
   found both, `787c480a`; the sweep is `scripts/probes/route_sweep.py tests-for <rule>`, US-AGORA-104).

   **The seam chain gates on the test VERDICT with `&&` — never `;`.** A fix-batch seam's chain STOPS on a red (`pytest … && git commit …`, or a tested exit code). A `| grep` on pytest passes on grep's exit code. Tell: a `git commit` chain without `&&`.

   **The second tell: a `;` ANYWHERE in the chain.** A gate holds only up to the first `;`: a diagnostic tacked on with `;` (a `git status` grep, an `echo`) reconnects the tail to `git commit` past a red. Gate `&&` end to end; print diagnostics separately.

   **And the rule binds every outward act the session takes — each `git commit`, `git push`, `gh pr create` and `gh pr merge`, in every repository it acts on** — a child repo's seams and PR step too; a `for … ; done` loop is the same break. (precedent)

   **And the verdict the chain read is written as a field once read** —
   `flask agora write evidence --kind suite --value "<passed>/<failed> <scope>"`
   after the summary line; the gate's own field is written by `flask agora gate <cmd>`
   and by `flask agora preflight` for its verdict (US-AGORA-097 — a hand-typed `gate`
   value is refused) — so the close reads the verdict the seam saw, never a regex over
   the Log (US-AGORA-062, `AGORA-DECL §5`).

   **And `set -e`, a `| tail -1` and a heredoc inside the chain are NOT gates
   either — runbook C1**: a gate runs BARE (a `>/dev/null` redirect keeps its exit
   code, ANY pipe replaces it) and its verdict prints in a SEPARATE command; the tell
   is a `|` before the `&&` (lived session 2026-09-12: commit 4 over a
   `[FAIL]`). The gate is **`flask agora gate <cmd>`** (US-AGORA-097): it runs the command
   bare, prints `[GATE] <cmd> -> exit <n>` last, exits with that code and writes the
   `gate` field itself — `… && flask agora gate pytest … && git commit …` stops on a red.

   **And when a seam's required gate CANNOT RUN, the seam waits — a refused
   gate is a red, not a missing tool.** The whole `&&`-chain family above
   assumes the gate *runs* and asks whether you read its verdict correctly.
   The case it does not cover is the gate that never produces one, and that
   case does not feel like a red: nothing fails, you are simply blocked, and
   the obvious repair is to reach for whatever checks *are* available. Those
   substitutes are the trap — a lint, a ratchet and a detector all inspect the
   tree's STATE, and none of them can evaluate a test's ASSERTIONS, which is
   exactly what a behaviour-changing commit needs checked. So the substitution
   silently swaps out the one gate that was load-bearing while looking like
   diligence.

   The canonical blocker is `tests/_db_lock.py` refusing a second pytest while
   a background suite holds the test DB. That refusal is **information** — it
   says the seam cannot close yet — not an obstacle to route around. Wait for
   the suite, stop it, or point the run at a genuinely separate DB per the
   one-pytest rule; do not commit on script gates and a promise to re-run — and
   a background run is only evidence for the tree it began on (lived
   session 2026-09-01: a commit shipped over a refused
   gate; the red pinned the invariant it reversed).

**A known env-only failure is a BLINDFOLD over the tests beside it — compare the failing SET, never the COUNT.** Keep the accepted local failures (WeasyPrint absent) as an explicit set of node ids and treat any failing id outside it as red, whatever the count says.

**And a verify-round fix batch is a SEAM** — run `flask agora preflight` at its commit: **before the commit when the seam moves no derived artefact; right AFTER it when it carries the stats companion** (`check_stats.py --check` exits 2 on a working copy whose HEAD differs, the #250 shape).

The after-commit preflight is a **visible** command printing its `[FAIL]` lines and the pass line (`| grep -E "^\[preflight\] \[(FAIL|WARN)\]|preflight clean"`, US-AGORA-099); a red there is a commit to amend. The `grep -q "preflight clean"` shape belongs only INSIDE a gated chain that must stop BEFORE the commit. (precedent)

   **Never `-F <file>` a commit message without verifying its first
   line.** Scratch paths persist across sessions and a short-circuited
   `&&` chain skips the write, so `-F` commits another session's message
   (lived session 2026-07-08: a commit landed with the
   prior session's subject). `head -1 <file>` first, or a session-unique
   path.

   **An UNTRACKED artifact of a LATER seam reds an EARLIER seam's pre-commit lint — the hook lints the WORKING
   TREE, not the index.** A story file and a template written for seam N+1 (wired into the catalogue only by
   seam N+1's own patch) sit untracked while seam N commits; the catalogue lint the pre-commit hook runs sees
   the story's `ui_pages:` reference to a not-yet-existing entry and the template extending the base layout
   without its `home:`, and refuses seam N — whose diff is innocent (lived
   session 2026-08-28: the 403 page's story + template tripped seam 7). Rule: when
   several seams are staged in one sitting, **land the catalogue-wiring seam first**, or author a later
   seam's story/template only when its wiring patch runs — never leave them on disk across another seam's
   commit. The park-aside is the recovery, not the plan.

   **When the pre-push hook ABORTS and stages a companion file, COMMIT that companion before retrying — the retry validates the WORKING tree; the push ships the COMMITTED tree.** A passing retry is not evidence the pushed tree is fresh.

   (a) A file the HOOK staged is a **companion, never a rider** — the index-verification discipline above must not unstage it. (b) After ANY hook abort-then-retry, the staged companion goes into a commit (its own `chore(stats)` or bundled with the push's last commit) BEFORE the retry.

   (c) **The regen reads the WORKING TREE — so the companion must ride in the same commit as every file whose CONTENT it counted**: untracked files, and the half that slips — a TRACKED file with uncommitted changes (the session Log feeds `agora.skills.called_by`).

   The tell: the staged stats diff mentions state — a session count, a file tally, a mechanism firing — whose source is not in this commit. The fix is one `git add` of that source alongside the companion, never a companion-only commit.

   **And the open record is never clean between record commits** (the *dirty-by-design tail*): gate a record push on the preflight's pass line, never on an empty `git status`; the tail rides the next record commit.

   (d) **The derived artefacts are a DAG, and `flask agora regen` runs it in order** (`scripts/checks/derived_artefacts.yaml`, US-AGORA-096): the FIRST link after the LAST edit — `flask agora regen && pytest && add && commit` — then ONE preflight (a second reds on the `state-check` tail by design).

   A filter that matches both the pass and the fail line is not a gate: `grep "clean"` matches `[preflight] [FAIL] preflight: NOT clean` too. Use `grep -q "preflight clean"`, never a substring the fail line contains. (precedent)

   **And a STASH-SPLIT seam carries each half's ratchet baselines with it.** When a
   mixed tree is split into two commits by stashing one half, any ratchet baseline
   that was updated FOR the stashed half is now wrong for the tree being committed,
   and the chain stops on a gate that is reporting the split, not a defect. Before
   the first half's preflight, restore every baseline the stashed half owns to
   HEAD; re-ratchet after the pop (lived session 2026-09-03: T-107's
   residue baseline reded the shell-macro commit). When the pop conflicts, the
   recovery is `git checkout HEAD -- <the files>`, `git stash drop`, re-apply the
   patch script — never a hand-merge of the markers.

   If the full body
   reveals something the summary didn't (a forgotten co-reference,
   a hidden migration risk), it's OK to surface that to the user
   between "go" and the actual commit call — abort cleanly if needed.
   **Pushing is a separate** step the user asks for explicitly; never
   chain `git push` to a "go" that was about committing. The user's
   redirects at this gate (*"also include X"*, *"split that commit"*)
   are expected per
   [policy-four-eyes](../../policies/policy-four-eyes.md) rule 5 — the
   gate's value is half error-prevention, half tweak-and-improve.

   **Self-audit trailer:** when a commit bundles a `/learn` self-audit
   patch to a `self_audit_loop: true` skill (the orchestrator patching
   itself via 2.4–2.5 — `/agora` patching `/agora`), add a
   `Self-audit: <skill>` trailer below the co-author trailer. This is
   what excludes the patch from the skill's M2 (`policy-skill-progression`
   Rule 2 self-audit exemption); without it the orchestrator's own
   improvement loop would block its promotion.

7. **The commit records itself.** `scripts/git_hooks/post-commit` runs `flask agora write session-commit <sha> "<subject>"` after every commit: the `commit` Evidence field AND the frontmatter `commits:` entry in one write; an amend REPLACES the superseded sha's two lines (US-AGORA-098), so a stale+fresh pair never lands.

   The hook never fails the commit; a refusal (no open session · a red last preflight, US-AGORA-097) prints one line and the same command is run by hand after the green preflight. `retro-context` reads the rows `[HOOK]` / `[MANUAL]`, so a missing hook shows. (precedent)

If the tree is already clean, say so and move on — no ceremony.

**Discipline trap — "smoke pass ≠ user confirmation".** Running
smoke tests is the right pre-flight before proposing a commit. It is
NOT the user saying "go". The skill must wait for an explicit textual
"go" / "yes" / "commit it" / equivalent. Interpreting "tests passed"
as implicit consent is the most common way this skill commits
unprompted (and was the pattern surfaced by the
an early session, 2026-05-17). The cost of a wrong
auto-commit is a `git reset --soft` + replan; the cost of waiting
30 seconds for a typed "go" is zero. Always wait.

---

## MODE 1 — `--start` (default)

Opens a work session. Run at the beginning of a working block. `/agora --start`
gets current, places the goal (new session vs. continuation), triages the deck,
and turns the goal into a reasoned skill-pipeline plan.

**The default is prompt-LESS — initiate first, steer second (US-AGORA-026).** You
do *not* have to write a large entry-prompt up front. `/agora --start` with no
prompt **reads the reconciled state first** (1.1 — `THREADS` + Goals + the
reconciled COMPASS + the current Era) and **proposes the natural way forward** as a
recommendation-with-default; *then* you steer (accept · adjust · go somewhere
completely different), and the structured goal-prompt is **co-authored after
initiation** (1.2, prompt-less path). A goal prompt is still welcome when you have
one — it's read as the goal and placed directly (1.2, prompt-present path). The
order is the point: orient against the verified state, *then* decide direction —
continuation becomes structural, not a paragraph you have to compose cold (BP-3).
**And the prompt-less proposal asks one standing question BEFORE the plan is drawn:
*"anything done or found since the baton?"*** The baton is a day old at best and the
user does not stop working at `--end` (lived session 2026-09-04:
a 22-item evening walk list reshaped the plan mid-session). The gate line is the fix,
not memory (mechanism captured, #459).

### 1.1 — Load context

Before anything else, `/agora` gets current. Four reads, always:

**The baton — the FIRST read (US-AGORA-035).** The last session already wrote
down what this one inherits. Read it rather than re-deriving it:

```bash
flask agora baton          # the last CLOSED session's baton, every pointer verified
```

It prints the baton's bullets verbatim (the hand-off, written for a human) and
then **verifies each pointer** — Issue still open? story still short of `tested`?
thread still in `## Open`? branch still there? path still present? — as
`[OK]` / `[DRIFT]` / `[?]`. **Drift is information, not a failure**: it exits 0
always, and a `[DRIFT]` line is something to *surface at the 1.4 gate*, not to
correct silently. When there is no baton (no closed session, or a session that
wrote none) it says so and you orient from COMPASS + THREADS as before.

**A `[DRIFT]` on a pointer the baton cites as WORK TO DO gets a content
re-check before it enters the plan — the verifier answers "where does this
pointer live now?", never "is the claim still true?".** A promoted thread's
`[DRIFT]` reads as benign bookkeeping (the content moved to its Issue), and
that reading is exactly where a stale work claim hides: the promotion comment
is itself a claim written at a moment in time, and nothing re-reads it against
the tree. The two-minute check is the work-state axis — do the referenced
tests/pins exist and pass? does the source carry the fixed shape? (lived
session 2026-08-09: T-060 + T-061, flagged benign, had been
fixed 15 days earlier; two phases were planned for them). Same rule for a
**banked map read at 1.1**: a map is a plan artifact with no re-verification
pass of its own, so its members are claims to spot-check, not facts to
inherit (the load-bearing-claim family, applied to the baton's own citations).

This read is **additive, not a replacement**. The baton says *what to do next*;
the reads below verify *the state is what we think*. A baton is a claim like any
other — `reconcile`, `env`, `closure-candidates` and the frontmatter lint all
still run exactly as they did.

**The unverified handoff — what the last blind run left open (US-AGORA-038).**
A blind run's numbered checklist is a first-class deliverable, and until this
read existed **nothing consumed it**: no record tracked which items the user
actually cleared. Run:

```bash
flask agora handoff        # the last `mode: blind` session's checklist, unchecked items surfaced
```

Every unchecked item is **open work carried across the boundary** — surface them
at the 1.4 gate alongside the threads and the closure candidates. It reads the
newest `mode: blind` session whether or not it is closed (a blind run parks and
the user verifies on return, so the checklist worth reading is usually on a
session that is still open). No blind session, or one that wrote no checklist →
it says so and the read costs nothing.

**Planned sessions — what is scoped and ready to load (US-AGORA-037).**

```bash
flask agora plan           # the PLANS.md registry, each entry's status DERIVED
```

Three states matter at 1.1: **`ready`** (gate complete — loadable *now*, a strong
candidate intent), **`loaded`** (an open session is executing it), **`incomplete`**
(a gate field is missing, so it cannot be loaded until someone fills it — surface
it as a small piece of work, not as a blocker). Status is never stored; it is
derived from session files' `plan_ref:`, so the registry cannot drift.

**Recent sessions** — `Read` the last 2–3 entries from
[`INDEX.md`](../../sessions/INDEX.md) and the session files they point to,
plus the tail of [`IMPROVEMENTS.md`](../../sessions/IMPROVEMENTS.md). A session
never starts cold: it starts knowing what the last few sessions did and how
Agora has been evolving.

**Current Era** — read the **`## Eras`** section of
[`COMPASS.md`](../../sessions/COMPASS.md) and surface the Era marked *(current)* —
its theme, the Goals inside it, and its backlog (slot 1). This is **the chapter the
session opens inside** (US-AGORA-016 / RP-AGORA-004 T1); naming it makes
continuation structural rather than inferred. If a goal prompt is given, the 1.4
placement slots it under this Era (or recognizes it opens a new Era). If no Era is
marked current (the Mission cycle parked between Eras), say so — a goal prompt then
opens a new Era. (The full Goal placement happens at 1.4; this is the *context*
surface.)

**The pile — one line (US-AGORA-112).** `flask agora oda --record --line` reads the whole open
board — the round ledger, THREADS, the bug and learn Issues, the current and next Era's tiers — as
one pile, records the day's row for the trend (`agora.pile`) and prints the size per tier and the
oldest unhomed age. A growing age is the cue; each unhomed item is a home to give at the 1.4 gate
(`flask agora oda` lists them). The row rides the opener commit.

**Open threads** — read [`THREADS.md`](../../sessions/THREADS.md) **whole**
(added 2026-06-12 — the central registry replaces scraping session files'
`## Open threads`). Surface the `## Open` blocks as candidate intents, and
flag any thread marked *promote-or-drop due* (≥3 sessions old, Rule 4 of the
registry) — the user decides promote / drop / carry at the 1.4 gate. Never
re-copy threads into the new session file; the session file's `## Open
threads` holds only **this session's deltas** (new ids born, ids resolved or
promoted).

**Skill-system state** — take a *fresh* inventory: `.claude/skills/` (the
skills + their frontmatter), `.claude/policies/` (the active policies), and
`git log --oneline -15 -- .claude/` (what changed in Agora itself recently).
`/agora` is the **driver** of this system — it must always know the *current*
state of it, never a remembered one. If the system looks drifted — several
Sessions since the last full `/inspect-pipeline --audit`, or visible churn in
the `.claude/` git log — flag it as a candidate task for this session.

**Frontmatter pre-flight check (HARD GATE).** Before declaring the skill
system healthy, run:

```
python scripts/checks/validate_skill_frontmatter.py --check
```

This PyYAML-parses every `.claude/skills/**/SKILL.md` and `.claude/policies/*.md`
frontmatter block. The Claude harness uses a tolerant parser, but the VS Code
Claude Code extension uses a strict one — risky scalars (`: `, `#`, leading
`[`, mid-string `|`, `<>`) parse fine for the agent yet crash the IDE with an
opaque "Unhandled case: [object Object]" popup that **blocks the user from
seeing assistant responses**. If the lint fails, **do not proceed with `1.2`**
— surface the failure, run `--fix` (it auto-quotes `description` /
`argument-hint` / `name` / `title`), confirm the diff with the user, and
commit it as the first commit of the session before touching anything else.
The underlying rule is [`policy-skill-authoring`](../../policies/policy-skill-authoring.md) Rule 2.

**Registry-state pre-flight (US-AGORA-048) — same breath, second command:**

```
flask agora state-check
```

Read-only validation of every registry-shaped state file (THREADS ·
IMPROVEMENTS · policy-breaches · the experience journals) against the write
path's own invariants. A `[FAIL]` here means a registry file was corrupted
OUTSIDE the writer (a freehand edit, a merge) — repair it before the session's
work begins, exactly like a frontmatter failure. This is what makes the #286
class (a truncated THREADS.md read by three consecutive `--start`s) loud at
the very next session open instead of never. The same run is the capture
spool's loud surface (US-AGORA-051): a `[SPOOL]` line is an **undelivered
capture** — run `flask agora capture --flush` to deliver it idempotently (a
pending queue, not corruption; it never fails the check).

**The product backlog state** — read `docs/stats.yaml`
for the story-status breakdown, and surface the **actionable buckets** so the
user can see what's next for the product and pick a goal informed by it:

- **Resume** — stories at `in-progress` / `partially-implemented` (name them — these are the half-built ones)
- **Ready to build** — stories at `approved` / `planned` (name them — these are `/implement-story` candidates)
- **Need tests** — stories at `implemented` but not `tested` (name them — `/iterate` / test-writing candidates)
- **Need refinement** — counts only for `draft` / `review`

Glob `docs/requirements/stories/**/*.md` and read frontmatter `status:` to fill
the named buckets when `docs/stats.yaml` only gives counts. Keep it a tight
summary — three buckets of story ids + titles, not a wall of text. This is the
"what are the next steps for the product" picture; it is shown **every `--start`**,
whether or not the user has already given a goal prompt.

**The same read carries the mechanism-adoption flags (US-AGORA-050):** while
in `docs/stats.yaml`, check `agora.mechanisms.below_threshold` — every name
there is a mechanism below the firing threshold across the window, surfaced
for the **call-sites-or-retire decision**. Mention it in the 1.4 proposal when
non-empty (one line; the user decides whether this session takes one on). The
counts are a labelled session-mention PROXY; the live learn-store number is
`flask agora store-level` when the round needs it.

**Open GH bug Issues (US-AGORA-001)** — surface user-opened, unresolved
bug Issues as candidate intents alongside the carry-over Open threads
from prior sessions. Read-only here — the mirror happens in `/fixbug`,
not in `/agora --start`.

```bash
flask agora list-bugs
```

The CLI is a thin wrapper around `gh issue list --label agora:type:bug
--state open`. A failed `gh` call (unauthenticated, rate-limited, offline)
prints `[?] gh failed: <reason>` and exits 1 — never an empty board (#905);
Open threads from prior sessions carry over until it answers.
When N > 0, surface the issues by number + title; the user can route
one to `/fixbug --gh:<n>` later in the session.

**GH Issue closure candidates (drift correction).** Open Issues whose
*tracked work has already shipped* are the second candidate-intents
source — they're surfaced now so the user can nod through the closures
at session open instead of catching them by hand after the fact (the
leak that opened #50 + #77 + earlier #74/#75: shipped work staying
open across the next `--end`).

```bash
flask agora closure-candidates
```

The CLI cross-references three signals on disk:

1. **Goal closure** — COMPASS lists a Goal under "Goals (closed)" (in
   `COMPASS-closed.md` since US-AGORA-067; every reader reads both files) but
   its `**GH mirror:** #<n>` is still OPEN on GitHub.
2. **Cascade sub-goal** — an open sub-goal Issue's body declares
   `**Parent Goal:** #<n>` and that parent Goal is itself a Goal-closure
   candidate (1) or already-closed on GitHub.
3. **Story closure** — an open sub-goal Issue's title carries a
   `US-XXX-NNN` whose story file in `docs/requirements/stories/`
   declares `status: tested`.

If N > 0, surface the list by number + title + reason + cite. **Closing
happens at `--end` step 2.8b** (the 4-eye gate); 1.1 is the
*proposal-now-so-the-user-sees-it* surface. The user picks per-Issue
whether to close it this session or leave it open with a note (e.g.
"sub-goal advanced but not yet shipped — keep open"). A failed `gh`
call prints `[?] gh failed: <reason>` in place of *no candidates*
(#905) — drift correction is a soft surface, not a gate: surface the
line and proceed.

**Environment — the dev server and the RIGHT database (US-AGORA-031 / 032).**
An executed step, not guidance to remember:

```bash
flask agora env          # server probe + resolved DB name + recency + divergence
```

Its `python:` line names the interpreter every launch in the session uses — a bare
`python` is the system Python. That trap and the other harness traps (cp1252 stdout,
heredocs, gated chains, completion signals, the capped grep) have ONE home, the
tooling runbook (`AGORA-DECL §3`);
`/learn` routes a tooling lesson there, never into this file.

Three outcomes, and each has a defined next move:

- **exit 0** — the server is serving (or is reported down), the DB is the one
  the last session used, and the baseline is refreshed. Proceed.
- **exit 2** — the DB is unreachable: `[DB DOWN] <host>/<db>` (the factory skips
  its DB boot for `flask agora`, so this line prints instead of a traceback —
  US-AGORA-059, `AGORA-DECL §S`; `devlink` degrades the same way). The command
  names the compose-resolved service it *would* start; re-run with `--start-db`
  to start **that** service. If it reports `ambiguous` or `none`, **stop and
  ask** — never start a candidate (this is the whole lesson of 2026-07-22). When more than the database is missing — a fresh clone, the always-on workstation — `/deploy --agora --check` (US-AGORA-065) reports all ten substrate items and `/deploy --agora` installs what a command can.
- **exit 3** — **recency divergence: STOP.** Data went backwards, which cannot
  happen on a live instance without a deliberate reseed. Surface it to the user
  before any read or write is trusted. If the change is expected, `--accept`
  records the new baseline.
- **exit 4** — **served code is STALE (US-AGORA-049 / #236).** A server answers,
  but NOT with your working tree: the marker probe (`/api/dev/served-marker`,
  same flag family as the devlink) compares the server's boot time against the
  newest source mtime — a dead reloader, a `--no-reload` launch predating the
  edits, or a no-`.py` phase against a template-caching process all land here.
  Do **not** report a change as live until a restart turns this green.

**A throwaway PROBE server is under the same served-code discipline as `:5000` — and
`flask agora env` does not cover it, so verify it by hand.** A `flask run --no-reload` on
a spare port caches every template it rendered before your edit (Jinja's per-process
cache) and serves the stale page through "restarts" whose kills never took (on Windows
`taskkill` is not on the Bash tool's PATH — exit 127, silent in a chain; kill by PID via
PowerShell and confirm the listener's start time before calling it restarted). Launch with
`--debug --no-reload`, and before reading a probe's verdict `curl` the served page for the
edited line (lived session 2026-08-29: three probe rounds against
a fix that was right the first time). **The dev server is agent-owned.** Launch it as a **background task** (not a
foreground command) so restarting after a fix is something you *do*, not
something you ask the user to do. A restart is only asserted once
`flask agora env` reports it serving — *"I restarted it"* without the probe is a
claim, not a guarantee. Do **not** silently restart while the user is
mid-interaction with a form; say so first. If the server was started outside
your control, say that plainly and fall back to asking — never report a restart
you did not perform.

**But "serving" is NOT "serving YOUR code" — the probe proves a weaker
proposition than the claim it licenses.** `flask agora env` answers *is a server
up on :5000?*; the thing you are about to tell the user is *your change is live*.
Those come apart, and when they do the probe actively works against you: it
converts *"I should look"* into *"I already looked."* **And it answers for ONE port**: a
second server of the same app on the box (a demo instance on another port, started
by a different script) serves the NEW static JS from disk and the OLD Python it imported at boot, so
*"the fix is live"* names the user's port or is a claim about the wrong server (lived
session 2026-09-19: *"documents fixed, Insights still crashing"*, both
true; `env` enumerating every listener → #477). Two mechanisms on the one port, both lived
in one session (session 2026-07-27):

- **The server predates the edit.** Launched with `--no-reload` before the work
  started, it serves the old templates indefinitely while reporting HTTP 200. And
  `flask run` enables the reloader only with debug — plain `--reload` is the
  explicit flag; *"Debug mode: off"* in the log means stat-reloading is off too.
- **A reload FAILED and the old process kept serving.** On Windows the stat
  reloader can die mid-restart with `OSError: [WinError 10038]`; the parent keeps
  answering on the port, so every probe stays green while the served bytes are
  stale. Symptom: your tests pass against the new code and the live page shows
  none of it.

So **before telling the user a change is live, fetch the page and assert a marker
from the change** — a class name, a data attribute, a rendered string. When the
marker is absent the honest next move is `os.utime` on a `.py` file (forcing a
restart) and re-fetch, not a hunt for the bug you have not got.
**Both halves are commands now (US-AGORA-049):** `flask agora env` runs the
served-code marker probe itself (exit 4 = stale, above), and

```bash
flask agora verify-fetch "<path>" --user admin --marker "<rendered string>"
```

mints a devlink, follows it **with a cookie jar**, asserts it **landed on the
requested path** (a cookie-less fetch gets the LOGIN page at HTTP 200 — the
lived #295 harness failure; a retired 302 bridge lands elsewhere and refuses),
and only then checks the marker against the body actually served. Exit 0 is
the licensed claim; the fetch consumes its own mint, so the user's link is a
separate mint as ever. Run it at every verify handover in place of a hand-rolled
curl.

**And a phase that ships NO `.py` file never trips the stat reloader at all —
force the reload BEFORE the verify handover, every time.** Templates, JS and CSS
change, no Python does — so `flask run --reload` keeps serving its **cached
compiled templates** (Jinja caches per-process with debug off) and the verify
links go out against old markup (lived session 2026-07-28: the marker
discipline held in the `.py` phases and was skipped for the template-only one).
The rule is mechanical, not situational: **any phase whose diff contains zero
`.py` files gets an `os.utime` on a `.py` + a re-fetch + a rendered-marker
assert before any live claim** — a restart is a fully reliable process or it is
a habit, not a tool (feeds the #236 marker-check mechanism).

**And pick the marker from the RENDERED output, never from the source.** The same
session's first live check searched the served HTML for `US-SET-036` and
`PAGE-ZONE` — both **Jinja comments**, which are stripped at render — so the check
could only ever return False and read as confirmation of a stale template that had
in fact already updated. A verification method that cannot return true is worse
than none: it manufactures agreement with whatever you already suspect.

**A verification that returns the SAME ANSWER before and after a fix cannot fail, and
a check that cannot fail is a formality, not evidence.** Before running it, name the
input that would have made it red; if you cannot, it measures something other than
the change (a light-node scan returned zero on both sides of two fixes because neither
surface renders in a walk — replaced by a computed-value probe per theme with an
unscoped control, session 2026-08-30). A positive control's planted mutation is verified ON DISK before its verdict is read — a `sed` range that
matched nothing reads as "nothing grew" (session 2026-09-03) — and a mutation a spawn PROPOSES is a claim: a
survivor names a test that cannot fail, so strengthen it or pick a line it asserts (3 of 8 survived, session 2026-10-02). A
control that changes TWO variables is not a control: fill the 2×2 (runbook D3). And
**one pytest owns the test db; a browser-driven run owns the MACHINE**: no second
pytest against the test database while a suite runs (phantom failures, ~40 min of false
archaeology — session 2026-07-05); the separate-DB escape is
a second database URI plus an allow-concurrent flag, which DISABLES the lock and
makes "separate" yours to verify (session 2026-07-29); while a Selenium
probe, suite or timing survey runs, nothing else runs at all
(session 2026-08-30, #426).

**Hand back a deep link, don't describe a path.** At every verify handoff:

```bash
flask agora devlink "orders?tab=open" --user admin
```

The user clicks instead of navigating — **and every STEP names a control the user can SEE**: check its visibility gate (an enable toggle's `display:none`, a collapsed `<details>` — `/fixbug` 5.2b's twin) before writing it. The mechanism is `verify-fetch --visible <selector>` (#477); the Git Bash leading-slash trap is runbook B4.

**A walk checklist drawn from batons is a list of claims: each step is checked against the code before the handover** — which ROLE lacks the grant (read the default role's grants) and how it signs in (`devlink` is superuser-only: name the password login and where its password is declared).

Each step is also checked for whether the fixed ROUTE has a caller on any page and which SURFACE carries the control — and a step never names a retired shortcut.

**What the UI ANSWERS with is read from THAT action's route response and its caller, cited `path:line` in the step** — never from the convention (a refusal `htmx_error` -> `showError` -> `KisDialog`; a save's `flash` toast) or from memory.

**Devlinks expire in 300 s and are SINGLE-USE**: mint only with the user present — a blind park's handoff names surfaces/paths; the attended walk mints fresh. Never hand over a link your verification touched (a curl consumes the token); the user's link is a separate, untouched mint, or none. (precedent)

**COMPASS reconcile — re-initiate the short-memory (US-AGORA-018, the crux).**
COMPASS is a **reconcilable short-memory**: the GitHub Issues hold the planning
truth; COMPASS is a verified working-set *cache* re-initiated each session
(RP-AGORA-004 T13). Run:

```bash
flask agora reconcile
```

It diffs COMPASS "Goals (active)" against the GH-Issue + git-tag truth and
**flags** per-Goal divergence — `closed-but-active` (a closed Goal still parked in
the active section), `issue-closed` (COMPASS active but the mirror Issue shipped),
`issue-open` (COMPASS closed-marked but the Issue is still open), `milestone-missing`
(a closed Goal with no matching `milestone-*` git tag), and `no-gh-mirror`. **It
flags, it never rewrites** — COMPASS's `Intent` prose is hand-authored (Shape B).
**It also reads dispositions (US-AGORA-056, `AGORA-DECL §2`) and exits 2 on a
finding:** every open learn Issue's latest disposition against its destination —
a fold into a closed Issue or a shipped story, a home at a closed Goal, a
parked-to-phase, a round-contract fold whose member is still open. A finding
names its remedy (`flask agora dispose`, 058); propose it at the 1.4 gate.

When drift is reported, **correct COMPASS (or the Issue) before the session's work
begins** — this is the *reinitiate* step: the session opens against a verified
working set, not a drifted one. The fix is usually consolidating a closed-but-active
Goal into "Goals (closed)" (`COMPASS-closed.md`) or ticking a stale status; surface the drift list to the
user and correct at the 1.4 gate. (`flask agora reconcile` is also the prime check
the US-AGORA-024 drift scheduler runs on a schedule.) When a `gh` call fails, reconcile
prints `[?] gh failed: <reason>`, runs the file-only checks (`closed-but-active`,
`milestone-missing`, `no-gh-mirror`) and exits 1 — never "in sync" (#927).

### 1.2 — Establish the goal → new session or continuation

There are **two paths** into this step (US-AGORA-026). Pick by whether the user
gave a prompt:

**Prompt-less path (the DEFAULT — `--start` with no goal prompt).** Agora has just
loaded the reconciled state (1.1). Now it **proposes the natural way forward** —
a recommendation-with-default per [policy-four-eyes](../../policies/policy-four-eyes.md)
Rule 2, read off the verified working set:

1. **Propose** — name the obvious continuation: the current Era's open Goal + its
   next unticked success criterion, OR the freshest carried `THREADS` item, OR a
   surfaced closure/drift the session should clear. State *one* recommended
   direction in prose ("the natural next step is X, because Y"), not a menu.
2. **The user steers** — accept the proposal, adjust it, or go somewhere
   completely different (a brand-new Goal/Era unrelated to the recommendation).
   Direction is decided *after* Agora has oriented, never before.
3. **Co-author the goal prompt** — once the direction is settled, compose the
   structured prompt **with** the user, in three parts: **intention** (what we
   want this session to achieve) · **context** (the reconciled state it builds on)
   · **instruction** (the concrete work). Confirm it, then it becomes the session
   `intent` and feeds the 1.4 plan. This is the "big prompt, co-authored after
   initiation" — the user never has to write it cold up front.

**Prompt-present path (a goal prompt WAS given).** The prompt is the **goal** —
place it directly, no co-authoring step needed. Classify it against 1.1:

- **Continues a session** — the goal matches the `intent` or an **Open thread**
  of a session that is `status: open`, or of a very recent `closed` one whose
  threads are unfinished. → *Append to that session file* (step 1.5,
  continuation path). Re-open a `closed` file if the work genuinely resumes.
- **A new session** — the goal is unrelated to recent work. → Open a fresh
  session file (step 1.5, new path).
- **Ambiguous** — name the open/recent session it might belong to and ask.

**Both paths converge** on the same placement question (continuation vs. new
session) and proceed identically from 1.3. Never silently open a second session
on top of an `open` one — either the new goal continues it, or the open one is
closed out first.

### 1.3 — Clean-start triage: working tree + open PRs + main-HEAD CI

"Start clean" is THREE checks, not two:

1. **Working tree** — run **the commit-tree triage** (above) on whatever the
   previous session left behind. The deck is cleared before new work begins —
   policy Rule 5.
2. **Open PRs** — `gh pr list --state open` and `gh pr status`. Surface every
   open PR with its state: waiting on review, mergeable, or stale. A session
   that starts on top of three forgotten PRs isn't starting clean. Don't merge
   or close anything — surface them so the user decides whether clearing a PR
   is part of *this* session's goal (and if so, it goes into the plan in 1.4).
   **A PR's red check is read against its run's HEAD SHA, never as the branch's
   state:** `gh run view <id> --json headSha`, then `git log <head>..HEAD --
   <the failing surface>` — a red on an older head may already be cleared, and
   a fix phase drawn from it is a phase for a defect HEAD does not have (lived
   session 2026-10-30: #945's red on `3be6a4c0`, cleared by #941
   before the session opened). The rule is EVENTS `PR-merged`'s green read (US-AGORA-093):
   a PR is triaged by its head sha's conclusion, never by `main`'s, and its merge is that
   chapter's script — the record step is `flask agora write milestone-record --pr <n>`.

   **Classify each PR's risk before proposing a merge — three buckets:**
   - **unproblematic** — docs, a test, a self-contained app change with green
     checks and no infra/dependency surface. Merge is a quick deck-clear.
   - **has-dependencies** — the change has a *paired* surface the PR does NOT
     touch. Canonical case: a **Dependabot bump of an infra-paired client**
     (`elasticsearch`, `pymongo`, `redis`, a DB driver) bumps the library but
     NOT the server image it talks to, and a major bump may drop a removed API
     the app still calls. Before merging, check (a) the paired server/image
     version (`docker-compose*.yml`) and (b) grep the app for the removed-API
     call shape. **Green CI does NOT clear this** — CI often doesn't exercise
     the real paired service (it falls back).
   - **problematic** — touches auth/security/migrations/data-shape, or a large
     diff in a fragile area. Needs deliberate review, not a deck-clear merge.

   **Merge only on an EXPLICIT green — never `gh pr merge --auto` on a repo
   without auto-merge enabled.** When auto-merge is disabled at the repo level,
   `--auto` does NOT queue-behind-CI as intended — it **falls through to an
   immediate merge**, front-running the PR's still-pending `Test` job (the
   "merge only on green" discipline, silently violated). Poll the check
   conclusion first (`gh pr checks <n>` all pass, or `gh run list --branch main`
   after — the explicit-conclusion read of the Milestone ceremony trap, applied
   to PR merges) THEN run a plain `gh pr merge --squash <n>` (lived
   session 2026-07-09: `--auto` merged Dependabot #188 with
   its Test job still pending).

   State the bucket when surfacing each PR. For **has-dependencies** /
   **problematic**, the paired-surface check / review is part of *this
   session's* plan (1.4), not a reflexive merge (lived
   session 2026-05-30: an `elasticsearch` bump deck-cleared over a
   server-image skew and a removed `body=` API).
3. **Main-HEAD CI conclusion** — `gh run list --branch main --workflow Test --limit 1`
   (Test by name: the newest row on `main` may be Build's). If its
   `conclusion` is `failure`, **surface as a session-blocking finding** — and
   read its **date**: a green from before a dependency's release is stale, since
   an unpinned `>=` requirement resolves to the newest release on CI's fresh
   install, so `main` reads green and is red on its next run (lived
   session 2026-10-22: last Test 2026-10-15, #904 red on every fresh run). Recommend an unblocker fix (which may itself become Phase 0 /
   Phase A0 of this session) *before* the goal-prompt work starts. The
   `--end` close-gate preflight only checks LOCAL state (ruff + check_stats +
   requirements_lint + frontmatter); it does NOT check whether the prior
   session's *push* went green. A Path-B-park session never fires the
   `gh run watch` ceremony, so a red main HEAD can sit undetected across N
   sessions until the next session's PR triage exposes it (cost: ~20 min of
   diagnosis time mid-session). The drift surfaced 2026-05-29 — a stale test
   reded `main` 2026-05-25; three sessions ran without noticing; the fourth
   only caught it at PR triage. Catching it here makes the unblocker the
   first explicit phase, not a session-blocking surprise.

### 1.4 — Place the goal in the vocabulary

Read [`COMPASS.md`](../../sessions/COMPASS.md). Surface the active **Vision**,
the current **Mission** cycle, the current **Era** (the chapter the session opens
inside), and the open **Goals** with their success criteria. This is the durable
picture the user's prompt slots into.

Now place the user's prompt — **Era first, then Goal** (the session opens inside an
Era; the Goal lives inside that Era):

- **Continues the current Era** — the prompt advances a Goal already inside the
  current Era, or opens a new Goal parented to it. Name the Era; the new Goal gets
  `**Era:** <name>` in its COMPASS entry.
- **Opens a new Era** — the prompt starts a themed chapter unrelated to the current
  Era (or the Mission cycle parked between Eras). Propose the Era (theme · why ·
  Goals-to-go-inside · when-finished), register its `agora:era:<slug>` label via
  `flask agora` (`ensure_era_label()`), and on confirmation open it in COMPASS's
  `## Eras` section before placing the Goal. **Forward-only** — don't retro-fit past
  Goals into the new Era.
- **Closes the current Era** — the prompt's work finishes the last open Goal in the
  Era → the **`New Era`** EVENTS.md chapter fires at `--end` (finish → document →
  start). Flag this at the gate so the session is scoped to land it cleanly.

Then place the Goal within the Era:

- **Continues an active Goal** — name it. The session's sub-goals are
  the next checks on that Goal's success criteria, or work that advances
  toward them.
- **Opens a new Goal** — name it, propose success criteria, and (on
  confirmation) append the Goal to COMPASS.md before continuing. A Goal
  without success criteria has no Milestone to trigger. **Per
  [policy-issue-templates](../../policies/policy-issue-templates.md)
  Rule 6:** the COMPASS entry + the `milestone-<slug>` tag declaration
  land in the same edit (the tag is the closing contract — declared
  with the criteria, fired at Goal closure, immutable once declared).
  If a **Backlog Goal Issue** already exists for this intent, this is
  the Backlog → Active move: `flask agora write compass-activate --goal <n>
  --file <entry.md>` (US-AGORA-113) writes the entry, strikes its backlog
  index line and prints `reconcile`'s verdict for it.
- **A Sub-goal under no clear Goal** — surface that and ask. Per
  [policy-issue-templates](../../policies/policy-issue-templates.md)
  Rule 6, every sub-goal references a parent Goal. Either it belongs
  to an existing Goal (link it explicitly in the session file + the
  sub-goal Issue body via `**Parent Goal:** #<n>`) or a Goal needs to
  be defined first (and the next prompt is to define it, either as a
  new Active COMPASS Goal or as a new Backlog Goal Issue).
- **Filler** — a session that advances no Goal (exploration, freestyle, a break): tag it
  `goal: Filler` in frontmatter (oda's session kind; La Paz's records keep `exploration`, and
  the readers accept both). No Milestone is targeted; `--end` parks rather than ceremonies.

Given the placement, work out the **skill pipeline** to advance the
relevant sub-goals — which skills, in which order, with which natural
commit seams. The pipeline plan is reasoned from the sub-goals, not
pasted from a table. Classify the session `type` (see **session types
& shapes** below) as a label, and confirm the plan with the user before
writing it down. For a doctor sweep, enumerate the concrete targets
(pull from the page registry, the entity lists, or a
backlog the user points at) so the queue is walkable.

Apply [policy-skill-routing](../../policies/policy-skill-routing.md) —
this is the **prospective** routing gate. Every sub-goal whose work
matches an existing skill's purpose is routed *to that skill* in the
plan, even if the user didn't name it; inline work appears in the plan
only with a one-phrase justification (no skill covers it · genuinely
trivial · needs in-flight context), written `inline -- <why>` in the box or as
an `exception` field citing policy-skill-routing Rule 1 (*route by default; inline
is the named exception*) and the phase: a box
naming a fix without either is `state-check`'s `[INFO] [routing]` line at the
opener's preflight, and a `fix(` seam without one is the post-commit hook's
`[WARN]` (US-AGORA-109). The plan is where "build it by
hand" drift is caught *before* it happens — the `--end` close-out paper
(2.10) catches what slipped past here.

**A plan PHASE is a gate boundary — so one skill invocation is ONE phase, never
four.** The session plan's granularity and the phase-completion gate's granularity
are the same thing: the gate fires when a checkbox flips, so every checkbox the plan
writes is a promise to stop and ask. When the plan splits a *single* `/implement-story`
(or `/check-page --finish`, or `/plaza`) invocation into its internal steps — "build
the check" · "retire the prose" · "write the tests" — those boxes cannot honestly gate,
because the skill runs them as one continuous unit under one authorization. The result
is a plan that *looks* like five gates and delivers one, which reads afterwards as
skipped discipline rather than as a mis-drawn plan.

So at 1.4, draw each phase at the boundary where you would genuinely stop: **one phase
per skill invocation**, plus a phase for each decision that needs the user between
invocations. The invoked skill's own internal gates (`/implement-story` Phase 2b's plan
gate, for instance) fire *inside* the phase and are the skill's business, not the
session plan's. A phase whose deliverable you cannot describe without naming the skill
that produces it is a sub-step, not a phase. **The RECORD of a build phase (ledger rows, the Log, the regen chain) is that phase's last seam, never a phase of its own** — a checkbox for it promises a gate nobody needs, and it gets written as fired without a nod (lived session 2026-10-04). **A `/wiki` sweep's EDIT half is drawn after the last phase that changes source; its READ half may run before it, where its findings are wanted** (lived session 2026-10-13: the whole sweep ran before the walk, the walk's twelve fixes re-staled 25 pages, and the reseed, rehash and stamp ran twice) — **and an edit phase that ends in `stamp` names the whole-page read the stamp licenses (`/wiki` 2.6) and its size in pages, or reads `no stamp`: every page it edits, and every page whose tracked source the session's fixes change, loses its stamp at the reseed** (lived session 2026-10-23: P-063's "reseed → rehash → stamp" over ~2 250 unsized lines; dropped by method adaptation, 10 stamps retired).

A low gate count has two causes — mis-drawn boundaries, or a gate that genuinely
did not fire — check which one you have before treating it as a breach (lived
session 2026-07-26 · session 2026-07-25: six
phases drawn over one invocation, gate fired 2×; 4 genuine phases, gate fired 0×
— the breach).

**The same rule has an INVERSE failure, and a loaded plan is where it hides: ONE
phase far too large.** The rule above guards against splitting one invocation into
four boxes. Nothing guards the other direction -- drawing a plan's scope MEMBER as
a single checkbox when nobody has measured what is inside it. The two look nothing
alike while you are planning and identical afterwards: both produce a plan whose
checkboxes do not match where the work actually stops.

A loaded `P-NNN` makes it likely rather than possible. Its `scope` field names
members in the planner's words, and those words are the natural phase text -- so
1.4 copies them, and a member that decomposes into several shapes with several
different treatments becomes one promise to stop. **The tell is mechanical and needs
no judgment: you are drawing a phase from a plan's scope member whose internals you
have not yet sized.** The vocabulary for the fix already exists -- a **split point**
(the cheatsheet's term: the boundary a plan names *in advance* as the place it may
legitimately split) -- so the correction is not a new concept but its placement:
**when a unit's internals are unmeasured, the split point belongs INSIDE it**, not
only between it and its siblings.

Cheapest remedy, in order of preference: run the opening audit BEFORE finalising
the phases (Phase 0 already produces exactly this sizing -- it simply ran after the
gate), or draw the inherited member as *provisional* and let the audit split it
(lived session 2026-08-31: P-039's member 1 was ~102 sites
across four shapes; it split 1a–1d mid-session, past the declared split point).

**When 1.4c forecasts per-unit commits, 1.4 must name which phase boundaries are the
COMMIT SEAMS.** The two plans are drawn minutes apart and are routinely both correct on
their own terms while disagreeing with each other. 1.4 draws phases at *gate* boundaries
(one skill invocation = one phase, above); 1.4c forecasts commit *groupings* by concern.
Nothing connects them — so a plan can promise "one commit per story" while its phases let
two stories accumulate in the same files before either is committed. By the time the
divergence is visible, the fix needs interactive hunk staging, which is unavailable, and
a hand-split patch reintroduces exactly the mis-staged-commit risk the index-verification
rule (triage step 6) exists to prevent. The declared grouping is then unachievable, not
merely inconvenient.

So when the repo plan forecasts a commit per story / per unit, **mark those phase
boundaries in the plan itself** — *"Phase B ends at commit 2"* — and treat reaching one
as the trigger to commit, not as a place you may commit. A phase whose build is green and
whose story has flipped to `implemented` is a seam whether or not you feel finished.

Not every phase boundary is a seam, which is why this is a judgement rather than a rule:
some phases produce nothing committable on their own, and some produce several commits.
The requirement is that the *plan says which*, before either plan is executed (lived
session 2026-07-27: two forecast build commits, one phase per story, both
stories in the same four files — one commit, unrecoverable as declared).

**And a seam whose gate reads LIVE STATE that a later phase repairs sits AFTER that
phase — name that at 1.4 too.** The seam rule above says *commit when the phase is
green*; the "refused gate is a red" rule (triage step 6) says *a gate that cannot pass
is a red, not a missing tool*. Between them is the case where the gate is red because
the RECORD it reads is pre-repair, not because the change is wrong: a mechanism that
adds an invariant over the registry (a `state-check` rule, a reconcile check) ships
with a real-repo smoke test, and that test reads the live registry — which the story's
own acceptance run, a later phase behind the user's nod, is what cleans (lived
session 2026-09-05: 058's Issue-parent invariant reded the real-repo
smoke on threads Phase C was about to promote; seam 4 waited). The tell at
planning: *a phase adds a check over live state and the phase that repairs that
state comes later*. Draw the seam after the repair, say so in the plan's seam
line, and do not read the interim red as a defect.

**The MIRROR: a seam whose gate READS THE RECORD sits BEFORE the run that reads it —
the record commit precedes ANY full-suite run, not only a blind one.** The rule above
moves a seam later because a phase repairs the state its gate reads; this is the same
dependency reversed. The suite's real-repo pins (`tests/cli/test_agora_state.py`, the live
stats-collector / prose-mass / record-consistency tests) read `.claude/sessions/` **from
disk**, so an untracked session file reds them: "run the suite" before "commit the record"
is unrunnable, failing on the session's own bookkeeping rather than on anything it built.
The blind-run section says this, which is why it is missed — **an attended session never
reads there**, and the dependency belongs to the suite, not to being unattended. Hence
1.4c forecasts **two** branch `chore(agora)` commits (opener, then verdict), and the
preflight's record-shaped reds at a first seam (`stats.yaml` stale · `state-check`) are the
**dirty-by-design tail**, cleared by committing in DAG order (lived
session 2026-09-16: Phase 1 drawn as "no seam, nothing commits here"; the
opening preflight caught it and the declared grouping was wrong by one).

**The Arc-③ conduct chain (US-AGORA-040 — the chief-doctor routing).** During
Themelion-Arc phase ③, cleanup work routes **`/agora → /design --conduct →
doctor → skill`**: the session plan names `/design` as the conductor of each
cleanup sub-pass, and the sub-pass employs the doctor that owns its
verification half (`/check-page` · `/check-ui-entity` · `/check-coverage` ·
`/wiki` · `/selenium` · `/manage-translations`) rather than re-implementing
its checks. A phase-③ plan that hand-rolls a doctor-owned check inline is a
missed-routing finding at 2.7's surviving close-out surface.

**Premium-page coaching hook (the discipline anchor for Goal #85's
rollout).** When a planned phase includes a build skill (`/implement-story`,
`/fixbug` with a UI tag, or direct frontend edits) that
touches surface elements on a page **NOT** in the **reference-quality
page list** (see `docs/implementation-plans/implementation-plan-pages-reference-rollout.md`),
prepend `/check-page <slug> --audit` to the phase as a prerequisite.
The audit is read-only (per Layer 1–4b) — it costs minutes and surfaces
the structural drift that would otherwise show up in the next iteration
round. Confirm the insertion with the user as part of the plan
4-eye gate (below) — the user can override with "we accept the drift
this time" but the override is logged as a missed-routing finding in the
`--end` close-out paper (2.10). The IMPROVEMENTS-cited driver was session 2026-05-23
— every iteration-round fix was a *predictable consequence* of
building UX into a non-premium baseline; the coaching hook catches
that prospectively. Reference-quality page list lives in the rollout
plan doc and is maintained per-phase as the rollout walks.

**Hub-page registry pre-flight (the layout-first rule).** Companion
to the premium-page coaching hook above. When a planned phase is a
Goal #85 page-rollout phase **on a hub page** (a page registered in
the hub registry), check the hub's registry entry
populated-vs-placeholder state **before** proposing per-zone work:

- **Populated** (declared `domains` + `subtabs` with `scope_options` per
  subtab — the first finished hub is the reference shape): per-zone polish is the right
  next phase; proceed with the premium-component sweep.
- **Placeholder** (empty `domains: []` + `subtabs: []` — comment names
  it explicitly as a placeholder, e.g. the second hub at the time of this
  rule's authoring): **the structural promotion is the PREREQUISITE
  phase, not a follow-up**. Recommend that the session plan opens with
  a "populate registry + split monolithic template into per-subtab
  includes + route restructure + URL-addressable nav" phase. The
  per-zone polish phases come AFTER. This is the reference hub's lived
  precedent (the three sessions that closed its
  page-complete milestone) — *layout first → zones walk*.

The IMPROVEMENTS-cited driver was session 2026-05-25:
session planned Round 2 as a premium-component sweep on a second hub's
monolithic 953-line template with its registry entry
still a literal placeholder. The structural-promotion need surfaced
mid-session as a Round 2.5 add-on instead of being Round 2 itself.
The bidirectional 4-eye gate caught it — but caught what should have
been caught here at planning. Surface the populated-vs-placeholder
status as a 4-eye-gate input; if placeholder, the recommended plan
opens with the structural promotion.

**The hub LANDING (the overview) is its own explicit phase — sequenced AFTER
every leaf is in, BEFORE the leaf-specific premium work — and it is BIG, not
an addon.** When planning a hub Goal (the La Paz hub-by-hub pattern), the
overview landing is **the reference hub's home pattern** (a top-level overview tab +
per-domain KPI badges + a configurable `<hub>.home` dashboard) and is ≈80% of
the hub's structural work — *not* a last-minute item to fold into an add-on
session. **Plan it as a named phase in the hub's §-sequence: leaves-move-in →
landing → per-leaf premium changes.** Two things this prevents: the landing
forgotten, and the **KPI-cards-in-every-leaf** strip (the reference hubs' per-leaf
chrome) forgotten alongside it (lived session 2026-06-28:
both squeezed in at the finish of the §4 add-ons). At `--start` 1.4 for a hub
Goal, surface the landing as an explicit plan phase and confirm it's scoped as a
real build (it routes to `/implement-story`'s hub-landing build pattern — the
reference-hub mirror + its styling gotcha live there).

**The hub's DOMAIN / TAB structure is an explicit, CONFIRMED plan item at 1.4 —
never inherited silently from the RP/story and discovered post-build.** When a
build session opens a **hub SHELL**, the domain grouping (which tabs, what's under
each) is the *first* thing to state and confirm — read it from the planning
artifact (RP / story) and **present it in the plan**, and **flag any divergence
from the user's earlier framing before a line is built**. The trap: the shell's
structure was decided in a prior planning session (e.g. RP-THER-001 resolved
FUNCTION-domains), so the build session inherits it as settled and builds it
*without surfacing that it changed the user's remembered plan* — the user then
discovers the new structure by looking at the built shell, not from the
orchestrator. That's a silent plan-change, and it reads as one even when the
decision itself is sound. So: (a) name the domain/tab structure explicitly in the
`--start` plan; (b) if it diverges from what the user last framed (e.g. "3
discipline-tabs" → "4 function-tabs"), say so *and why* at the plan gate, before
building; (c) the structure then holds for the session — a mid-build restructure is
a redirect, not the default (lived session 2026-07-07: 4 function-domains
shipped; the deferral of the 3-discipline framing was never stated). Pairs with the
landing-as-explicit-phase note above: the domain structure and the landing are the
two hub-shape items that must be explicit plan phases at 1.4, not emergent.

**A COMPLETENESS sweep is driven by an AUDIT MATRIX, produced at the
START — never a hand-written list.** When a session's goal is "bring
every X to standard Y" (every entity gets taxonomy+sparks+comments,
every page gets the premium components, every route gets a test), the
scope MUST come from a grep-built matrix of *which X already has which
Y*, generated as the sweep's opening step — not from a list composed
from memory. A hand-list guarantees **planned misses**: you only build
what you thought to write down, and the gaps surface at the retro
instead of the plan (lived session 2026-07-10: a
one-line grep matrix at the retro found three gaps the hand-list missed).
And the completeness sweep is its **own structured pass** (a
`/feature-plan`-style AVOR, `policy-shoulder-glance` similar-problem
sweep + T-035's premium-modal process), **not mixed into a manual
leaf-to-leaf walk** — so focus stays on the substantive changes and the
mechanical completeness is covered by the matrix, not by remembering.

**A TERMINAL-RULING gate is driven by a CLAIMS-VS-CODE AUDIT, produced BEFORE
the gate — the audit-matrix rule's story-status face.** When a session must
decide the end state of stories in limbo (`partially-implemented` at an Era
boundary: `tested` or explicitly deferred), the rulings are only as good as the
evidence of what is built — and a story's own ticks are claims, not evidence.
Dispatch an advisory spawn per cluster before the gate: per story, every AC
marked `[built]` / `[partial]` / `[missing]` with a `path:line` citation, the
built surface, the remainder, a size (S / M / L) and a verdict
(`begun-and-close` · `begun-but-far` · `not-begun`), plus a *seed / CLAUDE.md
claims not backed by code* list; the parent spot-checks the load-bearing claims
against the tree, then rules with citations (lived
session 2026-08-29: US-MOB-002's four ticked ACs described a
drawer retired two hubs ago). **And name every spawn at 1.4** — a spawn the plan
does not name is one the 1.4 allowlist diff never saw.

**And the audit matrix itself must be MULTI-LINE-aware and CLASSIFY BY
BINDING TYPE — a flat line-grep both undercounts and mislabels.** When the
"X" is a *code construct* (a colour literal, a string, an attribute), the
matrix's own grep is a source of error: (a) a **line-based** scan misses a
construct that wraps across lines — an inline `style="…"` attribute whose
value spans several lines is real scope a single-line `grep` never sees; and
(b) the same literal means different things in different **bindings** — a hex
in a plain `style=` is static (convert), in `{% if %}…{% endif %}` is a
conditional literal (convert per-branch), in `{% set x='#h' %}`/`{{ type_color }}`/
`:style` is a seed (skip, derive from the seed), in `var(--t,#h)` is a fallback (exempt). A
matrix that counts raw hits without classifying by binding **mis-sizes the scope
three ways at once**. Rule: build the sweep's audit multi-line-aware (`rg -U`)
and bucket every hit by binding *before* trusting the number (lived
session 2026-07-17: under-counted until a spawn caught the
wrapped attributes; a tag-stripping re-audit phantom-inflated it).

**A scanner you wrote is a CLAIM — validate it in BOTH directions before trusting its count, and check the RULE a guard encodes, not only that it passes.** Run it against a hand-read known positive and a known negative (strip comments and docstrings first); spot-check its truncation boundary.

After applying, **re-run it and require zero** — a sweep that cannot prove itself empty is not finished. When the question is BEHAVIOUR, check the effect — hover it, render it — not the declaration. A guard stricter than the standard it stands for becomes a defect generator.

**And a guard NARROWER than its class passes the sibling it exists to stop, so a guard written with a fix gets a known positive for every SPELLING of the class before it is trusted.** The measuring traps are the runbook's D-entries. (precedent)

**And the matrix's EXTRACTION SURFACE must grep the CONSUMER side, not one markup
shape.** An inventory that names the shapes a conversion retires (a column
list · the filter-shell macro call · the presets mount div) sizes the *producers*; the
ids those shapes render are READ elsewhere — a FilterPresets `<script>` mount,
a JS `elementMap`, a hub-host loader — and a migration that renames an id breaks
every reader the inventory never listed. The blind spot is exactly where a spawn
cannot be briefed: the parent writes "mirror the reference" for a shape it has
seen and nothing for the mount it has not. So beside the producer greps run the
consumer greps (`grep -rn "elementMap" templates/ static/js/`, every
`getElementById('<old-id>')`) and put each hit in the briefing — or in the
parent's own seam (lived session 2026-08-28: the user
leaves' FilterPresets mounts still mapped `evl-from-iso`; the spawn flagged it).

**A mechanical sweep's verification must RENDER, not just parse — the full
suite is the real gate.** A template that *parses* can still 500 at *render*:
`{% extends base.html %}` accidentally left inside an HTML/CSS comment parses
as a valid tag but throws `UndefinedError` when rendered (Jinja reads `{% %}` /
`{{ }}` even inside `<!-- -->` and `/* */`). A parse-only check (`env.parse` /
`get_template`) passes it; only rendering — i.e. the test suite — catches it.
So: (a) **spawn briefings that ask for documentation comments must forbid Jinja
syntax in those comments** (`{% %}`, `{{ }}` — write "extends base.html", never
`{% extends base.html %}`); and (b) **run the full suite before the PR on any
sweep that touched many templates** — a parse pass is necessary but not
sufficient (lived session 2026-07-17: a carve-out comment's
`{% extends base.html %}` parsed clean and 500'd at render).

**Scope is decided at 1.4, not carried as a maybe — and a phase point is SPECIFIED before it is planned as a build.** Ask + decide build-now vs defer in one line here.

**A rulings phase is drawn from the planned Issues' BODIES, read whole for "a ruling" — a title does not carry it.** And when an audit matrix exists for a planned fix, the SHAPE of its mechanism is an item on that gate, never a question at the fix's open.

**Each direction -- and each fix SHAPE -- the plan RECOMMENDS is probed before the gate** against the code it names, the tests pinning the route's present behaviour and the UI posting the field. An Issue's either / or candidate is a design claim, not a finding.

**A ruling recommended on a ROUTE is read against the story whose `related_routes` names it** — a reader briefing asks for that story beside the code.

**An unruled gate proposal (a redirect skipped it) is a carried maybe too** — a plan line or a baton pointer, never only a Log sentence.

A point nobody can describe routes to `/new-story` / `/feature-plan` to *become* specified, never into a build phase. A phase that overflows a session **splits across sessions** as a first-class option, with no Issue of its own.

A *"fade-out / finishing-touch"* framing gets a scope probe first: when page-by-page verification keeps surfacing the same class, STOP and re-scope it as its own planned Issue with its own audit matrix. CSS/theme work earns an audit-matrix-first sizing every time.

Three Issue-scoping corollaries: **an Issue holds ONE topic** — a topic outside the session's Issue gets its own; and **a hub Goal's specified topics become sub-goal Issues** linked from the milestone Issue, never absorbed into it.

And **an Era or half-time CLOSE-OUT is its own separately-planned Issue**, created and fired after the referenced Issues resolve, never a tail on the active topic. (precedent)

**Spawn fan-out is a session-PLAN decision, not a mid-session reach (the context-management rule).** When the plan has **several separable work units** (N modals, N pages, parallel research), decide AT 1.4 which units go to **write-tier spawns** (`--spawn` / MODE 4) — and say so in the plan.

Two planning-time reasons: (a) the units are independent + read/build-heavy (`policy-spawns` Rule 1, *When to spawn*), and (b) **keeping the session's own context tight is itself a valid reason to spawn**. State the disjoint path allowlists at plan time (`policy-spawns` Rule 3, *Parallel reads OK; parallel writes never*).

**And the PLAN's own claim of disjointness is a premise to verify, not a fact to inherit** — a loaded plan's "naturally disjoint" allowlists are a claim about the file layout; check it before the briefings are written.

**A file every member needs belongs to the parent, not to a queue** — the parent takes the shared file inline and writes it itself, leaving each spawn only its own templates, routes and pins.

**A fan-out the plan did not name is proposed at the phase gate BEFORE the dispatch, with its size and its allowlists; stating it after the agents run is a plan change the user never saw.** A whole-page `/wiki` read of several pages, a reader per page, is a fan-out like any other: 1.4 draws its readers, or the gate proposes them (lived session 2026-11-03). (precedent)

**Diff each spawn's
allowlist against the OTHER SPAWNS *and* against the files the parent walks
INLINE.** A spawn whose allowlist collides with a file the parent is holding
cannot be dispatched at all — and discovering that at dispatch time means the
phase silently doesn't happen (lived session 2026-07-10: F2 needed
`episodes.py`, held inline by Phase E, so F2 never ran). The fix costs three lines
at planning — list every inline phase's files beside the spawn allowlists and
diff them. **But pair every spawn-built premium/UI unit with a doctor pass IN THE
PLAN** — a spawn briefing inherently lacks the specifics `/check-ui-entity` /
`/check-page --finish` carry (lived session 2026-06-28:
spawn-built modals missed the sticky twin + vanilla dropdowns, ~5 verify rounds).
**And the same rule for a BLIND-built premium unit — a blind run is the whole
session running as one spawn, so every new premium surface it builds is paired
with its doctor pass in the plan, exactly as a spawn-built one is** (lived
session 2026-08-25: the Matrix leaf shipped with no
doctor pass; pagination + jump row were return-round 1). The plan that names
`/implement-story` for a new leaf names `/check-page --finish` (or
`/check-ui-entity`) beside it, or says why not.

This plan-confirmation is a **4-eye gate** per
[policy-four-eyes](../../policies/policy-four-eyes.md) — apply rules 2
and 3 specifically: **propose a recommended plan with a default path**
(not a menu of options without a recommendation), and **keep the
proposal summarized** (phase names + one-line skill+gate per phase, not
full prose for each phase). The user nods or redirects. Do NOT write
the session file (step 1.5) until the user nods; auto-mode advancing
past this gate is the failure mode the policy exists to prevent.

**Fire this gate in PROSE, not `AskUserQuestion`** — see the
[gate-shape rule](#gate-shape--prose-recommendation-with-default-is-the-default-askuserquestion-is-for-clean-separation-only)
below. A planning/discussion gate (the `--start` plan, "proceed or
refine?", goal placement) is a *conversation* — stating the
recommendation in prose and inviting a nod-or-redirect keeps the
reasoning readable and leaves the user room to add free-form feedback.
The `AskUserQuestion` dialog box *hides* the prose reasoning behind the
picker and reduces the user to selecting a preset option — exactly what
ruins the discussion at this gate. Reserve `AskUserQuestion` for the
clean either/or separation cases (Shape A/B/C; fix-now vs defer).

**A factual claim written into the session plan is LOAD-BEARING — probe it before asserting it, or write it as a question.** Before a codebase claim enters the plan, spend the two minutes (the likeliest file, sibling conventions, an Explore probe) — or write *"to verify: does X exist?"*.

Negative claims ("there is no X") deserve double suspicion: they are only as good as the conventions the grep guessed. **A SIZE lifted from an Issue (a count of groups, rows, sites) is the same kind of claim: re-run its census before the gate.**

**A NUMBER a plan writes before the call that mints it — "PR #1", "Issue #3" — is a claim too: the plan names *the Episode's PR*, *the story's Issue*, and the record takes the number `gh` returns.**

**A DESIGN sketch is the same kind of claim**, so it **names the reference surface it mirrors** (MODE 4's briefing rule) or is written *"to find: the precedent for X"*, never nodded as a design.

A ruling that keeps an action OUT of the UI says what the UI does when the user tries it — a silent no-op is a finding. (precedent)

**And when the negative claim is about a named ARTEFACT or PROJECT rather than a PATH, one candidate path is not the probe — grep the repo for the artefact's NAME.** The tell: you are about to write *"X does not exist"* having consulted exactly one location for X.

Ask which you are claiming — *this path is empty* (cheap, and usually all you need) or *this thing does not exist* (a claim about the whole repo, so search the whole repo by name).

**A loaded plan's claims about what a TOOL will produce are load-bearing in the same way — the shape of a seeded world, and the plan's own `verified by` command**: count a plan written from the declaration file against the generator's OUTPUT before a phase depends on it.

And the plan's verdict command is dry-run against its checker at the open, before any work is measured by it.

**A DATA probe is a load-bearing claim too — but you no longer have to remember how to verify it: run the command.** (precedent)

```bash
flask agora env          # resolved DB name + recency + divergence vs last session
```

This is the environment half of step 1.1 (below) and it is **executed, not
recalled**. It resolves the URI from config (never a guess), reports the
database name alongside newest-record timestamps per active collection, and
**exits 3 on a recency divergence** — data moving backwards cannot happen on a
live instance without a deliberate reseed. On a `--accept` you confirm the
reseed and it rewrites the baseline. It refuses to start any container it cannot
resolve from the compose file with high confidence (US-AGORA-032) — both halves
exist because a prose rule did not hold (lived
session 2026-07-21 · session 2026-07-22:
a guessed empty database nearly ruled "reseed"; a stale standalone container was
started and trusted — the tell *"yesterday 1 rule, today 0"* was written down and
ignored).

### 1.4b — Milestone targeting

Name the **Milestone** this session is aiming at (or explicitly: "no
Milestone targeted — exploration only"). One of:

- *"This session closes Goal X's success criterion N — that's the
  Milestone."*
- *"This session advances Goal X but doesn't trigger a Milestone — we'd
  need criteria M+N to also close."*
- *"Exploration only — no Milestone targeted."*

Write the answer into session frontmatter as `milestone_target:`. This
is what `--end` step 2.2 checks to decide between Haleluja-ceremony and
park-clean.

**And name WHERE it fires, read against the Goal's `**CI:**` and `**Repo handling:**`
lines — a Milestone fires only where its ceremony can run.** The ceremony is push →
CI-green → tag. On a Goal whose CI runs on the PR only and whose batch PRs squash-merge,
a branch push carries no green run and a tag on a branch commit is stranded by the
squash. So a batch sub-milestone targeted inside a branch session is written as
*"criteria close this session; the tag fires on the batch PR's green squash"*, never
*"fires at Phase N"*, and the session that closes the criteria records the verdict and
hands the tag to the PR session (lived session 2026-09-14:
a seeded-world milestone declared to fire on Phase 3, unexecutable at the gate,
ruled onto the #492 precedent).

**Then CHECK the Milestone's scoping — an executed step, not three rules to
recall (US-AGORA-039):**

```bash
flask agora milestone --goal "<Goal title substring>"
```

Four decisions, reported per Goal — the fourth, **size**, is US-AGORA-063's: every open batch parented to the Goal against `tier_thresholds` (sessions whose frontmatter cite it · plans whose parent names it; `>=`, so it fires AT the count).

A `[GAP]` is a batch that outgrew its tier, proposed at this gate as `flask agora batches --elevate <batch>` or recorded as `**Tier ruling:** stays a batch until: <date | N sessions>` **in its Issue BODY** (a ruling without `until:` silences nothing since US-AGORA-082).

The size check reads bodies, never comments (`list_open_sub_goals()`), so a ruling posted as a comment leaves the `[GAP]` standing; the escalation is a ruling, never automatic (`AGORA-DECL §7`).

The three original: **batches** (opened up front, or a stated single-batch) · **branch** (one per Milestone — *and the current branch is one the Milestone declares*, so a session branch inside an open Milestone is flagged) · **ci** (what runs on push vs PR).

A **targeted** Goal with a gap **exits 2**; the bare `flask agora milestone` survey of every active Goal exits 0. **Read the `(GitHub: N open sub-goal(s) parented here)` count as the batches fact** — the `[OK]` beside it counts any `#<n>` in the COMPASS `**Batches:**` prose (#285).

Fill a gap by declaring it in the COMPASS Goal entry — and `flask agora batches --goal <n> --batch "…" --batch "…"` opens the batch Issues in one call, each carrying `**Parent Goal:** #<n>`. (precedent)

The gaps are a **4-eye-gate input**, not an auto-refusal of the session: surface
them with the plan (1.4) and decide with the user whether to close them now or
proceed deliberately. What the check removes is the *forgetting*, not the
judgement.

**The milestone game-plan lives in its GH Issue — read it here, update it
at `--end` (US-AGORA-021).** A Milestone v2 (US-AGORA-019) is an
`agora:type:milestone` Issue, and **its game-plan lives in that Issue's
body/comments — the single referenceable source**, never reconstructed from
chat (the lived BP-1 friction: a "finish in the next phase" plan that lived
only in conversation was guessed wrong at the next session). So when this
session targets a Milestone:

- **Read the plan from the Issue first — WITH its comments, not just the body.** `gh issue view <n> --json title,state,body,comments --jq '…'` (the `agora:type:milestone` Issue; the plain `--comments` form dies on the Projects-classic deprecation — runbook A4).

  **The detailed game-plan usually lives in the COMMENTS, not the description** — the body + comments together are the authoritative phase plan; open the session's phases against *that*, not a remembered picture. With no milestone Issue yet, open one here (per US-AGORA-019's rollover) or decide it stays a single-Goal tag.

- **The Issue plan is part of the GitHub truth COMPASS reconciles against**
  (US-AGORA-018) — `flask agora reconcile` treats the milestone Issue's state as
  authoritative, so keep the Issue current, not COMPASS-only.

- **Update the Issue at `--end` — mark each shipped step implemented. This is a RELIABLE standing `--end` discipline, not an ad-hoc step: the Issue COMMENTS are the base of the planning.** Every `--end` documents progress into **every Issue the session worked on** (the milestone Goal Issue AND its sub-goals).

  As phases close, tick the description checklist box for each implemented step (or add a dated "✅ §3 shipped — <session/commits>" comment) so a reader sees which steps are done vs. open — an un-updated Issue makes the next session re-plan work that's already done.

  A parking session updates the *current* milestone Issue's checklist; the `Milestone-reached` Step 11 rollover writes the *next* milestone's plan into its Issue; **a closing session documents the completion before closing per step 2.8b**. Followable progress in the Issue at any time is the goal. (precedent)

### 1.4c — Declare the session's repo plan (US-AGORA-036)

**The commit and push decision is made HERE, at `--start`, and merely *executed*
at `--end`.** `--start` already establishes the goal, the plan and the milestone
target — it has every input the commit plan needs, and none of the fatigue.
`--end` is the point where the conversation has been running longest, context is
most compacted and the user is most tired: the worst moment to make a structural
decision. And it showed — the branch-vs-`main` call was missed twice (both §0
User-Hub sessions committed a whole feature straight to `main`), and the pre-push
hook's stats companion was mishandled three times in one session.

Declare three things as part of the same 4-eye gate as the session plan (1.4) —
**one more line in a proposal the user is already reading, not a new gate**:

| Field | Content |
|---|---|
| **branch** | `main`, or `feat/<slug>` / `fix/<slug>` with the name proposed now. For **non-trivial feature/build work the default is a feature branch**; docs / chore / tiny fixes go direct to `main`. **One branch per Milestone, not per session** — inside an open Milestone this is **read from 1.4b's `flask agora milestone`**, not composed here: the Goal's `**Repo handling:**` already declares it, and the check flags the current branch when it diverges. |
| **expected commit groupings** | The concerns this session is likely to produce, one line each. A forecast, not a contract — `--end` 2.1 surfaces the *differences*. **Each line is written in the subject's own shape — `type(scope): <the story id, or two words the subject will carry>`** — because the close reads it mechanically: `commit_matches_grouping` pairs a commit with a grouping on a shared story id, else on the same `type(scope)` prefix plus two shared content words, so a gloss (*"opener (+ pile-history row)"*, *"catalogue, directly after the feat seam"*) matches nothing and every forecast commit reads `[INFERRED]` (lived twice, session 2026-11-07 · session 2026-11-07: 4 of 6, then 8 of 9). **And when a gate adds or reshapes a phase, the groupings follow in the same edit** — `repo_plan.groupings` gains the phase's seams beside the gate's Log entry, or the close reads a ruled phase as divergence. **A PR session forecasts each CI red as a PAIR -- the fix seam and its `chore(agora)` record -- scoped by the AREA the red names, never by the plan's** (a shellcheck red is `fix(ops)`, a coverage-gate red `test(<area>)`), so one `fix(agora): ci-local reds` line matches neither; **and a PR session that also runs build phases draws a record seam per phase** (lived session 2026-11-01: the Lint-job fix and its record, unforecast · session 2026-11-07: 8 of 11 `[INFERRED]` -- four phase records, `fix(ops)` + `test(agora)` against `fix(agora)`). **A blind run whose plan expects an attended walk forecasts the walk's seams as conditional groupings** — `fix(<area>)` per ruling the handoff will ask for, and a second record seam — or the session's declared three read as five short at the close (lived session 2026-09-26: three declared, eight landed, five of them the walk's). **A blind run whose scope is CHECKS forecasts a conditional fix grouping per check that can red, each in the area its red would name** — one `fix(<area>): one per ci-local red` line matches neither a picker fix the journey tier found nor a harness fix its runner needed (lived session 2026-11-08: `fix(js)` + `fix(test)` from step 10, both `[INFERRED]`). **An ATTENDED session whose plan ends in a walk -- or holds a READ phase (a `/wiki` read, a reader fan-out), or reads a mechanism's FIRST LIVE OUTPUT (a bot PR, a first scheduled run), or ONBOARDS A MACHINE (a fresh clone's first run of the substrate) -- forecasts them the same way** -- a walk exists to find what the tests did not, a reader finds code defects beside the page drift, and a first live run meets the conditions no fixture reproduced (an onboarding is one: the new machine's checkout, interpreter and services are the conditions), so its fix seams, their catalogue seam and a second record seam are expected, not surprises (lived session 2026-10-05: seven declared, twenty landed, nine of them the walk's · session 2026-10-30: five declared, eleven landed, two `fix(...)` seams from the read · session 2026-11-08: the light mode's first bot PR, two unforecast `fix(agora)` seams · session 2026-11-09: the gaming PC's onboarding, a `fix(checks)` and a record seam unforecast). **Homing third-party input forecasts no tracked commit** -- it lands untracked at `data/input/` (#487 ruling 3); only the pointers that named its old path are a seam (the same session forecast a `docs(...)` per home group; one `docs(canon)` landed). **Forecast the CATALOGUE commit whenever ANY planned phase can add or change a user-visible string — a story's ACs predict it, and so does a doctor's mechanical half, a mechanism build or a fix that touches a template or a route's `_()`** — the translation catalogues are 24 files (12 `.po` + 12 `.mo`) that no feature diff mentions, so they are invisible to a forecast built by reading the *code* the session will touch; keying the trigger on *stories* misses the phases that mint a string without one (lived session 2026-09-26: a wiki doctor's fourth freshness state carried a page-view sentence and a label, the en-completeness guard reded seam 3, and `chore(i18n)` was the fourth grouping of a three-grouping forecast). **And draw that seam DIRECTLY AFTER the fix that mints the string, never last** — `en catalogue complete` reds every later seam's preflight until it lands, a standing known red of the kind the failing-SET rule warns hides a second one (lived session 2026-10-08: one msgid in the first fix, the catalogues eight seams later). **Several minting fixes may share ONE seam when 1.4 orders them back to back and the seam follows the last of them** -- a seam per fix costs a twelve-catalogue authoring round each; the guard is then a known red for exactly those commits and no preflight is read between them (lived session 2026-10-12: three fixes, one seam `ce99d58a`). Same shape for the other derived artifacts a build drags along: `docs/stats.yaml`, a wiki seed, the page registry -- **and a fan-out's own spawn files, counted records (#390) that `state-check` reds at every later seam until they ride a `chore(agora)` record seam with the stats companion, so 1.4c draws that seam BEFORE the first build seam the spawns feed** (lived session 2026-10-29: `7554f3c6`, unforecast, after the first cluster seam's preflight). **And forecast a `docs(wiki)` seam when the plan's SCOPE is something a wiki page names as missing, or a behaviour a page DESCRIBES** — tests for *"the founding resources have none"*, a route a page calls unbuilt: closing the gap makes the page false, and its correction is a seam of its own with the reseed → rehash → stamp behind it (lived session 2026-10-01: `0eae42e4`, unforecast; `grep -rn "<the scope's files, functions or feature>" docs/wiki/` at 1.4c finds the page -- never a grep by the Issue number: a page describes the behaviour a fix changes without naming its defect (lived session 2026-10-25: `feature-reschedule`'s slot step, found only at the edit)). **A `docs(wiki)` seam is a seed FILE edit; a REHASH is not one** -- `flask wiki rehash` writes the DB and no tracked file, so seeds the opener finds stale on a changed SOURCE forecast no grouping unless their TEXT will change, and the `docs(wiki)` grouping to draw is the one whose seed ENUMERATES the set the build extends (lived session 2026-11-02: three rehashed seeds declared as a `docs(wiki)` grouping that never stood; the one `docs(wiki)` seam that landed -- the hooks list, 088's third member -- was unforecast). The tell is that the file is *generated or swept* rather than *edited* — you will not think of it by imagining the diff (lived session 2026-08-08: three groupings declared, four landed — the fourth was the i18n catalogue). **A blind run that ends on a record commit forecasts EVERY group's tests before that commit and the baseline as its own seam** — `flask stats dump` counts the test files in the working tree, so a record over untracked tests cannot be fresh (lived session 2026-10-02: the last group declared *with the baseline, after the run*, unexecutable as drawn). |
| **push disposition** | `at close` · `at the Milestone only` · `none — local park`. Inside an open Milestone the Goal's `**CI:**` declaration (also read at 1.4b) says what runs on push vs PR — CI is a budgeted resource, and the disposition is a decision with an owner rather than something discovered when the quota runs out. **When that line says the suite runs on the PR only, the session that will open the batch's PR draws the full local suite as its OWN PHASE before the push** (EVENTS `Milestone-reached` Step 3) -- **and that phase runs CI's Test JOB, not the suite: the workflow's own command line with `--cov`, then `check_coverage.py --check`, under CI's machine conditions (`TZ=UTC`, the migrated index set, CI's server version) -- a local green on the suite alone is not CI's green** -- **that phase is ONE command, `flask agora ci-local`** (US-AGORA-091: the workflow's own pytest line under the job's env, `-x` stripped, the `suite` field bound to HEAD; `--job lint` for the Lint job) (lived [[2026-10-14-trigos-epF-part3]]: two local 22 237 / 0 runs, then five CI runs -- three machine-difference reds and the coverage gate; #888) **-- and the LINT job's scripts under ITS install set, Flask absent (`ruff pyyaml polib babel jinja2`; `sys.modules['flask'] = None` is the local stand-in): a check that imports `app` bare passes every local run and reds the PR in two minutes before the Test job starts** (lived session 2026-11-01: PR #965's first read; the import contract is pinned by `tests/unit/test_lint_job_flask_free.py`, the Lint half of `ci-local` captured on #477): "push at close" on such a session declares the push and silently drops its gate, because a multi-session branch otherwise meets the suite for the first time at its PR (lived session 2026-09-15: #495 pushed on the Selenium set and targeted runs; CI's Test was the suite's first run over four stories and three fixes). |

Write it into the session file's frontmatter as `repo_plan:` (1.5).

**When this session DRAFTS the repo handling for a batch or a Goal rather than
executing its own, the parent Goal's `**CI:**` line is a CONSTRAINT, not a
default to amend.** The table above reads as the session's own three fields, so a
declaration written *for someone else's future sessions* — a batch Issue's "Repo
handling · CI" block, a Goal's opener — slips the budget question entirely: it is
drafted from what suits the work (independent members, small fixes, merge each as
it lands) while the Goal already declared PR-only CI **because** the allowance is
finite. Read the parent's CI line first and cost the proposal in CI runs; a shape
that multiplies them needs the user's ruling, not the drafter's preference (lived
session 2026-09-17: C11 drafted as a branch per member — six PR
runs where one suffices — overruled by the user on quota, with the accepted cost
of the single branch then written into the Issue instead).

**Auto-push fires only when all three hold:** the plan declared it at `--start`,
the close-gate preflight is green, and the tree matches the declared groupings.
**Any divergence falls back to the explicit confirm-then-push path.** Firing a
Milestone tag is never auto — 2.2 keeps its own gate.

This is an explicit amendment to
[`policy-commit-discipline`](../../policies/policy-commit-discipline.md) Rule 4,
landed with the rule itself: the 4-eye gate **moves from `--end` to `--start`**.
It is *earlier*, not *absent*. A story that silently contradicts a live policy
rule is a breach, not a feature.

### 1.5 — Open or extend the session protocol file

**New session** — open the file with **`flask agora open --slug <slug> --type <t> --mode <m> [--plan P-NNN] --intent … --goal … --milestone-target … --branch … --grouping … --push … --agent …`** (US-AGORA-106, a call site, never `cp` plus a hand splice).

It copies [`_TEMPLATE.md`](../../sessions/_TEMPLATE.md), writes the frontmatter from the fields (the Era defaults to the newest session's; `--era` overrides), drops the Handoff section unless `blind`, parses the block back and renders the INDEX line; it refuses a second open session, an existing file and a `blind` run without `--plan`.

The template carries no inline frontmatter comment (T058 T088), so a file it writes is found open by every `write evidence`.

Write the **Intent** and the **session plan** (from 1.4), leave **Log**, **Open threads**, **Agora findings**, **Close-out** empty. Fill **`era:`** with the current Era's slug (COMPASS `## Eras`, the `agora:era:<slug>` label — `flask agora write era <slug>`), leave **`outcome:`** empty.

Then **`flask agora regen`** — the opener seam's companions in DAG order (US-AGORA-096); `open` already rendered the INDEX line (`flask agora write index`, US-AGORA-067).

[`INDEX.md`](../../sessions/INDEX.md) is generated from the frontmatters — the open line reads `<intent> — in progress` — and is never hand-spliced; the Era of the newest session is INDEX.md, every other Era its own `INDEX-<era>.md`. (precedent)

**`mode:` is orthogonal to `type:` (US-AGORA-037).** The five base types are
untouched; `mode` names *how the session relates to a plan*:

| `mode:` | The session | `plan_ref:` |
|---|---|---|
| `normal` (default) | plans and builds in the same window, as always | empty |
| `planning` | **produces** a plan, builds nothing | the `P-NNN`(s) it emits |
| `blind` | **executes** a plan, composes nothing | the `P-NNN` it loaded — **required** |

A `mode: blind` session with an empty `plan_ref:` is the failure the loader exists to prevent — a blind run that composed
its own scope. The field is the **only** place a plan's status lives (`flask agora plan` derives `ready`/`loaded`/`done` from
it, excluding only `mode: planning`): unfilled, a finished plan looks loadable forever; **filled on a `mode: normal` session
that merely DRAFTED the plan, it reads *loaded*, then *done*, for a run that never ran** — an emission lives in the Log + baton
and the field stays BARE (the reader takes the rest of the line: `""  # P-042 emitted` is a non-empty ref; lived session 2026-09-11).

**Continuation** — append to the existing file: add the new goal under
**Intent** (dated), extend the **session plan** with the new phase, and if the
file was `closed`, flip it back to `open` and re-render its `INDEX.md` line
(`flask agora write index`).

**During the session** (not a numbered step — a standing instruction): as each
queued skill completes, tick its checkbox and append a dense **Log** entry —
what was done, key decisions, surprises, docs/stories/code touched. Anything
that smells like skill-system drift goes in **Agora findings**. Keep it a
structured summary, not a transcript. See
[`.claude/sessions/README.md`](../../sessions/README.md).

**Log-entry-before-checkbox-flip is a hard order, not a suggestion — and it
binds in BOTH directions.** Write the Log entry FIRST, then flip the `[ ]` →
`[x]`. **Neither half is optional, and the flip is part of FIRING the gate, not
bookkeeping to do later.** The rule reads as a guard against flipping-without-
logging, and that is only one of its two failure modes; the inverse —
logging-without-flipping — is the one that survives a whole session, because
nothing downstream complains until the close. The phase gate is fired in
**prose**, so no tool call forces the flip: the only thing that makes it happen
is treating it as part of the gate (lived session 2026-08-05: four
phases logged, none flipped; `retro-context` opened the close at 0/4). The
exposure is that a session ending *without* `--end` leaves a durable file
claiming no work was done. Cheap check when firing the gate: the checkbox you
are about to describe as complete is the one you flip in the same edit.

**A record edit that anchors on a HEADING puts the heading back — a
`replace(anchor, entry)` that does not end with the anchor deletes it.** The
Log is written by freehand string replacement (no writer exists for it —
the opener-as-writer mechanism on #477 covers the frontmatter, not the Log),
and the natural anchor for "append an entry" is the NEXT section's heading:
`t.replace('\n## Open threads', entry + '\n## Open threads')`. Drop the
second half and the entry lands, the heading vanishes, and nothing objects
until the next edit's assertion looks for it — or never, if no later edit
does (lived session 2026-09-27: the Phase 1/2 write ate
`## Open threads`; the Phase 3 script's assertion found it one step later).
Rule: anchor on the heading LINE, re-emit it verbatim, and after every record
edit assert BOTH that the section list survived (`re.findall(r'^## ', t, re.M)`
against the template's eight) AND that the replacement LANDED — the anchor
present before the edit, the new text present after (`assert t.count(old) == 1`
… `assert new in t`). The section list alone passes a splice that matched
nothing: a `re.sub(…, count=1)` over the template's plan comment (which opens
`<The skill …>`, not an HTML comment marker) wrote nothing, the opener committed the template's
placeholder plan, and the eight headings were all still there (lived
session 2026-11-02; caught at the first flip). This is
the parse-back for the body that the frontmatter already gets; the
opener-as-writer mechanism on #477 retires the splice itself.

The phase-completion 4-eye
gate (below) is gated on the checkbox flip — if the Log entry hasn't landed,
the gate proposes a phase transition the session file doesn't yet reflect.
The drift this catches: checkboxes ticked as work finishes, Log entries
deferred to "later" — `--end` 2.3 then reconstructs the compacted summary from
conversation context that may already be partly compacted, and the file becomes
a misleading record (lived session 2026-05-29: ~10 work units
done, two logged, caught by a mid-session `/inspect-pipeline --session`).

**The frontmatter written at 1.5 is a FORECAST — when a planned phase does not
run, correct it at the close, or the record claims work that never happened.**
`intent:` and `milestone_target:` are composed when the plan is fresh and every
phase is still going to happen. A phase then gets deferred — legitimately, at
the user's call — and those two fields keep asserting the original scope. The
session file is the durable record, so what stays there becomes what happened:
the next `--start` reads it, `flask agora baton` verifies its pointers against
Issues and stories but *not* its prose, and nothing else ever re-reads the
plan's checkboxes against the intent. Worse, the wrong claim propagates
outward before the close — into what you tell the user at the phase gate, which
is where they decide what remains.

The check is mechanical — **for every unticked plan checkbox, confirm the story it
names is absent from `intent:` and from `milestone_target:`'s claimed closures** —
and it belongs at 2.0, before `retro-context`'s output is used to write anything
(lived session 2026-08-03: Phase D deferred, the intent still "lands
US-WIK-026", the Phase-C summary off by one story).

**And the Log is not written until it is on the DEFAULT BRANCH — a session
file committed to a feature branch after that branch's PR merged is a record
that can never arrive.** The rule above governs *when* the entry is written;
this governs *where it lands*, and the two come apart precisely at a
Milestone. A squash-merge collapses the branch at the commit the PR pointed
at; anything committed to the branch afterwards — and the close's own
housekeeping is exactly that — stays behind on a branch nobody will merge.
Nothing warns you: `git status` is clean, the file on disk is complete, and
the Log reads correctly in your own working tree (lived
session 2026-08-02: the Phase A–F Log landed after PR #292 merged;
`retro-context` on `main` saw 1/7 phases). This is Claim 5 failing in the one
way that is invisible from inside the session. The check is one command before
the close-out commit: `git log <default-branch>..HEAD -- <session-file>` **and**
the same against every other branch — anything it prints is record that has
not landed. On a Milestone close, write the Log to the branch *before* the PR
merges, or write it directly to the default branch afterwards; never to the
merged branch.

**Between phases** (also not a numbered step — a standing instruction
paired with the one above): when a session-plan checkbox is about to
flip from `[ ]` to `[x]`, fire the **phase-completion gate** *before*
flipping. Per [policy-four-eyes](../../policies/policy-four-eyes.md)
Rule 1 (phase-completion is the 5th named transition gate, added by
US-AGORA-003).
Shape — proposal-form per Rule 2, summarized per Rule 3:

> *"Phase X complete (<one-line deliverable>). Proceed to Phase Y, or more under X?"*

**A phase that names N deliverables is checked against N, not summarized to
one.** The `<one-line deliverable>` above governs what is *presented* — Rule 3,
summarized — and it is easy to read as governing what is *verified*. It does
not. A plan line that carries a second clause (*"…and reconciles X"*, *"…plus
the registry sweep"*) has made two promises, and the gate's own one-line shape
is what quietly drops the second: you summarize to the headline, the headline is
true, and the checkbox flips over an undone deliverable. Nothing downstream
objects, because a ticked box is indistinguishable from a complete one.

So before flipping, re-read the plan line you are about to tick and confirm
**each** thing it names actually happened. The tell is mechanical — an "and", a
comma-list, or a second sentence in the checkbox text (lived
session 2026-08-06: Phase C's "…Reconciles
`hub-header-template.md`" clause flipped untouched; caught incidentally).

**A phase that changes a GATE CONDITION sweeps what else was scoped to the old value
before its box flips** — a moved breakpoint, tier, scope or flag leaves every rule
written against the old value wrong, none of it in the phase's diff, so no symbol grep
and no test reaches it and the later phase that trips reads as a fresh defect. The
tell: you edited a number that appears in more than one file — `grep -rn "<old value>"
app/` before flipping (the 861 → 601 gate left eight hubs' chip rules and `layout.js`'s
`matchMedia` on 861, session 2026-08-07).

Four recognized user responses:

- **`proceed`** (default) — ONE call, after the nod, flips the Phase X box AND records
  the nod as its field: `flask agora write evidence --kind phase-gate --value "Phase X
  fired <log-heading>" --nod "<the user's words>"` (US-AGORA-097 — the writer IS the
  flipper: it refuses a box already ticked, an absent phase or a missing nod, so a
  gate that was not asked cannot be recorded as fired, and a hand flip without its
  field is what `retro-context` names at the close: `boundaries N > gates M`).
  **The flip and the field are ONE act** because a prose gate has no tool call to
  force the write — the one command is that call (lived
  session 2026-09-07: ~4 fired, 0 recorded ·
  session 2026-10-08: Phase 1's field before its nod ·
  session 2026-10-05: both boxes flipped before the Go).
- **`more under X: <what>`** — Phase X scope extends, checkbox stays
  unchecked, the addition lands inline (this is the bidirectional half
  per Rule 5 — small tweaks discovered at the gate are expected, not
  cost).
- **`redirect to Z`** — jumps to a different unchecked phase; Phase X
  checkbox may or may not flip per user intent (ask if ambiguous).
- **`stop`** — parks the session; no flip; `/agora --end` is the next
  step the user will run.

**Two edges where the gate does NOT fire** (per Rule 1, transition
gates are deliberately narrow):

- **Before the first phase** — the session-open 4-eye gate at step 1.4
  already covers it (Rule 1.a).
- **After the last phase** — `/agora --end` itself is the next gate
  (Rule 1.d).

The phase gate fires *strictly between* phases — never before the first,
never after the last. **Smoke-test pass ≠ user nod** per Rule 4: ruff
clean + tests passing are *prerequisites* to firing the gate, never
substitutes for the user's textual nod.

---

## MODE 2 — `--end`

Closes the session by **producing one thing — the close-out paper — presented at
one gate**. It commits and (on a Milestone) **pushes** the work and **waits for CI
to go green**, compacts the record, audits the session for skill-system drift, and
dispatches the lessons. A milestone session is not closed until it is pushed and
green — `--end` ends *red* only by being abandoned, never by being completed.

### The shape of `--end` (US-AGORA-034 / the US-AGORA-033 probe)

**`--end` is expensive because of GATE COUNT, not step count.** `--start` runs
comparable machinery — context load, reconcile, backlog read, environment
verification, goal placement, plan construction — through **one** nod-able gate,
and is not experienced as expensive. `--end` used to serialize four to five.

So the steps did **not** get deleted; the **gates** got consolidated. Across the
eleven steps there was exactly **one** genuine deletion (2.7 coaching). Nine of
eleven survive — as **sections of the paper** rather than as gates of their own.

```
2.0   Classify the session shape        [AUTOMATIC · flask agora retro-context]
2.1   Commit-tree triage                [PREPARED — proposed in the paper]
2.3   Compact · threads · skills        [AUTOMATIC]
2.4   /inspect-pipeline --session       [AUTOMATIC — interrupts only on 🟡/🔴]
2.3b  XP grading                        [paper section]
2.5   Dispatch + dispositions           [paper section]
2.6   Retrospective — DRAFTED           [paper section]
2.8b  Issue UPDATE (always) / CLOSE     [update executes · close proposed]
              │
              ▼
      ╔═══════════════════════╗
      ║  THE CLOSE-OUT PAPER  ║   ← 2.10 · the deliverable
      ╚═══════════════════════╝
              │
              ▼
        ◆ THE ONE GATE ◆        ← nod · correct inline · redirect
              │
              ▼
2.10  EXECUTE  ·  2.8 bookkeeping [AUTOMATIC]  ·  2.9 rollover

2.2 / 2.2.5  Milestone check + Goal retro  ← THE ONE SEPARATE GATE (Path A only)
2.7          [RETIRED — the single genuine elimination]
```

**Measured by gates fired per close, not steps removed.** A change that removes a
step but keeps a gate has failed. Target: **1** gate (2 on a milestone close).

**Why 2.2 keeps its own gate:** firing a tag is the only irreversible act in
`--end`. Everything reversible collapses behind the paper.

**The step numbers are IDENTIFIERS, not a sequence.** The corpus is keyed on them —
the journal-at-source header cites `--end 2.3b` in twelve `SKILL.md` files,
`policy-issue-templates` cites 2.8b, `/inspect-pipeline` cites 2.4/2.5 in its own
`## Claims at this level`. They are preserved deliberately. **2.7's number is
retired, never reused.**

Apply [policy-shoulder-glance](../../policies/policy-shoulder-glance.md) — `--end`
**is** the session-boundary *Schulterblick*: steps 2.3 (compact + reconcile
threads) + 2.5 (dispatch) are the **catch** half (surface anything left behind),
2.3 (compacted summary) + 2.6 (retro) are the **close** half (summarize what was
engaged + used). Recognize this existing sweep as the glance; do not add a new
gate. The Era-boundary glance is the EVENTS.md `New Era` Movement 1; the round
glance is `/plaza` close-out.

**The catch half includes the SIMILAR-PROBLEM sweep.** For every *specific*
problem the session fixed, the glance asks two questions before close-out:
**(a) does this problem class have unhandled siblings?** (same shape, other
entities/surfaces — the T-023 pattern, where one employee fix generalized to 12
modals) and **(b) is the fix at the RIGHT surface, or did we patch where the
user pointed rather than where the use case lives?** Fixing exactly what was
asked and stopping is the failure mode (lived
session 2026-07-05: the role-gap fixed on user settings;
its siblings and its real home, the user wizard, surfaced by the user). The
sweep's output is cheap: a named sibling list + a surface-question, each
becoming a thread/Issue at 2.3 — not more work in this session.

### 2.0 — Classify the session shape *(AUTOMATIC)*

An **executed step, not a judgement to remember**. Run:

```bash
flask agora retro-context .claude/sessions/<this-session>.md
```

This is `GetRetroContext()` — the retrieval that grounds the paper. It reports
the session's **evidence** — **read FIRST from the `## Evidence` block the seams
wrote** (commits · suite · skills · gates · the fired milestone; US-AGORA-062,
`AGORA-DECL §5`) and, only where the block lacks a kind, parsed from `git log` /
the Log and printed **`[PROXY]`** — plus phases ticked, threads touched, ungraded
stubs, Issues worked, and the **touched-and-unresolved list**, and it classifies
the **shape** from the tags actually fired, never from `milestone_target` alone:

| Shape | The paper carries | Gates |
|---|---|---|
| **simple / one-go** | commits · Issue comment · close-out. **No retro, no dispatch section.** | 1 |
| **substantive** | the full paper | 1 |
| **milestone** | full paper + the Goal retro | 2 (paper + 2.2) |

The shape is **computed and stated with its reason, never asked** — asking which
shape it is would reintroduce a gate, which is the thing being removed. Ambiguity
resolves to `substantive` (closing a substantive session light loses a retro;
closing a simple one heavy costs a skipped section). A wrong call costs the user
one word at the single gate.

The user's formulation this implements: *"this was a simple one-go session so a
retro and coaching is not needed, and the issue part comes down to a simple
comment."*

**Read the command's output rather than reconstructing it from the conversation.**
At `--end` the conversation has been running longest and may already be partly
compacted — which is exactly when writing the retro from memory degrades without
saying so.

**A `[REFUSED]` exit is consumed, not worked around (US-AGORA-047).** The
command verifies its own numbers: when it computes 0 commits while the
session's own Log names commit shas (or a ticked checkbox names a commit
seam), it exits non-zero with the contradiction printed and **makes no shape
call** — the close stops until the contradiction resolves (usually: commit
the session file, or correct the record). It also prints the **source** of
its commit count (`session-file-anchor` / `branch-span` / `frontmatter-claim`
/ `none` — the 0-commits class #232/#287, fixed at the root) and a
**warnings block** (declared-but-unsupported `skills_invoked` entries ·
intent claiming an unticked story · a ticked checkbox naming an untouched
path · shas stranded off the default branch) — each warning is a flag to
resolve in the paper, never silently dropped. The #331 sweep (a session
flipped `closed` with an empty Close-out body) runs in `flask agora
reconcile`, forward-only from 2026-08-14.

### 2.1 — Commit-tree triage *(PREPARED — proposed in the paper, not its own gate)*

**An open PR on the session's branch is read by its HEAD SHA** (EVENTS `PR-merged`, US-AGORA-093):
the paper states its head's conclusion and whether a green read covers it; a merge the session
made is recorded by `flask agora write milestone-record --pr <n>` before the close commit.

Run **the commit-tree triage** (above) on what this session produced — the
grouping work is unchanged and essential. What changed is that its **proposal
becomes a section of the close-out paper** rather than a gate of its own. The
tree closes the session clean — policy Rule 5.

**Execute the plan declared at `--start`; do not compose one (US-AGORA-036).**
`--start` step 1.4c wrote the session's `repo_plan:` — branch, expected commit
groupings, push disposition — when context was richest. So this step **compares
actual against declared and surfaces the DIFFERENCES**:

- **Tree matches the declared groupings** → the paper states the plan as executed,
  one line per commit. No re-derivation.
- **Tree diverges** (an unplanned concern, a group that split, work on a different
  branch than declared) → the paper names the divergence explicitly, and the
  divergent part falls back to the explicit confirm-then-commit path.

**Full commit bodies are written AFTER the nod, never before** — a paper carrying
full bodies turns the nod into a rubber-stamp of text the user may not have read
(`policy-four-eyes` Rule 3). The paper carries grouped files + one-line subjects.

The index-verification discipline, the behaviour-changing-test rule, the
`-F <file>` first-line check and the pre-push companion-file contract all still
apply verbatim — they are properties of *committing*, not of the gate.

### 2.2 — Milestone check → ceremony or park

Read the session's `milestone_target:` (set in 1.4b) and check whether
the targeted Milestone's success criteria are met.

**Discipline — read every criterion line-by-line.** Open COMPASS.md
and find the Goal the session advances. Walk every `- [ ]` checkbox
in its `Success criteria:` list. For each, decide concretely: is it
closed now? Cite the commit / artifact that closed it. **Do not
collapse the check into "the work feels done"** — that misses
criteria that were tacked onto the Goal early (e.g. "rolled out to
≥1 sibling page") and forgotten. If any criterion remains open, the
Milestone ceremony does NOT fire today; a sub-milestone may
(`milestone-<sub-slug>` annotated tag, recording the partial close
in COMPASS.md without retiring the Goal).

This is a **4-eye gate** per
[policy-four-eyes](../../policies/policy-four-eyes.md) — Milestone
firing is a transition gate (rule 1). Apply the full discipline:
**propose** the closure decision per criterion with a recommended
verdict (rule 2), **summarize** the proof (criterion + closing commit
sha + one-line evidence, not the full diff — rule 3), and wait for
explicit user confirmation before tagging + pushing (rule 4). The
ceremony is irreversible-ish (push + annotated tag); a wrong call here
is expensive to walk back.

The sub-milestone path is the right move whenever:
- 2+ criteria are closed, AND
- the remaining criteria genuinely belong to a separate session
  (not "the last 5% of this work"), AND
- the user agrees (ask via `AskUserQuestion` if not stated).

History: this discipline was added 2026-05-17 after an
early session nearly fired a
reference-quality milestone with 2/3 criteria closed (the
sibling-hub rollout criterion was open). The `AskUserQuestion`
interrupt caught the mismatch — but the skill prompt should make
the line-by-line read the default, not a save.

Given the criterion read, the session is at one of three **events** — follow its
chapter in [`EVENTS.md`](../../sessions/EVENTS.md). The ceremony lives there now
(WS3 / US-AGORA-012
extracted it from this step so it can be improved as a tangible, versionable
thing); `/agora` only **detects** which event is firing — the criterion 4-eye
gate above — and follows the chapter:

- **Milestone reached** (all the Milestone's spanned Goals' criteria met,
  user-confirmed) → the **`Milestone-reached`** chapter: the Milestone retrospective
  (its Step 1, runs first — the bidirectional abort point) then the Haleluja ceremony
  (stats dump → close-gate preflight → push → watch CI green → annotated
  `milestone-<slug>` tag → COMPASS move → **the record reads the tag:
  `flask agora write milestone-record --tag <tag> --plan <plan>` then `flask agora write improvement --archive-stale` (Step 7b, US-AGORA-056 / 079; every tag kind, behind the green-`suite` gate, US-AGORA-082; the fired rounds leave the live log by command)**
  → close the GH Goal Issue → Haleluja) **and
  then Steps 10–11 — the milestone-ending is a DEDICATED section that does NOT end at
  Haleluja: it hands back through `--end` 2.3 → 2.3b (XP grading, MANDATORY — the
  step that gets skipped when a milestone fires at session-close, the BP-3 bug
  US-AGORA-019 fixes) → 2.4–2.8, and produces the next Milestone's game-plan (the
  rollover).** A Milestone v2 may span multiple Goals (fires when all close);
  single-Goal is behaviour-preserving. Two Milestones in one session → run the chapter
  twice (one retro each).

**The wait itself is a trap with six faces — the compact pytest summary, the harness's
own exit code, `gh run watch --exit-status`, a watcher latched on a superseded run, a
poll that exits on the absence of data, silence under `-q` — read the tool's own
summary line and positive evidence only (runbook C2; `flask agora ci-local` is the reader of the run it made, US-AGORA-091).**

  **Four ceremony traps:**

  - **Verify the explicit CI *conclusion* before an irreversible merge — never the watch exit code.** `gh run watch --exit-status` can return `0` over a FAILED job. **Before merging/tagging, read the explicit `conclusion: success` from `gh run list --branch main --json conclusion` (or `gh pr checks` showing every check `pass`).**

    **And read it for EVERY workflow on the head SHA (Test AND Build):** `gh run list --branch main --json conclusion,workflowName,status` must show every run `completed` + `success` — a single `gh run watch <id>` may have watched a *sibling* workflow.

    **And it binds HOW the list is read: filter on the sha, never trim.** A `tail`/`head` on `gh run list` hides the cut workflow, worst right after a squash-merge; use `--jq '.[] | select(.headSha[0:8]=="<sha>")'` — the capped-grep family (triage step 6) one layer out.

  - **The milestone tag's date must be captured in the FINAL committed stats.**
    `flask stats dump` records each `milestone-*` tag's timestamp; if you
    **recreate the tag** (re-point it) *after* committing stats, the committed
    date no longer matches the pushed tag → CI `stats --check` reds the commit.
    The order: stats dump → commit → create the tag **once** → if stats now counts a
    new milestone, re-dump + commit *that*, then push commit + tag together
    (`--follow-tags`) so CI sees both. Don't recreate the tag after the stats
    commit. (Extends the 2026-06-22 stats↔tag-race note.)

  - **A green preflight is a claim about YOUR machine, not about a clean checkout.** A module-level third-party import in `app/` absent from `requirements.txt` passes every local gate, then reds CI's fresh install at collection — even transitively, with zero commits of ours.

    **When a close-gate run fails at COLLECTION rather than inside a test, diff the failing import chain against `requirements.txt` before suspecting your own diff.** The audit: AST-walk `app/` for module-level third-party imports minus the declared set; each remainder is a guaranteed sub-dependency or a deliberate function-local lazy import.

    **The same claim breaks on a tool's VERSION, not only on a missing package — so "lint clean" names the version that said so.** Before calling a linter clean on code a gate re-lints, read the workflow's installed version (`.github/workflows/*.yml`, the `apt-get` / action pin) and run that one.

  - **Commit or stash the session-log edit BEFORE `gh pr merge --delete-branch`.** The merge succeeds remotely, but a dirty tree aborts the flag's local checkout, and a chained `git pull origin main` merges main into the dead branch. Stash-carry the record to main FIRST; never write on the merged branch.

- **Partial close** (2+ criteria met, remainder belongs to a later session, user
  agrees) → the **`Sub-milestone`** variant of that chapter: a `milestone-<sub-slug>`
  tag records the partial close; the Goal stays active.

- **Parked** (criteria not all met, or `milestone_target: none`) → the **`Session-park`** chapter: confirm the commit triage, push optional (no CI gate), record what advanced toward the Goal.

  **A parked session that COMPLETED a batch/criterion ticks that criterion in COMPASS at THIS close — `- [ ]` → `- [x]` with the session + commits citation — never leaves it for the next `--start`'s reconcile to catch.** The deterministic check is a `mechanism` capture — **#264**. (precedent)

Behaviour is identical to the pre-extraction inline ceremony — EVENTS.md is the
improvable home, not a redesign.

Either event proceeds to 2.3 (compact the log). **The milestone path is NOT
exempt** — a `Milestone-reached` `--end` flows through 2.3 → **2.3b (XP grading)** →
2.4–2.8 exactly like a parked one; the Haleluja is mid-process, never the end (the
milestone-ending dedicated section, US-AGORA-019). If you find yourself writing
`## Close-out` right after a Haleluja, you skipped 2.3b — go back.

### 2.3 — Compact the log + reconcile `skills_invoked:` *(AUTOMATIC)*

> **No gate.** Pure bookkeeping with a checkable output — nothing here is a
> judgement call, so nothing here stops to ask. `flask agora retro-context`
> (2.0) already reported the reconciliation inputs: the skills the Log names,
> which of them are missing from `skills_invoked:`, and the threads touched.
> The XP *grading* half moved to the paper (2.3b); the reconciliation half runs
> unattended.


Read the session file's running **Log**. Distil it into the **Close-out →
Compacted summary** — 3–6 sentences of what the session actually accomplished.
The raw Log entries can stay (they are already a summary), but the Close-out is
the version a future reader starts with.

Carry anything unfinished by **reconciling [`THREADS.md`](../../sessions/THREADS.md)**
(the central registry, added 2026-06-12 — not by copying lists into the session
file): append new threads with fresh `T-NNN` ids (bump the `Next id:` counter),
flip resolved ones with a one-line citing note (session + commit/tag), mark
promotions with their target (`→ Goal #NN` / `→ Issue #NN` / `→ US-XXX-NNN`),
and apply the **promote-or-drop at 3 sessions** rule to anything stale. The
session file's `## Open threads` records only the deltas by id. Each `## Open`
block becomes a candidate intent for a future `/agora --start`.

**A new thread is born PLANNED, not just noted (US-AGORA-022).** Every thread
appended here MUST carry its two fields, set now — not deferred: a **`parent:`**
(the Era or Goal it lives under — the skeleton's slot-1 backlog) and a **`plan:`**
(its resolution plan — *when/how* it resolves). A bare note with no parent + no
plan is **not a valid thread** — either give it both fields or leave it as an
unspecified idea (don't write it to the registry). **Promotion = "gets its Issue"**
(`THREADS.md` Rule 5): when a thread outgrows its origin topic or survives 3
sessions, it earns a GitHub Issue (the slot-1 → slot-0 move), which *is* the
promotion target. **A thread whose parent already IS an Issue is promoted at
birth, not held** — `flask agora write thread-close <tid> --promote <goal-issue>`
posts its block on the Goal Issue (verified) and moves it to Resolved in one call;
`state-check` refuses an open thread parented to `#<n>` (US-AGORA-058, `AGORA-DECL
§6`). The registry holds only threads still awaiting a home (an Era, a Topic, a
Goal not yet opened).

**Registry writes go through the write path — `flask agora write thread-born` /
`thread-close` (US-AGORA-048; the #286 mechanism, shipped).** The writer anchors
on the heading (never the bare string — `THREADS.md`'s own intro contains the
literal text ``each session file's `## Open``, which is how commit `d084111d`
truncated the file and deleted `## Rules` + the `Next id:` counter unnoticed for
three sessions, and how the session 2026-08-01 repair attempt reproduced
the identical bug), assigns the id from the counter (zero-padded), **requires
`parent:` + `plan:` at birth** (US-AGORA-022 enforced structurally), and
post-checks that `## Rules`, `Next id:` and every sibling block survived — a
failed check REFUSES with the file untouched, exit non-zero for this step to
consume. `thread-born` takes the full block with the id written `T-NEW`
(`--file` for multi-line); `thread-close <tid>` takes the full resolution block
(a `**resolved**`/`**promoted**`/`**dropped**` disposition required) and moves
it newest-first under `## Resolved / promoted`. Freehand Edit calls on
THREADS.md are retired at this step.

**Born-thread write is verified, not assumed (drift guard, 2026-06-13).**
Every thread this session names as *born* — in the session file's `## Open
threads` deltas OR anywhere in the Log OR in the INDEX line being written —
MUST have a corresponding `## Open` block (or a `## Resolved / promoted`
block, if born-and-closed same session) in `THREADS.md` before close-out.
A born `T-NNN` id with **no** matching THREADS.md block is a reconciliation
miss to fix in this same step — not a "note it in the session file and move
on" (lived session 2026-06-12 · session 2026-06-13:
T-009 "born" in INDEX, never written to THREADS, recalled by the user). Cheap
check: the ids you write into the session's `## Open threads` deltas and the
ids present in `THREADS.md` after this step must reconcile — every born id
lands somewhere.

**Reconcile `skills_invoked:` frontmatter from the Log before closing.** The
frontmatter list is what `/level --board` reads as the M1 invocation count — if
it undercounts the session's actual skill usage, the leveling system mis-ranks
the corpus. Scan the session's Log for **four** signals:

- `^### Phase X — /<skill-name>` headings (an entire Phase delegated to a skill)
- `^### Step <X.Y> — /<skill-name>` headings (an agora-internal `--end`
  step that dispatched a skill — see step 2.3b / 2.4 / 2.5 below for the
  prepend discipline that writes these)
- Inline mentions like "ran `/<skill>`", "invoked `/<skill>`", "the
  `/<skill>` doctor"
- A **spawn briefed to execute a skill's MODE** ("the 9a spawn ran `/selenium`
  MODE 1", "`/wiki --audit`'s read-only steps via the 9b spawn") — the skill's own
  procedure ran, by a subagent reading its SKILL.md; it counts as an invocation,
  with the spawn named in the Log (lived session 2026-09-05: three doctor audits
  executed by sizing spawns, otherwise invisible to M1).

Build the canonical list from those signals **using set semantics**
(dedupe — one M1 per skill per session, regardless of how many times
the skill was dispatched). Compare against the existing
`skills_invoked:` frontmatter — if the two diverge (the common case:
`/implement-story`, `/new-story`, `/iterate`, `/check-page` get invoked
but not recorded), write the canonical list back to the frontmatter as
part of the same edit that flips `status: closed` (step 2.8). **A plan that names a skill is not evidence it ran** — an
entry no signal supports is REMOVED, never kept for the plan's intent (a blind run
hand-wrote `/implement-story` for two phases it built inline, inflating that skill's
M1 — session 2026-08-01).

History: this discipline was added 2026-05-17 after session
`2026-05-17-agora-issues-integration` Phase D's `/level --board` revealed that
`/implement-story` had `M1=0` despite being the doctor for many features that
week. The structural undercount was Finding F1 of that session's retrospective.
Without this reconciliation, `/level --promote` candidates stay invisible.

**Step-heading reconciliation added 2026-05-23 by US-AGORA-004.**
Until then, agora-internal dispatches at step 2.3b (`/level --xp`),
step 2.4 (`/inspect-pipeline --session`), and step 2.5 (`/learn --from-session`)
were invisible to this reconciliation pass — the called skills never
earned M1 for the work they actually did in `--end`. The load-bearing
problem this fix solves is **M1-promotion-blindness**: with M1 = 0 for
those skills, `/level --board` could never surface them as promotion
candidates. The XP-narrative gap was the cosmetic symptom; the
promotion-blindness is the bug that matters. `/inspect-pipeline` was
the canary — promoted `draft → used` on 2026-05-19 yet still showed
`xp_total: 0` until this fix.

#### 2.3b — Evaluate the unrated journal (grade-at-end) *(paper section)*

> **No separate gate — this becomes the paper's XP section.** The stubs are
> pre-written by the skills themselves (journal-at-source), so grading is a
> *proposal* the user nods once, alongside the commits and the dispatch list.
> `flask agora retro-context` (2.0) reports which buffers are non-empty — the
> union sweep below is what decides *which* of them to grade. Everything else
> in this step is unchanged.


Per [`policy-skill-progression`](../../policies/policy-skill-progression.md)
Rule 6, each `used`+ skill **wrote one-line unrated stubs to its own
`experience.md` `## Unrated journal` buffer as the work happened** (the
journal-at-source discipline — WS1, US-AGORA-009). This step is now pure
**evaluation**: read the stubs, rate them, convert to graded XP, clear the
buffer. The expensive *reconstruct-from-the-Log* distillation is gone — and
with it the "forgot to award XP" + "only `agora`/`learn` get XP" failure modes,
because grading no longer depends on what the orchestrator remembers. **This is
a 4-eye gate** per [`policy-four-eyes`](../../policies/policy-four-eyes.md) —
propose, summarize, nod.

**As `--end` invokes `/level --xp` for each accepted stub at the
end of this step, prepend** `### Step 2.3b — /level --xp` **to the
Log entry that records the awards** — one heading per awarded skill is
sufficient (set semantics; see step 2.3). This makes the dispatch
visible to the reconciliation pass (step 2.3) so `/level` itself earns
M1 for the work it does inside `--end`. Discipline added 2026-05-23 by
US-AGORA-004.

**Journal-at-source for orchestrator-inline dispatches (WS1 coverage, added
2026-06-01).** Every place `--end` prepends a `### Step <X.Y> — /<skill>` heading
— here at 2.3b, plus 2.4 (`/inspect-pipeline --session`) and 2.5
(`/learn --from-session`) — it ALSO appends a one-line unrated stub to that
skill's own `## Unrated journal` buffer **on the skill's behalf**:
`YYYY-MM-DD · [[session-id]] · inline dispatch at step <X.Y> · 🟢/🟡 <signal>`.
These skills are invoked by the machinery, not as a self-journaling phase, so the
orchestrator journals them at the same moment it writes the heading. The stub is
graded at a *subsequent* `--end` 2.3b (a one-session lag is expected — the buffer
is cross-session; `/level --xp` runs during 2.3b, while `/inspect-pipeline` (2.4)
and `/learn` (2.5) run after it).

**On-behalf stubs go through the write path —
`flask agora write journal-stub --skill <name> --text "<stub>"` (US-AGORA-048).**
The writer enforces the canonical shape (a leading `- ` is normalized away, a
dateless line refuses), lands the stub inside the journal section, and
post-checks that the file's `<!--`/`-->` markers still balance — an unterminated
opener means a stub fused into the comment marker, hiding everything after it
(lived session 2026-07-10: `<!-- P26-07-08 · …` in three buffers,
ungraded for two sessions). The format-tolerance rule (2026-07-04) fixed
*reading* a drifted stub; the writer refuses to *produce* one — freehand
appends to the buffers are retired at this step.

This closes the WS1 gap surfaced by
session 2026-05-31's retro: journal-at-source covers
orchestrator-inline skills, not only session-phase invocations. (Set semantics —
one stub per skill per session, matching the M1 reconciliation in step 2.3.)

**Grading scope is a UNION, not just this session's roster** (fix 2026-06-12,
session 2026-06-12): grade **(a)** each `used`+
skill invoked in this session AND **(b)** every `used`+ skill whose
`## Unrated journal` buffer is **non-empty** — regardless of `skills_invoked:`.
(b) exists because orchestrator-inline stubs (written on the skill's behalf at
steps 2.3b/2.4/2.5) land *after* this step already ran — they are only
gradeable at a **later** session's 2.3b, and that session may not have invoked
the skill at all. Without the sweep, those stubs rot: `inspect-pipeline`
carried a stub from 2026-06-06 through ~5 `--end`s ungraded. Cheap check:
`grep -A3 'Stubs land below' .claude/skills/*/experience.md` (or read each
`used`+ buffer) before drafting the proposal bundle.

**The sweep is FORMAT-TOLERANT — "non-empty buffer" means any content line,
not lines matching the canonical stub shape** (fix 2026-07-04,
session 2026-07-04). The canonical stub is ONE line with
**no leading list marker**: `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡
<signal>`. But a stub written with a leading dash (`- YYYY-MM-DD · …`), odd
indentation, or placed above/below the buffer's comment markers is STILL a
stub — a scan keyed to the canonical line shape silently skips it (lived
session 2026-06-30: three dash-prefixed stubs survived four
`--end`s ungraded). Sweep rule: treat **every
non-comment content line anywhere in the `## Unrated journal` section** as a
stub candidate; normalize format drift to canonical when grading (and when
writing on-behalf stubs, write the canonical shape — no dash).

For each skill in that union:

1. **Read its `## Unrated journal` buffer — BEFORE distilling anything from the Log.** The buffer is the primary source; grading from the Log while an unread stub sits in the buffer is the named failure mode **"log-sourced award + surviving stub"**.

   Each stub is a one-line
   `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <signal>` the skill wrote
   when it finished a unit of work. Rate each stub:
   - 🟢 **Success** (+20 to +30 XP) — the skill delivered a load-bearing
     sub-goal, validated a non-obvious pattern, earned a new cross-reference,
     or held up under genuine pressure.
   - 🟡 **Lesson** (+10 to +15 XP) — the skill needed a `/learn` patch
     this session, surfaced an edge case worth codifying, or absorbed a
     redirect that strengthens its contract.
   The stub already carries the 🟢/🟡 signal the skill self-assessed; the
   grading either confirms it or adjusts with reasoning.

2. **Expand each rated stub into the one-paragraph graded snippet** — the
   *why* of the XP entry. The stub is the seed; flesh it out from the stub +
   Log context into a self-contained paragraph (commit sha, file path,
   redirect, `/learn` patch hash) readable in 6 months. **Fallback:** if a
   skill's buffer is *empty* (it wrote no stubs — e.g. it forgot, or it's a
   freshly-promoted skill), distill 1–2 proposals from the Log as before. The
   buffer is the primary source; the Log is the fallback — never the other
   way around. **Every accepted `/level --xp` award MUST clear its
   corresponding stub from the buffer in the same write** (US-AGORA-010); an
   award whose stub survives is the bug, not a variant.

3. **Skip `draft` skills for XP** — XP starts at `used` per `policy-skill-progression`
   Rule 6. But a draft skill that was invoked IS a structural candidacy
   signal — surface it at step 4 below, not "in step 2.6 retro" (the
   prior rule had this responsibility floating in prose; US-AGORA-004
   makes it structural).

4. **Walk `skills_invoked:` for `level: draft` skills and emit one
   candidacy bullet per skill** at the same 4-eye gate as the XP
   proposals (per US-AGORA-004). Format:
   `Promotion candidate: /<skill> (draft → used; M1 now <N>, gate: <met / pending>)`.
   When no draft skills were invoked, no candidacy block appears — the
   absence is silent (avoids ceremony when there's nothing to surface). (precedent)

**Present the bundle as a summarized 4-eye gate:**

```
XP proposals from this session — 4-eye gate

/check-page       🟢 +25 XP  — "Drove the hub subtab rollout cleanly;
                              `--finish` mode held up across 10 zones
                              without rework. (commit fd9139a)"
/implement-story  🟢 +30 XP  — "Phase 3.2b registry-completeness step
                              caught the entity-list omission before any
                              UI work — the doctor caught what would
                              otherwise have been an iteration round."
/agora            🟡 +12 XP  — "Caught the 'smoke pass ≠ user confirmation'
                              drift; updated the commit-tree triage
                              discipline note in the SKILL.md body."

Promotion candidates (draft → used):
/selenium         M1 now 2, gate: pending  (gate met at M1 ≥ 3 per
                                            policy-skill-progression)

Total: 3 XP awards (+67 XP), 1 candidate. Confirm / edit / skip-some /
cancel?
```

The user nods, edits, or skips per item. On confirmation:
- For accepted XP proposals — call `/level <skill> --xp +<N> "<snippet>"`. The
  `--xp` write **converts the stub to a graded entry AND clears it from the
  `## Unrated journal` buffer** (US-AGORA-010), so a stub is never double-counted.
  A stub the user skips stays in the buffer for next session (or is dropped with
  a note — user's call).
- For accepted candidacy bullets where the gate is met — queue
  `/level <skill> --promote` (the actual promotion runs in step 2.6
  retro or a future session, depending on whether the user wants the
  naming-ceremony moment now or deferred). For pending-gate candidates
  — record the candidacy in the session's Open threads so the next
  `--start` surfaces it.

`/level --xp` does not commit; the close-out commit (step 2.1 if any
remain unstaged, or step 2.2 Path A's existing commit) batches them.

### 2.4 — session-scoped pipeline inspection (incl. Agora self-audit) *(AUTOMATIC — surfaces on finding)*

> **Runs unconditionally; interrupts only on 🟡/🔴.** A 🟢 verdict needs no gate —
> it is recorded in the paper as one line and the close moves on. A 🟡/🔴 verdict
> becomes findings in the paper's dispatch section, where the user sees them
> alongside everything else. The audit itself is unchanged — including the
> `/agora` self-audit, which is the whole reason a meta-skill with no doctor
> above it never goes unaudited.


Invoke [`/inspect-pipeline --session <file>`](../inspect-pipeline/SKILL.md) on
this session file. That mode audits the skill system *through the lens of what
happened this session* — skills that needed manual correction, rules stated
from memory more than once, repeatable procedures done ad-hoc. It produces a
verdict and a dispatch list. Record the verdict in **Close-out**.

**Prepend** `### Step 2.4 — /inspect-pipeline --session` **to the Log
entry that records the verdict** — this is the dispatch that the
reconciliation pass at step 2.3 reads via the `^### Step <X.Y>` regex,
so `/inspect-pipeline` earns M1 for the audit it runs every `--end`.
Discipline added 2026-05-23 by US-AGORA-004;
the canary bug that motivated the fix was `/inspect-pipeline` showing
`xp_total: 0` despite being invoked by every `--end` since its
promotion to `used` 2026-05-19.

**`/agora` audits itself here too — this is its self-learning loop.** `/agora`
is a meta skill: it has no doctor above it. But it is *always* an invoked skill
— it brackets every session — so `/inspect-pipeline --session` always
cross-checks it, and `--end` treats that as a deliberate **self-audit**. Ask of
this session:

- Did `--start` actually load context (1.1 — recent sessions, skill-system
  state, **the product backlog**) and place the goal as new vs. continuation (1.2)?
- Did the commit-tree + open-PR triage (1.3) and the push + CI gate (2.2)
  follow [policy-commit-discipline](../../policies/policy-commit-discipline.md)?
- Did the skill-pipeline plan (1.4) hold — or did the real work diverge from
  it, and was the divergence *reasoned* or just drift?
- Did the session file stay a useful structured summary, or rot into a stub or
  a transcript?

Every "no" is a finding **against `/agora` itself**, carried into the dispatch
list (2.5) like any other — `/learn --from-session <file>` patches `agora`'s
own SKILL.md, a recurring structural gap becomes a `/document` policy. The
orchestrator improves itself from the same session record it makes every other
skill improve from.

### 2.5 — Dispatch the findings *(paper section)*

> **No separate gate — this becomes the paper's dispatch section.** Since
> US-AGORA-029 every lesson already carries a `mechanism | prose | judgment`
> **disposition**, which is more reason to present the routing as one list the
> user nods rather than as a gate of its own. Everything below is unchanged;
> only the moment of asking moved.

Take the session file's **Agora findings**, the `/inspect-pipeline --session`
dispatch list, the self-audit findings (2.4), and any recurring-CI-fix findings
(2.2). For each, route per
[policy-documentation](../../policies/policy-documentation.md):

- **Skill-level correction** → [`/learn --from-session <file>`](../learn/SKILL.md)
  — `/learn` reads the findings straight from the session file and patches the
  skill(s) surgically.
- **Cross-cutting rule** → [`/document --policy <slug>`](../document/SKILL.md).
- **A real bug / a real feature** → `/fixbug` or `/new-story` — note it as an
  Open thread, don't try to do it inside `--end`.

**When `/learn --from-session` is dispatched, prepend** `### Step 2.5 — /learn --from-session`
**to the Log entry that records the dispatch.** Same reconciliation
discipline as step 2.3b + 2.4 — agora-internal invocations earn M1 for
the skill they call. When no `/learn` dispatches fire (the common case
on a clean session with no findings), no heading is written — the
absence is silent. Discipline added 2026-05-23 by US-AGORA-004.

**Surface each lesson's DISPOSITION in the dispatch proposal (US-AGORA-029).**
`/learn` classifies every lesson as `mechanism` / `prose` / `judgment` at its
Step 2b-mech, and the classification is only useful if it happens where
`/learn` is already being invoked — here — rather than depending on the agent
remembering to ask. So the dispatch list names the expected disposition per
lesson:

```
Dispatch (4-eye gate):
  /learn agora   — "a broken check reports success"     → mechanism  (capture the check)
  /learn plaza   — "a landscape is a map"               → judgment   (prose is its tier)
  /document      — policy-frontend-conventions Rule 14  → prose
```

A `mechanism` lesson is expected to come back with a change-request Issue, not just a patched SKILL.md — `/learn` calls `flask agora capture` itself. The disposition is *proposed* here and *recorded* by `/learn` in the target's `## Level history`.

`check_learn_dispositions` in the frontmatter validator fails the lint when a patch records none, so a skipped classification is caught at the next `--start` 1.1 pre-flight rather than never. (precedent)

Propose the dispatch list; the user confirms which to run (don't auto-fire).
Record what was dispatched in **Close-out**.

### 2.6 — session retrospective — DRAFTED, never solicited *(paper section)*

**Scope: session — work-window scope, sprint-retro analogue.** The
Goal-scoped *release-retro* analogue is at step 2.2.5 (Path A only);
2.6 is the *sprint-retro* analogue that fires Path A AND Path B both.
The two are deliberately separate per US-AGORA-005 — Goal-scoped
lessons go to IMPROVEMENTS.md via 2.2.5; session-scoped tactical
lessons live here and feed `--start`-of-next-session via Open threads.

**Skipped entirely on a `simple` shape** (2.0). A one-go session does not earn a
retro; asking for one is the ceremony the shape classification exists to avoid.

**The agent WRITES the retro; it does not ask for one (D2).** A blank
three-question form presented at the end of a long session was the user's first
named drop candidate — it arrives exactly when they have least appetite to
compose prose. So `/agora` drafts all three answers from the session record
(grounded by `flask agora retro-context`, 2.0), puts the draft in the paper, and
the user **nods, corrects, or adds**. Three prompts, now three *drafted
sections*:

1. **What worked this session?** — what to keep, what to repeat.
2. **What didn't?** — what frustrated, what felt forced, what skill
   misbehaved, what the orchestrator pushed when it shouldn't have.
3. **What to change next session?** — concrete asks: skill tweaks,
   policy clarifications, vocabulary refinements, ceremony adjustments.

Draft from **evidence, not impression** — a redirect the user actually made, a
phase that overran, a gate that did not fire, a test that caught something late.
A draft that only says "the session went well" is not a retro; it is filler, and
it teaches the user to skim the paper.

**The user's own words stay verbatim.** The agent writes the *structure* and the
*evidence*; anything the user says at the gate goes in unparaphrased, replacing
or extending the draft. Items in (2) and (3) that
look like skill-level corrections or policy candidates feed the dispatch
(2.5) on the way to close-out — if the retro surfaced something 2.5
missed, loop back briefly.

**Bank the Agora-shaped items BEFORE the session closes — a step that runs
(US-AGORA-030).** Some retro answers are neither a skill correction (2.5) nor a
policy candidate: they are *ideas about how Agora itself should work*. Those have
historically died in retro prose — the v5 prep session had to sweep 11 retros to
recover **four rulings that had been made and lost**, each because at the time it
read as praise or as next-session planning rather than as an improvement ask. So
for every retro item that is an Agora-improvement candidate, make one call before
writing the close-out:

```bash
flask agora capture "<the item, one or two sentences>" --type retro --source "<session-id>"
```

It lands on the current self-improvement round Issue — resolved from COMPASS
**"Goals (active)" first, then the Goal-backlog index** (US-AGORA-051), so the
store collects in the between-rounds window too; no network needed to resolve
it — and the next `/plaza` round harvests it with zero recovery work.
**Capture is never a gate** — with `gh` unavailable it spools to
`.claude/sessions/capture-spool.md`, exits 0, and the spooled block is surfaced
as a standing `[SPOOL]` line by `flask agora state-check` at every `--start`
1.1 until `flask agora capture --flush` delivers it (idempotent — the
`agora-capture-id` anchor prevents double-posting). Propose the list at the same 4-eye gate as the retro
answers; the user nods or trims. When no retro item is Agora-shaped, nothing is
captured — the absence is silent.

**Edit the existing `### Retrospective` block in place — do NOT append
a new template.** The session file already carries an empty
`### Retrospective` scaffold from `_TEMPLATE.md` (under `## Close-out`,
after the touched-and-unresolved list). Fill that scaffold
*in situ*; never insert a second `### Retrospective` heading. A
duplicate empty stub at the bottom of the close-out is the classic
template-stickiness drift (lived
session 2026-05-23: a filled retro AND an empty
scaffold at the file tail).
The check before saving: grep the file for `### Retrospective` and
confirm exactly **one** occurrence.

The retro always runs — Milestone reached or not. It is the only step
in `--end` that cannot be deferred.

### 2.7 — [RETIRED] Prompting & skill-usage coaching

**Deleted by US-AGORA-034.**
The US-AGORA-033 probe
audited all eleven `--end` steps against *"what breaks if this stops existing?"*
and found exactly **one** genuine elimination: this one. The user's words —
*"the points I see which are not necessary are also the coaching."*

**The number is retired, never reused** — a future step numbered 2.7 would make
every historical citation ambiguous.

**What survived, and where it went.** Coaching's two useful outputs were never
the advice; they were the *findings*:

- **Missed routing** — work done inline where a skill exists
  ([`policy-skill-routing`](../../policies/policy-skill-routing.md) Rule 4,
  the retrospective half) → now a **finding in the close-out paper**, and a 🟡
  lesson note for the skill at 2.3b where the missed skill is `used`+. The
  named exception still holds: *rapid single-surface live-verify rounds with
  the user present* are legitimately inline and are NOT a finding.
- **Policy breaches** (WS2, US-AGORA-006) — confirmed violations of a *named*
  policy → still appended to
  [`policy-breaches.md`](../../sessions/policy-breaches.md), now confirmed
  at the paper's single gate rather than at a gate of its own, and written
  through the write path:
  `flask agora write breach --date YYYY-MM-DD --policy policy-<slug> --session <session-id> --text "<what broke>"`
  (US-AGORA-048 — newest-first date order is an enforced invariant; the ledger
  had drifted out of order and sat that way silently until the writer's first
  acceptance run found it). Confirmed
  breaches only — an over-eager ledger is as useless as none.

What did *not* survive is the register: prose advising the user how to drive
better. The findings go in the paper as **observations about the session**, not
as coaching addressed to the person reading it.

### 2.8b — Issue UPDATE (always) · Issue CLOSE (conditionally)

**This step always runs — Milestone reached or parked.** A session that
*finished* work tracked by a GH Issue closes that Issue; otherwise done
work drifts open and the board lies (the live evidence at this step's
authoring: #74 + #75 shipped 2026-05-20 yet sat open until 2026-05-21).

**The step SPLITS in two, because the two halves are not equally conditional
(D5).** The user's ruling: *"it should always be a part of the end that the
current issue is updated."*

| Half | When | Gate |
|---|---|---|
| **UPDATE** — comment progress onto every Issue the session worked | **always**, every shape including `simple` | none — it executes |
| **CLOSE** — close an Issue whose work shipped | only when work actually shipped | **proposed in the paper**, nodded once |

The **update** half is what makes a plan read at the *next* `--start`
trustworthy: an un-updated Issue makes the next session re-plan work that is
already done (US-AGORA-021 — the Issue comments are the base of the planning).
`flask agora retro-context` (2.0) reports the Issue numbers the session
referenced, so the update half has its candidate list without hand-scanning.

On a `simple` shape the update half is the *whole* Issue story — *"the issue
part comes down to a simple comment."*

Closing stays behind the nod: it is an outward, irreversible-ish GitHub-state
action, and *"leave open"* is a common and correct answer for a sub-goal that
advanced without finishing.

1. **Build the candidate list from the session.** Walk the Log + the
   `commits:` frontmatter for work that *completed* something an open
   GH Issue tracks. Three sources:
   - the **Goal mirror Issue** (Path A step 7 — when a Milestone fired);
   - **sub-goal Issues** (`agora:type:sub-goal`) whose deliverable this
     session shipped — match by the story id / slug in the Issue title
     against `stories_touched:` + the Log;
   - any **`agora:type:section`** Issue mirroring this session.
   Cross-check against the open board with
   `gh issue list --state open --label agora:type:sub-goal` (and `:goal`).
   On Windows, the conda env may shadow the real CLI — call
   `"C:\Program Files\GitHub CLI\gh.exe"` if `gh` resolves elsewhere.
2. **Present the close list as a 4-eye gate** per
   [`policy-four-eyes`](../../policies/policy-four-eyes.md) — closing an
   Issue is an outward, GitHub-state action; never auto-fire. Summarize:
   `#<n> <title> — closed by <commit/tag>; comment: "<one-line cite>"`.
   The user nods, edits, or drops entries. **A "leave open" is common
   and fine** — partial work, or a sub-goal that advanced but didn't
   finish, stays open.

   **NEVER close an Issue whose body still carries scaffold placeholders**
   (`_(fill in — ...)_` — the `flask agora batches` template's Scope /
   Done-means stubs). An empty closed Issue is the board lying twice: it
   claims work it never describes. Before proposing a close, read the
   Issue body; a placeholder means either fill it now (from the session
   record — a two-minute write) or leave it open with the fill as the
   named blocker. The **fill belongs at the batch's OPEN** (the session's
   Phase 0, when its scope is being confirmed anyway — the
   session 2026-07-29 precedent, which the user contrasted with
   #255 closing unfilled at the B1 blind session). Already-closed empty
   Issues stay closed (no retro-backfill sweep — the user's ruling);
   the rule is forward-only. The deterministic check (a body-grep for the
   placeholder marker in the 2.8b close proposal + `closure-candidates`)
   is a `mechanism` capture — **#263**.
3. **On the nod, close each with a citing comment:**
   `gh issue close <n> --comment "Closed by <session-id> — <commit shas / milestone tag>. <what shipped>."`
   The comment is the durable bridge from the Issue back to the session
   that closed it.
4. **Record** the closed Issue numbers in the Close-out report.

Per [`policy-issue-templates`](../../policies/policy-issue-templates.md) —
the Issue board is Agora's external mirror; `--end` is where it
reconciles with what actually shipped.

### 2.10 — THE CLOSE-OUT PAPER · THE ONE GATE · EXECUTE

**This is `--end`'s deliverable.** Everything above produced a *section*; this
step assembles them into one paper, presents it **once**, and — on the nod —
executes all of it.

> **On the number:** a fresh one (2.10), deliberately — not 2.7b. Step numbers
> here are **identifiers, not a sequence**, and 2.7 is retired. This step is
> assembled after 2.8b and runs before 2.8; the diagram at the top of MODE 2 is
> the execution order.

**The paper is produced by a step, not filled in from a template.** A `--end`
that produces no paper is incomplete in exactly the way a `--end` with no commit
triage is. That is the round's acceptance question applied to this story: a call
site, not a rule.

#### The paper's sections (by shape, per 2.0)

| Section | simple | substantive | milestone |
|---|:--:|:--:|:--:|
| **Compacted summary** (2.3) | ✓ | ✓ | ✓ |
| **Commits** — declared-vs-actual, grouped files + one-line subjects (2.1) | ✓ | ✓ | ✓ |
| **Issue update** — the comment(s) going onto every worked Issue (2.8b) | ✓ | ✓ | ✓ |
| **Touched-and-unresolved** — one visible list, a disposition each (2.0) | ✓ | ✓ | ✓ |
| **Baton** — what the next session inherits, drafted by `flask agora baton --draft` (2.9) | ✓ | ✓ | ✓ |
| **Handoff checklist** — `mode: blind` only; seeded by `flask agora handoff --draft` | if blind | if blind | if blind |
| **Plans emitted** — `mode: planning` only; the `P-NNN`(s) written to PLANS.md, each `ready` or with its gate gap named | if planning | if planning | if planning |
| **XP awards** — one line per skill (2.3b) | — | ✓ | ✓ |
| **Dispatch** — one line per lesson **with its disposition** (2.5) | — | ✓ | ✓ |
| **Audit verdict** — one line; findings only if 🟡/🔴 (2.4) | — | ✓ | ✓ |
| **Drafted retro** — three written sections (2.6) | — | ✓ | ✓ |
| **Issue closes** — proposed, never auto-fired (2.8b) | if shipped | if shipped | ✓ |
| **Goal retro** (2.2.5) | — | — | ✓ (own gate) |

**The touched-and-unresolved list is `policy-shoulder-glance`'s catch half made
an artifact.** Every item carries a named disposition — **resolved · thread ·
Issue · deliberately dropped**. "Deliberately dropped" is a legitimate answer;
*absent from the list* is not. `flask agora retro-context` produces the raw list;
the paper is where each item gets its disposition.

#### The one gate

Present the assembled paper and wait for **one** textual nod. Per
[`policy-four-eyes`](../../policies/policy-four-eyes.md):

- **Rule 3 — summarized.** Grouped files + one-line subjects; XP one line each;
  dispatch one line each; the retro drafted but tight. **Full commit bodies are
  written after the nod, never before** — a paper carrying full bodies turns the
  nod into a rubber-stamp of text the user may not have read carefully. The gate
  consolidation must not become gate *evasion*.
- **Rule 4 — smoke-test pass ≠ user nod.** Ruff clean, tests green and a clean
  close-gate preflight are *prerequisites* to presenting the paper, never
  substitutes for the nod.
- **Rule 5 — bidirectional.** The nod routinely arrives as *"yes, and also X"*
  or *"split that commit"*. That is the gate working, not friction.

**What the single nod authorizes:** the commits · the XP writes · the dispatches ·
the Issue comments and the proposed closes · the retro as written · the
bookkeeping.

**What it does NOT authorize:** firing a Milestone tag (2.2 keeps its own gate,
because a tag is the one irreversible act) and `git push` on a milestone close.

#### Execute

On the nod, run it all without further asking:

1. Write the full commit bodies and commit, staging by explicit path
   (**verify the index before each commit** — `git diff --cached --name-only`
   against the commit's own file list).
2. `/level <skill> --xp +<N> "<snippet>"` per accepted award, **clearing each
   graded stub from its buffer in the same write**.
3. Fire the accepted dispatches (`/learn --from-session`, `/document --policy`,
   `flask agora capture`), prepending the `### Step <X.Y> — /<skill>` Log
   headings so 2.3's reconciliation counts them.
4. Comment on every worked Issue; close the ones the user accepted, each with a
   citing comment.
5. Continue to 2.8 (bookkeeping) — automatic, order-sensitive.

If assembling the paper surfaces something its summary did not (a forgotten
co-reference, a hidden migration risk), surface it **between the nod and the
action** and abort cleanly if needed — the same escape hatch the old commit gate
carried.

### 2.8 — Close out *(AUTOMATIC)*

This step always runs — Milestone reached or parked. **No gate** — it is
mechanical and order-sensitive; the ordering below is the whole content. The
gating differs
by path: if a Milestone was reached, 2.2 Path A is **green and pushed**
before reaching here; if parked, 2.2 Path B simply finished cleanly.

- Flip the session with **`flask agora write close`** (US-AGORA-106) — it refuses, file
  untouched, until the file carries `## Close-out` with its `### Baton` and `### Retrospective`
  filled (2.10 writes the paper INTO the file first; a `**Shape:** simple` close may drop the
  retro) and no line is still one of the template's placeholders (T019 T038). `state-check`
  reads the flip at every `--start`: one open session at a time, a close carries its paper.

- Write the one-line outcome and re-render the index: `flask agora write outcome
  "<one line>"`, `flask agora write roster --session <id>` (the Era roster's line,
  US-AGORA-092), then `flask agora write index` (US-AGORA-067 — the `INDEX.md` line
  is a projection of `type` · `status` · `outcome` · `era`; a hand-spliced line is
  overwritten by the next render and reds the record-consistency check).

- **Before the close commit, run `flask wiki touched` -- the close's files against every seed's sources (US-AGORA-103).** The close writes files a `truth: source` seed hashes (the cheatsheet, EVENTS, COMPASS), so a page stamped earlier in the session is stale the moment the close commits.

  Each group prints its remedy: a `source_of_truth` hit is read, then `flask wiki rehash --slug <slug> --yes` + `flask wiki verify <slug> --by <user>`; a changed seed file is reloaded with `flask wiki seed --slug <slug>`.

- If the session produced a **real lesson about Agora itself** — a skill
  patched, a policy authored, a prompting pattern worth keeping, a
  recurring CI fix turned into a policy — append one entry to
  [`IMPROVEMENTS.md`](../../sessions/IMPROVEMENTS.md) **through the write
  path**: `flask agora write improvement --file <entry.md>` (US-AGORA-048 —
  it anchors below the newest-entries marker and refuses the #333 shape,
  where ~17 consecutive closes had inserted their entries INSIDE the format
  template's code fence unnoticed). Not every session
  earns an entry; a routine feature build does not. A session that
  *changed how Agora works* does.

- **`flask agora regen` runs IMMEDIATELY after the session-file flip + the `write outcome` + `write index` + the IMPROVEMENTS.md append** — not before (US-AGORA-096; the chain's first member is `flask stats dump`): a dump while the session is still `status: open` commits the open-snapshot, and CI's fresh-checkout regen reds.

  The order is load-bearing: `write close` → `write outcome` → `write roster` → `write index` → append IMPROVEMENTS → `flask agora regen` → stage all → commit. The close-out commit bundles all of them.

- Report to the user: commits made; the **Milestone outcome** (if
  reached: tag + green CI run id + push; if parked: which success
  criteria advanced and which remain); the session file path; the
  inspection verdict; what was dispatched; the retrospective entry; the
  coaching. (precedent)

### 2.9 — The rollover is not a question (US-AGORA-035)

**There is no rollover offer. Do not ask one.** The step keeps its number and its
place; what was removed is the *question* — the same treatment 2.7 got.

**Why the offer went.** The US-AGORA-033 probe inverted this step's premise. The
rollover is **not unused**: 11 of the last 18 sessions were preceded by another the
same day, and every recent milestone is followed by an immediate continuation. What
is unused is the *step* — "rollover" appears in one of five recent Path-A session
files, and there it is the successor describing itself, not the predecessor making
the offer. US-AGORA-027
shipped **a description of what already happens** rather than a mechanism that
changes anything.

The root cause is not the wording. **An offer that saves nothing will not be taken
however it is worded** — saying yes still cost a full `--end` followed by a full
`--start`, so declining was rational. Adding "proactively offer it, never skip the
offer" made a rational decline slightly more awkward and changed nothing else.

**So the boundary got cheap instead of chatty:**

1. **The paper's single nod carries the close.** 2.10 executes; 2.8 does the
   bookkeeping. Nothing pauses to ask what happens next.
2. **The baton is written on EVERY close, both paths** — its section of the paper,
   drafted by `flask agora baton --draft <session-file>` rather than composed from a
   conversation that may already be compacted.
3. **If the conversation continues, `--start` opens against that baton.** Its first
   read is `flask agora baton` (1.1) — verified pointers, not a cold re-derivation.
   The correctness reads still all run; they are four cheap commands. What is gone is
   the expensive half: re-deriving *where we were* from INDEX + COMPASS + THREADS by
   hand.
4. **If it doesn't, the session is simply over.** That is the park, and it needs no
   ceremony either.

**Both paths, not milestone-only.** The old step fired at a Goal boundary. The probe
measured the cost somewhere else: **unnatural cuts** — sessions ended for
context-window reasons rather than work reasons (*"the cut is not natural — it's
needed to hold the session context together"*), which are overwhelmingly Path-B
parks. Writing the baton only at milestones would leave the boundary expensive
exactly where it is paid most.

**Path B stays behaviour-preserving (AC9).** "No *forced* rollover" is honoured by
deleting a question, not by keeping one. Nothing is forced on either path; a session
that ends, ends.

Pairs with **US-AGORA-026** (the prompt-less `--start` proposes *from* the baton) and
**US-AGORA-019** (the milestone-ending that produces the next game-plan, which the
baton then points at).

---

## MODE 3 — `--status`

A mid-session check. **Read-only** — makes no commits, no edits.

1. Find the `open` session file (`Grep: status: open` in `.claude/sessions/`).
   If none, say so — "no open session; `/agora --start` to begin one."
2. Report:
   - the session **intent** and **type**
   - the **`milestone_target:`** — the Milestone this session is aiming at and
     which Goal criteria it closes (the "what are we focusing on" answer, surfaced
     prominently per WS3/US-AGORA-012). If `none — exploration`, say so.
   - the **session plan** with checked / unchecked progress
   - the **dirty-tree state** — `git status --short` (how much is uncommitted
     since the last triage) + any **open PRs** (`gh pr list --state open`)
   - the **Open threads** and **Agora findings** logged so far
3. End with the obvious next action — the next unchecked plan item, or
   "everything ticked — `/agora --end` to close out."

---

## MODE 4 — `--spawn <sub-goal description>`

Outsources a separable sub-goal to a subagent. The parent writes a
self-contained briefing into a spawn file; the subagent reads that file,
does the work, and **writes its answer back into the file's `## Result`
section itself** — the parent folds the returned summary into its Log. No
copy-paste.

**Two delivery mechanisms** (orthogonal to the authorization tier):

- **Auto-spawn — the default.** The parent dispatches the briefing via the
  **Agent tool**. The subagent reads the spawn file, executes within its
  tier, writes its deliverable into the spawn file's `## Result` block, and
  replies with the reply-protocol summary. The harness returns that summary
  to the parent automatically — zero copy-paste.
- **Manual spawn — opt-in.** The parent surfaces the briefing as a
  copy-pasteable block; the user runs it in an **external window or a
  different model** (Claude.ai, a Copilot, a task-specific model) and pastes
  the result into `## Result`. Use this only when the value is *a different
  model or a separate context window* — otherwise auto is strictly better.

Apply [`policy-spawns`](../../policies/policy-spawns.md) — MODE 4 is
the canonical dispatch path; the policy is what MODE 4 reads to
validate a dispatch (authorization tier, delivery mechanism,
parallel-write disjointness, five required briefing sections,
append-only lifecycle).

**When to use** (per policy-spawns Rule 1):

- The sub-goal is **read-only research** or **drafting in isolation** —
  doesn't need the parent's working tree.
- The sub-goal would **derail the parent session's flow** if walked
  in-thread.
- The parent session is approaching its **context budget** and the
  sub-goal would push it over.
- Two sub-goals can run in **parallel** without sharing state.

**When NOT to use:** sub-goals that need to edit files the parent is
in flight on, run tests, or coordinate with the parent's open changes —
those need the parent's context, not a fresh one.

### Procedure

1. **Receive the sub-goal description.** It should name (a) what
   question the spawn answers, (b) what output format is expected, (c)
   what the parent will do with the result.

2. **Decide the authorization tier** (policy-spawns Rule 2):
   `advisory` (return markdown, default) · `write` (Write/Edit
   allowlisted paths, no commits) · `commit` (commit allowlisted paths).
   `write` and `commit` REQUIRE a path allowlist. `commit` requires
   explicit user authorization at dispatch.

3. **Check concurrency** (policy-spawns Rule 3): scan
   `.claude/sessions/spawns/*.md` for `status: open` files. For a
   `write`-tier dispatch, every open `write` spawn's `allowlist:` must
   be **disjoint** from the new one. Max 3 concurrent `write` spawns. A
   `commit` spawn does NOT run alongside any other `write` / `commit`
   spawn.

4. **Draft the briefing — five required sections** (policy-spawns
   Rule 4): **Background** (zero-context setup) · **Files to sweep**
   (concrete paths) · **Constraints** (explicit "do NOT touch" list —
   every parent-in-flight path) · **Deliverable shape** (testable —
   file + structure + a size budget in the deliverable's own unit — tests,
   locators, rows, never lines) · **Reply protocol** (what to
   include in the return message; do NOT paste file contents back).
   Reference: the briefings in
   `spawns/2026-05-16-agora-vocabulary-consolidation.md`
   and
   `spawns/2026-05-16-premium-save-toast.md`.

   **Briefing precision — pin exact verified paths + canonical data sources; never let the spawn infer a location or invent a value.** **(a)** *verify the actual file path before writing the allowlist; don't infer it from the entity name*; **(b)** name every select's data source, or the spawn hardcodes one.

   So: in **Files to sweep**, name the *exact, opened-and-confirmed* paths the spawn edits; in **Deliverable shape**, name the **canonical source** for any select-of-enum field (`get_enum_values(entity,field)`), any save-route, any shared macro — never leave the spawn to choose, nor rely on it flagging a wrong path.

   **And an advisory READER's deliverable names the CORRECT value beside every `[drifted]` verdict** — the real path, count or version in the Note column — so the parent edits from the table; the parent's grep of every negative claim stays the rule.

   **A SECURITY claim's row asks the inverse question — *what does the code ACCEPT that the claim excludes?* — not *does the named mechanism exist?*:** presence is exactly what a bypass leaves intact. The briefing names that question per security claim, and the parent reads those rows' code itself.

   **And a reader that COUNTS a shape is briefed with every spelling of it, taken from a grep of the callers, never from the macro file alone.** (precedent)

   **A briefing's claim about BACKEND READINESS is load-bearing — verify it like the plan's claims; and verify a returned spawn's NEGATIVE claims before building on them.** **(a)** A readiness claim about a route is one `grep -rn "<url-prefix>/" app/routes/` away from verified — spend it before the briefing ships.

   **(b)** A spawn's negative claim about a ROUTE or a TEMPLATE needs a repo-wide grep by the key its CONSUMERS use before the parent acts on it — the spawn read one file; the parent owns the repo-wide view.

   A "no caller" claim greps both the path and the endpoint name (`url_for('main.<endpoint>')`) across `app/`; an "orphaned partial" claim also greps the computed include shapes (`include .* ~`) before it becomes an Issue. (precedent)

   **A briefing must never prescribe a step that takes a GLOBAL or SHARED
   resource — `policy-spawns` Rule 3 guards disjoint FILES, not shared external
   state.** Disjoint allowlists make parallel *writes* safe; they say nothing
   about a lock, a port, a fixture database, or a rate-limited API that every
   parallel subagent would grab at once. The canonical case: a briefing whose
   "Deliverable shape" says *run `pytest -k <x>`*. Dispatch three of those in
   parallel and the second and third hit `tests/_db_lock.py` (US-QA-002) and
   `pytest.exit` loudly — or, before that lock existed, silently drop each
   other's collections (lived session 2026-07-10: three briefings
   prescribed pytest, corrected mid-flight). Rule: **verification that takes a
   shared resource is the PARENT's job** — brief the spawn to run only
   resource-free checks (a template lint, `node --check`, `ruff`) and run the
   suite centrally once every spawn has returned. If a spawn genuinely must run
   the suite, give it its own `MONGO_DBNAME` in the briefing.

   **And the second half of that rule binds the PARENT: do not run pytest while ANYTHING is still editing the tree — a write-tier spawn, or the parent's own next edit.** A run that overlaps a live edit renders whatever is on disk and comes back a false GREEN.

   The DB lock cannot help — the collision is on the SOURCE, not the database. Cheap tell: **an open spawn file with `tier: write` and `status: open`.** The parent's verification window opens when the fan-out closes.

   **The parent-side face needs no spawn at all:** writing the story flip, the Log entry or the plan's surprises during a run makes its verdict evidence for a tree you are not committing. The order is edits → run → read → commit; nothing is written between launch and verdict.

   Second tell: **you are about to edit a file while a `pytest` background task shows `running`.** Third: **two tool calls in ONE message where one is a suite run** — parallel calls start together. One pytest per message, alone. (precedent)

   **A write-tier spawn that OWNS a file must be briefed load-modify-save ONLY — recovery is the PARENT's job, never the spawn's.** A spawn's improvised `git checkout --`/restore on its owned file silently wipes the PARENT's uncommitted work underneath. One briefing sentence prevents it:

   *"use load-modify-save on the EXISTING file only; never `git checkout`/ restore, never rebuild from a source artifact; if something goes wrong, STOP and report."*

   **And a spawn keeps its scripts under its own `scratchpad/<spawn-id>/`, never the shared scratchpad root** -- a helper named like a module (`ed.py`, `nt.py`) is overwritten by a sibling spawn, or shadows a stdlib module for the next script run from that directory.

   **And a spawn that edits a file by SCRIPT is briefed to read the whole file into memory first, write the result to a temp file beside it and replace -- never `open(p, 'w').write(convert(p))`, which empties the file before it is read.**

   The parent checks every allowlisted file's size when a spawn returns, before any other read of its work. (precedent)

   **A mechanical / multi-item spawn briefing must forbid NESTING explicitly —
   "for EACH item …" reads as an instruction to ORCHESTRATE, not to DO.** A
   Sonnet (or any) subagent handed a briefing that iterates over N items ("for
   each of es/fr/it, translate its worklist …") may interpret it as *dispatch a
   sub-agent per item* — spawning untracked grandchildren the parent has no ID
   for, whose output lands late or not at all (an orphaned nested fan-out). The
   fix is one sentence in the briefing: **"Do the work YOURSELF; do NOT use the
   Agent/Task tool; do NOT delegate to sub-agents — you personally read and write
   the files."** (lived session 2026-07-12: 2 of 3 multi-locale
   translators spawned grandchildren; the single-locale agent did not).
   Corollary: when you must fan a mechanical job across many items, prefer
   **single-item agents** (one locale each) — a single-item briefing has
   nothing to orchestrate — over a multi-item agent that is tempted to
   sub-orchestrate. **A spawn's tier follows where it WRITES, and 1.4 names it that way: translators that write one verdict file each OUTSIDE the repository are `advisory`, may all run at once, and the parent's `i18n_apply.py` is the only catalogue writer** -- a plan that calls them write-tier, three at a time, budgets a limit that guards nothing (lived session 2026-10-13: eleven ran in parallel against a plan that said three).

   **And when ONE locale is fanned across SEVERAL single-item chunks, pin the recurring judgment terms PER LOCALE in the dispatch prompt — the briefing stays verbatim; the locale line grows, and each pin is the word the catalogue's entries OUTSIDE the worklist use, counted, never one msgid's translation.**

   The terms are those the reply protocol's Q4 keeps surfacing (the VAT abbreviation, the dunning family, a tariff term like `Dignität`, a product noun like `Langzeit`): chunks choose them independently, and the applier cannot see a split. **And the briefing says what each placeholder HOLDS.**

   The parent settles the locale-level facts the same way (the sr script, counted from the catalogue — Cyrillic vs Latin) rather than letting each chunk decide.

   **And the briefing says the references can be WRONG** — they carry the catalogue's own mis-couplings (#522), so *when every reference disagrees with the msgid and its source path, trust the msgid*; the parent reviews the authored entries whose references sit in a shared-translation group. (precedent)

   **For UI work: name a lived reference surface to MIRROR EXACTLY — never
   hand-compose the spec from macro documentation.** A briefing that
   assembles a UI from macro rules ("use the premium select macro with
   its blank option", "wire range mode per the filter-bar pattern") encodes the
   PARENT's guesses, and the spawn builds them faithfully (lived
   session 2026-07-05: both hand-composed filter-zone choices
   overturned in the first verify round). The correct shape: *"mirror the
   filter row of the ledger page's template exactly, swapping only the
   field names"*. Macro rules constrain; a reference surface SPECIFIES.

   **A UI-spawn briefing that adds SIBLING or CHILD styling to an existing CSS
   class must NAME policy-frontend-conventions Rule 11(c) — the equal-specificity
   source-order tie-break.** A spawn styling a new variant of an existing class
   (an expansion child row, a modifier state) will naturally write a **bare**
   re-declaration of that class later in the file — which silently wins the
   source-order tie-break and re-styles EVERY instance, not just its variant
   (the compound-selector rule exists precisely for this). The parent knows the
   rule; the spawn does not unless the briefing says so. One sentence suffices:
   *"any override of an existing class scopes as a compound/descendant selector
   (`.group .row`), never a bare re-declaration — Rule 11(c)."* (lived
   session 2026-07-24: a bare `.csd-case` re-declaration
   stripped every top-level row's colour strip).

   **…but verify the reference's DATA contract before prescribing "mirror it" —
   not just its markup shape.** A reference surface specifies the *look*; it does
   NOT guarantee its *plumbing* is correct. Before a recipe tells N spawns to
   mirror surface X, confirm X's form-field names against the route that actually
   reads them (lived session 2026-07-10: the reference's
   `tag_ids[]` inputs vs the route's `getlist('tag_ids')` — a latent bug, T-041,
   propagated to five briefings). Grep the reference's `name="…"` against its
   save route's `get`/`getlist`/update-parser reads before writing "mirror it".

   **A briefing that asks the spawn to write PINS says: assert the SPEC, never the observed output.** A pin of "what renders now" passes by construction; name the ground truth it is written from — the retired hand config, the descriptor, the story's AC — so a pin can fail.

   **Forbidding the spawn to RUN the code does not close this: it still pins what it READS, and the branches with no spec row — a default, a fallback, an `else` — are where it does.** The briefing says such a branch is REPORTED as a surprise, never asserted.

   The parent reads every returned file for exactly those lines before the seam — the read is the gate, the briefing (and `scripts/probes/fallback_pins.py <files>`) only shrinks it — and the `#<n>` that replaces a `SURPRISE <n>` is the number `gh issue create` returned, never one predicted before the call.

   **And the parent RUNS every returned file before the seam, because a no-exec spawn cannot see its own SETUP fail:** a test whose seed call answers 400 passes vacuously on whatever it asserts next.

   So a test-writing briefing names, under *Files to sweep*, the fake and fixture libraries the tests must use (`tests/fakes/`, `tests/fixtures/`), names ONE existing test to copy each request payload from rather than compose it, and requires an assertion on every setup call's status.

   **The request under test is a setup too — a refusal or not-found expectation needs a control that its URL exists** (a sibling success on the same path, or the path read from the route's decorator), or a guessed URL passes on the wrong route's 404. (precedent)

5. **Write it to `.claude/sessions/spawns/<YYYY-MM-DD>-<slug>.md`**
   following `_TEMPLATE.md` with the
   Write tool, or N from one cluster list with `scripts/ops/spawn_brief.py`,
   which writes the scratch, Result, agent-type, fakes and row-rule lines
   itself; `check_spawn_briefings.py` holds them at the push. Fill `tier:`,
   `allowlist:`, `delivery:` frontmatter from steps 2 + the mechanism choice.

6. **Dispatch.** The default is **auto**:

   - **Auto (default) — Agent tool.** Call the Agent tool with
     `subagent_type: agora-spawn` (no Agent tool, so it cannot nest) and a lean prompt that points the
     subagent at the briefing file and tells it to write its own result:

     > Read `.claude/sessions/spawns/<file>.md` in full — it is your
     > complete briefing (Background · Files to sweep · Constraints ·
     > Deliverable shape · Reply protocol) and names your authorization
     > tier `<tier>`. Execute it. **Write your deliverable into the
     > `## Result` section of that same file** (replace the placeholder).
     > At `advisory` tier, the spawn file's `## Result` is the ONLY thing
     > you may write — everything else is read-only. At `write`/`commit`
     > tier, you may also touch the allowlisted paths (and, at `commit`,
     > commit them per the briefing). Then reply to me with the
     > reply-protocol summary — do NOT paste full file contents back.

     For long or parallel spawns, pass `run_in_background: true` (the
     harness notifies the parent on completion). For independent parallel
     spawns, issue multiple Agent calls in one message — but only if their
     allowlists are disjoint (policy-spawns Rule 3).

     **Match the spawn's MODEL to the task, not the session (cost
     discipline).** A subagent inherits the session model by default — so a
     high-tier session (Fable/Opus) dispatching a **mechanical** spawn
     (bulk translation via polib, large mechanical search, format
     conversion — work with no reasoning surface) runs that spawn at the
     expensive tier for no benefit. Pass a **cheaper `model:` override**
     (Haiku / Sonnet) on mechanical spawns; reserve the session tier for
     reasoning-heavy spawns (research, adversarial verify, design). Decide
     the model at dispatch as part of the tier decision (step 2) (lived
     session 2026-07-06: an 11-locale polib fan-out ran on Fable 5).
   - **Manual (opt-in) — copy-paste.** Surface the briefing as a
     copy-pasteable code block plus the spawn file path; the user runs it
     externally and pastes the output into `## Result`.

7. **Update the parent session's `Open threads`** with a link to the
   spawn file and a note: *"Spawn dispatched YYYY-MM-DD (tier: X,
   delivery: auto|manual) — return value feeds <which decision>."*

When the spawn returns (auto: the Agent tool result; manual: the pasted
output), `/agora` **folds the summary into the relevant Log entry as one
summary entry** (not a transcript) and flips the spawn file to
`status: returned`. **When the fold READS a `## Result` block
programmatically, anchor on the heading LINE (`^## Result$`, re.M) — never
the bare string:** the briefing's own Deliverable-shape prose mentions
`## Result` and its example block matches first, so a bare-string regex
harvests the EXAMPLE instead of the deliverable (lived
session 2026-08-23: the five-spawn merge read 1 key
instead of 432 — caught by checking the count against the worklist). In
**auto** mode the `## Result` block is already
written by the subagent — the parent reads it from disk, it does not
re-paste. In **manual** mode the user pastes `## Result`. Either way the
parent reviews what landed before relying on it (a `write`/`commit`
auto-spawn's edits go through the parent's commit-tree triage at `--end`,
per policy-spawns Rule 2 — `auto` delivery does NOT bypass that gate).

**Multi-iteration is normal** (~⅔ of real spawns iterate once). A
refinement round gets a new `## Iteration 2` heading in the same spawn
file — append-only; for an auto-spawn, re-dispatch the Agent tool with
the iteration's added briefing. **Tier escalation** (e.g. `write` →
`commit` after the user asks the spawn to ship) is a new iteration with
the new tier restated. Never rewrite an earlier iteration.

A spawn that takes a long time or never returns is a
`status: closed-without-result` entry in the spawn file — not a failure
of the parent session.

---

## MODE 5 — `--plaza` → moved to the `/plaza` skill

**Plaza was extracted into its own skill on 2026-06-19** (session 2026-06-19).
The freeform-workspace Plaza grew into a structured **7-stage self-improvement
pipeline** (Landscape paper → Background analysis → Idea harvest →
Traktandenliste → Feature plan → Change requests → Leveling) — a different
shape from the `/agora` session bracket, so it became its own pipeline.

**Use [`/plaza`](../plaza/SKILL.md) instead.** When the user types
`/agora --plaza` (or "open the plaza" / "skill board" / "improvement round"),
route to `/plaza`:

- `/plaza` (default) — run a self-improvement round (opens a recorded
  `type: plaza` captured session, runs the pipeline).
- `/plaza --status` — where the open round is.
- `/plaza --resume` — continue an open round.

For a quick ad-hoc look at the skill board *without* a round, `/level --board`
directly is still the right call (no pipeline needed). `/agora` no longer hosts
a Plaza mode of its own — it brackets work sessions; `/plaza` runs rounds.

The full Plaza model — the open-round guard, the 7 stages, the captured-session
record, and the close-out retro — now lives in
[`.claude/skills/plaza/SKILL.md`](../plaza/SKILL.md).

---

## Session types & shapes

The reference the start sequence uses in 1.2 + 1.4. A session's `type` is a
**label for the plan**, not a cage — the plan itself is reasoned from the goal
(1.4). The five base types:

```
pipeline   /new-story | /feature-plan  →  /implement-story  →  /iterate  →  /fixbug*
doctor     enumerate targets  →  /check-page | /check-ui-entity | /check-coverage
                                  | /selenium | /manage-translations | /wiki  (×N targets)
fix        /fixbug ×N   (from /iterate --feedback output, or the bugs collection)
meta       /inspect-pipeline  →  /learn | /document  (per finding)
mixed      multi-phase — see the shapes below
```

### Planning sessions — the plan is an artifact, not a conversation

The **other half** of the blind mode, and its precondition (US-AGORA-037). A
`mode: planning` session **produces a plan and builds nothing**; a `mode: blind`
session **executes one and composes nothing**. The pair is the user's named
backbone — *"focus on the planning to launch multiple sessions after each other"* —
and it only works if what the planning session emits can be **loaded**.

Until now it could not: a plan lived as conversation plus an Issue comment, so the
build session re-derived its own understanding of it. A blind run **cannot stop to
re-scope**, which makes loadability a correctness property rather than a
convenience.

So a planning session's deliverable is one or more entries in
[`PLANS.md`](../../sessions/PLANS.md) — the registry that is
[`THREADS.md`](../../sessions/THREADS.md)'s sibling:

```bash
flask agora plan --draft .claude/sessions/<this-session>.md   # skeleton + the gate's fields
```

**`git fetch` first and read `origin/main`'s `Next id` in the same minute as the
draft** -- ids are minted on `main` (the P-088 ruling), and a counter read at `--start`
is stale by the time `plan --draft` runs on a multi-machine day (lived session 2026-11-09:
P-089 reserved five hours after the fetch, renumbered to P-093); the mechanism, `plan
--draft` refusing a counter behind `origin/main`, is captured on #983.

Then write the seven fields as prose (they are parsed, never filled into a form), record the emitted
ids in the session's `plan_ref:`, and the plan is loadable the moment its gate is
complete. **Partial planning is first-class**: `part: N of M` splits an effort
across sessions — plan part 1 now, part 2 later — each part its own `P-NNN` block with
its own gate, so a later `--start` loads the part whose turn it is rather than
re-reading the whole effort.

A planning session that emits nothing loadable has not finished. That is the honest
test, and `flask agora plan` reports it as `incomplete` with the missing field named.

### Blind (autonomous) sessions — the user leaves, the plan runs

An **orthogonal mode**, not a base type: any type above can run **blind** — the user
signals they'll be away ("build it while I'm gone", "make this a blind session") and the
whole plan executes autonomously, ready for them to test on return. First run
session 2026-07-09: it worked — all the work landed, only
tweaking was left. **This is a deliberate direction** (real work starting when the user
isn't at the screen), grown **step by step**.

Because the 4-eye gates can't fire mid-run, a blind session **front-loads every gate
decision at `--start`**. Since US-AGORA-038 those decisions are **fields of a loaded
plan, not questions the agent must remember to ask**:

```bash
flask agora plan --load P-NNN     # the blind --start's opening move
```

The loader **refuses** (exit 2) a plan missing any of its seven gate fields, naming
what is absent — `parent · scope · done means · verified by · repo · autonomy ·
fan-out`. Four of those are the front-loaded gate itself:

1. **Scope** — how far the run goes (which stories; where it stops; explicitly what it does
   NOT do — e.g. no cut-over, no milestone).
2. **Repo state** — commit-on-branch / commit+push / leave-dirty; and **never** push / merge
   / tag / fire a Milestone unattended unless explicitly opted in.
3. **Mid-flight autonomy** — pre-authorize story reconciliation (`/update-story` on a split),
   reasonable build calls, and proceeding without asking.
4. **Inline-vs-spawn fan-out** — decide the spawn plan up front, exactly as the non-blind
   1.4 rule requires (`policy-spawns` Rule 1 + the "spawn fan-out is a session-PLAN decision"
   note). **The field is mandatory and never blank**: `inline — <why>` is a complete
   answer, silence is not (lived session 2026-07-09: the first
   blind run walked separable units inline because fan-out was not on the gate).

   **But the fan-out field answers EXECUTION, not AUTHORSHIP — they are two
   questions and the field can only answer one.** `inline — the run owns the
   machine` is a correct and complete answer about *who runs the thing*; it says
   nothing about *who writes it*, and reading one as covering the other is how a
   blind plan silently routes past a skill that owns the ground (lived
   session 2026-08-30: `inline — the run owns the machine`
   was true, and the detector was authored inline where `/selenium` owns it). A
   justification for bypassing the owning skill may exist — but **a justification
   unstated is a justification assumed** (`policy-skill-routing` Rule 1's
   one-phrase exception). So when the fan-out answer is `inline`, say which
   question it answers, and answer the other one out loud: *who authors this,
   and if not the skill that owns it, why not?*

The remaining three carry 037's **testing gate** (`done means` + `verified by` — a plan is
not loadable into a blind run until it declares what done looks like and how it will be
verified) and the structural parent. The gate is then fired **in prose** as a confirm-this-
loaded-scope (per the gate-shape rule), not as a multi-question dialog composing it fresh —
the fields already exist; what the user is nodding is *this plan, now*. Reserve
`AskUserQuestion` for a genuine either/or that the plan left open.

**A blind session EXECUTES a big plan — it does not compose one at the gate.** Its scope comes
from an artifact that already exists (a milestone Issue's game-plan, an RP + its stories, a
`/feature-plan` decomposition), and the `--start` gate *confirms* that scope rather than
inventing it. Do not bolt an extra topic onto the gate because it is nearby: a topic that
wasn't in the plan hasn't been sized, and the blind run cannot stop to re-scope it (lived
session 2026-07-10: the planned scope landed clean; T1, added at the gate, came
back two-thirds undone). Corollary: a blind session cannot be ended and restarted mid-run, so
a scope that would need a re-plan mid-run is simply the wrong scope for one — split it across
sessions (the over-scoped-phase rule) rather than betting on it. **Confirming is a diff, not a
read-back: the gate reads the plan's `parent:` Issue BODY whole — its rulings and its unticked
boxes — against the plan's `scope`, and names a member the body asks for and no plan carries.**
The plan's own words are what a planning session copied, so they cannot show what it dropped;
the member is not added (that is the bolt-on above) but homed — the next plan, or the Issue —
before the run starts (lived session 2026-10-29: #530's R4 flipped the 44
and "ruled the 11 partial ones one by one"; P-074 carried the first half, and the close found
the second).

**But adapting the planned METHOD to an audit finding is NOT a re-scope — it's correct
execution.** The scope (the *member / deliverable*) is fixed at the gate; the *method* bends to
what the opening audit reveals. When a blind session's audit-matrix step **invalidates the
premise of a planned method**, switch to a safer method that delivers the *same member* and
record it as a method-adaptation in the Log — do not force the invalidated method through, and
do not treat the switch as a re-scope needing a stop (lived session 2026-07-24:
the a11y macro-conversion spawns became one mechanical id-add script — same member). The tell
that it's a legitimate adaptation (not scope-creep): the deliverable and its acceptance are
unchanged; only *how* it's produced changed, driven by a finding the plan couldn't have known.

Then: **self-verification stands in for the user's browser-test** — run the app, drive the flows, write + run tests (respecting the one-pytest-owns-the-db lock), and run the full suite **as CI invokes it — bare `pytest`, never a list of tier directories: the directory ORDER is part of the suite**.

Never `-o addopts=""` — it un-deselects the headless-failing selenium tests and manufactures false failures — **and never `-x`: a blind run has no one to read the first red and re-launch, so `-x` hides every red behind the first and the re-run costs the whole suite again**.

**The record commit precedes the suite and the verdict rides a second one — the general rule, at 1.4 above.** Its blind-run half: **nothing in the tree is edited until the run reports** (a mid-run record edit IS read by it).

Park clean (Path B) with a **"here's exactly what to test" handoff** in the session file — a **numbered, walkable checklist is a first-class deliverable of the run, not a courtesy**: the user verifies the whole session in one pass on return; the session closes with the retro together. (precedent)

**The checklist is GENERATED and READ BACK — it is no longer written into the void
(US-AGORA-038).** Two call sites close the loop:

```bash
flask agora handoff --draft .claude/sessions/<this-session>.md   # seed it: one item per scope member
flask agora handoff                                              # the NEXT --start reads it back
```

Seed the numbered items from the loaded plan's scope members rather than composing them
at the end of a long run, then edit and extend. **The drafter seeds one item per scope
BULLET** — a plan whose `scope:` is one paragraph with a sub-bullet drafts a single item
quoting the caveat, not the members, and the checklist is composed by hand again (lived
twice, session 2026-09-26 · session 2026-09-26); a
planning session writes the members as a list, or the drafter learns to split a ` · `
paragraph — the mechanism is captured on #477. **Name the surface/path per step —
do NOT mint devlinks at the park**: the 300 s TTL means park-minted links are dead by
the return walk (the step-1.1 devlink rule); the attended walk's opening move mints
fresh links for the steps that want them. It lives under `## Handoff checklist` in the session file; the user ticks items as
they verify them. The **next** `--start` 1.1 surfaces everything still unchecked as open
work. That read-back is the whole point: the checklist was always a deliverable, but until
it had a reader, *nothing tracked which items the user actually cleared* — and it was the
one element of the blind pattern the user does not personally re-invoke, which is exactly
why it was the one element that never worked.

**A blind sweep's NAMED EXCEPTIONS are its first attended findings — list each one as a handoff RULING item, never as a footnote.** A completeness sweep's named exclusions read as decided, so the run parks proud of its coverage while the user's first clicks land on them.

Rule: an exception that is NOT a ruling (the sweep simply could not reach it) is a finding — a numbered handoff item with the class it belongs to — and the class's audit matrix runs BEFORE the park if the sweep's own grep can size it.

**An AMBIGUOUS scope wording is a ruling item too — the run executes its REVERSIBLE reading and parks the question, never the irreversible one.**

**A ruling item over a CLASS shows the class's census split BY KIND — a count and one example per kind — never one example for the whole class:** the user rules on what the item shows.

The handoff's "ruling wanted" items exist for the decisions; the exceptions belong beside them as "not reached". **And the park message asks for those rulings by their HANDOFF item numbers** — a second numbering turns the user's answer into a mapping exercise. (precedent)

**And a blind run's NEW premium surface is paired with a doctor pass in the
plan, as a spawn-built unit is** — see the 1.4 spawn-fan-out rule. A blind
build cannot ask "does this look premium?" mid-run; the doctor pass is how it
answers before the park instead of at the user's first click (lived
session 2026-08-25: the Matrix leaf's pagination +
jump row were return-round 1).

**And the pairing names EVERY HOST the unit ships on — one doctor target per host,
each a deliverable the blind run's own gate checks by name.** A component that
claims two hosts (a staff modal AND a portal page) needs its doctor pass on both;
the plan line that names both targets is an N-deliverables line, and in a blind run
there is no user at the phase gate to notice the second target was skipped — the
flip is the run's own act, so the run re-reads the line before flipping (lived
session 2026-08-29: Phase F named the staff hub AND the portal
page; the box flipped on the staff hub alone, and the portal picker sat inert). The doctor
pass was in the plan; it was the gate that dropped it.

**Carry the good half to NON-blind sessions too:** resolving the "obvious" questions **up
front** (scope, repo-state, fan-out) is valuable whether or not the user leaves — it removes
the mid-session re-litigation the `--start` plan exists to prevent. The blind mode just makes
front-loading *mandatory*; non-blind sessions should reach for it by default.

### Common session shapes

Real sessions are usually **multi-phase** — they cross type boundaries. These
are the recurring shapes; 1.4 reasons the actual plan, but starting from a
shape beats starting from a blank page.

- **Feature + rollout** — `/feature-plan` → `/new-story` ×N → `/implement-story`
  → ui tweaks (direct edits / `/fixbug`) → roll the new pattern out to sibling
  pages with `/check-page --finish` → `/wiki` to seed the feature. The single
  most common shape: build a thing, then make the rest of the app match it.
- **A doctor sweep** — pick a doctor, enumerate targets, walk them. "Roll the
  finished reference-hub structure across the other pages" is this:
  `/check-page <slug> --finish` ×N. No pipeline skills at all — the user
  explicitly called this out as a session that uses *only* doctor skills.
- **Health check / deep inspection** — a maintenance pass: `/check-coverage`
  + `/manage-translations` + `/wiki --audit` + `/inspect-pipeline` for a broad
  read, or one doctor's deep mode (`/wiki --surprises <slug>`,
  `/check-page <slug> --audit`) for a focused one. Output is a state-of-health
  report and a dispatch list, not shipped features.
- **Fix batch** — `/fixbug` ×N down a backlog (a prior `/iterate --feedback`
  triage, the bugs collection, a review's findings).
- **Meta** — working on Agora itself: `/inspect-pipeline` → `/learn` /
  `/document`. (This very session — building `/agora` — was one.)

`/agora --start` enumerates the concrete targets of whichever shape applies
into the **session plan**; the conversation walks them, ticking the checklist.

---

## Mode dispatch

Parse `$ARGUMENTS`:

| User says | Mode |
|-----------|------|
| (nothing) / `--start` / "start" / "begin a session" | **Mode 1** (start) — **prompt-less by default**: orient against the reconciled state, propose the way forward, user steers, co-author the prompt after (US-AGORA-026) |
| `--end` / "end" / "close the session" / "wrap up" | Mode 2 |
| `--end --rollover` / "roll over" / "close and start the next" | Mode 2 → Mode 1. **Not a distinct mode** since US-AGORA-035 — every `--end` writes the baton and every `--start` reads it, so continuing is just running Mode 1 next. The flag is accepted as a synonym for "and then open the next session". |
| `--status` / "status" / "where are we" | Mode 3 |
| `--spawn <description>` / "outsource this" / "spawn a side conversation" | Mode 4 |
| `--plaza` / "plaza" / "open the plaza" / "skill board" / "improvement workspace" | Mode 5 |

---

## Gate shape — prose recommendation-with-default is the default; AskUserQuestion is for clean separation only

The 4-eye gate has **two shapes**, and the default is **prose**, not the
`AskUserQuestion` dialog:

- **Prose recommendation-with-default (the DEFAULT).** State the recommended
  path in prose with the reasoning, then invite a nod-or-redirect in text
  (*"I'd do X because Y — nod, or redirect"*). This is the right shape for
  **every planning / discussion / "proceed or refine?" gate**: the `--start`
  plan-confirmation (1.4), goal placement (1.4), Milestone-targeting (1.4b),
  phase-completion (*"Phase X done — proceed to Y, or more under X?"*), the
  retro (2.6). These are *conversations* — the user reads the reasoning and
  often adds free-form feedback ("yes, and also Z"), which is half the value
  of the gate (`policy-four-eyes` Rule 5, bidirectional).

- **`AskUserQuestion` dialog (the EXCEPTION).** Use it ONLY for a **clean
  either/or separation** — a small set of genuinely mutually-exclusive options
  where side-by-side selection actually helps: *Shape A / B / C*, *fix-now via
  /fixbug vs defer*, *promote / park / cancel*, *accept-epithet / propose-
  alternative / cancel*. The naming ceremony and the regression confirmation
  are legitimate dialog cases.

**Every time relayed to the user is local and labelled** — in a gate, a status line or a wait estimate. GitHub, CI and log timestamps arrive in UTC; convert them to the machine's zone (`date` names it) and write the zone (`18:17 CEST`), never a bare `Z` the reader takes for their own clock and misreads by the offset (lived session 2026-09-15: `15:31Z` and "around 15:55Z" read against the user's 17:58).

**Why the default flipped to prose** (user retro, 2026-06-08, recurring — also
flagged 2026-06-07 as "AskUserQuestion-heavy"): the dialog box **visually
blocks the prose explanation** the agent just wrote, so the user can't read the
reasoning before being forced to pick; and it **shuts down the discussion** —
the user is reduced to selecting a preset option with no room for free-form
feedback. That's worst exactly in the `--start` discussion and mid-session
planning gates, where the reasoning and the user's feedback matter most. Prose
keeps the explanation readable and the conversation open. (Sessions normally
open with a prompt carrying the whole intention and rarely change it
mid-session — so the gates are mostly confirm-or-tweak, which prose serves
better than a picker.) `policy-four-eyes` Rule 2 already says *propose a
default, never just list options* — this is the **mechanism** clarification:
prose IS the default mechanism; the dialog is reserved for clean separation.

> **`--start` discussion-flow redesign — landed (US-AGORA-026).** The user had the
> `--start` discussion flow in focus for a future redesign (making the session
> opening more discussion-friendly). The AskUserQuestion→prose-default change was the
> first concrete step; the **prompt-less default** (MODE 1 intro + step 1.2's
> prompt-less path: orient → propose → user steers → co-author the prompt) is the
> rework itself. Together they make `--start` a discussion that *initiates first and
> steers second*, rather than a paragraph composed cold up front.

## Principles

- **Lightweight is the design constraint.** `/agora` plans, routes, records, reflects;
  the moment it starts *doing* the queued skills' work it has overreached.
- **`--start` and `--end` both triage commits** — a session opens clean and closes
  clean (`policy-commit-discipline` Rule 5); the push + CI-green ceremony is gated on
  Milestone reach (2.2 Path A), never on every `--end`.
- **The Milestone is the ceremony, not the session.** Sessions may park without firing
  one; a recurring CI fix becomes a `/document --policy` candidate.
- **`/agora` is the driver — it stays current by reading, not remembering.** 1.1
  re-inventories `.claude/` and the product backlog every start; stale self-knowledge
  is a 2.4 self-audit finding.
- **`--end` is where Agora learns about itself — `/agora` included.** 2.4–2.6 audit
  the session with the orchestrator in scope and dispatch the findings; a session that
  skips `--end` loses the loop.
- **The phase gate fires between phases; the session file is git-tracked.** The
  standing instructions at the end of MODE 1 and `.claude/sessions/README.md` are the
  rules — this list only names them.

## Initialisation

**What this skill reads before acting** (US-AGORA-041): MODE 1's step 1.1 IS
the initialisation — the baton (pointer-verified), `reconcile`, `state-check`,
the frontmatter lint, `env`, the planned-session registry, THREADS whole, the
skill-system inventory and the product backlog; MODE 2's is
`flask agora retro-context` (2.0). The orchestrator never opens or closes on
a remembered picture — every bracket starts from the reconciled state.

**Self-model:** the session bracket — Agora's centre. It plans, routes,
records and reflects; it never does the queued skills' work. When a bracket
surfaces a context gap (a state file it should have read, a pointer it
trusted unverified), the gap lands as a 🟡 journal stub in
[`experience.md`](experience.md) — the journal-at-source channel — so 2.3b
grades it and the contract improves.

## Claims at this level

The invariants other skills and the user depend on `/agora` to hold (the
`hardened`-tier commitments). Each is the unit `/learn` checks for contradiction
per `policy-skill-progression` Rule 4.

1. **Sessions open and close clean.** Every session opens and closes through the
   commit-tree triage; the working tree is clean at both boundaries. No
   uncommitted work spans a session boundary (`policy-commit-discipline` Rule 5).
2. **A Milestone fires only behind the criterion gate.** `/agora` tags + pushes a
   Milestone only after a line-by-line read of the Goal's success criteria,
   confirmed per-criterion at a 4-eye gate — never on "the work feels done".
3. **Skill usage is never undercounted.** Every closed session reconciles
   `skills_invoked:` from the Log — including agora-internal `/level`,
   `/inspect-pipeline`, and `/learn` dispatches — so M1 and XP reflect what
   actually ran.
4. **Work routes to skills; inline is a logged exception.** `/agora` routes
   matching work to the skill that owns it by default, and records every
   inline-where-a-skill-exists as a missed-routing finding — the win condition of
   the leveling game (`policy-skill-routing`).
5. **The session file is a current, shareable record.** The session file is kept
   current (Log entry before checkbox flip) and git-tracked — it is the
   between-agents, between-machines record other sessions rely on, never a stub or
   a transcript.
