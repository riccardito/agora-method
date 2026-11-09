# Agora Compass

The durable layer above session files. Updated rarely — when the Vision shifts,
when a new Mission cycle opens, when a Goal lands or a new one is committed to.
`/agora --start` reads this every session and surfaces the active tiers in 1.4.

## Vocabulary note — Tier vs Milestone vs North star

Three adjacent concepts that are NOT the same thing:

- **Tier** (a.k.a. release group) — the GH `milestone:` attribute. *Where a
  Goal/sub-goal sits in the queue.* Examples today: "Finance Roll-out for
  full premium", "Mobile UX", "Tier 3", "Tier 4". Reassignable any time
  by editing the Issue; doesn't carry a closing contract.
- **Agora Milestone** — the `milestone-<slug>` annotated git tag fired
  at Goal closure (the Haleluja event, `/agora --end` Path A). *What we
  call the Goal when it ships.* Declared in COMPASS at the moment a Goal
  moves Backlog → Active; immutable once declared.

- **North star** *(added 2026-08-11, session 2026-08-11)* —
  a **named horizon for a topic or design line**: not a tier, not a
  committed deliverable, never "closed". It exists to **orient
  decisions** — the standing test question is *"does this make the north
  star harder or easier to reach?"* — and it is topic-scoped where Vision
  is system-wide. A north star is retired or replaced only by an explicit
  ruling, never by drift. Example: *"every hub configurable from the UI,
  no code change"* -- a direction a configuration Goal steers by and never
  closes.

User-friendly framing: *"a tier is where it sits in the queue; a
Milestone is what we'll call it when it ships; a north star is what we
steer by and never arrive at on purpose."* See
[`policy-issue-templates`](../policies/policy-issue-templates.md) Rule 6
for the full timing rules.

## Vision

<The forever horizon: what the product is for, in two or three sentences.>

## Mission

<The current multi-year cycle, with the date it opened.>

## The fractal planning skeleton

The **operable** planning tiers — **Era** and **Goal** — share **one 6-part
skeleton** (US-AGORA-017 / RP-AGORA-004 T3). Same mental model at both sizes:
fractal simplicity, the same shape at every scale. An author opening *either*
object fills the same six slots in order, so a follow-up / open thread always has
a structural home and continuation is never guessed.

| Slot | Name | What it holds |
|---|---|---|
| **0** | **structure** | the topics this object holds — its agenda |
| **1** | **backlog** | the bucket for follow-ups + open threads parented here |
| **2** | **start** | the game-plan — why it exists, what's in, when it's done |
| **3** | **sections** | implementation + testing, across one or more sessions |
| **4** | **evaluation** | open-thread handling — the shoulder-glance (US-AGORA-020) lands here |
| **5** | **ending** | plan the next + close the current — the ceremony (Milestone / New Era) |

**Topics taxonomy (slot 0)** — what an object's agenda is made of: *unspecified
ideas* · *open goals / milestones* · *open Issues* · *open threads*. A thread
**gets its Issue** when it is promoted from the backlog (slot 1) to a topic (slot 0)
— promotion is the slot-1 → slot-0 move (US-AGORA-022 formalizes the thread side).

**Backlog = an empty Era** — a not-yet-started chapter is the **same object** with
its **slot 2 (start)** unfilled: it has a structure (slot 0) and a backlog (slot 1)
but no opened game-plan. Opening it fills slot 2 and sessions begin inside it
(reconciled with US-AGORA-016's Era model).

**The existing fields ARE the slots** (behaviour-preserving — no restructure):

| Slot | …in a **Goal** | …in an **Era** |
|---|---|---|
| 0 structure | `**Era:**` parent + the sub-goals/stories it spans | **Goals inside** |
| 1 backlog | deferred/non-blocking follow-ups noted on the Goal | **Next steps / backlog** |
| 2 start | **Intent** (why · what's in) + **Success criteria** (when done) | **Theme** + **Why it exists** + **When it's finished** |
| 3 sections | the `- [ ]` **Success criteria** ticked across sessions | the member Goals closing in turn |
| 4 evaluation | the shoulder-glance at each `--end` / Milestone | the `New Era` Movement-1 backlog sweep |
| 5 ending | the **Milestone** (Haleluja) | the **New Era** event |

New Goals + Eras inherit the skeleton through this mapping — the slots are read off
the existing structure, not added as new prose per object. Full rationale:
`docs/references/strategy/agora-planning-skeleton.md`.

**Tiers have sizes (US-AGORA-063, `AGORA-DECL §7`):** a batch that needs more than one
loadable plan or more than N sessions is a Goal; a Goal that needs more than one Milestone
is a phase. Measured, not felt — `flask agora milestone --goal` reads every open batch
against `tier_thresholds` in `mechanisms.yaml` (first setting 3 sessions · 2 plans, from
the phase-④ data: B8 would have fired at its second plan) and exits 2 at the count; the
escalation is a **ruling at the plan gate**, never automatic — `flask agora batches
--elevate <batch>` re-tiers it, or `**Tier ruling:** stays a batch` on the batch Issue
records the decision to keep it.

### The Arc — a movement, not a tier (US-AGORA-042)

An **Arc** is a **named multi-session movement inside an Era** — the Era's
actual working structure since the Hub-Arc emerged mid-La-Paz: a themed
sequence of **phases** with **a paper** (its narrative record) and **a ledger
Issue** (its topic bucket), spanning one or more Goals **without joining the
tier ladder**. The Era is the chapter; the Arc is how the chapter's work
actually moves; the Goals inside it still fire their own Milestones.

- **Opens** by a ruling at a session's plan gate, against real inventory —
  named at open (the Themelion-Arc precedent, ruling D1), its ledger Issue
  opened, its phase sequence recorded in the Era entry → the `Arc-open`
  event ([`EVENTS.md`](EVENTS.md)).
- **Closes** when its last phase ships: the **paper** written, the ledger
  Issue emptied + closed with a ledger comment, the Era entry updated → the
  `Arc-close` event. **No tag of its own** — an Arc is not a Goal.
- **In the skeleton:** an Arc is how an *Era's* slot 3 (sections) organizes
  itself when the chapter's work is bigger than a plain Goal sequence. Lived
  precedents: the **Hub-Arc** (ten hubs; closed with the Hub-Arc paper) and
  the **Themelion-Arc** (five phases; ledger #339).

*Incorporated 2026-08-15 (US-AGORA-042) — the term circulated since
mid-La-Paz with no vocabulary home; this is its declared incorporation
(spec + structural home + events).*

## Eras

<!--
  An ERA is a themed chapter that groups Goals into a coherent arc (US-AGORA-016 /
  RP-AGORA-004 T1). Sessions open *inside* the current Era, so continuation is
  STRUCTURAL, not inferred — every Goal has a clear chapter it belongs to, which is
  what stops the drift at the boundaries between loose Goals (BP-3).

  An Era is a COMPASS chapter + an `agora:era:<slug>` Issue label + an EVENTS.md
  `New Era` chapter — NOT a new data model (behaviour-preserving constraint).

  Shape of an Era entry (the 6-part fractal skeleton lands fully in US-AGORA-017;
  US-AGORA-016 carries the 5 essentials):
    - Theme / name        — what the chapter is about
    - Why it exists       — the arc it groups
    - Goals inside        — which Active Goals belong here
    - When it's finished  — the closing condition (fires the `New Era` event)
    - Next steps / backlog — follow-ups parented to this Era (slot 1)

  **Forward-only (RP-AGORA-004 open-q 2):** the first Era is opened forward, NOT
  retro-fitted over history. Active Goals that predate the Era tier stay un-chaptered
  until a future Era claims them or they close — retro-chunking all history would
  cost capture-time for no memory benefit.

  **Backlog = an empty Era** — a not-yet-started chapter is the SAME object with its
  `start` slot (the Era-plan) not yet filled. A backlog Era has a theme + a why but
  no opened game-plan; opening it fills `start` and sessions begin inside it.
-->

## Goals (active)

## Goals (closed)

## Goal backlog (GH Issues)
