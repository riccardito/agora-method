from agora_checks import shipped_refs


def append(mini, text: str) -> None:
    p = mini / ".claude/skills/learn/SKILL.md"
    p.write_text(p.read_text(encoding="utf-8") + "\n" + text + "\n", encoding="utf-8")


def test_each_kind_is_counted(mini):
    before = {k: sum(v.values()) for k, v in shipped_refs.scan(mini).items()}
    append(mini, "Run `flask agora frobnicate`, then /fixbug, per US-AGORA-999 (session 2026-01-02); "
                 "see `scripts/checks/nowhere.py`.")
    after = {k: sum(v.values()) for k, v in shipped_refs.scan(mini).items()}
    assert {k: after[k] - before[k] for k in after} == {
        "command": 1, "skill": 1, "story": 1, "session": 1, "path": 1}


def test_shipped_things_and_placeholders_are_not_counted(mini):
    before = shipped_refs.scan(mini)
    append(mini, "Run /learn and /agora; read `docs/wiki/feature-<slug>.md` and `docs/x/RP-*.md`; "
                 "the code is in `agora_checks/`.")
    assert shipped_refs.scan(mini) == before


def test_a_catalogued_story_is_shipped(mini):
    append(mini, "per US-AGORA-998")
    before = sum(shipped_refs.scan(mini)["story"].values())
    story = mini / "requirements/stories/x/US-AGORA-998-shipped-here.md"
    story.parent.mkdir(parents=True)
    story.write_text("---\nid: US-AGORA-998\n---\n", encoding="utf-8")
    assert sum(shipped_refs.scan(mini)["story"].values()) == before - 1


def test_growth_reds_and_falling_passes(mini, capsys):
    assert shipped_refs.run(mini) == 0
    append(mini, "`flask agora frobnicate`")
    assert shipped_refs.run(mini) == 1
    assert "command:" in capsys.readouterr().out
    assert shipped_refs.run(mini, update=True) == 1
    assert shipped_refs.run(mini, update=True, allow_growth=["command"]) == 0
    assert shipped_refs.run(mini) == 0


def test_a_removed_reference_passes_and_says_the_baseline_can_tighten(mini, capsys):
    p = mini / ".claude/skills/agora/SKILL.md"
    text = p.read_text(encoding="utf-8")
    p.write_text(text.replace("flask agora retro-context", "the retro reader", 1), encoding="utf-8")
    assert shipped_refs.run(mini) == 0
    assert "tighten with --update-baseline" in capsys.readouterr().out


def test_the_repository_holds_its_baseline(repo):
    assert shipped_refs.run(repo) == 0
