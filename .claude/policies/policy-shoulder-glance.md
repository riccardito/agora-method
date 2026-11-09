---
name: shoulder-glance
title: "Shoulder-glance — the Schulterblick reflex (glance back before moving on)"
status: active
domain: discipline
related_skills:
  - agora
  - plaza
related_lint_rules: []
---

# Shoulder-glance policy

## TL;DR

1. **The shoulder-glance fires before leaving any chapter** — a phase, a session, a topic, or an Era. It is a **retrospective over the whole span just finished** (the time "at the seat"), not a final-moment loss-check. Three checks: **(1) have I missed something? · (2) what have I used? · (3) how should it look?**
2. **Both halves — catch AND close.** The glance surfaces anything left behind (the *safety* half) **and** summarizes what was engaged + used to **close the chapter** (the *closure* half). The closure is what licenses moving forward with confidence. A glance that only does the safety half is incomplete.
3. **Sibling of `policy-four-eyes` — backward-looking, not forward.** Four-eyes is *propose-and-confirm at a transition gate* (forward-looking: "here's what I'd do — nod?"). Shoulder-glance is *retrospective summary-and-leftover-check before leaving* (backward-looking: "here's what just happened — anything dropped?"). The two pair at a boundary: glance back, then propose forward.
4. **It is the fractal skeleton's slots 4 + 5.** The glance is the concrete act of **slot 4 (evaluation / open-thread handling)** and **slot 5 (ending: summarize + close)** of the planning skeleton (`agora-planning-skeleton.md`). It gives the skeleton's "ending" a defined ritual.
5. **Recognize, don't multiply.** The glance *names* a reflex Agora already does through scattered mechanisms — open-threads capture (`THREADS.md`), Issue documentation, the implementation-plan Surprises-&-decisions log. It unifies them as one discipline and wires into the **existing** fires (`/agora --end`, `/plaza` close-out, the Era off-boarding "finish old Era" movement). It adds **no new gates** beyond those (per `policy-four-eyes` Rule 1, "recognize, don't add").

## Why this exists

Agora *already* avoids forgetting topics — it opens threads in `THREADS.md`, mirrors work into GitHub Issues, and appends to the implementation-plan Surprises-&-decisions log. But the discipline behind all of these was **unnamed**: the *why* behind "we never forget a topic when we move on." Unnamed disciplines drift (the cross-cut behind all five round-4 background problems, especially BP-2 *capture cost above the amnesia threshold* — an idea with no obvious slot gets noted-not-planned and ages out). The lived evidence: T-009 silently fell out of `THREADS.md`; the breach ledger had 2 entries across ~30 sessions; a milestone phase-plan lived only in chat and was guessed wrong at the next session.

The **Schulterblick** (German for the shoulder glance) — the glance back over your shoulder when you stand to leave a train seat — is the metaphor, and it carries **two halves**. You glance back **(a)** to check you left nothing behind, but also **(b)** to look over the *whole time you sat there* — what you did, what you used. That summary **closes the chapter**, and the closure is what gives you the **confidence to leave the seat clean**. A glance that only checks for dropped items misses the larger half: the reflex is a *retrospective over the span just finished*, not a final-moment loss-check. Naming it makes the closure deliberate — and a deliberately-closed chapter is one a future session can trust without re-deriving.

This policy is the **human-discipline** answer to boundary drift; the `flask agora audit` drift scheduler (US-AGORA-024) is its **automated backstop**. Discipline catches what tooling can't see; tooling catches what discipline forgets.

## The rules

### 1. The glance is retrospective over the whole chapter, not a final-moment check

**What:** Before leaving a phase / session / topic / Era, scan the **topics of the whole chapter just finished** — the entire "time at the seat" — with three checks: *(1) have I missed something? · (2) what have I used? · (3) how should it look?* Not just "did I drop anything in the last minute".

**Why:** A loss-check at the final moment only catches what's visible right then. The value is in re-reading the *span*: the thread opened three phases ago, the skill used once and never logged, the surface that drifted from its plan. The retrospective is what surfaces those.

**Where enforced:** skill prompt (`/agora --end` — the close-out paper's *touched-and-unresolved* list at 2.10 is the catch half made an artifact; `/plaza` close-out; the Era off-boarding "finish old Era" movement) + self.

### 2. Both halves — catch (safety) AND close (closure)

**What:** The glance does two things and is incomplete without both: **(a) safety** — surface anything left behind (becomes a `THREADS.md` thread / a GitHub Issue / a Surprises-log entry, never a silent abandonment); **(b) closure** — summarize what was engaged + used, so the chapter is *closed*, not just abandoned-without-leftovers. The closure (the compacted summary, the retro, the Era theme line) is what licenses moving forward with confidence.

**Why:** A safety-only glance leaves chapters that are "clean" but unsummarized — the next session still has to reconstruct what happened. The closure half is what makes the chapter a durable, trustable record. Confidence to move on comes from having *accounted for the seat*, not just from having dropped nothing.

**Where enforced:** skill prompt (`/agora --end` 2.3 compacted summary + 2.6 retro = the closure half; 2.3 thread reconciliation + 2.5 dispatch = the safety half) + self.

### 3. Sibling of `policy-four-eyes` — the backward-looking half of a boundary

**What:** Position the shoulder-glance explicitly as the retrospective counterpart of the four-eye gate. **Four-eyes** = propose-and-confirm at a transition gate (forward-looking). **Shoulder-glance** = retrospective summary + leftover-check before leaving (backward-looking). At a real boundary they pair: *glance back over what just finished, then propose forward what comes next.*

**Why:** The two disciplines are easy to conflate ("checking at a boundary"), but they point in opposite directions and catch different failures. Four-eyes catches *acting without consent*; shoulder-glance catches *leaving without accounting*. Naming both, and their pairing, keeps each sharp.

**Where enforced:** this policy + `policy-four-eyes` (cross-linked) + self.

### 4. The glance is the skeleton's slots 4 + 5

**What:** The shoulder-glance is the concrete ritual of the fractal planning skeleton's **slot 4 (evaluation / open-thread handling)** and **slot 5 (ending: summarize + close)** (US-AGORA-017). When a Goal or Era reaches its ending, the glance *is* how slots 4 + 5 get done.

**Why:** The skeleton names the slots but not the act that fills them. Without a named ritual, "ending" degrades to "stop working". The glance gives slots 4 + 5 a defined, repeatable shape — and `slot 5 → next slot 2` (the rollover, US-AGORA-019) follows naturally once the chapter is properly closed.

**Where enforced:** `agora-planning-skeleton.md` (the skeleton doc names this mapping) + skill prompt + self.

### 5. Recognize, don't multiply — unify the existing mechanisms

**What:** The glance names the mechanisms Agora already has — `THREADS.md` open-threads capture, GitHub Issue documentation, the implementation-plan Surprises-&-decisions log — as the **concrete expressions of one reflex**. It is wired into the **existing** boundary fires (`/agora --end`, `/plaza` close-out, the Era off-boarding movement) and adds **no new gates** beyond them.

**Why:** Per `policy-four-eyes` Rule 1 ("recognize, don't add"), naming a discipline must not multiply ceremony. The point is to make the *one* reflex explicit and citable, not to bolt a new checkpoint onto every step. A skill that already does a closing sweep adopts this policy by recognizing it; it does not add a second sweep.

**Where enforced:** skill prompt (recognition at existing fires) + self.

## Common mistakes

- **Safety-only glance** — checking "did I drop anything?" and skipping the summary. The chapter ends clean-but-unsummarized; the next session re-derives what happened. Do both halves — catch *and* close.
- **Final-moment-only check** — glancing only at the last thing done, not the whole span. The thread opened early in the chapter slips. Re-read the *span*, not the last minute.
- **Adding a new gate** — inventing a "shoulder-glance step" at every phase boundary. The reflex is *recognized* at the existing `--end` / close-out / Era-off-boarding fires, not multiplied. If a skill already has a closing sweep, that sweep *is* the glance.
- **Confusing it with four-eyes** — treating the backward glance as a forward proposal (or vice versa). Glance back over what finished; *then* propose forward what's next.

## See also

- [`policy-four-eyes`](policy-four-eyes.md) — the forward-looking sibling (propose-and-confirm at a transition gate); the two pair at a boundary.
- [`policy-documentation`](policy-documentation.md) — the Surprises-&-decisions log (one concrete expression of the glance).
- `.claude/skills/agora/SKILL.md` — `--end` steps 2.3 (compact + reconcile threads), 2.5 (dispatch), 2.6 (retro): the glance's safety + closure halves at the session boundary.
- `.claude/skills/plaza/SKILL.md` — the round close-out glance.
- [`THREADS.md`](../sessions/THREADS.md) — where surfaced leftovers land (the safety half's destination).
- `agora-planning-skeleton.md` — the glance is slots 4 + 5 of the fractal skeleton.
- `RP-AGORA-004` (T6) — the research paper that proposed the policy; US-AGORA-024 (drift scheduler) is its automated backstop.
