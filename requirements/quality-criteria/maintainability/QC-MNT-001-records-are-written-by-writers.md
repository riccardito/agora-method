---
id: QC-MNT-001
title: The session record is written by writers, never by hand
category: maintainability
status: tested
measure: Session status, phase ticks and the index change only through `agora_checks/session.py`; a writer refuses an invalid state and leaves the file unchanged.
---

# QC-MNT-001: The session record is written by writers, never by hand

## Measure

Session status, phase ticks and the index change only through `agora_checks/session.py`; a writer refuses an invalid state and leaves the file unchanged.

## Why

A record edited freehand drifts quietly; a writer that refuses is loud at the moment of the mistake.
