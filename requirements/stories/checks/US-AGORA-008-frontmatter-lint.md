---
id: US-AGORA-008
title: Skill and policy frontmatter is parsed strictly and held to its level
actor: maintainer
feature_area: checks
priority: must-have
status: tested
source: gap-analysis
related_tests:
- tests/test_frontmatter.py::test_hardened_needs_epithet_boundary_and_three_claims
- tests/test_frontmatter.py::test_policy_enums_and_related_skills
- tests/test_frontmatter.py::test_risky_scalars
- tests/test_frontmatter.py::test_the_repository_is_clean
- tests/test_frontmatter.py::test_unquoted_colon_in_a_description_is_caught
- tests/test_frontmatter.py::test_used_needs_role_and_sidecar
quality_criteria:
- QC-REL-001
glossary_terms:
- GLOSS-CHECK
---

# US-AGORA-008: Skill and policy frontmatter is parsed strictly and held to its level

## User Story

As a **maintainer of the skills and policies**, I want **every frontmatter block parsed strictly and held to the shape its level requires**, so that **a file the editor cannot parse, or a skill claiming a level it has not earned, fails the build**.

## Acceptance Criteria

- [x] risky scalars must be quoted -- `tests/test_frontmatter.py::test_risky_scalars`
- [x] an unquoted colon in a description is caught -- `tests/test_frontmatter.py::test_unquoted_colon_in_a_description_is_caught`
- [x] a `used` skill needs a role and an experience sidecar -- `tests/test_frontmatter.py::test_used_needs_role_and_sidecar`
- [x] a `hardened` skill names its boundaries and at least three claims -- `tests/test_frontmatter.py::test_hardened_needs_epithet_boundary_and_three_claims`
- [x] a policy's domain comes from the list, and its related skills exist -- `tests/test_frontmatter.py::test_policy_enums_and_related_skills`
- [x] the repository passes -- `tests/test_frontmatter.py::test_the_repository_is_clean`

## Origin

Adapted from the parent's US-AGORA-008, which added the policy `domain:` field and its lint. Here the story covers the whole frontmatter check.
