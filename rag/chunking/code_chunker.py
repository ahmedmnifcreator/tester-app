import re
from typing import Dict, List


def extract_java_context(content: str) -> str:
    """
    Extract package and import statements.
    This context will be added to each code chunk.
    """

    package_match = re.search(
        r"package\s+[\w.]+\s*;",
        content
    )

    package = (
        package_match.group(0)
        if package_match
        else ""
    )

    imports = re.findall(
        r"import\s+[\w.*]+\s*;",
        content
    )

    context_parts = []

    if package:
        context_parts.append(package)

    if imports:
        context_parts.extend(imports)

    return "\n".join(context_parts)


def extract_class_name(content: str) -> str:
    """
    Extract the main Java class, interface, or enum name.
    """

    match = re.search(
        r"(?:public\s+)?(?:abstract\s+)?"
        r"(?:class|interface|enum)\s+(\w+)",
        content
    )

    return match.group(1) if match else "Unknown"


def split_java_methods(content: str) -> List[str]:
    """
    Basic Java method splitter.

    V1 strategy:
    Detect possible method declarations and split before them.
    """

    pattern = (
        r"(?=^\s*"
        r"(?:@\w+(?:\([^)]*\))?\s*)*"
        r"(?:public|private|protected)"
        r"(?:static\s+)?"
        r"[\w<>\[\], ?]+\s+"
        r"\w+\s*\([^)]*\)"
        r"(?:\s*throws\s+[\w,\s]+)?"
        r"\s*\{)"
    )

    parts = re.split(
        pattern,
        content,
        flags=re.MULTILINE
    )

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def split_large_code(
    content: str,
    chunk_size: int,
    chunk_overlap: int
) -> List[str]:
    """
    Split large code blocks when they exceed chunk_size.
    """

    if len(content) <= chunk_size:
        return [content]

    chunks = []
    start = 0

    while start < len(content):

        end = min(
            start + chunk_size,
            len(content)
        )

        if end < len(content):

            newline = content.rfind(
                "\n",
                start,
                end
            )

            if newline > start:
                end = newline

        chunk = content[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(content):
            break

        start = end - chunk_overlap

    return chunks


def chunk_code(
    document: Dict,
    chunk_size: int = 1500,
    chunk_overlap: int = 200
) -> List[Dict]:
    """
    Chunk a normalized Java document.

    Each chunk contains:
    - package/import context
    - class information
    - method or code block
    - inherited metadata
    """

    content = document.get("content", "")
    metadata = document.get("metadata", {})

    if not content.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    java_context = extract_java_context(content)

    class_name = (
        metadata.get("class")
        or extract_class_name(content)
    )

    code_parts = split_java_methods(content)

    chunks = []
    chunk_index = 0

    for part in code_parts:

        sub_chunks = split_large_code(
            content=part,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for sub_chunk in sub_chunks:

            # Add Java context only if it is not already present
            chunk_content = sub_chunk

            if java_context and not sub_chunk.startswith("package"):
                chunk_content = (
                    f"{java_context}\n\n"
                    f"// Class: {class_name}\n\n"
                    f"{sub_chunk}"
                )

            chunk_metadata = metadata.copy()

            source_path = metadata.get("path") or metadata.get("source", "unknown")
            chunk_metadata.update({
                "chunk_index": chunk_index,
                "chunk_id": (
                    f"{source_path}_chunk_{chunk_index}"
                ),
                "class": class_name,
                "chunk_type": "code"
            })

            chunks.append({
                "content": chunk_content,
                "metadata": chunk_metadata
            })

            chunk_index += 1

    return chunks