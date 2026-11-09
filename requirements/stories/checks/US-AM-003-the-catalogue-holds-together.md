---
id: US-AM-003
title: The catalogue holds together, and every claim of done names a test
actor: requirements-engineer
feature_area: checks
priority: must-have
status: tested
source: requirements
related_tests:
- tests/test_catalogue.py::test_a_test_reference_must_name_a_real_function
- tests/test_catalogue.py::test_a_valid_catalogue_passes
- tests/test_catalogue.py::test_each_rule_reds_its_planted_fault
- tests/test_catalogue.py::test_the_repository_catalogue_holds
quality_criteria:
- QC-REL-001
glossary_terms:
- GLOSS-CATALOGUE
---

# US-AM-003: The catalogue holds together, and every claim of done names a test

## User Story

As a **requirements engineer**, I want **the catalogue's stories, use cases and quality criteria checked against one another and against the tests they name**, so that **every claim of done in the catalogue is backed by a test that exists**.

## Acceptance Criteria

- [x] a well-formed catalogue passes -- `tests/test_catalogue.py::test_a_valid_catalogue_passes`
- [x] each of the fourteen rules fails on its planted fault -- `tests/test_catalogue.py::test_each_rule_reds_its_planted_fault`
- [x] a test reference must name a file and a function that exist -- `tests/test_catalogue.py::test_a_test_reference_must_name_a_real_function`
- [x] this repository's own catalogue passes -- `tests/test_catalogue.py::test_the_repository_catalogue_holds`

## Origin

Born in this repository. The fourteen rules are distilled from the parent's catalogue lint of 184 rules; see `agora_checks/catalogue.py`. This story specifies the check that checks it.
