---
id: US-AGORA-106
title: Open and close a session through writers, never by hand
actor: developer
feature_area: session
priority: must-have
status: tested
source: requirements
related_tests:
- tests/test_session.py::test_close_refuses_without_a_baton_or_a_retro
- tests/test_session.py::test_open_writes_fields_and_refuses_a_second_open_session
- tests/test_session.py::test_the_demo_is_green
quality_criteria:
- QC-MNT-001
glossary_terms:
- GLOSS-SESSION
---

# US-AGORA-106: Open and close a session through writers, never by hand

## User Story

As a **developer working with an AI agent**, I want **the session file opened and closed by commands that write its fields**, so that **a session's record cannot be left half-written or claim a state it never reached**.

## Acceptance Criteria

- [x] `open` writes the frontmatter from fields and refuses while another session is open -- `tests/test_session.py::test_open_writes_fields_and_refuses_a_second_open_session`
- [x] `close` refuses until the file carries its baton and its retrospective -- `tests/test_session.py::test_close_refuses_without_a_baton_or_a_retro`
- [x] one whole session, start to end, leaves a record every check accepts -- `tests/test_session.py::test_the_demo_is_green`

## Origin

Adapted from the parent's US-AGORA-106, *Session-file and state readers and writers*. The parent's story covers a larger command set; this repository ships `open`, `log`, `tick` and `close` in `agora_checks/session.py`.
