---
name: documentation
title: Documentation
status: active
domain: authoring
related_skills:
  - learn
  - agora
  - plaza
related_lint_rules:
  - R013
  - R073
---

# Documentation policy

## TL;DR

1. Every **implemented** feature has a wiki seed at `docs/wiki/feature-<slug>.md` (path config) — narrative source of truth, authored by `/implement-story` Phase 3.8.
2. Every **non-trivial** feature has an implementation plan at `docs/implementation-plans/implementation-plan-<id-or-slug>.md` — written **before** code (Phase 2b) and updated **during** implementation with a Surprises & decisions entry per phase.
3. **Cross-cutting** rules that span two or more skills go in `.claude/policies/policy-<slug>.md` (authored via `/document --policy`) — never duplicated across skill SKILL.md prompts. **A scattered rule earns its own policy once the same rule lives in ≥3 places** (the consolidation threshold).
4. **Skill-level corrections** (a skill misbehaved or missed a step) go through `/learn` — they patch the relevant SKILL.md surgically and never become a policy or wiki seed.
5. Story status flips reflect work state: `draft → review → approved → planned → in-progress → partially-implemented → implemented → tested`. The implementation plan's `Status:` field tracks the build separately (`draft → in-progress → done`).

## Why this exists

A project run this way has many homes for knowledge: requirements stories, use cases, workflows, quality criteria, wiki seeds, implementation plans, skill SKILL.md files, CLAUDE.md, memory entries, policies. Without a discipline that maps "what kind of knowledge → which home", the same rule ends up in three places (and drifts), or the wrong rule ends up in the wrong place ("how to handle migrations" buried in one skill's Key Rules instead of available to every skill that touches a rewrite). The cost is silent drift; the fix is one canonical home per kind of knowledge.

## The rules

### 1. Wiki seed for every implemented feature

**What:** When a story flips to `status: implemented`, the corresponding wiki seed at `docs/wiki/feature-<slug>.md` (the path is the child's config) must exist and reflect the current state. It includes a markdown body (narrative) and a structured `ai_section:` YAML block (machine-consumable summary).

**Why:** The wiki is the canonical "what is this feature, what does it do, where does it live" reference. Both humans and the AI assistant query it. Without it, the feature exists but isn't discoverable.

**Where enforced:** `/implement-story` Phase 3.8 ("REQUIRED — not optional") authors the seed during the build. **Lint-gated** by R073 (UCs with status `implemented|partially-implemented|tested` must declare `wiki_seed:` pointing to an existing seed file) and R074 (every `feature-*` seed must have populated `related_routes` or `related_models`, or declare `source_tracking: opt-out`). CI fails if either is violated. `/wiki --audit` catches the same drift periodically.

### 2. Implementation plan for every non-trivial feature

**What:** Before any code change in `/implement-story` Phase 3 (BUILD), Phase 2b writes a plan at `docs/implementation-plans/implementation-plan-<id-or-slug>.md`. The plan must have Goal, Guiding principles, Phases, and a Surprises & decisions log. Each Build phase appends one entry to the log. Phase 5 closes the plan out (`Status: done`).

**Why:** Diffs and commit messages tell you *what* changed. The plan tells you *what we tried, what surprised us, and which decisions stuck* — the load-bearing context that survives the chat Section. The Surprises log specifically captures the non-obvious: schema fields that weren't where you thought, regex gotchas, existing macros that already covered the case.

**Where enforced:** `/implement-story` Phase 2b / 2c / 5. `/feature-plan` Phase D.4a writes the umbrella plan for multi-story platform initiatives. Procedural; a lint rule (`R0xx-implementation-plan-required`) that gates `status: implemented` stories on a matching plan file is planned but not yet shipped.

### 3. Cross-cutting rules → policy file, not skill prompt

**What:** A rule that applies to two or more skills (or to direct edits the user makes outside any skill) belongs in `.claude/policies/policy-<slug>.md`. The policy file is the single source of truth; its TL;DR is mirrored into `CLAUDE.md` so the critical lines are always loaded; skills that enforce the rule reference the file rather than restating the rule.

**Why:** Restating a rule across three skill prompts is how rules drift. When the migration discipline lived inside `/implement-story` Phase 1.4b, `/update-story` Phase 3.1, and `/fixbug` case C step 3, three subtly different versions emerged. Single-source-of-truth in a policy file makes drift impossible.

**The ≥3-places consolidation threshold:** a scattered rule earns its own policy once the *same rule lives in ≥3 places*. Below three, a cross-reference between the surfaces is usually enough; at three or more, the copies have proven they will drift (each surface tends to grow its own slightly-different enumeration). `policy-skill-authoring` (2026-05-20, GH #75) was the first deliberate application — the frontmatter-quoting rule had crossed four surfaces (`/agora` appendix, `/learn` section, the lint script, the pre-commit hook) with three subtly different risky-char lists before being consolidated. The threshold is a heuristic, not a hard gate: a rule that is *obviously* cross-cutting (e.g. a security invariant) earns a policy on sight, regardless of count.

**Where enforced:** `/document --policy <slug>` is the only way to author a policy. The skill walks the author through the steps (write file, mirror TL;DR, cross-reference from related skills, update index) so the discipline is enforced at authoring time.

### 4. Skill-level corrections → `/learn`, not a policy

**What:** When a skill misbehaved (used the wrong path, missed a step, made a wrong assumption) or when a non-obvious successful pattern is worth pinning, `/learn` patches the relevant SKILL.md surgically. Never write a one-skill correction as a policy — that inflates the policy folder with rules nobody else reads.

**Why:** Policies are about *cross-cutting* rules. A correction that only affects one skill belongs in that skill's `Key Rules` section or in the relevant phase. Misclassifying it dilutes the policy concept.

**Where enforced:** `/learn` skill flow includes a Step 2 ("Identify the target skill") that filters out cross-cutting lessons; those get redirected to `/document --policy`.

### 5. Story status reflects work state

**What:** Story frontmatter `status:` advances through eight values as the work progresses. The lint enforces the enum (R007) and that `status: tested` requires non-empty `related_tests:` (R013). The implementation plan's `Status:` field is independent — it tracks the build (`draft / in-progress / done`), not the requirement.

**Why:** Status is read by humans triaging "what's the state of this feature" and by the AI assistant when answering questions about coverage. Drift between code state and story status leads to wrong answers.

**Where enforced:** Lint rules R007 (enum) and R013 (`tested` requires tests). `/implement-story` Phase 4.4 flips the story status; `/update-story` may update it as part of feedback propagation.

## Common mistakes

- **Wiki seed drift after a refactor.** A feature was implemented and seeded; later refactor moves files, renames things, and the wiki seed doesn't get updated. The seed becomes wrong reference data the AI assistant feeds back to users. **Fix:** part of any refactor that moves entry points is a wiki seed pass.
- **Implementation plan written *after* the build.** The Surprises log loses its value if it's filled in retroactively from memory — the surprises are forgotten by then. **Fix:** the plan is mandatory at Phase 2b *before* code moves; surprises log entries are written *during* each phase, not at the end.
- **Cross-cutting rule duplicated in three skills.** A pattern like "always sanitize input" gets copy-pasted into `/implement-story`, `/fixbug`, `/update-story`. Six months later the wording diverges. **Fix:** move to a policy; skills reference the policy.
- **Documentation written into CLAUDE.md prose instead of a wiki seed.** CLAUDE.md grows by 200 lines for one feature. **Fix:** CLAUDE.md gets a one-line pointer to the wiki seed; the seed has the body.

## See also

- `docs/implementation-plans/README.md` — implementation plan convention
- `docs/implementation-plans/_TEMPLATE.md` — copy-paste skeleton
- `docs/wiki/` — wiki seed body files (path config)
- `/implement-story` SKILL.md — Phase 2b (plan), Phase 3.8 (wiki seed)
- `/feature-plan` SKILL.md — Phase D.4a (umbrella plan)
- `/learn` SKILL.md — skill-level correction flow
- `/document` SKILL.md — policy authoring flow
- Lint rules: R007 (status enum), R013 (`tested` → tests required), R073 (UC `wiki_seed:` coverage), R074 (feature seed `related_routes` / `related_models` populated or explicit opt-out)
