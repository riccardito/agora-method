from agora_checks import prose_mass

SKILL = """---
name: s
---
## Steps

A rule.

Lived 2026-01-05: a story told beside the rule.

## Level history

- 2026-01-05 promoted
- 2026-01-06 patched
"""


def test_measure_counts_each_axis():
    m = prose_mass.measure(SKILL)
    assert m == {"record": 2, "lived": 1, "incident": 0, "total": 6}


def test_a_long_cited_paragraph_is_an_incident():
    long_para = "word " * 130 + "(lived session 2026-01-05)"
    m = prose_mass.measure(f"## Steps\n\n{long_para}\n")
    assert m["incident"] == 1


def test_growth_reds_and_the_baseline_refuses_it_unless_named(mini, capsys):
    skill = mini / ".claude/skills/learn/SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\nLived 2026-02-01: another story.\n",
                     encoding="utf-8")
    assert prose_mass.run(mini) == 1
    assert "learn: lived" in capsys.readouterr().out
    assert prose_mass.run(mini, update=True) == 1
    assert prose_mass.run(mini, update=True, allow_growth=["learn"]) == 0
    assert prose_mass.run(mini) == 0


def test_shrinking_always_passes(mini):
    skill = mini / ".claude/skills/level/SKILL.md"
    lines = skill.read_text(encoding="utf-8").splitlines()
    skill.write_text("\n".join(lines[: len(lines) // 2]) + "\n", encoding="utf-8")
    assert prose_mass.run(mini) == 0


def test_the_repository_holds_its_baseline(repo):
    assert prose_mass.run(repo) == 0
