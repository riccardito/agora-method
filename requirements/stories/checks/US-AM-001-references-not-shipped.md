---
id: US-AM-001
title: References to what was not shipped are counted and may only fall
actor: reader
feature_area: checks
priority: should-have
status: tested
source: user-feedback
related_tests:
- tests/test_shipped_refs.py::test_a_catalogued_story_is_shipped
- tests/test_shipped_refs.py::test_a_removed_reference_passes_and_says_the_baseline_can_tighten
- tests/test_shipped_refs.py::test_each_kind_is_counted
- tests/test_shipped_refs.py::test_growth_reds_and_falling_passes
- tests/test_shipped_refs.py::test_shipped_things_and_placeholders_are_not_counted
- tests/test_shipped_refs.py::test_the_repository_holds_its_baseline
quality_criteria:
- QC-REL-001
glossary_terms:
- GLOSS-RATCHET
---

# US-AM-001: References to what was not shipped are counted and may only fall

## User Story

As a **reader of an extracted corpus**, I want **every reference to a command, skill, story, session or path the repository does not ship counted against a baseline that may only fall**, so that **I know what the files point at that I cannot open, and the number only improves**.

## Acceptance Criteria

- [x] each kind of reference is counted -- `tests/test_shipped_refs.py::test_each_kind_is_counted`
- [x] shipped things and placeholders are not counted -- `tests/test_shipped_refs.py::test_shipped_things_and_placeholders_are_not_counted`
- [x] a story present in this catalogue counts as shipped -- `tests/test_shipped_refs.py::test_a_catalogued_story_is_shipped`
- [x] growth fails and falling passes -- `tests/test_shipped_refs.py::test_growth_reds_and_falling_passes`
- [x] a removed reference says the baseline can tighten -- `tests/test_shipped_refs.py::test_a_removed_reference_passes_and_says_the_baseline_can_tighten`
- [x] the repository holds its baseline -- `tests/test_shipped_refs.py::test_the_repository_holds_its_baseline`

## Origin

Born in this repository, from an outside review of its first version: a reader met references to commands and stories with no way to tell which ones exist.
