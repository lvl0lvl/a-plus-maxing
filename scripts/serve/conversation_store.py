"""Care-agent conversation vault: persist + restore each conversation as searchable markdown.

Each care/specialist thread is one markdown file with YAML frontmatter under a GITIGNORED
`vault/conversations/` — the same searchable markdown+frontmatter shape the specialist library uses,
so a conversation SURVIVES a reload (restored via `read_turns`, so the operator never redoes it) and is
greppable / basic-memory-indexable. Raw operator words are PII, so this vault is gitignored (never
committed) + `block-pii-commit`-guarded; it is on-device only, the SAME posture as `vault/scaffold`.

The file shape (daemon-safe — plain scalar frontmatter, no placeholders):

    ---
    title: Care Assistant conversation
    type: conversation
    participant: care
    created: 2026-07-02
    updated: 2026-07-02
    turns: 3
    status: active
    tags: [conversation, care-agent]
    ---

    # Care Assistant conversation

    ## 2026-07-02T18:30:00+00:00 — You
    It's my age.

    ## 2026-07-02T18:30:05+00:00 — Assistant
    Got it — you're 55.

`read_turns` reconstructs `[{role, content}]` for the restore; the turn delimiter is anchored on the
`<ts> — You|Assistant` header so an incidental `##` inside a message is never a false boundary.
"""

import datetime
import re
from pathlib import Path

DEFAULT_ROOT = Path("vault/conversations")

# The display label written per role, and the reverse map for the round-trip read.
_ROLE_TO_LABEL = {"user": "You", "assistant": "Assistant"}
_LABEL_TO_ROLE = {"You": "user", "Assistant": "assistant"}

# A human title per known thread; an unknown thread falls back to a title-cased id.
_THREAD_TITLES = {"care": "Care Assistant conversation"}

# The turn boundary: `## <timestamp> — You|Assistant`. Anchored on the KNOWN role labels so a `##`
# inside a message body is not mistaken for a turn header. `re.MULTILINE` so `^` matches each line.
_TURN_RE = re.compile(r"^## (?P<ts>\S+) — (?P<label>You|Assistant)\n(?P<body>.*?)(?=\n## \S+ — (?:You|Assistant)\n|\Z)",
                      re.DOTALL | re.MULTILINE)


def _now_iso():
    """The UTC-offset timestamp a turn carries (injectable for tests via the `_now` param)."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _safe_thread(thread):
    """Sanitize a thread id into a single safe filename stem (no path traversal, no separators)."""
    stem = re.sub(r"[^A-Za-z0-9_-]", "-", str(thread)).strip("-") or "conversation"
    return stem


def _title(thread):
    """The conversation title for a thread (a known label, else a title-cased id)."""
    return _THREAD_TITLES.get(thread, f"{str(thread).replace('-', ' ').title()} conversation")


def _frontmatter(thread, created, updated, turns):
    """Render the conforming YAML frontmatter block for a conversation file."""
    return (
        "---\n"
        f"title: {_title(thread)}\n"
        "type: conversation\n"
        f"participant: {thread}\n"
        f"created: {created}\n"
        f"updated: {updated}\n"
        f"turns: {turns}\n"
        "status: active\n"
        "tags: [conversation, care-agent]\n"
        "---\n"
    )


def _split(text):
    """Split an existing conversation file into (frontmatter-fields, body-after-the-H1)."""
    fields = {}
    body = ""
    m = re.match(r"---\n(.*?)\n---\n(.*)\Z", text, re.DOTALL)
    if not m:
        return fields, text
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip()
    rest = m.group(2)
    # drop the leading `# <title>` H1 line if present; the turns follow it
    rest = re.sub(r"\A\s*# [^\n]*\n+", "", rest)
    body = rest
    return fields, body


def record_turn(thread, role, content, *, root=None, _now=None):
    """Append one conversation turn to the thread's markdown vault file (create with frontmatter if new).

    Args:
        thread (str): The conversation thread id (a specialist id, e.g. "care"); sanitized to a filename.
        role (str): "user" or "assistant".
        content (str): The turn text (raw; PII lives on-device in this gitignored vault only).
        root (str | Path, optional): The conversation vault root; None -> `vault/conversations/`.
        _now (str, optional): An injected ISO timestamp (tests); None -> the real UTC-offset now.

    Returns:
        (Path) The conversation file written.
    """
    base = Path(root) if root is not None else DEFAULT_ROOT
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{_safe_thread(thread)}.md"
    ts = _now or _now_iso()
    day = ts[:10]
    label = _ROLE_TO_LABEL.get(role, "You")
    turn_block = f"\n## {ts} — {label}\n{content}\n"

    if path.exists():
        fields, body = _split(path.read_text())
        created = fields.get("created", day)
        try:
            turns = int(fields.get("turns", "0")) + 1
        except ValueError:
            turns = 1
        new_body = body.rstrip("\n") + "\n" + turn_block
    else:
        created = day
        turns = 1
        new_body = turn_block

    path.write_text(_frontmatter(thread, created, day, turns) + f"\n# {_title(thread)}\n" + new_body)
    return path


def read_turns(thread, *, root=None):
    """Reconstruct a thread's conversation as `[{role, content}]` (empty when the file is absent).

    Args:
        thread (str): The conversation thread id.
        root (str | Path, optional): The conversation vault root; None -> `vault/conversations/`.

    Returns:
        (list) The turns in order, each `{"role": "user"|"assistant", "content": str}`.
    """
    base = Path(root) if root is not None else DEFAULT_ROOT
    path = base / f"{_safe_thread(thread)}.md"
    if not path.exists():
        return []
    _fields, body = _split(path.read_text())
    turns = []
    for m in _TURN_RE.finditer(body):
        role = _LABEL_TO_ROLE.get(m.group("label"), "user")
        turns.append({"role": role, "content": m.group("body").rstrip("\n")})
    return turns
