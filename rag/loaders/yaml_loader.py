from pathlib import Path
import yaml


def load_yaml(file_path: str) -> dict:
    """
    Load a YAML file and return a normalized document.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() not in [".yaml", ".yml"]:
        raise ValueError(
            f"Expected a YAML file, got: {path.suffix}"
        )

    content = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(
            f"Invalid YAML file: {file_path}"
        ) from e

    return {
        "content": content,
        "metadata": {
            "source": path.name,
            "path": str(path),
            "type": "configuration",
            "format": "yaml"
        },
        "data": data
    }