---
id: US-UNITS-001
title: Convert the four imperial lengths exactly
actor: user
feature_area: lengths
priority: must-have
status: approved
source: user-request
related_tests: []
quality_criteria: []
glossary_terms: [GLOSS-EXACT]
---

# US-UNITS-001: Convert the four imperial lengths exactly

## User Story

As a **user**, I want **inches, feet, yards and miles converted to metres and back from their
defining factors**, so that **a round trip returns the number I started with**.

## Acceptance Criteria

- [ ] each of in, ft, yd and mi converts with its exact international definition (1 in = 0.0254 m)
- [ ] metres -> unit -> metres returns the start value within 1e-12
- [ ] the display rounds to 6 significant digits and says that the stored value is exact

## Origin

The child's first Goal, *Length conversions*, criterion 2. The story stays `approved` until a
test names it: the catalogue check refuses `implemented` without one (rule C10).
