"""Link integrity -- every relative markdown link in the repository resolves.

A corpus moved out of its parent repository keeps the links that pointed into
it unless something checks. External links (`http:`, `mailto:`) and pure anchors
are not checked; a link's `#fragment` is ignored.
"""
from __future__ import annotations

import re
from pathlib import Path

from .common import rel

LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")
SKIP_DIRS = {".git", ".venv", "node_modules", ".pytest_cache", ".ruff_cache"}


def markdown_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(root).parts))


def broken(root: Path, path: Path) -> list[tuple[int, str]]:
    out, in_fence = [], False
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
        if in_fence:
            continue
        for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            dest = (path.parent / target.split("#", 1)[0]).resolve()
            if not dest.exists():
                out.append((n, target))
    return out


def run(root: Path) -> int:
    files = markdown_files(root)
    errs = [(rel(root, p), n, t) for p in files for n, t in broken(root, p)]
    for path, n, target in errs:
        print(f"[FAIL] {path}:{n}: link target does not exist: {target}")
    print(f"[links] {len(files)} markdown file(s), {len(errs)} broken link(s)")
    return 1 if errs else 0
