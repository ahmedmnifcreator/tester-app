from typing import List, Dict
import chromadb


class VectorStore:
    """
    Manage storage and retrieval of document embeddings using ChromaDB.
    """

    def __init__(
        self,
        persist_directory: str = "rag/chroma_db",
        collection_name: str = "piggymetrics_knowledge"
    ):

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]]
    ):
        """
        Store chunks, embeddings and metadata in ChromaDB.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings"
            )

        ids = []
        documents = []
        metadatas = []
        unique_embeddings = []

        for chunk, embedding in zip(chunks, embeddings):
            chunk_metadata = chunk.get("metadata", {})
            chunk_id = chunk_metadata.get("chunk_id")

            if not chunk_id:
                source = chunk_metadata.get("source", "unknown")
                chunk_index = chunk_metadata.get("chunk_index", len(ids))
                chunk_id = f"{source}_chunk_{chunk_index}"
                chunk_metadata["chunk_id"] = chunk_id
                chunk["metadata"] = chunk_metadata

            normalized_id = str(chunk_id)
            if normalized_id in ids:
                normalized_id = f"{normalized_id}_{len(ids)}"
                chunk_metadata["chunk_id"] = normalized_id
                chunk["metadata"] = chunk_metadata

            ids.append(normalized_id)
            documents.append(chunk["content"])
            metadatas.append(chunk_metadata)
            unique_embeddings.append(embedding)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=unique_embeddings,
            metadatas=metadatas
        )

    def get_collection_count(self) -> int:
        """
        Return the number of stored chunks.
        """

        return self.collection.count()

    def delete_collection(self):
        """
        Delete the current collection.
        """

        self.client.delete_collection(
            self.collection.name
        )