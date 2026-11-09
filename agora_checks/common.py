"""Shared helpers: repository root, frontmatter split, markdown sections."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
H2 = re.compile(r"^## +(.+?)\s*$", re.M)


def find_root(start: Path | None = None) -> Path:
    """The nearest ancestor holding a `.claude/` directory."""
    here = (start or Path.cwd()).resolve()
    for p in (here, *here.parents):
        if (p / ".claude").is_dir():
            return p
    raise SystemExit(f"no .claude/ directory above {here}")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (raw frontmatter, body). Raw is None when the file has none."""
    m = FRONTMATTER.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def load_frontmatter(text: str) -> dict | None:
    raw, _body = split_frontmatter(text)
    if raw is None:
        return None
    data = yaml.safe_load(raw)
    return data if isinstance(data, dict) else None


def sections(body: str) -> dict[str, str]:
    """Map each `## ` heading to the text below it, up to the next `## `."""
    out: dict[str, str] = {}
    marks = list(H2.finditer(body))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        out[m.group(1).strip()] = body[m.end():end]
    return out


def corpus(root: Path, pattern: str = ".claude/**/*.md") -> list[Path]:
    return sorted(p for p in root.glob(pattern) if p.is_file())


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()
