from rag.retriever import Retriever
from rag.reranker import Reranker
from rag.context_builder import ContextBuilder


class RAGPipeline:
    """
    Main entry point for the RAG system.

    Pipeline:
    Query
        -> Query Analyzer
        -> Retriever
        -> Reranker
        -> Context Builder
        -> Final Context
    """

    def __init__(
        self,
        collection_name: str = "piggymetrics_knowledge",
        retrieval_top_k: int = 10,
        rerank_top_k: int = 5
    ):

        self.retrieval_top_k = retrieval_top_k
        self.rerank_top_k = rerank_top_k

        self.retriever = Retriever(
            collection_name=collection_name
        )

        self.reranker = Reranker()

        self.context_builder = ContextBuilder()

    def query(
        self,
        query: str
    ) -> dict:

        # ==========================================
        # 1. RETRIEVE
        # ==========================================

        retrieval_result = self.retriever.retrieve(
            query=query,
            top_k=self.retrieval_top_k
        )

        query_analysis = (
            retrieval_result["query_analysis"]
        )

        retrieved_chunks = (
            retrieval_result["chunks"]
        )

        # ==========================================
        # 2. RERANK
        # ==========================================

        reranked_chunks = self.reranker.rerank(
            query=query,
            chunks=retrieved_chunks,
            top_k=self.rerank_top_k
        )

        # ==========================================
        # 3. BUILD CONTEXT
        # ==========================================

        context = self.context_builder.build_context(
            chunks=reranked_chunks,
            max_chunks=self.rerank_top_k
        )

        # ==========================================
        # 4. FINAL RESULT
        # ==========================================

        return {
            "query": query,

            "query_analysis": query_analysis,

            "retrieved_chunks": retrieved_chunks,

            "reranked_chunks": reranked_chunks,

            "context": context
        }