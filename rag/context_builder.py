from typing import List, Dict


class ContextBuilder:
    """
    Build a structured context from reranked chunks.
    """

    def categorize_chunk(
        self,
        metadata: Dict
    ) -> str:

        source = metadata.get(
            "source",
            ""
        ).lower()

        file_type = metadata.get(
            "type",
            ""
        ).lower()


        # ==========================================
        # BUSINESS LOGIC
        # ==========================================

        if (
            "business_logic" in source
            or source.endswith(".md")
            and any(
                keyword in source
                for keyword in [
                    "authentication",
                    "account_management",
                    "transactions",
                    "statistics"
                ]
            )
        ):
            return "BUSINESS LOGIC"


        # ==========================================
        # TECHNICAL CONTEXT
        # ==========================================

        if (
            "technical_context" in source
            or any(
                keyword in source
                for keyword in [
                    "architecture",
                    "microservices",
                    "api",
                    "docker",
                    "database"
                ]
            )
        ):
            return "TECHNICAL CONTEXT"


        # ==========================================
        # SOURCE CODE
        # ==========================================

        if (
            file_type == "java"
            or source.endswith(".java")
            or file_type == "source_code"
        ):
            return "SOURCE CODE"


        # ==========================================
        # CONFIGURATION
        # ==========================================

        if (
            source.endswith(".yaml")
            or source.endswith(".yml")
            or source.endswith(".json")
            or file_type in [
                "yaml",
                "json"
            ]
        ):
            return "CONFIGURATION"


        return "OTHER KNOWLEDGE"


    def build_context(
        self,
        chunks: List[Dict],
        max_chunks: int = 5
    ) -> str:

        if not chunks:
            return "No relevant knowledge found."


        categorized_chunks = {}


        # ==========================================
        # CATEGORIZE CHUNKS
        # ==========================================

        for chunk in chunks[:max_chunks]:

            metadata = chunk.get(
                "metadata",
                {}
            )

            category = self.categorize_chunk(
                metadata
            )

            if category not in categorized_chunks:

                categorized_chunks[
                    category
                ] = []


            categorized_chunks[
                category
            ].append(chunk)


        # ==========================================
        # BUILD FINAL CONTEXT
        # ==========================================

        context_parts = []


        for category, category_chunks in (
            categorized_chunks.items()
        ):

            context_parts.append(
                "\n"
                + "=" * 80
                + f"\n{category}\n"
                + "=" * 80
            )


            for index, chunk in enumerate(
                category_chunks,
                start=1
            ):

                metadata = chunk.get(
                    "metadata",
                    {}
                )

                source = metadata.get(
                    "source",
                    "Unknown source"
                )

                content = chunk.get(
                    "content",
                    ""
                )

                score = chunk.get(
                    "rerank_score",
                    None
                )


                context_parts.append(
                    f"\n[CHUNK {index}]"
                )

                context_parts.append(
                    f"Source: {source}"
                )


                if score is not None:

                    context_parts.append(
                        f"Relevance score: "
                        f"{score:.4f}"
                    )


                context_parts.append(
                    "\nCONTENT:\n"
                    + content
                )


        return "\n".join(context_parts)