---
id: US-AM-002
title: Links resolve and no secret is committed
actor: maintainer
feature_area: checks
priority: must-have
status: tested
source: gap-analysis
related_tests:
- tests/test_links_and_secrets.py::test_a_broken_relative_link_is_found_and_code_is_skipped
- tests/test_links_and_secrets.py::test_known_secret_shapes_are_found
- tests/test_links_and_secrets.py::test_the_allow_marker_silences_one_line
- tests/test_links_and_secrets.py::test_the_repository_has_no_secret
- tests/test_links_and_secrets.py::test_the_repository_links_resolve
quality_criteria:
- QC-REL-001
glossary_terms:
- GLOSS-CHECK
---

# US-AM-002: Links resolve and no secret is committed

## User Story

As a **maintainer of a public repository**, I want **every relative link checked and every file scanned for known secret shapes**, so that **a moved corpus does not point into nowhere and nothing private leaks**.

## Acceptance Criteria

- [x] a broken relative link is found, and code is skipped -- `tests/test_links_and_secrets.py::test_a_broken_relative_link_is_found_and_code_is_skipped`
- [x] the repository's links resolve -- `tests/test_links_and_secrets.py::test_the_repository_links_resolve`
- [x] known secret shapes are found -- `tests/test_links_and_secrets.py::test_known_secret_shapes_are_found`
- [x] an allow marker silences one line, and only that one -- `tests/test_links_and_secrets.py::test_the_allow_marker_silences_one_line`
- [x] the repository holds no secret -- `tests/test_links_and_secrets.py::test_the_repository_has_no_secret`

## Origin

Born in this repository: the export from the parent left 117 links pointing at files it does not ship.
