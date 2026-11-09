---
id: US-AGORA-097
title: A phase is ticked only together with the human's nod
actor: developer
feature_area: session
priority: must-have
status: tested
source: requirements
related_tests:
- tests/test_session.py::test_a_gate_without_a_nod_cannot_be_recorded
- tests/test_session.py::test_the_demo_is_green
quality_criteria:
- QC-MNT-001
glossary_terms:
- GLOSS-NOD
- GLOSS-SESSION
---

# US-AGORA-097: A phase is ticked only together with the human's nod

## User Story

As a **developer who approves each phase**, I want **the phase checkbox and my recorded approval to be one act**, so that **a gate that was never asked cannot be recorded as passed**.

## Acceptance Criteria

- [x] a tick without a nod is refused and the file is left unchanged -- `tests/test_session.py::test_a_gate_without_a_nod_cannot_be_recorded`
- [x] the nod is written beside the box in the same write, as the demo shows -- `tests/test_session.py::test_the_demo_is_green`

## Origin

Adapted from the parent's US-AGORA-097, *the seam-gate wrapper and the phase-gate warning*. There the writer refuses a box already ticked, an absent phase or a missing nod; this repository ships the same refusal in `session.tick()`.
