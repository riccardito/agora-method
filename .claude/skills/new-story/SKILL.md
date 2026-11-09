---
name: new-story
description: "Create a user story with use case and quality criteria documents following the project's requirements format. Use when defining new features, writing requirements, or documenting planned functionality. Also writes the use case for a non-trivial feature and the workflow where multi-actor handoffs exist; prefix, actor and priority are inferred from the description unless given."
argument-hint: "<feature-description> [--prefix PREFIX] [--actor ROLE] [--priority LEVEL] [--from-plan RP-XXX-NNN]"
level: used
promoted_at: 2026-06-19
role: "the playwright"
---

# Create User Story + use case

Generate a complete requirements package for **$ARGUMENTS** in this project.

## When to use this skill vs `/feature-plan`

- **`/new-story`** (this skill) — for **≤2** well-scoped stories you already understand. One US-, optional UC-, optional WF-, optional mockup prompt. ~2 min.
- **`/feature-plan`** — for anything that **compounds to 3+ stories** OR a feature larger than one story (a module, a workflow, a compliance topic). Runs research + critical review + decomposition first, then invokes this skill once per story in the decomposition with `--from-plan`. ~30–60 min for the full pipeline.

**The boundary is ≤2 vs 3+/compounding.** `/new-story` writes **≤2 stories**; the moment the input compounds — several "simple" things that *add up* to something complex (the user's framing: *"5 simple things added together gets something complex; the feature plan holds all ideas together"*) — route to `/feature-plan` so the holding pipeline keeps the ideas coherent. If the user brings a "feature idea" that decomposes into several stories, push back: suggest `/feature-plan` instead. Don't write 6 stories from one paragraph of input — that compounds errors.

**The paper-backed exception (2026-08-29).** When the input is a strategy-paper
*topic* that already carries the description, acceptance criteria, consumers and
challenges (the `la-paz-last-topics.md` shape — a decomposition that never became
an RP file), 3 stories written from it are a Phase-D-style **write**, not a
compounding idea: treat it as `--from-plan` — link the paper from `## Notes` /
`## Background`, take actor and priority from it, skip Step 4b's mockup prompt —
and author the umbrella UC. Running `/feature-plan` would redo research the paper
already holds. Lived session 2026-08-29: Topic 5 →
US-UX-035 / US-PHY-014 / US-DGN-004 + UC-UX-013, lint 0/0/0 first pass.

## Arguments

- `$0` — Feature description (e.g., "bulk contact import", "duplicate booking checker")
- `--prefix` — Story ID prefix (e.g., `APT`, `PAT`, `INV`). If omitted, infer from feature area
- `--actor` — Primary actor (default: infer from feature)
- `--priority` — `must-have`, `should-have`, `could-have`, `won't-have` (default: `should-have`)
- `--from-plan RP-XXX-NNN` — invoked by `/feature-plan` Phase D. Pre-fill `feature_area` from the research paper, link the paper from `## Notes`, and skip the optional mockup-prompt step (Phase D handles design separately).

## Step 0 — `--from-plan` pre-load (when invoked from /feature-plan)

If `--from-plan RP-XXX-NNN` is given:

1. Read `docs/references/research/RP-XXX-NNN-*.md` — confirm it exists and `status: active` (Phase C marked it active when decomposition was approved)
2. Pull from the research paper:
   - `feature_areas[0]` → use as the story's `feature_area`
   - The decomposition table row matching `$0` (the title) → use its `actor`, `priority`, `phase`, and listed QCs as defaults
3. The story's `## Notes` section MUST include a back-link line:
   ```
   - Derives from research paper RP-XXX-NNN at `docs/references/research/RP-XXX-NNN-<slug>.md` (use a relative link from the story file's location: `../../../docs/references/research/RP-XXX-NNN-<slug>.md`).
   ```
4. **Skip Step 4b** (mockup prompt). `/feature-plan` Phase D handles design separately for the whole feature, not per-story.
5. Otherwise continue with Steps 1–8 below as normal.

## Step 1 — Research existing conventions

Before writing, gather context:

1. Read `requirements/README.md` for ID conventions, the canonical prefix registry, the status / source / priority enums, and the QC reference table — all in one place. Do NOT duplicate any of this knowledge into the story you're writing; just reference it.
2. Use Glob to find existing stories in the target feature area:
   ```
   requirements/stories/<feature-area>/US-*.md
   ```
3. Determine the **next available ID number** for the prefix (e.g., if US-APT-012 exists, use US-APT-013)
4. Check existing use cases:
   ```
   requirements/use-cases/UC-*.md
   ```
5. Determine the next available UC ID
6. Read the related route file(s) if the feature touches existing code (find them through the story prefix and the feature area)
7. Read the related model file(s) if applicable
8. **If the story is grounded on a research paper (RP-)** — via `--from-plan` OR a
   prompt pointing at the RP — re-verify the RP's **architectural contract claims**
   (render pattern, fragment-load vs inline, widget lifecycle) against the **lived
   pattern notes** in the build skill (`/implement-story` Phase 1.4b) before writing
   them into acceptance criteria. RPs age faster than the pattern library: data-shape
   facts (model fields, enums) are verified against *code* (steps 6–7 above);
   architecture claims are verified against the *current SKILL.md notes*. Lived:
   RP-UHB-001 prescribed a "fragment-load contract" for User-Hub leaves, but the
   lived §2 pattern was inline server-side render (Option B) — the copied AC had to
   be corrected at implement Phase 1 (session 2026-07-04).

## Step 2 — Pick the ID prefix and folder

The canonical prefix registry lives in `requirements/README.md` ("User Stories (US-)" section, grouped by domain). Read it. Pick the closest existing prefix; the folder under `requirements/stories/` matches the prefix's domain.

If no existing prefix fits, propose a new one (format `US-[A-Z][A-Z0-9]+`, e.g. `US-REF`). New prefixes must be added to the README's domain table BEFORE the story is linted (here the check holds the id's shape, rule C01; the parent's R003 also held the prefix table) — insert into the closest thematic group; create a new group only if no existing group plausibly fits.

## Step 3 — Write the User Story

Create `requirements/stories/<feature-area>/US-<PREFIX>-<NNN>-<kebab-title>.md` using the canonical story template at `requirements/templates/_STORY_TEMPLATE.md`. The template defines the frontmatter contract (which fields are required, which enums apply, which lint rule each field is checked by) and the body section structure (User Story, Acceptance Criteria, use case flow, Preconditions, Postconditions, Notes).

When you replace the template's placeholders with real values:
- `actor` must resolve to a level-3 heading slug in `requirements/actors.md` (C06)
- `quality_criteria` ids must resolve to existing QC files (C12) — see the QC reference table in `requirements/README.md` for what each QC covers
- `ui_pages` ids must resolve to entries in the UI page registry (the parent's R011; a registry this repository does not ship, so the catalogue check does not hold it)
- `glossary_terms` ids must resolve to entries in `requirements/glossary.md` (C12)
- `status: draft` for newly-authored stories (the lifecycle moves forward later via `/implement-story`) -- `review` when the story is complete and waits on the user's ruling of its open questions, and never `approved` at authoring, whoever writes it and whatever a spawn briefing asks (lived session 2026-10-10: two spawn-authored stories briefed `approved` over 16 and 13 unruled questions)

Acceptance criteria must be **specific and testable** — avoid vague criteria like "should work well". **An AC that states a HARD RULE over an existing corpus is measured against that corpus at authoring** (one grep or a ten-line script), and the measured count goes into the AC: a rule the corpus contradicts wholesale is a sweep the story must price, not a lint the build can turn on, and a count taken from memory is a premise the builder will have to re-derive (lived session 2026-09-11: US-WIK-031 forbade a body H1 that 105 of 107 seeds carried, guarded a Jinja trap seed markdown cannot fire, and said 20 non-parsing blocks where the corpus held 32 — all three moved at the build's plan gate). **The same holds for an AC that NAMES A CHECK or A PATH — each is a claim, measured at authoring:** run the named verification once against an input that must FAIL it (a check that answers the same for a good and a bad input cannot fail), and `ls` every path the AC says something lives at (lived session 2026-09-21: US-OPS-019, written from an Issue's text, put uploads in an `instance/` folder, assumed a signing-key directory the box did not have, and verified a database dump with a restore dry-run — which exits 0 on a truncated archive; the build overturned all three within the hour). **A `docs/stats.yaml` key an AC adds must be TREE-derivable.** The stats collector reads the repository only; the pre-push hook regenerates the file and CI compares it on a fresh checkout with an EMPTY database, so a count of DB rows there reds the staleness gate on every machine whose data differs. Live numbers (pages published, checks made, rows per origin) belong to a CLI line or a UI tile that reads the database — the plan default *"`wiki.pages_live` in stats.yaml"* was overturned at authoring for exactly this (lived session 2026-09-11, US-WIK-030).

## Step 4b — Mandatory `## Design Reference` for UI-touching stories

**Skip this step only if the story is genuinely API-only** (no Jinja template touched, no route renders an HTML response). If the story affects *any* surface a user sees — a new page, a modal, a form, a list, a single column added to a table — this step is required.

Apply `policy-ui-wireframes` (the wireframe is mandatory) and `policy-ui-surface-discipline` (the surface placement is explicit). The story body's `## Design Reference` section answers three coupled questions: **(a) where it lives**, **(b) where it's reachable from**, and **(c) what it looks like (wireframe).**

### Step 4b.1 — Audit existing UI surfaces

For every `ui_pages:` id you're about to put in the frontmatter:

1. **Look it up in the UI page registry.** Does it already exist?
2. **If yes:** read the page's `template:` and `notes:`. Name what currently renders there. List the visible widgets / sections.
3. **Decide the relationship explicitly:** is this story (a) **replacing** the current content, (b) **extending** it (new column / new button / new region), or (c) creating a **sibling surface** alongside it?
4. **If sibling-of or new-surface, justify it.** Default is "extend the existing surface." See `policy-ui-surface-discipline` Rule 3 for what counts as a valid sibling-surface reason.

This is the gate that prevents the "we built a duplicate page" failure (US-ACC-001 incident). Do it before drafting the wireframe — the audit constrains what the wireframe must show.

**And every LISTING SITE an AC names is read from its template before the AC is written — a plausible tile name is a claim.** "The `/wiki?tab=stats` coverage tile gains a row" named a tile that leaf does not have (its *Wiki pages* KPI unit was the listing site); the build found out at Phase 4 and re-homed the row. One `grep -n "bento-head\|kpi.key" <leaf>.html` at authoring is the whole check — the same load-bearing-claim rule the `ui_pages` lookup already applies to the *page*, applied to the *element* (lived session 2026-09-11, US-WIK-030 AC6).

### Step 4b.2 — Draft the ASCII wireframe

Apply `policy-ui-wireframes`. Draw a low-fidelity ASCII wireframe showing four things:

- **Boundary** — which page/modal contains it (label the outer box)
- **Regions** — header, sidebar, content blocks, footer
- **Primary actions** — `[+]`, `[Save]`, `[X]`, `[↗]` — position matters
- **Deep-links / nav** — arrows out, anchors, `← Back` links

Use UTF-8 box-drawing characters (`┌─┐│└┘├┤┴`). Don't render content for every cell — show structure. See the policy file for two worked examples (a hub page and a modal).

If you cannot draft a wireframe, the story is under-specified — ask the user. Authoring code from prose-only specs reproduces the US-ACC-001 failure mode.

**For layout-sensitive SHARED CHROME (the app header, overlay/badge systems,
anything absolutely-positioned among flowing siblings), actively RECOMMEND a
ClaudeDesign mockup at story time** — the ASCII wireframe stays canonical
(`policy-ui-wireframes` Rule 3), but it cannot express container reality
(which elements share a positioning context, what's fixed vs flowing vs
absolutely-centered), and that's exactly where the build degrades into manual
element-moving rounds. Lived: US-MOB-023 — the badge-pair wireframe was right,
but the app-header elements "weren't on proper containers, so there was a lot
of manually moving around the badges"; the user's retro: *"it would probably
be better to directly get a mockup from ClaudeDesign, that would have saved
us a lot of time"* (session 2026-07-23). Offer the mockup as a
supplement in the Design Reference (`Source:` row); for ordinary
page-body/modal stories the ASCII alone remains sufficient.

### Step 4b.3 — Write the `## Design Reference` block

Add to the story body, immediately after `## Notes`:

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
┌──────────────────────────────────────────────────┐
│  <page / modal title>          [primary action]  │
├──────────────────────────────────────────────────┤
│  <regions, widgets, links, deep-links>           │
└──────────────────────────────────────────────────┘
\`\`\`
```

Optional supplementary blocks (only if helpful):

- `### Frontmatter updates needed` — routes/models to add to story frontmatter
- `### Macro mapping` — element → Jinja macro (`field`, `select_field`, `textarea_field`, `btn`); flag any **NEW:** macros to create
- `### Behavior rules` — 0/1–N/N+ counts, device differences, permission variants
- `### Out of scope` — features visible in the wireframe but deferred (with follow-up story IDs)

The Design Reference is what `/implement-story` Phase 1.6 reads as the layout spec. The wireframe outranks prose acceptance criteria in conflict (see `policy-ui-wireframes` Rule 5).

### Optional Step 4b.4 — Figma supplement (not a substitute)

If the user wants a high-fidelity Figma mockup *in addition to* the ASCII wireframe, draft a Claude Design prompt and let them paste it into [claude.ai/design](https://claude.ai/design). The prompt is supplementary — the ASCII wireframe is still mandatory and is the authoritative artefact. Add the Figma URL to the `## Design Reference` section under `**Source:**` once it exists.

Prerequisite for Claude Design: the project's **design-system seed** (`docs/references/strategy/design-system-seed.md`) must be active in the user's Claude Design project, otherwise output drifts from the project's conventions.

If/when a Figma file exists, `/update-story <US-ID> --from-figma <url>` syncs the structured Design Reference fields back from it — but the ASCII wireframe stays in the body regardless.

## Step 5 — Write the use case (if the feature is non-trivial)

For simple CRUD stories, skip this step. For features with multiple actors, alternative flows, or complex logic, create `requirements/use-cases/UC-<DOMAIN>-<NNN>-<kebab-title>.md` using the canonical UC template at `requirements/templates/_USE_CASE_TEMPLATE.md`. The template defines the frontmatter contract (R020 — every `related_stories` id must resolve) and the body sections (Summary / Actors / Preconditions / Main Flow / Alternative Flows / Error Handling / Postconditions / Related Stories).

Pick the next available `UC-<DOMAIN>-NNN` by globbing `requirements/use-cases/UC-<DOMAIN>-*.md`. The DOMAIN is a topic-name, not necessarily a story prefix (existing examples: `UC-SEARCH-`, `UC-BOOKING-`, `UC-EXPORT-`, `UC-AUTH-`).

## Step 6 — Write a Workflow (only if multi-step handoffs exist)

Only create `requirements/workflows/WF-<NNN>-<kebab-title>.md` when the feature involves handoffs between multiple actors or systems. Use the canonical WF template at `requirements/templates/_WORKFLOW_TEMPLATE.md`. The template defines the frontmatter contract (R030 — every `related_use_cases` id must resolve) and the body structure (Overview / Flow Diagram / Handoff Points / Audit-log events / Notes).

Pick the next available `WF-NNN` by globbing `requirements/workflows/WF-*.md`.

## Step 7 — Cross-link documents

After creating files:
1. Add `quality_criteria` references in the user story frontmatter
2. Add `related_stories` in the use case frontmatter
3. If a workflow was created, add `related_use_cases` in its frontmatter

## Step 8 — Summary and Next Steps

Print a summary of created files and the full skill workflow the user can follow:

```
Created:
  - requirements/stories/<area>/US-XXX-NNN-title.md
  - requirements/use-cases/UC-DOMAIN-NNN-title.md (if applicable)
  - requirements/workflows/WF-NNN-title.md (if applicable)

Quality criteria referenced: QC-SEC-001, QC-REL-001, ...
```

Then show the **next steps workflow** — the full pipeline of skills available to take this story from requirements to production:

```
You are here
  ✓ /new-story         ─── Requirements written (+ optional mockup prompt drafted)
    │
    ▼  If mockup was drafted: paste prompt into claude.ai/design, iterate in Figma
    │
    ▼  Sync the Figma design back into the story (skip if no mockup):
    /update-story US-XXX-NNN --from-figma <url>
    │
    ▼  Build the feature:
  → /implement-story US-XXX-NNN    ─── Build model, routes, templates, tests
    │                                 (reads ## Design Reference if present)
    │
    ▼  Iteration loop — any time the story or design changes:
    /update-story US-XXX-NNN --from-feedback "..."  ─── Apply text feedback
    /update-story US-XXX-NNN --from-figma <url>     ─── Re-sync Figma edits
    /update-story US-XXX-NNN                        ─── Propagate hand-edits
    │
    ▼  Validate:
    /check-ui-entity <Entity>       ─── Audit registries / modals / gaps
    /fixbug                         ─── Fix any issues found during testing
    │
    ▼  Ship:
    /deploy #dev #seed              ─── Deploy and verify
    /learn                          ─── Capture lessons from the loop
    │
    ▼  Cross-cutting (periodic, not per-feature):
    /check-coverage                 ─── Python test coverage health check
    /selenium --add <feature>       ─── Add Selenium tests once shape is stable
    /manage-translations            ─── Audit i18n pipeline health
```

**Provide the concrete commands** with the actual story ID and feature name filled in. For example:

```
Next steps:
  1. /implement-story US-EXP-005
  2. /check-ui-entity ExportJob
  3. /deploy #dev #seed

Periodic (not per-feature):
  /check-coverage --module export_jobs ─── focused coverage drill
  /selenium --add export-jobs          ─── once the UI has stabilised
```

## Key Rules

- **A sweep is not a story.** If the story's whole content is bringing existing files to the state a check demands (fix what a lint reports, restructure what a ratchet measures), it is that check's acceptance run — route it to the session that lands the check, citing the rule it enforces (`/feature-plan` Phase B.1 Q5b). A story needs behaviour of its own.

- **Always** use YAML frontmatter with `---` delimiters
- **Always** use unchecked checkboxes `- [ ]` for acceptance criteria
- **Always** include the `As a **X**, I want to **Y**, so that **Z**` format
- **Always** reference at least one quality criterion
- **Never** skip preconditions or postconditions
- Use `status: draft` for all new documents
- Use **bold** for actor roles and "quotes" for UI button text
- Use backticks for code values: `status: 'active'`, `appointments:write`
- Dates in prose in DD.MM.YYYY format (e.g., "25.03.2026")
- Keep acceptance criteria **specific and testable** — avoid vague criteria like "should work well"
