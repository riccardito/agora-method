"""Domain share -- how much of the corpus belongs to the product it was extracted from.

Every non-blank line takes the FIRST class whose patterns match it: agora, domain,
layout, stack, else neutral. That is the measuring method; the share per class is
the report. The gate is stricter: a line is a domain hit when any domain pattern
matches it after the agora spans are masked out, so a domain word cannot hide
behind an agora word on the same line. The publish rule is 0 domain hits.

The parent product's own names are never written here: `private_terms_sha256`
holds the SHA-256 of each lower-cased word, and every word in the corpus is hashed
and compared.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .common import corpus, rel

CLASSES = ("agora", "domain", "layout", "stack")
WORD = re.compile(r"[A-Za-z][A-Za-z0-9-]*")


@dataclass
class Terms:
    patterns: dict[str, list[re.Pattern]]
    private: set[str] = field(default_factory=set)

    @classmethod
    def load(cls, path: Path) -> Terms:
        cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
        skills = "|".join(sorted(cfg.get("skill_names", []), key=len, reverse=True)) or "(?!)"
        pats = {}
        for name in CLASSES:
            pats[name] = [re.compile(p.replace("<skills>", skills)) for p in cfg.get(name, [])]
        return cls(pats, set(cfg.get("private_terms_sha256", [])))

    def private_hit(self, line: str) -> str | None:
        for w in WORD.findall(line):
            if hashlib.sha256(w.lower().encode()).hexdigest() in self.private:
                return w
        return None

    def classify(self, line: str) -> str:
        if self.private_hit(line):
            return "domain"
        for name in CLASSES:
            if any(p.search(line) for p in self.patterns[name]):
                return name
        return "neutral"

    def strict_hit(self, line: str) -> str | None:
        """The domain match left after masking every agora span, or None."""
        word = self.private_hit(line)
        if word:
            return word
        masked = line
        for p in self.patterns["agora"]:
            masked = p.sub(lambda m: " " * len(m.group(0)), masked)
        for p in self.patterns["domain"]:
            m = p.search(masked)
            if m:
                return m.group(0)
        return None


@dataclass
class FileShare:
    path: str
    counts: dict[str, int]
    hits: list[tuple[int, str, str]]

    @property
    def lines(self) -> int:
        return sum(self.counts.values())

    def share(self, cls: str) -> float:
        return 100.0 * self.counts[cls] / self.lines if self.lines else 0.0


def measure(root: Path, terms: Terms, files: list[Path] | None = None) -> list[FileShare]:
    out = []
    for p in files or corpus(root):
        counts = dict.fromkeys((*CLASSES, "neutral"), 0)
        hits = []
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            counts[terms.classify(line)] += 1
            hit = terms.strict_hit(line)
            if hit:
                hits.append((n, hit, line.strip()))
        out.append(FileShare(rel(root, p), counts, hits))
    return out


def run(root: Path, report: bool = False) -> int:
    terms = Terms.load(root / "agora" / "domain-terms.yaml")
    shares = measure(root, terms, corpus(root) + corpus(root, "requirements/**/*.md"))
    total = dict.fromkeys((*CLASSES, "neutral"), 0)
    for s in shares:
        for k, v in s.counts.items():
            total[k] += v
    n = sum(total.values()) or 1
    if report:
        print(f"{'file':52} {'lines':>6} " + " ".join(f"{c:>7}" for c in CLASSES))
        for s in shares:
            print(f"{s.path:52} {s.lines:6} " + " ".join(f"{s.share(c):6.1f}%" for c in CLASSES))
    hits = [(s.path, *h) for s in shares for h in s.hits]
    for path, line_no, word, text in hits:
        print(f"[FAIL] {path}:{line_no}: domain term {word!r}: {text[:100]}")
    print(f"[domain-share] {n} lines, method share {100 * total['domain'] / n:.1f} % domain, "
          f"{len(hits)} strict hit(s)")
    return 1 if hits else 0
