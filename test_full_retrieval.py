from rag.retriever import Retriever
from rag.reranker import Reranker
from rag.context_builder import ContextBuilder


query = (
    "Generate authentication test scenarios "
    "for PiggyMetrics"
)


# ==========================================
# 1. RETRIEVE
# ==========================================

retriever = Retriever()

result = retriever.retrieve(
    query=query,
    top_k=10
)

chunks = result["chunks"]


# ==========================================
# 2. RERANK
# ==========================================

reranker = Reranker()

reranked_chunks = reranker.rerank(
    query=query,
    chunks=chunks,
    top_k=5
)


# ==========================================
# 3. BUILD CONTEXT
# ==========================================

context_builder = ContextBuilder()

context = context_builder.build_context(
    chunks=reranked_chunks
)


# ==========================================
# 4. DISPLAY
# ==========================================

print("\nQUERY ANALYSIS")

print(
    result["query_analysis"]
)


print("\nFINAL CONTEXT")

print(context)