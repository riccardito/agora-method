# Policy breaches ledger

> Append-only. One line per **confirmed** policy breach, confirmed at
> `/agora --end`'s close-out paper gate (the finding survives from the retired
> step 2.7) — only user-confirmed violations get a line, and the line is
> appended **via `flask agora write breach`** (US-AGORA-048's write path:
> anchored below the marker, date order + format enforced by the writer —
> never a freehand edit). This is the **measure-don't-level** answer to policy
> enforcement (WS2, US-AGORA-006 / RP-AGORA-003): a policy people keep
> breaking is badly worded or badly placed, not a policy people are bad at.
> The most-breached policies are the **rewording queue**.
>
> **Counting note (2026-08-14, US-AGORA-051) — the confound is retired.** While
> the append was a freehand edit, a low breach count was undecidable between
> *discipline holds* and *the append was forgotten* (structural
> under-counting). The append being a command invoked at `--end`'s dispatch —
> behind the same 4-eye confirm — removes the structural half: from 2026-08-14
> forward, a session with no line is a session with no confirmed breach, and
> the counts carry signal.
>
> `US-AGORA-011` computes the scorecard on top of this ledger (citations +
> breach-count + last-breach-recency → a `needs-rewording` flag) and surfaces it
> via `/level --board --policies`.
>
> **Format** (newest at the top):
>
> ```
> YYYY-MM-DD · policy-<slug> · [[session-id]] · <one clause: what broke>
> ```
>
> Not every finding is a breach — only a *confirmed violation of a named
> policy*. An over-eager ledger is as useless as none. When a session has no
> confirmed breaches, nothing is appended (silence is correct).

<!-- Breach lines land below this line, newest first. -->
