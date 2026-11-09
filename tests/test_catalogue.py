"""The catalogue check: a valid catalogue passes, and each rule fails on its own planted fault."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from agora_checks import catalogue

STORY = {"id": "US-AB-001", "title": "t", "actor": "developer", "feature_area": "a", "priority": "must-have",
         "status": "tested", "source": "requirements", "related_tests": ["tests/test_x.py::test_it"],
         "quality_criteria": ["QC-REL-001"], "glossary_terms": ["GLOSS-ONE"]}
BODY = ("## User Story\n\nAs a developer, I want a thing, so that it helps.\n\n"
        "## Acceptance Criteria\n\n- [x] done\n")
CASE = {"id": "UC-AB-001", "title": "u", "actor": "developer", "status": "tested", "stories": ["US-AB-001"]}
QC = {"id": "QC-REL-001", "title": "q", "category": "reliability", "status": "tested", "measure": "m"}


def write(root: Path, rel: str, fm: dict | None, body: str = "") -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    head = "" if fm is None else "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n"
    p.write_text(head + body, encoding="utf-8")
    return p


def make(root: Path, story: dict | None = None, body: str = BODY, case: dict | None = None) -> Path:
    write(root, "requirements/actors.md", None, "### developer\n")
    write(root, "requirements/glossary.md", None, "### GLOSS-ONE\n")
    write(root, "tests/test_x.py", None, "def test_it():\n    pass\n")
    write(root, "requirements/quality-criteria/QC-REL-001-q.md", QC)
    s = story or STORY
    write(root, f"requirements/stories/a/{s.get('id', 'none')}-t.md", s, body)
    write(root, "requirements/use-cases/UC-AB-001-u.md", case or CASE)
    return root


def rules(root: Path) -> set[str]:
    return {r for r, _f, _m in catalogue.problems(catalogue.load(root))}


def test_a_valid_catalogue_passes(tmp_path):
    assert rules(make(tmp_path)) == set()


PLANTED = {
    "C01": dict(story={**STORY, "id": "US-x-1"}),
    "C03": None,  # built below: two files, one id
    "C02": None,
    "C04": dict(story={k: v for k, v in STORY.items() if k != "source"}),
    "C05": dict(story={**STORY, "status": "done"}),
    "C06": dict(story={**STORY, "actor": "stranger"}),
    "C07": dict(body=BODY.replace("so that", "because")),
    "C08": dict(body=BODY.replace("- [x] done", "done")),
    "C09": dict(story={**STORY, "related_tests": ["tests/test_x.py::test_missing"]}),
    "C10": dict(story={**STORY, "related_tests": []}),
    "C11": dict(body=BODY.replace("- [x] done", "- [x] done\n- [ ] not yet")),
    "C12": dict(story={**STORY, "glossary_terms": ["GLOSS-NONE"]}),
    "C13": dict(case={**CASE, "stories": []}),
    "C14": dict(case={**CASE, "status": "draft"}),
}


@pytest.mark.parametrize("rule", sorted(PLANTED))
def test_each_rule_reds_its_planted_fault(tmp_path, rule):
    if rule == "C02":
        make(tmp_path)
        stories = tmp_path / "requirements/stories/a"
        (stories / "US-AB-001-t.md").rename(stories / "story.md")
    elif rule == "C03":
        make(tmp_path)
        write(tmp_path, "requirements/stories/b/US-AB-001-again.md", STORY, BODY)
    else:
        make(tmp_path, **PLANTED[rule])
    assert rule in rules(tmp_path)


def test_a_test_reference_must_name_a_real_function(tmp_path):
    make(tmp_path)
    assert catalogue.resolve_test(tmp_path, "tests/test_x.py::test_it") is None
    assert "no test named" in catalogue.resolve_test(tmp_path, "tests/test_x.py::test_gone")
    assert "does not exist" in catalogue.resolve_test(tmp_path, "tests/test_nowhere.py")


def test_the_repository_catalogue_holds(repo, capsys):
    assert catalogue.run(repo) == 0
    out = capsys.readouterr().out
    assert "0 problem(s)" in out and " 0 stories" not in out
