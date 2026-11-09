---
name: update-story
description: Reconcile a change to an existing user story across the story file, code, and tests. Three input modes — text feedback, Figma mockup sync, or hand-edited story file. Auto-invokes implement-story for the delta (gated) and optionally runs check-ui-entity. Use when refining requirements after initial implementation, syncing design feedback from Figma, or when the story has drifted from the code.
argument-hint: '<US-ID> [--from-feedback "<text>"] [--from-figma <url>] [--no-implement] [--no-validate]'
level: used
promoted_at: 2026-05-31
role: "the mediator"
---

> **Journal-at-source** (policy-skill-progression Rule 6): when you finish a unit of work in a session, append ONE unrated stub to [`experience.md`](experience.md) `## Unrated journal` — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`. One line, lighter than the session Log; `/agora --end` 2.3b grades it.

# Update User Story

Reconcile a change to **$ARGUMENTS** across the story document, the implementation, and the tests.

## Arguments

- `$0` — User story ID (e.g., `US-APT-013`) or path to the story file
- `--from-feedback "<text>"` — Apply text feedback to the story. The skill rewrites the affected sections (acceptance criteria, use case flow, frontmatter) and shows a diff before writing.
- `--from-figma <url>` — Sync a Figma design back into the story. Pulls design context via the Figma MCP and appends a `## Design Reference` section. Acceptance criteria are NOT auto-rewritten — you merge them manually.
- `--no-implement` — Update the story only. Do not propagate to code.
- `--no-validate` — Skip tests and check-ui-entity after implementation.

If neither `--from-feedback` nor `--from-figma` is given, the skill assumes you have already hand-edited the story file. It runs `git diff <story-path>` and propagates whatever changed.

---

## PHASE 1: LOCATE & UNDERSTAND

### 1.1 — Find the story

- If `$0` looks like a path, read it directly
- If `$0` looks like an ID (e.g., `US-APT-013`), search: `requirements/stories/**/US-APT-013*.md`

### 1.2 — Read the current story state

Note from the file:
- **Frontmatter**: `status`, `ui_pages`, `actor`, `related_routes`, `related_models`, `related_tests`, `quality_criteria`
- **Acceptance criteria** (the checkboxes)
- **Use case flow** (the numbered steps)
- **`## Design Reference` section** (if present)

**Story status guard:** if `status: tested`, ask the user before continuing — updating a tested story regresses it.

### 1.3 — Read related artifacts (skip if `--no-implement`)

Read the use case (`requirements/use-cases/UC-*.md`), workflow (`requirements/workflows/WF-*.md`), and quality criteria docs referenced in the frontmatter — same pattern as `implement-story` Phase 1.2-1.5. You need these to know what code areas the change might touch.

Also audit what already exists for the related routes and models (Phase 1.4 of `implement-story`).

---

## PHASE 2: APPLY THE CHANGE

Pick one branch based on the arguments.

### 2A — `--from-feedback "<text>"`

The user gave plain-text feedback. Map it to story sections:

| Feedback shape | Likely target section |
|----------------|----------------------|
| "the button should be at the top-right" | Use case flow + design notes |
| "we also need to support X" | New acceptance criterion |
| "this is editor-only" | Frontmatter `actor` + permissions in QC |
| "make it work for archived projects too" | Preconditions + alternative flow |
| "rename Y to Z everywhere" | Acceptance criteria + use case flow |
| "the rebuilt surface dropped a claimed AC" (a ruling pin on a retired editor's feature — ruled *deferred parity*, not dropped) | A `[~]` note **under the AC** naming the gap + the surface + the strict-xfail pin by test name and file; `status:` → `partially-implemented`; the use-case step annotated; the build's home cited (a sub-goal Issue). Nothing is un-ticked and nothing is built — the pin stays the acceptance test (lived session 2026-09-10: US-DOC-007/016 → #483) |

**Procedure:**

1. Draft the edits (in memory, not yet written).
2. Show the user a unified diff of the story file (before vs after).
3. Ask: **"Apply these changes? (y/n)"** — wait for explicit confirmation.
4. On `y`, write the file.

Do not silently rewrite. Always show the diff first.

**Scoping (2026-08-29) — a diff gate does not re-fire a ruling already nodded.**
When a session gate has ALREADY nodded per-story rulings that name each edit (a
`--start` plan gate or a phase gate reading *"drop the retired-drawer ACs · defer X
to #NNN · flip to `review`"*), the per-story diff-and-y/n re-gates a decision made
minutes earlier (`policy-four-eyes` Rule 1 — gates fire at transitions, and this
one already had its gate). Apply the edits, summarize the diff per story in the
phase's Log entry, and let the phase seam be the gate — the §2D reading of the
Key Rule applies here too: *silently* is forbidden; a second gate is not
required. Lived session 2026-08-29: five mobile stories
under the B7 terminal rulings, each tick cited from the claims-vs-code audit. **The scoping covers the edits the ruling NAMES, never a design claim the edit adds:** a `### Lives at` / wireframe written while re-homing an Issue is a new decision, so it is put to the user at the phase gate BEFORE its commit, not disclosed after (lived session 2026-10-09: #672's re-home was ruled, the link token's place on the User-Hub Notifications leaf was not, and `9c2c93e7` preceded the nod).

### 2B — `--from-figma <url>` (or `--from-html` / paste)

The user iterated on the design (in Figma, in Claude Design HTML output, or in any other tool) and wants the result reflected in the story.

> **Boundary — the same-session planning fold is NOT this mode.** When a
> planning session authors stories and a mockup (or its correction) returns
> **in that same session, before any code exists**, folding it into the
> just-written `draft` stories is legitimately inline — the fold is part of
> the planning pass, not a drift-reconciliation. This mode's territory is a
> story that has drifted from a **later** design iteration (code and tests
> may exist; propagation is the point). Lived twice with the same
> justification (session 2026-07-27, session 2026-07-28
> — recorded as borderline missed-routing both times before this note named
> the exception).

1. **Parse the source URL** — if a Figma URL, extract `fileKey` and `nodeId` per the Figma MCP rules:
   - `figma.com/design/:fileKey/:fileName?node-id=:nodeId` — convert `-` to `:` in nodeId
   - `figma.com/design/:fileKey/branch/:branchKey/:fileName` — use `branchKey` as fileKey
   - For Claude Design HTML: the source is a relative path or upload URL — no parsing needed
2. **Pull design context** — for Figma, call `mcp__claude_ai_Figma__get_design_context` with the parsed args. For HTML, the user pastes a structured Design Reference block directly (see step 4 for the format).
3. **Extract** from the response:
   - Component list (name + role) — map each to an existing template macro from the shared components file, or mark **NEW** if a macro doesn't exist yet
   - Design tokens used — prefer canonical names from the design-token file over Figma/HTML paraphrases (e.g., use `--color-border` not `--color-border-input`)
   - Page layout pattern (sidebar / full-page / hub-tab / htmx-fragment-modal / inline-js-modal / mobile-tablet-wizard)
   - Code Connect mappings, if any — these point at existing shared macros (`field()`, `btn()`, `section_filter_bar`, etc.)
   - **NEW routes / NEW models** implied by the design (see step 5)
4. **Build the Design Reference block.** The full template — every section is optional and only appears when relevant, but the order is fixed. This is the rewrite `policy-ui-wireframes` Rule 4 assigns to this skill (the wireframe is redrawn when the design changes) and the re-answer `policy-ui-surface-discipline` Rule 4 expects (`### Lives at` / `### Reachable from` re-resolved against the synced design):

   ```markdown
   ## Design Reference

   - **Source:** <Figma URL | HTML mockup path | other>
   - **Synced:** <ISO date, e.g., 2026-05-07>
   - **Page id:** <existing-id | NEW: <proposed-id>>
   - **Layout pattern:** <sidebar | full-page | hub-tab | htmx-fragment-modal | inline-js-modal | mobile-tablet-wizard | other>
   - **Actor:** <role> · **Domain:** <domain group>

   ### Frontmatter updates needed

   (Only if the design implies new routes or models not currently in the story's frontmatter.)

   related_routes (add):
     - <METHOD> /<path>#<handler>
   related_models (add):
     - <ModelName>

   ### Page entry to add to the UI page registry

   (Only if the design introduces a new page surface.)

   ```yaml
   - id: <new-page-id>
     kind: <primary | secondary | data-tab | quick-create>
     menu_item: "<label>"
     url: /<path>
     template: <relative path>
     route_file: <relative path>
     entities_managed: [<EntityName>, ...]
   ```

   ### Surface chrome

   App bar / progress strip / body / action bar — describe each region with sizing, colors (referencing tokens), and content rules.

   ### Macro mapping (Jinja → mockup)

   | Mockup element | Jinja macro | File |
   |---|---|---|
   | <element> | `field(...)` | the shared components file |
   | <element> | **NEW:** `<new_macro>(...)` | add to the shared components file |

   The **NEW:** annotation tells `/implement-story` Phase 3.3 to create the macro. Mark every macro that doesn't exist yet.

   ### Tokens (referenced from the design-token file)

   - List the tokens used (use canonical names from the token file)
   - Touch target sizes, radii, shadows, motion durations as needed

   ### Step-by-step (or per-screen layout)

   For each screen / step / artboard, describe:
   - Fields and their types
   - Behavior contracts (e.g., "On-blur after name + date of birth: POST /signup/match → ...")
   - Device variants (tablet vs phone, detail-mode vs base, etc.)
   - Validation rules

   Behavior contracts are the most important — they specify routes and JS behavior in plain English so `/implement-story` translates 1:1 without guessing.

   ### State machine

   ASCII diagram of state transitions (only for multi-step flows). Maps directly to wizard router state in JS or to the route handler graph.

   ### Acceptance-criteria mapping

   | Criterion (from story) | Where shown |
   |---|---|
   | <criterion> | <element / artboard / behavior> |

   Makes verification trivial — every criterion gets a where-it-lives anchor.

   ### Behavior rules

   Edge-case rules that don't fit acceptance criteria but matter for implementation:
   - 0 / 1–N / N+ count rules
   - Device-specific behavior differences
   - Permission-gated UI variants

   ### Out of scope (do not implement from this mockup)

   - Features visible in the mockup but deferred to a separate story
   - Adjacent flows referenced but owned elsewhere

   Keeps scope creep out of `/implement-story`.

   ### Caveats / follow-ups

   - Known gaps in the design with logged follow-up story IDs (e.g., "low-confidence match disambiguation → US-MOB-016")
   - Reviewer-flagged concerns with resolution path

   _Review and merge into Acceptance Criteria as needed._
   ```

   Not every section is required. Scale to story complexity — a one-button change might only need Source / Synced / Macro mapping. A multi-step wizard uses the full template.

5. **Frontmatter sync detection.** While building the block, scan for routes and models the design references. Compare against the story's current `related_routes` and `related_models` frontmatter:
   - For each route mentioned (e.g., `POST /signup/match`) not in `related_routes`: add to the **Frontmatter updates needed** subsection.
   - For each model mentioned (e.g., `SignupReasonPreset`) not in `related_models`: add to the same subsection.
   - During Phase 3 propagation, ask the user before applying frontmatter updates — never silent.

6. **Append** to the story file. If a `## Design Reference` block already exists, replace it (the new sync is the source of truth for design now).
7. **Acceptance criteria are NOT auto-rewritten.** The user reads the Design Reference and decides what's load-bearing.
8. **New surface check:** if the design implies a new page (e.g., a layout pattern that doesn't match any `nav-*` in the UI page registry), surface this:

   > "The design appears to introduce a new page surface. Add an entry to the UI page registry? (y/n)"

   Only add on explicit `y`. The proposed entry should already be in the **Page entry to add to the UI page registry** subsection of the Design Reference block.
9. Show the user the diff.

### 2C — Direct edit (no flag)

The user already edited the story file. Read `git diff <story-path>` and identify what changed:

| Section changed | Likely code impact |
|-----------------|--------------------|
| Frontmatter `actor` | Permission decorators, the default-role table |
| Frontmatter `related_routes` (added) | New route handlers |
| Frontmatter `related_models` (added) | New model fields, `ALLOWED_UPDATE_FIELDS` |
| Frontmatter `ui_pages` (added) | New page entry in the UI page registry, possibly new template |
| Frontmatter `quality_criteria` (added) | New QC requirements (e.g., audit logging) |
| Acceptance criteria | Tests + possibly route handlers |
| Use case flow | Route handlers + templates |
| `## Design Reference` (any subsection) | Templates + JS at minimum. Plus, depending on subsections present: |
| ↳ `### Frontmatter updates needed` | Apply to story frontmatter (with confirm); cascades to routes/models below |
| ↳ `### Page entry to add to the UI page registry` | Add the entry to the UI page registry (with confirm) |
| ↳ `### Macro mapping` with **NEW:** annotations | Add the new macros to the shared components file |
| ↳ `### Step-by-step` behavior contracts | Route handlers + JS state management |
| ↳ `### State machine` | Wizard router state in JS, or route handler graph |
| ↳ `### Acceptance-criteria mapping` | Drives test cases (one per row) |
| ↳ `### Behavior rules` | Conditional rendering / edge-case logic in templates and routes |
| ↳ `### Out of scope` | What NOT to build — exclude from the propagation plan |
| ↳ `### Caveats / follow-ups` | Logged story IDs (`US-XXX-NNN`) — verify they exist or propose creating them |
| Pre/postconditions | Validation logic, side effects |

This is an analysis step only — no story edits.

---

### 2D — Reconcile-to-code (the code landed first)

The fourth shape, and the one `/agora` routes here most often at a session
close: **the code changed deliberately to satisfy ACs the story itself had
deferred**, and the story now has to catch up. It is none of 2A/2B/2C — no
feedback text, no design sync, and 2C is explicitly *analysis only*.

The tell is the **direction of truth**. In 2A–2C the story leads and code
follows; here an earlier session wrote `[~]` against an AC with a stated reason,
a later session removed that reason, and the story is the stale artefact. That is
still the "story is the source of truth" rule holding — the code was changed to
satisfy *the story's own criteria*, not the story bent to match drift.

**The diff gate does not re-fire when a session plan already authorized the
flip.** The Key Rule *"never rewrite acceptance criteria silently — always show
the diff and ask"* exists to stop the skill inventing requirements. When
`/agora --start` 1.4 declared the phase as *"flip US-XXX off
`partially-implemented`"* and the user nodded it, asking again is re-gating a
decision already made (`policy-four-eyes` Rule 1 — gates fire at transitions, and
this transition already had one). Report what changed instead of gating it.

**What this mode must still do, and it is not optional:**

1. **Tick each `[~]` AC with a citation** — the commit sha and what closed it.
   An AC flipped without a citation is indistinguishable from one flipped by
   optimism.
2. **Re-read every *other* AC against the new code**, especially a
   "no user-visible change" claim — the deferral may have been protecting it.
   State the evidence rather than re-asserting the claim.
3. **Update the stale rationale in the CODE**, not only in the story. A comment
   explaining why something was deferred is wrong the moment it lands, and it is
   the artefact the next reader hits first.
4. **Flip `status:`** and run the requirements lint.

Skip Phase 3 — the propagation already happened; that is what defines this mode.

Lived session 2026-08-09: US-UX-024's two `[~]` ACs were closed by
T-080, and the skill had no mode for the direction — so the run either re-gated a
nodded flip or skipped a Key Rule. Same shape as §2B's planning-fold exception:
the rule is right, its scope needed naming.

## PHASE 3: PROPAGATE TO CODE (skip if `--no-implement`)

### 3.1 — Build the propagation plan

For each story change, list the concrete files that need to be touched. The plan should walk through the Design Reference subsections in order (if a `## Design Reference` block changed) — that ordering matches the implementation phases in `/implement-story`.

**If the change rewrites an existing template** (Figma sync of an existing page, "match the new mockup" feedback, layout standardization), apply policy-migration-discipline — inventory the existing template's `extrahead` block, visible UI elements, inline `<script>`s, and `onclick=` handlers; map each to the new design; surface anything without a home in the propagation plan as an Open question **before** writing code. Silent drops are the regression class this catches.

**When the propagation plan changes templates, modals, or htmx flows**, apply policy-frontend-conventions — every new template must follow the 8 entity-registration touchpoints (Rule 1), modal title/border conventions (Rules 2–4, *modal title* · *modal border* · *modal click-event safety*, and the spark/detail corollary), htmx self-refresh + `hx-select` patterns (Rules 5, 7 and 14 — *JS-rendered cards* · *section refresh* · *context-processor helper / `hx-select` inheritance*), and the Alpine + htmx data-passing rules (Rule 6, *Alpine + htmx timing*). Surface convention violations in the plan *before* invoking `/implement-story`.

**When the propagation plan adds or renames code paths, surfaces, or fields**, apply [policy-documentation](../../../.claude/policies/policy-documentation.md) — the related wiki seed (`docs/wiki/feature-<slug>.md`) MUST be updated in the same change set, not deferred. If no seed exists yet for the touched feature, add seed-creation to the propagation plan.

**When the propagation plan touches user-facing pages or modals**, apply policy-selenium-coverage — Selenium coverage for the affected page must be re-asserted or extended. If the touched route has no Selenium test, surface that gap in the plan; `/implement-story` Phase 4 will follow up.

Example output:

```
Story changes detected:
  + Acceptance criterion: "User can bulk-import records from CSV"
  ~ Design Reference replaced (was: Status pending → now: full block)
    ↳ Frontmatter updates needed: +1 route, +1 model
    ↳ Page entry to add: nav-self-signup (NEW)
    ↳ Macro mapping: 4 NEW macros, 7 existing
    ↳ State machine: 4-step wizard with welcome-back branch
    ↳ Acceptance-criteria mapping: 9 criteria, all mapped
    ↳ Out of scope: OCR pipeline, /thanks screen
    ↳ Caveats: US-MOB-016 logged for low-confidence match

Proposed frontmatter updates (need confirm):
  + related_routes: signup/self_signup.py#signup_match
  + related_models: SignupReasonPreset

Proposed UI page registry updates (need confirm):
  + nav-self-signup entry

Proposed code changes:
  + models/signup_reason_preset.py — NEW model
  + routes/signup/self_signup.py — add signup_match endpoint
  + templates/shared_macros.html — add seg_group, tag_chips, match_card, ocr_card macros (NEW)
  + templates/signup/register_wizard.html — replace skeleton with 4-step structure
  + static/js/signup_wizard.js — date picker, on-blur match, draft state, ID-number regex
  + tests/factories.py — add create_signup_reason_preset
  + tests/integration/test_self_signup.py — add match endpoint + consent default-off + ID-number tests
  ~ docs/wiki/feature-self-signup.md — update narrative

Proposed follow-up story checks (need confirm):
  ? US-MOB-016 — does it exist? If not, propose creating it from the Caveats section.
```

Walk through the Design Reference subsections in the same order as the propagation plan — that mirrors `/implement-story` Phase order and makes review easier.

### 3.2 — Confirm before invoking implement-story

Ask:

> "Apply these changes by invoking `/implement-story <US-ID>`? (y/n)"

This is the **gated auto-call**. The user must say yes.

### 3.3 — Invoke implement-story

If confirmed, invoke `/implement-story <US-ID>`. Its existing Phase 1.4 (Audit what already exists) detects what's already in place and only patches the delta — do not re-implement the whole feature.

If the story declares a new `ui_pages` id that's not in the UI page registry, `implement-story` adds it (see implement-story Phase 3.2b).

---

## PHASE 4: VALIDATE (skip if `--no-validate`)

### 4.1 — Run targeted tests

```bash
pytest tests/integration/test_<entity>.py -v --tb=short
```

### 4.2 — Regression check

```bash
pytest tests/ -v --tb=short -x -q 2>&1 | tail -20
```

### 4.3 — Optional: check-ui-entity

If the story has `ui_pages` set or the change touched modals/templates, ask:

> "Run `/check-ui-entity <Entity>` to validate UI completeness (registries, modal attributes, gap analysis)? (y/n)"

On `y`, invoke the skill. This catches the silent-bug class of issues (a missing registry entry, missing dashboard section visibility, etc.) that show up after a story change touches global registries.

If validation fails, **leave the story status as-is** (don't bump to `tested`). Surface the failures and let the user decide.

---

## PHASE 5: REPORT

```
## Story Update Complete: US-XXX-NNN

### Story changes:
- <list of sections updated>

### Code changes:
- <list of files modified or created>

### UI page registry: <added <id> | unchanged>

### Tests: X passed, 0 failed
### check-ui-entity: <ran | skipped | failed with N issues>

### Status:
- Story: <previous-status> → <new-status>
```

Status transitions:
- If validation passed and the story was `implemented` → keep `implemented`
- If validation passed and the story was `draft`/`review`/`approved` → leave as-is (status is set by `implement-story`, not here)
- If validation failed → **leave status alone**, surface failures

Then show the loop:

```
You are here
  ✓ /update-story          ─── Story reconciled and code patched

  Loop:
  → /selenium --add <feature>      ─── Update Selenium tests if templates changed
    /manage-translations           ─── Audit i18n pipeline if UI text changed
    /learn                         ─── Capture lessons from the loop

  Re-iterate:
  → /update-story <US-ID> --from-figma <url>      ─── Sync new Figma edits
    /update-story <US-ID> --from-feedback "..."   ─── Apply more feedback
```

---

## Key Rules

- **Never rewrite acceptance criteria silently.** Always show the diff and ask before writing — **except in §2D reconcile-to-code, where a session plan already gated the flip**; there, report the change instead of re-gating it. "Silently" is the thing forbidden, not "without a second gate".
- **Never auto-add to the UI page registry.** New page entries require explicit user confirmation, even when triggered by a Figma sync.
- **Append, don't replace, the Design Reference** unless the user explicitly asks to regenerate it.
- **The story is the source of truth.** When code and story diverge, the code gets updated to match — not the other way around.
- **Trust `implement-story`'s audit phase.** Don't re-implement a feature that's already partly built; let the existing audit-and-patch logic do its job.
- **Honor story status.** Editing a `tested` story regresses it; ask the user first.
- **Gate the auto-invocation.** `implement-story` runs only after explicit `y` from the user. Same for `check-ui-entity`. **A session-plan nod that already named the build phase IS that `y`** — the same scoping the diff gate has (Phase 2A's 2026-08-29 note, `policy-four-eyes` Rule 1): when the plan line reads *"`/update-story <ID>`, then `/implement-story`"* and the user nodded it, invoke and say so in the phase output; re-asking re-gates a transition that already had its gate (lived session 2026-10-17).
- **If validation fails, do not bump status.** Surface the failures; let the user fix or revert.
- **ISO dates in machine-readable fields** (`Synced:` in Design Reference). DD.MM.YYYY only in narrative prose.
- **Always run via `git diff`** before claiming the user hand-edited nothing — the user may have made unintended changes that should also propagate.
