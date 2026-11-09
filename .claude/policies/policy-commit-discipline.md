---
name: commit-discipline
title: Commit discipline — one concern per commit, properly documented, clean tree at session boundaries
status: active
domain: discipline
related_skills:
  - agora
  - learn
  - plaza
related_lint_rules: []
---

# Commit discipline policy

## TL;DR

1. **One commit, one concern.** Stage deliberately by path — never `git add -A` / `git add .`. Each commit is a single coherent change describable in one line.
2. **Conventional-commit messages.** `type(scope): summary` — `feat` / `fix` / `refactor` / `docs` / `test` / `chore` — imperative mood, ≤72-char subject. Reference the story id (`US-XXX-NNN`) when the change implements or advances one. **The `commit-msg` hook refuses a subject outside the form or over 72 characters** (US-AGORA-099); the detail belongs in the body.
3. **Co-author trailer is mandatory.** Every commit message ends with a `Co-Authored-By: Claude <model name> <noreply@anthropic.com>` trailer naming the model that actually authored the commit (per the harness's standing instruction — e.g. `Claude Fable 5`); never a stale hardcoded model.
4. **Commit only on explicit textual confirmation — declared at `--start`, executed at `--end`.** `/agora --start` (1.4c) proposes the session's **repo plan** (branch — a feature branch by default for non-trivial build work, **one branch per Milestone**; expected commit groupings; push disposition) on the session-plan gate the user is already reading. `--end`'s **close-out paper** (2.10) then proposes the actual commits as one section — **summarized**: grouped files + one-line subjects, no full bodies — compared against what was declared, and the user's **single nod** authorizes them. Full bodies are written only after that nod: presenting them in the proposal turns "go" into a rubber-stamp of text the user may not have read carefully. Smoke tests passing, ruff clean, manual verification — none of these are user confirmation; they are *prerequisites* to asking. **Auto-push fires only when the plan declared it, the close-gate is green, and the tree matches the declared groupings**; any divergence falls back to explicit confirm-then-push, and firing a Milestone tag is never automatic (2.2 keeps its own gate). The gate moved *earlier*, not away. Inside an open Milestone the branch is not composed at 1.4c but **read from the Goal's declaration and checked** — `flask agora milestone --goal "<Goal>"` (US-AGORA-039) reports batches / branch / CI and flags a session branch that diverges from the one the Milestone declares. **Named exception — the bot-PR amendment (AGORA-DECL §6, ruling 6; US-AGORA-110):** an unattended job commits to its own `bot/` branch and opens a PR; that PR is a proposal, the merge is the four-eye gate, and nothing merges or closes unattended.
5. **Milestones open and close clean, pushed, and green. Sessions may park between them.** `/agora --start` triages the previous session's leftovers; `/agora --end` triages this session's commits and always retros. When a session reaches a targeted Milestone, the ceremony fires — `flask stats dump` + annotated `git tag milestone-<slug>` + push + wait for CI green. When a session parks without a Milestone, it commits cleanly; push is optional; no CI gate. Uncommitted work never spans a session boundary.

## Why this exists

At the time this policy was written the working tree held **25 modified files** — CSS, templates, admin lists, tests, docs, stats — accumulated across multiple sessions with not one commit. Nobody can review that, `git bisect` it, or revert one piece of it; the design rationale for each change lives only in chat history that is already gone. That blob is the failure mode this policy prevents.

The repo's history already *trends* toward discipline — recent commits use `feat:` / `feat(<scope>):` and cite story ids in parens — but inconsistently (`Refactor the results section and update landing page functionality` has no type and bundles two concerns). This policy makes the good pattern the rule, and gives `/agora` a concrete standard to enforce at session boundaries so the tree never silently drifts into a blob again.

## The rules

### 1. One commit, one concern — stage deliberately

**What:** Stage by explicit path (`git add <path> <path> …`), never `git add -A` or `git add .`. If the working tree holds two unrelated changes, that is two commits. A commit message that needs the word "and", a bullet list, or a changelog is the signal that it should be split.

**Why:** Deliberate staging is what keeps `git log` reviewable and `git bisect` meaningful. The 25-file blob happened because every session deferred staging "to be safe" and swept everything together.

**Where enforced:** `/agora --start` and `--end` commit-tree triage; `self` for direct commits.

**Example:**

```
# bad — one commit, six unrelated concerns
git add -A && git commit -m "ui tweaks and test fixes and docs"

# good — three commits, staged by path
git add src/components/table.css src/pages/orders_list.html
git commit -m "feat(orders): adopt the table component on the list page"
git add tests/test_orders_list.py tests/js/row_disclosure.test.js
git commit -m "test(orders): cover row disclosure on the list page"
git add docs/pages/orders.md docs/stats.yaml
git commit -m "docs: refresh the orders page doc and the stats"
```

### 2. Conventional-commit message form

**What:** `type(scope): summary`. Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore` — plus the rest of the conventional-commits set (`perf`, `build`, `ci`, `style`, `revert`) and `level`, `policy-skill-progression`'s promotion-marker subject. Imperative mood ("add", not "added"). Subject ≤72 chars. A body (after a blank line) explains *why* when the change isn't self-evident. Reference the story id (`US-XXX-NNN`) in the subject parens or the body when the commit implements or advances one.

**Why:** A consistent form makes `git log --oneline` scannable, lets tooling group commits by type/scope, and ties code back to the catalogue. The repo already half-does this — codifying it removes the guesswork.

**Where enforced:** `scripts/git_hooks/commit-msg` (US-AGORA-099) refuses a subject that is not `type(scope): summary` with one of those types, or that runs past 72 characters — counted in characters, so an em dash is one; git's own subjects (`Merge …`, `Revert "…"`, `fixup!`, `squash!`, `amend!`) pass. The check is shell, so an ordinary commit starts no Python. Before the hook, 148 of the last 200 subjects ran past 72 (the longest 198): the rule was prose the history did not hold. Also `/agora` commit-tree triage; `self`.

### 3. Co-author trailer is mandatory

**What:** Every commit message ends with a trailer of the shape `Co-Authored-By: Claude <model name> <noreply@anthropic.com>`, naming the model that actually authored the commit — the harness's current standing instruction is the authority on the exact name (e.g. `Claude Fable 5`; earlier eras used `Claude Opus 4.7 (1M context)`). PR bodies end with the `🤖 Generated with [Claude Code](https://claude.com/claude-code)` line.

**Why:** Provenance — the trailer distinguishes AI-assisted commits in the history AND records *which* model authored them, which is only true if the name tracks the actual model rather than a hardcode that goes stale on a model upgrade (lived 2026-07-23: this rule still said "Opus 4.7" while Fable 5 had been committing for weeks). It is not optional; a commit without it is a policy violation `/agora` will flag.

**Where enforced:** harness standing instruction + `/agora` commit-tree triage.

### 4. Commit only on explicit ask or confirmation — the gate is at `--start`, executed at `--end`

**What:** Neither `/agora` nor any other skill commits unprompted. The confirmation happens **twice over, at two different granularities**:

- **At `--start` (step 1.4c)** — `/agora` proposes the session's **repo plan**: branch (`main` vs a proposed `feat/<slug>`; for non-trivial feature/build work a feature branch is the default, **one branch per Milestone**), the expected commit groupings, and the push disposition. This rides the session-plan 4-eye gate the user is already reading — one more line, not a new gate. Recorded as `repo_plan:` in the session frontmatter.
- **At `--end` (step 2.10)** — the close-out paper proposes the **actual** commits as one of its sections, comparing them against what `--start` declared and surfacing only the *differences*. The user's single nod on the paper authorizes them. Full commit bodies are written **after** that nod, never before.

**Auto-push fires only when three conditions hold**: the plan declared it at `--start`, the close-gate preflight is green, and the tree matches the declared groupings. **Any divergence falls back to the explicit confirm-then-push path.** Firing a Milestone tag is *never* automatic — `--end` 2.2 keeps its own separate gate, because a tag is the one irreversible act in the close.

**Why:** Commits and pushes are outward-facing and hard to reverse, so a gate must exist — but the *placement* was wrong. `--end` is where the conversation has been running longest, context is most compacted and the user is most tired: the worst moment for a structural decision. It showed — the branch-vs-`main` call was missed twice (both §0 User-Hub sessions committed a whole feature straight to `main`), and the pre-push hook's stats companion was mishandled three times in one session. `--start` has every input the decision needs and none of the fatigue.

**The gate moved earlier; it did not disappear.** Amended 2026-07-26 by US-AGORA-036 together with US-AGORA-034's gate consolidation, per the US-AGORA-033 probe finding that `--end` is expensive because of *gate count*, not step count.

**The named exception — the bot-PR amendment** (round 8, R4; AGORA-DECL §6, ruling 6; US-AGORA-110). The light mode's weekly job (`scripts/ops/linux/run_plaza_light.sh`) commits without a person present — to a `bot/plaza-light-<year>-W<week>` branch in a dedicated worktree, never to a branch a person works on — and opens a PR. The rule's gate is not removed but **moved to the merge**: the PR is a proposal, the user reads it and merges or closes, and nothing merges, closes or changes other state unattended. The wrapper's own refusals (one file, an allowlist, a size budget) are what make the unattended commit safe to propose.

**Where enforced:** `/agora` skill prompt (`--start` 1.4c declares, `--end` 2.1 compares, 2.10 gates); harness standing instruction.

### 5. Milestones open and close clean, pushed, and green. Sessions may park between them.

**What:** `/agora --start` triages whatever the previous session left uncommitted *before* new work begins. `/agora --end` always runs the commit-tree triage and always runs the retrospective. Whether `--end` fires the push + CI-green ceremony depends on whether a **Milestone** was reached: when a Goal's success criteria are met this session, `--end` runs `flask stats dump` + annotated `git tag milestone-<slug>` + push + waits for CI green + Haleluja. When the session is advancing a Goal but not closing it, or is exploration-only, `--end` parks: commits stage cleanly, push is optional, no CI gate. Uncommitted work never spans a session boundary, and a Milestone-closing session is never red or unpushed.

**Why:** Tying the push + CI-green ceremony to the session boundary turned every `--end` into a forced close — a freestyle session that hadn't reached a Goal got the same close-pressure as one that had. The fix is to bind the ceremony to the **Milestone event**: the celebration fires when there's something to celebrate. Sessions become honest about what they are — some reach a Goal, most just advance one. The clean-tree-at-boundary rule is preserved (commits still happen at session close); the green-and-pushed gate moves to where it earns its weight. Recurring CI fixes are themselves a signal — the same pipeline failure across Milestones is a `/document --policy` candidate so the fix is captured once.

**Where enforced:** `/agora` start sequence (1.3) + end sequence (2.1, 2.2 Path A/B, 2.6).

## Common mistakes

- **`git add -A` "to be safe"** — sweeps unrelated changes, local settings, and lock files into one unreviewable commit. Stage by path.
- **Changelog commit messages** — "update X, fix Y, also Z" is three commits wearing one hat. The "and" is the tell.
- **Deferring all commits to "later"** — later is the 25-file blob. Commit at the natural seams as work completes, and always at session boundaries.
- **Dropping the co-author trailer** — easy to forget on a quick fix; it is still mandatory.
- **Committing generated / throwaway files** — `.claude/scheduled_tasks.lock`, `.claude/settings.local.json`, build artefacts. Staging by path (Rule 1) prevents this for free.
- **Treating every session end as a Milestone** — forcing push + CI green on a session that only advanced a Goal turns `/agora --end` into ceremony theater. If no Milestone was reached, park clean and move on; ceremony fires at Milestone reach, not at clock-end.
- **Closing a Milestone red or unpushed** — when a session *does* reach a Milestone, "I tagged locally, I'll push later" is a broken-`main`-on-the-next-session waiting to happen. Path A of `--end` 2.2 does not exit until pushed and green (Rule 5).

## See also

- `.claude/skills/agora/SKILL.md` — the session orchestrator; its start and end sequences are where this policy is enforced
- [`.claude/sessions/README.md`](../sessions/README.md) — the session protocol file records each commit the triage produces
- [`policy-documentation`](policy-documentation.md) — the division of labour: commit messages hold *what changed*, implementation plans hold *what we tried and why* — neither substitutes for the other
