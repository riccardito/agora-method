import hashlib
from pathlib import Path

import yaml

from agora_checks import domain_share


def terms(tmp_path: Path, private: list[str] = ()) -> domain_share.Terms:
    cfg = {"skill_names": ["agora", "wiki"],
           "agora": [r"\.claude/", r"(?<![\w/])/(<skills>)\b"],
           "domain": [r"\b(Patient|clinic)s?\b", r"(?<![\w.-])/(wiki-page)\b"],
           "layout": [r"\btests/"], "stack": [r"\bFlask\b"],
           "private_terms_sha256": [hashlib.sha256(w.encode()).hexdigest() for w in private]}
    p = tmp_path / "terms.yaml"
    p.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return domain_share.Terms.load(p)


def test_first_class_wins(tmp_path):
    t = terms(tmp_path)
    assert t.classify("see .claude/ for the Patient rules") == "agora"
    assert t.classify("a Patient record") == "domain"
    assert t.classify("tests/ hold the Flask app") == "layout"
    assert t.classify("plain prose") == "neutral"


def test_strict_mode_sees_a_domain_word_behind_an_agora_word(tmp_path):
    t = terms(tmp_path)
    assert t.strict_hit("see .claude/ for the Patient rules") == "Patient"
    assert t.strict_hit("run /agora and /wiki") is None  # skill commands are masked


def test_private_terms_are_matched_by_hash(tmp_path):
    t = terms(tmp_path, private=["zebracorp"])
    assert t.strict_hit("built for ZebraCorp in 2026") == "ZebraCorp"
    assert t.classify("built for zebracorp") == "domain"
    assert t.strict_hit("built for zebras") is None


def test_a_planted_term_reds_the_check(mini, capsys):
    skill = mini / ".claude/skills/agora/SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\nThe clinic opens at eight.\n", encoding="utf-8")
    assert domain_share.run(mini) == 1
    assert "domain term 'clinic'" in capsys.readouterr().out


def test_the_repository_has_no_domain_hit(repo):
    assert domain_share.run(repo) == 0
