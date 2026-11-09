---
name: level
description: "Skill leveling system — audit one skill against its current level's criteria, propose promotion (with naming ceremony at used→hardened) or regression, append XP entries with knowledge snippets, manage the skills board. Implements policy-skill-progression."
argument-hint: "[--board (default) | --board --policies | <skill-name> | <skill-name> --promote | <skill-name> --regress --corrects <sha> | <skill-name> --xp +<N> \"<snippet>\"]"
model: opus
level: reference
promoted_at: 2026-10-31
role: "the assessor"
epithet: "Solon — the lawgiver who ranks the citizens"
---

> **Journal-at-source** (policy-skill-progression Rule 6): when you finish a unit of work in a session, append ONE unrated stub to [`experience.md`](experience.md) `## Unrated journal` — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`. One line, lighter than the session Log; `/agora --end` 2.3b grades it.

# `/level` — Skill leveling meta-skill

> **Authored:** 2026-05-17 (Section session 2026-05-17 Phase C). Implements [`policy-skill-progression`](../../policies/policy-skill-progression.md). Thresholds calibrated from spawn `2026-05-17-skill-progression-research`. Promotes to `used` after one successful closed-Section invocation.

Operates [`policy-skill-progression`](../../policies/policy-skill-progression.md).
The policy defines the levels, the criteria, the metrics, and the audit
trail. This skill is the operational interface: it *computes* metrics, it
*reports* fit, it *applies* level changes — with the audit trail policy-skill-progression Rule 4 requires.

This skill is **read-mostly**. Mode 1 (`--board`) and Mode 2 (`<skill>` audit)
are pure-read. Only Modes 3 and 4 (`--promote` / `--regress`) write — and only
to one SKILL.md frontmatter + one `IMPROVEMENTS.md` entry.

## Identity

**Solon — the lawgiver who ranks the citizens.** Solon wrote the Athenians their laws and
then left the city for ten years, so that no one could ask him to bend them. `/level` is
that lawgiver: it ranks every citizen of the corpus and has never once promoted or demoted
one on its own authority — the metrics gate, the human confirms (Claim 1). At its own
`hardened` promotion on 2026-06-20 it carried M2 = 0 and, the same day, verified the one
`/learn` patch that touched it against all five of its claims before letting it land. At
round 7's Stage 7 (session 2026-09-05) the board it computed with
promotion-marker cutoffs overruled the assumption of the person computing it: `feature-plan`,
expected at the `reference` gate, failed it on M1 24 < 30, and `learn` passed — the ranking
corrected the ranker. On 2026-08-16 it gave the XP rollup to the writer, and
`xp_total == sum(xp_by_level)` has held at every `--start` since, after 716 XP had drifted
across eleven skills by hand. At round 8's Stage 7 (session 2026-10-31)
it found that its own M2 had become a touch count under the PR-squash flow and read the
sidecars instead, then named the finding against itself. The lawgiver's virtue is not that the
law is clever; it is that the one who wrote it is bound by it too.

## When NOT to use this skill

| Need | Use instead |
|------|-------------|
| Patch a misbehaving skill | [`/learn`](../learn/SKILL.md) (level-aware — reads `level:` before patching) |
| Audit the full skill system structurally | [`/inspect-pipeline`](../inspect-pipeline/SKILL.md) `--audit` |
| Audit a skill through one lived session | [`/inspect-pipeline`](../inspect-pipeline/SKILL.md) `--session <file>` |
| Author a new policy | [`/document`](../document/SKILL.md) `--policy` |
| Decide whether to spawn a sub-conversation | [`/agora`](../agora/SKILL.md) MODE 4 |

The boundary with `/inspect-pipeline --audit`: `/inspect-pipeline` audits the
**static structure** of the skill system (categories, cross-references,
description-vs-body coherence). `/level` audits **dynamic progression** —
how a skill's lived experience compares to its declared level.

---

## MODE 1 — `--board` (default)

The **skills-board view**. Read every `.claude/skills/*/SKILL.md` frontmatter
+ compute the six metrics from policy-skill-progression Rule 2. Output a
single ranked table.

### 1.1 — Run the command

`flask agora board [--json] [--sort level|xp|m1|m2|staleness]` — **a command's output, computed
from the files** (US-AGORA-078, `app/commands/agora_board.py`): every SKILL.md frontmatter
(`level`, `promoted_at`, `role` (used+), `epithet` (hardened+); a missing `level:` reads `draft`),
every `experience.md` (`xp_total`, `## Level history`, the graded entries), the closed sessions'
`skills_invoked:`, the policies' `related_skills:`, git for M6 only. The hand computation is retired.

> The required *shape* of these fields/sections at each level — and the lint that enforces it — is [`policy-skill-authoring`](../../policies/policy-skill-authoring.md) (the artifact); this skill enacts the *transitions* per [`policy-skill-progression`](../../policies/policy-skill-progression.md). When `--promote` writes `role:` / `epithet:`, apply `policy-skill-authoring` Rule 2's quoting (always double-quote those prose scalars).

### 1.2 — The six metrics the command computes

Per policy-skill-progression Rule 2. **The reference point for M1 / M2 / M3 is the frontmatter's
`promoted_at:`** (claim 4) — the `level(skill): promote …` subject grep missed batch and squashed
markers (landscape v6 §a); a `used`+ skill without `promoted_at:` is flagged `[?]`, measured all-time.

1. **M1 Invocation count** — closed sessions whose `skills_invoked:` names the skill, all-time AND since `promoted_at` (by the session's `date`).
2. **M2 Correction load (raw)** — `/learn patch` entries in the sidecar's `## Level history` dated on/after `promoted_at`, minus entries marked `M2-exempt` / `Self-audit` (the **self-audit exemption**, `policy-skill-progression` Rule 2 — `agora` declares `self_audit_loop: true`; `/learn` writes the mark). The **cross-reference exclusion** (a patch that only adds a link to this skill) stays the auditor's read over the entries the command lists: M2 is *correction* load, not *touch* count, and no mechanical marker says "this commit only links me".
3. **M3 Redo rate** — the fraction of invoking closed sessions whose Log carries `^### … /<skill>` headings 2+ times.
4. **M4 Reference depth** — SKILL.md lines + `## ` / `### ` headings (soft signal).
5. **M5 Cross-reference fan-in** — other SKILL.md bodies naming `/<skill>` + policies listing the skill in `related_skills:` (shown as `N+Pp`; the policy count is the `reference` gate's own check).
6. **M6 Last-update recency** — `git log -1 -- SKILL.md`, days ago.

**Codification rate is NOT computed.** Per policy-skill-progression Rule 2: parsing prose `Agora findings` blocks is too fragile at corpus scale.

### 1.3 — The candidate column

For each skill not at `reference` the command evaluates the next gate all-of (metrics AND the quest
artefacts — `## When NOT to use`, `## Claims at this level` ≥ 3, `epithet:`, a policy's `related_skills:`
entry, `## Identity`): `->used` / `->hard` / `->ref` when every check holds, else `N short`. **Candidate
is a computed view, NOT a stored level** — the promotion is MODE 3 behind the user's nod.

### 1.4 — Output the board

<!-- rc:sample-board -->
```
$ /level --board
Skills board — 21 skills (identity columns from the skills' frontmatter;
M1 · M2 · M5 · XP · Cand. are the live columns of `flask agora board`)

Skill              Level     Identity
──────────────────────────────────────────────────────────
agora              hardened  Socrates — the dialectician
check-coverage     used      "the coverage doctor"
check-page         used      "the architect"
check-ui-entity    used      "the magistrate"
deploy             used      "the quartermaster"
design             used      "the Themelion conductor — red-flag code-design review, Arc phase-③ cleanup conducting, post-cleanup QC"
document           used      "the scribe"
feature-plan       hardened  Euclid — the surveyor who lays out the grid
fixbug             used      "the janitor"
implement-story    reference Hero of Alexandria — the master builder
inspect-pipeline   hardened  Diogenes — the iconoclast with the lamp
iterate            used      "the steward"
learn              reference Theophrastus — the careful classifier
level              reference Solon — the lawgiver who ranks the citizens
manage-translations used      "the curator"
new-story          used      "the playwright"
plaza              used      "the reformer"
selenium           used      "the pilot"
update-story       used      "the mediator"
wiki               used      "the chronicler"
write              used      "the artefact author — gather · brief · produce · measured style pass"
```
<!-- /rc:sample-board -->

Three identity columns ladder by level:
- `draft` skills: no identity
- `used` skills: `role:` shown in quotes — *"the inspector"*
- `hardened`+ skills: `epithet:` shown without quotes — `Aristotle — the categoriser`

`XP` column = `xp_total` from each skill's `experience.md` (zero if no file).
`Cand.` column = next-level candidacy. `→hard (?)` means "candidate for
hardened, audit recommended"; `(?)` is removed once the user runs the audit.

Mastery markers shown for `reference`-tier skills (parenthetical citation
count + which skills cite them by epithet) — per policy-skill-progression
Rule 7 step iii — make doctrine value visible without further promotion.

Sort modes (named — user picks at invocation):
- `--by-level` (default) — level desc, then M5 fan-in desc within tier
- `--by-corr` — M2 desc (which skills are unstable?)
- `--by-inv` — M1 desc (which skills get the most use?)
- `--by-xp` — `xp_total` desc (which skills have the deepest journey?)
- `--by-staleness` — M6 asc (which skills haven't moved?)

The board is Agora's **character sheet** — without it the leveling system is
invisible and dies (game-design lesson from the spawn). The user reads it,
picks a target, runs Mode 2 on that target.

### 1.6 — `--board --policies` (the policy scorecard, US-AGORA-011)

Policies are **not skills** — they're cited and enforced, not invoked, so they
have no level / M1 / XP / ceremony (the *measure-don't-level* decision, WS2).
`--board --policies` is their parallel surface: a ranked **scorecard**, computed
deterministically by `scripts/generators/policy_scorecard.py`
(Flask-free, the `check_stats` family). Run it and render the table:

```
python scripts/generators/policy_scorecard.py          # ranked table
python scripts/generators/policy_scorecard.py --json    # machine-readable
```

Per-policy signals:
- **citations** — references to `policy-<slug>` across `.claude/skills/**/SKILL.md`
  + `CLAUDE.md` + sibling policies (≈ skill M5; the policy's own file excluded).
- **breaches** — lines in [`.claude/sessions/policy-breaches.md`](../../sessions/policy-breaches.md)
  for the slug (confirmed violations captured in `/agora --end`'s close-out
  paper, 2.10 — step 2.7 was retired by US-AGORA-034).
- **last-breach recency** — days since the most recent breach.
- **`needs-rewording`** — the derived flag. **Breach-driven only — citations NEVER
  trigger it** (the Goodhart guard: citing a policy more without following it more
  must not read as compliance). Fires at ≥2 breaches ever, or 1 breach within 30 days.

The most-breached policies are the **rewording queue**: a policy people keep
breaking is badly worded or badly placed, not a policy people are bad at. A
`needs-rewording` policy routes to [`/document --policy <slug>`](../document/SKILL.md)
for a rewrite. (Closes Goal #91 Phase 2 / #92 — policies get a first-class
observable surface without a level enum.) An optional `wiki/stats` Plotly panel
reusing Goal #91's policy-density/domain charts is a noted follow-on.

---

## MODE 2 — `/level <skill>`

Audit one skill against its current level's criteria. Read-only.

### 2.1 — Read the target

Read `.claude/skills/<skill>/SKILL.md` frontmatter. If the skill doesn't
exist, error out: "no skill named `<skill>` — see `/level --board` for the
inventory".

### 2.2 — Compute the skill's metrics

`flask agora board --skill <name>` — the same six metrics as Mode 1.2, scoped to this one skill and printed in 2.6's two-column shape (holding tier · reaching for next) with the quest checks named.

### 2.3 — Compare to current level's criteria

Read `policy-skill-progression.md` to extract the level's criteria. For
each criterion:
- Compute fit (the metric value vs. the threshold)
- Mark `✓` or `✗`

### 2.4 — Compare to next level's criteria (if room to grow)

If the current level is not `reference`, do the same comparison against the
next level's criteria gate.

### 2.5 — Verdict + proposed action

Three verdicts:

1. **Promotion candidate** — all next-level criteria met. Propose:
   `/level <skill> --promote`.
2. **Park** — current level criteria all met; next-level criteria partially
   met. Surface the gaps. Propose: keep using; re-audit after N more
   sessions.
3. **Regression candidate** — current level criteria no longer met
   (correction load accumulated, behaviour-changing patches landed).
   Surface the breach. Propose: `/level <skill> --regress` to drop one
   level.

### 2.6 — Report — two-column "Holding tier" + "Reaching for next"

```
$ /level iterate
Skill: iterate
Current level: used (promoted 2026-04-22)

Holding tier — used (since promotion):
  M1 invocation count: 7
  M2 correction load: 1
  M3 redo rate: 0.0
  M5 cross-reference fan-in: 4 (implement-story, update-story, fixbug, agora)
  M6 last-update recency: 5d
  M4 reference depth: 458L, 31H

  ✓ M1 ≥ 1: 7
  ✓ Quest — has structure (## headings): yes
  (All used-tier criteria still met — no regression flag.)

Reaching for next — hardened:
  ✓ M5 ≥ 3: 4
  ✓ M2 ≤ 1: 1 (at limit)
  ✗ M1 ≥ 10 (since used promotion): 7 — 3 more invocations needed
  ✓ Quest — body contains a "When NOT to use" table: yes (line 47)

Verdict: park — close, but not yet at the hardened gate.

Proposed action: re-audit after 3 more closed-Section invocations.
  When M1 ≥ 10 AND M2 still ≤ 1, the next /level iterate run will tag it
  candidate-for-hardened. User then runs `/level iterate --promote`.
```

---

## MODE 3 — `/level <skill> --promote`

Apply a promotion. Writes.

### 3.1 — Re-audit (Mode 2)

Run the audit. If the verdict is not "promotion candidate", refuse:
"<skill> is not promotion-ready — <N> next-level criteria unmet:
<list>. Run `/level <skill>` to see the gaps."

If promotion candidate, proceed.

### 3.2 — Quest check (gate-specific)

Before confirming with the user, verify the gate's quest artifacts exist
(per [`policy-skill-progression`](../../policies/policy-skill-progression.md)
Rules 6, 7, 8):

**`draft → used`:** verify frontmatter validates + body has ≥ 1 `## ` heading.

**`used → hardened`:** verify three artifacts:
1. `## When NOT to use` table OR equivalent boundary-statement section exists in body.
2. `## Claims at this level` section exists with **at least 3** named claims.
3. (deferred until step 3.4 — the naming ceremony writes `epithet:`).

If artifact 1 or 2 is missing, **pause the promotion** and surface to the user:
> "<skill> isn't hardened-ready — the quest needs: <missing artifact(s)>.
>  Want me to scaffold a `## Claims at this level` section for you to fill in,
>  then re-run `--promote`?"

This is itself a 4-eye gate. Authoring the claims is a sub-task the user
may want to do inline before continuing.

**`hardened → reference`:** verify two artifacts:
1. The skill has authored OR is the primary entry in a `policy-*.md` file's `related_skills:`
2. A `## Identity` opening section exists (or will be written at step 3.4).

**Cadence of the `reference` ceremony: one per plaza round, executed at Stage 7** — the
2026-09-05 ruling (round 7; "one per session" was ruled 2026-08-14 and never fired). The
ruling's home is the Agora declaration §6
(`agora-declaration.md`); this
line is its mirror, kept verbatim in meaning.

### 3.3 — Identity step (gate-specific)

The identity arc unfolds per Rule 7. Different gates trigger different
identity work — and each gate has a **4-eye gate** per
[`policy-four-eyes`](../../policies/policy-four-eyes.md).

**`draft → used` — role descriptor.** Ask the user via `AskUserQuestion`:
> "Set a one-line role descriptor for `<skill>` (e.g. *'the inspector'*, *'the doctor'*, *'the architect'*). What should it be?"
> Options: propose a default (extracted from the skill's `description:`),
> or "let me name it" for free-text.
> Write the chosen value to `role:` in frontmatter.

**`used → hardened` — the naming ceremony.** Five sub-steps:

1. **Gather the skill's profile** — read its `## When NOT to use`, its modes,
   its `## Claims at this level` section, and its `experience.md` log.
2. **Present the philosophers catalog** from
   `agora-naming.md`:
   *Socrates (the dialectician), Aristotle (the categoriser), Euclid (the
   systematiser), Diogenes (the iconoclast), Hero of Alexandria (the
   engineer), Callimachus (the cataloguer), Plato (the form-seer), Pythagoras
   (the harmoniser), Heraclitus (the flux-seer), Thales (the first principle),
   Solon (the lawgiver), Pericles (the orator), Anaxagoras (the cosmologist),
   Theophrastus (the botanist / characterologist).* The catalog is open —
   propose a philosopher not yet listed if the fit is strong.
3. **Issue the structured naming prompt.** Reason through the skill's
   profile against the catalog. Propose ONE epithet + a one-sentence
   justification grounded in the skill's actual behaviour (cite a specific
   `## When NOT to use` entry or claim or XP-log moment — never poetic
   association alone). Format:
   > `<Philosopher> — <one-line domain>` (e.g. `Aristotle — the categoriser`)
   > *Justification:* "Like Aristotle's Categories, /check-ui-entity organises
   > every entity's surface into a fixed taxonomy of layers; the sticky
   > icon-twin spec is Aristotle's substance vs. accident applied to UI."
4. **4-eye gate** via `AskUserQuestion` — options:
   - *Accept* (proceed with proposed epithet)
   - *Propose alternative* (user names a different philosopher; skill re-justifies)
   - *Cancel* (promotion aborted; user re-runs later)
5. **On accept**, write `epithet: "<Philosopher> — <one-line>"` to frontmatter.

**`hardened → reference` — Identity canonicalization.** The `epithet:` already
exists. Write a `## Identity` opening section to the SKILL.md body — 1–3
paragraphs telling the story of why this epithet fits, citing 2–3 specific
XP-log moments as proof. Propose the draft as a 4-eye gate; user nods or
redirects.

### 3.4 — Confirm with the user

Display the audit report + the prospective new level + the identity step
result. Ask via `AskUserQuestion`:

> "<skill> meets all criteria for promotion to `<new-level>` with
>  identity `<role | epithet>`. Proceed?"

Options: Promote / Park / Cancel.

### 3.5 — Apply the promotion

Four writes, in this order:

1. **Frontmatter** — `.claude/skills/<skill>/SKILL.md`:
   ```yaml
   level: <new-level>
   promoted_at: <today's ISO date>
   role: "<role descriptor>"        # added at draft → used
   epithet: "<Philosopher> — <line>" # added at used → hardened
   ```

2. **Append the `## Level history` entry to the sidecar** — `.claude/skills/<skill>/experience.md`, newest first (US-AGORA-057: the sidecar is the append-only log; SKILL.md's own `## Level history`, where one still exists, is legacy and only shrinks — never write there, the prose ratchet reds on it). The section exists from the template; create it above `## Unrated journal` where it does not:
   ```markdown
   ## Level history

   - YYYY-MM-DD — promoted: <old> → <new> (M1=<N>, M2=<M>, M5=<F>, XP=<X>, quest: <one-line>, identity: <role/epithet>)
   - YYYY-MM-DD — promoted: <previous-from> → <previous-to> ...
   ```

3. **Identity section writes** (only at `hardened → reference`):
   - Insert the drafted `## Identity` section near the top of the SKILL.md
     body (after the frontmatter + intro paragraph, before the first MODE
     or Phase heading).

4. **experience.md scaffold** (only at `draft → used`, if file doesn't exist):
   - Create `.claude/skills/<skill>/experience.md` with empty frontmatter
     (`xp_total: 0`, `xp_by_level: {used: 0}`, no `last_xp_at`).

5. **Append one entry** to `.claude/sessions/IMPROVEMENTS.md`:
   ```markdown
   ## YYYY-MM-DD — `<skill>` promoted to `<new-level>`

   **Session:** <current session id or "-- standalone --">
   **What changed:** `<skill>`'s `level:` flipped from `<old>` to `<new>`. <identity-line if applicable>
   **Why:** All gate criteria met — M1=<N>, M2=<M>, M5=<F>, quest: <which artifacts>.
   **Effect:** <one-line on what changes — e.g. "/learn patches now check this skill's 3 named claims for contradiction">.
   ```

6. **Commit** with subject `level(skill): promote <name> <old> → <new>` — **this is the promotion-marker commit**. All subsequent M1/M2/M3 reference-point computations key off this commit's date.

### 3.6 — Report

Confirm the promotion to the user. Show the new frontmatter values, the
identity (role / epithet), the new `## Level history` entry, and the new
IMPROVEMENTS.md entry.

---

## MODE 4 — `/level <skill> --regress --corrects <sha>`

Apply a regression. Writes.

### 4.1 — `--corrects <sha>` is MANDATORY

Per [`policy-skill-progression`](../../policies/policy-skill-progression.md) Rule 3, regression triggers ONLY on a `/learn` patch that contradicts a claim the skill makes at its current level. The `--corrects <sha>` argument names the contradicting commit. Refuse without it:

> "Regression requires `--corrects <sha>` — the commit that introduced a behaviour-change contradicting a `<level>`-level claim. Threshold-based regression is forbidden. If M2 is high but no specific contradiction has landed, the right surface is a `/level <skill>` finding, not a regression."

`/learn` is the canonical caller of this mode — its final step asks the user the contradiction question and on a "yes" answer calls `/level <skill> --regress --corrects <new-commit-sha>` with the freshly-landed patch's sha.

### 4.2 — Confirm with the user

Display the contradicting commit (`git show --stat <sha>`), the level-claim being contradicted (cite a specific section of the skill's body), and the proposed new level. Ask via `AskUserQuestion`:

> "<skill> at `<current-level>` makes the claim: '<extracted claim>'. Commit `<sha>` contradicts it. Regress to `<new-level>`?"

Options: Regress / Cancel.

### 4.3 — Apply the regression

Same three-write shape as Mode 3.3:

1. **Frontmatter** — `level:` drops one tier; `promoted_at:` updates to today (the new tier's start).
2. **Append the `## Level history`** entry to the sidecar (`experience.md`, as in Mode 3.3):
   ```markdown
   - YYYY-MM-DD — regressed: <old> → <new> (corrects: <sha>, claim: "<one-line>")
   ```
3. **Append `IMPROVEMENTS.md`** entry framed as regression:
   ```markdown
   ## YYYY-MM-DD — `<skill>` regressed to `<new-level>`

   **Session:** <current session id>
   **What changed:** `<skill>`'s `level:` dropped from `<old>` to `<new>`.
   **Why:** Commit `<sha>` introduced behaviour contradicting the `<old>`-level claim '<extracted claim>'.
   **Effect:** <e.g. "/learn patches now run without the contradiction-question gate; cross-references in other skills should re-evaluate when next touched">.
   ```
4. **Commit** with subject `level(skill): regress <name> <old> → <new> (corrects: <sha>)` — this is the new reference point for subsequent M1/M2/M3 computations.

### 4.4 — Report

Confirm to the user. Note any follow-up — a skill regressed three times in six months is the system telling you the **concept** is wrong, not just the skill text; surface as a `/inspect-pipeline` finding for review.

---

## MODE 5 — `/level <skill> --xp +<N> "<snippet>"`

Append one XP entry to a skill's `experience.md`. Writes, but light —
the granular write-mode the orchestrator (`/agora --end` 2.3) and the
user call repeatedly across a session.

Per [`policy-skill-progression`](../../policies/policy-skill-progression.md)
Rule 6, the XP marker (🟢 success / 🟡 lesson) is inferred from the value
of `N`:
- `+20` to `+30` → 🟢 success
- `+10` to `+15` → 🟡 lesson
- Other values → ask the user which marker fits.

### 5.1 — Verify the skill is XP-eligible

XP applies only to skills at `used` or above (Rule 6). For a `draft`
skill:
- If this is the first XP attempt: refuse with *"<skill> is `draft` — XP starts accumulating at `used`. Promote first via `/level <skill> --promote`."*
- Caller (typically `/agora --end`) should skip `draft` skills in its `skills_invoked:` walk.

### 5.2 — Read or scaffold `experience.md`

Path: `.claude/skills/<skill>/experience.md`.

If the file doesn't exist, scaffold it from `_TEMPLATE_experience.md`:

```markdown
---
skill: <skill>
xp_total: 0
xp_by_level:
  <current-level>: 0
last_xp_at: null
---

# <skill> — experience log

```

Then proceed with the append.

### 5.3 — Append the graded XP entry

**Through the registry write path** (US-AGORA-048) — compose the entry, then:

```bash
flask agora write xp-entry --skill <skill> --file <entry.md>   # or --text "..."
```

The writer anchors on the `## Graded XP entries` **heading itself** (skipping
any comment block attached to it), inserts newest-at-the-top, and post-checks
the result — entry exactly once, below the heading, comment markers balanced.
A refusal (exit 1) means the file needs repair first; never hand-edit past it.
*(Why the heading, not the `<!-- Entries land below … -->` comment: that
marker is NOT reliably at the section top — in `agora`'s own experience.md it
sits near the file's BOTTOM, and anchoring on it inserted a newest-first entry
into the MIDDLE of the history — the lived #303 defect, fixed by construction
in the writer.)*

The entry format:

```markdown
## YYYY-MM-DD — session [[<session-id>]] · +<N> XP <emoji>

<snippet — one paragraph, no more than 4 sentences. The *why*: what
was learned or what the skill did right this session. Cite specific
moments (a commit sha, a file edit, a `/learn` patch, a redirect) when
relevant — the snippet is the durable memory.>
```

Where `<session-id>` is the current `/agora` session's slug (or
`"-- standalone --"` for hand-written entries outside a session) and
`<emoji>` is 🟢 (success) or 🟡 (lesson).

### 5.3b — Clear the converted stub (stub→rated conversion)

When the XP award **originates from a stub** in the skill's `## Unrated journal`
buffer (the normal path at `/agora --end` 2.3b *evaluate-the-stubs* — US-AGORA-010),
the same write **removes that stub line from the buffer**. The stub is the seed of
the graded entry just written; leaving it in the buffer would let it be graded
again next session (double-count). Rule:

- **Stub-sourced award** → write the graded entry (5.3) **and** delete its stub
  line from `## Unrated journal` — one call does both:
  `flask agora write xp-entry --skill <skill> --file <entry.md> --clear-stub "<substring unique to the stub>"`.
  The writer refuses when the substring hits zero or several journal lines, so
  a mis-targeted clear can never silently delete the wrong stub. The buffer
  shrinks as stubs graduate; an empty
  buffer is the steady state after a clean `--end`.
- **Log-sourced or hand-written award** (no stub) → nothing to clear; the buffer
  is untouched.
- A stub the user **skipped** at the 2.3b gate stays in the buffer (it graduates
  a later session) — only *graded* stubs are cleared.

The `## Unrated journal` buffer is the one part of `experience.md` the invoked
skill may append to directly (the narrow Rule 5 carve-out, `policy-skill-progression`
Rule 6); `/level --xp` is still the only writer of *graded* entries and the only
thing that *clears* the buffer.

### 5.4 — The rollup frontmatter is maintained BY THE WRITER

`flask agora write xp-entry` rolls the award into the frontmatter itself
(2026-08-16): `xp_total` always, `xp_by_level.<current-level>` (level read
from the skill's SKILL.md frontmatter), and `last_xp_at` (the entry
heading's date). **Do NOT hand-edit these fields around an award** — the
hand-maintained bucket line is exactly what drifted 716 XP across 11
skills before the writer took the rollup over, and
`flask agora state-check` now holds `xp_total == sum(xp_by_level)` at
every `--start`, so a hand-edit that double-counts or skips the bucket
refuses the next write against that file.

### 5.5 — No commit by `/level --xp` itself

Unlike `--promote` / `--regress`, `--xp` does **not** commit. The caller
commits in its own flow:
- `/agora --end` commits one combined `xp(skills): award N skills` commit at session close, with the `experience.md` diffs grouped.
- Hand-written `--xp` calls land in the next commit-tree triage like any other working-tree change.

This is intentional — XP awards are too granular to commit one-by-one;
the session boundary is the right grouping.

### 5.6 — Report

Echo to the user: `<skill>` gained `+<N> XP` (marker, total now `<xp_total>`).
For batched calls from `/agora --end`, the orchestrator aggregates the
report into a single summary table.

---

## MODE 6 — `/level <skill> --retire`

The lifecycle's ending (US-AGORA-040 — the retirement half `policy-skill-progression`
carries promote/regress without; the "skill eats skill" IMPROVEMENTS entry of
2026-07-25 prescribed exactly this by-hand shape: doctrine merges to the
consumer, XP/history archives as provenance and is **never summed**, and the
carcass stays as a tombstone so routers land on the consumer).

### 6.1 — Preconditions

- A **disposition exists and is user-approved** — retirement executes a
  decision made at a 4-eye gate (a US-AGORA-040-style audit pass, a `/plaza`
  ruling, or an explicit user ask); `--retire` never decides on its own.
- The **displacing pattern is named** (what absorbed the work — a skill, a
  phase, a mechanism). "Nothing would call this" is only believable when the
  caller's work went *somewhere*.

### 6.2 — Confirm with the user

Summarize: the skill, its level + XP record, the displacing pattern, and the
reference-sweep hit list (`grep -rn "<skill>" .claude/ docs/ CLAUDE.md` —
live surfaces only; session files, IMPROVEMENTS entries and research papers
are historical record and are never rewritten). Explicit textual confirm.

### 6.3 — Apply the retirement

1. `git mv .claude/skills/<name>/ .claude/skills-retired/<name>/` — the full
   directory (SKILL.md + experience.md if present) preserved as the audit
   trail, outside the roster's, the validator's, and the stats collector's
   globs — the corpus count drops.
2. Append a **tombstone entry** to the moved skill's `experience.md`
   `## Level history` (create the file from the template if the skill never
   had one; the moved SKILL.md is not written): date · `retired` · the
   displacing pattern · the authorizing pass/story · "routers land on
   <consumer>".
3. **Sweep the live references** (from 6.2's hit list): policy
   `related_skills:` frontmatter, other SKILL.md examples and hooks, the
   README roster — each repointed to the consumer or annotated *(retired)*.
4. `flask stats dump` (or note it for the session's ceremony seam) — the
   corpus count is derived, never hand-edited.

### 6.4 — Report

Confirm: `<skill>` retired to `.claude/skills-retired/`, N references swept,
consumer named. A retired skill can be un-retired only by the reverse move
plus a Level-history entry — silent resurrection is drift.

---

## Mode dispatch

Parse `[--board (default) | <skill-name> | <skill-name> --promote | <skill-name> --regress | <skill-name> --xp +<N> "<snippet>" | <skill-name> --retire]`:

| User says | Mode |
|-----------|------|
| (nothing) / `--board` / "board" / "show me the skills" | Mode 1 |
| `<skill-name>` / "audit X" / "how is X doing" | Mode 2 |
| `<skill-name> --promote` / "promote X" | Mode 3 |
| `<skill-name> --regress` / "regress X" / "downgrade X" | Mode 4 |
| `<skill-name> --xp +<N> "<snippet>"` / "award X N XP for ..." | Mode 5 |
| `<skill-name> --retire` / "retire X" / "the disposition says retire" | Mode 6 |

---

## Notes

- **First-cut thresholds are tentative.** The corpus is tiny (3 closed sessions as of 2026-05-17). After 10 closed sessions, the next `/level --board` run should surface "the thresholds put N skills at the gate; recalibrate?" as its own finding. Calibration is a `/document --update skill-progression` event.
- **Implementation efficiency:** the six metric computations are git-log + grep + frontmatter-parse operations. A Python helper (`scripts/skill_metrics.py`) would avoid recomputing per invocation but isn't required for correctness — the procedural shape is fine while the corpus is small.
- **`/level --board` is also the `/skills` skill the user originally proposed.** Folded into Mode 1 here — one skill with three modes is cleaner than two near-identical board skills.
- **Integration points** (per policy-skill-progression Rule 5 — wired in follow-on Sections, not in this skill's first cut):
  - `/agora --start` 1.1 reads the skill board and shows it in the skill-system state surface.
  - `/agora --end` 2.6 Section retrospective surfaces promotion candidates as findings.
  - `/learn` final step asks the contradiction question; on "yes" calls `/level <skill> --regress --corrects <sha>`.
  - `/inspect-pipeline --session` Mode 4 dispatch list includes regression candidates alongside existing finding types.
- After ratifying this skill's structure, run `/clear` or restart Claude Code for it to appear in the `/` menu.

---

## Initialisation

**What this skill reads before acting** (US-AGORA-041): the corpus's recorded
state — every SKILL.md's level frontmatter (`promoted_at:` is M1/M2/M3's
"since promotion" anchor; the `level(skill): promote …` marker subjects are its
git twin, never the source — US-AGORA-078), the `experience.md` journals,
totals and `## Level history`, and the session files' `skills_invoked:` (M1's
source) — read by `flask agora board`. The board is a command's output, never
remembered.

**Self-model:** the registrar of the leveling game — the ONLY authorised
writer of `level:` / `promoted_at:` / `role:` / `epithet:` / XP state
(`policy-skill-progression` Rule 5), including the lifecycle's ending
(MODE 6 `--retire`). A gap noticed mid-audit (a record the metrics could not
see) lands as a 🟡 journal stub in [`experience.md`](experience.md).

## Claims at this level

The invariants other skills and the user depend on `/level` to hold (the
`reference`-tier commitments — rules other skills cite; each is the unit `/learn` checks for contradiction
per `policy-skill-progression` Rule 4).

1. **Promotion and regression are never automatic — every level change passes a human 4-eye gate.** `--promote` (Mode 3.4) and `--regress` (Mode 4.2) both display the audit/contradiction report and wait on a nod before writing; the system *surfaces* candidacy, the user *confirms* it.
2. **`/level` is the sole writer of `level:` / `promoted_at:` / `role:` / `epithet:` frontmatter and of graded XP entries.** No other skill or direct edit may set those fields or write a `## Graded XP entries` block — an invoked skill may only append unrated stubs to its own `## Unrated journal` buffer.
3. **Regression fires only on a named contradicting commit, never on a threshold.** Mode 4.1 refuses without `--corrects <sha>` and cites the specific level-claim the patch contradicts; high M2 alone is a `/level <skill>` finding, not a regression.
4. **Every promotion and regression sets `promoted_at:` and writes a marker commit; the M1/M2/M3 measurement window keys off `promoted_at:`.** The frontmatter date is the robust reference point (a batch marker `level(skills): promote a, b, c` and a marker inside a squashed PR are invisible to a subject grep — lived at round 8's Stage 7); the marker subjects `level(skill): promote …` / `regress … (corrects: <sha>)` are its git twin, never the only source.
5. **A `used → hardened` promotion is gated on the quest artifacts existing before the nod.** Mode 3.2 pauses unless the body carries a boundary section AND a `## Claims at this level` section with ≥3 named claims, and the naming ceremony writes `epithet:` only after a separate accept.
