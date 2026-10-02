from rag.pipeline import RAGPipeline


# ============================================================
# CONFIGURATION
# ============================================================

QUERY = "Generate authentication test scenarios for PiggyMetrics"


# ============================================================
# CREATE RAG PIPELINE
# ============================================================

rag = RAGPipeline(
    collection_name="piggymetrics_knowledge",
    retrieval_top_k=10,
    rerank_top_k=5
)


# ============================================================
# EXECUTE RAG
# ============================================================

result = rag.query(QUERY)


# ============================================================
# 1. ORIGINAL QUERY
# ============================================================

print("\n" + "=" * 100)
print("1. ORIGINAL QUERY")
print("=" * 100)

print(result["query"])


# ============================================================
# 2. QUERY ANALYSIS
# ============================================================

print("\n" + "=" * 100)
print("2. QUERY ANALYSIS")
print("=" * 100)

analysis = result["query_analysis"]

for key, value in analysis.items():
    print(f"\n{key.upper()}:")

    if isinstance(value, list):
        for item in value:
            print(f"  - {item}")
    else:
        print(f"  {value}")


# ============================================================
# 3. RETRIEVED CHUNKS
# ============================================================

print("\n" + "=" * 100)
print("3. RETRIEVED CHUNKS")
print("=" * 100)

for i, chunk in enumerate(result["retrieved_chunks"], start=1):

    metadata = chunk.get("metadata", {})
    content = chunk.get("content", "")
    distance = chunk.get("distance", "N/A")

    print(f"\n{'-' * 100}")
    print(f"CHUNK #{i}")
    print(f"{'-' * 100}")

    print("Knowledge type:",
          metadata.get("knowledge_type", "Unknown"))

    print("Source:",
          metadata.get("source", "Unknown"))

    print("File type:",
          metadata.get("file_type", "Unknown"))

    print("Vector distance:",
          distance)

    print("\nCONTENT:")

    print(content[:1000])

    if len(content) > 1000:
        print("\n... [TRUNCATED]")


# ============================================================
# 4. RERANKED CHUNKS
# ============================================================

print("\n" + "=" * 100)
print("4. RERANKED CHUNKS")
print("=" * 100)

for i, chunk in enumerate(result["reranked_chunks"], start=1):

    metadata = chunk.get("metadata", {})
    content = chunk.get("content", "")

    score = chunk.get(
        "rerank_score",
        "N/A"
    )

    print(f"\n{'-' * 100}")
    print(f"RANK #{i}")
    print(f"{'-' * 100}")

    print("Knowledge type:",
          metadata.get("knowledge_type", "Unknown"))

    print("Source:",
          metadata.get("source", "Unknown"))

    print("Rerank score:",
          score)

    print("\nCONTENT:")

    print(content[:1000])

    if len(content) > 1000:
        print("\n... [TRUNCATED]")


# ============================================================
# 5. FINAL CONTEXT
# ============================================================

print("\n" + "=" * 100)
print("5. FINAL CONTEXT")
print("=" * 100)

print(result["context"])