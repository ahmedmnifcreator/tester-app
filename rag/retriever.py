from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore
from rag.query_analyzer import QueryAnalyzer


class Retriever:

    def __init__(
        self,
        collection_name: str = "piggymetrics_knowledge"
    ):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore(
            collection_name=collection_name
        )

        self.query_analyzer = QueryAnalyzer()


    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        # ==========================================
        # 1. ANALYZE THE QUERY
        # ==========================================

        analysis = self.query_analyzer.analyze(query)

        expanded_query = analysis["expanded_query"]

        knowledge_sources = analysis["knowledge_sources"]


        # ==========================================
        # 2. CREATE QUERY EMBEDDING
        # ==========================================

        query_embedding = (
            self.embedding_model.embed_text(
                expanded_query
            )
        )


        # ==========================================
        # 3. SEARCH CHROMADB
        # ==========================================

        results = self.vector_store.collection.query(
            query_embeddings=[
                query_embedding
            ],

            n_results=top_k,

            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )


        # ==========================================
        # 4. FORMAT RESULTS
        # ==========================================

        retrieved_chunks = []

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]


        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_chunks.append({

                "content": document,

                "metadata": metadata,

                "distance": distance

            })


        return {

            "query_analysis": analysis,

            "chunks": retrieved_chunks

        }