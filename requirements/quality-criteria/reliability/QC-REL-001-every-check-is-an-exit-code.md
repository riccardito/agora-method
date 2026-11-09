---
id: QC-REL-001
title: Every check is a script whose exit code is the verdict
category: reliability
status: tested
measure: Each of the eight checks exits non-zero on a planted fault and zero on the repository; CI runs them as one command.
---

# QC-REL-001: Every check is a script whose exit code is the verdict

## Measure

Each of the eight checks exits non-zero on a planted fault and zero on the repository; CI runs them as one command.

## Why

A rule a person must remember is not enforced. A rule a script checks is enforced on every push.
