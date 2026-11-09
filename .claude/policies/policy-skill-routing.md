---
name: skill-routing
title: "Skill routing — route work to skills, inline is the justified exception"
status: active
domain: discipline
related_skills:
  - agora
  - inspect-pipeline
related_lint_rules: []
---

# Skill routing policy

## TL;DR

1. **Route by default; inline is the named exception.** When non-trivial work matches an existing skill's purpose, invoke the skill — even if the user didn't name it. Doing it inline requires a **one-phrase justification** (no skill covers it · genuinely trivial · needs in-flight context a fresh invocation would lose). **Bugs route to `/fixbug` by default** — anything with a root cause worth diagnosing (misbehaviour, wrong style, silent data loss), even mid-session, even when the fix looks small, **and even when a sweep surfaced it** — a defect found inside a conversion or completeness sweep reads as part of the sweep and is not (lived twice, session 2026-09-01 · session 2026-09-02); a one-line typo or an in-flight tweak during a live verify round with the user present is the named exception (the 2026-07-29 ruling) — **a gate redirect that births or reshapes a STORY is not an in-flight tweak: it routes to `/new-story --from-plan` / `/update-story`** (lived session 2026-09-19: two stories authored inline at a ruling gate; `retro-context` warns on a `fix(`-typed seam with no `/fixbug` in the record — a sweep's own seam is `feat(`-typed, which is why the case is named here, not left to the check).
2. **The harness rule covers explicit invocation; this policy covers proactive routing.** When the user *types* `/skill` you must invoke it (the harness BLOCKING rule). This policy extends that to work the user *described but didn't name* — the gap where "felt faster inline" drift lives.
3. **Routing is how the agent wins the leveling game.** A skill earns M1 + XP only when it appears in `skills_invoked:` — it literally cannot level if unused. The agent's job in Agora is to level the skills; routing real work to them *is* the win condition (per [`policy-skill-progression`](policy-skill-progression.md)).
4. **Planned at `--start`, caught at `--end`.** `/agora --start` step 1.4 routes planned work to skills; `/agora --end`'s **close-out paper** (2.10) surfaces every "did inline what a skill exists for" as a **missed-routing finding** that feeds the next session's plan.
5. **"Faster inline" is the smell, not the signal.** Inline feels faster because it skips the skill's scaffolding — but that scaffolding (surface-confirm gates, registry checks, wiki seeds, plan files) is what prevents the iteration rounds that cost *more* than it saved. Speed-to-goal counts the reworks.

## Why this exists

The 2026-05-20 session (`agora-consolidate-finish`) closed with a coaching note that named the failure exactly: *"this session built features + authored stories by hand, skipping `/implement-story` and `/new-story` — whose Phase-1 surface-confirm gate would likely have caught the rebind misses before code."* The identity-badge work failed twice (wrong surface, wrong attribute) before a precise prompt shipped it — and `/implement-story`'s Phase 1.6 surface-discipline gate is built to catch precisely that class of miss. The work was done inline because inline *felt* faster; it was not.

This is a recurring pattern, not a one-off. Before this policy there was **no general rule** telling the agent to route proactively. The harness enforces *explicit* invocation — when the user types `/skill`, the Skill tool is a BLOCKING requirement. But when the user describes work in prose ("build me a reschedule feature", "fix this broken modal") without naming the skill, nothing pulled the agent toward `/implement-story` or `/fixbug`. The agent decided case-by-case, and "I can just do this directly" won too often.

The deeper fix is not a rule the agent reads and rationalises around — it is changing what the agent *wants*. Agora already has a motivation engine: the leveling system. Skills accrue M1 (invocation count) and XP **only** when they appear in a closed session's `skills_invoked:` list. A skill that is never invoked cannot level past `draft`, no matter how good it is. The agent's standing job in Agora is to grow the skill corpus — and routing real work through skills is the *only* way that happens. This policy makes that stake salient at the decision moment, so routing is the thing the agent wants to do, not the thing it's told to do.

## The rules

### 1. Route by default; inline is the named exception

**What:** When a unit of non-trivial work matches the purpose of an existing skill, invoke that skill rather than doing the work inline — regardless of whether the user named the skill. The default is *route*. Doing the work inline is permitted only with a justification that fits in one phrase, drawn from a closed set:

- **No skill covers it** — the work genuinely falls outside every skill's scope.
- **Genuinely trivial** — a one-line edit, a typo fix, a single rename; the skill's scaffolding would cost more than the task.
- **Needs in-flight context** — the work depends on state the current conversation holds that a fresh skill invocation would lose (e.g. a half-built mental model mid-debug), AND splitting it out would derail more than it saves.

If the inline justification doesn't fit one of those phrases, route to the skill.

**The bug shape, ruled 2026-07-29** (session 2026-07-29 retro, the user's words: *"we should use the fixbug more often, not by every bug, but the fixbug skill was created for exactly that, to fix bugs structurally and with experience"*): a reported bug with a **diagnosable root cause** routes to `/fixbug` by default — even mid-session, even when the fix looks small — because the skill carries the accumulated diagnostic playbook (probe design, the stale-chrome family, the hx-select traps, surface-pinned regression discipline) that an inline fix rediscovers. The named exception is the second phrase above: a **one-line typo** or an **in-flight tweak during a live verify round** with the user present stays inline. **A defect the sweep itself surfaces is the same bug shape, not a third exception:** a conversion or completeness sweep that finds a broken control in the surface it is converting reads the fix as part of the sweep — the sweep was briefed for the conversion, not for the diagnosis, and its seam is `feat(`-typed, so the check half below cannot see it. Route it (`/fixbug`, then resume the sweep), or state the one-phrase exception at the seam; lived twice in consecutive B8 sessions (session 2026-09-01 F3 · session 2026-09-02, the orders populate bug — both in the breach ledger). The check half (US-AGORA-058): `flask agora retro-context` warns at `--end` 2.0 when a session's commits carry a `fix(`-typed seam and neither `skills_invoked:` nor the Log names `/fixbug`. The ruling lives here and in the two skills' `## When NOT to use` tables; the memory file that first held it is a pointer.

**Why:** Skills carry scaffolding the inline path silently skips — surface-confirm gates, registry-completeness checks, wiki-seed authoring, implementation-plan files, the four-eye plan gate. That scaffolding is the project's accumulated defence against the exact mistakes that produce iteration rounds. Skipping it to "go faster" trades a known small cost (the skill's ceremony) for an unknown larger one (the rework when the skipped check would have caught the miss).

**Where enforced:** the agent at the decision moment (procedural); `/agora` SKILL.md step 1.4 (planned work) + the close-out paper's findings, 2.10 (missed-routing finding).

**Example:**

```
# bad — work described in prose, done inline
User: "add a reschedule button to the appointment modal"
Agent: *edits the template, the route, the JS directly*
   → skips /implement-story Phase 1.6 surface discipline + Phase 3.8 wiki seed

# good — route to the skill the work matches
User: "add a reschedule button to the appointment modal"
Agent: "This is a story-shaped change — routing to /implement-story
        (it'll confirm the surface and seed the wiki). One sec."
```

### 2. The harness rule covers explicit invocation; this policy covers proactive routing

**What:** Two distinct obligations, not one. **(a)** When the user *types* a slash command, the harness makes invoking the Skill tool a BLOCKING requirement — that is the harness's rule, not this policy's. **(b)** When the user *describes* work without naming a skill, this policy obliges the agent to recognise the match and route anyway. This policy is exactly the second clause — the proactive half the harness rule doesn't reach.

**Why:** The explicit-invoke rule is unambiguous and well-enforced; the gap was always the *implicit* case. Naming the boundary keeps the two from being conflated — "the user didn't type `/implement-story`, so I'm free to do it inline" is the rationalisation this rule closes.

**Where enforced:** the agent at the decision moment (procedural); recognised, not added — no new gate beyond `/agora`'s existing 1.4 plan gate and its single close-out gate.

### 3. Routing is how the agent wins the leveling game

**What:** Treat routing work to skills as the agent's win condition, not a tax. The mechanism is already built: per [`policy-skill-progression`](policy-skill-progression.md), a skill's M1 (invocation count) and its XP are computed *only* from its appearances in closed sessions' `skills_invoked:` frontmatter. A skill that isn't invoked earns nothing and cannot promote past `draft`. The agent's standing job in Agora is to grow and level the skill corpus — and invoking skills on real work is the only thing that moves those numbers.

**Why:** This is the motivation half of the policy, and it answers the design question the policy was born from: *can we use the XP system to make the agent want to use skills?* Yes — not by paying the agent XP (XP flows to skills, not the agent), but by making the agent's existing objective (level the corpus) and the routing decision the same act. Reframing "use the skill" from obligation to win-condition is what turns a rule the agent obeys into a behaviour the agent wants.

**Where enforced:** `policy-skill-progression` (M1 / XP computation); `/agora --end` step 2.3b (XP awards) + the close-out paper's findings, 2.10; the agent's framing (procedural).

### 4. Planned at `--start`, caught at `--end`

**What:** Skill routing is enforced at both session brackets. At **`--start` step 1.4**, the skill-pipeline plan routes the session's planned work to skills — that is the *prospective* gate. At **`--end`**, the **close-out paper** (2.10) surfaces every instance where the session **did inline what a skill exists for** as an explicit **missed-routing finding** — that is the *retrospective* catch. The finding names the skill that should have run; where it maps to a skill's XP narrative, it lands as a 🟡 lesson note for that skill at step 2.3b.

> **Note (2026-07-26).** This catch used to live in step 2.7, *prompting & skill-usage coaching*, which US-AGORA-034 **deleted** — the US-AGORA-033 probe's single genuine elimination across eleven `--end` steps. The *finding* survives and is unchanged; what went away is the register — advice addressed to the user about how they drove. It is now an observation about the session, recorded in the paper.

**Why:** A purely prospective rule misses emergent work (tasks that arise mid-session, unplanned). A purely retrospective rule only diagnoses after the cost is paid. Pairing them means planned work is routed up front and the unplanned drift is caught and fed back — the loop that makes the *next* session route better. The retrospective finding is the data that keeps the rule honest.

**Where enforced:** `/agora` SKILL.md step 1.4 (prospective) + the close-out paper, 2.10 (retrospective); `policy-four-eyes` Rule 1 (the 1.4 plan is already a transition gate).

### 5. "Faster inline" is the smell, not the signal

**What:** When the inline path feels faster than invoking the skill, treat that feeling as a signal to *check the routing rule*, not as license to skip it. The feeling is real — inline is faster *to first output*. But speed-to-goal is measured to the *verified, shipped, no-rework* state, and on that metric the skill path usually wins because its scaffolding pre-empts the reworks.

**Why:** The 2026-05-20 identity-badge work is the worked example: the inline path produced output fast, then failed twice and had to be redone — slower end-to-end than `/implement-story`'s gated path would have been. The instinct "this is faster" is calibrated to first output, which is the wrong finish line. Naming the smell lets the agent catch its own rationalisation in the moment.

**Where enforced:** the agent at the decision moment (procedural — depends on the AI internalising the framing); `/agora --end`'s close-out paper, 2.10 (names the cost when it recurs).

## Common mistakes

- **"The user didn't name the skill, so inline is fine."** The harness rule covers explicit invocation; this policy covers exactly the case where the user described the work without naming the skill. (Rule 2)
- **Inline justification that doesn't fit one phrase.** If you can't say *why* inline in one of the three allowed phrases (no skill / trivial / in-flight context), the honest answer is "route to the skill". (Rule 1)
- **Counting speed to first output, not to shipped-and-verified.** Inline wins the sprint and loses the race; the reworks the skill would have prevented are part of the time. (Rule 5)
- **Treating routing as a tax instead of the win.** A skill that isn't invoked can't level — routing real work is how the corpus grows, which is the agent's job. (Rule 3)
- **Skipping the `--end` missed-routing finding because "it worked out".** The retrospective catch is the data that makes the next session route better; record it even when the inline work shipped clean. (Rule 4)

## See also

- [`policy-skill-progression`](policy-skill-progression.md) — the motivation engine this policy leans on. M1 (invocation count) and XP are computed only from `skills_invoked:` appearances; a skill that isn't routed work cannot level. Rule 3 here makes that stake the agent's win condition.
- [`policy-four-eyes`](policy-four-eyes.md) — `/agora --start` step 1.4 (the skill-pipeline plan) is already a four-eye transition gate; this policy's Rule 4 prospective half rides on it. No new gate is added.
- [`policy-documentation`](policy-documentation.md) — Rule 4 (skill-level corrections go through `/learn`) and the canonical-home discipline; this policy is the routing counterpart — *which* skill, not *how* it's patched.
- `.claude/skills/agora/SKILL.md` — the enforcer. Step 1.4 routes planned work; the close-out paper (2.10) surfaces missed-routing findings; step 2.3b lands them as XP lessons.
