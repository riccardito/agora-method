# Agora planned-session registry

The single home for **planned sessions** — scoped units of future work, each
carrying the gate a blind run needs, waiting for their turn. Built 2026-07-26
(US-AGORA-037) as [`THREADS.md`](THREADS.md)'s sibling: that file replaced the
per-session copy-forward for *work items*; this one does the same for *plans*.

The problem it solves: a plan produced by a planning session used to live as
**conversation plus an Issue comment**, so the build session that consumed it
re-derived its own understanding rather than *loading* it. The documented cost —
a blind session that composes scope at its own opening gate comes back with work
two-thirds undone (session 2026-07-10). A blind session **cannot
stop to re-scope**, which makes loadability a correctness property, not a
convenience.

## Rules

1. **One plan, one block, one id.** `P-NNN` ids are append-only; the counter
   never resets. **The counter is written by `flask agora plan --draft`**, which
   reserves the id it hands out (US-AGORA-107), and `flask agora state-check` reds
   when `Next id:` is not above every `### P-NNN` -- never bump it by hand.

2. **Status is DERIVED, never written here.** A plan is `ready` when its gate is
   complete and no session claims it; `loaded` when an **open** session declares
   `plan_ref: P-NNN`; `done` when a **closed** one does. The registry holds
   *definitions*; the session files hold *state*. Nothing to keep in sync, so
   nothing can drift — the same discipline `flask agora retro-context` uses when
   it reads commits from `git log` rather than from a frontmatter claim.
   **An emitted plan is not a loaded one:** `plan --draft` writes the reserved id
   into the drafting session's `plans_emitted:`, and an id a session lists there is
   never read from its `plan_ref:` as a claim. A plan whose `prerequisite:` (or
   `after:`) names a plan not yet `done` derives **`blocked`**, and `--load`
   refuses it.

3. **Seven fields are the gate — a plan missing any one is NOT loadable.**
   `flask agora plan --load` **refuses** with exit 2 and names what is missing.
   A loader that merely warns is a rule with extra steps.

   | Field | What it answers |
   |---|---|
   | **parent** | the Goal / Era / Issue this lives under |
   | **scope** | the members — what the run delivers, one line each |
   | **done means** | what "done" looks like (037 AC4, the testing gate) |
   | **verified by** | *how* it is verified — the suite, the walk, the check |
   | **repo** | branch · commit groupings · push disposition |
   | **autonomy** | what the run may decide alone, and what it must not |
   | **fan-out** | the spawn units + their allowlists **diffed against each other AND against the files the parent walks inline**, or `inline — <why>` |

   **`fan-out` is mandatory and never blank.** Its omission is the lived
   first-blind-session miss — that run never used spawns at all, because fan-out
   was not on the opening gate and separable build-heavy units got walked inline
   (session 2026-07-09). `inline — <why>` is a
   complete answer; *silence* is not.

   And the **diff is part of the field, not a later step**: a spawn whose
   allowlist collides with a file the parent holds inline cannot be dispatched at
   all, so discovering the collision at dispatch time means the phase silently
   does not happen — a planned spawn never ran, and its work carried to the next
   session (session 2026-07-10). Writing the allowlists beside the
   parent's inline files is what makes the collision visible while it is still
   cheap.

   **Optional fields the gate also reads** (US-AGORA-107): `prerequisite:` /
   `after:` (the plans that must be `done` first), `tree:` (where the commands run,
   for a child repository's plan). `flask agora plan --check P-NNN` runs the whole
   gate without loading: the seven fields, the prerequisite, and every backticked
   `verified by` command resolved against the tree -- a `--cov=` that names a
   FILE, or a `tests/` / `scripts/` path not in the tree, is a refusal. An
   `autonomy` that says what the run may do but not what the **parent may
   author** itself is a warning.

4. **Partial planning is first-class.** `part: N of M` splits a plan across
   sessions — plan part 1 now, part 2 later. Each part is its own `P-NNN` block
   with its own gate; loading picks up the part whose turn it is.

5. **Prose is parsed, never a form.** These blocks are readable markdown a human
   writes and edits. A fill-in template someone must remember to complete is the
   failure mode this round exists to kill (the US-AGORA-035 precedent).

6. **Done plans move to `## Archive`.** Keep the last ~10; git history is the
   archive proper. The move is a write path (US-AGORA-067): `flask agora write
   plan-archive P-NNN` moves ONE block whose derived status is `done` to the top
   of the archive, `--all-done --prune 10` archives every done plan and keeps the
   newest ten -- never a hand move (the block sat empty for three months while
   the rule said "move").

Next id: **P-001**

## Ready

## Archive
