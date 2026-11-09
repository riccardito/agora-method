"""Frontmatter lint -- the static shape of skill and policy files (policy-skill-authoring).

Skills (`.claude/skills/<name>/SKILL.md`):
  * the frontmatter parses as strict YAML and is a mapping with a `name`
  * prose scalars that YAML would misread are quoted (Rule 2)
  * `level` is draft / used / hardened / reference (missing = draft)
  * `role` from used, `epithet` from hardened (Rule 3)
  * an `experience.md` sidecar carrying `xp_total` from used (Rule 3)
  * at least one `## ` heading; from hardened a `## When NOT to use` section and a
    `## Claims at this level` section with three or more items; at reference an
    `## Identity` section (Rule 4)
Policies (`.claude/policies/policy-*.md`):
  * `status` is draft / active / deprecated, `domain` is in the enum (Rule 6)
  * every `related_skills` entry names a skill that exists
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from .common import load_frontmatter, rel, sections, split_frontmatter

LEVELS = ("draft", "used", "hardened", "reference")
POLICY_STATUS = ("draft", "active", "deprecated")
POLICY_DOMAINS = ("discipline", "authoring", "ui", "i18n", "testing", "migration", "leveling")
PROSE_KEYS = ("name", "description", "argument-hint", "title", "role", "epithet")
ITEM = re.compile(r"^\s*(\d+\.|[-*])\s+\S", re.M)


def risky(value: str) -> str | None:
    """Why an UNQUOTED scalar would be misread by a strict YAML parser, or None."""
    if not value or value[0] in "\"'":
        return None
    checks = [
        (": " in value, "contains ': '"),
        (re.search(r"\s#", value) is not None, "contains ' #'"),
        (value[0] in "[{", "starts with [ or {"),
        (re.search(r".\s[|>]\s", value) is not None, "has a mid-string | or >"),
        ("<" in value or ">" in value, "contains < or >"),
        (value[0] in "&*!%@`", "starts with a reserved indicator"),
    ]
    return next((why for bad, why in checks if bad), None)


def lint_scalars(path: str, raw: str) -> list[str]:
    out = []
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s+(.*\S)\s*$", line)
        if m and m.group(1) in PROSE_KEYS:
            why = risky(m.group(2))
            if why:
                out.append(f"{path}: `{m.group(1)}` must be double-quoted -- it {why}")
    return out


def lint_skill(root: Path, skill_md: Path) -> list[str]:
    path = rel(root, skill_md)
    text = skill_md.read_text(encoding="utf-8")
    raw, body = split_frontmatter(text)
    if raw is None:
        return [f"{path}: no frontmatter block"]
    errs = lint_scalars(path, raw)
    try:
        fm = load_frontmatter(text)
    except yaml.YAMLError as e:
        return errs + [f"{path}: frontmatter does not parse: {e.__class__.__name__}"]
    if fm is None:
        return errs + [f"{path}: frontmatter is not a mapping"]
    if not fm.get("name"):
        errs.append(f"{path}: frontmatter has no `name`")
    level = fm.get("level", "draft")
    if level not in LEVELS:
        return errs + [f"{path}: level {level!r} is not one of {', '.join(LEVELS)}"]
    rank = LEVELS.index(level)
    if rank >= 1 and not fm.get("role"):
        errs.append(f"{path}: `role` is required at {level}")
    if rank >= 2 and not fm.get("epithet"):
        errs.append(f"{path}: `epithet` is required at {level}")
    if rank >= 1:
        side = skill_md.parent / "experience.md"
        side_fm = load_frontmatter(side.read_text(encoding="utf-8")) if side.exists() else None
        if not side_fm or "xp_total" not in side_fm:
            errs.append(f"{path}: an experience.md sidecar with `xp_total` is required at {level}")
    secs = sections(body)
    if not secs:
        errs.append(f"{path}: the body has no `## ` heading")
    if rank >= 2:
        if not any(h.lower().startswith("when not to use") for h in secs):
            errs.append(f"{path}: a `## When NOT to use` section is required at {level}")
        claims = next((v for h, v in secs.items() if h.lower().startswith("claims at this level")), None)
        if claims is None:
            errs.append(f"{path}: a `## Claims at this level` section is required at {level}")
        elif len(ITEM.findall(claims)) < 3:
            errs.append(f"{path}: `## Claims at this level` names fewer than 3 claims")
    if rank >= 3 and not any(h.lower().startswith("identity") for h in secs):
        errs.append(f"{path}: an `## Identity` section is required at reference")
    return errs


def lint_policy(root: Path, policy: Path, skills: set[str]) -> list[str]:
    path = rel(root, policy)
    text = policy.read_text(encoding="utf-8")
    raw, _body = split_frontmatter(text)
    if raw is None:
        return [f"{path}: no frontmatter block"]
    errs = lint_scalars(path, raw)
    try:
        fm = load_frontmatter(text)
    except yaml.YAMLError as e:
        return errs + [f"{path}: frontmatter does not parse: {e.__class__.__name__}"]
    if fm is None:
        return errs + [f"{path}: frontmatter is not a mapping"]
    if fm.get("status") not in POLICY_STATUS:
        errs.append(f"{path}: status {fm.get('status')!r} is not one of {', '.join(POLICY_STATUS)}")
    if fm.get("domain") not in POLICY_DOMAINS:
        errs.append(f"{path}: domain {fm.get('domain')!r} is not one of {', '.join(POLICY_DOMAINS)}")
    for s in fm.get("related_skills") or []:
        if s not in skills:
            errs.append(f"{path}: related_skills names {s!r}, which is not a skill here")
    return errs


def run(root: Path) -> int:
    skill_files = sorted(root.glob(".claude/skills/*/SKILL.md"))
    skills = {p.parent.name for p in skill_files}
    errs: list[str] = []
    for p in skill_files:
        errs += lint_skill(root, p)
    policies = sorted(root.glob(".claude/policies/policy-*.md"))
    for p in policies:
        errs += lint_policy(root, p, skills)
    for e in errs:
        print(f"[FAIL] {e}")
    print(f"[frontmatter] {len(skill_files)} skill(s), {len(policies)} policy file(s), {len(errs)} error(s)")
    return 1 if errs else 0
