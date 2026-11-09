"""Secret scan -- no key, token or private key is committed.

Pattern-based, so it finds the shapes it knows. It reads every text file git
would track (the working tree minus the usual tool directories) and fails on a
match. A line that must carry a fake key for a test says so with
`secret-scan: allow` on the same line.
"""
from __future__ import annotations

import re
from pathlib import Path

from .common import rel

PATTERNS = {
    "private key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "Anthropic / OpenAI key": re.compile(r"\bsk-(ant-)?[A-Za-z0-9_-]{24,}\b"),
    "Slack token": re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}\b"),
    "assigned secret": re.compile(
        r"(?i)\b(api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"),
}
SKIP_DIRS = {".git", ".venv", "node_modules", ".pytest_cache", ".ruff_cache", "__pycache__"}
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt", ".cfg", ".ini", ".sh", ""}


def scan_file(path: Path) -> list[tuple[int, str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return []
    hits = []
    for n, line in enumerate(lines, 1):
        if "secret-scan: allow" in line:
            continue
        hits += [(n, kind) for kind, pat in PATTERNS.items() if pat.search(line)]
    return hits


def run(root: Path) -> int:
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES
             and not SKIP_DIRS & set(p.relative_to(root).parts)]
    errs = [(rel(root, p), n, k) for p in sorted(files) for n, k in scan_file(p)]
    for path, n, kind in errs:
        print(f"[FAIL] {path}:{n}: looks like a {kind}")
    print(f"[secrets] {len(files)} file(s), {len(errs)} finding(s)")
    return 1 if errs else 0
