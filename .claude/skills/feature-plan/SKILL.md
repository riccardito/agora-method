---
name: feature-plan
description: Decompose a feature idea into a research paper + critical review + a list of stories ready to write. Use when starting a feature that's bigger than one story (a module, a workflow, a compliance topic, a multi-actor process). For single stories, use /new-story directly.
argument-hint: "<feature-description> [--deep] [--no-research] [--no-review]"
level: hardened
promoted_at: 2026-06-20
role: "the cartographer"
epithet: "Euclid — the surveyor who lays out the grid"
---

> **Journal-at-source** (policy-skill-progression Rule 6): when you finish a unit of work in a session, append ONE unrated stub to [`experience.md`](experience.md) `## Unrated journal` — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`. One line, lighter than the session Log; `/agora --end` 2.3b grades it.

# Feature Plan

Run a four-phase decomposition pipeline for **$ARGUMENTS** in this project. The pipeline produces:

1. A **research paper** under `docs/references/research/RP-<DOMAIN>-NNN-<slug>.md` — internal scan + web research, structured per the template at `docs/references/research/_TEMPLATE.md`.
2. A **hard, honest critical review** of the user's framing — alternative shapes with explicit trade-offs.
3. A **decomposition table** — the proposed stories grouped by phase (must / should / could).
4. The **actual story files** (and umbrella UC, optional WF) — emitted only after explicit `y` from the user.

**This skill is HARD-MODE by default.** Critical review is not soft suggestions. If the user's framing is questionable, say so directly with reasoning. The user has explicitly asked for honest review, not encouragement.

**When to use this vs `/new-story` — the boundary is ≤2 vs 3+/compounding.** `/new-story` writes **≤2** well-scoped stories you already understand; the moment the input **compounds to 3+ stories** — several "simple" things that *add up* to something complex (the user's framing: *"5 simple things added together gets something complex; the feature plan holds all ideas together"*) — this is the skill, because the holding pipeline (research → critical review → decomposition) is what keeps the compounded ideas coherent. The Phase C heuristic restates this from the other side: fewer than 5 decomposed stories means it should probably have been a single `/new-story`.

## When NOT to use

| Need | Use instead |
|---|---|
| Write **≤2** well-scoped stories you already understand (no compounding) | `/new-story` — the single/small-batch entry point; the boundary is ≤2 vs 3+/compounding |
| Add **one** story to a research paper that's **already decomposed** | `/new-story --from-plan RP-XXX-NNN` — the post-hoc addition path (Phase D.2 note) |
| **Build** a decomposed story into code (model/routes/templates/JS/tests) | `/implement-story <US-id>` — `/feature-plan` plants Goal + Milestones; it never builds |
| **Refine** an existing story after Phase D | `/update-story` |
| Open/close the **session** that does the work, fire a Milestone tag | `/agora --start` / `--end` — `/feature-plan` writes the *plan*; sessions reach the Milestones it plants |
| Correct a **skill's** behaviour after it misbehaved | `/learn` — skill-level corrections never go through a research paper |
| Author a **cross-cutting policy** or ad-hoc explainer | `/document` (`--policy` for rules spanning ≥2 skills) |
| Plan an **Agora self-improvement** round (the skill system itself) | `/plaza` — `/feature-plan` is for product features. **Two named exceptions run here:** `/plaza` Stage 5 routes the round's own prioritized agenda to `/feature-plan` (it never re-implements decomposition), and a topic that spans a **product batch AND an Agora round** is planned in one run with stories in both homes — the round's plaza then harvests the RP instead of re-planning it (lived session 2026-09-11: RP-CANON-001 → C10 on #461 + seven US-AGORA stories on #477) |
| Pure UI-structure audit / page-zone polish of an **existing** surface | `/check-page` / `/check-ui-entity` |

## Where this fits in the Goal vocabulary

A `/feature-plan` run **opens a Goal** in [`COMPASS.md`](../../sessions/COMPASS.md)
— the feature itself is the Goal, with success criteria that the
decomposition table makes concrete. Within that Goal:

- **Each story** is a **sub-goal** — implemented in one or more
  conventional commits via `/implement-story`.
- **Each phase boundary** (must-have done, should-have done, could-have
  done) is a **Milestone** — the event that fires `/agora` `--end` 2.2
  Path A: stats refresh + annotated `milestone-<slug>` tag + push + CI
  green + Haleluja.

`/feature-plan` writes the *plan*. The Milestones it plants are reached
later — by the Sections (via `/implement-story`, `/iterate`, `/fixbug`)
that close their sub-goals. See [agora](../agora/SKILL.md) for the
ceremony.

## Arguments

- `$0` — Feature description (free-form). Examples: `"search filter management module"`, `"booking series with recurring rules"`, `"invoice export format migration"`.
- `--deep` — Phase A runs the deeper research path (15–30 min, more web fetches, structured comparison table).
- `--no-research` — Skip Phase A. Use when the feature is purely internal (no compliance, no domain standards).
- `--no-review` — Skip Phase B. Rare; only when the user explicitly says "I know exactly what I want, just decompose."

## Output structure

```
docs/references/research/
  RP-<DOMAIN>-<NNN>-<slug>.md     ← Phase A output, appended by Phase C

requirements/stories/<area>/
  US-<PREFIX>-<NNN>-<slug>.md      ← Phase D output (one per row in the table)
  ...

requirements/use-cases/
  UC-<DOMAIN>-<NNN>-<slug>.md      ← Phase D output (umbrella UC)

requirements/workflows/      ← Phase D output (only if cross-actor handoffs)
  WF-<NNN>-<slug>.md
```

---

## PHASE A — DISCOVERY

Skip if `--no-research` given. Default depth is **medium**; `--deep` switches to deep.

### A.1 — Internal scan

Read everything the project already has that overlaps with the feature. The catalogue is read from the FILES — glob the story / UC / WF frontmatter; `python -m agora_checks catalogue` prints the lint's ISSUE list, not the catalogue — it prints nothing on a clean tree (lived session 2026-09-19: A.1 fell back to file globs):

```bash
grep -rl "^feature_area: <area>" requirements/stories/      # an area's stories, by frontmatter
python -m agora_checks catalogue                                   # the catalogue's HEALTH -- issues, never rows
```

Cross-reference:
- Existing stories in the candidate feature area: `requirements/stories/<area>/US-*.md`
- Related use cases: `requirements/use-cases/UC-<DOMAIN>-*.md`
- Related workflows: `requirements/workflows/WF-*.md`
- Quality criteria the feature will likely cite: `requirements/quality-criteria/<category>/QC-*.md`
- Glossary terms in scope: `requirements/glossary.md`
- UI page registry for surfaces this feature might add (the project's own page map)
- Models and routes: the project's model and route modules
- Strategy papers that pre-date this folder: `docs/references/strategy/*.md`
- **For a seed / config / catalogue topic — the CONSUMER registries beside the collections:** the `get_enum_values(` call sites and `enum:<x>.<y>` descriptors, `DEFAULT_WORKFLOW_TOPICS`, the taxonomy registries (the tag, type and detail entity lists). "Which counts are zero" is answered by collection; "which dropdowns are empty" and "which workflows have no template" are answered by CONSUMER, and a scan that reads only collections hands both to the user at the ruling gate (lived session 2026-09-19: the enum vocabularies had no seeder at all and four of seven workflow topics no template — both found by the user, both in registries the scan never opened).
- **For hub-page rollout RPs** — the hub page registry's `<hub>` entry: read it and surface its **populated-vs-placeholder** state. A populated entry (declared `domains` + `subtabs` with `scope_options` per subtab — the reference hub is the reference shape) means the hub is structurally promoted; per-zone polish is the right RP scope. A placeholder entry (empty `domains: []` + `subtabs: []` — comment often names it explicitly) means the structural promotion is the PREREQUISITE phase, not a follow-up; the RP must surface this. This was missed in RP-UX-002 Phase A: the resolver code was read but the registry's populated state was not — Round 2.5 (structural promotion) surfaced mid-session as a correction rather than being identified at Phase A. The reference hub's lived precedent (US-UX-002 + the three sessions closing `milestone-<hub>-page-complete`) encodes *layout first → zones walk* as the rollout discipline; checking the registry surfaces whether the next session is layout work or zones work.
- **For ANY hub RP — classify the hub's SCOPING MODEL explicitly, in the paper, before Phase B.** A hub is one of two kinds, and the choice decides its empty state, its filter semantics, its columns and its create buttons. Getting it wrong doesn't cost a detail — it inverts the page.
  - **Identity hub** — resolves the subject from the **login** and **gates** to it: you may only see your own records. No Owner column (every row is yours); no-subject is an error state. Reference: a **My Account** hub (`current_identity_scope()`), where showing anyone else's rows would be a privacy breach.
  - **Workspace hub** — a professional tool over **other people's** records. Shows **ALL entries by default** with a **Customer/Project column**; the app-header select is an **OPTIONAL filter that narrows**, never a gate; no-selection is the normal state, not an empty state. Its creates are **parent-scoped**, so "+ New" with no parent in context opens a **select-parent picker dialog** (the custom-package pattern), *never a disabled button*. Reference: a **Support Hub** (`support_scope()`); a future **customer hub** is the same kind.
  - **Content hub** — a hub with **no subject at all**. It shows the same content to every reader who may see it: no customer/project context band, no scope resolver, no Owner column, and **no empty state tied to a missing selection** because nothing is ever selected. Its creates are **hub-new** (a new instance of the hub's own entity), never parent-scoped. Reference: the **Wiki Hub** — documentation, schema, statistics and guides are the same for everyone; access varies by *permission*, which is a different axis from scoping. **Access-gating is not scoping** — a hub whose leaves carry different permissions is still a content hub if none of them resolves a subject.
  - **The question that separates them:** *"Is the subject who I AM, who I'm WORKING ON, or is there no subject?"* Self → identity, gate. Someone else → workspace, filter. **Nobody → content, neither.** **A hub that resolves its subject from a header selection rather than from the login is a workspace hub**, whatever it is called — and a hub that resolves no subject at all is a content hub, however much machinery it inherits from the other two.
  - **Naming a hub after the scaffolding it reuses is how this goes wrong.** RP-SUP-001 called the Support Hub "the second **identity hub**" six times — true of the *code it borrowed* (the identity-hub scope resolver), false of the *model it needed*. The §2a build inherited the label and shipped subject-**gated** empty states + **disabled** add-buttons; the model had to be pivoted mid-session and two stories' ACs rewritten (session 2026-07-07, session 2026-07-08, thread T-029). **Reusing an identity hub's resolver does not make the new hub an identity hub.**
  - **Output:** one line in `## Existing art` — *"Scoping model: workspace (show-all + optional `<x>` filter) | identity (gated to self)"* — and Phase C carries its four consequences into every UI story's ACs: the default row set, the Owner/Customer column, empty-state-vs-no-gate, and the create-button branch.

**Output of A.1:** an "Existing art" section listing what overlaps. Be specific — cite story ids, model names, route file paths. **For hub-page rollouts**, the `## Existing art` body must include a one-line statement of the target hub's registry status ("populated" or "placeholder"), since that single fact reshapes the decomposition (placeholder → structural promotion is phase 1; populated → per-zone polish is phase 1).

**For a reference-MATCH rollout** (adopting a reference hub's whole structure — the Goal #85 pattern, e.g. a second hub → the reference hub), "populated" is **not** sufficient: a populated registry only means `domains` + `subtabs` are declared, NOT that the **URL scheme / nesting depth / leaf-granularity** match the reference. Phase B critical review must capture the reference's **complete nav contract** up front — read `/check-page` Layer 4c (the 5-point spec: flat `?tab=<leaf>` URLs · registry `subtabs`=leaves-grouped-by-domain · strict 2-level depth · `hub_tabs` two-row contract · route leaf→body mapping) and make "copy the reference structure exactly" an explicit Phase-B alternative shape. Skipping this is what made the 2026-05-30 second-hub restructure take **three iterations** instead of one (its registry was populated the whole time).

#### A.1.b — Existing UI-surface audit (apply policy-ui-surface-discipline)

Equally important — and the section most likely to get skipped — is the **existing UI-surface audit**. For every candidate UI surface this feature might touch:

1. **Inventory the UI page registry** for any `nav-*`, `data-*`, or section id whose `entities:` or `notes:` overlap with this feature's data shape.
2. **Read each candidate's `template:` file** to see what currently renders there. A page that "looks empty" in the YAML notes is often dense in reality.
3. **For each existing surface that overlaps**, name explicitly:
   - What's currently rendered (count of widgets, sections, modal openers)
   - Whether the feature **replaces**, **extends**, or **sits beside** that content
   - If "sits beside" — what justifies the sibling surface vs an extension? (The bar is high; see policy rule 3.)
4. **Output a "UI surfaces in scope" subsection** in the research paper's `## Existing art`, with one row per overlapping surface and the resolved relationship.

This audit is what catches the "we built a duplicate page" failure mode — surfaces overlap silently in the YAML registry, and only a direct read of the templates reveals it. Skip this and Phase C will produce stories with `ui_pages: [a, b]` that have no resolved relationship — exactly the US-ACC-001 incident.

### A.2 — External research

Use `WebSearch` first to identify the right sources, then `WebFetch` the canonical ones.

**Medium (default) — 5–10 web ops (searches and/or fetches):**
- 1–2 regulatory sources if the feature touches compliance (the data-protection, accessibility or sector rules that apply)
- 2–3 domain-standards sources (W3C, ISO, IETF, OpenAPI, iCalendar, …) where applicable
- 1–2 commercial-product or open-source references that show common workflow archetypes
- 1 academic / professional-association source if the topic has a body of literature (e.g. a standards body's handbook for the domain)

`WebSearch` summaries are often dense enough to write a useful paper without `WebFetch`-ing the canonical pages in full. **Fetches are optional** — only fetch when you need verbatim regulatory text, full schema definitions, or a quote you want to cite directly. Don't burn the budget on fetches for things the search summary already covered.

**Deep (`--deep`) — 15–30 web ops:**
- All of the above, plus structured comparison across 3+ implementations
- Read full regulatory text via `WebFetch` (not just summaries)
- Pull the relevant standard's schemas where relevant
- Compare 2–3 commercial products' approaches in a table

**Citation rules:**
- Every source goes in `sources:` frontmatter (url + title + accessed date)
- The lint does NOT check URLs (R060 stops at structural validation), but stale sources are a maintenance cost — prefer durable URLs (W3C, IETF, official standards registries) over random blog posts
- Quote sparingly — paraphrase and cite, do not paste large blocks

### A.3 — Compose the research paper

Pick the next available `RP-<DOMAIN>-NNN`:
1. The domain matches a story prefix where the feature lives (e.g. `SRC`, `BKG`, `EXP`) **OR a clean topic-name for a greenfield domain** (e.g. `REF` for referrals when no `US-REF` prefix exists yet)
2. Glob `docs/references/research/RP-<DOMAIN>-*.md` to find the next number
3. Filename: `RP-<DOMAIN>-NNN-<kebab-slug>.md`

**Note on prefix freedom:** RP- prefixes are NOT cross-checked against `requirements/README.md` (R060 only validates the `RP-[A-Z][A-Z0-9]+-NNN` format). Research often opens a new domain that may or may not become a registered story prefix later — forcing alignment too early would block legitimate research on greenfield topics. If Phase D ends up writing stories with a matching new US- prefix, that's the moment the prefix gets registered (D.1 pre-flight handles it).

Write the paper using the template at `docs/references/research/_TEMPLATE.md`. Required sections:

1. **`## Context`** — what problem, scope, why now (2–3 paragraphs)
2. **`## Constraints`** — hard limits (regulatory, architectural, team / time)
3. **`## Standards & regulations`** — table of standard → coverage → relevance to the project
4. **`## Existing art`** — output of A.1, with model / route / story citations
5. **`## Common objects & workflows`** — what this domain converges on across multiple implementations. **This is the highest-leverage section for downstream design** — it's where the architectural insights live. Default LLM behaviour is to list nouns ("entities involved: Account, Booking, Document"); resist that. Push yourself to articulate (a) **entity shapes** (and which fields are load-bearing vs incidental), (b) **state machines** (the lifecycle the artefact moves through, including failure / retry edges), and (c) **actor archetypes** (who drives each transition, where handoffs happen). Surface where naive framings of the feature fall apart — e.g. "this looks like one PDF but the standards converge on two artefacts (a structured request + a rendered letter)". If you can't name a non-obvious insight in this section, the research is too shallow — go back and read more. **And a classification the paper PROPOSES is a claim to test against the data the paper MEASURED** — read each proposed class against the paper's own table before Phase A closes; a class that contradicts a row the paper already carries is wrong on the page, not later (lived session 2026-09-19: an `empty` class listed `audit_log` at 834 rows under "intentionally empty", survived B, C and D, and was corrected at the build's first live count).
6. **`## Open questions`** — numbered list of unresolved decisions

**Do NOT yet write `## Decomposition`** — that's appended in Phase C.

### A.4 — Pause gate

Print:

> ✅ Phase A complete. Wrote `docs/references/research/RP-XXX-NNN-<slug>.md` ({N} sources cited, depth: {medium|deep}).
>
> Read it now. Refine, push back, or proceed to Phase B (critical review)?
>
> - `proceed` → start Phase B
> - `refine: <feedback>` → I'll revise the paper based on your feedback and pause again
> - `stop` → stop here; you can resume later by re-running `/feature-plan` with the same description

Wait for explicit instruction. Do NOT proceed silently.

---

## PHASE B — CRITICAL REVIEW (HARD MODE)

Skip if `--no-review` given. Otherwise mandatory — this is what the skill is for.

### B.1 — Test the framing

Pose four uncomfortable questions, in this order, with reasoning:

**1. What problem does this actually solve?**
Reflect the user's feature description back through the lens of the research paper. If the framing assumes a problem that the research suggests is already solved (or doesn't exist in this project's context), say so. Cite the research paper's "Existing art" section.

**2. What's the smallest version that gets 80%?**
Identify the must-have core. Strip everything else. The point isn't to argue the user down; it's to surface what's load-bearing vs aspirational, so the decomposition phase doesn't bury must-haves under wishlist items.

**3. Does this fit the project's architecture, or does it fight it?**
The project has strong architectural patterns: a shared model base class, a single route blueprint, fragment + inline-script modal patterns, soft delete + audit log, i18n, schema validation. If the feature requires a new pattern, name it explicitly and explain the trade-off. If it can fit existing patterns, that's almost always cheaper.

**4. Is any topic mixed-direction? (the "AND" smell)**
Walk each topic / sub-item in the feature. A topic that bundles a **general improvement** AND a **concrete use case** — "improve X across the app *and* do concrete Y here" — is a **mixed-direction smell**: it has two directions, two scopes, two definitions-of-done in one item. Split it into **single-direction topics** *now* (one becomes a concrete, shippable story; the other a separate broad/exploratory story or its own future `/feature-plan`). This is the decomposition analogue of commit-discipline's "one commit, one concern" — a topic whose description needs an "and" between a sweep and a spot-fix is two topics. **Catch it at scoping, not mid-build:** lived driver session 2026-06-14 — Issue #135's A2 ("Datetime engine") bundled a data-hub-concrete local-datetime display AND a broad app-wide automated-datetime improvement; the build was clean *because* the plan split them (A2-concrete → US-DAT-026 shipped; A2-broad → a parked thread for its own plan), but the user's retro point is the mixing shouldn't have been framed into one topic in the first place. The single-direction topic ships straight; the mixed one stalls on the half nobody scoped.

**5. Is any topic actually premium/consistency POLISH, not a feature? (the "doctor-pass" smell)**
Walk each topic again with a different lens: does it describe **new behavior** (a thing the system couldn't do before — a new entity, a new flow, a fixed bug) or **premium/consistency polish on existing surfaces** (datatable view, filtershell, card/table toggle, premium-component swap, count badges, sticky-twin save — applied *across leaves/pages that already work*)? **Polish is a DOCTOR pass, not a feature story.** It belongs to `/check-page <slug> --finish` (the premium reference-page sweep — Layer 3b), run as a SEPARATE pass, NOT decomposed into `US-*` stories. The tell: the "acceptance criteria" read like a CSS/component checklist ("uses the shared data-table component, premium filtershell, rectangular add button") rather than a behavior change — and CSS/component specs correctly don't live in a user story (per `policy-frontend-conventions` + implement-story 3.3.pre), so a story whose whole point is the premium bar can't even *express* its own done-condition. **The efficient sequence is doctor-pass FIRST, features SECOND:** run `/check-page --finish` across all the leaves so they share one premium baseline, *then* `/feature-plan` only the genuinely new behavior. Lived driver session 2026-06-22: §3 Configuration was *fully* feature-planned including the premiumification — US-SET-008 (reusable upload) + US-SET-010 (enums-fix) were real features and ran efficiently, but US-SET-011 (list-surface) + US-SET-013 (physio premium) + the cross-leaf datatable/filtershell/card-toggle/count-badge work were a **power-through**, because that work is a doctor sweep wearing a story's clothes. Extract every polish topic at Phase B (like the AND-smell above) and route it to `/check-page --finish`; what remains as stories is the actual feature. **Sequencing exception — doctor-FIRST assumes the surfaces already exist; when the feature *creates* the sibling surfaces, do doctor-LAST (one sweep after the build).** The "doctor-pass FIRST so all leaves share one baseline" rule is for *existing* leaves. If the decomposition introduces **new** leaves/pages (they don't exist until the feature stories build them), a doctor-first pass can only cover the pre-existing surfaces and forces a *second* sweep for the new ones — so the single-sweep path is **build all the feature stories first, then one `/check-page --finish` across all leaves at once**. Decide the order at Phase B by asking *do the surfaces exist yet?*: all-exist → doctor-first; any-created-by-the-feature → doctor-last/one-sweep. Lived driver session 2026-06-23: §4's Profiles + Filters leaves didn't exist until US-SET-015/016 built them, so the premium sweep ran once at the end across all four UM leaves (the user's own sequencing call, validated).

**5b. Is any topic a SWEEP that a new check will force? (the acceptance-run smell — Q5
generalised beyond polish.)** Walk the topics once more with the checks in view. When a
topic's whole content is *bring the corpus to the state a new check demands* — fix the
twelve contradictions a consistency lint will report · restructure the file a ratchet
will measure · close the folds a reader will flag · replace the banners a registry will
check — it is the **acceptance run of the check's story**, not a story of its own. The
tell is the same as Q5's: its ACs read as a checklist the check already prints, and it
has no behaviour beyond "the check passes". Route it as the **first execution of the
check, in the session the check lands in, citing the statement or rule the check
enforces** (the Themelion phase-③ discipline: every sub-pass cites the declaration).
A sweep decomposed as a story is powered through; a sweep run as an acceptance proves
the check on production data on day one. Lived session 2026-09-05
(RP-AGORA-007, Shape B): five sweeps — the F1–F12 fixes and the `CLAUDE.md` rewrite, the
lived-record repair, the 31 bookkeeping closes, the `agora` restructure, Theme A's
canonicals — became the acceptance runs of five *statement + check* stories, and the
plan shrank from eighteen stories to twelve with nothing dropped.

### B.2 — Generate alternative shapes

Produce **2–3 alternative shapes** for the feature. Each shape is a different decomposition / scope / sequencing of the same goal. Format as a comparison table:

| Shape | What it is | Scope | Effort | Risk | What it defers |
|---|---|---|---|---|---|
| A | <one-liner> | <COUNTED stories + areas touched> | <weeks / one-dev> | <main risks> | <what gets cut to fit> |
| B | <one-liner> | … | … | … | … |
| C | <one-liner> | … | … | … | … |

At least one shape MUST be smaller than what the user proposed. At least one shape MUST be a "do nothing / use existing" option if it's plausible. **Every Scope figure is a count, never an estimate** — size each shape by a draft decomposition at the
C.1 grain before the table is written; a shape offered at a guess is a claim the user rules on (lived
session 2026-10-31: Shape A was offered at ~28 and counted 44 at Phase C — the ten defect families were ten stories).

### B.3 — Make a recommendation

State your honest recommendation. Use direct language. Examples:

- "Shape B. Reason: <reason>. Shape A is over-scoped because <X>; Shape C is under-scoped because <Y>."
- "I'd push back on the original framing. Reason: <reason>. None of the three alternatives address <Z> — that suggests the feature is being framed in the wrong direction."
- "Shape A as proposed. Reason: the simpler alternatives don't actually reduce scope — they defer hard decisions that block other work."

Avoid weasel words ("you might consider", "it depends on..."). The user has asked for direct review.

### B.4 — Pause gate

Print the comparison table + recommendation, then:

> ⏸  Phase B complete.
>
> - `proceed: <shape>` → decompose using shape A / B / C / your-merge
> - `refine: <feedback>` → I'll regenerate alternatives based on your feedback
> - `stop` → stop here

Wait for the user. Do NOT proceed silently.

---

## PHASE C — DECOMPOSITION

Once the user picks a shape:

### C.1 — Break into stories

Decompose the chosen shape into stories. Aim for **5–15 stories per feature** as a heuristic — fewer than 5 means the feature should probably be a single `/new-story` invocation; more than 15 means the shape is still too big and Phase B should have caught that.

**Allocate IDs by rescanning, not remembering (added 2026-06-01).** Before
assigning any number, `Glob requirements/stories/**/*.md` and extract every
existing `id:` for each prefix you'll use; compute `max(existing NNN) + 1` per
prefix and allocate the batch **sequentially** from there (max+1, max+2, …).
NEVER continue from a remembered count, the RP's own example ids, or "where the
last batch left off" — last session's Agora-improvements-3 decomposition collided
on US-AGORA-006/007/008 (already taken) and had to be manually renumbered to
009…015. This rescan is deterministic and must run **before** the C.3 table is
written; it is the *proactive* complement to the *reactive* collision-stop at
Phase D (line ~"Surface and stop … story id collision").

For each candidate story:
- Pick a prefix (existing or new — check `requirements/README.md` registry)
- Allocate the next available number **from the rescan above** (max+1 per prefix, sequential across the batch — never a guessed or remembered count)
- Write a one-line title
- Pick a priority (must-have / should-have / could-have / won't-have)
- Pick a phase (1 / 2 / 3 — implementation order)
- Pick the primary actor (must resolve to `actors.md`)
- List quality criteria the story will cite
- **UI surfaces touched** — list `ui_pages:` ids the story will affect. **Apply policy-ui-surface-discipline:** for each id, name the relationship to existing content (replaces / extends / sibling-of / new-surface). If "new-surface" or "sibling-of", justify it. This list flows into the story body as `### Lives at` and `### Reachable from` subsections in Phase D.

### C.1.b — Author one ASCII wireframe per UI-touching story (apply policy-ui-wireframes)

For every story in the decomposition whose `ui_pages:` is non-empty (or that adds a modal / changes a layout), draft a low-fidelity ASCII wireframe **now** — at decomposition time, not at implementation time.

The wireframe goes into the story body in Phase D under `## Design Reference`, alongside the `### Lives at` + `### Reachable from` blocks. It shows four things: **boundary** (which page/modal contains it), **regions** (header, sidebar, content blocks), **primary actions** (buttons, icons, placement), and **deep-links / nav** (arrows out, anchors, where you arrive from). See the policy file for two worked examples (a hub page and a modal).

Authoring wireframes at decomposition has two payoffs:

1. **It surfaces over-scoped stories early.** A story whose wireframe needs three pages worth of content is a story that should be split.
2. **It surfaces under-specified surfaces.** A story whose wireframe you can't draw because you don't know where it lives is a story missing a surface-discipline answer — fix at decomposition, not at implementation.

If you find yourself unable to draft a wireframe for a row in the decomposition table, **stop and ask the user**: that row is incomplete.

**A row-action story and a columns-on-an-existing-surface story are UI-touching too — they do not get to skip the Design Reference because "the wireframe lives in the sibling story".** The trap has a specific shape: a story whose UI is one button on a surface another story wireframed (a restore action on the Graveyard row, a "↶ undo" on a history-panel row), or two new columns on a leaf that already exists, reads as "no wireframe of its own" — and at volume (15 stories) the copy step is skipped for exactly those. Rule: every such story carries a `## Design Reference` that **references the parent surface's wireframe by story id** and draws **only its own delta** — the row's action column, the confirm/reason dialog, the new columns. Lived session 2026-08-26: three of fifteen stories (US-DAT-037, US-AUD-009, US-SET-044) shipped without one; the `--end` 2.4 audit caught it (Claim 5), fixed in `92032ceb`. The tell is mechanical: a story whose ACs name a button, a dialog, a badge or a column on an existing surface is on the C.1.b list whether or not its `ui_pages:` is empty.

### C.2 — Group umbrella UC + optional WF

Umbrella UC: one UC linking all the stories. ID format `UC-<DOMAIN>-NNN`. Frontmatter `related_stories:` lists every story in the decomposition.

Optional WF: only if the feature involves **cross-actor handoffs** (e.g. clerk → reviewer → auditor). For a feature that is one actor's CRUD against one entity, no WF is needed.

### C.3 — Append decomposition to the research paper

Open the paper from Phase A. Append:

```markdown
## Decomposition

**Chosen shape:** <A | B | C | merged> (Phase B)
**Decomposed:** YYYY-MM-DD
**Umbrella use case:** UC-<DOMAIN>-NNN

| Story id | Title | Actor | Priority | Phase | QCs |
|---|---|---|---|---|---|
| US-XXX-NNN | ... | editor | must-have | 1 | QC-SEC-001, QC-REL-002 |
| ... | ... | ... | ... | ... | ... |

**Phase 1 (must-have):** US-XXX-NNN, US-XXX-NNN, ...
**Phase 2 (should-have):** ...
**Phase 3 (could-have):** ...

## Goal & Milestones (Agora)

**Goal:** <feature name — added to COMPASS.md "Goals (active)" when the first Section opens against this paper>

**Milestones planted:**
- `milestone-<slug>-mvp` — Phase 1 (must-have) stories all implemented + tested
- `milestone-<slug>-reference` — Phase 2 (should-have) closed
- `milestone-<slug>-complete` — Phase 3 (could-have) closed (omit if no Phase 3)

Each Milestone fires `/agora --end` Path A when its sub-goal stories are
done. Drop a Milestone whose phase is empty.
```

**Do NOT update the paper's frontmatter yet.** Status stays `draft` and `related_stories` / `related_use_cases` stay empty until the actual files exist (Phase D writes them). Updating the frontmatter here would break the lint (R060 `related_stories` references must resolve to real story files) — the body table is the plan, the frontmatter is the commitment.

### C.4 — Pause gate

Print the decomposition table + summary:

> ⏸  Phase C complete.
>
> Proposed: {N} stories, 1 umbrella UC, {0|1} workflow.
> (If {N} differs from the chosen shape's Scope figure by more than a fifth, say so here first — the shape was sized wrong at B.2.)
> Affected feature areas: <list>.
> New prefixes that need adding to README registry: <list, or "none">.
> New actors that need adding to actors.md: <list, or "none">.
> New UI page registry entries needed: <list, or "none">.
> New QCs that don't exist yet: <list, or "none">.
>
> - `write` → write all {N+1+W} files now (auto-invokes /new-story for each story)
> - `split: 1,3,5` → write only stories 1, 3, 5 (you'll do the rest later)
> - `revise: <feedback>` → revise the decomposition table based on your feedback
> - `stop` → keep the research paper, do not write story files

Wait for explicit instruction.

---

## PHASE D — WRITE FILES

On `write` or `split`:

### D.1 — Pre-flight: register new vocabulary

Before writing stories, ensure all the metadata they reference exists:

- **New prefixes** → append to the appropriate thematic group in `requirements/README.md`. Insert into the closest existing group (e.g. a new `US-REF` for referrals belongs in the **Documents** or **Accounts & records** group depending on framing — pick the dominant one). Create a new group only if no existing group plausibly fits — adding a 22nd group of one prefix is almost always wrong.
- **New actors** → append a level-3 heading to `requirements/actors.md` in the right section (System-defined / Implicit / System actors)
- **New ui-pages** → append entries to the UI page registry (with all required fields — id, kind, label, url, template, route_file, entities, modal_pattern)
- **New glossary terms** → append rows to `requirements/glossary.md` in the appropriate section table

If any of these would be too speculative ("we'd need a new actor 'shift-supervisor' but I'm not sure that's right"), pause and ask the user instead of guessing.

### D.2 — Write story files using the canonical template

For each story in the decomposition table (filtered by `split:` if provided), write the file directly using the canonical template at `requirements/templates/_STORY_TEMPLATE.md`.

Each story's `## Notes` section MUST include a back-link line in this shape:

```
Derives from research paper [RP-XXX-NNN](RELATIVE-PATH) (Phase C, Shape <X>, story #<N> of <total>).
```

The link target is `docs/references/research/RP-XXX-NNN-<slug>.md`. From a story file's location at `requirements/stories/<area>/`, the relative path is `../../../docs/references/research/RP-XXX-NNN-<slug>.md` (three dots).

**For UI-touching stories**, the body MUST also include a `## Design Reference` section with three subsections, populated from Phase C.1 + C.1.b:

```markdown
## Design Reference

### Lives at

- **Primary surface:** <UI page registry id, or NEW: proposed-id>
- **Relationship to existing content:** replaces | extends | sibling-of | new-surface
- **If replacing/extending:** what currently lives there, and the migration plan.

### Reachable from

- **Primary entry:** <nav-id, or "deep-link from <surface>">
- **Secondary entries:** <list, or "none">
- **Search / global picker:** <yes/no>

### Wireframe

\`\`\`
<ASCII wireframe drafted in Phase C.1.b — boundary, regions, primary actions, deep-links>
\`\`\`
```

These blocks satisfy policy-ui-wireframes + policy-ui-surface-discipline. `/implement-story` Phase 1.6 reads them as the layout spec — the wireframe outranks prose acceptance criteria in conflict.

**Why we don't nest-invoke `/new-story` here:** earlier versions of this skill said to call `/new-story --from-plan RP-XXX-NNN` for each row. In practice, nesting 5+ skill invocations per `/feature-plan` run created friction (every nested invocation has its own pause gates and instruction-loading overhead). Both `/feature-plan` Phase D and `/new-story` use the same canonical `_STORY_TEMPLATE.md`, so writing files directly here produces identical output without the nesting cost. The `--from-plan` flag on `/new-story` still has a use: post-hoc story addition (when a user wants to add a 6th story to a research paper that's already been decomposed).

### D.3 — Write umbrella UC

Pick the next available `UC-<DOMAIN>-NNN` (DOMAIN is a topic-name — see existing `UC-SEARCH-`, `UC-BOOKING-`, `UC-EXPORT-`). Write the file using the canonical template at `requirements/templates/_USE_CASE_TEMPLATE.md`. Frontmatter:
- `related_stories:` lists every story id from D.2
- `actors:` is the union of all story actors
- `feature_areas:` from the research paper

### D.4 — Write WF (if applicable)

Only when the feature involves cross-actor handoffs. Pick the next available `WF-NNN`. Write the file using the canonical template at `requirements/templates/_WORKFLOW_TEMPLATE.md`. Frontmatter `related_use_cases:` references the umbrella UC from D.3.

### D.4a — Write umbrella implementation plan

Apply [policy-documentation](../../../.claude/policies/policy-documentation.md) — multi-story features get a platform-level implementation plan.

Copy `docs/implementation-plans/_TEMPLATE.md` to
`docs/implementation-plans/implementation-plan-<topic-slug>.md` and
fill in:

- `Story:` line replaced with `Stories:` listing every id from D.2
- `Scope:` referencing the research paper RP-XXX-NNN as the source of truth
- **Goal**, **Guiding principles**, **Architecture** lifted from the research paper's Phases A–B (don't re-derive — paraphrase)
- **Agora Goal & Milestones** — a short block naming the COMPASS Goal this plan opens and the Milestone tag(s) each phase will fire (mirror of the Phase C "Goal & Milestones (Agora)" appendix). The umbrella plan and the research paper carry the same Goal/Milestone mapping.
- **Phase 1..N** mirroring the decomposition table from Phase C of the research paper. Each phase block names the story id(s) it lands **and the Milestone its completion fires**.
- **Surprises & decisions log** with placeholder `_Phase N:_ tbd` lines (one per phase) — these get filled in by `/implement-story` as each story is built.
- `Status: draft`

This is the umbrella plan. Per-story plans (single-file, one per US-id)
are still authored by `/implement-story` Phase 2b when each individual
story is built — they reference back to this umbrella by URL.

Skip this step only when the decomposition produced exactly one story
(the per-story plan from `/implement-story` is enough on its own).

See `docs/implementation-plans/implementation-plan-hub-pages.md` for the reference example — that plan was authored from the US-UX-002 decomposition.

### D.4b — Update the research paper's frontmatter

Now that the story files, the umbrella UC, and any WF exist on disk, the research paper's frontmatter can finally be updated to commit the decomposition:

- `status: draft` → `status: active`
- `related_stories: []` → `related_stories: [<every story id from D.2>]`
- `related_use_cases: []` → `related_use_cases: [UC-<DOMAIN>-NNN from D.3]`

This is deliberately the LAST step before lint validation: every reference the frontmatter introduces must already resolve to a real file, otherwise R060 fails.

### D.5 — Validate

**First, the Design Reference presence check — before the lint, because the lint cannot see it.** For every story the C.1.b list names (every row with a non-empty `ui_pages:` PLUS every row-action / columns-on-an-existing-surface story per the C.1.b rule), assert the file carries `## Design Reference`:

```bash
grep -L '^## Design Reference' <the story files from the C.1.b list>   # must print NOTHING
```

A file name printed is a story to fix now, not later — at volume the copy step is the one that slips (three of fifteen at session 2026-08-26, caught only by the `--end` audit). The requirements lint has no notion of "UI-touching", so this grep is the executor's check; the deterministic half (non-empty `ui_pages:` ⇒ `## Design Reference` present) is captured as a lint-rule change request.

Then run the lint immediately:

```bash
python -m agora_checks catalogue
```

If errors:
- **Fix forward** if trivial (e.g. a typo'd actor slug)
- **Surface and stop** if the error suggests a structural mistake (e.g. a story id collision means decomposition picked an already-used number — this should *never* fire if C.1's rescan-don't-remember allocation ran; if it does, C.1 was skipped, so re-run the rescan rather than nudging the number by hand)
- Never silently rewrite a file the user just approved

### D.6 — Final summary

Print:

```
✅ Feature plan executed.

Research paper:
  docs/references/research/RP-<DOMAIN>-NNN-<slug>.md (status: active, depth: <m|d>)

Stories written ({N}):
  US-XXX-NNN — <title> [must-have, phase 1]
  US-XXX-NNN — <title> [must-have, phase 1]
  ...

Umbrella use case:
  UC-<DOMAIN>-NNN

Workflow (if any):
  WF-NNN

Catalogue updates:
  + N new prefixes registered in README
  + N new actors registered in actors.md
  + N new UI page registry entries
  + N new glossary terms

Agora Goal opened: <feature name>
Milestones planted:
  milestone-<slug>-mvp        ← Phase 1 (must-have) complete
  milestone-<slug>-reference  ← Phase 2 (should-have) complete
  milestone-<slug>-complete   ← Phase 3 (could-have) complete (if present)
(Remember to append the Goal to .claude/sessions/COMPASS.md before the
first /agora --start that works against it.)

Lint: 0 errors, 0 warnings (--check passed)

Next steps:
  /implement-story US-XXX-NNN     ← start with the highest-priority phase-1 story (one sub-goal = one commit)
  /implement-story US-XXX-NNN
  ...
  /agora --end (when Phase 1 stories close)  ← fires milestone-<slug>-mvp
```

---

## Key rules

- **Pause at every phase boundary.** Do not chain A → B → C → D silently. The user must approve each transition.
- **Hard-mode review.** No "you might consider…" — direct language with reasoning. The user has explicitly opted into honest critical review.
- **Cite, don't paste.** Web research goes into `sources:` with quoted summaries. Don't paste large blocks.
- **Prefer durable URLs.** W3C, IETF, official standards registries, professional-association pages. Avoid random blogs unless they're the canonical source.
- **No silent file creation.** Phase D writes files only after explicit `write` or `split: ...` from the user.
- **Run the lint after Phase D.** Always. The lint is the safety net — if a decomposition has dangling references, surface immediately.
- **Status transitions.** Research paper: `draft` (Phase A) → `active` (Phase C). Stories: always start `draft` (set by `/new-story`).
- **When unsure, pause and ask.** A speculative actor / prefix / page-id is worse than asking the user to confirm.

## Composes with other skills

- `/new-story` — Phase D writes story files directly using the canonical `_STORY_TEMPLATE.md` (no nested invocation). `/new-story` is the entry point when authoring a single story outside this pipeline, or for post-hoc additions to an already-decomposed paper (`--from-plan RP-XXX-NNN`)
- `/update-story` — for refining individual stories after Phase D
- `/implement-story` — for taking each story to code; **each story implementation is one sub-goal closed with one or more commits**
- `/agora` — `/feature-plan` plants the **Goal + Milestones**; Sections opened via `/agora --start` advance the sub-goals; `/agora --end` fires Milestone ceremonies when phases close (Path A). Add the Goal to `COMPASS.md` after Phase D writes the files
- `/learn` — capture lessons from the loop, especially after a feature plan that hit friction

## Initialisation

**What this skill reads before acting** (US-AGORA-041): Phase A discovery IS
the initialisation — the internal scan (models, routes, registries, existing
stories + UCs for the domain), the wiki AI context for the touched surfaces,
and web research at the chosen depth. A decomposition written before the
scan decomposes guesses.

**Self-model:** the decomposer — a feature bigger than one story becomes a
research paper, a critical review and N buildable stories. A gap noticed
mid-plan (a domain fact the scan missed, a registry it did not know to read)
lands as a 🟡 journal stub in [`experience.md`](experience.md).

## Claims at this level

The invariants other skills and the user depend on `/feature-plan` to hold (the
`hardened`-tier commitments; each is the unit `/learn` checks for contradiction
per `policy-skill-progression` Rule 4).

1. **Every run produces a lint-passing RP- research paper before any story is decomposed.** Phase A composes `RP-<DOMAIN>-NNN-<slug>.md` to the `_TEMPLATE.md` shape and Phase D runs the requirements lint to 0 errors before the run is done — downstream skills can always trust the paper resolves (Phase A.3 + D.5).
2. **No file is written without an explicit per-phase user nod.** The pipeline pauses at every phase boundary (A.4 / B.4 / C.4) and Phase D creates files only on a literal `write` / `split:` — A→B→C→D never chains silently.
3. **Story ids are allocated by rescanning the catalogue, never from memory.** Phase C.1 globs every existing `id:` per prefix and allocates `max+1` sequentially before the table is written, so a run never emits a colliding id (D.5 collision-stop is the backstop).
4. **A decomposed paper's frontmatter commits only after every reference it names exists on disk.** `related_stories` / `related_use_cases` stay empty and `status: draft` until Phase D.4b — after the files are written — so R060 reference resolution never breaks on a half-written plan.
5. **Every UI-touching story it emits carries a resolved surface relationship and an ASCII wireframe.** Phase C.1/C.1.b require `### Lives at` + `### Reachable from` + `### Wireframe` per UI story before Phase D writes it, satisfying policy-ui-surface-discipline + policy-ui-wireframes for the downstream `/implement-story` Phase 1.6 layout spec.
