---
name: write
description: "Author a written artefact to a specified form, voice and language — papers, explainers, chapters, letters, CVs, one-pagers, landing copy. Runs gather then a content brief then produce, and finishes with a named style pass that targets burstiness and markdown-leakage rather than cosmetic em-dash removal. Voice is derived from a reference corpus when one is named, from prose parameters otherwise. NOT for deciding where a file lives or keeping it in sync — that is /document."
argument-hint: "<what to write> [--brief | --style <path>] [--corpus <path-or-glob>] [--lang <code>]"
level: used
promoted_at: 2026-07-27
role: "the artefact author — gather · brief · produce · measured style pass"
---

> **Journal-at-source** (policy-skill-progression Rule 6): when you finish a unit of work in a session, append ONE unrated stub to [`experience.md`](experience.md) `## Unrated journal` — `YYYY-MM-DD · [[session-id]] · <did X> · 🟢/🟡 <one-clause signal>`. One line, lighter than the session Log; `/agora --end` 2.3b grades it.

# Write — Author a Written Artefact to a Specified Form and Voice

`$ARGUMENTS` names what to write. The skill produces **prose**, to a
specification agreed before drafting starts, in a voice derived from a real
corpus wherever one exists.

Every premium written artefact follows the same three beats regardless of what
is being written:

```
GATHER  ─→  SPECIFY (the brief)  ─→  PRODUCE  ─→  STYLE PASS
 facts       audience · purpose       the draft     burstiness
 sources     form · structure                       markdown-leak
 corpus      length · density                       voice match
 constraints voice · tone · language                language-native
```

Without the skill that pattern gets re-derived every time, and the beat that
gets skipped under time pressure is always the same one — the brief — which is
why the draft then needs three rewrites.

| Mode | Output | When |
|------|--------|------|
| (default) | The finished artefact at a path you name | You want the whole loop: gather → brief → draft → style |
| `--brief <topic>` | The content brief alone, then stop | You want to approve the spec before any prose exists — also the mode another skill calls |
| `--style <path>` | The same file, restyled in place | Prose already exists (yours, mine, or a model's) and needs the pass |

**When NOT to use this skill:**

| Need | Use instead |
|------|-------------|
| Decide *where* a doc lives, its frontmatter, its index entry, its CLAUDE.md mirror | [`/document`](../document/SKILL.md) — placement and sync is its whole job. It may call *this* skill for the prose |
| Author a cross-cutting rule as a policy | [`/document --policy`](../document/SKILL.md) |
| Document a feature you just built | `/implement-story` Phase 3.8 writes the wiki seed |
| Write a user story / use case / quality criteria | `/new-story` — the catalogue has its own format and lint |
| Write a research paper that decomposes into stories | `/feature-plan` — RP-*.md is its Phase A output |
| Capture a skill-level correction | [`/learn`](../learn/SKILL.md) |
| Commit messages, code comments, PR bodies | Direct — these have their own conventions and are not artefacts |

**This skill never chooses a path.** If the request implies "and put it
somewhere sensible", that is `/document`'s call, not this one. Ask for the path
or hand back to `/document`.

---

## The brief — what "specify" means

The industry convention for a content brief is stable, and it is what this beat
produces. **Nine fields; none of them optional, though several are often one
word.** Write them down and confirm before drafting — this is the skill's 4-eye
gate per [`policy-four-eyes`](../../policies/policy-four-eyes.md) Rule 2, fired
in prose with a proposed default for each field, not as a blank form.

| Field | What it fixes |
|-------|---------------|
| **Audience** | Who reads this, and what they already know. "A developer who has never seen Agora" and "the user who built it" produce different documents |
| **Purpose** | What it must achieve. Persuade · explain · record · orient · sell |
| **Form** | Paper · explainer · chapter · letter · CV · one-pager · landing copy · README |
| **Structure** | The section skeleton, named up front. For a known form, inherit it (see *Inherited shapes* below) |
| **Length** | A range, not a number |
| **Density** | *How much per paragraph.* Inherited from the session-file discipline — a **structured summary, not a transcript**. Two artefacts of equal word count can differ 3× in what they actually say, and length alone never catches that |
| **Voice** | Constant. Derived from a corpus where one exists (below) |
| **Tone** | Varies per artefact — the mood, not the personality. Same voice, different tone: a milestone paper and an incident post-mortem |
| **Language** | A real parameter, not a flag. See *Writing native* below |

Voice-versus-tone is a genuine split and collapsing it is the common mistake:
**voice is the personality and holds across everything you write; tone is the
mood of this one piece.** A skill parameterised only on "tone" will drift its
voice between artefacts.

**Provenance markers (`⟨ergänzt⟩` on every passage you added to the user's own words) are
a Voice-field OPTION, never a default** — a review aid stripped in the acceptance seam, not
a second edit (lived session 2026-10-17: accepted whole, markers the one remark).

### Inherited shapes

Agora already has four house conventions. Where the artefact matches one,
**inherit it rather than inventing a shape** — this is what keeps a new
document recognisable as part of the same corpus:

| Shape | Source | Inherit for |
|-------|--------|-------------|
| **Research-paper** — discovery → critical review with alternatives → decomposition | `docs/references/research/RP-*.md` (lint R060) | Analytical artefacts that end in a recommendation |
| **Summary + body** — a short self-contained summary paired with the full rationale | `.claude/policies/` + its verbatim CLAUDE.md mirror | Any long artefact. Carries its own hard rule: **the summary is verbatim, never a paraphrase** — if the two need different wording, the rules are not sharp enough yet |
| **Narrative "what currently is"** — present tense, narrative rather than reference | `docs/wiki/feature-*.md` | State-of-the-system documents |
| **Structured summary** — dense, no transcript | `.claude/sessions/*.md` | Anything where a reader needs the shape fast |

---

## Voice — corpus first, prose as the fallback

**If a reference corpus exists, derive the voice from it. Describing a voice in
adjectives is the fallback, not the default** — "warm but precise" is four
different documents depending on who reads it.

### Corpus mode (preferred)

Given `--corpus <path-or-glob>` — or a corpus the request implies — **run the
instrument**:

```bash
flask agora voice-profile "docs/references/research/RP-*.md"
flask agora voice-profile docs/book --lang de
flask agora voice-profile "<corpus-a>" "<corpus-b>"   # side by side
```

It reports words sampled · sentence mean / median / **standard deviation (the
burstiness baseline the style pass targets)** · share under 10 words · share
over 30 · em dash, bold and semicolon per 1 000 words · contractions · person
counts · prose share of lines · mean heading depth. Each argument is a file, a
directory or a **quoted** glob and becomes one column -- an unquoted glob is
expanded by the shell into one argument per file, so eight READMEs become eight
columns and the row runs off the page; pass the directory when the set is a folder
(lived session 2026-11-09) -- so **comparing two or three corpora is how a profile is
sanity-checked**.

Read the numbers, then judge what the command cannot: **tense** (present, past,
mixed — and whether the mix is systematic), **vocabulary tics** (recurring
constructions, favoured connectives, terms of art used without gloss), and
**paragraph rhythm** (whether one-sentence paragraphs are used for emphasis).
Those stay yours.

Two things the output tells you that are easy to misread:

- **`n/a` is not zero.** Contractions and `we`/`I`/`you` are English constructs;
  against a German corpus they are reported `n/a`, because a zero would read as a
  finding about the corpus when it is one about the tool.
- **A guard warning means suspect the instrument, not the corpus.** An
  implausible per-1k rate is the signature of a stripping failure.
- **An implausible WORD COUNT is the same signal, and nothing guards it.**
  `voice-profile` strips fenced code blocks — correct for prose, wrong for an
  artefact whose content *lives inside a fence*. **A design brief is the
  canonical case:** the markdown around the fence is a three-line wrapper and
  the entire prompt is inside it, so profiling the file measures the wrapper.
  Lived session 2026-08-01: the design-brief corpus reported **84
  words from a 73-line file** — a rate no guard flags, because every *per-1k*
  figure derived from 84 words is internally consistent. **Sanity-check words
  against file length before trusting a profile**; when they disagree, extract
  the fenced content to a scratch file and profile *that*. Corpora that need
  this: `docs/references/ui/*-design-brief.md`, and anything else whose
  deliverable is a pasteable block.
- **The profile measures PROSE LINES ONLY — table content is stripped too, so
  every rate it reports is a *prose* rate.** The sibling of the fenced-block
  trap above, and more dangerous because it does not look like a failure: the
  numbers are correct, they simply do not describe the part of the artefact you
  are about to edit. The tool already tells you — **`Prose share of lines`** is
  the signal — and it is easy to read as trivia rather than as scope. The
  failure mode is a style pass that **corrects the wrong layer and cannot tell**:
  bold and em dashes added inside `| Commits |` cells change nothing the profile
  can see, so the re-measure comes back **byte-identical** and reads as "the edit
  didn't take" rather than "the edit wasn't measured." Lived
  session 2026-08-06: six table-cell corrections, 1 484 words
  and 82 sentences before and after, `bold 16.2` both times — the corpus's
  `32.4` was its prose rate and the gap was in the paragraphs. **Before
  correcting a rate, ask which layer the target rate came from**; when the
  artefact is table-heavy, match the tables to the corpus's *visible* convention
  by reading it, and match the numbers by editing prose.

State the profile back before drafting. A wrong profile is cheap to correct at
this point and expensive afterwards.

> *Why this is a command and not a procedure* (US-AGORA-045 — the record, not an
> instruction): this skill said "measure it, don't guess it" and shipped no
> instrument, so every invocation re-derived a scanner. The first re-derivation
> wrote a bug into it — a negated character class matched newlines, so one stray
> `<` consumed everything to the next `>`, reading 4392 prose words as 537 and
> inflating every per-1k rate ~8×. It was caught only because 125 em dashes per
> 1 000 words is implausible on its face. A rule that depends on re-deriving an
> instrument re-gambles that instrument's correctness on every use.

**The known corpora in this repo:**

- `docs/book/` — the product book: 16 German chapters plus
  appendices, third person. The voice reference for any book work
- `docs/references/research/RP-*.md` — the research-paper voice
- `docs/wiki/feature-*.md` — the narrative "what currently is" voice
- `.claude/policies/` — the rule-statement voice

### Prose mode (fallback)

No corpus — a genuinely new artefact type, or writing for an external target
whose voice you cannot sample. Then specify the voice in prose *and say that
you are in fallback mode*, because the style pass loses its measured baseline
and falls back to general targets. Where the external target has public writing
(a company's site, a journal's back issues), **that is a corpus** — prefer it
over adjectives.

---

## Writing native — language as a real parameter

`--lang de` does not mean "write it in English and translate". A German
artefact is **written as German**: compound nouns rather than noun phrases,
verb-final subordinate clauses, native connectives, and no Anglicism the
reference corpus would not use.

The tell of translated-not-written prose is that the *sentence shapes* stay
English while the words become German. This check is part of the style pass and
it is the one that most needs the corpus — the book is the specification for
what German-as-written looks like here.

The parent project ships 12 locales; the same rule applies to any of them.

---

## The style pass — the named step

**This is the step the skill exists for**, and it is specified against the
signals that actually carry, not the one everybody names.

### 1. Burstiness — the load-bearing check

**Human prose alternates short and long sentences; generated prose settles into
a metronomic middle of roughly 18–24 words with low variance.** This is the
strongest single tell, and it survives every cosmetic edit.

- Measure the draft's sentence-length spread; compare against the corpus
  profile (or, in fallback, against a target that is *visibly varied*)
- Fix by **splitting and merging**, never by padding. A short sentence lands
  because it is short. Adding filler to make a long one raises the mean and
  lowers the variance — the opposite of the goal
- One-sentence paragraphs are legitimate emphasis if the corpus uses them

### 2. Markdown leakage

The em dash is **one instance of a class, not the target**. It is markdown
structure surviving into prose, which is why instructing "avoid em dashes" does
not help: the instruction is not recognised as being about formatting. Sweep
the class:

- Em dashes used as the default connective, where a comma, colon, full stop or
  restructure is what the sentence wanted
- The `X — not Y` appositive, used reflexively
- The `It is not just X, it is Y` frame
- Bold-for-emphasis mid-sentence, where the sentence should carry its own stress
- Bulleted lists where the corpus writes prose. **Lists are structure leaking
  into narrative** — the book has chapters, not bullet points
- Tricolons and heading scaffolding in a piece too short to need them

**Do not strip these to zero.** A corpus that uses em dashes should keep them
at its own rate — matching the profile is the goal, not abstinence.

### 3. Voice match

Re-read against the profile: person, tense, register, paragraph length,
vocabulary. Name any deliberate divergence rather than leaving it to look like
drift.

### 4. Language-native

Per *Writing native* above. Skip only for English.

### Reporting the pass

State what changed and why, per check — *"mean sentence length 21.4 → 17.9,
share under 10 words 4% → 19%, matching the book's 21%"* beats *"improved
flow"*. A style pass whose result cannot be stated in numbers or named
constructions was probably not run.

---

## MODE 1 — author (default)

### 1.1 — Gather

Collect what the artefact needs before deciding anything about its shape:

- **Facts and sources** — the repo, the catalogue, the session record, the web
  where the artefact needs outside grounding. **A source is a claim, not a fact:**
  a spawn's `## Result`, a landscape figure, a prior paper's number is *probed
  against the tree or re-measured* before the brief wherever a recommendation
  will rest on it — and two sources that disagree are reconciled by ONE stated
  method, never by picking a side (lived session 2026-09-06: a spawn's
  "the agora CI leg can skip MongoDB" was false on probe and turned the paper's
  central recommendation into a staged one; two domain-tag counts a factor of two
  apart were replaced by a re-measure)
- **Constraints** — what must appear, what must not, deadlines, house rules
- **The corpus** — the voice reference, if one exists
- **The target's context** — for external writing, research the recipient

**Missing or unverified information surfaces here, not mid-draft.** If a required
fact is unavailable, say so now and either get it or record the gap as an explicit
assumption in the brief; a load-bearing claim you could not probe is named in the
brief as an assumption, not carried into the draft as a fact.

### 1.2 — Specify: write the brief

Fill the nine fields. Inherit a shape where one matches. Derive the voice
profile from the corpus. **Confirm with the user before drafting** — prose,
with a proposed default per field.

**One-pass exception (lived session 2026-07-27):** when **every
field is already user-settled** (the request + its refinements answered them
all) **and the user asked for the deliverable now**, presenting the brief and
the draft **in one pass is legitimate** — the brief is stated visibly at the
top as the redirect surface, never skipped silently. The beat survives; only
the extra round-trip goes. The tell that the exception does NOT apply: any
field you had to guess — then the gate fires as written, because a guessed
field is exactly what the round-trip exists to catch.

**A brief addressed to an AI design tool (ClaudeDesign or similar) is a
SPAWN BRIEFING — brief it and verify its return like one.** Two halves,
both lived session 2026-07-28:

- **Briefing half:** the `policy-spawns` precision rules apply — for every
  chrome region the brief constrains, **name a lived reference surface to
  mirror exactly** ("the header is the catalogue hub's header, verbatim"),
  never a hand-composed description ("the standard premium hub header").
  The first workspace-hub brief hand-composed its header region and the mockup came
  back with a wrong header — one full correction round-trip that a named
  mirror would have prevented.
- **Verification half:** the returned mockup is a spawn RESULT — the
  parent verifies it against the shipped reality (chrome classes, existing
  conventions, responsive rules) **before any downstream consumer folds
  it**, so the plan receives a validated full-premium mockup rather than
  correcting mid-session. The same session's fold-time verification DID
  catch a footer contradiction — the discipline works when it runs; run it
  at the return, not after the plan started consuming.

### 1.3 — Produce

Draft to the brief. Write it as prose, in the target language, in the profiled
voice — do not draft in English and convert, and do not draft in a generic
register intending to fix it in the style pass. **The style pass corrects a
draft; it does not rescue one written to the wrong spec.** The register most
likely to leak in is the one you write *from* — the harness's chat rules (no em
dashes, no bold) are a house style — so **profile the draft before the pass**
and rewrite to the corpus rates, never let the pass find the mismatch (lived
session 2026-09-26: 3.8 em dashes /1k against 18–22).

### 1.4 — Style pass

Run all four checks. Report per check.

### 1.5 — Verify

- [ ] Every brief field is satisfied, or the divergence is named
- [ ] Length inside the range; density matches the specified density
- [ ] Voice profile matched, or divergences named
- [ ] Style pass run and **reported with specifics**
- [ ] For a non-English artefact: written native, not translated
- [ ] Path was given by the user or by `/document` — this skill did not invent one
- [ ] Every claim a recommendation rests on was probed or re-measured; disagreeing
      sources were reconciled by one stated method, and any unprobed claim is a
      named assumption
- [ ] For an AI-design-tool brief: every constrained chrome region names a
      lived mirror surface, and the return gets verified against the shipped
      reality before anything downstream consumes it

---

## MODE 2 — `--brief <topic>`

Produce the brief and stop. Two uses:

- **The user wants to approve the spec** before any prose exists — the cheapest
  possible correction point
- **Another skill is calling** — `/document --explainer` uses this to get a
  brief it can hand back, or to hand the whole loop over

Output is the nine fields plus the voice profile. No prose.

---

## MODE 3 — `--style <path>`

Run the style pass on prose that already exists, in place.

Requires a voice target: `--corpus <path>` for the measured version, or the
prose fallback. **Without either, the pass reduces to the burstiness check plus
markdown-leakage** — still worth running, and say that is what happened.

Useful on: an artefact drafted before this skill existed, a model's output, a
chapter that has drifted from the book's voice.

---

## Mode dispatch

| User says | Mode |
|-----------|------|
| `<what to write>` with no flag | **Mode 1** (author) |
| `--brief <topic>` / "just the spec" / "brief me first" | Mode 2 |
| `--style <path>` / "de-AI this" / "match the voice" / "restyle" | Mode 3 |
| Anything about *where a file goes*, frontmatter, an index entry | Not this skill — hand to [`/document`](../document/SKILL.md) |

---

## Key rules

- **The brief is not optional and not implicit.** Drafting without one is the
  single reliable way to produce an artefact that needs three rewrites. If the
  user wants to skip it, produce a three-line brief and confirm that — do not
  skip the beat.
- **Corpus beats adjectives.** Wherever a reference corpus exists, measure it.
  "Warm but precise" is not a specification.
- **The style pass targets burstiness and markdown leakage, not em dashes.**
  A pass that only removes em dashes has removed the visible signal and left the
  real one in place.
- **Match the corpus rate; do not strip to zero.** Abstinence is its own tell.
- **Never invent a path.** Placement is `/document`'s job.
- **Do not draft in English and translate.** Write native, or say plainly that
  a translation is what is being produced.
- **Report the style pass in specifics.** Numbers and named constructions, not
  "improved the flow".

---
