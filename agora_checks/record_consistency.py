"""Record consistency -- one fact, one home, one direction.

Every fact that lives in more than one file is declared in
`agora/record-consistency.yaml`: which copy is the SOURCE, which copies are
DERIVED, and how they derive. A derived copy is the text between
`<!-- rc:<id> -->` and `<!-- /rc:<id> -->` in its target file.

  generated  the block equals the generator's output from the source; `--fix`
             rewrites it
  verbatim   the block equals a section of the source (links reduced to their
             text, whitespace collapsed); never auto-fixed -- edit the source,
             then re-derive the mirror by hand, so the edit is read twice
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from .common import load_frontmatter, sections, split_frontmatter

LINK = re.compile(r"\[([^\]\n]+)\]\([^)\s]+\)")


def block_re(fact_id: str) -> re.Pattern:
    """The block between the markers; an empty block (adjacent markers) matches too."""
    fid = re.escape(fact_id)
    return re.compile(rf"(<!-- rc:{fid} -->\n)(.*?)(\n?<!-- /rc:{fid} -->)", re.S)


def normalise(text: str) -> str:
    return " ".join(LINK.sub(r"\1", text).split())


def gen_tier_table(source: Path) -> str:
    tiers = yaml.safe_load(source.read_text(encoding="utf-8"))["tiers"]
    rows = ["| Tier | Granularity | Closes with |", "|---|---|---|"]
    rows += [f"| {t['cell']} | {t['granularity']} | {t['closes_with']} |" for t in tiers]
    return "\n".join(rows)


def gen_skill_table(source: Path) -> str:
    """One row per skill directory: name, level, role, epithet -- read from frontmatter."""
    rows = ["| Skill | Level | Role | Epithet |", "|---|---|---|---|"]
    for p in sorted(source.glob("*/SKILL.md")):
        fm = load_frontmatter(p.read_text(encoding="utf-8")) or {}
        rows.append(f"| [`/{p.parent.name}`]({p.parent.name}/SKILL.md) | {fm.get('level', 'draft')} "
                    f"| {fm.get('role', '')} | {fm.get('epithet', '')} |")
    return "\n".join(rows)


def gen_policy_table(source: Path) -> str:
    """One row per policy file: name, domain, status, title -- read from frontmatter."""
    rows = ["| Policy | Domain | Status | Title |", "|---|---|---|---|"]
    for p in sorted(source.glob("policy-*.md")):
        fm = load_frontmatter(p.read_text(encoding="utf-8")) or {}
        rows.append(f"| [`{p.stem}`]({p.name}) | {fm.get('domain', '')} | {fm.get('status', '')} "
                    f"| {fm.get('title', '')} |")
    return "\n".join(rows)


GENERATORS = {"tier_table": gen_tier_table, "skill_table": gen_skill_table,
              "policy_table": gen_policy_table}


def source_section(source: Path, heading: str) -> str:
    _raw, body = split_frontmatter(source.read_text(encoding="utf-8"))
    secs = sections(body)
    if heading not in secs:
        raise KeyError(f"{source.name} has no `## {heading}` section")
    return secs[heading].strip()


def run(root: Path, fix: bool = False) -> int:
    registry = yaml.safe_load((root / "agora" / "record-consistency.yaml").read_text(encoding="utf-8"))
    errs, fixed, checked = [], 0, 0
    for fact in registry["facts"]:
        fid, mode = fact["id"], fact["mode"]
        source = root / fact["source"]
        if mode == "generated":
            want = GENERATORS[fact["generator"]](source)
        elif mode == "verbatim":
            want = source_section(source, fact["heading"])
        else:
            errs.append(f"{fid}: unknown mode {mode!r}")
            continue
        for target in fact["targets"]:
            checked += 1
            tpath = root / target
            text = tpath.read_text(encoding="utf-8")
            m = block_re(fid).search(text)
            if not m:
                errs.append(f"{fid}: {target} has no rc:{fid} block")
                continue
            if mode == "generated" and m.group(2) != want:
                if fix:
                    new = f"{m.group(1)}{want}\n<!-- /rc:{fid} -->"
                    tpath.write_text(text[:m.start()] + new + text[m.end():], encoding="utf-8", newline="\n")
                    fixed += 1
                else:
                    errs.append(f"{fid}: {target} differs from the generator (run with --fix)")
            elif mode == "verbatim" and normalise(m.group(2)) != normalise(want):
                errs.append(f"{fid}: {target} differs from {fact['source']} `## {fact['heading']}` "
                            "(edit the source, re-derive the mirror)")
    for e in errs:
        print(f"[FAIL] {e}")
    print(f"[record-consistency] {len(registry['facts'])} fact(s), {checked} copy(ies), "
          f"{len(errs)} drift(s)" + (f", {fixed} rewritten" if fixed else ""))
    return 1 if errs else 0
