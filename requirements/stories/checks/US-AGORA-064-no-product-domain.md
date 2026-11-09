---
id: US-AGORA-064
title: The method carries no product domain
actor: maintainer
feature_area: checks
priority: must-have
status: tested
source: strategy-paper
related_tests:
- tests/test_domain_share.py::test_a_planted_term_reds_the_check
- tests/test_domain_share.py::test_first_class_wins
- tests/test_domain_share.py::test_private_terms_are_matched_by_hash
- tests/test_domain_share.py::test_strict_mode_sees_a_domain_word_behind_an_agora_word
- tests/test_domain_share.py::test_the_repository_has_no_domain_hit
quality_criteria:
- QC-REL-001
- QC-POR-001
glossary_terms:
- GLOSS-DOMAIN-SHARE
---

# US-AGORA-064: The method carries no product domain

## User Story

As a **maintainer publishing the method**, I want **every line of the corpus classified, and any line naming the parent product's domain to fail**, so that **the method can be copied into another project without carrying the first one along**.

## Acceptance Criteria

- [x] a line takes the first class that matches -- `tests/test_domain_share.py::test_first_class_wins`
- [x] strict mode sees a domain word behind a method word -- `tests/test_domain_share.py::test_strict_mode_sees_a_domain_word_behind_an_agora_word`
- [x] private product names are matched by hash, never written -- `tests/test_domain_share.py::test_private_terms_are_matched_by_hash`
- [x] a planted domain term fails the check -- `tests/test_domain_share.py::test_a_planted_term_reds_the_check`
- [x] the repository has no domain hit -- `tests/test_domain_share.py::test_the_repository_has_no_domain_hit`

## Origin

Adapted from the parent's US-AGORA-064, *the domain-tag pass and the child-pipeline contract sketch*. The raw copy measured 1.06 % domain lines; the published corpus measures 0.0 %.
