---
name: plaza
description: "the Agora self-improvement pipeline — the civic plaza where Agora inspects and improves itself. A 7-stage pipeline (Landscape paper -> Background analysis -> Idea harvest -> Traktandenliste -> Feature plan -> Change requests -> Leveling) that takes the skill system from current-state to a planned, documented set of improvements ready for an implementation session. Runs as a recorded `type: plaza` captured session. The planning counterpart to /agora: /agora brackets goal-bound WORK sessions; /plaza runs self-improvement ROUNDS. Plaza plans the changes; a normal session implements them."
argument-hint: "[ (default = run the pipeline) | --preflight | --status | --resume | --store-report | --light <file> ]"
level: used
promoted_at: 2026-06-19
role: "the reformer"
---

> **/plaza plans; it never implements.** The pipeline's output is a *feature
> plan + change requests* the next normal session executes via `/agora --start`
> + `/implement-story`. The moment Plaza starts editing app code to "just fix
> it", it has overreached — capture the change as a request and move on. Plaza
> MAY edit Agora's own substrate (skills, policies, docs, the round Issue),
> because that IS its material; it may NOT build product features.

# Plaza — the Agora self-improvement pipeline

`/plaza` is the **open civic workspace of Agora** — the Athenian agora where
the citizens gather to inspect the system and decide how it should change. It
is the planning counterpart to [`/agora`](../agora/SKILL.md):

- **`/agora`** brackets a goal-bound **work session** — it plans, routes,
  records, and reflects on building *the product*. (start · end · status · spawn)
- **`/plaza`** runs a self-improvement **round** — it inspects *Agora itself*
  and produces a planned, documented set of improvements. (the 7-stage pipeline)

They share the substrate — [`COMPASS.md`](../../sessions/COMPASS.md),
[`EVENTS.md`](../../sessions/EVENTS.md),
[`IMPROVEMENTS.md`](../../sessions/IMPROVEMENTS.md),
[`THREADS.md`](../../sessions/THREADS.md),
[`policy-breaches.md`](../../sessions/policy-breaches.md), and the leveling
system — but they are genuinely **separate pipelines** with separate triggers.
Plaza was extracted from `/agora` MODE 5 on 2026-06-19 (presetup session
session 2026-06-19) precisely because the two stopped being
the same shape: `/agora` is a *bracket*, `/plaza` is a *pipeline*.

> **Agora hosts the conversation; the plaza is where it happens.**

**Plaza is for system maintenance + improvement; the session is for goal-bound
work — never blend them.**

---

## What a round is

A **round** is one pass of the pipeline: it starts from the current state of
Agora and ends with a documented improvement plan. Rounds are numbered (`v1`,
`v2`, …) and each has a **round Issue** on GitHub — the durable idea store
(`agora:type:goal`, the `#131`-shaped Issue). The round Issue is where ideas
land *at the moment they are born* (a comment each), so they don't age out of
a session's context window. The pipeline's job is to turn that pile of comments
into a coherent plan.

Prior rounds: #43 (r1) · #87 (r2) · #105 (r3) · #131 (r4) · #184 (r5) · #231 (r6) · #460 (r7) · **#477 (r8)**.

> **No presetup from round 5 on (lived lesson, session 2026-06-19
> retro).** Round 4's #131 agenda was pre-clarified in a one-time *presetup* session
> because `/plaza` didn't exist yet. That bootstrap is **not** part of the steady
> state: a concrete improvement idea for the next round lands as a **comment on that
> round's Issue at the moment it's born**, and Stage 3 (harvest) + Stage 4
> (Traktandenliste) build the agenda from those comments directly — no separate
> pre-clarification step. The user's standing request: "when we have a bigger concrete
> improvement for round N, we comment on the round-N Issue, and the Plaza makes the
> Traktandenliste." Capture cost stays near-zero; the pipeline does the structuring.

**An Era closes with a round and its implementation round** (the user's ruling,
2026-10-03). A round may span **one long captured session** or **several** — the
captured session file records stage progress so `--resume` picks up where it left off.
But a round is *not* the implementation: when the pipeline produces the feature
plan + change requests, the round **hands off** to one or more normal
`/agora --start` work sessions that build the changes.

---

## The captured session record

Unlike the old freeform Plaza (which wrote nothing but an `IMPROVEMENTS.md`
line), a `/plaza` run **is recorded** — as a `type: plaza` **captured session**:

- Created at pipeline-open from `_TEMPLATE-plaza.md`,
  at `.claude/sessions/<YYYY-MM-DD>-plaza-<round-slug>.md`.
- Gets an [`INDEX.md`](../../sessions/INDEX.md) line like any session.
- Tracks the **7-stage checklist** + the **artifacts produced** (each stage
  links its output doc / Issue / commit).
- Closes with a **retro** + a **dispatch** + an `IMPROVEMENTS.md` round-vX entry.

It is a **lighter ceremony** than an `/agora` work session — because Plaza ships
docs and plans, not product features:

- **No Milestone ceremony.** Plaza never closes a product Goal; the round's own
  milestone (`milestone-agora-improvements-N`) fires later, in the *implementation*
  session that ships the changes — not here.
- **No commit-as-gate.** Plaza commits its own substrate edits (skill/policy/doc
  changes, the round Issue) through the normal commit-tree triage + 4-eye gate,
  but there is no push+CI-green close-gate — a round parks clean.
- **It DOES retro + dispatch.** Those *are* the point of a self-improvement
  round, so they always run (close-out below).

---

## The 7-stage pipeline

The stages run **in order** — each consumes the prior stage's artifact. A
[4-eye gate](../../policies/policy-four-eyes.md) fires **between** stages
(prose recommendation-with-default — see the gate-shape note below). Tick the
captured session's checklist as each stage completes; write the Log entry
*before* the tick.

```
0. Health         flask agora round-topics --health → the previous round read (build rows · plans · carry · citations · learnings); red stops
1. Landscape      map the corpus + the improvement arc → agora-landscape.md (versioned)
                  — a MAP, not an inventory; stats are an input (see 1a–1d)
2. Analysis       landscape + metrics + breaches → background-problems analysis
3. Harvest        round-Issue comments + open Issues + THREADS + findings → raw candidate list
4. Traktandenliste consolidate + dedupe + prioritize → the agenda (finalized topic descriptions)
5. Feature plan   /feature-plan on the agenda → research paper + decomposed stories + impl plan
6. Change requests the plan → concrete documented change requests (the implementation contract)
7. Leveling       /level --board → surface + (gated) execute promotions / regressions / XP
```

### Stage 0 — Health (the round reads its own previous ledger)

**Run `flask agora round-topics --health` before the landscape** (US-AGORA-080). One
command, no composition: the previous round's `build` rows against story status, every
round plan's `**Status:**`, the previous round's carry list (its live-log ⏳ lines), the
declaration's citation counts across the three spellings (`§` · `sect.` · `section`), and
the open Plaza learnings (journal stubs · the last plaza session's findings · the learn
Issues). **Exit 2 stops the round**: an unshipped build row or a round plan with every
story shipped and not `done` is the previous round's debt, and a round that opens over it
plans on a ledger it has not read. The remedy is named by the line — `write plan-status
<plan> done`, or the Issue the unshipped story waits on. Nothing here is remembered; the
preflight runs the same read as its step 0.

### Stage 1 — Landscape (the "V1 paper")

**Paint the current state of Agora as a paper**, the way
`agora-naming.md` paints the
naming. Read the system fresh — never from memory.

> **A landscape is a MAP, not an inventory — the stats are an INPUT, never the
> output.** Counting skills, levels, policies and milestones is the *cheap* half
> and was, until v5, most of what this stage produced. A list of what exists
> tells the round nothing it can act on: the later stages need to know **what the
> skills actually cover**, **where the corpus is thin or doubled**, and **how far
> the previous rounds' intentions actually got**. If the paper could be
> regenerated by a script, it is not yet a landscape. (Rewritten 2026-07-25 on the
> user's ruling: *"we have all Agora stats but that's not the real landscape I
> mean."*)

**Boundary against Stage 2 — hold it deliberately.** The landscape is
**descriptive**: *what is here, what it covers, where the seams are.* Stage 2 is
**diagnostic**: *why it drifts.* Stage 1 may say "two skills both claim the
verify step and routing between them is ambiguous"; naming the root cause of the
resulting drift is Stage 2's job. A Stage 1 that diagnoses leaves Stage 2 with
nothing but a re-clustering — the exact failure that stage is already warned
about.

#### 1a — The corpus map: what is *inside* the skills

The stage's centre of gravity. Per skill, read the SKILL.md itself — not just its
board row: its **modes**, its **`## Claims at this level`** (`hardened`+), its
**`## When NOT to use`** boundary, and its role/epithet. Then derive the four
things a list cannot show:

- **Coverage** — map each skill onto the phases of the work cycle (plan · build ·
  verify · document · audit · meta). Which phases have an owner, which have
  several, which have none.
- **Overlaps** — skills whose declared boundaries touch, where routing is
  genuinely ambiguous. (`## When NOT to use` tables are the primary evidence:
  where two of them point at each other, the seam is real.)
- **Thin spots** — a phase with no skill, a `draft`-level skill carrying
  load-bearing work, a skill whose claims exceed what it demonstrably does.
- **Weight** — which skills carry the corpus (M1 + M5 fan-in + XP) and which are
  near-dormant. Dormancy is a finding, not a footnote: it feeds the keep / merge /
  retire question directly.

#### 1b — Position in the improvement arc: where we stand

Where the round sits in the *sequence* of rounds — the question "are we
accumulating unshipped intentions?".

- Walk the **prior round Issues** (the list under *What a round is*): what each
  shipped, what it **deferred**, what is **still open**.
- Read the **`IMPROVEMENTS.md`** arc — not the tail, the arc: which lessons
  recur across rounds (a lesson logged in three rounds is a structural gap that
  earlier rounds failed to close).
- Name explicitly what previous rounds **decided but did not build**, and what
  they **built but nobody uses** — both are load-bearing for the agenda, and the
  second is the harder one to see.
- **The adoption half of that question is a COMMAND READ (US-AGORA-050) — cite
  it, do not re-grep it.** `docs/stats.yaml` → `agora.mechanisms` carries the
  per-mechanism adoption table (session-mention counts over the newest-30
  window — a labelled PROXY — plus called-vs-remembered from
  `.claude/mechanisms.yaml`; `below_threshold` names the call-sites-or-retire
  candidates — partly a timing artefact of when session files are counted, so
  never a retire ruling on its own, #477 2026-09-30), and `agora.prose_mass` / `agora.learn_dispositions` /
  `agora.xp_bucket_drift` carry the D4-1 metrics. The one LIVE number is
  `flask agora store-level` (open learn-issue count + opened/closed per month —
  "did the round drain the store?"). **The acceptance table is a command read too
  (US-AGORA-081):** `flask agora acceptance` — every mechanism UPPER / PARTIAL / LOWER with
  the corpus dimension that moved. The landscape's §b tables cite these outputs; hand-grepping
  or spawning them is retired. The MAP on top — what the numbers mean — remains this stage's job.

#### 1c — The operating state (the inventory — one section, not the paper)

The cheap half, kept because the later stages cite it — and a count that sums two
lists names their overlap (round 7's "31" was 23 distinct):

- **Skills + levels** — `flask agora board` (level · `promoted_at` · M1 all-time and since promotion · M2–M6 · XP · the candidate column; US-AGORA-078 — one command over the files, the read `/level --board` wraps).
- **Policies** — `ls .claude/policies/` + each `## TL;DR`; rule counts in `docs/stats.yaml`.
- **Sessions + milestones** — `INDEX.md` tail + `git tag -l 'milestone-*'` — the trajectory.
- **The declaration** —
  `docs/references/agora/agora-declaration.md`
  §0: the corpus is read **against the seven statements**, and the landscape's verdict
  names the statement each finding violates (`AGORA-DECL §<n>`) or declares a new one;
  §3's record flags are 1a's review vocabulary beside the boundary tables
  (US-AGORA-054; the declaration's §5.1 binds this stage).
- **Goals** — `COMPASS.md` active + closed; the current **Era**; open `agora:type:goal` Issues.
- **The pile** — `docs/stats.yaml` → `agora.pile` (the trend `flask agora oda --record` writes at every `--start`: total, unhomed, oldest unhomed age) + `flask agora oda` for today's unhomed list (US-AGORA-112). *"The pile gets smaller"* is read here as a trend, not asserted.
- **Drift signals** — `IMPROVEMENTS.md`, `policy-breaches.md`, `THREADS.md`; `docs/stats.yaml` `agora.exceptions` + `agora.breaches` (the exception rate per session — §M's proxy, US-AGORA-084).
- **Frontmatter health** — `python scripts/checks/validate_skill_frontmatter.py --check`
  (hard pre-flight — fix + commit before proceeding if red).
- **Mechanism adoption + store level** — `docs/stats.yaml` → `agora.mechanisms`
  (freshness-gated by CI) + `flask agora store-level` (the live learn-store
  read). Both are US-AGORA-050 command reads.
- **The policy scorecard** — `python scripts/generators/policy_scorecard.py` (US-AGORA-011): the
  per-policy citations · breaches · `needs-rewording` flag (breach-driven; citations
  never trigger it) — the **rewording queue**, read here so §c's breach paragraph is a
  command read. Lived, round 7: the script existed since round 3 and sat `remembered`
  (0 mentions) for three landscapes because this list never named it; the round read it
  at Stage 7 instead of here (four-eyes 4 · commit-discipline 3 · skill-routing 3
  flagged). US-AGORA-058 records this call site in `mechanisms.yaml`.
- **The defect ledger** — `flask agora battle-map --check`, regenerate if
  stale, then read
  `docs/references/agora/bug-battle-map.md`
  — the four defect sources (bugs intake · Selenium recorded set · breaches ·
  learn board) with per-source trend. "Are we winning?" is a READ here, not a
  hand-grep; the map's authored defect classes feed the landscape's verdict
  (US-AGORA-052 command read).

#### 1d — The verdict: where Agora stands, and the next focus

Two paragraphs, and the second is the one the round is judged against:

1. **Where Agora stands right now** — the state-of-the-system verdict, grounded in
   1a + 1b rather than asserted.
2. **The general next focus** — where the system's centre of gravity *should* move
   next, argued from the map. This is written **before** the agenda exists, so it
   is a genuine prior: Stage 4's Traktandenliste is then checked against it, and a
   divergence between the two is itself a finding worth surfacing to the user.

**Output:** `docs/references/agora/agora-landscape.md` — a versioned snapshot
(`## v<N> — <date>` sections; the paper accretes one section per round, never
overwrites — the version history *is* the landscape's evolution). **The paper's
version counter is independent of the ROUND number** (v1=r4 · v2=the Era close ·
v3=r5 · v4=r6) — a non-round snapshot (an Era close) advances it too, so never
derive the section number from the round; read the file's last `## v<N>` header
and increment. Sections mirror
1a–1d: the corpus map, the position in the improvement arc, the operating state
(including the four Agora layers — policies / skills / tools / the `/agora` +
`/plaza` orchestrators), and the verdict + next focus.

**Gate — a DISCUSSION, not just an acknowledgement.** The landscape's job is not
finished when the user agrees it is accurate. **The map brings improvements into
view that are in nobody's store**, and this gate is where they are surfaced and
talked through — before the analysis, before the harvest.

Two parts, in order:

1. **Confirm the map** — *"this is where we are; agreed?"*
2. **Open the discussion** — name, explicitly, **what the map brings into view that
   is not yet a candidate**: a thin spot with no owner, a dormancy nobody decided
   on, a mechanism the arc shows was built and abandoned, a §1d next-focus with no
   corresponding store item. Propose each as a **landscape-born candidate** and
   discuss it with the user. Whatever survives enters Stage 3's harvest as a
   first-class source (`Source 5`), alongside the store.
3. **Bank every surviving candidate — as a step that runs, not a note to self:**

   ```bash
   flask agora capture "<the finding, one or two sentences>" --type landscape --source "<round-session-id>"
   ```

   One call per surviving candidate, straight onto the open round Issue
   (US-AGORA-030). This is what makes the landscape's own discoveries reach the
   agenda **by construction** rather than by luck — a §1d finding that lives only
   in the paper depends on the next round's prep session excavating it, which is
   precisely the leak the v5 retro named. Capture never blocks: with `gh` down it
   spools locally and `flask agora audit` flags it.

> **Why this gate is a discussion (lived, v5 retro).** The v5 round's landscape was
> the first written under the rewritten stage and the user's verdict was that it *"is
> now really the base of the improvement structure"* — but its findings still reached
> the agenda only **indirectly**, through Stage 2's analysis. The user's ask:
> *"the next Agora Plaza should profit more from the landscape in **opening a
> discussion** for improvements that come into view from the landscape analysis."*
> The underlying purpose the same retro named — *"a goal of this collection of ideas
> is that we can **solve topics in relation to each other**, rather than focusing on
> one specific topic"* — is exactly what a map is good for and a store is not: the
> store holds topics; the map shows the **relations between them**.
>
> This is the *discussion* sibling of **US-AGORA-030**'s capture path (N5): that story
> makes landscape findings **durable**; this gate makes them **discussed**. Both are
> needed — a captured finding nobody talks about is still a finding that decays.

#### 1e — The external survey (time-boxed, cited)

**Thirty minutes, outward.** Before the verdict closes, read what the open world has built
since the last round for the problems this landscape names: the agent-harness repositories
and frameworks whose shape Agora borrows or rejects (a session bracket, a skill registry, a
lesson loop, an evaluation ledger). Three to five sources, each **cited by URL** with one
sentence on what it does that Agora does not, or does differently. The findings are
**landscape-born candidates** (1d step 2's `Source 5`) — banked with `flask agora capture
--type landscape`, harvested at Stage 3, never a reading list in the paper. A survey that
cites nothing happened to nobody; a survey with no candidate says so in one line.

### Stage 2 — Background analysis

**Check-in before composing (US-AGORA-080):** one question to the user before the
analysis is written — *"the landscape names these signals; which one hurts most right
now?"* — and the answer orders the diagnosis. The stage's output is composed after it,
never before.

**From the landscape, diagnose the background problems** — the *why behind the
drift*, not the symptom list. Read the signals the landscape surfaced:

- the `policy-breaches.md` scorecard (which policies get broken most — the
  rewording queue),
- the `IMPROVEMENTS.md` tail (recurring lessons — a lesson logged 3× is a
  structural gap, not a one-off),
- the M2 correction-load + M3 redo-rate outliers from `/level --board`,
- stale THREADS (promote-or-drop overdue), under-referenced policies (drift
  risk per `/inspect-pipeline --audit`).

**Output:** a structured background-problems section (in the captured session
file, or a short `docs/references/research/` note if the round warrants it) —
each problem named, root-caused, and tagged with the evidence. This is the
"background issues" the round exists to solve.

> **The stage must yield NOVEL insight, not restate the Traktandenliste (lived
> lesson, session 2026-06-19 retro).** When the agenda is
> already finalized going in, the easy failure is to "diagnose" by simply grouping
> the topics you already have — the user sees no new input. Mirror `/feature-plan`'s
> A.5 discipline: if you can't name at least one root cause, cross-cutting pattern, or
> connection the topic list does NOT already make obvious, the analysis is too shallow —
> read more signal (the breach ledger, the M2/M3 outliers, the IMPROVEMENTS tail, stale
> THREADS) until it surfaces something the agenda didn't. The deliverable is the *why
> behind the drift* (e.g. "all five problems instance one missing reflex"), not a
> re-clustering of the *what*.
>
> **Since v5, Stage 1 hands this stage far more to work with** — the corpus map's
> overlaps/thin-spots/dormancy (1a) and the "decided-but-never-built" /
> "built-but-unused" findings (1b) are *descriptions*; converting them into root
> causes is exactly this stage's job. The boundary runs: Stage 1 says **what the
> seam is**, Stage 2 says **why work falls through it**.

**Gate:** user confirms the problem framing before ideas are harvested against it.

### Stage 3 — Harvest (idea store → raw candidate list)

**Gather every improvement candidate** from the durable idea stores:

- **the newest store report first** — `flask agora store-report` (US-AGORA-060): the
  open learn Issues already mapped into themes, duplicate families with a canonical,
  already-built, declaration-shaped and a proposed disposition per family. Read it, do
  not redo it; run it fresh if the newest comment is older than the round's open.
- **the round Issue's comments** (`gh issue view <N> --json comments`) — the primary store;
  each comment is a candidate. **US-AGORA-076:** `flask agora round-topics --target <N> --harvest
  --dossier-ids <file>` snapshots the set `state-check` holds the close to; `--propose-done` splits the shipped rows.
- **open `agora:type:*` Issues** — goals/sub-goals/sections that are really
  Agora-improvement asks.
- **`THREADS.md`** open threads tagged Agora-meta + anything promote-or-drop due.
- **recent session `## Agora findings`** + `IMPROVEMENTS.md` "what to change
  next" items not yet actioned.
- **landscape-born candidates** — whatever survived Stage 1's discussion gate.
  These are **first-class**, not an afterthought: they are the round's only source
  of candidates nobody thought to file, and in v5 the item that became the round's
  *spine* (the `/learn` mechanism exit) was of exactly this kind — absent from the
  store and produced by reading the map. A round whose harvest contains **zero**
  landscape-born candidates should re-read §1a/§1b before proceeding; it means the
  map was confirmed but never mined.

**Output:** a raw candidate list (id + one-line each) — unstructured, complete.
Completeness over tidiness here; structuring is stage 4.

**Gate:** "here's everything I found — anything missing before we consolidate?"

### Stage 4 — Traktandenliste (the agenda)

**Check-in before composing (US-AGORA-080):** one question before the agenda is drafted
— *"of the clusters the harvest shows, which must this round not leave out?"* — so the
Traktandenliste is prioritized with the user's answer in hand, not re-ordered after a draft.

**Consolidate the raw list into a single prioritized agenda** with **finalized
topic descriptions** (not bullet fragments). This is the heart of the planning
round — discuss, structure, prioritize *with the user*:

- **Dedupe + cluster** — many candidates are the same topic from different
  angles (e.g. "Eras", "milestones v2", "fractal simplicity" are one
  structural theme). Cluster them into named topics.
- **Finalize each topic's description** — a clear, self-contained statement of
  what the topic is, the problem it solves, and the rough shape of the change.
  (This is the work the presetup session does *ahead of time* for the #131
  comments — Plaza inherits descriptions that are already clear.)
- **Prioritize** — must / should / could, sequenced. Note dependencies.

**Output:** the **Traktandenliste** — a prioritized topic list with finalized
descriptions, written into the captured session file (and mirrored to the round
Issue as a consolidated comment / the Issue body, per the Issues-as-idea-store
model). This is the agenda the feature plan decomposes.

**Gate (4-eye, prioritization):** propose the priority order with a
recommendation; the user nods or re-sorts. This is the round's key decision
gate.

### Stage 5 — Feature plan

**Route the prioritized agenda to `/feature-plan`** —
do NOT reimplement decomposition here. Feature-plan produces the research paper
(`RP-AGORA-NNN`), the critical review (alternative shapes), the decomposed
`US-AGORA-NNN` stories, and the umbrella implementation plan.

For a small round (≤2 topics) route to `/new-story`
instead, per the compounding-simple rule (`new-story` writes ≤2 stories;
3+ compounding topics route to `feature-plan`).

**Output:** `RP-AGORA-NNN` + the decomposed stories + the implementation plan.

**Gate:** the feature-plan skill's own decomposition gate (already a 4-eye gate) — **read against the
round contract.** A shape that breaks a Stage-4 ruling (the build cap, a disposition verb set aside) is a
**re-ruling**, asked once and explicitly, and its consequences are written into the paper and the plan so
nothing downstream pretends the contract held (lived session 2026-10-31: Shape A
over the recommended B — 44 stories against a 15-story cap, `fix` unused; one picker, both recorded).

### Stage 6 — Change requests (the implementation contract)

**Turn the plan into concrete, documented change requests** — the contract the
implementation session executes "all at once". Each change request names:

- **the target** — which skill SKILL.md / policy / doc / template / script file,
- **the change** — what is added / moved / rewritten (specific enough to build
  from without re-deriving),
- **the routing** — `/learn <skill>` (skill patch) · `/document --policy <slug>`
  (cross-cutting rule) · direct edit · new skill,
- **the order** — dependency sequence for the implementation session.

**Output:** the change-request set — mirrored to the round Issue (the openable
plan, per #131's "the milestone plan lives in a GH Issue the user can open")
and/or an implementation plan at `docs/implementation-plans/`. The next session
opens `/agora --start` against this contract.

**And executed, not only mirrored (lived, round 7).** Every disposition the contract
declares for a store Issue — *fold* into a story · *duplicate* of a canonical · *built* ·
*home* on a Goal Issue · *store* — is **executed at this stage**: the citing comment
posted, the close performed **and re-read** (`gh issue view … --json state` — #304's
`-F` no-op is why), a home list commented on each receiving Goal Issue. Until
US-AGORA-058's `flask agora dispose` exists, a scripted `gh` pass does it (round 7's
`stage6_execute.py` shape: one comment per Issue citing the session + the contract
comment + `AGORA-DECL §6`, verify after every close, zero failures across 99). Driver:
round 6 *mirrored* nine folds and twenty-two phase-③ dispositions in its contract
comment and executed none — all were still open 22 days later, and phase ③ had closed
without its passengers (landscape v5 §b). A disposition that is written down and not
performed is a remembered write; the reader that would catch it is US-AGORA-056's
`reconcile disposition-drift`, and the step that prevents it is this one.

**Gate:** user confirms the change-request set is the implementation scope.

### Stage 7 — Leveling

**Run `flask agora board`** (US-AGORA-078 — `promoted_at:` the window, the candidate column computed; the read `/level --board` wraps)
and surface promotion / regression / XP candidates from the round's vantage point — the natural moment to level the skills that did the work. Per [`policy-skill-progression`](../../policies/policy-skill-progression.md):

- **Promotions** — gate met + quest artifact present → `/level <skill> --promote`
  (with the naming ceremony at `used → hardened`). Human-confirmed, never auto.
- **Regressions** — only a `/learn` patch contradicting a named claim
  (`--regress --corrects <sha>`).
- **XP** — any moments worth awarding (the round itself earns XP for the skills
  it invoked — `/feature-plan`, `/level`, `/plaza` once it's `used`+).

**Output:** the leveling actions taken (or candidacies recorded for a later
`/agora --end`).

**Gate (4-eye):** promotion/regression is human-confirmed per the policy.

---

## Close-out — retro, dispatch, handoff

When stage 7 finishes (or the round parks mid-pipeline), close the captured
session. Apply [policy-shoulder-glance](../../policies/policy-shoulder-glance.md) —
this close-out **is** the round's *Schulterblick*: the retro + dispatch (steps 2–3)
are the **catch** half (nothing the round surfaced is silently abandoned) and the
retro + `IMPROVEMENTS.md` vX entry (steps 2 + 4) are the **close** half (the round
is summarized and closed). Recognize this existing sweep as the glance; no new gate.

1–N below are that glance, made concrete:

1. **Commit-tree triage** — Plaza's own substrate edits (skills/policies/docs/
   the landscape paper) go through the normal triage + 4-eye gate
   ([policy-commit-discipline](../../policies/policy-commit-discipline.md)).
   No push+CI close-gate (a round parks clean).
2. **Retro (two-way)** — the same three prompts as `/agora --end` 2.6: what
   worked / what didn't / what to change. Plaza is itself the lived test of the
   leveling + planning system — a round where the board or the pipeline didn't
   help is a finding. Answers go into the captured session's `## Retrospective`
   verbatim.
3. **Dispatch findings** — route per [policy-documentation](../../policies/policy-documentation.md):
   skill correction → `/learn`; cross-cutting rule → `/document --policy`;
   a real bug/feature → note as a thread/Issue.
4. **`IMPROVEMENTS.md` round-vX entry — written and maintained by command (US-AGORA-023 / 079).**
   `flask agora write improvement --round vX --file <entry.md>` places the round's entry
   (what the round changed about Agora, why) under `## Current round (live log)` with its
   **status checklist** in the file's markers: **✅ implemented · ⏳ carried/unhandled · ❌
   dropped** (legend in `## Reading this file`); a second entry for the round refuses. The
   current round's `vX` is the **live log** — as implementation `/agora` sessions land each
   phase, `write live-log` marks ✅ / ⏳ / ❌ (never silently lose an item). Then
   `flask agora write improvement --archive-stale`: every round whose milestone tags have
   all fired (read from `git tag`) leaves the live log for `## Archive` — the Era
   "document" movement (US-AGORA-016); IMPROVEMENTS is the round/Era history. **Then the Harness paper** (US-AGORA-089, ON-7): `check_record_consistency.py --fix` regenerates its blocks, `version:` takes the ontology CHANGELOG head and `generated:` the date, and the narrative is rewritten where the CHANGELOG moved.
5. **Handoff** — state explicitly: the round produced `<plan + change requests>`;
   the next step is `/agora --start` against that contract to implement; **per round
   plan whose stories all shipped, `flask agora write plan-status <plan> done`** (it
   refuses on an unshipped story — r3 · r4 · r5 read `draft` / `in-progress` with every story shipped until US-AGORA-079). Flip the captured
   session `status: closed`; update its INDEX line; **`flask stats dump` last** (after the status flip, so the closed-count is fresh — same load-bearing
   order as `/agora --end` 2.8).

---

## Preflight — `--preflight` (US-AGORA-074)

**Run manually, before a round, inside an `/agora` session.** It merges the two
things that used to happen by hand before every round — the *prep session* that
read the round Issue and banked the user's new inputs (the session 2026-08-14
· session 2026-09-05 shape, now superseded by this mode) and the
*patch-Plaza-first* habit, where a lesson about Plaza reached this file only if
someone remembered it before the next round. After the preflight the round opens
directly, on an improved skill. The command under it is `flask agora round-topics`
— **not** `flask agora preflight`, which is the close gate.

0. **Health first — `flask agora round-topics --health`** (US-AGORA-080). Stage 0's read,
   run before anything else: a red (an unshipped build row of the previous round, a round
   plan unflipped) **stops the preflight** with the rows named; the remedy is a write, not a
   note. Green, the preflight continues.
1. **Prepare the Issue — the complete topic list.**
   `flask agora round-topics --out <scratch>/round-topics.md` prints one numbered
   row per body section (`B1..`) and per comment (`T001..`, oldest first): date,
   kind (the captured type, a banked `C<k>`, or `free`), a title, and every story
   the topic names with its current status. **The footer's count must equal what
   `gh` returned** — that equality is what makes the list complete, never a reading
   of the Issue by eye. Present it themed by kind as the user's overview, and ask
   the standing question: *what is missing?* The user's new inputs are written as
   `## Title` sections and banked as numbered C-comments with
   `flask agora store-report --topics <file>` — `--dry-run` first, the post on the
   nod. A topic whose named stories are all `implemented` / `tested` reads as done:
   say so, it is a candidate to close at Stage 3, not new work.
2. **The Plaza-skill comments.** `flask agora round-topics --plaza` keeps the rows
   that concern this skill (its stages, the round contract, the landscape) and lists
   the **open Plaza learnings**: the stubs in `experience.md` `## Unrated journal`,
   the `## Agora findings` + `**Dispatched:**` of the newest closed plaza session,
   and the open `agora:type:learn` Issues naming plaza. Each row is said to be one of
   two things, out loud: a **learning** (it changes how Plaza runs — step 3) or a
   **round topic** (it changes what the round decides — it stays on the Issue).
3. **Apply the previous round's learnings — implemented, not recorded.** Classify
   each learning **apply now** (a patch to this file a session can write and verify:
   a stage instruction, a gate, a reader a stage must call) or **round topic** (too
   big for a patch — a new mode, a new command, a change to the stage structure; it
   goes on the round's agenda). Every *apply now* item goes through
   [`/learn`](../learn/SKILL.md) so it lands in `experience.md` `## Level history`
   with its `mechanism | prose | judgment` disposition, and the patches are
   **committed before the round opens** — a learning still only in a journal when
   Stage 1 starts is the failure this step exists to remove.
4. **Read the board once — `flask agora board`** (US-AGORA-078): the candidate column names
   the skills Stage 7 will rule on; the `[?]` lines name a window the record lacks.

The preflight's gate is the `/agora` session's own: the topic list, the C-comments
and the patch list go to the user as one proposal. **It is the one sanctioned
`/plaza` use inside an open `/agora` session** (the open-round guard below), because
it edits this skill and therefore commits; the round itself still opens as its own
`type: plaza` session afterwards.

---

## Open-round guard

**`/plaza` requires no `/agora` work session be open.** If a session is
`status: open` when `/plaza` runs, surface it and ask the user to `/agora --end`
it first (or continue work inside it). The two pipelines never run nested. Two
exceptions: `--preflight` (above), which runs inside the `/agora` session that
commits its patches, and the *presetup* pattern — improving Plaza itself from within a
regular meta session (how this skill was born) — which uses Plaza-adjacent tools
inline without formally entering the pipeline.

If a captured `type: plaza` session is already `open`, `/plaza` (default) offers
`--resume` instead of opening a second round.

---

## Gate shape — prose recommendation-with-default

Same rule as `/agora`: the between-stage gates are **conversations**, so fire
them in **prose** (state the recommended path + reasoning, invite nod-or-redirect)
— NOT the `AskUserQuestion` dialog, which hides the reasoning and shuts down
free-form feedback. Reserve `AskUserQuestion` for clean either/or separations
(promote / park / cancel; shape A / B / C). Per
[`policy-four-eyes`](../../policies/policy-four-eyes.md) Rule 2.

## When NOT to use this skill

| Need | Use instead |
|------|-------------|
| Bracket a goal-bound work session | [`/agora --start`](../agora/SKILL.md) |
| Just check the skill board ad-hoc | `/level --board` directly (no pipeline) |
| Patch one misbehaving skill from a lived session | [`/learn`](../learn/SKILL.md) |
| Audit the static `.claude/` tree (no round) | [`/inspect-pipeline --audit`](../inspect-pipeline/SKILL.md) |
| Implement the changes a round planned | [`/agora --start`](../agora/SKILL.md) + `/implement-story` |
| Author one cross-cutting policy | [`/document --policy`](../document/SKILL.md) |

## Claims at this level

The invariants other skills and the user depend on `/plaza` to hold (the `hardened`-tier
commitments, written at round 8's Stage 7 candidacy — US-AGORA-080; each is the unit
`/learn` checks for contradiction per `policy-skill-progression` Rule 4).

1. **A round opens on a read of its own previous ledger.** Stage 0 and the preflight's step 0 are `flask agora round-topics --health`; a red stops the round. Nothing about the previous round is remembered.
2. **Every stage gate is a prose recommendation-with-default fired between stages, and Stages 2 and 4 compose their output only after the check-in.** No stage runs on an unasked question.
3. **The harvest is complete by construction.** The topic list's footer equals what `gh` returned, and the harvest snapshot (`round-topics --harvest`) is what the close is held to — a candidate the round never saw is a `state-check` finding, not a memory.
4. **A round closes with every candidate disposed and its bookkeeping written by command.** The ledger's undisposed count is 0 at the close; the live-log entry, the stale-round archive and the plan statuses are writes (US-AGORA-075 / 079), never edits.
5. **`/plaza` never runs nested inside an open `/agora` session**, `--preflight` being the one sanctioned exception (it edits this file and therefore commits).

## Mode dispatch

| User says | Mode |
|-----------|------|
| (nothing) / `--run` / "open the plaza" / "run a plaza round" / "improvement round" | **run the pipeline** (default — open the captured session, start stage 1; offer `--resume` if a round is open) |
| `--preflight` | **before a round, inside an `/agora` session** (US-AGORA-074) — the complete numbered topic list of the round Issue (`flask agora round-topics`, its count checked against `gh`), the user's new inputs banked as C-comments, the Plaza-skill comments separated, and the previous round's open Plaza learnings applied to this file via `/learn` and committed before the round opens. See `## Preflight`. |
| `--status` | report which stage the open round is on + the next gate |
| `--resume` | continue the open captured `type: plaza` session from its last ticked stage |
| `--store-report [--topics <file>]` | **the store's reader** (US-AGORA-060, `AGORA-DECL §2`) — run `flask agora store-report --post` (themes · families · built · declaration-shaped · top-N · level · one disposition per family, comment-only, on the round Issue; over the threshold it says a round is due and never opens one); with `--topics <file>` bank the user's prepared topics as numbered C-comments instead. Runs from the workstation's crontab (row `store-report`, `scripts/ops/linux/jobs.yaml`): `run_store_report.sh` calls `flask agora store-report --post` directly, no model (US-AGORA-065's ruling); `claude -p "/plaza --store-report"` is the attended alternative, a `/schedule` routine on a fresh clone the cloud one. No stages, no session file. |
| `--light <file>` | **the light modes model step** (US-AGORA-110) — run headless by `scripts/ops/linux/run_plaza_light.sh` in its worktree, never in the live checkout. `<file>` is the plan `flask agora light --draft` wrote: replace each rows `--as <verb> --target <target> --reason "<why>"` hole with ONE proposal in the round ledgers vocabulary (`build` a story id · `fold` a sibling row or story · `home` an open Issue · `fix` a Trigos row · `done` / `drop` a reason) — read-only `flask agora` calls (`round-topics`, `acceptance --mechanism`) to decide; edit that file and nothing else, change no `gh` state, run no `write`. A row you cannot rule keeps its hole. The PR is the proposal; the user runs the lines they accept. No stages, no session file. |

## Notes

- **Plaza plans; the session implements.** The hard boundary. A round's success
  is a plan an implementation session can execute "all at once" — not changes
  shipped here.
- **The round Issue is the durable idea store.** Ideas land as comments on it at
  the moment they're born (#131's core thesis); the pipeline (stages 3–4) turns
  the pile into an agenda. Capture cost must be near zero or amnesia wins.
- **Plaza is its own lived test.** Every round implicitly audits whether the
  leveling board + the pipeline structure actually help direct attention — a
  round where they didn't is a `## Retrospective` finding.
- **`used` skill.** `/plaza` was authored at `draft` (2026-06-19, presetup) and
  promoted to `used` *"the reformer"* in its own inaugural run (round 4, #131) — the
  lived test passed end-to-end. It now earns XP per `policy-skill-progression`; the
  `used → hardened` gate (the naming ceremony + a `## Claims at this level` section)
  is a future pass once M1 + the quest are met.
