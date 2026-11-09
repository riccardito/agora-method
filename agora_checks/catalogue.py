"""The requirements catalogue -- stories, use cases and quality criteria that hold together.

`requirements/` keeps the catalogue as files: one story, use case or quality
criterion per file, YAML frontmatter on top, prose below. This check is its gate.
It reads every file, then applies fourteen rules, each with an id so a failure
names the rule that caught it:

  C01  the id has its kind's shape (US-<AREA>-NNN, UC-<AREA>-NNN, QC-<CAT>-NNN)
  C02  the file name starts with the id
  C03  no id is used twice
  C04  the kind's required fields are present
  C05  status, priority and source take values from their lists
  C06  the actor is one of the `###` headings of `requirements/actors.md`
  C07  a story states its user story: "As a ..., I want ..., so that ..."
  C08  a story has at least one acceptance criterion (a `- [ ]` line)
  C09  every `related_tests` entry resolves: the file exists, and a `::test_name` exists in it
  C10  a story at `implemented` or `tested` names at least one test
  C11  a story at `tested` has every acceptance criterion ticked
  C12  references resolve: a use case's stories, quality criteria, glossary terms
  C13  every story at `implemented` or `tested` is named by a use case
  C14  a use case whose stories have all shipped is no longer `draft`

The rules are distilled from the parent project's catalogue lint (184 rules over
a larger catalogue); these are the ones a catalogue of any size needs.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .common import load_frontmatter, rel, split_frontmatter

STATUS = ("draft", "review", "approved", "planned", "in-progress", "partially-implemented",
          "implemented", "tested")
SHIPPED = ("implemented", "tested")
PRIORITY = ("must-have", "should-have", "could-have")
SOURCE = ("codebase", "user-feedback", "user-request", "regulation", "strategy-paper",
          "requirements", "gap-analysis")

KINDS = {
    "story": {"dir": "stories", "id": re.compile(r"^US-[A-Z][A-Z0-9]+-\d{3}[a-z]?$"),
              "fields": ("id", "title", "actor", "feature_area", "priority", "status", "source",
                         "related_tests", "quality_criteria", "glossary_terms")},
    "use-case": {"dir": "use-cases", "id": re.compile(r"^UC-[A-Z][A-Z0-9]+-\d{3}$"),
                 "fields": ("id", "title", "actor", "status", "stories")},
    "quality": {"dir": "quality-criteria", "id": re.compile(r"^QC-[A-Z]+-\d{3}$"),
                "fields": ("id", "title", "category", "status", "measure")},
}
USER_STORY = re.compile(r"\bAs an? .+?\bI want\b.+?\bso that\b", re.S | re.I)
CRITERION = re.compile(r"^\s*- \[([ xX])\]", re.M)
GLOSSARY = re.compile(r"^###\s+(GLOSS-[A-Z0-9-]+)\b", re.M)
ACTOR = re.compile(r"^###\s+([a-z][a-z0-9-]*)\s*$", re.M)


@dataclass
class Entry:
    kind: str
    path: Path
    fm: dict
    body: str


@dataclass
class Catalogue:
    root: Path
    entries: list[Entry] = field(default_factory=list)
    actors: set[str] = field(default_factory=set)
    glossary: set[str] = field(default_factory=set)
    unreadable: list[tuple[Path, str]] = field(default_factory=list)

    def ids(self, kind: str) -> dict[str, Entry]:
        return {str(e.fm.get("id")): e for e in self.entries if e.kind == kind}


def load(root: Path) -> Catalogue:
    base = root / "requirements"
    cat = Catalogue(root)
    if (base / "actors.md").exists():
        cat.actors = set(ACTOR.findall((base / "actors.md").read_text(encoding="utf-8")))
    if (base / "glossary.md").exists():
        cat.glossary = set(GLOSSARY.findall((base / "glossary.md").read_text(encoding="utf-8")))
    for kind, spec in KINDS.items():
        for p in sorted((base / spec["dir"]).rglob("*.md")):
            if p.name.startswith("_"):
                continue  # templates
            text = p.read_text(encoding="utf-8")
            fm = load_frontmatter(text)
            if fm is None:
                cat.unreadable.append((p, "no YAML frontmatter"))
                continue
            cat.entries.append(Entry(kind, p, fm, split_frontmatter(text)[1]))
    return cat


def resolve_test(root: Path, ref: str) -> str | None:
    """None when `path[::name]` names an existing file and, if given, a test function in it."""
    path, _, name = ref.partition("::")
    file = root / path
    if not file.is_file():
        return f"test file {path} does not exist"
    if name and not re.search(rf"^\s*def {re.escape(name)}\(", file.read_text(encoding="utf-8"), re.M):
        return f"{path} has no test named {name}"
    return None


def problems(cat: Catalogue) -> list[tuple[str, str, str]]:
    """(rule, file, message) for every broken rule."""
    out: list[tuple[str, str, str]] = [("C04", rel(cat.root, p), why) for p, why in cat.unreadable]
    stories, cases, quality = cat.ids("story"), cat.ids("use-case"), cat.ids("quality")
    seen: dict[str, str] = {}
    named_by_case = {s for e in cases.values() for s in (e.fm.get("stories") or [])}

    for e in cat.entries:
        spec, f, fm = KINDS[e.kind], rel(cat.root, e.path), e.fm
        eid = str(fm.get("id", ""))

        def bad(rule: str, msg: str, f: str = f) -> None:
            out.append((rule, f, msg))

        if not spec["id"].match(eid):
            bad("C01", f"id {eid!r} is not a {e.kind} id")
        if not e.path.name.startswith(eid + "-") and e.path.stem != eid:
            bad("C02", f"file name does not start with its id {eid}")
        if eid in seen:
            bad("C03", f"id {eid} is also used by {seen[eid]}")
        seen.setdefault(eid, f)
        for name in spec["fields"]:
            if name not in fm:
                bad("C04", f"required field {name!r} is missing")
        for name, allowed in (("status", STATUS), ("priority", PRIORITY), ("source", SOURCE)):
            if name in fm and fm[name] not in allowed:
                bad("C05", f"{name} {fm[name]!r} is not one of {', '.join(allowed)}")
        if "actor" in fm and fm["actor"] not in cat.actors:
            bad("C06", f"actor {fm['actor']!r} is not a heading of requirements/actors.md")

        if e.kind == "story":
            criteria = CRITERION.findall(e.body)
            if not USER_STORY.search(e.body):
                bad("C07", "no user story sentence (As a ..., I want ..., so that ...)")
            if not criteria:
                bad("C08", "no acceptance criterion (a `- [ ]` line)")
            tests = fm.get("related_tests") or []
            for ref in tests:
                why = resolve_test(cat.root, str(ref))
                if why:
                    bad("C09", why)
            if fm.get("status") in SHIPPED and not tests:
                bad("C10", f"status {fm['status']} but no related_tests")
            if fm.get("status") == "tested" and any(c == " " for c in criteria):
                bad("C11", f"status tested but {sum(c == ' ' for c in criteria)} criterion(s) unticked")
            for qc in fm.get("quality_criteria") or []:
                if qc not in quality:
                    bad("C12", f"quality criterion {qc} does not exist")
            for term in fm.get("glossary_terms") or []:
                if term not in cat.glossary:
                    bad("C12", f"glossary term {term} is not in requirements/glossary.md")
            if fm.get("status") in SHIPPED and eid not in named_by_case:
                bad("C13", f"status {fm['status']} but no use case names {eid}")

        if e.kind == "use-case":
            listed = fm.get("stories") or []
            for s in listed:
                if s not in stories:
                    bad("C12", f"story {s} does not exist")
            for qc in fm.get("quality_criteria") or []:
                if qc not in quality:
                    bad("C12", f"quality criterion {qc} does not exist")
            shipped = [s for s in listed if s in stories and stories[s].fm.get("status") in SHIPPED]
            if listed and len(shipped) == len(listed) and fm.get("status") == "draft":
                bad("C14", f"all {len(listed)} stories have shipped, but the use case is still draft")
    return sorted(out, key=lambda r: (r[1], r[0], r[2]))


def run(root: Path) -> int:
    cat = load(root)
    found = problems(cat)
    for rule, f, msg in found:
        print(f"[FAIL] {f}: {rule} {msg}")
    counts = {k: len(cat.ids(k)) for k in KINDS}
    print(f"[catalogue] {counts['story']} stories, {counts['use-case']} use cases, "
          f"{counts['quality']} quality criteria; {len(found)} problem(s)")
    return 1 if found else 0
