---
name: four-eyes
title: "Four-eye principle — propose, nod, then act at transition gates"
status: active
domain: discipline
related_skills:
  - agora
  - design
  - inspect-pipeline
  - learn
  - level
  - plaza
  - write
related_lint_rules: []
---

# Four-eye principle policy

## TL;DR

1. **Apply at transition gates, not steps — and CONSOLIDATE gates that fire together.** session open (plan + repo plan, one gate) · **phase completion (mid-session)** · **session close (the close-out paper — ONE gate carrying commits, XP, dispatch, retro and Issue actions)** · Milestone firing (its own gate — a tag is irreversible) · mode switches. Never at every file edit, every tool call, every mid-loop sub-step. **Gate COUNT is itself the cost.** The US-AGORA-033 probe found `--end` expensive not for its eleven steps but for the four-to-five gates it serialized, while `--start` runs comparable machinery through one gate and is not experienced as expensive. When several proposals arrive at the same boundary, present them as **one paper with one nod**, not as a queue — but keep the summarized discipline of Rule 3, or consolidation becomes evasion. **For non-Agora skills: recognize, don't add.** `/implement-story` Phase 2b plan, `/feature-plan` decomposition, `/iterate` retro proposal — these are *already* 4-eye gates today. The policy names them; it does not multiply them. A skill that has a working natural gate adopts the policy implicitly by recognizing it; a skill with no obvious transition gate does NOT get one added just because the policy exists.
2. **Propose a default, never just list options.** A 4-eye gate is *"here's what I'd do — nod or redirect"*, never *"what do you want?"* without a recommendation. The agent names a recommended path; the user accepts, redirects, or asks for alternatives. Deferring decisions to the user is a *failure mode*, not the point of the gate. **Mechanism: prose is the default; a picker dialog (`AskUserQuestion`) is reserved for clean either/or separation.** A planning/discussion gate is a conversation — state the recommendation + reasoning in prose and invite a nod-or-redirect, so the user can read the reasoning and add free-form feedback. A dialog box *hides* the prose reasoning behind the picker and reduces the user to selecting a preset option — use it only for genuinely mutually-exclusive choices (Shape A/B/C, fix-now vs defer, promote/park/cancel), never for open discussion (`/agora` retro 2026-06-08).
3. **Summarized, not detailed.** The proposal fits in one glance — grouped files + one-line subjects (commit-tree triage), plan phases + one-line gates (session open), N criteria max (Milestone firing). Full bodies after the nod, never before. Detailed proposals turn "nod" into reflexive rubber-stamping; the user can't pattern-spot in a wall of text.
4. **Smoke-test pass ≠ user nod.** Tooling green (ruff, tests, lint, type-check, smoke verification) is a *prerequisite* to asking, never a substitute for asking. The 4-eye gate fires only on explicit textual "yes" / "nod" / "go" / equivalent — never inferred from "tests passed".
5. **The gate is bidirectional — for tweaks, not just safety.** The user's nod often includes *"while we're there, also do X"* or *"wait, what about Y?"*. The gate is half error-prevention, half small-improvement discovery. The agent treats redirects as expected, not as cost.

## Audience

This policy has two audiences with different obligations:

- **`/agora`** is the **primary enforcer**. Agora *is* the transition layer of the pipeline (session open, commit groupings, Milestone firing, mode switches), so every rule lands somewhere in its skill prompt. The patches that accompany this policy add explicit citations at the three existing transition gates in `agora/SKILL.md` (step 1.4, commit-tree triage, step 2.2 Milestone check).

- **All other skills** adopt the policy by **recognition, not addition**. Most pipeline skills already have natural transition gates — `/implement-story` Phase 2b plan, `/feature-plan` Phase D decomposition write-step, `/iterate` retro proposal, `/document --policy` body draft, `/update-story` change proposal. They already follow rules 2–5 implicitly. The policy names what they do; it does NOT instruct them to add new ceremony. A skill must NOT introduce a new 4-eye gate at a non-transition point just because the policy exists. When a skill's existing gate falls short of one of the 5 rules (e.g. proposes options without a default, dumps full bodies before the nod), a future `/learn` patch on that skill cites this policy and corrects the gate — that's the only path for non-Agora skills to actively engage with the policy.

## Why this exists

The 2026-05-17 session (`agora-issues-integration`) closed feeling *"sprint-y, not smooth sailing"*. The user observed afterward: *"the conversation should have gone that you summarized your plan, so that I can look over and nod."* Auto-mode advanced through natural review points without asking — not because gates were missing, but because they weren't *named*. The commit-tree triage already had a summarized-plan-then-go gate (`policy-commit-discipline` Rule 4), but `/agora`'s **session open** (step 1.4) and **Milestone firing** (step 2.2) had only weak procedural prose — easy to glide past in auto-mode.

The previous session's retrospective also surfaced the *"smoke pass ≠ user confirmation"* failure mode in an early session (2026-05-16): smoke tests green is a prerequisite, not consent. That finding was a 4-eye policy waiting to be named.

The policy lifts the implicit "propose, summarize, default, nod, tweak" pattern from one skill's prose into a named cross-cutting discipline that `/agora` enforces structurally and other skills recognize at their existing gates. The bidirectional framing (Rule 5) matters: the user explicitly named the *tweaks-and-improvements* benefit — a quick glance often surfaces *"while we're there, also do X"* — turning the gate from a checkpoint into a conversation.

## The rules

### 1. Apply at transition gates, not steps — recognize, don't add

**What:** Fire the 4-eye gate at the boundaries between phases of work, not at every sub-step. The transition gates Agora cares about are: **(a)** session open — agreeing on the skill-pipeline plan; **(b)** commit groupings — proposing which files go in which commit with which subject; **(c)** **phase completion (mid-session)** — at every mid-session phase boundary, surfacing *"Phase X complete — proceed to Y, or more under X?"* before flipping the session-plan checkbox; **(d)** Milestone firing — confirming the Goal's success criteria are met before tagging + pushing; **(e)** mode switches — going from `--start` to `--end`, escalating a spawn from `write` to `commit` tier, entering `--plaza`.

The **phase-completion gate** (1.c, added 2026-05-23 by US-AGORA-003) is `/agora`-specific — it lives in the `/agora` SKILL.md "Between phases" standing instruction, NOT in the table of non-Agora skills' natural gates below. Two edges where it deliberately does NOT fire: **before the first phase** (the session-open gate at 1.a already covers it) and **after the last phase** (`/agora --end` is the next gate at 1.e). The gate fires *strictly between* phases.

Inside a skill's normal mid-loop work, the gate does NOT fire. `/implement-story` editing 12 files between Phase 2b's plan agreement and Phase 4's verification does not stop after each file to ask for a nod — that's the failure mode Rule 1 explicitly excludes. The phase-completion gate is the boundary *between* a session's `### Phase X` blocks; it is not a nod-per-file gate inside one phase.

**For non-Agora skills: recognize the gates you already have.** Most pipeline skills have a natural transition gate today that does this work:

| Skill | Existing transition gate |
|---|---|
| `/implement-story` | Phase 2b plan review before code |
| `/feature-plan` | Phase D decomposition table before story-writing |
| `/iterate` | Retro proposal before patches |
| `/document --policy` | Outline before full body |
| `/update-story` | Change summary before edits |
| `/learn` | Patch proposal before applying |

A skill on this list adopts the policy implicitly — its existing gate IS the 4-eye gate. A skill not on this list must NOT add one just because the policy exists. The principle is enforced primarily by `/agora` because Agora *is* the transition layer; other skills are addressed by recognition.

**Why:** Without the boundary discipline, two failure modes appear. **Bureaucracy creep:** if the gate fires at every step, work that should take 10 minutes takes 40 with no benefit. **Ceremony multiplication:** if every skill thinks it needs to add a 4-eye gate, the pipeline ends up with twice as many proposals and twice as many nods for the same work. The "recognize, don't add" framing keeps the policy weight on the one skill where it actually structures the work.

**Where enforced:** `/agora` SKILL.md step 1.4, commit-tree triage, step 2.2 (skill prompt); other skills' existing gates (skill prompt + self).

### 2. Propose a default, never just list options

**What:** Every 4-eye gate names a recommended path. *"Here's what I'd do — nod or redirect."* The proposal includes the rationale in one sentence and stops. The agent never presents a menu and asks the user to pick blind.

**Why:** A gate that defers the decision to the user is not a 4-eye gate — it's an interruption. The point of the gate is to surface the agent's *intended* action so the user can pattern-spot, not to dump options into the user's lap. The failure mode this rule prevents is "I learned the gate exists, so I'll ask about everything" — turning the discipline into an excuse to stop deciding.

**Where enforced:** `/agora` skill prompt; other skills' natural gates (skill prompt).

**Example:**

```
# bad — no default, the user has to pick blind
"Should I (a) commit each phase separately, (b) bundle phases A+B,
 or (c) use a single commit?"

# good — proposes a default, invites redirect
"I'll commit per phase (A, B, C, D, E separately) — five commits
 total. Phase A is the policy + agora patches; phase B is the
 --plaza mode work; etc. Nod or redirect."
```

### 3. Summarized, not detailed

**What:** The proposal fits in one glance. Concretely: grouped files + one-line subjects per commit (the commit-tree triage standard from `policy-commit-discipline` Rule 4); plan phases + one-line gate description (session open); the success-criteria checklist + closure proof per criterion (Milestone firing). Full bodies — commit message bodies, policy body text, complete diffs — come *after* the nod, never before.

**Why:** Detailed proposals turn "nod" into reflexive rubber-stamping. The user can't pattern-spot in a wall of text — they skim, they say "go", and the actual hazard ships unreviewed. The summarized form forces the agent to identify what's *load-bearing* at the boundary and surface only that.

**Where enforced:** `/agora` commit-tree triage step 5 + step 1.4 + step 2.2 (skill prompt); `policy-commit-discipline` Rule 4 (skill prompt).

### 4. Smoke-test pass ≠ user nod

**What:** Tooling green (ruff, pytest, frontmatter lint, requirements lint, type-check, ad-hoc smoke verification) is a **prerequisite** to asking for the nod. It is never a substitute for asking. The 4-eye gate fires only on explicit textual confirmation from the user — "yes", "nod", "go", "commit it", "approve", or an equivalent affirmative. Never inferred from "tests passed". **This applies at every transition gate named in Rule 1** — session open, commit groupings, **phase completion**, Milestone firing, mode switches. Green tooling at the end of a phase does NOT auto-flip the session-plan checkbox any more than green tooling auto-commits.

**Why:** An early session (2026-05-16) surfaced this exact pattern at the commit-groupings gate: the agent ran smoke tests, saw them green, and committed unprompted — interpreting the green light as consent. The cost was a `git reset --soft` and a replan. The 2026-05-23 drift-sweep session surfaced the same pattern at the *phase boundary*: Phase H bundled three independent features because the previous phase's tests passed and the agent auto-chained. The discipline costs roughly 30 seconds of waiting for a typed "go"; the bypass at any gate costs an unwound commit, a re-scoped phase, or the trust hit of having to ask the user to undo work.

**Where enforced:** `/agora` commit-tree triage step 5 + step 6 + "Between phases" standing instruction (skill prompt); `policy-commit-discipline` Rule 4 (skill prompt).

### 5. The gate is bidirectional — for tweaks, not just safety

**What:** The user's nod often is not a pure "yes". It frequently contains *"while we're there, also do X"*, *"that one — flip the wording on it"*, or *"wait, what about Y?"*. The agent treats those redirects as the *expected* outcome of a 4-eye gate, not as cost.

**Why:** Framing the gate as pure error-prevention misses half its value. A summarized proposal is a *thinking surface* for the user — seeing the agent's intended action laid out compactly often surfaces "now that you mention it, also..." that the user wouldn't have brought up without the prompt. The 2026-05-17 retro named this benefit explicitly: *"it can also lead to improvements and tweaks."* The agent that treats redirects as overhead misses this; the agent that expects them keeps the gate productive.

**Where enforced:** `/agora` skill prompt (procedural — depends on the AI internalizing the framing); self.

## Common mistakes

- **Firing the gate at every step.** A nod per file edit is bureaucracy creep. The gate fires at the *boundary*, not inside the loop. (Rule 1)
- **Adding a 4-eye gate to a non-transition point in a non-Agora skill.** *"This skill should ask the user before each test run"* is the failure mode Rule 1 explicitly prevents. Non-Agora skills recognize, don't add. (Rule 1)
- **Auto-chaining phases when smoke tests pass.** The 2026-05-23 drift-sweep session bundled refresh + PDF zoom + sign-modal layering into a single Phase H because the previous phase's smoke tests passed and the agent advanced without asking. The phase-completion gate (Rule 1.c, added 2026-05-23) is the structural fix: tooling-green at end-of-phase is the prerequisite to surfacing *"Phase X complete — proceed to Y, or more under X?"*, never a substitute for it. (Rule 1 + Rule 4)
- **Listing options without a default.** "(a) policy, (b) skill-patch, (c) both — which do you prefer?" without a recommendation. The agent's job at the gate is to *propose*, not to defer. (Rule 2)
- **Dumping the full commit body / policy body / wireframe before the nod.** The user skims a wall of text, says "go", and the hazard ships unreviewed. Summarize first, draft after. (Rule 3)
- **Inferring consent from green tooling.** "Tests passed, so I committed" is the smoke-test bypass. Tooling green is the *floor* to ask from, never the answer itself. (Rule 4)
- **Treating user redirects as overhead.** *"They keep changing the plan"* is the wrong frame — that IS the gate working. Redirects are the discovery half of the value. (Rule 5)

## See also

- [`policy-commit-discipline`](policy-commit-discipline.md) — Rule 4 of commit discipline ("summarized plan, then go") is a specific instance of four-eye principle rules 2 + 3 + 4. The two policies are layered: commit-discipline says *what* to propose at the commit-tree triage; four-eyes says *how* to propose at any transition gate.
- `.claude/skills/agora/SKILL.md` — the primary enforcer. Step 1.4 (session plan), the commit-tree triage (step 1.3 / 2.1), step 2.2 (Milestone firing), and MODE-switch points all cite this policy.
- [`policy-spawns`](policy-spawns.md) — Rule 2's authorization tiers (`advisory` / `write` / `commit` declared in the briefing) are also a four-eye gate: the user sees the tier in the briefing and nods on it before the spawn dispatches. Tier escalation mid-spawn re-invokes the gate.
