from pathlib import Path
import re


def load_java(file_path: str) -> dict:
    """
    Load a Java source file and return a normalized document.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".java":
        raise ValueError(f"Expected a Java file, got: {path.suffix}")

    content = path.read_text(encoding="utf-8", errors="ignore")

    # Extract package name
    package_match = re.search(
        r"package\s+([\w.]+)\s*;",
        content
    )

    package = (
        package_match.group(1)
        if package_match
        else None
    )

    # Extract class / interface name
    class_match = re.search(
        r"(?:class|interface|enum)\s+(\w+)",
        content
    )

    class_name = (
        class_match.group(1)
        if class_match
        else path.stem
    )

    return {
        "content": content,
        "metadata": {
            "source": path.name,
            "path": str(path),
            "type": "source_code",
            "language": "java",
            "package": package,
            "class": class_name
        }
    }