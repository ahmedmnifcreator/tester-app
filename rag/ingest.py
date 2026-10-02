import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from rag.loaders.markdown_loader import load_markdown
from rag.loaders.java_loader import load_java
from rag.loaders.yaml_loader import load_yaml
from rag.loaders.json_loader import load_json

from rag.chunking.document_chunker import chunk_document
from rag.chunking.code_chunker import chunk_code

from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore


KNOWLEDGE_INPUT = Path("knowledge_input")


def load_file(file_path: Path):
    """
    Select the appropriate loader according to file extension.
    """

    suffix = file_path.suffix.lower()

    if suffix == ".md":
        return load_markdown(str(file_path))

    elif suffix == ".java":
        return load_java(str(file_path))

    elif suffix in [".yaml", ".yml"]:
        return load_yaml(str(file_path))

    elif suffix == ".json":
        return load_json(str(file_path))

    return None


def chunk_document_by_type(document):
    """
    Select the appropriate chunker.
    """

    metadata = document.get("metadata", {})

    language = metadata.get("language", "")
    file_type = metadata.get("type", "")

    if language == "java" or file_type == "source_code":
        return chunk_code(document)

    return chunk_document(document)


def collect_chunks(root_directory: Path):
    """
    Scan the knowledge_input directory and transform all
    supported files into chunks.
    """

    all_chunks = []

    supported_extensions = {
        ".md",
        ".java",
        ".yaml",
        ".yml",
        ".json"
    }

    for file_path in root_directory.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        print(f"\nProcessing: {file_path}")

        try:

            document = load_file(file_path)

            if document is None:
                print("Unsupported file.")
                continue

            chunks = chunk_document_by_type(document)

            print(f"Generated {len(chunks)} chunks")

            all_chunks.extend(chunks)

        except Exception as error:

            print(
                f"Error processing {file_path}: {error}"
            )

    return all_chunks


def ingest():
    """
    Complete ingestion pipeline.
    """

    print("=" * 60)
    print("STARTING KNOWLEDGE INGESTION")
    print("=" * 60)

    chunks = collect_chunks(KNOWLEDGE_INPUT)

    if not chunks:

        print("\nNo chunks generated.")
        return

    print("\n" + "=" * 60)
    print(f"TOTAL CHUNKS: {len(chunks)}")
    print("=" * 60)

    print("\nLoading embedding model...")

    embedding_model = EmbeddingModel()

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    print("\nGenerating embeddings...")

    embeddings = embedding_model.embed_documents(
        texts
    )

    print("\nConnecting to ChromaDB...")

    vector_store = VectorStore()

    print("\nStoring chunks in ChromaDB...")

    vector_store.add_documents(
        chunks=chunks,
        embeddings=embeddings
    )

    print("\n" + "=" * 60)
    print("INGESTION COMPLETED")
    print(
        "TOTAL DOCUMENTS IN DATABASE:",
        vector_store.get_collection_count()
    )
    print("=" * 60)


if __name__ == "__main__":
    ingest()