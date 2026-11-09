---
name: document
description: "Author or update a policy or an ad-hoc explainer document. Use for cross-cutting rules of engagement that span multiple skills (policy mode), or for one-off explainers / ADRs / stakeholder one-pagers that don't fit a feature story (explainer mode). NOT for documenting features (use `/implement-story` — it auto-generates the wiki seed) and NOT for skill-level corrections (use `/learn`). --update refines a policy or flips draft → active; --deprecate retires one (status, the CLAUDE.md mirror, the skill cross-references)."
argument-hint: "<slug-or-topic> [--policy | --explainer | --update | --deprecate]"
level: used
promoted_at: 2026-05-19
role: "the scribe"
---

> **Journal-at-source** (policy-skill-progression Rule 6): when you finish a unit of work in a session, append ONE unrated stub to [`experience.md`](experience.md) `## Unrated journal` — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`. One line, lighter than the session Log; `/agora --end` 2.3b grades it.

# Document — Author Cross-Cutting Rules and Ad-Hoc Docs

`$ARGUMENTS` names what to author (a kebab-case slug or a free-text
topic). The skill produces durable documentation that doesn't fit any
other authoring workflow.

| Mode | Output | When |
|------|--------|------|
| `--policy <slug>` | `.claude/policies/policy-<slug>.md` + CLAUDE.md mirror + skill cross-references | Cross-cutting rule that must be respected by multiple skills (e.g. documentation discipline, migration discipline, i18n rules) |
| `--explainer <slug>` | `docs/references/<area>/<slug>.md` | One-off explainer, architecture decision record, stakeholder one-pager — durable but not policy-grade |
| `--update <slug>` | Edit an existing policy or explainer | Refining a written rule; bumping `status: draft → active` |
| `--deprecate <slug>` | Flip an existing policy to `status: deprecated` and remove from CLAUDE.md mirror | Superseded by a stronger enforcement layer or another policy |

**When NOT to use this skill:**

| Need | Use instead |
|------|-------------|
| Document a feature you just built | `/implement-story` Phase 3.8 already creates the wiki seed |
| Capture a skill-level correction | [`/learn`](../learn/SKILL.md) — patches the relevant skill surgically |
| Write the implementation plan for a story | `/implement-story` Phase 2b — automatic |
| Update a CLAUDE.md prose section | Direct edit (no skill needed) |
| Author prose to a voice / language / style — a paper, chapter, letter, one-pager | [`/write`](../write/SKILL.md) — this skill owns *placement*, that one owns *prose*. Mode 2 (`--explainer`) **delegates** to it for any substantial body (see 2.1) |

If the request fits one of the above, redirect the user there and stop.

**Confirmation step (all modes):** Before writing anything, summarise to
the user `Authoring: <mode> "<slug>" → Output: <path>`. If the slug came
from free-text, propose a kebab-case slug and confirm. If the request
genuinely fits a different skill, surface the redirect and stop.

**`--policy <slug>` is Mode 1 only when the slug does NOT exist** — the dispatch's
FIRST command, `test -f .claude/policies/policy-<slug>.md && echo "Mode 3" || echo "Mode 1"`,
its output named in the confirmation line (US-AGORA-109); present means Mode 3, whatever
flag was typed. Mode 1 copies `_TEMPLATE.md` over a live file, dropping every
rule the caller never mentioned, and the mirror propagates the loss — and the
wrong dispatch is the natural one (lived session 2026-09-09).

---

## MODE 1 — `--policy <slug>` (primary mode)

Authors a new cross-cutting policy file, mirrors its TL;DR into
CLAUDE.md, and adds cross-references in every related skill's SKILL.md.

### 1.1 — Read the template

```
.claude/policies/_TEMPLATE.md
```

Copy to `.claude/policies/policy-<slug>.md`.

### 1.2 — Fill in the frontmatter

| Field | What to write |
|-------|---------------|
| `name` | `<slug>` (kebab-case, no `policy-` prefix) |
| `title` | Human title — match the `# <Title> policy` heading |
| `status` | `draft` while the policy is being written; flip to `active` only after the CLAUDE.md mirror and all skill cross-references are in place |
| `related_skills` | Slugs of every skill that enforces or reads this policy (`implement-story`, `update-story`, `feature-plan`, `fixbug`, `learn`, …) |
| `related_lint_rules` | Lint rule ids that overlap this policy. Empty if the policy is procedural-only. |

Apply [`policy-skill-authoring`](../../policies/policy-skill-authoring.md) Rule 2 to these scalars — double-quote any `title:` / `name:` value containing `: `, `#`, leading `[`, `<`/`>`, etc., or the VS Code strict YAML parser crashes on the policy file.

### 1.3 — Write the body

Mandatory sections (per `_TEMPLATE.md`):

1. **TL;DR** — 3–5 numbered, copy-able rules. One sentence each. This block is mirrored verbatim into CLAUDE.md, so it has to be self-contained — no cross-references that depend on the surrounding policy text.
2. **Why this exists** — one paragraph on what goes wrong without this policy. Concrete past incidents > abstract concerns.
3. **The rules** — each rule gets a `### N. Heading` with **What / Why / Where enforced / Example**.
4. **See also** — cross-references back to skills, related policies, and lint rules.

Optional sections: **Common mistakes** (drift patterns we've seen), **Examples** (good vs bad), more detailed enforcement notes.

### 1.4 — Mirror the TL;DR into CLAUDE.md

In `CLAUDE.md` under `## Policies`, **append** a block:

```markdown
### policy-<slug> — <Title> &nbsp;<sup>(full text)</sup>

1. <rule 1>
2. <rule 2>
3. <rule 3>
```

The TL;DR text is verbatim from the policy file — no rewording. If a
"No active policies yet" placeholder is present, replace it with the
first policy block.

### 1.5 — Cross-reference from related skills

For each skill in `related_skills:`, edit its SKILL.md to add a short
reference at the point in the workflow where the policy applies:

> Apply policy-<slug> — &lt;one-line reminder of the rule&gt;.

Don't paraphrase the policy here; the skill just notes "this policy
applies, go read it" with a short reminder. The full rule lives in the
policy file.

### 1.6 — Update the policies index

In `.claude/policies/README.md`, under
**Active policies**, add:

```markdown
- `policy-<slug>` — <one-sentence description>
```

If the placeholder "_None yet_" is still there, replace it.

### 1.7 — Validate

Run the catalogue lint (sanity check — no policy-specific rule yet,
but if the policy referenced lint rule ids in `related_lint_rules`,
those must resolve):

```bash
python app/requirements_lint.py --check
```

Then flip the policy's `status:` field from `draft` to `active`.

### 1.8 — Report

Show the user:

- Policy file created
- CLAUDE.md mirror block added
- Skills cross-referenced (list)
- README index updated
- Status: active

---

## MODE 2 — `--explainer <slug>`

Lighter-weight than a policy — for one-off explainers, ADRs,
stakeholder one-pagers. Output goes under `docs/references/` (the area
folder is up to the topic — `docs/references/strategy/`,
`docs/references/operations/`, `docs/references/research/` for
research papers, etc.).

No CLAUDE.md mirror. No skill cross-references. No status enum to
manage. Just a focused markdown file:

```markdown
# <Title>

**Audience:** <stakeholders / engineers / future-me>
**Status:** <draft | published>
**Last reviewed:** <YYYY-MM-DD>

## Why this exists

<one paragraph>

## The content

<the actual explainer>

## See also

<links>
```

Skip the policy ceremony entirely — explainers are durable but
informal. If the explainer is being read by 3+ skills or starts to
look like a rule rather than a description, escalate it to a policy
via Mode 1.

### 2.1 — Delegate the prose to [`/write`](../write/SKILL.md)

**This mode owns *placement*; it does not own *prose*.** `/document`
decides the path, the frontmatter header, the section skeleton, the
index entry and the cross-references — it carries nothing on audience,
voice, tone, length, density or style, and an explainer of any
substance needs all six.

So for anything longer than a page, **call `/write` for the body**:

| Step | Owner |
|------|-------|
| Path under `docs/references/<area>/`, the header block, `## See also` links | `/document` (this mode) |
| Audience · purpose · form · structure · length · **density** · voice · tone · language | [`/write --brief`](../write/SKILL.md) |
| The prose itself, in the profiled voice and target language | `/write` |
| The **style pass** — burstiness, markdown-leakage, voice match, language-native | `/write` |

Pass `/write` the **corpus** to match. For a strategy explainer that is
usually `docs/references/research/RP-*.md` or the sibling files in the
same area folder; for book work it is `docs/book/`.

**Short and purely factual explainers do not need the delegation** —
a half-page ADR stating a decision and its rationale is fine written
directly here. The trigger is *length plus a reader who is not you*:
once an explainer has an audience, it has a voice, and voice is
`/write`'s.

Skipping the delegation on a substantial explainer is how a
`docs/references/` file ends up in a register that matches nothing else
in the folder.

---

## MODE 3 — `--update <slug>`

Edit an existing policy or explainer.

### 3.1 — Read the existing file

Identify what's changing — TL;DR rule wording? Adding a new rule? New
example? New related skill?

### 3.2 — Apply the edits

Make the surgical changes. Preserve the structure (frontmatter +
mandatory sections).

### 3.3 — Sync the CLAUDE.md mirror (policies only)

If the TL;DR changed, **also** update the CLAUDE.md mirror to match.
The two MUST stay verbatim-equal — that's the framework's "single
source of truth" rule. A drifted mirror is the most common silent
failure: the policy gets edited, the mirror doesn't, and the
always-loaded version (CLAUDE.md) no longer matches the on-disk file.

### 3.4 — Sync skill cross-references

If new related skills were added, walk each one's SKILL.md and add the
cross-reference. If a rule was removed, search for any orphan skill
cross-references that pointed at the removed rule and clean them up.

### 3.5 — Report

Show the diff (the policy file changes + the CLAUDE.md mirror change +
the skill cross-references touched). User reviews.

---

## MODE 4 — `--deprecate <slug>`

When a policy is superseded by a stronger enforcement layer (a lint
rule, a hook, a different policy):

### 4.1 — Mark the policy deprecated

Set `status: deprecated` in the policy file's frontmatter.

Add a `## Deprecated` section at the top of the policy explaining what
superseded it. Link to the new policy or the lint rule that absorbed
the rule.

### 4.2 — Remove the CLAUDE.md mirror

Strip the TL;DR block from CLAUDE.md `## Policies`. Deprecated
policies are NOT mirrored — they're kept in the folder for historical
reference but no longer always-loaded.

### 4.3 — Update the policies index

Move the entry in `.claude/policies/README.md` from **Active policies**
to a new "Deprecated" sub-section (or remove it; deprecated policies
stay in the folder but aren't actively referenced).

### 4.4 — Clean skill cross-references

Walk every skill in `related_skills:` — remove the cross-reference
OR repoint it to the new policy / lint rule that superseded this one.

### 4.5 — Report

Confirm the deprecation: file marked, mirror removed, index updated,
N skill references cleaned.

---

## VERIFY (after any mode)

- [ ] Policy / explainer file is at the expected path
- [ ] If `--policy`: CLAUDE.md mirror present and verbatim-equal to the file's TL;DR
- [ ] If `--policy`: every `related_skills:` entry has a cross-reference in its SKILL.md
- [ ] `.claude/policies/README.md` index reflects current state
- [ ] `python app/requirements_lint.py --check` passes
- [ ] No accidental edits to unrelated files (`git status` is clean except for the intended changes)

---

## Mode dispatch

Parse `$ARGUMENTS`:

| User says | Mode |
|-----------|------|
| `--policy <slug>` (or "policy" + slug) | **Mode 1** if the slug is new · **Mode 3** if `policy-<slug>.md` already exists — test the path |
| `--explainer <slug>` (or "explainer" + slug) | Mode 2 |
| `--update <slug>` (or "update" + slug) | Mode 3 |
| `--deprecate <slug>` (or "deprecate" + slug) | Mode 4 |
| `<slug-or-topic>` with no flag | Ask which mode the user wants — default to Mode 1 (policy) for free-text topics that look like rules |

---

## Key rules

- **Don't paraphrase the TL;DR in CLAUDE.md.** It's a verbatim mirror.
  If the rules need different wording for the index vs the file, the
  rules aren't sharp enough — refine them in the file first, then
  mirror.
- **Don't author features or skill corrections here.** Both redirects are
  rows in the `## When NOT to use` table above — that is the boundary.
- **Don't create a policy for a one-time rule.** Policies are for
  rules that span multiple skills or that change AI behaviour broadly.
  A single skill's internal rule belongs in that skill's SKILL.md.
- **Status: active is a commitment.** A policy in `active` state means
  CLAUDE.md is mirrored AND skills are cross-referenced. Don't flip
  the field until both are done.

---
