# Agora events catalog

The **transitions** layer, sibling to [`COMPASS.md`](COMPASS.md) (the *state*
layer — Vision / Mission / Goals). An **event** is a fixed thing that *fires* at
a session boundary; `/agora` only needs to **detect** that an event is firing and
**follow its chapter** here. Extracting the ceremonies into improvable chapters
(WS3, US-AGORA-012 /
RP-AGORA-003) makes each one a tangible, versionable artifact — and answers
"what milestone are we focusing on" by giving the ceremony a name and a home.

**Each chapter has four parts:** `Trigger` (what fires it) · `Preconditions`
(what must hold first) · `Script` (the steps, in order) · `Output` (what is
recorded). `/agora --end` step 2.2 does the *detection* (which event is firing,
behind the criterion 4-eye gate); the chapter does the *ceremony*.

**Behaviour is identical to the pre-extraction inline steps** — this is
documentation-extraction + indirection, not a redesign (the explicit WS3
constraint). When a ceremony needs to improve, edit the chapter here; `/agora`
is untouched.

**Four chapters today** — `Milestone-reached`, `Session-park`, `New Era`
(US-AGORA-016), and `Arc-open`/`Arc-close` (US-AGORA-042). Further chapters
(`Mission-cycle-open`, `Goal-Backlog→Active`, `Goal-closure`) are *additive* —
added when a real need surfaces, never pre-abstracted. The `policy-four-eyes`
transition **gates** are NOT events (a gate is not a ceremony) — do not move
them here.

**Rituals and habits (US-AGORA-042 — the carrier decision).** A **ritual is
what an event does** — the chapters below ARE the ritual catalogue, each
movement naming where it fires; there is deliberately **no separate Rituals
file** (one vocabulary, one home). The **`## Habits`** section at the file's
end carries the third category — recurring *practices* (not boundary
ceremonies, not rules of engagement) — so this one file answers "how does
Agora perform X" for both categories, with the section boundary keeping them
distinct.

**The event hierarchy.** A `Milestone-reached` closes one **Goal**; a `New Era`
closes one **Era** (a themed chapter of Goals). New Era is the Era-level analogue
of the Haleluja — bigger, rarer, and bracketed by a retro + a landscape snapshot +
a hand-off to the next Era. It fires only after every Goal in the current Era has
reached its Milestone.

---

## Event: `Milestone-reached` (Path A — the Haleluja ceremony)

**Trigger.** `/agora --end` step 2.2 reads the session's `milestone_target:` and
confirms — via the line-by-line criterion 4-eye gate — that **all** of a Goal's
`Success criteria:` in COMPASS.md are met.

**Milestone v2 — may span multiple Goals (US-AGORA-019).** A Milestone is a
first-class, always-planned tracking object (its own `agora:type:milestone` Issue +
template), not merely the closing tag. It may span **several** Goals/sub-goals — it
fires when **all its spanned Goals** close, not just one. **Behaviour-preserving:** a
single-Goal Milestone fires exactly as before (the tag, the ceremony, the Haleluja
are unchanged); the object just *also* supports a multi-Goal span. Everywhere this
chapter says "the Goal", read "the Goal(s) the Milestone spans".

**This is a DEDICATED section of `--end` — it does NOT end at Haleluja.** The
milestone path runs the ceremony below AND THEN always flows back through `--end`
2.3 → **2.3b (XP grading)** → 2.4–2.8 before `## Close-out`. See Step 10 — the
XP-grading step is the one that gets skipped when a milestone fires at session-close
(the lived BP-3 bug US-AGORA-019 fixes by making this hand-back explicit).

**Preconditions.**
- The criterion read is line-by-line, not "the work feels done" — every `- [ ]`
  in the Goal's `Success criteria:` is decided concretely with a citing commit/
  artifact. If any remains open, this event does **not** fire today; the
  `Sub-milestone` variant may (see the variant note below).
- The user has confirmed the closure decision (the 4-eye gate at 2.2 — Milestone
  firing is irreversible-ish: push + annotated tag).

**Script.**

**Step 1 — Milestone retrospective (runs FIRST, before any irreversible step).**
One retro per Milestone fired — when two Milestones fire in one session (lived
precedent: session 2026-05-23 fired
`milestone-drift-sweep-tooling` + `milestone-report-premium`), run two retros
back-to-back, each Goal-scoped to its own Milestone. **Path A only** — `Session-park`
does not fire the milestone retro, only the session retro at `--end` 2.6.

Three prompts per Milestone, Goal-scoped (the *release-retro* analogue distinct
from 2.6's *sprint-retro* session-scoped retro):

1. **What does closing this Goal change?** — the durable lesson the Milestone
   codifies. This is the IMPROVEMENTS.md material.
2. **What was hardest about this Goal?** — friction, decisions reversed, blockers
   chewed through. The lesson for *next* multi-session Goal.
3. **What should the next Goal in this Mission cycle look like?** — what's freed
   up now. Planning surface for the next `--start`.

Write the answers verbatim (lightly edited for clarity, not summarized) into a
new `### Milestone retrospective — <milestone-slug>` section under Close-out,
**above** the existing `### Retrospective` block. When two Milestones fire, two
`### Milestone retrospective — <slug>` sections appear back-to-back in firing
order. The header is inserted at run time, not pre-drawn in `_TEMPLATE.md` (the
comment-only placeholder there avoids template-stickiness drift — IMPROVEMENTS.md
2026-05-23 (d) Finding 4a). Discipline added 2026-05-23 by
US-AGORA-005.

The retro-before-irreversible-step placement is deliberate per
[`policy-four-eyes`](../policies/policy-four-eyes.md) Rule 5 (bidirectional gate):
a *"wait, the 4th criterion isn't actually met — abort and convert to a
sub-milestone"* finding has a clean abort path here, before the tag + push fires.

After the milestone retro(s), the mechanical ceremony sequence:

**Step 2 — `flask agora regen`.** Refresh every derived artefact in DAG order (one declaration,
`scripts/checks/derived_artefacts.yaml`, US-AGORA-096) and commit the refresh
(`chore(stats): regenerate after milestone <slug>`). **Regenerate on the COMMITTED tree** — commit
the code first, `git stash -u` the records, then run it: the stats collector counts `flask agora`
mentions across `.claude/sessions/*.md`, so an uncommitted record shifts counts CI's clean checkout
never sees (lived as three refusals in one ceremony, session 2026-09-04; #456).

**Step 3 — Close-gate preflight (BEFORE push).** Run the same checks CI runs,
locally — refuse to suggest the push if any fail. Bundle any fixes into the
in-flight commits (not as follow-ups). The cost of skipping this step is the
**fix-push-re-watch loop**; running locally first is the **fix-once-push-clean**
path. (The `scripts/git_hooks/pre-push` hook now *enforces* this same checklist
on every push — WS5/US-AGORA-014; the preflight here is the belt-and-suspenders.)
**For a PR-only batch** (CI declared *Test + Build on the PR only*), **the LAST session runs
`flask agora ci-local` before the PR push** (US-AGORA-091: CI's Test job under CI's conditions —
the workflow's pytest line, `-x` stripped, `TZ=UTC`, the `suite` field bound to HEAD; `--job lint`
for the Lint job's Flask-free scripts) — otherwise a multi-session branch meets the
suite for the first time at its PR. B8's ~140 commits reded three times from pin-green seams
(a C6 resolver, two loop inputs without a bound id, a second lockstep pin), ~45 min per
red-fix-rewatch loop, where one 38-minute local run would have caught all three
(session 2026-09-04). **And once the session record is committed
on the branch before the PR** (so the squash carries the Log), the LIVE-TREE tests run
once more — the record commit changes what the collector and the registry checks read:
the adoption surface, the prose ratchet's baseline, record consistency, `state-check`
(lived session 2026-09-05: a below-threshold pin flipped between the local
full run and CI because the third mention of a mechanism arrived with the session file
itself — one 55-minute loop). The `live_tree` marker that makes this one command is
captured; until it lands, name the files: `tests/unit/test_stats_collector.py -k Live`,
`test_check_prose_mass.py -k Live`, `test_check_record_consistency.py -k live`,
`tests/cli/test_agora_state.py -k "real_repo or CliSmoke"` *(corrected 2026-09-16 at session 2026-09-16: the path this line carried, `tests/cli/test_agora_readers.py -k real_repo`, selects NOTHING today — `33 deselected, 0 selected`, exit 0 — so the gate was skipped while the command looked like it fired. A checklist that names a test by path degrades silently when the test moves; read the SELECTION COUNT, not the exit code)*.

```bash
flask agora preflight                # runs the hook's OWN check list, read-only
# optional smoke for the changed surface:
# pytest tests/smoke/ -x
```

**There is deliberately no checklist here to keep in sync (#289).**
`flask agora preflight` executes `scripts/git_hooks/pre-push --dry-run` — the
same script, the same list, nothing regenerated and nothing staged. That is the
*only* reason the manual gate and the enforced gate cannot diverge; an
enumerated list here would be a second copy, and a second copy drifts.

It drifted twice, one session apart, which is why the prose tier was abandoned.
session 2026-07-31: the manual preflight ran four checks,
the translation guard was not on the documented list, and the push aborted on 20
protected-path fuzzies a template rewrite's occurrence renumbering had
re-attributed into another page's templates. The lesson was then written
here as prose — *"this checklist must match the pre-push hook's FULL mirror"* —
and broken again the very next session, session 2026-08-01: 5 of 9
checks run by hand, with `validate_templates.py` among the four skipped, which
had caught a nested Jinja comment that would have leaked prose onto the page.
Both times the guard itself worked exactly as designed. What failed was asking
a human or an agent to re-derive a script list by hand.

If a check fails: fix it as a working-tree change, loop back through the
commit-tree triage (`--end` 2.1) to commit (or amend the last commit — judgment
call), then re-run the preflight. The preflight is the **last 4-eye gate before
pushing**.

**Step 4 — Push** the session's commits (confirm with the user — pushing is the
separate explicit step the commit-tree triage defers to here).

> **stats↔tag race — ordering (a) is CANONICAL, push the tag WITH the commit.**
> `check_stats.py` counts `milestone-*` tags, so the stats refresh and the tag
> must reach origin **together** or CI's fresh checkout sees a tag count that
> doesn't match the committed `stats.yaml` → `check_stats.py --check` stale →
> red. This has now reded `main` at **multiple** milestone pushes (2026-05-31,
> again at 2026-06-21 §2) *despite* the `--follow-tags` note existing — because
> the default Step ORDER (stats at Step 2, tag at Step 6, pushed separately) IS
> the racy in-between path. So the canonical sequence is **ordering (a), not an
> option**: create the annotated `git tag -a milestone-<slug>` **FIRST** (before
> the Step 2 stats dump, so stats counts it) → `flask stats dump` → commit the
> stats refresh → **`git push --follow-tags`** (commit + tag land in ONE push).
> Step 6 below then only *authors* the tag message if you deferred it — it does
> NOT push a second time. (Ordering (b) — stats dumped before the tag exists, so
> the milestone count lags one session — is the only acceptable alternative, and
> only when you deliberately accept stats trailing reality. Never the in-between.)
> The pre-push hook does **not** catch this (its regen still counts the local tag).
> Lived: 2026-05-31 cost a whole session (session 2026-06-01);
> 2026-06-21 §2 reded again → this canonical-ordering rewrite (session 2026-06-22).

**Step 4.5 — Assert remote coherence BEFORE watching CI (the hard gate).** The
race recurred because nothing *verified* the tag actually reached origin before
CI ran on the pushed tree. After the push, assert it — refuse to watch CI until
the remote tree is what CI will check out:

```bash
# The milestone tag MUST be on origin (when stats counted it — ordering (a)):
git ls-remote --tags origin "milestone-<slug>"   # must print the tag; empty = race, push it now
# And the pushed HEAD must carry fresh stats (CI re-runs this on a clean checkout):
git fetch origin && git stash && python scripts/checks/check_stats.py; git stash pop 2>/dev/null || true
```

If `git ls-remote` returns empty, the tag is local-only — `git push origin
milestone-<slug>` (or re-push with `--follow-tags`) **before** Step 5. This
assertion is what turns the "two safe orderings" guidance into an *enforced*
invariant: CI never watches a tree whose tag/stats the remote doesn't yet have.

**Step 5 — Watch CI** — `gh run watch` (or `gh run list --limit 3` + `gh run view`).
If red, fix it: a CI fix is a real commit, loops back through the commit-tree
triage (2.1), gets pushed, CI re-watched, until green. Log every CI fix. **A CI
failure that the local preflight could have caught is a finding** — the preflight
is missing a check the CI runs. Recurring failures are `/document --policy`
candidates.

**Step 6 — Tag the Milestone** — annotated tag carrying the closed criteria:

```
git tag -a milestone-<slug> -m "$(cat <<'EOF'
<Goal name> — success criteria met:
- <criterion 1>
- <criterion 2>
- ...
EOF
)"
git push origin milestone-<slug>   # skip if already pushed via `--follow-tags` at Step 4
```

If you took ordering **(a)** above (tag created before the stats dump, pushed with
`git push --follow-tags` at Step 4), the tag is already on origin — only the
`git tag -a` authoring happens here, not a second push.

**Step 7 — Update COMPASS.md** — **first tick the closed criterion(s)**, then
move the Goal. **Writers (US-AGORA-113):** `flask agora write compass-tick --goal <n>
--criterion <k> --cite <session>` per closing criterion, then
`flask agora write compass-close --goal <n> --tag milestone-<slug>` -- it refuses an unticked criterion, a tag
the entry does not declare and a tag not yet in git, and moves the entry newest-first in the
closed entries' shape; the Era sweep (c) stays judgment. The criterion read at `--end` 2.2 already named exactly which
`Success criteria:` line(s) this Milestone closes — flip each from `- [ ]` to
`- [x]` in COMPASS.md with the closing date + session cite, in the same edit
that moves the Goal to "Goals (closed)" — in `COMPASS-closed.md` since US-AGORA-067
(COMPASS.md keeps the heading as a pointer). **Don't skip the tick because the
Goal is being moved anyway** — a half-ticked criteria list is the drift this
step exists to prevent (see the Sub-milestone note below for the lived case).

The move is **three surfaces, and the CLOSING Goal's own entry is the first of
them**: (a) every closing criterion ticked with citation, (b) the whole Goal
block relocated to "Goals (closed)" in `COMPASS-closed.md` with its `*(closed <date>)*` heading +
`**Milestone:**` + `**Status:**` lines, (c) the **Era chapter swept** for stale
claims about this Goal (its "Goals inside" line, the scope-guard prose, "when
it's finished"). Updating a *sibling* Goal's criterion is NOT this step — lived
session 2026-07-28: the ceremony ticked #130's mini-hub criterion
(correct, a genuine sibling effect) and never touched closing-Goal #237's own
entry, which sat active-with-unticked-criteria until the next `--start`'s
reconcile caught it. **The step ends with its own verification call —
`flask agora reconcile` must report clean BEFORE the ceremony's close-out
commit.** A drift it reports is fixed now, in this ceremony, not surfaced to
the next session. The mechanism shipped (US-AGORA-048, closing #251):
reconcile's `closed-with-open-criteria` check flags any Goal sitting in
"Goals (closed)" with unticked `- [ ]` boxes — the half-executed Step-7 shape
(#237's lived case, and #184's, found by the check's own first run). `[x]`
and the deliberately-partial `[~]` both count as resolved.

**Step 7b — the record reads the tag (US-AGORA-056, `AGORA-DECL §2`).** After
the tag is pushed, ONE call performs the three record writes the tag makes
true — the live-log line carrying the tag flips ✅ (any round below the live
log), the implementation plan's `**Status:**` flips to `done` — **only the plan the tag
CLOSES: `--plan` is passed when every story it names has shipped, so a phase or batch tag
under the round's one umbrella plan records `--pr <n> --tag …` and leaves the plan to the
round's last tag** (the writer refuses the flip otherwise; lived
session 2026-11-04: copied from the Phase 1 PR session) — and, when the
tag closes a round, the round's entry moves below `## Archive`:

```bash
flask agora write milestone-record --tag milestone-<slug> --plan <plan-slug>              # a phase tag that closes its own plan
flask agora write milestone-record --pr <n> --tag milestone-<slug>                          # a phase / batch tag under the round's umbrella plan: no --plan
flask agora write milestone-record --tag milestone-<slug> --plan <plan-slug> --archive "Improvements <N>"   # the round's last tag
flask agora write milestone-record --tag milestone-<slug> --plan <plan-slug>              # a Goal / batch tag: COMPASS carries it, the live log is skipped
flask agora write improvement --archive-stale                                              # then: every live-log round whose tags have ALL fired -- ⏳ tag lines flipped, entry archived (US-AGORA-079)
```

Each step refuses on its own anchor (a tag git does not know, or one neither the
live log nor COMPASS names, refuses the whole call) and every refusal is reported
at this gate, not at the next landscape. Since US-AGORA-082 the call records **every
tag kind** — a Goal tag resolves against its closed COMPASS entry, a batch tag
against the ticked criterion that carries it — and **refuses without a green
`suite` Evidence field** on the open session (T001: the tree being tagged proved
green by the seam, never by memory); `--late` records a tag whose ceremony ran in an
earlier session. The
command is the step; this paragraph is the pointer. `--archive-stale` follows it
(US-AGORA-079): the ledger's stale rounds are found by reading `git tag`, never by
remembering which round closed -- round 6's entry sat in the live log 78 days. Since US-AGORA-062 the same
call also writes `milestone <tag> fired` into the open session's `## Evidence`
block — the field the close's shape call reads (`AGORA-DECL §5`). Why it exists: `write
live-log` shipped in US-AGORA-048 and no step called it, so round 6's two ⏳
lines outlived both of its tags by three weeks — *a write with no reader is a
remembered write.*

**Step 8 — Close the GH Goal mirror Issue.** A closed Goal's GH mirror
(`**GH mirror:** #<n>`) is closed with a citing comment. This is part of the
GH-issue-closing pass (`--end` step 2.8b) — surface it there with the completed
sub-goal Issues so the user nods on one list, then
`gh issue close <n> --comment "Closed by milestone-<slug> (<closing session>). Criteria met: …"`.

**Step 9 — 🎉 Haleluja — ANNOUNCE THE TIER (US-AGORA-042).** Announce the
Milestone explicitly in the close-out, AND its scale — seven tiers deserve
more than one celebration size, so the announcement carries information about
what was achieved (the StatQuest principle). The MECHANICS are unchanged —
stats dump, tag, push, CI-green, COMPASS move, Issue close all behave exactly
as before; only the announcement scales:

| What closed | The announcement |
|---|---|
| Sub-milestone (a criterion/batch; the Goal stays open) | 🔩 the SMALL Haleluja |
| Milestone, single-Goal | 🎉 the Haleluja |
| Milestone spanning several Goals | 🎉🎉 the double — name every Goal it closes |
| Era close | 🏛️ the New Era event — the biggest; its own chapter below |

**Step 10 — XP grading is MANDATORY (the milestone path does NOT end at Haleluja).**
The push + green + tag + Haleluja *feels* like the end — it is NOT. Control returns
to `--end` 2.3 → **2.3b (evaluate the unrated journal → award XP)** and onward through
2.4–2.8. **2.3b is the step that gets skipped when a milestone fires in the same
`--end` as session-close** — the lived BP-3 bug (US-AGORA-019). The milestone-ending
is a *dedicated section* of `--end` that **always** flows through the 2.3b XP-grading
4-eye gate before `## Close-out`; a milestone `--end` that reaches Close-out with no
XP grading is **incomplete**, not done. (Set semantics still apply — one M1 per skill
per session; the milestone ceremony's own `### Step <X.Y>` dispatches are reconciled
into `skills_invoked:` at 2.3 like any other.)

**On a PR-merged Milestone, the post-merge records land on `main` — never on
the spent feature branch.** Once the PR squash-merges, the feature branch is
history: the records 2.3→2.8 still produce (XP grades, learn patches, the
session file's Close-out fill, stats) committed there reach the remote branch
but never `main`, and the next session branches off `main` without them.
Lived: B3's five trailing close-out commits sat branch-only until the user
spotted GitHub's "recent pushes" banner at the session 2026-07-29
`--start`; fixed by cherry-pick. So the moment the merge lands and BEFORE
control returns to 2.3: `git checkout main && git pull`, land the remaining
close-out records on `main` directly (they are records — the branch
discipline that created the feature branch is already satisfied), and delete
the merged branch in the same breath (`git branch -d` + `git push origin
--delete`) so nothing more can land there by inertia. **The session record is dirty by construction at this moment — the Evidence writer appends a field at every seam, so the file is never clean when the merge lands — which makes stash-carry the DEFAULT move, not the exception:** `git stash push -- .claude/sessions/<session>.md` · `git checkout main` · `git pull --ff-only` · `git stash pop` (lived session 2026-09-06: the checkout refused on exactly that file, one round)

**Step 11 — produce the next Milestone's game-plan (the rollover).** Ending a
Milestone always sets up the next one — the fractal skeleton's **slot 5 → next slot 2**
(US-AGORA-017). Name the next Milestone, draft its game-plan, and (for a multi-Goal
effort) open it as an `agora:type:milestone` Issue set in-progress, its plan living in
the Issue (US-AGORA-019 + US-AGORA-021). A Milestone closing with no successor planned
is the boundary-drift between efforts this step prevents. (If the Goal's Era is also
ending, this rolls up into the `New Era` event instead — see that chapter.)

**Output.** Record the final green run id, the milestone tag, and the push in
**Close-out → Milestone outcome**; confirm the 2.3b XP grading ran and the next
Milestone's game-plan is set.

### Variant: `Sub-milestone` (partial close)

When 2+ criteria are closed AND the remaining criteria genuinely belong to a
separate session (not "the last 5% of this work") AND the user agrees (ask via
`AskUserQuestion` if not stated): fire a `milestone-<sub-slug>` annotated tag
recording the partial close in COMPASS.md **without retiring the Goal**. Same
Steps 2–6/9 shape, scoped to the sub-slug; the Goal stays in "Goals (active)"
with the closed criteria annotated. **Tick the just-closed criterion's
checkbox** (`- [ ]` → `- [x]`, with date + session cite) — the Step-7
criterion-tick applies to the sub-milestone too, even though the Goal isn't
moved. This is the **exact drift F2 caught (2026-06-13)**: `milestone-data-hub-dashboard`
fired as a Phase-3 sub-milestone but Goal #39's Phase-3 checkbox sat `- [ ]`
unchecked for a session, because the sub-milestone path moves nothing and the
tick was implicit. The tick is now explicit here. History: added 2026-05-17
after an early session nearly fired
a reference-quality milestone with 2/3 criteria closed; criterion-tick
step added 2026-06-13 (session 2026-06-13 F2).
**The announcement is the SMALL Haleluja** (🔩 — Step 9's tier table): a
criterion closed and the Goal stays open; the celebration says so.

---

## Event: `Session-park` (Path B — no Milestone reached)

**Trigger.** `/agora --end` step 2.2 determines the targeted Milestone's criteria
are **not** all met (or `milestone_target:` was `none — exploration`).

**Preconditions.** The session's sub-goal work is committed (the commit-tree
triage at `--end` 2.1 ran).

**Script.**

1. Confirm the commit-tree triage (2.1) staged all sub-goal work.
2. **Push is optional** — ask the user. No CI gate. If pushed, log the run id but
   don't wait on green; if it later fails, it's a finding for the next `--start`.
3. Record what advanced toward the Goal (which success criteria are now met,
   which remain) in **Close-out → Milestone outcome**.
4. **Leave the dirty-by-design tail, take it at the close.** The evidence fields a
   seam writes AFTER its own preflight (`commit <sha>` · `gate … clean`) and the
   journal stubs land in the open session file behind the last record commit —
   the park's tree is clean *except* for that tail, by design, and the `--end`
   close commit is what carries it (the term's structural home; incorporated
   2026-09-26 at 10 of the newest 30 sessions).

**Output.** Close-out → Milestone outcome names which criteria advanced and which
remain. No tag, no Haleluja, no CI gate — the session parks clean, its record tail
riding the close.

---

## Event: `PR-merged` (the batch or Goal PR lands on `main` — US-AGORA-093)

**Trigger.** A pull request into `main` is merged — a batch PR on a PR-only Goal (the
`**CI:**` line says *Test + Build on the PR only*), a Goal PR, a Dependabot bump. The PR is
the unit the Era ships by (landscape v6: six tags against twelve batch PRs); a merge with no
tag of its own is still this event, and a merge that fires a tag is this event AND
`Milestone-reached`'s Steps 6–11 on the squash commit.

**Preconditions — the green read on the head sha.**

<!-- rc:green-read -->
A green read names what it covers. The PR's Test job proves the PR's HEAD sha and nothing
else, so it is read on that sha: `gh run list --branch <head> --json headSha,status,conclusion`,
filtered on the sha and never trimmed. The job runs `-x`: a red conclusion proves the suite up
to its first red and nothing after it, a green one proves the whole suite. `flask agora ci-local`
is the local twin; its `suite <passed>/<failed> ci-local@<sha>` field covers exactly the sha it
names. `flask agora write milestone-record --pr <n>` refuses a merge no green read covers
(US-AGORA-093).
<!-- /rc:green-read -->

The PR session meets it before the push with `flask agora ci-local` (the full suite, `-x`
stripped, `--job lint` for the Flask-free Lint job — `Milestone-reached` Step 3), and reads the
PR's own run on the head sha before the merge.

**Script.**

1. **The green read** on the PR's head sha (above). `gh pr checks <n>` lists every check;
   `gh run list --branch <head> --json headSha,status,conclusion,workflowName` filtered on the
   sha gives the explicit conclusions. A run on an older head is not a read of this one
   (`/agora` 1.3).
2. **Merge** — `gh pr merge <n> --squash` (plain; never `--auto` on a repo without auto-merge,
   which merges at once over a pending job). Commit or stash the session record first; the
   `--delete-branch` checkout aborts on a dirty tree (`Milestone-reached`'s fourth trap).
3. **The record step** — `flask agora write milestone-record --pr <n> [--tag <tag>] [--plan <plan>]`:
   reads the PR (merged · into `main` · its merge and head shas), refuses a merge no green read
   covers (`--late` when the merge was an earlier session's), re-reads every closing reference
   and names one GitHub left open, flips the plan, and writes `pr <n> merged <sha>`; with `--tag`
   it also runs the tag's own record (the tag fires on the squash).
4. **The tag**, when this merge closes a batch's or a Goal's criteria — `Milestone-reached`
   Steps 6–7b on the squash commit, never on a branch commit the squash strands.
5. **The Issue closes** the record step named as still open — `--end` 2.8b's gate, each with a
   citing comment (the session, the PR, the squash sha).

**The squash rule.** A squash-merge leaves the branch's commits unreachable from `main`; the
record's branch shas stay valid because they are listed by the PR's commit list, which
`retro-context` and `baton` read so (US-AGORA-085) — a branch sha is `squashed`, never
`stranded`, when its PR carries it.

**Output.** The `pr <n> merged <sha>` field in the session's Evidence block; the plan flipped;
every closing reference CLOSED or named for 2.8b; the tag (if any) recorded.

---

## Event: `New Era` (the Era-level Haleluja — close a chapter, open the next)

**Trigger.** **`flask agora era-close`** (US-AGORA-090 — R2 of 2026-10-14 made a
command the trigger, decoupling it from the last Goal): the runner walks the Era
Close playbook (`era-close-playbook.yaml`,
fourteen steps — board read · Issues homed · ledgers emptied · repository ·
catalogue · `ci-local` · coverage · wiki · translation · Selenium · finisher hunt ·
reports · the detector ceiling · Movements 1–2), records each step's verdict in the
closing session, and stops at the first red or unruled gate; `New Era` fires when
the walk reads every step green or ruled. `--dry-run` reads where the Era stands
without writing. The Era-level analogue of `Milestone-reached`: a Milestone closes
a Goal; New Era closes a chapter of Goals.

**Preconditions.**
- Every Goal listed under the Era's **Goals inside** has moved to "Goals (closed)"
  in COMPASS-closed.md (each behind its own `Milestone-reached` criterion gate).
- The user has confirmed the Era is genuinely finished — this is a **4-eye gate**
  per [`policy-four-eyes`](../policies/policy-four-eyes.md) (closing an Era is a
  durable, outward state change). An Era with a still-open follow-up in its
  backlog (slot 1) that belongs to *this* chapter does **not** close — the
  follow-up either ships first or is explicitly re-parented / dropped (the
  shoulder-glance, US-AGORA-020).

**Script.** Three movements (RP-AGORA-004 T1):

**Movement 1 — finish the old Era.** The retrospective + state snapshot, before
anything is written as closed. This is the Era-boundary
[shoulder-glance](../policies/policy-shoulder-glance.md) — both halves: **catch**
(steps 3 + 5 surface what shipped + sweep the backlog so nothing is abandoned) and
**close** (steps 1 + 2 + 6 retro + version + name the theme):

1. **Era retro** (Era-scoped, distinct from the session retro at `--end` 2.6 and
   the Goal-scoped Milestone retro at the `Milestone-reached` chapter Step 1) —
   three prompts: *What did this Era change about how Agora and the product work? · What was
   hardest across the whole chapter? · What should the next Era be?* **Judgment** —
   no writer: drafted from step 3's list, ruled by the user.
2. **Agora landscape snapshot** — refresh / version
   `docs/references/agora/agora-landscape.md`
   (the state-of-the-system paper, born in the round-4 Plaza) to its post-Era state.
3. **List what shipped** — the Goals closed, the Issues created + closed, the stories
   moved to `tested`, the wiki seeds + doc-seeds authored, the skills promoted under
   this Era. **Writer:** `flask agora roster --era <slug> --shipped` renders the sessions,
   the tags fired and the Goals from `era-roster.md`,
   the line `flask agora write roster` appends at every `--end` 2.8 (US-AGORA-092).
4. **Map product ↔ Agora** — what the Era delivered on each side (the product feature
   surface and the Agora-substrate surface), so the next Era opens with both pictures.
5. **Finish open Agora improvements** — sweep the Era's backlog (slot 1): every
   parented follow-up is shipped, re-parented to the next Era, or dropped with a note
   (the shoulder-glance reflex applied at the chapter boundary).
6. **Name the theme** — give the closing Era its one-line legacy summary (the line
   that lands in "Goals (closed)"-style Era history). **Judgment** for the words;
   **writer:** `flask agora write compass-era --close <slug> --legacy "<line>"` (US-AGORA-113)
   marks the entry `*(closed <date>)*` with its Legacy and Status lines.

**Movement 2 — document the Era.** Make the chapter durable:

7. **History** — the Era's narrative goes into the durable record: the book
   (`docs/book/` if the Era warrants a chapter), the commit range, and the session
   journal (INDEX entries spanning the Era). Append one **Era entry** to a version
   file (the IMPROVEMENTS.md restructure of US-AGORA-023 will formalize the per-Era
   `vX` grouping; until then, an IMPROVEMENTS.md heading + an Era summary line).
8. **Version file** — record the Era's open/close dates + the milestone tags it
   contained, so the timeline is reconstructable. **Writer (7 + 8):**
   `flask agora write improvement --era <slug> --open <date> --close <date> --tags <list>`
   writes the Era's version entry once, every tag checked against `git tag`.

**Movement 3 — start the new Era.** Plan forward (or park the Mission cycle):

9. **Era-plan** — open the next Era in COMPASS (theme · why · Goals-to-go-inside ·
   when-finished · backlog), register its `agora:era:<slug>` label with
   `flask agora setup-labels --era <slug>` (`ensure_era_label()`), and (optionally) open
   its tracking Issue. **Writer:** `flask agora write compass-era --open <slug> --file <entry.md>`
   (US-AGORA-113) — the entry heading carries `*(current)*` and its `**GH label:**`; it refuses
   while the old Era is still current (step 6 closes it first). If no next Era is
   ready, the Mission cycle parks with no current Era — the next `--start` with a
   goal prompt opens one.
10. **Architecture hardening** — the deliberate "tidy the substrate before the next
    chapter" pass: the deferred leveling promotions, the policy rewordings the breach
    ledger surfaced, the doc-seeds gone stale. This is where the chapter boundary buys
    the cleanup that mid-Goal sessions defer.

**Output.** The closed Era recorded in COMPASS (moved out of "Eras" / annotated
closed with its theme line + dates + milestone tags), the landscape paper versioned,
the next Era opened (or the Mission cycle parked), and the Era retro written into the
closing session's Close-out. Announce the New Era explicitly — 🏛️ a chapter closes.

---

## Event: `Arc-open` / `Arc-close` (a movement inside the Era — US-AGORA-042)

An **Arc** is a *multi-session movement inside an Era* — phases + a paper + a
ledger Issue — the Era's actual working structure since the Hub-Arc emerged
mid-La-Paz. **A movement, not a tier**: it nests between Era and Goal without
joining the tier ladder (full definition: COMPASS `## The fractal planning
skeleton`; the CLAUDE.md vocabulary table). Both chapters record the LIVED
choreography — the Hub-Arc and the Themelion-Arc are the precedents; nothing
here is invented.

**`Arc-open` — Trigger.** A ruling at a session's plan gate names the Arc
(theme + phase sequence). **Preconditions.** The Era is open; the Arc's scope
is defined against real inventory (the Themelion-Arc opened only after #221
was read whole and emptied into `la-paz-last-topics.md`). **Script.** (1)
**Name it at open** — the Hub-Arc was named retrospectively, the Themelion-Arc
by ruling D1; naming at open is the improvement the precedent teaches. (2)
Open (or designate) the **ledger Issue** holding the Arc's topics (#339). (3)
Record the phase sequence in COMPASS's Era entry. **Output.** The Arc named in
COMPASS, its ledger open, its phases the Era's working plan.

**`Arc-close` — Trigger.** The last phase's work ships. **Script.** (1) The
Arc's **paper** is written — the inventory + the documented session history,
telling the movement's whole story (the Hub-Arc paper, P-010, is the
reference). (2) The **ledger Issue is emptied and closed** with a ledger
comment (#221's precedent: the done-half cited, every outstanding topic given
a successor home). (3) The Era entry records the Arc closed. **Output.** The
paper in `docs/references/strategy/`, the ledger closed, the Era's next
movement (or its finale) sequenced. **No tag** — an Arc is not a Goal; its
Goals fired their own Halelujas along the way.

---

## Habits — recurring practices (not boundary events; US-AGORA-042)

The third category beside events and policies (the cheatsheet's `habit`
coinage, session 2026-08-14): an **event** is boundary choreography, a
**policy** is a rule of engagement, a **habit** is a recurring *practice* —
how Agora performs a class of work whenever that class comes up. One home, two
bounded categories: this file answers "how does Agora perform X" for both.
**A habit with no current firing site is a proposal, not an entry** — nothing
below is invented; each names where it is performed today.

- **AVOR** (Arbeitsvorbereitung — the upfront preparation pass) — *trigger:*
  a hub's leaves are about to move in, or a multi-unit build is about to fan
  out. *Practice:* audit matrix → one story → disjoint spawn waves → matrix
  re-runs to zero (the banked T-035 "Modal AVOR" methodology).
  *Performed at:* `/agora` 1.4 (the spawn-fan-out plan decision + the
  audit-matrix rule) and `/implement-story` Phase 2's plan for the build half.
- **Close-out (as its own Issue)** — *trigger:* an Era phase, half-time or
  Goal line finishes and the deck needs clearing. *Practice:* the close-out
  sweep is its OWN planned sub-goal Issue, created + fired after the
  referenced issues resolve — never a tail bolted onto the active topic.
  *Performed at:* `/agora` 1.4 (the close-out-is-its-own-Issue note), parented
  per `policy-issue-templates` Rule 6.
- **Audit-matrix-first** — *trigger:* any completeness sweep ("bring every X
  to standard Y") or any colour/theme-class sizing. *Practice:* the scope
  comes from a grep-built, multi-line-aware, binding-classified matrix
  generated at the start — never a hand-written list; the sweep ends when the
  matrix re-runs to zero. *Performed at:* `/agora` 1.4 (the
  completeness-sweep rule) + MODE 4 spawn briefings.
- **Shoulder-glance** — *trigger:* leaving any chapter (a phase, a session, a
  topic, an Era). *Practice:* the backward look — catch (what was left
  behind, incl. the similar-problem sweep) + close (summarize what was
  engaged). *Performed at:* `/agora --end` 2.3/2.5 (catch) + 2.3/2.6 (close),
  per `policy-shoulder-glance` (recognized there, never multiplied).
- **Round-prep** — *trigger:* a `/plaza` round is about to become loadable.
  *Practice:* the board cleared (PRs merged on explicit green), the idea
  store read whole and mapped into themes, the user's inputs banked as
  numbered candidates — the round starts loaded, not cold. *Performed at:*
  the prep session before `/plaza` Stage 1 (the session 2026-08-14
  precedent — the coinage's own session).

**Incorporation** (the vocabulary lifecycle's declared last step — coined →
adopted → circulating → **incorporated**): a circulating term crossing the
frequency threshold earns a spec, a structural home, and (where it has a
boundary moment) an event chapter. The call site is `/inspect-pipeline`
`--session` step 4.5's incorporation check; **Arc, AVOR and close-out are the
first three walked through it** (US-AGORA-042 — Arc's spec above + COMPASS;
AVOR's and close-out's specs are their habit entries here).

---

_Every event proceeds to `--end` step 2.3 (compact the log)._
