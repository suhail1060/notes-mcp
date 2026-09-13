from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("notes-mcp")

# Directory where actual note files live
NOTES_DIR = Path(__file__).parent.parent / "data" / "notes"
NOTES_DIR.mkdir(parents=True, exist_ok=True)


@mcp.resource("notes://list")
def list_notes() -> str:
    """List all available notes."""
    files = sorted(f.name for f in NOTES_DIR.glob("*.md"))
    return "\n".join(files) if files else "No notes yet."


@mcp.tool()
def create_note(title: str, content: str) -> str:
    """Create a new note with the given title and content."""
    filename = f"{title.lower().replace(' ', '_')}.md"
    path = NOTES_DIR / filename
    if path.exists():
        return f"Note '{filename}' already exists."
    path.write_text(content)
    return f"Created note: {filename}"


@mcp.tool()
def delete_note(filename: str) -> str:
    """Delete a note by filename (e.g. 'my_note.md')."""
    path = NOTES_DIR / filename
    if not path.exists():
        return f"Note '{filename}' not found."
    path.unlink()
    return f"Deleted note: {filename}"


@mcp.tool()
def search_notes(query: str) -> str:
    """Search note contents for a query string. Returns matching filenames."""
    matches = [
        f.name for f in NOTES_DIR.glob("*.md")
        if query.lower() in f.read_text().lower()
    ]
    return "\n".join(matches) if matches else "No matches found."


@mcp.prompt()
def summarize_note(filename: str) -> str:
    """Generate a prompt asking the LLM to summarize a given note."""
    path = NOTES_DIR / filename
    if not path.exists():
        return f"Note '{filename}' not found."
    content = path.read_text()
    return (
        f"Summarize the following note in 2-3 sentences.\n\n"
        f"Title: {filename}\n"
        f"Content:\n{content}"
    )

if __name__ == "__main__":
    mcp.run(transport="stdio")