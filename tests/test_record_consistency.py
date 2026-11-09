from agora_checks import record_consistency as rc


def test_a_hand_edit_to_a_generated_block_is_drift_and_fix_restores_it(mini, capsys):
    readme = mini / "docs/method.md"
    text = readme.read_text(encoding="utf-8")
    readme.write_text(text.replace("| **Era** |", "| **Epoch** |"), encoding="utf-8")
    assert rc.run(mini) == 1
    assert "tier-table: docs/method.md differs" in capsys.readouterr().out
    assert rc.run(mini, fix=True) == 0
    assert rc.run(mini) == 0
    assert readme.read_text(encoding="utf-8") == text


def test_a_source_change_reaches_the_generated_copies(mini):
    vocab = mini / "agora/vocabulary.yaml"
    vocab.write_text(vocab.read_text(encoding="utf-8").replace("a work window", "one sitting"),
                     encoding="utf-8")
    assert rc.run(mini) == 1
    assert rc.run(mini, fix=True) == 0
    assert "one sitting" in (mini / ".claude/skills/agora/SKILL.md").read_text(encoding="utf-8")


def test_verbatim_drift_is_reported_and_never_auto_fixed(mini, capsys):
    claude = mini / "CLAUDE.md"
    claude.write_text(claude.read_text(encoding="utf-8").replace("Propose a default", "Offer options"),
                      encoding="utf-8")
    assert rc.run(mini, fix=True) == 1
    assert "policy-four-eyes: CLAUDE.md differs" in capsys.readouterr().out
    assert "Offer options" in claude.read_text(encoding="utf-8")


def test_links_are_ignored_by_the_verbatim_comparison():
    assert rc.normalise("see [the  file](a/b.md)\nnow") == rc.normalise("see the file now")


def test_the_repository_is_consistent(repo):
    assert rc.run(repo) == 0
