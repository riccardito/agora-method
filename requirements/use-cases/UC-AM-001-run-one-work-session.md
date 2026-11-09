---
id: UC-AM-001
title: Run one work session
actor: developer
status: tested
stories:
- US-AGORA-106
- US-AGORA-097
- US-AGORA-035
- US-AGORA-067
quality_criteria:
- QC-MNT-001
- QC-POR-001
---

# UC-AM-001: Run one work session

## Goal

A developer and an AI agent do one bounded piece of work and leave a record the next session can trust.

## Main flow

1. The developer opens a session: intent, goal and phase plan are written as fields (US-AGORA-106).
2. The agent reads the last session's baton and starts from it (US-AGORA-035).
3. Phase by phase, the agent proposes; the developer nods; the tick and the nod are one write (US-AGORA-097).
4. The agent closes the session with a summary, a retrospective and the next baton (US-AGORA-106).
5. The index is regenerated from the session files (US-AGORA-067).

## Alternative flows

- **No nod at a gate:** the tick is refused; the phase stays open.
- **A second session while one is open:** refused; the open one closes first.
- **Close without a baton or a retrospective:** refused; the file is unchanged.
