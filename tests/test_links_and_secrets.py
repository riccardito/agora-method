from agora_checks import links, secrets


def test_a_broken_relative_link_is_found_and_code_is_skipped(tmp_path):
    (tmp_path / "real.md").write_text("x", encoding="utf-8")
    doc = tmp_path / "doc.md"
    doc.write_text("[ok](real.md#top) [gone](missing.md) [web](https://example.org)\n"
                   "`[inline](nowhere.md)`\n```\n[fenced](nowhere.md)\n```\n", encoding="utf-8")
    assert links.broken(tmp_path, doc) == [(1, "missing.md")]


def test_the_repository_links_resolve(repo):
    assert links.run(repo) == 0


def test_known_secret_shapes_are_found(tmp_path):
    # assembled at run time so this file does not itself trip the scan
    gh = "gh" + "p_" + "a" * 36
    aws = "AKIA" + "ABCDEFGHIJKLMNOP"
    key = "-----BEGIN " + "PRIVATE KEY-----"
    assigned = "api_key = '" + "s3cr3tvalue1234" + "'"
    f = tmp_path / "leak.py"
    f.write_text("\n".join([gh, aws, key, assigned, "token = os.environ['X']"]), encoding="utf-8")
    kinds = [k for _n, k in secrets.scan_file(f)]
    assert kinds == ["GitHub token", "AWS access key", "private key", "assigned secret"]


def test_the_allow_marker_silences_one_line(tmp_path):
    f = tmp_path / "fixture.py"
    f.write_text("AKIA" + "ABCDEFGHIJKLMNOP  # secret-scan: allow\n", encoding="utf-8")
    assert secrets.scan_file(f) == []


def test_the_repository_has_no_secret(repo):
    assert secrets.run(repo) == 0
