# Agora — the session layer

This folder is the **session layer of Agora**, the AI-requirements pipeline that
builds the product.
Where the policy layer holds the *rules* and the skill layer holds the
*workflows*, this layer holds the *sessions* — the temporal record of what
actually happened, one file per work session.

In the Athenian Agora's map, this is the **Centre** — the open orchestra where
the citizen stands and the conversation happens. Every other layer exists to
serve the work that gets logged here.

> The skill that owns this folder is [`/agora`](../skills/agora/SKILL.md) — the
> session orchestrator. Its `--start` sequence opens a session file; its `--end`
> sequence compacts and closes it.

---

## A note on naming — "session" vs "session"

The canonical noun for a work-window in Agora is **session** (capitalized).

The on-disk directory is `.claude/sessions/` for **historical reasons** — when
the system was bootstrapped (2026-05-14) it was named `session`; the goal
vocabulary refresh (2026-05-16, see [`COMPASS.md`](COMPASS.md) Goal "Agora
vocabulary + milestone ritual operational") settled on **session** as the right
word because "session" already overloads three other concepts:

- **assistant chat session** (the Claude Code conversation itself)
- **domain session** (the product's own meaning — a treatment session, a training session, `session_id` foreign keys)
- **HTTP/auth session** (login sessions, cookies)

The directory rename was rejected as high-churn / low-value during session
`2026-05-17-agora-issues-integration` Phase E. The directory name stays as a documented alias; prose, prompts, and the
canonical noun are **session**. Where you see "session" in this README or in
SKILL.md prose, treat it as a stale spelling pending a future pass — the
intent is always **session**.

What still legitimately uses "session" in Agora context:

- The directory path `.claude/sessions/` (this folder)
- The frontmatter key `session_id:` in every session file
- The flag names `--session` (on `/inspect-pipeline`) and `--from-session` (on `/learn`) — CLI surfaces don't churn
- This historical-naming-note section

Everything else in prose is a **session**.

---

## What a session file is

A **session protocol file** records one work session end-to-end:

- the **intent** — what the session set out to do
- the **session plan** — the queued sequence of skill invocations, as a checklist
- the **log** — a running summary of what each skill did, decisions made,
  surprises hit, and references to the docs/stories/code touched
- the **open threads** — deltas against [`THREADS.md`](THREADS.md), the
  central open-threads registry (T-NNN ids, born/resolved/promoted lifecycle,
  promote-or-drop at 3 sessions). The registry is the single home for carried
  threads; the session file records only what this session changed
- the **Agora findings** — things that should become `/learn`, `/document`, or
  `/inspect-pipeline` candidates (the feedback loop into Agora itself)
- the **close-out** — written by `/agora --end`: a compacted summary, the
  push + green-CI confirmation, the `/inspect-pipeline --session` verdict, what
  was dispatched, and a short piece of prompting/skill-usage coaching for the
  user

It is **not** a transcript. It is a *structured summary* — dense enough that a
later session (or a different agent) can pick up cold, light enough that it
doesn't try to be the chat history.

## File naming and lifecycle

```
.claude/sessions/                   ← historical directory name (kept; see naming note above)
├── README.md                       ← this file
├── _TEMPLATE.md                    ← session-file skeleton
├── INDEX.md                        ← one line per session of the CURRENT Era -- GENERATED (`flask agora write index`, US-AGORA-067)
├── INDEX-<era>.md                  ← the same for each closed Era (and `pre-era` for the sessions before the tier)
├── IMPROVEMENTS.md                 ← cumulative ledger of how Agora itself evolves
├── COMPASS.md                      ← Vision + Mission + active Goals (the STATE layer)
├── EVENTS.md                       ← event catalog (Milestone-reached / Session-park) — the TRANSITIONS layer; `--end` 2.2 follows a chapter
├── policy-breaches.md              ← append-only confirmed-policy-breach ledger (WS2; `--end` 2.7 appends, US-AGORA-011 scores)
└── YYYY-MM-DD-<slug>.md            ← one per session
```

Lifecycle:

1. **`/agora --start`** first **gets current** — it reads the last 2–3 session
   files + the `IMPROVEMENTS.md` tail, and re-inventories `.claude/skills/` +
   `.claude/policies/` (the skill never relies on a *remembered* picture of the
   system). It then reads the user's **goal prompt** and decides: does this
   goal **continue** a recent session, or start a **new** one? It triages the
   working tree *and* open PRs (`gh pr list`) so the session starts genuinely
   clean, reasons a skill-pipeline plan from the goal, and either creates
   `YYYY-MM-DD-<slug>.md` with `flask agora open` (new) or appends a phase to an
   existing file (continuation) — then `flask agora write index` renders its
   `INDEX.md` line from the frontmatter (`era:` set, `outcome:` empty → `— in progress`).
2. The session runs. The skill (or the conversation) appends to the **Log** and
   ticks the **session plan** checklist as work completes.
3. **`/agora --status`** can be run any time mid-session — read-only, reports
   plan progress + dirty-tree + open-PR state.
4. **`/agora --end`** triages this session's commits, **pushes** them when a
   Milestone is reached, and **waits for CI to go green on GitHub** — a
   Milestone-reaching session does not close red or unpushed; CI fixes are
   part of `--end`. (A session that parks without reaching a Milestone commits
   cleanly; push is optional; no CI gate — see `policy-commit-discipline`
   Rule 5.) It then compacts the log into the **Close-out**, runs
   `/inspect-pipeline --session` (which **always includes `/agora` itself**
   — the self-audit), dispatches findings to `/learn` / `/document`, flips
   `status: closed` with `flask agora write close`, writes the outcome (`flask agora write outcome` + `write index`
   re-render the `INDEX.md` line), and appends any durable
   Agora-evolution lesson to `IMPROVEMENTS.md`.

A session left `open` at the start of a new `/agora --start` is surfaced — you
either resume it or close it out first. Sessions do not silently overlap.

## Multi-agent model

Session files are **git-tracked**, so they are shareable three ways:

- **Across machines / clones** — `git pull` brings another machine's sessions in.
- **Across worktrees** — a `worktree`-isolated agent reads `.claude/sessions/`
  from its own checkout.
- **Across concurrent agents on one machine** — they share the filesystem path
  directly.

To keep concurrent writes sane:

- The `agent:` frontmatter field labels who opened the session (terminal /
  worktree / purpose). When two agents genuinely work in parallel, each opens
  its **own** session file — they do not co-write one file line-by-line.
- A later agent picking up an `open` session from a *previous* (finished)
  session is the common case and is fully supported — that is the "run `/agora`
  in multiple windows to initiate" flow. It reads the open file, continues the
  Log, and closes it.
- `INDEX.md` is generated from the session files (`flask agora write index`);
  a conflict there is resolved by re-rendering, never by hand.

## INDEX.md vs IMPROVEMENTS.md

- **`INDEX.md`** — the loadable index. One line per session: date, slug, type,
  status, one-line outcome — **rendered** from the session file's frontmatter
  (`type` · `status` · `outcome` · `era`) by `flask agora write index` and held by
  the record-consistency check; cut by Era (`INDEX-<era>.md` for a closed Era).
  The fast scan of "what has Agora been doing."
- **`IMPROVEMENTS.md`** — the durable memory of **how Agora itself gets better**.
  Per-session logs get compacted and eventually age out of relevance;
  `IMPROVEMENTS.md` does not. Every `/agora --end` that produced a real lesson
  about the pipeline — a skill patched, a policy authored, a prompting pattern
  that worked — appends one entry here. This is Agora's self-improvement ledger.

## See also

- [`/agora` skill](../skills/agora/SKILL.md) — opens, tracks, and closes session files
- [`policy-commit-discipline`](../policies/policy-commit-discipline.md) — the commit rules `/agora` enforces at session boundaries
- [`/inspect-pipeline`](../skills/inspect-pipeline/SKILL.md) — `--session` mode audits a closed session for skill/policy drift
- [`/learn`](../skills/learn/SKILL.md) — `--from-session` mode reads a session file's findings and patches the skill system
- [`COMPASS.md`](COMPASS.md) — Vision, Mission, and active Goals
- `.claude/skills/README.md` — the skill layer
- `.claude/policies/README.md` — the policy layer
