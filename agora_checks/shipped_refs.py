"""Shipped references -- what the corpus points at that this repository does not ship.

The operating files came out of a larger project and still name its parts. The
domain check cannot see them, because they are not domain words; a reader can,
because each is a promise with nothing behind it. This check counts them per kind:

  command   a `flask …` CLI command (the parent's substrate; none ships here)
  skill     a `/skill` that has no `.claude/skills/<name>/` directory here
  story     a `US-AGORA-NNN` id from the parent's tracker, unless `requirements/` ships that story
  session   a `session YYYY-MM-DD` citation of a parent session file
  path      a repository path (`app/`, `scripts/`, `tests/`, `docs/`) that does not exist here

and holds `agora/baselines/shipped-refs.json` as a ratchet: each count may fall or
hold, never grow. `--update-baseline` refuses growth unless the kind is named with
`--allow-growth`. `--report` lists the distinct references, most cited first.
`docs/method.md` explains, under "Referenced but not shipped", what they are.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import yaml

from .common import corpus

KINDS = ("command", "skill", "story", "session", "path")
COMMAND = re.compile(r"\bflask (agora (?:write )?[a-z][a-z-]*|[a-z]+ [a-z][a-z-]*)")
STORY = re.compile(r"\bUS-AGORA-\d+")
SESSION = re.compile(r"\bsession (20\d\d-\d\d-\d\d)\b")
PATH = re.compile(r"(?<![\w.<>/-])((?:app|scripts|tests|docs)/[A-Za-z0-9_./-]*[A-Za-z0-9_/])")


def scan(root: Path) -> dict[str, Counter]:
    terms = yaml.safe_load((root / "agora" / "domain-terms.yaml").read_text(encoding="utf-8"))
    shipped = {p.name for p in (root / ".claude" / "skills").iterdir() if p.is_dir()}
    missing = sorted(set(terms.get("skill_names", [])) - shipped, key=len, reverse=True)
    skill = re.compile(r"(?<![\w/`.-])/(" + "|".join(map(re.escape, missing)) + r")\b") if missing else None
    catalogued = {m.group(0) for p in (root / "requirements" / "stories").rglob("US-*.md")
                  for m in [STORY.match(p.name)] if m}
    found = {k: Counter() for k in KINDS}
    for p in corpus(root):
        for line in p.read_text(encoding="utf-8").splitlines():
            found["command"].update("flask " + m for m in COMMAND.findall(line))
            found["story"].update(s for s in STORY.findall(line) if s not in catalogued)
            found["session"].update(SESSION.findall(line))
            if skill:
                found["skill"].update("/" + m for m in skill.findall(line))
            for m in PATH.finditer(line):
                ref, tail = m.group(1), line[m.end():m.end() + 2]
                placeholder = tail.startswith(("<", "-<", "*", "-*"))  # `feature-<slug>.md`, `RP-*.md`
                if not placeholder and not (root / ref.rstrip("/")).exists():
                    found["path"][ref] += 1
    return found


def run(root: Path, update: bool = False, allow_growth: list[str] | None = None, report: bool = False) -> int:
    path = root / "agora" / "baselines" / "shipped-refs.json"
    base = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    found = scan(root)
    now = {k: sum(found[k].values()) for k in KINDS}
    if report:
        for k in KINDS:
            top = ", ".join(f"{ref} ({n})" for ref, n in found[k].most_common(8))
            print(f"  {k:8} {now[k]:5} citations, {len(found[k]):4} distinct -- {top}")
    grown = [k for k in KINDS if k in base and now[k] > base[k]]
    if update:
        refused = [k for k in grown if k not in (allow_growth or [])]
        for k in refused:
            print(f"[FAIL] {k}: {now[k]} > baseline {base[k]} -- name it with --allow-growth to record it")
        if refused:
            return 1
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(now, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"[shipped-refs] baseline written: {now}")
        return 0
    errs = [f"{k}: {now[k]} references, baseline {base[k]} -- the count may only fall" for k in grown]
    errs += [f"{k}: no baseline (run --update-baseline)" for k in KINDS if k not in base]
    for e in errs:
        print(f"[FAIL] {e}")
    fell = [f"{k} {base[k]}->{now[k]}" for k in KINDS if k in base and now[k] < base[k]]
    print(f"[shipped-refs] {sum(now.values())} references to unshipped parts "
          f"({', '.join(f'{k} {now[k]}' for k in KINDS)}), {len(errs)} growth(s)"
          + (f"; fell: {', '.join(fell)} -- tighten with --update-baseline" if fell else ""))
    return 1 if errs else 0
