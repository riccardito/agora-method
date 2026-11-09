---
name: spawns
title: Spawn discipline — when, how, and with what authorization
status: active
domain: discipline
related_skills:
  - agora
  - write
related_lint_rules: []
---

# Spawn discipline policy

## TL;DR

1. **Spawn when the sub-goal is separable, read-heavy, or context-budget-relieving — not as a default.** A spawn fits when (a) the sub-goal is research / drafting / web-search work, (b) walking it inline would derail the parent flow, or (c) the parent is approaching its context budget. Skills that need the parent's working tree, the parent's open changes, or the parent's full context do NOT spawn — they run inline.
2. **Authorization is per-spawn and stated in the briefing — three tiers.** `advisory` (return markdown in conversation — the default), `write` (Write/Edit allowlisted paths, NO commits), `commit` (commit allowlisted paths). Every briefing names its tier explicitly. Spawn output is **raw material** by default — the **parent's `/agora --end` commit-tree triage** stages and commits. Spawn-commits requires explicit `tier: commit` authorization in the briefing.
3. **Parallel reads OK; parallel writes never.** Multiple `advisory` spawns can run unrestricted. Multiple `write` spawns require **disjoint path allowlists** — the parent checks every open spawn's allowlist before dispatching the next one. Max **3 concurrent write-tier spawns** (the briefing-burden ceiling — past 3 the parent's bookkeeping costs more than the parallelism saves).
4. **The briefing is self-contained — five required sections.** **Background** (zero-context setup: what the parent system is, the relevant naming and abbreviations) · **Files to sweep** (concrete paths the spawn must read first) · **Constraints** (explicit "do NOT touch" path list — every file the parent is in flight on, by exact path) · **Deliverable shape** (testable: file path + structure + a size budget in the deliverable's own unit — tests, locators, rows, never lines — not "explore the area") · **Reply protocol** ("when you're done, reply with X, Y, Z — do NOT paste full file contents back"). Skipping any of the five is the most common cause of an iteration round.
5. **Delivery is auto by default; manual is the opt-in.** An **auto-spawn** is dispatched via the Agent tool — the subagent reads its own briefing file and writes its deliverable into the `## Result` block itself (no copy-paste). A **manual spawn** (copy-paste into an external window or a different model) is the opt-in alternative, used only when a *different model or separate context window* is the point. Auto delivery does NOT bypass the tier — a `write`/`commit` auto-spawn still goes through the parent's commit-tree triage.
6. **Lifecycle: clear, finite goal — then fade.** A spawn moves `open → returned → folded`. The parent folds the result into one Log entry and never touches it again (the `## Result` block is written by the subagent in auto mode, pasted by the user in manual mode). **Multi-iteration is normal** (~⅔ of real spawns iterate once or twice) — but documented **append-only** as `## Iteration 2`, `## Iteration 3` in the same spawn file. **Extra-scope discoveries come back as findings**, never as silent extension; the parent decides whether to dispatch a follow-up spawn, address inline, or park for a future session.

## Why this exists

An early session (2026-05-16) dispatched two spawns. Both worked well; the retrospective surfaced that they worked **in spite of** ad-hoc procedure, not because of explicit rules. The cost was bookkeeping the user did from memory:

- **Spawn 1 (agora-vocabulary-consolidation)** went through three iterations. The first iteration returned a markdown report; the parent then re-briefed for "write files directly, add a fourth artifact"; iteration 3 fixed four content gaps the parent flagged after reading. MODE 4 of `/agora` implied a single-shot pattern; lived experience was multi-round. Nothing in the spawn template anticipated this, so each iteration was a fresh prompt-engineering pass.
- **Spawn 2 (premium-save-toast)** escalated mid-flight from a design-only spawn (story + plan, no code) to a shipping spawn that landed 5 commits. The parent asked the spawn to ship; the spawn said yes; the authorization tier had to be re-negotiated from "design-phase, do not modify production code" to "commit five conventional commits on `main`" — a tier change that none of the existing rules acknowledged. It worked because the spawn was careful, but the discipline was ad-hoc.

Two failure modes the policy guards against:

1. **Concurrent write conflicts.** Spawn 2 nearly conflicted with the parent's settings-panel work in one route module. The accident-of-timing — parent committed the conflicting file BEFORE spawn applied its edit — saved a backup-and-replay dance. The next time the dice roll the other way, the spawn either fights the parent's later commit or silently overwrites it.
2. **Spawn drift into "ongoing".** A spawn with no clear finish line accumulates responsibilities. The user's exact phrase in the retrospective: *"A spawn must always have a clear, finite goal and then fade out."* Without an explicit lifecycle rule, a useful spawn becomes a long-running side-conversation that competes with the parent for the user's attention.

## The rules

### 1. When to spawn — separable, read-heavy, or context-budget-relieving

**What:** Spawn a sub-goal when at least one of these is true:

- **Read-only research** — internal scan + web search + drafting. The spawn produces a report; the parent applies it later.
- **Drafting in isolation** — writing a story, an implementation plan, a wiki seed, a research paper, a translation pass. The output is a finite set of files at known paths.
- **Context-budget relief** — the parent is approaching its conversation budget and the sub-goal has its own paged-in working memory (its own set of files to read, its own deliverable shape).
- **Independent parallelism** — two sub-goals that can run in parallel without sharing state. The classic case: two research spawns dispatched at once while the parent advances unrelated work.

Spawn is the **more expensive option** — it adds a briefing-write cost, a context-switch cost, and a fold-in cost. Default to inline. The bar for spawning is "would the parent be visibly worse if I did this inline?"

Do **NOT** spawn for:

- **Coordinated edits with the parent's open changes.** If the spawn would touch files the parent is in flight on, the merge is the failure mode.
- **Anything needing the parent's full context.** A spawn re-reads from scratch; if the cost of re-reading exceeds the cost of inline, the spawn is the wrong tool.
- **Trivial outputs.** A spawn that returns five bullet points is not paying for its briefing.

**Why:** The cost asymmetry. A good spawn buys parallelism + context relief; a bad spawn buys a 30-minute briefing for output the parent could have produced in 5 minutes inline. The bar exists to make the decision deliberate.

**Where enforced:** `/agora --spawn <description>` skill prompt (MODE 4). The dispatch step checks the four conditions; if none apply, refuses to spawn and asks the user to confirm.

### 2. Authorization tiers — three named levels, stated in the briefing

**What:** Every spawn briefing declares its authorization tier in the spawn file's frontmatter and re-states it in the briefing prose:

| Tier | What the spawn may do | When to use |
|------|----------------------|-------------|
| `advisory` | Return markdown in the conversation. Do not touch the filesystem. **Default.** | Research, design pass, multi-deliverable drafting where the parent wants to review-before-applying. |
| `write` | `Write` / `Edit` allowlisted paths. **Do NOT commit.** The parent's commit-tree triage commits. | Drafting files the parent has already committed to landing (a story, a plan, a wiki seed, a research paper). |
| `commit` | Commit allowlisted paths. The briefing names commit-message convention + push policy. | Shipping spawns — a feature whose design + implementation + tests + docs land inside the spawn. Rare and load-bearing; requires explicit user authorization. |

**Path allowlist is mandatory** at `write` and `commit` — a list of exact paths or path-prefixes the spawn is allowed to touch. Anything outside the allowlist is forbidden.

**Tier escalation mid-spawn is allowed** with explicit parent-to-spawn message captured as a new iteration in the spawn file. Spawn 2 (premium-save-toast) escalated from `write` (design phase) to `commit` (ship phase) — that's the supported path, not a violation. The new iteration's briefing re-states the new tier so the spawn file records the change.

**Why:** Authorization should be **explicit, not inferred**. A spawn that doesn't know whether it can commit either asks (round trip) or guesses (failure mode). Naming the tier in the briefing eliminates both. Spawn output as **raw material by default** means the parent's commit-tree triage stays the single source of commit truth — the policy-commit-discipline boundary holds even when work happens in spawns.

**Where enforced:** `/agora --spawn` briefing template; spawn file frontmatter (`tier: advisory|write|commit`, `allowlist: [paths]`). Procedural — Claude reads the tier and refuses to escalate without an explicit parent message.

### 3. Parallel reads OK; parallel writes never — concurrency rules

**What:**

- **`advisory` spawns:** unrestricted parallelism. Multiple reading spawns can dispatch at once.
- **`write` spawns:** path allowlists must be **disjoint**. Before dispatching a new `write` spawn, the parent reads every open spawn's allowlist and confirms no overlap. Max **3 concurrent `write` spawns** — past 3, the parent's bookkeeping cost (re-checking allowlists, folding N results) exceeds the parallelism gain.
- **`commit` spawns:** never run in parallel with any other write- or commit-tier spawn. The merge — two spawns committing to the same branch — is the failure mode. A `commit` spawn runs alone or alongside `advisory` spawns only.

**Why:** Two spawns writing to the same path is a race the spawn can't see. The parent is the only actor with visibility into both spawns; the parent must enforce the disjointness. The ceiling of 3 isn't a hard technical limit — it's the briefing-burden cap. Past 3, the user's bookkeeping ("which spawn does which?") becomes the bottleneck.

**Where enforced:** `/agora --spawn` dispatch step — before writing the spawn briefing, scan `.claude/sessions/spawns/*.md` for `status: open` files, read their `allowlist:` frontmatter, refuse overlap. Procedural.

### 4. Briefing template — five required sections

**What:** Every spawn briefing has five sections, in this order:

1. **Background** — zero-context setup. What's the parent system? What are the relevant proper nouns (the product, Agora, the project's terminology)? What's the sub-goal in one paragraph? The spawn starts with no knowledge of the parent conversation.
2. **Files to sweep** — concrete paths the spawn must read first. Not "look at the relevant code" — `.claude/skills/agora/SKILL.md`, `.claude/sessions/2026-05-16-<the-parent-session>.md`, etc. The list is the spawn's mental map of "the current state of the area".
3. **Constraints** — explicit "do NOT touch" path list. Every file the parent is in flight on, named by exact path. Plus: do NOT run global commands (`flask stats dump`, `pytest tests/`, `pybabel extract` from project root) — those are parent's responsibility. **And name a scratch location OUTSIDE the repository** — a spawn that needs a helper script must write it to its OS temp directory, never to the working tree. Lived 2026-07-25: a translation spawn left a 0-byte `scratch_patch_pt.py` at the repo root; harmless in itself, but it is an allowlist breach and it pollutes the parent's commit-tree triage with an untracked file the parent must recognise as not-its-own before staging. It was caught by a *sibling* agent's report, not by the agent that made it — self-reports do not cover files the agent forgot it wrote.
4. **Deliverable shape** — testable. File paths the spawn produces, structure (headings, table shape), and a size budget in the deliverable's OWN unit — "2–4 tests per use case", "≤ N locators", "≤ N rows" — never a line count: the house style runs ~70 lines per browser test with cited locators, so a line budget can only be met by stripping the citations the parent wants (three C5 spawns overran a line budget 1.5–2.6× and said so, lived session 2026-09-13). "Explore the area and report" is **not** a deliverable shape — that's an open-ended drift target.
5. **Reply protocol** — "when you're done, reply with X, Y, Z." Names the format of the spawn's return message. Almost always: list of file paths + line counts, decisions the spawn made that warrant parent confirmation, surprises. Almost never: paste the full file contents back (the parent reads from disk).

**Why:** The briefing is the unit of disambiguation. A spawn that runs without one of the five sections produces predictable failure modes: missing background → wrong scope; missing files-to-sweep → spawn invents context; missing constraints → spawn conflicts with parent; missing deliverable shape → drift; missing reply protocol → parent re-asks "so what did you produce?".

**Where enforced:** `/agora --spawn` walks the user through all five before writing the briefing file. The spawn file template enforces section presence.

### 5. Delivery mechanism — auto by default, manual on demand

**What:** A spawn is delivered one of two ways, declared in the spawn file's `delivery:` frontmatter (`auto` | `manual`, default `auto`). This is **orthogonal to the authorization tier** — any tier can be delivered either way.

| Mechanism | How | When |
|-----------|-----|------|
| `auto` (default) | Parent dispatches the briefing via the **Agent tool**. The subagent reads the spawn file, executes within its tier, **writes its deliverable into the file's `## Result` block itself**, and replies with the reply-protocol summary (returned to the parent automatically). | The normal case. No copy-paste; the durable record is written by the subagent. |
| `manual` (opt-in) | Parent surfaces the briefing as a copy-pasteable block; the user runs it in an external window / a different model and pastes the output into `## Result`. | Only when a *different model or a separate context window* is the actual goal (e.g. cross-checking against a Copilot, or a task-specific model). |

For an `auto` spawn the subagent always writes its own spawn file's `## Result` (even at `advisory` tier — the spawn file is Agora bookkeeping, not parent-in-flight work); at `advisory` that is the *only* path it may write. Parallel auto-spawns are issued as multiple Agent calls in one parent message, subject to the Rule 3 disjoint-allowlist check; long ones run with the Agent tool's background option.

**Why:** The copy-paste round-trip was the original spawn pattern from when the only "fresh context" available was a separate chat window. The Agent tool makes a subagent with its own context a first-class primitive — the parent can dispatch and the subagent can write its own result, removing the manual paste on both ends. Manual is retained because it is the *only* way to reach a different model or a genuinely separate window, which is occasionally the point.

**Where enforced:** `/agora --spawn` MODE 4 step 6 (the dispatch branch); spawn file `delivery:` frontmatter. `auto` delivery does NOT relax the commit boundary — a `write`/`commit` auto-spawn's edits are still raw material for the parent's commit-tree triage (Rule 2).

### 6. Lifecycle — clear, finite goal; multi-iteration is normal but append-only

**What:**

- A spawn's `status:` moves through `open` → `returned` → `folded` (a spawn that never delivered is `closed-without-result`). The flip is a write path since US-AGORA-067: `flask agora write spawn-status <file> returned|folded|closed-without-result` — `returned` and `folded` refuse a file whose `## Result` is empty or still the template placeholder; `flask agora state-check` holds the vocabulary and reports an `open` spawn with a filled Result as `[INFO]`.
- The briefing names a **finite, testable goal**. "Produce wiki seed at path X with sections A, B, C" is finite. "Improve our understanding of Y" is not.
- When the spawn returns, the parent does **three things in order**: (1) reads the spawn's reply, (2) folds the result into the parent session's Log as **one summary entry** (not a transcript), (3) appends the spawn's full reply to the spawn file's `## Result` block. Then `status:` flips to `returned`.
- **Multi-iteration is normal** — about ⅔ of real spawns iterate at least once. The pattern is **append-only**: the same spawn file gains `## Iteration 2` (with its own briefing block), then `## Iteration 3`, etc. Never rewrite earlier iterations — the iteration history is itself a record of how the spawn's understanding refined.
- **Extra scope comes back as findings, not silent extension.** If the spawn discovers a related problem outside its briefing, it surfaces the finding in its reply. The parent decides: dispatch a follow-up spawn, address inline, or park as an Open thread. The spawn does NOT silently take on the new scope.

**Why:** "Clear finite goal and fade out" is the user's exact requirement. A spawn that drifts into "ongoing" competes with the parent for the user's attention and produces output the parent didn't ask for. Append-only iteration documents the history; the next person reading the spawn file sees how the deliverable evolved, not just where it ended. Findings-not-extension preserves the user's authority over scope.

**Where enforced:** spawn file template (`status:` field), `/agora --spawn` reply-fold step, MODE 4 of `/agora`.

## Common mistakes

- **Spawning a 5-bullet-point task.** The briefing cost exceeds the saving. If the deliverable is small enough to fit in five inline bullets, do it inline.
- **Briefing without a "do NOT touch" list.** The spawn picks up the same file the parent is editing; merge conflict at fold-in. Always enumerate the parent's in-flight paths.
- **Re-running an `advisory` spawn at `write` tier without re-briefing.** The first round's briefing assumed "return markdown"; the second round needs explicit "write to path X, do not commit" plus the path allowlist. A tier change is a new iteration.
- **Two `write` spawns touching overlapping paths "because they're related".** Related sub-goals can be one spawn or two sequential spawns. Two parallel writes is a race.
- **Spawn output rewriting earlier iterations.** The reader of the spawn file should see how the understanding refined. Rewriting collapses that history. Append `## Iteration N`; don't edit the original briefing.
- **Spawn quietly takes on extra scope.** "While I was here, I also fixed X." Sounds helpful; is actually scope-creep that bypasses the parent's authority. Surface as a finding; let the parent decide.
- **Parent commits the spawn's output without reviewing it.** The commit-tree triage applies even to spawn-produced files: the parent reads what landed, stages by path, drafts a conventional-commit message. `tier: write` does NOT mean "blind-trust commit at parent close".

## See also

- `.claude/skills/agora/SKILL.md` — MODE 4 (`--spawn`) is the canonical dispatch path; this policy is what MODE 4 reads to validate a dispatch
- `.claude/sessions/spawns/_TEMPLATE.md` — the spawn briefing file shape
- `.claude/sessions/spawns/2026-05-16-agora-vocabulary-consolidation.md` — reference example of a multi-iteration `write`-tier spawn
- `.claude/sessions/spawns/2026-05-16-premium-save-toast.md` — reference example of a tier-escalating spawn (`write` → `commit`) that landed 5 production commits
- the hub-rollout recipe §2 — the canonical worked **multi-entity fan-out** plan (per-entity `write`-tier spawns with disjoint allowlists, parent serialising the shared registry/mixin/CSS/doc files, max-3-concurrent ceiling)
- [`policy-commit-discipline`](policy-commit-discipline.md) — the commit boundary policy this one defers to; spawn output is raw material for the parent's commit-tree triage
- [`policy-documentation`](policy-documentation.md) — when a spawn produces a wiki seed / implementation plan / story, the relevant home rules from policy-documentation apply
