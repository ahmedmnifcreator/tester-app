from pathlib import Path
import json


def load_json(file_path: str) -> dict:
    """
    Load a JSON file and return a normalized document.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".json":
        raise ValueError(
            f"Expected a JSON file, got: {path.suffix}"
        )

    content = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON file: {file_path}"
        ) from e

    return {
        "content": content,
        "metadata": {
            "source": path.name,
            "path": str(path),
            "type": "structured_data",
            "format": "json"
        },
        "data": data
    }