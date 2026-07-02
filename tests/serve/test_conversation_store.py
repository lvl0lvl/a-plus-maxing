"""Care-agent conversation vault tests (persist + restore + frontmatter).

`conversation_store` persists each care/specialist conversation as a markdown file with YAML
frontmatter under a GITIGNORED `vault/conversations/` — the same searchable markdown+frontmatter shape
the specialist library uses. A conversation survives a reload (restored via `read_turns`) so the
operator never redoes it, and it is greppable / basic-memory-indexable. Raw operator words are PII, so
the vault is gitignored + `block-pii-commit`-guarded (verified by the linter tests + the .gitignore).

Fixture-driven over a tmp root; deterministic timestamps injected. No live API, no network.
"""

from scripts.serve import conversation_store as cs


def test_record_turn_creates_a_frontmattered_file(tmp_path):
    """The first turn creates `<thread>.md` with conforming YAML frontmatter + the turn body."""
    cs.record_turn("care", "user", "It's my age, 55.", root=tmp_path, _now="2026-07-02T18:30:00+00:00")
    path = tmp_path / "care.md"
    assert path.exists(), "the conversation file was not created"
    text = path.read_text()
    # frontmatter fence + the required fields
    assert text.startswith("---\n"), "no YAML frontmatter fence"
    for field in ("title:", "type: conversation", "participant: care", "created:", "updated:",
                  "turns: 1", "status: active"):
        assert field in text, f"frontmatter missing {field!r}"
    assert "It's my age, 55." in text, "the turn content was not written"


def test_record_turn_appends_and_round_trips_through_read_turns(tmp_path):
    """Multiple turns append in order and `read_turns` reconstructs `[{role, content}]` exactly."""
    cs.record_turn("care", "assistant", "Is 55 your age or training years?", root=tmp_path, _now="2026-07-02T18:30:00+00:00")
    cs.record_turn("care", "user", "My age.", root=tmp_path, _now="2026-07-02T18:31:00+00:00")
    cs.record_turn("care", "assistant", "Got it — you're 55.", root=tmp_path, _now="2026-07-02T18:31:05+00:00")
    turns = cs.read_turns("care", root=tmp_path)
    assert turns == [
        {"role": "assistant", "content": "Is 55 your age or training years?"},
        {"role": "user", "content": "My age."},
        {"role": "assistant", "content": "Got it — you're 55."},
    ], f"the round-trip did not reconstruct the conversation: {turns}"
    # the turn count in the frontmatter tracks the appends
    assert "turns: 3" in (tmp_path / "care.md").read_text(), "the frontmatter turn count did not update"


def test_read_turns_absent_thread_is_empty(tmp_path):
    """Reading a thread with no file yet returns an empty list (a fresh conversation)."""
    assert cs.read_turns("care", root=tmp_path) == [], "an absent conversation did not read as empty"


def test_record_turn_content_with_markdown_headers_round_trips(tmp_path):
    """A message body containing its own `## ...` markdown line still round-trips intact.

    The turn delimiter is anchored on the `<ts> — You|Assistant` header shape, so an incidental `##`
    inside a message is not mistaken for a turn boundary. Failing-capable: a naive split reds this.
    """
    body = "Here's my plan:\n## Monday\nsquats\n## Tuesday\nrest"
    cs.record_turn("care", "user", body, root=tmp_path, _now="2026-07-02T18:30:00+00:00")
    cs.record_turn("care", "assistant", "Looks good.", root=tmp_path, _now="2026-07-02T18:30:05+00:00")
    turns = cs.read_turns("care", root=tmp_path)
    assert turns[0]["content"] == body, f"a message with markdown headers did not round-trip: {turns[0]['content']!r}"
    assert turns[1]["content"] == "Looks good."


def test_threads_are_isolated(tmp_path):
    """Each thread is its own file — a `pt` turn does not appear in the `care` conversation."""
    cs.record_turn("care", "user", "care message", root=tmp_path, _now="2026-07-02T18:30:00+00:00")
    cs.record_turn("pt", "user", "trainer message", root=tmp_path, _now="2026-07-02T18:30:00+00:00")
    assert [t["content"] for t in cs.read_turns("care", root=tmp_path)] == ["care message"]
    assert [t["content"] for t in cs.read_turns("pt", root=tmp_path)] == ["trainer message"]


def test_thread_id_is_sanitized_no_path_traversal(tmp_path):
    """A crafted thread id cannot escape the conversation root (no `../` path traversal)."""
    cs.record_turn("../../etc/evil", "user", "x", root=tmp_path, _now="2026-07-02T18:30:00+00:00")
    # nothing was written outside the root
    assert not (tmp_path.parent.parent / "etc" / "evil.md").exists(), "a thread id escaped the conversation root"
    # the sanitized file (if any) is inside the root
    for p in tmp_path.rglob("*.md"):
        assert tmp_path in p.parents, f"a conversation file landed outside the root: {p}"
