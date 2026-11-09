---
id: US-AGORA-035
title: The next session starts from the last one's baton
actor: developer
feature_area: session
priority: should-have
status: tested
source: requirements
related_tests:
- tests/test_session.py::test_close_refuses_without_a_baton_or_a_retro
- tests/test_session.py::test_the_baton_of_the_last_closed_session_is_read
quality_criteria:
- QC-MNT-001
glossary_terms:
- GLOSS-BATON
- GLOSS-SESSION
---

# US-AGORA-035: The next session starts from the last one's baton

## User Story

As a **developer coming back to the work**, I want **each closed session to hand over a short list of what comes next, read back when the next one opens**, so that **the agent does not re-derive from memory where the work stands**.

## Acceptance Criteria

- [x] the baton of the last closed session is read at the next start -- `tests/test_session.py::test_the_baton_of_the_last_closed_session_is_read`
- [x] a session cannot close without a baton -- `tests/test_session.py::test_close_refuses_without_a_baton_or_a_retro`

## Origin

Adapted from the parent's US-AGORA-035, *Rollover baton plus judgement-free steps made automatic*. The parent also verifies every pointer in the baton against its tracker; this repository reads the baton back as written.
