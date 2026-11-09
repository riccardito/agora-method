---
name: learn
description: Capture a lesson from the current conversation into the skill system. Use after a skill misbehaved, OR after any correction/insight worth preserving even when no skill was invoked. Updates the relevant existing skill, propagates the lesson to other skills it affects, and proposes a new skill when the lesson doesn't fit anywhere.
argument-hint: '[skill-name | "new" | --from-session <file>] [what went wrong or what to improve]'
level: reference
promoted_at: 2026-09-05
role: "the tutor"
epithet: "Theophrastus — the careful classifier"
---

> **Journal-at-source** (policy-skill-progression Rule 6): when you finish a unit of work in a session, append ONE unrated stub to [`experience.md`](experience.md) `## Unrated journal` — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`. One line, lighter than the session Log; `/agora --end` 2.3b grades it.

# Learn — Capture a Lesson into the Skill System

Analyze what went wrong (or could be improved) in this conversation and update the skill system so the same issue doesn't happen again. The lesson may come from a skill that was invoked, OR from ordinary work where no skill was used at all — both are valid.

The goal is not just to patch one file. It is to:

1. Find the lesson in the conversation.
2. Decide where it belongs: an existing skill, several skills, or a brand-new skill.
3. Apply the update(s) surgically.

## Identity

**Theophrastus — the careful classifier.** Theophrastus succeeded Aristotle at the
Lyceum and wrote the *Characters*: thirty types of conduct, each drawn from observed
behaviour and classified so exactly that the description is the diagnosis. `/learn`
works the same way. It takes one lived lesson and asks first **what kind it is** —
`mechanism`, `prose` or `judgment` (US-AGORA-029) — before it asks where it goes; the
classifier's question is deliberately blunt and observational (*could a script, a hook
or an inserted step catch this?*), never "what did we mean". Calibrated 16 / 2 / 4 on
its first twenty-two patches, it has since routed every `mechanism` to `flask agora
capture`: at the phase-⑤ opener's close it turned seven findings into four captures
(#456–#459), one `judgment` line and one prose patch, each with its disposition recorded.

Its second discipline is the **home**. Step 2c's cross-check keeps a patch single-target
— on 2026-09-01 only `/agora` inherits a plan's scope members as its own phases, so the
phase-granularity lesson landed in one file instead of spreading to four — and Step 8's
per-claim contradiction question reads a `hardened`+ target's claims one by one (the
2026-06-20 M2 exclusion was verified against all five of `/level`'s). Its third is
**read the target first**: on 2026-08-31 the shared-resource rule already existed in
`/agora` MODE 4, and the patch became a pointer rather than a second copy.

Why the epithet holds at `reference`: the *Characters* classify by what is seen done,
and a skill that classifies lessons by their checkable shape is what lets the rest of
Agora cite it — `policy-skill-authoring` and `policy-skill-progression` both name it
first among their skills. Round 7's declaration makes it statement 3's routing surface
(*a lesson integrates into the rule it changes; tooling lessons have a runbook* —
US-AGORA-057): the classifier gains the home-discovery its epithet always implied.

---

## When NOT to use

| Need | Use instead |
|------|-------------|
| Author a **cross-cutting rule** that lives in ≥3 places (three or more skills, or skills + `CLAUDE.md`) | `/document --policy <slug>` — inlining a cross-cutting rule into one skill prompt is the exact drift policies exist to prevent (Step 2b decision table) |
| **Promote or regress** a skill, append XP, or read the skills board | `/level <skill>` — `learn` only *detects* a contradiction at Step 8 and *delegates* the regression; it never writes `level:` / `epithet:` / XP itself |
| A **structural audit** of the skill system (frontmatter-vs-behaviour, under-referenced policies, cross-reference health) | `/inspect-pipeline` — `learn` patches a known lesson into a known target; it does not survey `.claude/` for drift |
| **Build a feature** (model, routes, templates, tests) or author its wiki seed | `/implement-story` — `learn` edits skill *prompts*, not product code. **This still holds under the `mechanism` disposition** (Step 2b-mech): a mechanism-class lesson produces a *change request* via `flask agora capture`, never an inline hook or lint rule. `learn` names the check that would have caught the lesson; it does not build it. |
| Store a **one-off fact** about the user, project, or environment (not a repeatable procedure) | Auto-memory — `learn` tells you this and stops (Step 2b decision table) |
| Capture a lesson from a **closed session** rather than the live conversation | Still `learn`, via `/learn --from-session <file>` (Step 1) — same downstream steps |
| A test plan or feedback triage for **one story** | `/iterate` — the loop's manager; `learn` takes the lesson the loop surfaces, never runs the loop (the three-sided grain: iteration → `/iterate`, session → `/agora --end` 2.6, pipeline → `/inspect-pipeline --session`) |

## Step 1 — Identify the lesson

Parse `$ARGUMENTS` and the conversation to determine **what** should be learned. Look for:

- An explicit description in `$ARGUMENTS` (e.g., "it used the wrong python path")
- Errors, corrections ("no", "not that", "wrong", "use X instead"), workarounds
- Missing steps, wrong assumptions, hardcoded values that turned out incorrect
- Successful non-obvious patterns the user confirmed

If the lesson is unclear, ask the user what should be captured.

### `--from-session <file>` — lesson source is an Agora session file

When `$ARGUMENTS` is `--from-session <path>` (the form
[`/agora --end`](../agora/SKILL.md) step 2.5 dispatches), the lesson source is
**not the conversation** — it is a closed session protocol file under
`.claude/sessions/`. Read it and treat:

- the **Agora findings** section — each bullet is an explicit lesson candidate, already triaged by `/agora`
- the **Log** — manual corrections, workarounds, "had to" / "instead" entries
- the **`/inspect-pipeline --session` verdict** recorded in the Close-out — its per-skill cross-check table names the drifting skills directly

as the conversation would be treated in the bullets above. A session file may
carry **several** lessons — process each one through Steps 2–7 in turn, then
report them together. Everything downstream (target identification,
cross-check, surgical edits) is unchanged.

**Self-audit trailer (M2 exemption — `policy-skill-progression` Rule 2).** When a
`--from-session` patch targets a skill that declares `self_audit_loop: true` AND
that skill is the session's *audit subject* (the orchestrator patching itself via
its own `--end` 2.4–2.5 self-audit — i.e. `/agora` patching `/agora`), flag the
patch as **self-audit**: the committer (`/agora --end`'s commit-tree triage) adds a
`Self-audit: <skill>` trailer to that commit. This is what excludes the patch from
the skill's M2, so the orchestrator's own self-improvement loop never blocks its
promotion. An *external* `/learn` (a user correcting the skill from a normal
session) is NOT self-audit and still counts toward M2.

## Step 2 — Identify the target skill(s)

A learning does **not** require a skill to have been invoked. Evaluate in order:

1. **Explicit target** — `$ARGUMENTS` names a skill (e.g., `fixbug`, `deploy`). Use it as the primary target.
2. **Recently invoked skill** — conversation contains a recent `/skill-name` invocation that is related to the lesson. Use it as the primary target.
3. **Topical match** — no skill was invoked, but the lesson clearly fits the domain of an existing skill (e.g., a bug-hunting insight → `fixbug`; a deployment gotcha → `deploy`). List `.claude/skills/` and read each skill's frontmatter `description` to find the best fit.
4. **No fit** — the lesson is valuable but does not belong in any existing skill. Go to Step 2b.

If still ambiguous between two candidates, ask the user which to target.

### Step 2a — Home-discovery: name the ONE section the lesson rewrites (REQUIRED output)

**Before any edit, and before Step 2b decides whether a new home is needed**, run
home-discovery over the WHOLE structure — not over the skill that happened to be
open when the pain was felt:

```bash
python scripts/probes/find_rule_home.py "<the rule's key phrase>"        # top 5 as path#section
python scripts/probes/find_rule_home.py "<phrase>" --grep "<literal>"    # narrow by verbatim text
```

It sections every skill (by heading and by `- **bold**` Notes bullet), every
policy, `CLAUDE.md`, COMPASS / EVENTS / the templates, the tooling runbook, the
declaration, the scripts and the `agora` CLI (by def) and the hooks (by numbered
block), and ranks them by weighted token overlap. Level-history sections and
thread blocks are excluded by construction — a record quotes every lesson it
ever absorbed and would out-score the rule it belongs to.

**The required output is one line, recorded in Step 5's Level-history entry:**

- `home: <path>#<section>` — the ONE section the lesson rewrites (the top hit, or
  a lower one with a reason), **or**
- `home: new — <rule | policy | runbook | mechanism>: <why no existing section is
  the home>` — a new home, with its kind stated.

**Phrase the query as the RULE BEING CHANGED, not as the new case.** A lesson that
adds a case shares only the base tokens with its home, so a query written from the
new words ranks whichever long section mentions them all (lived on the first run,
session 2026-09-05: *"a bug found inside a sweep still routes to fixbug"*
proposed a 470-line orchestrator section; *"bugs route to fixbug by default, a
one-line typo … is the named exception"* returned the routing policy's Rule 1, its
mirror and the two reciprocal rows — the whole target list). A second run with the
rule's own words, or `--grep` on a phrase the rule already carries, is cheaper than a
wrong home.

The proposal is the tool's; the choice is yours (`AGORA-DECL §3`'s judgment line:
*whether a lesson rewrites an existing rule or founds a new one — home-discovery
proposes, a person confirms*). A `home:` naming a `## Notes` bullet is legitimate
only while that bullet IS the rule's home; when the lesson sharpens a rule that
lives elsewhere, the bullet is where the pain was felt, not where the rule lives.

### Step 2b — Consider creating a new skill, a new policy, or auto-memory

Per [policy-documentation](../../../.claude/policies/policy-documentation.md), the lesson belongs in exactly one home — pick by what the lesson is:

| Lesson shape | Home |
|--------------|------|
| Repeatable procedure that doesn't cleanly extend any existing skill | New skill (`/learn` → propose, then create) |
| **Cross-cutting rule that lives in ≥3 places** (three or more skills — the consolidation threshold, policy-documentation Rule 3; e.g. "always do X before rewriting", "never use Y as a discard target") | New policy via `/document --policy <slug>` — **redirect the user, do not write the lesson into a skill prompt** |
| One-off fact about the user, project, or environment | Auto-memory |
| **Harness / tooling lesson** — the interpreter, the encoding, the shell, a heredoc, a gated chain, a completion signal, a measurement tool | The **tooling runbook**, `docs/references/agora/tooling-runbook.md` — one entry (symptom · rule · lived), or a sharper rule on an existing entry plus one citation; the skill's launch line already points there. Neither a skill nor a policy, by design (`AGORA-DECL §3`); a memory file carries at most the one-sentence rule and a pointer at the entry |

For new-skill candidates, all of the following must hold:

- The lesson describes a repeatable procedure (not a one-off fact).
- It doesn't cleanly extend any existing skill.
- It's not cross-cutting (would not be duplicated across multiple skills).
- It's likely to be triggered again by a recognizable user request.

If those hold, propose a new skill to the user **before** creating it: name, one-line description, and trigger condition. Wait for confirmation. On approval, create `.claude/skills/<new-name>/SKILL.md` with proper frontmatter (`name`, `description`, `argument-hint`) and add an entry to `.claude/skills/README.md`.

If the lesson is **cross-cutting** (would live in ≥3 places — three or more skills), it's a policy candidate — redirect the user to `/document --policy <slug>` rather than writing the rule into one skill's prompt. Inlining cross-cutting rules into individual skills is the drift pattern policies exist to prevent.

If none of the above hold, the lesson is likely better stored as auto-memory — tell the user and stop.

### Step 2b-mech — Classify the lesson: mechanism, prose, or judgment (REQUIRED)

**This step has a required output. It is not a question to consider — it is a
disposition to record, and the frontmatter validator fails when it is missing**
(`check_learn_dispositions`, wired into `/agora --start` 1.1, the pre-commit hook,
and the CI lint job).

`/learn` is the system's only routine learning path, and until US-AGORA-029 it could
emit exactly one kind of artifact: **prose**. Step 2b's four exits are all prose or
bookkeeping (`/document --policy`, `/level`, `/inspect-pipeline`, auto-memory), and
this skill's own `## When NOT to use` states the exclusion outright — *"`learn` edits
skill **prompts**, not product code."* So when a lesson's correct fix was a hook, a
lint rule, or an inserted step, the loop structurally could not produce it and wrote
*remember to do X* instead. The corpus records the result in its own words: *"reded
main **AGAIN** … despite the 2026-06-01 note"*, *"the same mistake twice"*, *"**second**
lived spawn instance"*, *"codified after **recurring twice**"*, *"fired **3×** in one
session"*, *"had crossed **four** surfaces"*.

**The routing question, asked once per lesson:**

> **Could a script, a hook, or an inserted step catch this *without judgment*?**

| Answer | Disposition | What `/learn` does |
|---|---|---|
| Yes — the condition is deterministically checkable | **`mechanism`** | Patch the prose *and* call `flask agora capture` to open a change request for the check. `/learn` does **not** build it — this skill stays a surgical-patch skill. |
| No, but the rule is stable and worth stating | **`prose`** | Patch the prose. This is the normal path and is not a failure. |
| No — applying it requires reading the situation | **`judgment`** | Patch the prose. **First-class and non-pejorative** — some lessons genuinely cannot be a check. |

**The disposition names the statement it serves.** The Agora declaration
(`agora-declaration.md` §0)
is the rubric: a `prose` or `mechanism` lesson records the statement it enforces as
`AGORA-DECL §<n>` (a lesson about a copy that drifted is §1; about a write nobody read,
§2; about a lesson appended where it hurt, §3; a banner in the callee, §4; evidence
parsed from prose, §5; a disposition with no home, §6; a batch endured past its tier,
§7); a `judgment` lesson names the statement it stands beside. A lesson that fits no
statement is the declaration's harvest, not this skill's — say so in the disposition
(US-AGORA-054; the declaration's §5.2 binds this step).

**`judgment` is not a lesser answer.** *"A landscape is a map, not an inventory"* or
*"adapting the planned method to an audit finding is not a re-scope"* cannot be a
script; prose is their correct tier. The goal is to stop **defaulting** to prose, not
to eliminate it. A `/learn` run that classifies everything as `mechanism` is as broken
as one that classifies nothing.

**On a `mechanism` disposition**, make the capture call as part of this step:

```bash
flask agora capture "<the check that would have caught this>" --type mechanism --source "<session-id>"
```

It lands on the open self-improvement round Issue so the mechanism is *planned* rather
than *remembered*. Capture never blocks — with `gh` down it spools locally and
`flask agora audit` flags it (US-AGORA-030).

**Recording the disposition is Step 5's job** — it goes in the `## Level history`
entry of the skill's `experience.md` (the sidecar log, US-AGORA-057), in the form
`**disposition: <value>**` plus one clause of reasoning. That entry is what the
validator reads.

> **Calibration (validated against the last 22 real `/learn` patches, 2026-07-08 →
> 2026-07-26).** Retrospective classification: **~16 mechanism · ~2 prose · ~4
> judgment**. The mechanism share is high because that is exactly the gap this exit
> exists to close — several were *literally* a script (an AST-walk for undeclared
> module-level imports; a `git diff --cached --name-only` comparison before commit; a
> recency probe on a DB connection; a regex matching pytest's compact summary), and two
> of them had *already recurred* before being written down again. The distribution also
> shows the test discriminates rather than rubber-stamps: 6 of 22 land outside
> `mechanism`. Full working: `implementation-plan-US-AGORA-029`.

### Step 2c — Cross-check other skills

After identifying the primary target, **always** scan the other skills for cross-applicability. Many lessons (path conventions, environment quirks, test patterns, Windows/bash gotchas) affect multiple skills.

For each other skill, ask: *"If I had invoked this skill in the same situation, would it also have made this mistake?"* If yes, it's a secondary target and should receive a (possibly smaller) patch too.

List every target — primary and secondary — before editing.

**The citation check is the propagation check.** When a patch renumbers, renames or retires something other prose cites — a policy rule, a skill step heading, a `flask agora` command, a path — run `python scripts/checks/check_record_consistency.py --check` (the citation mode, US-AGORA-087; `--census` lists every rule citation with the heading it resolves to): its findings ARE the secondary targets, named with file:line, so the cross-check reads them instead of guessing which skills cite the thing you changed (T-116 renumbered a policy and thirteen lines in five skills kept the old numbers for two months).

## Step 3 — Read the current skill(s)

For every target identified in Step 2, read:

```
.claude/skills/<skill-name>/SKILL.md
```

If a skill has additional files (`experience.md`, a reference table), read those too using:

```
Glob .claude/skills/<skill-name>/**/*
```

Understand the full skill definition before making changes. For secondary targets, a quick read of the frontmatter + relevant section is usually enough.

## Step 3b — Analyze the conversation context

Review the conversation to find **all** of the following (for
`--from-session`, the session file's **Log** + **Agora findings** stand in for
the conversation — scan those for the same six categories):

- **Errors**: Commands that failed, wrong file paths, missing imports, incorrect flags
- **Corrections**: Places where the user said "no", "not that", "wrong", "use X instead"
- **Workarounds**: Things that had to be done differently than the skill prescribed
- **Missing steps**: Steps the skill should have included but didn't
- **Wrong assumptions**: Hardcoded values, paths, or patterns that turned out to be incorrect
- **Successful patterns**: Things that worked well and should be preserved or generalized

## Step 4 — Draft the changes

Determine what kind of update is needed:

| Problem Type | Fix |
|-------------|-----|
| Wrong command/path | Fix the specific command or path in the skill |
| Missing step | Add the step in the right position |
| Wrong assumption | Add a conditional or note about the correct behavior |
| Missing edge case | Add handling for the case |
| Incorrect order | Reorder the steps |
| Outdated info | Update the information |
| Too verbose/slow | Simplify or remove unnecessary steps |
| Missing tool/technique | Add the approach that actually worked |

**Integrate, never append (`AGORA-DECL §3`).** The patch rewrites the rule at the
`home:` Step 2a named — the diff shows that rule's own sentences changed. A lived
instance folds INTO the rule as a one-line citation (`… (lived [[session-id]])`),
never as a paragraph beside it: an instruction and its historical exception must
not look identical on the page. A patch whose only additions fall under
`## Level history` or `## Notes` is an append — the pre-commit gate refuses it
(`scripts/checks/check_learn_patch_shape.py`), and a sentence that merely says *remember
to do X* is the shape the gate exists to stop. When the lesson genuinely founds a
new rule, write it as a rule in the operating text of its home (a new bullet in
the section that owns the topic), not as a `## Notes` entry.

**Rules for changes:**
- Be surgical — only change what needs to change, don't rewrite the whole skill
- Preserve the existing structure and style of the skill
- Add context for **why** the change was made (brief inline comment if helpful)
- Don't remove working parts just because they weren't used this time
- If the fix is environment-specific (e.g., Windows path), make it conditional rather than replacing the general case

## Step 5 — Apply the update(s)

Use the Edit tool to modify each target skill's `SKILL.md`. Make the minimum changes needed per file. If a new skill was approved in Step 2b, use Write to create it.

**Record the disposition in the `## Level history` entry — this is the required
output of Step 2b-mech.** The entry goes to the **sidecar**,
`.claude/skills/<skill>/experience.md ## Level history` (US-AGORA-057 — the
append-only log; newest first; the section exists in every sidecar from the
template, create it above `## Unrated journal` where it does not — and a `draft`
target may have **no sidecar at all**: create `experience.md` from
`.claude/skills/_TEMPLATE_experience.md` with the skill's name filled, lived
session 2026-09-30). SKILL.md carries
operating text only: its own `## Level history`, where one still exists, is legacy
and only shrinks — a patch never writes there, which is what keeps the prose ratchet
green on a lesson. Every `/learn patch` entry carries, alongside its existing
content, the classification and one clause of reasoning:

```markdown
- YYYY-MM-DD — /learn patch (<what changed + driver>) … home: <path#section>
  **disposition: mechanism** — <why: what check would catch this, and where it
  was captured (#NNN)>
```

The validator (`check_learn_dispositions`) reads this and **fails the lint** when a
patch dated on or after 2026-07-26 records nothing. It parses wrapped entries, so the
trailer may sit at the end of a long multi-line block. Historical entries are not
retro-fitted — their disposition was never asked, and back-filling would be invention
rather than a record. The `home:` field is Step 2a's required output (US-AGORA-057):
the section the patch rewrote, or `home: new — <kind>: <why>`; a promotion, a
ceremony or a Step-8 verification line with no operating half writes
`home: record-only`, which is what the pre-commit patch-shape gate reads.

After editing, show the user:
1. **Targets** — every skill touched (primary + secondary + new)
2. **Home** — the `path#section` the patch rewrote (Step 2a), or the new home and its kind
3. **What was changed** — a brief summary of each modification
4. **Why** — what problem in the conversation this fixes
5. **Disposition** — `mechanism` / `prose` / `judgment` + the reasoning, and for
   `mechanism`, the Issue the change request landed on
6. **Before/after** — for non-trivial changes, show the key diff

## Step 6 — Verify

For each updated or created skill file, confirm:
- YAML frontmatter is valid (`name`, `description`, `argument-hint` present)
- Markdown structure is intact, no broken formatting
- The fix actually addresses the problem from the conversation
- **The `## Level history` entry records its `disposition:`** (Step 2b-mech). The lint
  below enforces this; a failure here means the classification step was skipped, not
  that the wording is wrong.

If a skill's `description` in frontmatter should be updated to reflect new capabilities or changed scope, update it.

**Always run the frontmatter lint after editing or creating a SKILL.md:**

```
python scripts/checks/validate_skill_frontmatter.py --check
```

If it fails, the YAML is broken for the VS Code Claude Code extension's strict
parser — the harness will still load it, but the IDE picker will crash with
`Unhandled case: [object Object]` and block the user from seeing assistant
responses. Apply the quoting rule below and re-run; use `--fix` for
auto-quoting if the change is mechanical.

**And run the patch-shape gate on the working tree before reporting** — the same
check the pre-commit hook runs on the staged diff (US-AGORA-057, `AGORA-DECL §3`):

```
python scripts/checks/check_learn_patch_shape.py --working
```

A `[FAIL] … append-only` here means Step 4 did not rewrite the rule at the named
home — fix the patch, never the gate. A promotion, a ceremony or a Step-8
verification line with no operating half declares `home: record-only` in its
Level-history line; that is the one exemption, and it is visible.

### SKILL.md frontmatter quoting rule

The full rule lives in [`policy-skill-authoring`](../../policies/policy-skill-authoring.md) Rule 2 — apply it; don't restate it here. **Summary:** every prose frontmatter scalar (`description:`, `argument-hint:`, `name:`, `title:`, `role:`, `epithet:`) must be double-quoted when it contains `: `, whitespace-`#`, a leading `[`/`{`, a mid-string `|`/`>`, a `<`/`>`, or a leading reserved indicator (`& * ! ' " % @` backtick). Unquoted, the VS Code extension's strict YAML parser crashes with `Unhandled case: [object Object]` and blocks the user from seeing assistant responses.

When `/learn` writes or edits SKILL.md frontmatter — directly or via a new-skill proposal in Step 2b — apply this rule **reflexively**, at the moment of authorship. Don't wait for the lint to flag it. The defence-in-depth layers (`/agora --start` pre-flight, `pre-commit` hook, CI `lint` job) catch regressions; `/learn` is the layer that *prevents* them. If a patch lands on a `hardened`+ skill, the same policy's Rule 4 (body sections gate by level) governs whether the `## Claims at this level` section is still satisfied.

## Step 7 — Update README if needed

If any change affects a skill's usage, arguments, or description visible in the quick reference, update `.claude/skills/README.md` to match. A new skill always needs a README entry.

Only update the README if:
- A new skill was created
- A new argument/flag was added
- A skill description changed meaningfully
- Usage examples need updating

## Step 8 — Claims-aware contradiction check (hardened+ targets only)

Per [`policy-skill-progression`](../../../.claude/policies/policy-skill-progression.md)
Rule 4 + Rule 8 — for any patched target whose current `level:` is
`hardened` or `reference`, the contradiction question is **per-claim and
specific**, not abstract.

After Step 5 (the patch lands), for each `hardened`+ target:

1. **Read the target's `## Claims at this level` section.** If the
   section doesn't exist on a `hardened`+ skill, that itself is a quest
   violation — surface as a `/level <skill>` audit finding and skip the
   contradiction question for this round (the policy can't enforce
   without the section).
2. **For each of the 3–5 named claims**, run the contradiction question —
   **in PROSE by default** (per the gate-shape rule, `policy-four-eyes`
   Rule 2 / agora `## Gate shape`): when the patch was pre-confirmed by the
   user or plainly strengthens/leaves a claim untouched, state the per-claim
   verdict in prose and let the user object (lived precedent: the 06-08 and
   06-12 agora self-audit patches, both verified in prose). Reserve the
   `AskUserQuestion` walk for when a contradiction is **genuinely ambiguous**:

   > "**Claim N:** *'<verbatim claim text>'*
   >  Does the patch you just applied (commit `<sha>` — or staged for
   >  commit) contradict this claim?"
   > Options: *No (still holds) / Yes (contradicts) / Unsure (defer)*.

   Walk the claims one at a time; don't batch. A "yes" on any one is
   sufficient to trigger regression — no need to continue down the list.

3. **On a single "yes" answer:**
   - Capture the patch's commit sha (for already-committed patches) or
     stage the patch first and capture the new sha.
   - Call `/level <skill> --regress --corrects <sha>` to apply the
     regression per policy-skill-progression Rule 3.
   - The regression's `## Level history` entry cites *which claim* was
     contradicted, by index + text.

4. **On all "no" answers:** the level claim still holds. Append one line
   to the sidecar's `## Level history` (`experience.md`, under the current
   level's most recent entry — never SKILL.md's legacy section):

   ```markdown
   - YYYY-MM-DD — /learn patch (<sha>) verified non-contradicting against all <N> claims at <level> · home: record-only
   ```

   This is the audit trail of the verification — without it the user
   has no way to see *that the check happened* on routine patches. The line has
   no operating half, so it declares `home: record-only` — the patch-shape gate's
   one exemption (Step 6).

5. **On any "unsure" answer:** park the regression decision; surface as
   a finding in the next `/agora --start` step 1.1 skill-system state
   (the deferred review). Don't auto-regress on uncertainty.

For `used`-tier targets, **skip Step 8** — the contradiction-question
gate only kicks in at `hardened`+ where named claims exist. A `used`
skill's `/learn` patch is part of its normal growth toward `hardened`.

For `draft`-tier targets, also skip — no level claim to contradict.

---

## Examples

### Example 1: Wrong Python path (skill was invoked)
```
User: /learn manage-translations it used the wrong python path
```
-> Primary target: `manage-translations`. Cross-check: does `deploy` or `check-coverage` also hardcode that path? If yes, patch them too.

### Example 2: Missing step (implicit, skill was invoked)
```
User: /learn
```
-> Conversation shows `/deploy` failed because it didn't check MongoDB first. Patch `deploy`. Cross-check: do other skills assume Mongo is running? If `fixbug` or `check-coverage` would also fail in that state, add a note there too.

### Example 3: Explicit improvement
```
User: /learn fixbug should also check the browser console for JS errors
```
-> Patch `fixbug`. Cross-check: `add-selenium-test` and `implement-story` also touch the frontend — does the same lesson apply?

### Example 4: Lesson without any skill invocation
```
User: /learn we just spent an hour chasing a bug that turned out to be a stale Jinja cache — always hard-refresh after editing templates
```
-> No skill was invoked. Topical match → `fixbug` (debugging workflow). Also relevant to `deploy` (post-deploy verification) and `implement-story` (testing step). Patch all three with a short note.

### Example 5: Lesson that needs a new skill
```
User: /learn every time I add a new MongoDB migration I forget to update migrate-status and to add a rollback — we should have a standard procedure for this
```
-> No existing skill covers migration authoring. Repeatable procedure, clear trigger. Propose a new `new-migration` skill to the user. On approval, create `.claude/skills/new-migration/SKILL.md` and add an entry to `README.md`.

### Example 6: Lesson that should go to memory, not a skill
```
User: /learn Dr. Huwyler prefers p-values reported to 3 decimal places
```
-> Not a repeatable procedure, just a fact. Tell the user this belongs in auto-memory, not in a skill. Do not modify any skill file.

### Example 7: Lesson sourced from a closed Agora session
```
User: /learn --from-session .claude/sessions/2026-05-14-hub-rollout.md
```
-> Read the session file (not the conversation). Its "Agora findings" lists two items: (1) `/check-page --finish` left the structure doc stale on two pages; (2) the commit triage kept re-explaining the conventional-commit format. Item 1 → patch `/check-page`. Item 2 → cross-cutting and already covered by `policy-commit-discipline` — surface that the policy exists rather than patching a skill. Process both through Steps 2–7, report together. This is the form `/agora --end` dispatches.

---

## Initialisation

**What this skill reads before acting** (US-AGORA-041): the lesson's full
context — the target SKILL.md whole (its `## Claims at this level` section,
boundary table and Level history), the session record the lesson comes from,
and the sibling skills the cross-check might route a secondary patch to. A
patch written without the claims read is a contradiction-check skipped.

**Self-model:** the surgeon — corrections land as minimal, surgical patches
to the right skill at the right tier (mechanism | prose | judgment), never
as rewrites. A noticed context gap (a claim it did not know existed, a
sibling it failed to cross-check) lands as a 🟡 journal stub in
[`experience.md`](experience.md).

## Claims at this level

The invariants other skills and the user depend on `/learn` to hold (the
`hardened`-tier commitments; each is the unit `/learn` checks for contradiction
per `policy-skill-progression` Rule 4 — including against itself).

1. **Every patch is surgical.** `learn` edits the smallest SKILL.md surface that fixes the lesson and never rewrites a skill or removes working parts it didn't touch (Step 4 + Step 5).
2. **A lesson lands in exactly one home, chosen by its shape.** A repeatable procedure with no fit becomes a new skill, a rule spanning ≥3 places is redirected to `/document --policy` rather than inlined, and a one-off fact goes to auto-memory (Step 2b decision table).
2b. **Every patch carries a recorded disposition — `mechanism` / `prose` / `judgment`.** The routing question (*could a script, a hook, or an inserted step catch this without judgment?*) is asked once per lesson and its answer is written into the target's `## Level history` entry, where `check_learn_dispositions` verifies it; a `mechanism` answer opens a change request via `flask agora capture` rather than appending another rule, and `judgment` is a first-class outcome, not a fallback (Step 2b-mech + Step 5).
3. **Every primary target is cross-checked against the other skills before any edit.** Each candidate is asked "if I had invoked this skill in the same situation, would it also have made this mistake?" and the full target list is named before editing (Step 2c).
4. **A patch to a `hardened`+ target runs the per-claim contradiction check before it is done.** Each named claim in the target's `## Claims at this level` is tested individually; a single "yes" delegates to `/level <skill> --regress --corrects <sha>`, an all-"no" pass writes one verification line to the target's `## Level history` (Step 8).
5. **Frontmatter quoting is applied reflexively at authorship, then lint-verified.** Any SKILL.md `learn` writes has its prose scalars quoted per `policy-skill-authoring` Rule 2 at the moment of writing, and `validate_skill_frontmatter.py --check` is run before the patch is reported (Step 6).
6. **Every patch integrates into the rule it changes, at a home found over the whole structure — an append is refused.** Step 2a runs `scripts/probes/find_rule_home.py` and records `home: <path#section>` (or `home: new — <kind>`); Step 4 rewrites that section and folds the lived instance in as a citation; the pre-commit gate (`scripts/checks/check_learn_patch_shape.py`) refuses a SKILL.md diff whose only additions sit under `## Level history` / `## Notes`, the one exemption being a declared `home: record-only` (`AGORA-DECL §3`).
