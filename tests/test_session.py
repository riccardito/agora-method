import datetime as dt
import importlib.util
from pathlib import Path

import pytest

from agora_checks import session

REPO = Path(__file__).resolve().parents[1]
DAY = dt.date(2026, 2, 1)


@pytest.fixture
def child(tmp_path: Path) -> Path:
    spec = importlib.util.spec_from_file_location("demo", REPO / "examples" / "demo.py")
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)
    return demo.build_child(tmp_path / "units")


def opened(child: Path) -> Path:
    return session.open_session(child, "work", intent="do it", goal="G",
                                plan=["Phase 1 -- a", "Phase 2 -- b"], date=DAY)


def test_the_baton_of_the_last_closed_session_is_read(child):
    sid, bullets = session.read_baton(child)
    assert sid == "2026-01-05-units-kickoff"
    assert bullets[0].startswith("Goal: Length conversions, criterion 2")


def test_open_writes_fields_and_refuses_a_second_open_session(child):
    p = opened(child)
    text = p.read_text(encoding="utf-8")
    assert "status: open" in text and "- [ ] Phase 1 -- a" in text and "<!--" not in text
    with pytest.raises(session.SessionError, match="still open"):
        session.open_session(child, "other", intent="x", goal="G", plan=["p"], date=DAY)


def test_a_gate_without_a_nod_cannot_be_recorded(child):
    p = opened(child)
    with pytest.raises(session.SessionError, match="nod"):
        session.tick(p, "Phase 1", nod="  ")
    session.tick(p, "Phase 1", nod="go")
    assert '- phase-gate "Phase 1" nod "go"' in p.read_text(encoding="utf-8")
    with pytest.raises(session.SessionError, match="already ticked"):
        session.tick(p, "Phase 1", nod="go")
    with pytest.raises(session.SessionError, match="not in the plan"):
        session.tick(p, "Phase 9", nod="go")


def test_close_refuses_without_a_baton_or_a_retro(child):
    p = opened(child)
    retro = {"worked": "a", "did not": "b", "change": "c"}
    with pytest.raises(session.SessionError, match="baton"):
        session.close(p, "s", baton=[], retro=retro, outcome="o")
    with pytest.raises(session.SessionError, match="missing: change"):
        session.close(p, "s", baton=["next"], retro={**retro, "change": ""}, outcome="o")
    session.close(p, "s", baton=["next"], retro=retro, outcome="done")
    text = p.read_text(encoding="utf-8")
    assert "status: closed" in text
    assert "**Unticked phases:** Phase 1 -- a; Phase 2 -- b" in text
    assert session.read_baton(child) == (p.stem, ["next"])


def test_the_index_is_a_projection_of_the_frontmatter(child):
    opened(child)
    index = session.render_index(child).read_text(encoding="utf-8")
    first = [line for line in index.splitlines() if line.startswith("- [")][0]
    assert first.startswith("- [2026-02-01-work]") and first.endswith("do it — in progress")


def test_the_demo_is_green(capsys):
    spec = importlib.util.spec_from_file_location("demo", REPO / "examples" / "demo.py")
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)
    assert demo.main() == 0
    assert "[agora_checks] 7/7 green" in capsys.readouterr().out


def test_the_child_inherits_the_method_untouched(child):
    for f in ("skills/agora/SKILL.md", "policies/policy-four-eyes.md"):
        assert (child / ".claude" / f).read_bytes() == (REPO / ".claude" / f).read_bytes()
