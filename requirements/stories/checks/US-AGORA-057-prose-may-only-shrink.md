---
id: US-AGORA-057
title: Skill prose may only shrink, unless a growth is named
actor: maintainer
feature_area: checks
priority: should-have
status: tested
source: gap-analysis
related_tests:
- tests/test_prose_mass.py::test_a_long_cited_paragraph_is_an_incident
- tests/test_prose_mass.py::test_growth_reds_and_the_baseline_refuses_it_unless_named
- tests/test_prose_mass.py::test_measure_counts_each_axis
- tests/test_prose_mass.py::test_shrinking_always_passes
- tests/test_prose_mass.py::test_the_repository_holds_its_baseline
quality_criteria:
- QC-REL-001
glossary_terms:
- GLOSS-RATCHET
---

# US-AGORA-057: Skill prose may only shrink, unless a growth is named

## User Story

As a **maintainer of skills that learn from every session**, I want **each skill's prose measured against a baseline that may only fall**, so that **a lesson is integrated into the skill rather than appended until nobody reads it**.

## Acceptance Criteria

- [x] each axis is counted -- `tests/test_prose_mass.py::test_measure_counts_each_axis`
- [x] a long cited paragraph is counted as an incident -- `tests/test_prose_mass.py::test_a_long_cited_paragraph_is_an_incident`
- [x] growth fails, and the baseline refuses it unless the skill is named -- `tests/test_prose_mass.py::test_growth_reds_and_the_baseline_refuses_it_unless_named`
- [x] shrinking always passes -- `tests/test_prose_mass.py::test_shrinking_always_passes`
- [x] the repository holds its baseline -- `tests/test_prose_mass.py::test_the_repository_holds_its_baseline`

## Origin

Adapted from the parent's US-AGORA-057, *learn integrates or refuses*, where a lesson that would grow a skill must replace a weaker rule instead.
