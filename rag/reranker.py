from sentence_transformers import CrossEncoder


class Reranker:
    """
    Rerank retrieved chunks using a Cross-Encoder.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):

        print(f"Loading reranker model: {model_name}")

        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        chunks: list,
        top_k: int = 5
    ) -> list:
        """
        Reorder chunks according to their relevance
        to the user query.
        """

        if not chunks:
            return []

        pairs = [
            (query, chunk["content"])
            for chunk in chunks
        ]

        scores = self.model.predict(pairs)

        scored_chunks = []

        for chunk, score in zip(chunks, scores):

            chunk_copy = chunk.copy()

            chunk_copy["rerank_score"] = float(score)

            scored_chunks.append(chunk_copy)

        scored_chunks.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return scored_chunks[:top_k]