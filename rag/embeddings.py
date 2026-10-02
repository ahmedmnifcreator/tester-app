from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Wrapper around SentenceTransformer for generating embeddings.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list:
        """
        Generate an embedding for a single text.
        """

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """

        embeddings = self.model.encode(
            documents,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings.tolist()