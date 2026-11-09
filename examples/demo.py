"""`make demo` -- one Agora session, start to end, in a throwaway child.

1. Build a child in a temporary directory: the method layer from this repository
   (`.claude/`, `agora/`, the catalogue templates) with `examples/first-child/` laid
   over it. The child measures its own shipped-refs baseline once, at birth.
2. --start: read the baton the last closed session left; open a session from it.
3. Two phases, each closed at a gate that records the user's nod.
4. --end: the close-out paper (summary, baton, retrospective), the index re-rendered.
5. Run every check over the child. Exit 0 only if all are green.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from agora_checks import session  # noqa: E402
from agora_checks.__main__ import main as checks  # noqa: E402


def say(step: str, text: str = "") -> None:
    print(f"\n== {step}" + (f"\n   {text}" if text else ""))


def build_child(dest: Path) -> Path:
    for part in (".claude", "agora"):
        shutil.copytree(REPO / part, dest / part)
    for f in (dest / ".claude" / "sessions").glob("*.md"):
        if f.name not in ("_TEMPLATE.md", "EVENTS.md", "README.md", "IMPROVEMENTS.md", "PLANS.md",
                          "policy-breaches.md"):
            f.unlink()
    shutil.copytree(REPO / "requirements" / "templates", dest / "requirements" / "templates")
    shutil.copytree(REPO / "examples" / "first-child", dest, dirs_exist_ok=True)
    # The copied skills cite the method's own stories, which live in this repository's
    # catalogue, not the child's: the child measures what its copy points at, once.
    checks(["shipped-refs", "--root", str(dest), "--update-baseline", "--allow-growth", "story"])
    return dest


def run_session(child: Path) -> Path:
    say("--start", "read the baton the last session left")
    last, baton = session.read_baton(child)
    print(f"   from {last}:")
    for b in baton:
        print(f"     - {b}")

    path = session.open_session(
        child, "imperial-lengths",
        intent="Inches, feet, yards and miles convert to metres and back (criterion 2); rule T-001",
        goal="Length conversions",
        plan=["Phase 1 -- the four imperial units in units.yaml, exact factors",
              "Phase 2 -- rule T-001: display rounding vs the exact value"])
    say("plan", f"opened {path.name} with two phases; the plan gate is the user's nod on it")

    session.log(path, "Phase 1 -- imperial units", [
        "in, ft, yd and mi added with their exact international definitions (1 in = 0.0254 m)",
        "round-trip test for each: metres -> unit -> metres within 1e-12"])
    session.tick(path, "Phase 1", nod="go")
    say("gate", "Phase 1 ticked -- the nod 'go' is written beside the box, in one act")

    session.log(path, "Phase 2 -- T-001 ruled", [
        "results keep the exact value; the display rounds to 6 significant digits and says so",
        "T-001 resolved; the ruling feeds criterion 3 (name the definition)"])
    session.tick(path, "Phase 2", nod="yes, and say 'exact' in the output")
    say("gate", "Phase 2 ticked -- the user's redirect rides inside the nod")

    session.close(
        path,
        summary="Criterion 2 is met: four imperial units convert exactly; T-001 ruled on display rounding.",
        baton=["Goal: Length conversions, criterion 3 next -- every result names its definition",
               "the display already says 'exact'; extend it to the definition's source"],
        retro={"worked": "the baton named the next criterion, so the plan took one minute",
               "did not": "nothing tested the display string until Phase 2's redirect",
               "change": "pin the display format with a test before the next output change"},
        outcome="criterion 2 met (four imperial units), T-001 ruled")
    session.render_index(child)
    say("--end", "close-out paper written, status closed, INDEX re-rendered")
    return path


def main() -> int:
    t0 = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="agora-child-") as tmp:
        child = build_child(Path(tmp) / "units")
        path = run_session(child)
        say("checks", "every check over the child")
        verdict = checks(["all", "--root", str(child)])
        say("the session file")
        print(path.read_text(encoding="utf-8"))
    print(f"\n[demo] {'green' if verdict == 0 else 'RED'} in {time.perf_counter() - t0:.1f} s")
    return verdict


if __name__ == "__main__":
    sys.exit(main())
