import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from server.notes_server import create_note, delete_note, search_notes, read_note, list_notes, NOTES_DIR


@pytest.fixture(autouse=True)
def clean_notes_dir():
    """Ensure a clean notes directory before and after each test."""
    for f in NOTES_DIR.glob("*.md"):
        f.unlink()
    yield
    for f in NOTES_DIR.glob("*.md"):
        f.unlink()


def test_create_note():
    result = create_note("test note", "hello world")
    assert "Created note" in result
    assert (NOTES_DIR / "test_note.md").exists()


def test_create_note_duplicate():
    create_note("dup", "first")
    result = create_note("dup", "second")
    assert "already exists" in result


def test_read_note():
    create_note("readable", "some content")
    result = read_note("readable.md")
    assert result == "some content"


def test_read_note_missing():
    result = read_note("nope.md")
    assert "not found" in result


def test_delete_note():
    create_note("to delete", "content")
    result = delete_note("to_delete.md")
    assert "Deleted note" in result
    assert not (NOTES_DIR / "to_delete.md").exists()


def test_search_notes_finds_match():
    create_note("groceries", "eggs and milk")
    result = search_notes("eggs")
    assert "groceries.md" in result


def test_search_notes_no_match():
    create_note("groceries", "eggs and milk")
    result = search_notes("nonexistent")
    assert "No matches" in result


def test_list_notes_empty():
    result = list_notes()
    assert result == "No notes yet."


def test_list_notes_with_files():
    create_note("a", "content a")
    create_note("b", "content b")
    result = list_notes()
    assert "a.md" in result
    assert "b.md" in result