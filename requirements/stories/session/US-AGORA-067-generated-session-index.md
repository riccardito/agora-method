---
id: US-AGORA-067
title: The session index is generated, never edited
actor: developer
feature_area: session
priority: should-have
status: tested
source: requirements
related_tests:
- tests/test_session.py::test_the_index_is_a_projection_of_the_frontmatter
quality_criteria:
- QC-MNT-001
glossary_terms:
- GLOSS-SESSION
---

# US-AGORA-067: The session index is generated, never edited

## User Story

As a **developer reading the history**, I want **the index of sessions rendered from each session's own fields**, so that **the index can never disagree with the files it lists**.

## Acceptance Criteria

- [x] the index is a projection of the session frontmatter -- `tests/test_session.py::test_the_index_is_a_projection_of_the_frontmatter`

## Origin

Adapted from the parent's US-AGORA-067, *The record aggregates bounded*: the index generated from a session outcome field.
