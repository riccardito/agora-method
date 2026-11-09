from pathlib import Path

import pytest

from agora_checks import frontmatter


@pytest.mark.parametrize("value,bad", [
    ("the mayor", False),
    ('"a: quoted value"', False),
    ("a value: with a colon", True),
    ("a value #with a hash", True),
    ("[looks like a list]", True),
    ("one | two", True),
    ("less <than> more", True),
    ("@handle", True),
])
def test_risky_scalars(value, bad):
    assert (frontmatter.risky(value) is not None) is bad


def write_skill(root: Path, name: str, fm: str, body: str, xp: bool = True) -> Path:
    d = root / ".claude" / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")
    if xp:
        (d / "experience.md").write_text("---\nskill: x\nxp_total: 0\n---\n", encoding="utf-8")
    return d / "SKILL.md"


def test_a_draft_skill_needs_only_a_heading(tmp_path):
    p = write_skill(tmp_path, "s", "name: s", "## Steps\n", xp=False)
    assert frontmatter.lint_skill(tmp_path, p) == []


def test_used_needs_role_and_sidecar(tmp_path):
    p = write_skill(tmp_path, "s", "name: s\nlevel: used", "## Steps\n", xp=False)
    errs = " ".join(frontmatter.lint_skill(tmp_path, p))
    assert "`role` is required" in errs and "experience.md" in errs


def test_hardened_needs_epithet_boundary_and_three_claims(tmp_path):
    body = "## Steps\n\n## Claims at this level\n\n1. one\n2. two\n"
    p = write_skill(tmp_path, "s", 'name: s\nlevel: hardened\nrole: "r"', body)
    errs = " ".join(frontmatter.lint_skill(tmp_path, p))
    assert "`epithet` is required" in errs
    assert "When NOT to use" in errs
    assert "fewer than 3 claims" in errs


def test_unquoted_colon_in_a_description_is_caught(tmp_path):
    p = write_skill(tmp_path, "s", "name: s\ndescription: does X: then Y", "## Steps\n", xp=False)
    assert any("must be double-quoted" in e for e in frontmatter.lint_skill(tmp_path, p))


def test_policy_enums_and_related_skills(tmp_path):
    d = tmp_path / ".claude" / "policies"
    d.mkdir(parents=True)
    p = d / "policy-x.md"
    p.write_text("---\nname: x\nstatus: live\ndomain: cooking\nrelated_skills: [ghost]\n---\n## TL;DR\n",
                 encoding="utf-8")
    errs = " ".join(frontmatter.lint_policy(tmp_path, p, skills={"agora"}))
    assert "status 'live'" in errs and "domain 'cooking'" in errs and "'ghost'" in errs


def test_the_repository_is_clean(repo):
    assert frontmatter.run(repo) == 0
