from __future__ import annotations

import shutil
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def repo() -> Path:
    return REPO


@pytest.fixture
def mini(tmp_path: Path) -> Path:
    """A copy of the repository's method layer to mutate."""
    for part in (".claude", "agora", "docs", "requirements"):
        shutil.copytree(REPO / part, tmp_path / part)
    for f in ("CLAUDE.md", "README.md"):
        shutil.copy(REPO / f, tmp_path / f)
    return tmp_path
