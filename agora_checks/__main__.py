"""`python -m agora_checks <check> [options]` -- one entry point for every check.

Each check prints `[FAIL] ...` lines and one summary line, and its exit code is the
verdict. `all` runs every check and exits non-zero if any failed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import (
    catalogue,
    domain_share,
    frontmatter,
    links,
    prose_mass,
    record_consistency,
    secrets,
    shipped_refs,
)
from .common import find_root

CHECKS = {
    "frontmatter": lambda root, a: frontmatter.run(root),
    "record-consistency": lambda root, a: record_consistency.run(root, fix=a.fix),
    "prose-mass": lambda root, a: prose_mass.run(root, update=a.update_baseline,
                                                 allow_growth=a.allow_growth or []),
    "domain-share": lambda root, a: domain_share.run(root, report=a.report),
    "shipped-refs": lambda root, a: shipped_refs.run(root, update=a.update_baseline,
                                                     allow_growth=a.allow_growth or [], report=a.report),
    "links": lambda root, a: links.run(root),
    "secrets": lambda root, a: secrets.run(root),
    "catalogue": lambda root, a: catalogue.run(root),
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="agora_checks", description=__doc__)
    ap.add_argument("check", choices=[*CHECKS, "all"])
    ap.add_argument("--root", type=Path, help="repository root (default: nearest .claude/ above cwd)")
    ap.add_argument("--fix", action="store_true", help="record-consistency: rewrite generated blocks")
    ap.add_argument("--report", action="store_true",
                    help="domain-share: the per-file table; shipped-refs: the distinct references")
    ap.add_argument("--update-baseline", action="store_true",
                    help="prose-mass / shipped-refs: record the current counts")
    ap.add_argument("--allow-growth", action="append", metavar="NAME",
                    help="prose-mass: a skill, shipped-refs: a kind, whose baseline may grow (repeatable)")
    a = ap.parse_args(argv)
    root = (a.root or find_root()).resolve()
    names = list(CHECKS) if a.check == "all" else [a.check]
    failed = [n for n in names if CHECKS[n](root, a) != 0]
    if a.check == "all":
        print(f"[agora_checks] {len(names) - len(failed)}/{len(names)} green"
              + (f" -- red: {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
