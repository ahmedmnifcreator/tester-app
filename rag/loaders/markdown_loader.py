from pathlib import Path


def load_markdown(file_path: str) -> dict:
    """
    Load a Markdown file and return a normalized document.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".md":
        raise ValueError(f"Expected a Markdown file, got: {path.suffix}")

    content = path.read_text(encoding="utf-8")

    return {
        "content": content,
        "metadata": {
            "source": path.name,
            "path": str(path),
            "type": "markdown"
        }
    }