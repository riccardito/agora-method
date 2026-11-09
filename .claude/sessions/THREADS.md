# Agora open-threads registry

The single home for **open threads** — work that carries across sessions but
isn't (yet) a Goal, an Issue, or a story. Built 2026-06-12
(session 2026-06-12) to replace the per-session
copy-forward: threads used to live only in each session file's `## Open
threads`, so every `--start` re-copied them by hand (wording drifting each
hop) and anything outside the last-2-3-session read window silently died.

## Rules

1. **One thread, one block, one id.** `T-NNN` ids are append-only; the
   counter never resets. A thread is `open`, `resolved`, or `promoted`.
2. **A thread is born PLANNED, not just noted (US-AGORA-022).** Every thread
   carries two fields set **at creation**, never deferred:
   - **`parent:`** — the **Era or Goal** it lives under (the fractal skeleton's
     slot-1 *backlog*, US-AGORA-017). A thread always belongs to a chapter.
   - **`plan:`** — its **resolution plan**: *when/how* it will be resolved
     (e.g. "next `/agora --start` routes it to `/learn`", "fold into Goal #NN's
     next session", "needs a spike first"). Answering "when/how?" at birth is
     what stops a thread from trailing implementation as a loose note.
   A bare note with no parent + no plan is **not a complete thread** — it's an
   unspecified idea (slot 0); promote it to a planned thread or drop it.
3. **`/agora --start` 1.1 reads this file whole** — it is THE open-threads
   source. Session files' `## Open threads` sections hold only **this
   session's deltas** (new `T-NNN` born / resolved / promoted), never the full
   carried list.
4. **`/agora --end` 2.3 reconciles** — appends new threads with fresh ids
   (**each with its `parent:` + `plan:` — reject a bare note**), flips resolved
   ones with a one-line citing note (session + commit), marks promotions with
   the target (`→ Goal #NN` / `→ Issue #NN` / `→ US-XXX-NNN`).
5. **Promote-or-drop at 3 sessions — promote = "gets its Issue".** A thread
   surviving ≥3 sessions must be **promoted** or deliberately **dropped** with a
   note — threads are short-lived carry-overs, not a second backlog. **Promotion
   is the slot-1 → slot-0 move** (US-AGORA-017): when a thread's scope grows too
   big or diverges from its origin topic, it **earns its own GitHub Issue** (a
   Backlog Goal / sub-goal / bug Issue per `policy-issue-templates`) — that Issue
   *is* the promotion. A thread that's still small + on-topic after 3 sessions is
   dropped, not promoted (don't promote for its own sake). **Promotion runs
   through the command** (US-AGORA-058, `AGORA-DECL §6`):
   `flask agora write thread-close <tid> --promote <goal-issue>` posts the block
   on the Goal / sub-goal Issue, re-reads it, then moves the thread here. And a
   thread whose `parent:` already names an Issue (`#<n>`) is promoted at birth,
   not held — `flask agora state-check` refuses it; the registry holds only
   threads still awaiting a home (an Era, a Topic, a Goal not yet opened).
6. Resolved/promoted blocks move to the bottom section; keep the last ~20,
   prune older (git history is the archive).

Next id: **T-001**

## Open

## Resolved / promoted (newest first)
