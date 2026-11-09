# The Agora method

The files under `.claude/` are the real operating text of a pipeline that has run
every day since May 2026. They are long, dense and full of their own history. This
page is the way in: what the parts are, how they connect, and how to read the
corpus without its parent repository beside you.

## The idea in one paragraph

An agent that writes code needs three things a prompt cannot give it: a memory that
survives the conversation, rules that stay true as the project changes, and a way to
turn a mistake into something that cannot happen twice. Agora supplies all three with
plain files. Sessions are recorded. Rules live in one place and are mirrored, never
copied. And every lesson is sorted by how it should be kept — the strongest form
being a check that fails the build.

## Four layers

| Layer | Lives in | Does |
|---|---|---|
| **Orchestration** | `/agora`, `/plaza` | brackets the work; plans, routes, records, reflects |
| **Skills** | `.claude/skills/<name>/SKILL.md` | packaged workflows the agent invokes by name |
| **Policies** | `.claude/policies/policy-*.md` | rules every skill and every direct edit must respect |
| **Tools and state** | `agora_checks/`, `.claude/sessions/` | the checks, the session writers, the record |

The layers point one way. A skill applies a policy; a policy is never invoked. The
orchestrator never does a skill's work — it lays out the queue and ticks it off. The
one arrow that runs back up is the learning loop, below.

## The session bracket

All work happens inside a session, and a session is a file.

**`/agora --start`** reads before it proposes anything. It loads the baton the last
session left, re-checks every pointer in it (is that Issue still open? does that
branch still exist?), reconciles the planning cache against the tracker, and only
then suggests what to do. The user steers. The plan and the repo plan — branch,
expected commits, push — go to the user as one proposal, and nothing is written
until the user nods.

**During the session** each phase ends at a gate. The phase box in the session file
flips only together with a recorded nod, in the user's words. A gate that was not
asked cannot be recorded as fired; `agora_checks.session.tick` refuses without one.

**`/agora --end`** produces one thing: the close-out paper. It carries the commits,
grouped by concern, and the XP each skill earned. It routes each lesson to its home.
It holds an audit of the session, a drafted retrospective, the list of things touched
and not resolved, and the baton for next time. One paper, one nod. An earlier version asked
five separate questions at the end and felt expensive; the steps were never the
cost, the gates were.

Firing a Milestone — tag, push, wait for CI green — is the only irreversible act, so
it keeps a gate of its own.

## The planning tiers

Work is planned in nested tiers: a Vision and a Mission that are restated rather than
closed, Eras that group several Goals into a chapter, Goals with success criteria,
Sub-goals that end in one commit, and the Session itself. A Milestone is an event, not
a tier: it fires when a Goal's criteria are met. The table below is generated from
[`agora/vocabulary.yaml`](../agora/vocabulary.yaml), here and in the orchestrator skill;
edit the source, not the table. *Haleluja* is the parent's name for the Milestone ceremony.

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

The planning truth lives in the issue tracker. `COMPASS.md` is a cache of it,
re-verified at every start. `THREADS.md` holds work not yet big enough for an Issue;
each thread is born with a parent and a plan. `PLANS.md` holds sessions planned in
advance. A later session loads its scope from there instead of inventing it — even one
run unattended.

## How a lesson becomes permanent

When a session goes wrong, `/learn` patches the skill that misbehaved. Before it writes
anything it classifies the lesson:

- **mechanism** — the failure is checkable. The lesson becomes a check, and the
  prose patch is only the pointer to it. This is the preferred outcome.
- **prose** — the lesson is a reading the agent must do (which file to open first,
  which question to ask). It goes into the skill's text, folded into the rule it
  changes.
- **judgment** — the lesson is a call that depends on the situation. It is written
  down as a judgment, and explicitly not as a rule.

The organising constraint behind the classification: *a mechanism the system calls
survives; a mechanism a human must remember does not.* Most of the seven checks here
started as a prose rule that failed twice. The newest is the clearest case: a reviewer
pointed out that the corpus names hundreds of things this repository does not ship, so
that observation became `shipped-refs`, a count that may only fall.

The prose-mass ratchet holds the other end. A skill that keeps absorbing incidents
grows until nobody reads it; the ratchet lets each file shrink freely and grow only by
an explicit, named exception.

## Levels

Skills are levelled `draft → used → hardened → reference`, and every step up is a
human decision through `/level`, never automatic. Each level has a metric gate and a
file the frontmatter lint can check. At `used` a skill gets a role and an experience
log. At `hardened` it must name where it does not apply and list three or more claims
that other skills rely on. At `reference` it opens with its identity.

Levels are deliberately a game. A skill earns XP only when it actually runs. So the
agent wins by routing real work to the skill that owns it, not by doing it by hand.
The epithets come from the philosophers who walked the Athenian Agora: Socrates for the
orchestrator, Solon for the levelling skill, Theophrastus for the learning skill. They
are given at the `hardened` ceremony.

## Reading the corpus

The skill and policy files are used verbatim apart from two kinds of edit.

**Mechanical.** Backlinks to the parent's session files (`[[2026-07-10-…]]`) became
dates — *lived session 2026-07-10* — 188 of them. Links to files that did not travel
lost their target and kept their text. Frontmatter lists naming skills that did not
travel were pruned.

**By hand.** About a hundred lines named the parent product or its domain: an example
commit for a laboratory page, a filter row from a ledger screen, the product's name in
a heading. Each was rewritten to a neutral example with the same lesson. The domain
check confirms the result line by line; the parent's product names are listed in
[`agora/domain-terms.yaml`](../agora/domain-terms.yaml) only as hashes.

What you will still meet is listed in the next section. Two kinds of name need no table:

- **Era and Arc names** — *La Paz* was the parent's Era for giving every entity a home
  in the interface; *La Obra* is the current one. The *Themelion-Arc* (Greek
  *themelion*, a foundation) was a five-phase cleanup inside La Paz, the *Hub-Arc* an
  earlier movement. They appear as precedents, the way case law cites a case.
- **The ceremony words** — the *Haleluja* is the Milestone ceremony; the *Schulterblick*
  (German for the glance over the shoulder before leaving a seat) is the retrospective
  check before closing any chapter.

## Referenced but not shipped

The corpus still names parts of the project it came from. The `shipped-refs` check counts
them, 859 citations today, and holds the count with a ratchet that may only fall:

| Kind | Citations | What it is |
|---|---:|---|
| `flask agora …` commands | 221 | the parent's substrate CLI, 59 commands |
| skills not in this repository | 51 | the parent's build and doctor skills, 12 of them |
| `US-AGORA-NNN` | 288 | stories in the parent's tracker, one per mechanism |
| `session YYYY-MM-DD` | 188 | the parent session where a rule was learned |
| paths (`app/`, `scripts/`, `docs/`, `tests/`) | 111 | the parent's code and documents |

The story ids and session dates are provenance, kept deliberately: they show that each
rule has a recorded reason. The commands and skills are the part a reader trips over, so
here is what the most cited ones do in the parent, and what ships in their place.

| Command | What it does in the parent | Here |
|---|---|---|
| `baton` | reads the last session's hand-off and verifies every pointer in it | `session.read_baton` |
| `open` | opens a session file from fields, refusing a second open session | `session.open_session` |
| `write close` · `write index` | close a session once its paper is written; render the index | `session.close` · `session.render_index` |
| `write evidence --kind phase-gate` | ticks a plan box and records the user's nod in one act | `session.tick` |
| `retro-context` | collects a closing session's evidence for the close-out paper | — |
| `capture` | files an improvement idea on the current improvement round | — |
| `plan` · `handoff` | load a planned session's scope; read back an unattended run's checklist | — |
| `state-check` | validates every registry-shaped state file | the `frontmatter` check, in part |
| `reconcile` | compares the planning cache with the issue tracker and the git tags | — |
| `regen` · `stats dump` | regenerate every derived artefact in dependency order | `record-consistency --fix` |
| `preflight` · `ci-local` · `gate` | run the push gate locally, CI's test job locally, one gate with its verdict | `make check` |
| `milestone` · `batches` | check a milestone's scoping; open its batch Issues | — |
| `board` · `write xp-entry` | the skills board; one graded experience entry | — |
| `env` · `devlink` · `verify-fetch` | check the dev server and database; mint and follow a login link | — |
| the other `write …` subcommands | the only writer of each state file: threads, plans, ledgers | — |

| Skill | What it does in the parent |
|---|---|
| `/fixbug` | diagnoses and fixes a bug, with a failing test first |
| `/implement-story` | builds a user story end to end, from a written plan |
| `/new-story` · `/update-story` · `/feature-plan` | write a story; reconcile a changed one; decompose a feature into a research paper and stories |
| `/iterate` | derives a manual test plan and triages feedback |
| `/check-page` · `/check-ui-entity` | audit one page's structure; audit one entity's whole surface |
| `/wiki` · `/check-coverage` · `/manage-translations` · `/selenium` | doctors for the wiki, test coverage, translations and the browser suite |
| `/deploy` | sets up, deploys and verifies the application |

A child writes its own build skills; the eight here are the ones that run the method.

## What a child takes

A child copies `.claude/`, `agora/`, `agora_checks/` and `CLAUDE.md`. Then it writes
three things of its own. The product half of `CLAUDE.md`. A COMPASS with a first Era and
Goal. And, if its corpus came from somewhere, its parent's vocabulary for the domain check.
[`examples/first-child/`](../examples/first-child/) is the smallest such child, and
`make demo` runs one session in it from start to end.
