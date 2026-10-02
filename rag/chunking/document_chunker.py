from typing import List, Dict


def chunk_document(
    document: Dict,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Dict]:
    """
    Split a normalized document into overlapping text chunks.

    Parameters
    ----------
    document : dict
        Normalized document containing:
        {
            "content": str,
            "metadata": dict
        }

    chunk_size : int
        Maximum number of characters per chunk.

    chunk_overlap : int
        Number of overlapping characters between chunks.

    Returns
    -------
    List[dict]
        List of chunked documents with inherited metadata.
    """

    content = document.get("content", "")
    metadata = document.get("metadata", {})

    if not content.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0
    chunk_index = 0
    content_length = len(content)

    while start < content_length:

        end = start + chunk_size

        chunk_content = content[start:end]

        chunk_metadata = metadata.copy()

        source_path = metadata.get("path") or metadata.get("source", "unknown")
        chunk_metadata.update({
            "chunk_index": chunk_index,
            "chunk_id": (
                f"{source_path}_chunk_{chunk_index}"
            )
        })

        chunks.append({
            "content": chunk_content,
            "metadata": chunk_metadata
        })

        chunk_index += 1

        start += chunk_size - chunk_overlap

    return chunks