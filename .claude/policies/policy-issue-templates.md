---
name: "issue-templates"
title: "GitHub Issue templates — agora:type:* axis labels at create-time"
status: active
domain: authoring
related_skills:
  - agora
related_lint_rules: []
---

# GitHub Issue templates policy

## TL;DR

1. **Every new external-facing Issue surface at GitHub uses one of the 6 markdown templates** at `.github/ISSUE_TEMPLATE/` — `agora-bug.md`, `agora-goal.md`, `agora-sub-goal.md`, `agora-section.md`, `agora-milestone.md`, `agora-learn.md`. Each auto-applies its `agora:type:*` label, so no triage step is needed at `/agora --start`.
2. **Markdown templates, not YAML form fields.** The user's workflow is "write a prompt in an Issue and we work on making it structured" — markdown gives an editable starting point with sections to fill in; YAML form fields enforce validation that gets in the way of freeform prompting. The six templates in `.github/ISSUE_TEMPLATE/` are the canonical shape.
3. **`config.yml` keeps `blank_issues_enabled: true`** so users are never locked out of opening a plain Issue. The template chooser is a guide, not a fence. `contact_links:` in the chooser point at the Agora vocabulary README and the product's story backlog — the two references a confused user would want first.
4. **Adding a new template means adding a new `agora:type:*` axis value** — the template-to-axis mapping is one-to-one by design. Extend `_CANONICAL_LABELS` in `app/commands/agora_helper.py` AND run `flask agora setup-labels` before merging the new template, otherwise GitHub rejects the unknown label at Issue creation.
5. **The bug template is the live-traffic one.** `/agora --start` step 1.1 queries `flask agora list-bugs` (filtered by `agora:type:bug --state open`) as a candidate-intents source. The other five templates (goal / sub-goal / section / milestone / learn) are for occasional cross-referencing — `agora:type:goal` Issues mirror COMPASS Goals one-way; `agora:type:milestone` Issues track a (possibly multi-Goal) effort with its game-plan living in the Issue (US-AGORA-019/021); `agora:type:learn` Issues are optional external echoes of skill-level lessons; `agora:type:section` Issues are optional retro mirrors.
6. **Goal/Sub-goal hierarchy + Milestone-tag timing.** Every sub-goal Issue references a parent Goal Issue (`**Parent Goal:** #<n>`) — a Milestone's **batch** Issues are scaffolded from that shape in one call via `flask agora batches --goal <n> --batch "…"`, never hand-written as scope accretes. Every Goal Issue is **Backlog** (GH-only, no Milestone tag) or **Active** (mirrored in COMPASS with committed success criteria AND a declared `milestone-<slug>` tag) — Backlog → Active moves in the same `/agora --start` step 1.4 edit when a session picks the Goal up. The Milestone tag is the *closing contract*; declared at COMPASS entry, fired at Goal closure, immutable once declared. The GH `milestone:` attribute is **orthogonal** — it's a **tier / release group** (Tier 3, Release 2), not an Agora Milestone; tiers can be reassigned freely. User-friendly framing: *"a tier is where it sits in the queue; a Milestone is what we'll call it when it ships."*
7. **Issues close when their work ships — at `/agora --end` step 2.8b.** A Goal mirror Issue closes when its Milestone fires (Path A step 7); a sub-goal / section Issue closes when the session that finished its deliverable closes (step 2.8b, both paths). Closing is a **4-eye gate** — propose the close list, the user nods, since closing is an outward GitHub-state action that never auto-fires. Every close carries a **citing comment** linking the Issue back to the closing session + commits/tag. Done work that stays open makes the board lie (the gap that motivated this rule: #74 + #75 shipped 2026-05-20 yet sat open until 2026-05-21).

## Why this exists

Session `2026-05-17-agora-issues-integration` opened with all 9 existing GitHub Issues unlabeled. Triage at session open cost 5 minutes of manual labeling — a recoverable one-time cost. The structural fix landed in Phase G of the same session: markdown templates that apply the canonical `agora:type:*` label at create-time (5 originally; `agora-milestone.md` added 2026-06-20 by US-AGORA-019 → 6). Every Issue opened from a template now lands correctly-classified by construction.

The trade-off considered:

- **YAML form fields** (`agora-bug.yml`) — strict structured fields, dropdowns, validation. Rejected: the user explicitly wanted "write a prompt and we work on structuring it." YAML forms get in the way of freeform brainstorming.
- **Markdown templates** (`agora-bug.md`) — pre-filled markdown body with `<!-- HTML comments -->` as guidance. Editable freely. Picked: matches the actual workflow.

## The rules

### 1. Five templates, one per `agora:type:*` axis value

**What:** `.github/ISSUE_TEMPLATE/` contains exactly five markdown templates plus `config.yml`. One template per `agora:type:*` axis value defined by US-AGORA-001's canonical label taxonomy.

**Why:** One-to-one mapping keeps the system small enough to remember. Adding a sixth template means defining a sixth axis value (which requires updating `_CANONICAL_LABELS` in `app/commands/agora_helper.py` and running `flask agora setup-labels`).

**Where enforced:** Manually at template-creation time. No lint rule today.

**Example:**

```
.github/ISSUE_TEMPLATE/
├── config.yml          # chooser config + contact links
├── agora-bug.md        # auto-label: agora:type:bug
├── agora-goal.md       # auto-label: agora:type:goal
├── agora-sub-goal.md   # auto-label: agora:type:sub-goal
├── agora-section.md    # auto-label: agora:type:section
└── agora-learn.md      # auto-label: agora:type:learn
```

### 2. Markdown templates, not YAML form fields

**What:** Each template is a `.md` file with frontmatter (`name`, `about`, `labels`) and a markdown body. The body has `<!-- HTML comments -->` as guidance and editable sections the user fills in.

**Why:** Form fields enforce validation that breaks the user's "write a prompt freely" workflow. Markdown templates support the same use case but stay out of the way. The user can delete any section they don't need.

**Where enforced:** Manually at template-creation time.

**Example:**

```markdown
---
name: "Bug report (agora:type:bug)"
about: "Report a bug. Closure flows through /fixbug --gh."
title: ""
labels: ["agora:type:bug"]
---

## Symptom

<!-- One sentence: what the user sees that's wrong. -->

## Reproduction

<!-- Steps to reproduce. -->
```

### 3. `config.yml` keeps blank Issues enabled

**What:** `blank_issues_enabled: true`. Users can always open an unstructured Issue if no template fits.

**Why:** Locking the chooser is a fence that punishes users for not fitting the system's mental model. The templates guide; they don't restrict.

**Where enforced:** Manually in `config.yml`.

**Example:**

```yaml
blank_issues_enabled: true
contact_links:
  - name: Agora vocabulary reference
    url: https://github.com/.../sessions/README.md
    about: How sessions, Goals, Sub-goals, and Milestones fit together.
```

### 4. Template-to-axis mapping is one-to-one

**What:** Adding a new template requires adding a new `agora:type:*` axis value to `_CANONICAL_LABELS` in `app/commands/agora_helper.py`, then running `flask agora setup-labels` to create the label on GitHub. The template references the new label in its `labels:` frontmatter.

**Why:** The label taxonomy is the system's spine — every Issue body, every `mirror_bug` call, every `/agora --start` query keys off it. Adding a template without extending the canon causes labels to fail at Issue creation (GitHub rejects unknown labels).

**Where enforced:** Manually in code review. the label test (`TestCanonicalLabels`) asserts the canonical count (17 today: 5 type + 12 tag) but doesn't currently check template-to-axis symmetry — that's a follow-on test.

### 5. The bug template is the live-traffic one

**What:** Of the six templates, `agora:type:bug` is the only one that feeds an automated workflow (`/agora --start` step 1.1's `flask agora list-bugs` query). The other five are for human reference.

**Why:** Bugs are the highest-volume Issue type and the one most likely to be opened by a non-author (the user reporting a bug while testing). The other five (goal / sub-goal / section / milestone / learn) are written by the developer for cross-referencing — they're optional mirrors of canonical surfaces (COMPASS for Goals, sub-goal Issues for sub-goals, session files for sessions, SKILL.md for lessons).

**Where enforced:** `/agora` SKILL.md step 1.1 calls `flask agora list-bugs` and surfaces open bug Issues alongside Open threads. The other five template types are NOT queried at session start.

### 6. Goal/Sub-goal hierarchy + Milestone-tag timing

**What:** Two coupled rules about Goal-axis Issues.

**(a) Every sub-goal Issue references a parent Goal Issue.** `agora:type:sub-goal` Issue bodies start with a line like `**Parent Goal:** #40` (linking to the `agora:type:goal` Issue). An orphan sub-goal is implementation work with no strategic anchor — either name the parent or reclassify (the sub-goal might actually be a new Goal in disguise, or it might be work that belongs in a session log rather than its own Issue).

A Milestone's **batch** Issues are scaffolded from this shape in one call rather than hand-written as scope accretes — `flask agora batches --goal <n> --batch "…" --batch "…"` (US-AGORA-039) opens one `agora:type:sub-goal` Issue per batch, each body carrying the `**Parent Goal:**` line, so the hierarchy holds by construction. `flask agora milestone` then reports whether the Goal declares them.

**(b) Goal Issues exist in one of two states with different Milestone-tag rules.**

| State | Where defined | Success criteria | Milestone tag |
|---|---|---|---|
| **Backlog** | GH Goal Issue only | Not committed (intent placeholder) | **NOT declared** |
| **Active** | GH Goal Issue + COMPASS mirror | Explicit, committed in COMPASS | **Declared** alongside criteria (`milestone-<slug>`) |
| **Closed** | COMPASS "Goals (closed)" (`COMPASS-closed.md`) | Met | **Fired** — real annotated git tag pushed |

A Goal moves Backlog → Active when a session picks it up for pursuit; the COMPASS mirror + the Milestone tag declaration land in the same `/agora --start` step 1.4 edit (the "opens a new Goal" path). The Milestone tag is part of the **closing contract** — you can't name what closes a Goal until you've committed what's *in* it. Pre-declaring tags for Backlog Goals creates dead documentation (most Backlog Goals get rescoped or dropped).

**Sub-milestones (iterative Goals)** are declared per round, not all upfront. A round-N Goal declares `milestone-<goal>-N` when round N is scoped (typically in the session that opens it); future rounds get tags as they're scoped.

**(c) The GH `milestone:` attribute is orthogonal — it's a *tier / release group*.** When you assign Goal #40 to GH milestone "Release 2", you are saying "this Goal ships with the Release 2 group" — that is a **tier** concept, NOT an Agora Milestone. The vocabulary collision is solved by renaming our INTERNAL term:

| GitHub UI term | Our internal term | Trigger |
|---|---|---|
| Milestone attribute | **Tier** / **release group** | Assigned by user at any time; can move freely |
| (nothing) | **Agora Milestone** (`milestone-<slug>` git tag) | Declared at Goal-COMPASS-entry; immutable once chosen; fires at Goal closure |

User-friendly framing: *"a tier is where it sits in the queue; a Milestone is what we'll call it when it ships."*

**Why:** Without this rule, three confusions accumulate. **Orphan sub-goals** — implementation work with no strategic anchor — drift in the Issues board because nobody can decide what they're "for". **Premature Milestone tags** — Backlog Goals get tags that never fire because the Goal got rescoped — pollute the vocabulary. **Tier-vs-Milestone vocabulary clash** — using the word "milestone" for two different concepts (GH UI tier grouping + Agora Goal-closure event) makes every conversation about goal-system structure ambiguous.

**Where enforced:** `/agora` SKILL.md step 1.4 (sub-goal placement names the parent Goal; new Goals enter COMPASS with the tag); manually on Issue creation (sub-goal template body asks for `Parent Goal: #<n>`); `/agora --start` step 1.4 ("place in vocabulary") surfaces orphan sub-goals as a finding when triaging recent Issues.

**Example — settling today's orphans (session 2026-05-18 Phase D):**

```
# bad — sub-goal with no parent, milestone-tag pre-declared
#46 "Sub-goal: US-EXP-003 filter-presets - finish"
  body: ## Goal: ship filter presets
        Milestone tag: milestone-exp-filter-presets   ← premature
  parent Goal Issue: (none)                          ← orphan

# good — parented sub-goal, Backlog parent has no tag
#46 "Sub-goal: US-EXP-003 filter-presets - finish"
  body: **Parent Goal:** #NN "Goal: the exports module ships"
        ## Sub-goal scope: ...
#NN "Goal: HR module ships premium" (Backlog — no COMPASS entry, no tag)
  Tier: GH milestone "Release 2"                     ← orthogonal, fine
```

### 7. Issues close when their work ships — at `/agora --end` step 2.8b

**What:** A GH Issue is closed by the session that *finishes* the work it tracks. Two timings, one pass: a **Goal mirror Issue** (`agora:type:goal`) closes when its Milestone fires (`--end` Path A step 7); a **sub-goal / section Issue** (`agora:type:sub-goal` / `agora:type:section`) closes when the session that shipped its deliverable closes (`--end` step 2.8b, which runs on **both** Path A and Path B). The close is a **4-eye gate** — `/agora` builds the candidate list from the session Log + `commits:` + `stories_touched:`, presents it summarized, and the user nods, edits, or drops entries before any `gh issue close` fires. Every close carries a **citing comment**: `gh issue close <n> --comment "Closed by <session-id> — <commit shas / milestone tag>. <what shipped>."`

**Why:** The Issue board is Agora's external mirror of what's in flight and what's done. Without a close step at session end, completed work stays open and the board lies — `gh issue list --state open` stops answering "what's left?" honestly. The concrete trigger: #74 (leveling-field lint) and #75 (`policy-skill-authoring`) both shipped in the 2026-05-20 session yet sat open until the user manually noticed and closed them 2026-05-21. The 4-eye gate (not auto-close) matters because closing is an outward GitHub-state action and because "advanced but not finished" sub-goals are common — those stay open by design.

**Where enforced:** `/agora` SKILL.md Path A step 7 (Goal mirror) + step 2.8b (sub-goal / section Issues) — skill prompt; the user's nod at the 4-eye gate.

**Example:**

```
# good — close list presented at --end 2.8b, then closed on the nod
#74 "Extend validate_skill_frontmatter.py …" — shipped 2026-05-20 (--levels lint)
#75 "Author policy-skill-authoring …"        — shipped 2026-05-20 (commit 20bdf27)
  → gh issue close 74 --comment "Closed by 2026-05-21-… — shipped 2026-05-20; …"

# bad — session closes, Issues stay open, board drifts
(work shipped, no close step → #74/#75 linger open for days)
```

## Common mistakes

- **Mixing markdown templates with YAML forms in `.github/ISSUE_TEMPLATE/`** — pick one shape per surface; mixing confuses the chooser UX.
- **Closing a GH Issue without a citing comment.** The comment is the durable bridge from the Issue back to the session + commits that closed it; a bare close loses the trail. (Rule 7)
- **Letting completed work stay open because `--end` skipped the close pass.** Done sub-goal Issues that linger make `gh issue list --state open` lie about what's left. Run step 2.8b every session, both paths. (Rule 7)
- **Adding a 6th template without a 6th axis value** — the new template's `labels: ["agora:type:foo"]` frontmatter will fail at Issue creation because GitHub rejects the unknown label. Always extend `_CANONICAL_LABELS` and run `flask agora setup-labels` first.
- **Setting `blank_issues_enabled: false` "to force good triage"** — locks users out of the freeform shape they need for half their use cases (one-off questions, screenshots-only reports). Keep it true; rely on the chooser's prominence to guide most users to a template.
- **Putting required-field validation in YAML form templates** — switching from markdown to YAML loses the "write a prompt and we work on structuring it" workflow. If you find yourself wanting validation, the right surface is a /fixbug or /new-story workflow, not the Issue template.
- **Creating a Backlog Goal Issue with a pre-declared Milestone tag.** The tag is part of the closing contract; without committed criteria it's premature. Backlog Goals carry intent only.
- **Sorting a Backlog Goal into a tier and treating the tier as a Milestone.** Tiers are queue-position; they can move. Milestones are closing events; once declared they don't rename.
- **Sub-goal Issue with no `Parent Goal:` line.** Orphan sub-goals drift because nobody can decide what they're for. Either name the parent Goal or reclassify the work.
- **Mirroring a Backlog Goal into COMPASS prematurely.** COMPASS is the *active* register. A Goal Issue can sit in Backlog for months; only when a session picks it up does the COMPASS mirror + Milestone tag declaration land. The Goal backlog index in COMPASS is the discoverability surface for backlog Goals — it links *to* them; it doesn't promote them.

## See also

- `.claude/skills/agora/SKILL.md` — step 1.1 queries the bug-template traffic via `flask agora list-bugs`
- `.claude/skills/fixbug/SKILL.md` — STEP 6.2 mirrors closed bugs via the same label taxonomy
- `docs/requirements/stories/agora/US-AGORA-001-fixbug-gh-issues-bridge.md` — the source story for the 3-axis taxonomy
- `docs/wiki/feature-agora-gh-issues.md` — wiki narrative for the bridge (path config)
- the substrate's label module — `_CANONICAL_LABELS` is the source of truth for the axis values
