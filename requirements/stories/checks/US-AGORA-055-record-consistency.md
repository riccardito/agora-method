---
id: US-AGORA-055
title: 'One fact, one home: every copy is generated or checked'
actor: maintainer
feature_area: checks
priority: must-have
status: tested
source: gap-analysis
related_tests:
- tests/test_record_consistency.py::test_a_hand_edit_to_a_generated_block_is_drift_and_fix_restores_it
- tests/test_record_consistency.py::test_a_source_change_reaches_the_generated_copies
- tests/test_record_consistency.py::test_links_are_ignored_by_the_verbatim_comparison
- tests/test_record_consistency.py::test_the_repository_is_consistent
- tests/test_record_consistency.py::test_verbatim_drift_is_reported_and_never_auto_fixed
quality_criteria:
- QC-REL-001
glossary_terms:
- GLOSS-CHECK
---

# US-AGORA-055: One fact, one home: every copy is generated or checked

## User Story

As a **maintainer whose agent reads the same facts in several files**, I want **every copy to name its source and how it is derived**, so that **a copy that drifts from its source fails the build instead of misleading the agent**.

## Acceptance Criteria

- [x] a hand edit to a generated block is drift, and `--fix` restores it -- `tests/test_record_consistency.py::test_a_hand_edit_to_a_generated_block_is_drift_and_fix_restores_it`
- [x] a change to the source reaches every generated copy -- `tests/test_record_consistency.py::test_a_source_change_reaches_the_generated_copies`
- [x] verbatim drift is reported and never fixed automatically -- `tests/test_record_consistency.py::test_verbatim_drift_is_reported_and_never_auto_fixed`
- [x] links do not count as a difference in a verbatim copy -- `tests/test_record_consistency.py::test_links_are_ignored_by_the_verbatim_comparison`
- [x] the repository is consistent -- `tests/test_record_consistency.py::test_the_repository_is_consistent`

## Origin

Adapted from the parent's US-AGORA-055, *the record-consistency lint: one fact, one home, one direction*. The parent's version found twelve contradictions in its own record on the first run.
