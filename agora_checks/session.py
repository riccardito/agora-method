"""The session bracket as callable writers -- a small, file-only substrate.

The parent project drives sessions through a CLI of about sixty commands. This
module keeps the six that make the bracket work, so a child can run a whole
session without it:

  open_session  writes a session file from `_TEMPLATE.md` (fields, not a hand
                splice); refuses a second open session
  log           appends one entry under `## Log`
  tick          flips a plan box AND records the user's nod in `## Evidence` --
                one act, so a gate that was not asked cannot be recorded as fired
  close         writes the close-out paper and flips `status: closed`; refuses
                while the baton or the retrospective is empty
  render_index  rewrites INDEX.md from every session's frontmatter
  read_baton    the newest closed session's baton, for the next `--start`

Each writer re-reads what it wrote and raises `SessionError` on a mismatch.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

import yaml

from .common import load_frontmatter, split_frontmatter

SESSIONS = Path(".claude/sessions")
SESSION_FILE = re.compile(r"^\d{4}-\d\d-\d\d-[a-z0-9-]+\.md$")
COMMENT = re.compile(r"<!--.*?-->\n?", re.S)


class SessionError(RuntimeError):
    pass


def session_files(root: Path) -> list[Path]:
    d = root / SESSIONS
    return sorted(p for p in d.glob("*.md") if SESSION_FILE.match(p.name))


def find_open(root: Path) -> Path | None:
    for p in session_files(root):
        if (load_frontmatter(p.read_text(encoding="utf-8")) or {}).get("status") == "open":
            return p
    return None


def _replace_section(body: str, heading: str, content: str) -> str:
    """Replace the text under `heading` up to the next heading of the same or a higher level."""
    level = heading.split(" ", 1)[0]
    stop = f"^#{{1,{len(level)}}} "
    m = re.search(rf"^{re.escape(heading)}\s*$", body, re.M)
    if not m:
        raise SessionError(f"no `{heading}` heading")
    nxt = re.compile(stop, re.M).search(body, m.end())
    end = nxt.start() if nxt else len(body)
    return body[:m.end()] + "\n\n" + content.strip() + "\n\n" + body[end:]


def _write(path: Path, fm: dict, body: str) -> None:
    body = "\n" + re.sub(r"\n{3,}", "\n\n", body).strip("\n") + "\n"
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---\n" + body
    path.write_text(text, encoding="utf-8", newline="\n")
    if load_frontmatter(path.read_text(encoding="utf-8")) != fm:
        raise SessionError(f"{path.name}: the frontmatter did not read back")


def _read(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    _raw, body = split_frontmatter(text)
    return load_frontmatter(text) or {}, body


def open_session(root: Path, slug: str, intent: str, goal: str, plan: list[str],
                 type_: str = "mixed", date: dt.date | None = None) -> Path:
    if find_open(root):
        raise SessionError(f"{find_open(root).name} is still open -- close it first")
    date = date or dt.date.today()
    sid = f"{date.isoformat()}-{slug}"
    path = root / SESSIONS / f"{sid}.md"
    if path.exists():
        raise SessionError(f"{path.name} already exists")
    template = (root / SESSIONS / "_TEMPLATE.md").read_text(encoding="utf-8")
    _raw, body = split_frontmatter(template)
    body = COMMENT.sub("", body)
    body = re.sub(r"^# Session .*$", f"# Session {sid}", body, count=1, flags=re.M)
    body = _replace_section(body, "## Intent", intent)
    body = _replace_section(body, "## Session plan", "\n".join(f"- [ ] {p}" for p in plan))
    for h in ("## Log", "## Open threads", "## Agora findings", "## Evidence"):
        body = _replace_section(body, h, "")
    # the handoff checklist belongs to a blind run only
    body = re.sub(r"^## Handoff checklist\s*$.*?(?=^## )", "", body, flags=re.S | re.M)
    body = body[:body.index("## Close-out")] + "## Close-out\n"
    fm = {"session_id": sid, "date": date.isoformat(), "closed_date": "", "type": type_,
          "mode": "normal", "intent": intent, "goal": goal, "status": "open", "outcome": ""}
    _write(path, fm, body)
    return path


def log(path: Path, heading: str, bullets: list[str]) -> None:
    fm, body = _read(path)
    entry = f"### {heading}\n\n" + "\n".join(f"- {b}" for b in bullets) + "\n\n"
    i = body.index("## Open threads")
    body = body[:i] + entry + body[i:]
    _write(path, fm, body)
    if entry.strip() not in path.read_text(encoding="utf-8"):
        raise SessionError("the log entry did not land")


def tick(path: Path, phase: str, nod: str) -> None:
    """Flip `- [ ] <phase…>` to `[x]` and record the nod -- refuses without one."""
    if not nod.strip():
        raise SessionError("a phase gate needs the user's nod, in their words")
    fm, body = _read(path)
    box = re.compile(rf"^- \[ \] ({re.escape(phase)}.*)$", re.M)
    m = box.search(body)
    if not m:
        done = re.search(rf"^- \[x\] {re.escape(phase)}", body, re.M)
        raise SessionError(f"phase {phase!r} is {'already ticked' if done else 'not in the plan'}")
    body = body[:m.start()] + f"- [x] {m.group(1)}" + body[m.end():]
    ev = re.search(r"^## Evidence\s*$(.*?)(?=^## |\Z)", body, re.S | re.M)
    lines = ev.group(1).strip()
    entry = f'- phase-gate "{phase}" nod "{nod.strip()}"'
    body = _replace_section(body, "## Evidence", f"{lines}\n{entry}" if lines else entry)
    _write(path, fm, body)


def close(path: Path, summary: str, baton: list[str], retro: dict[str, str], outcome: str) -> None:
    if not baton:
        raise SessionError("the close-out paper needs a baton -- what the next session inherits")
    missing = [k for k in ("worked", "did not", "change") if not retro.get(k, "").strip()]
    if missing:
        raise SessionError(f"the retrospective is missing: {', '.join(missing)}")
    fm, body = _read(path)
    open_boxes = re.findall(r"^- \[ \] (.*)$", body, re.M)
    paper = (f"**Compacted summary:** {summary}\n\n"
             + (f"**Unticked phases:** {'; '.join(open_boxes)}\n\n" if open_boxes else "")
             + "### Baton — what the next session inherits\n\n" + "\n".join(f"- {b}" for b in baton)
             + "\n\n### Retrospective\n\n"
             + f"1. **What worked:** {retro['worked']}\n2. **What did not:** {retro['did not']}\n"
             + f"3. **What to change:** {retro['change']}\n")
    body = body[:body.index("## Close-out")] + "## Close-out\n\n" + paper
    fm.update(status="closed", closed_date=dt.date.today().isoformat(), outcome=outcome)
    _write(path, fm, body)


def render_index(root: Path) -> Path:
    lines = []
    for p in reversed(session_files(root)):
        fm = load_frontmatter(p.read_text(encoding="utf-8")) or {}
        text = fm.get("outcome") or f"{fm.get('intent', '')} — in progress"
        lines.append(f"- [{p.stem}]({p.name}) — {fm.get('type', '')} · {fm.get('status', '')} · {text}")
    index = root / SESSIONS / "INDEX.md"
    head = index.read_text(encoding="utf-8").split("\n- [", 1)[0].rstrip() + "\n\n"
    index.write_text(head + "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return index


def read_baton(root: Path) -> tuple[str, list[str]] | None:
    closed = [p for p in session_files(root)
              if (load_frontmatter(p.read_text(encoding="utf-8")) or {}).get("status") == "closed"]
    if not closed:
        return None
    last = closed[-1]
    m = re.search(r"^### Baton.*?$\n(.*?)(?=^### |\Z)", last.read_text(encoding="utf-8"), re.S | re.M)
    bullets = [b[2:].strip() for b in (m.group(1) if m else "").splitlines() if b.startswith("- ")]
    return last.stem, bullets
