"""Prose-mass ratchet -- a lesson integrates into the rule it changes.

A skill file grows two ways: a rule gets sharper, or an incident gets parked
beside the rule it taught. Only the first is wanted. Per SKILL.md this counts

  record    lines under `## Level history` and `## Notes` -- log-shaped text that
            belongs in the experience sidecar, not the operating file
  lived     `Lived` paragraphs (capital L): an incident written next to a rule
            instead of folded into it
  incident  paragraphs in operating sections that cite a session and run past
            120 words -- a rule carrying its whole story
  total     non-blank lines

and holds `agora/baselines/prose-mass.json` as a ratchet: record, lived and
incident may only fall or hold; total may exceed its baseline by 1 %. The
baseline is rewritten only by `--update-baseline`, which refuses to record growth
unless the skill is named with `--allow-growth` -- visible, never silent.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .common import H2, split_frontmatter

RECORD_SECTIONS = ("level history", "notes")
SLACK = 0.01
INCIDENT_WORDS = 120
AXES = ("record", "lived", "incident", "total")
CITE = re.compile(r"\[\[[^\]\n]+\]\]|\bsession 20\d\d-\d\d-\d\d\b|\blived\b", re.I)
FENCE = re.compile(r"^\s*(```|~~~)")


def measure(text: str) -> dict[str, int]:
    _raw, body = split_frontmatter(text)
    record = lived = incident = total = 0
    section, in_fence, para = "", False, []

    def close_para() -> None:
        nonlocal incident
        chunk = " ".join(para)
        if section not in RECORD_SECTIONS and CITE.search(chunk) and len(chunk.split()) > INCIDENT_WORDS:
            incident += 1
        para.clear()

    for line in body.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        m = None if in_fence else H2.match(line)
        if m:
            close_para()
            section = m.group(1).strip().lower()
        if not line.strip():
            close_para()
            continue
        total += 1
        if section in RECORD_SECTIONS and not m:
            record += 1
        if not in_fence:
            para.append(line.strip())
            if re.search(r"\bLived\b", line) and len(para) == 1:
                lived += 1
    close_para()
    return {"record": record, "lived": lived, "incident": incident, "total": total}


def current(root: Path) -> dict[str, dict[str, int]]:
    return {p.parent.name: measure(p.read_text(encoding="utf-8"))
            for p in sorted(root.glob(".claude/skills/*/SKILL.md"))}


def verdict(name: str, now: dict[str, int], base: dict[str, int]) -> list[str]:
    errs = [f"{name}: {axis} {now[axis]} > baseline {base[axis]}"
            for axis in ("record", "lived", "incident") if now[axis] > base[axis]]
    if now["total"] > base["total"] * (1 + SLACK):
        errs.append(f"{name}: total {now['total']} > baseline {base['total']} + {SLACK:.0%}")
    return errs


def run(root: Path, update: bool = False, allow_growth: list[str] | None = None) -> int:
    path = root / "agora" / "baselines" / "prose-mass.json"
    base = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    now = current(root)
    errs = []
    for name, m in now.items():
        if name not in base:
            if not update:
                errs.append(f"{name}: no baseline (run --update-baseline)")
            continue
        errs += verdict(name, m, base[name])
    if update:
        growing = {e.split(":")[0] for e in errs} - set(allow_growth or [])
        if growing:
            for e in errs:
                if e.split(":")[0] in growing:
                    print(f"[FAIL] {e} -- name it with --allow-growth to record the growth")
            return 1
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(now, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(f"[prose-mass] baseline written for {len(now)} skill(s)")
        return 0
    for e in errs:
        print(f"[FAIL] {e}")
    print(f"[prose-mass] {len(now)} skill(s), {len(errs)} growth(s) over the baseline")
    return 1 if errs else 0
