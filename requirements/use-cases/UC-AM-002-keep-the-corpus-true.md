---
id: UC-AM-002
title: Keep the corpus true
actor: maintainer
status: tested
stories:
- US-AGORA-008
- US-AGORA-055
- US-AGORA-057
- US-AGORA-064
- US-AM-001
- US-AM-002
- US-AM-003
quality_criteria:
- QC-REL-001
---

# UC-AM-002: Keep the corpus true

## Goal

A maintainer changes the skills, policies or catalogue and the build says whether the corpus still holds.

## Main flow

1. The maintainer edits a skill, a policy or a catalogue entry.
2. `python -m agora_checks all` runs the eight checks; each prints its failures and one summary line.
3. Frontmatter, record consistency and prose mass hold the skills and policies (US-AGORA-008, 055, 057).
4. Domain share, shipped references, links and secrets hold the published corpus (US-AGORA-064, US-AM-001, US-AM-002).
5. The catalogue check holds the requirements and their tests (US-AM-003).
6. CI runs the same command; the exit code is the verdict.

## Alternative flows

- **A generated copy drifted:** `--fix` regenerates it; a verbatim copy is reported for a human.
- **A skill grew:** the ratchet fails unless the growth is named with `--allow-growth`.
- **A story claims `tested` with a test that does not exist:** the catalogue check fails (C09).
