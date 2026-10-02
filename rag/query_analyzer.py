from typing import Dict, List


class QueryAnalyzer:
    """
    Analyze a query before retrieving information
    from the knowledge base.
    """

    DOMAINS = {
        "authentication": [
            "authentication",
            "login",
            "logout",
            "signin",
            "sign in",
            "jwt",
            "token",
            "credential",
            "password",
            "user"
        ],

        "account_management": [
            "account",
            "income",
            "expense",
            "saving",
            "budget"
        ],

        "transactions": [
            "transaction",
            "income",
            "expense",
            "deposit",
            "withdraw"
        ],

        "statistics": [
            "statistics",
            "statistic",
            "chart",
            "data",
            "analytics"
        ]
    }

    INTENTS = {
        "test_generation": [
            "generate test",
            "test scenario",
            "test cases",
            "create test",
            "testing"
        ],

        "failure_analysis": [
            "failure",
            "failed",
            "error",
            "exception",
            "bug",
            "why did"
        ],

        "test_execution": [
            "execute",
            "run test",
            "run the test"
        ],

        "coverage_analysis": [
            "coverage",
            "uncovered",
            "missing test",
            "test coverage"
        ],

        "technical_analysis": [
            "architecture",
            "endpoint",
            "api",
            "microservice",
            "database",
            "docker",
            "service"
        ]
    }

    def detect_domain(self, query: str) -> str:

        query_lower = query.lower()

        scores = {}

        for domain, keywords in self.DOMAINS.items():

            score = sum(
                1
                for keyword in keywords
                if keyword in query_lower
            )

            scores[domain] = score

        best_domain = max(
            scores,
            key=scores.get
        )

        if scores[best_domain] == 0:
            return "general"

        return best_domain

    def detect_intent(self, query: str) -> str:

        query_lower = query.lower()

        scores = {}

        for intent, keywords in self.INTENTS.items():

            score = sum(
                1
                for keyword in keywords
                if keyword in query_lower
            )

            scores[intent] = score

        best_intent = max(
            scores,
            key=scores.get
        )

        if scores[best_intent] == 0:
            return "general"

        return best_intent

    def determine_knowledge_sources(
        self,
        intent: str
    ) -> List[str]:

        mapping = {

            "test_generation": [
                "business_logic",
                "technical_context",
                "source_code"
            ],

            "failure_analysis": [
                "technical_context",
                "source_code"
            ],

            "test_execution": [
                "technical_context",
                "source_code"
            ],

            "coverage_analysis": [
                "source_code",
                "technical_context"
            ],

            "technical_analysis": [
                "technical_context",
                "source_code"
            ],

            "general": [
                "business_logic",
                "technical_context",
                "source_code"
            ]
        }

        return mapping.get(
            intent,
            mapping["general"]
        )

    def expand_query(
        self,
        query: str,
        domain: str,
        intent: str
    ) -> str:

        expanded_query = query

        if domain == "authentication":

            expanded_query += (
                " authentication login logout "
                "JWT token credentials security user"
            )

        elif domain == "account_management":

            expanded_query += (
                " account management account-service "
                "income expense saving budget"
            )

        elif domain == "transactions":

            expanded_query += (
                " transactions income expense "
                "account operations"
            )

        elif domain == "statistics":

            expanded_query += (
                " statistics analytics charts "
                "statistic-service"
            )

        if intent == "test_generation":

            expanded_query += (
                " business rules validation "
                "API endpoint test scenarios edge cases"
            )

        elif intent == "failure_analysis":

            expanded_query += (
                " error logs exception implementation "
                "root cause source code"
            )

        elif intent == "coverage_analysis":

            expanded_query += (
                " methods classes branches "
                "uncovered code tests"
            )

        return expanded_query

    def analyze(
        self,
        query: str
    ) -> Dict:

        domain = self.detect_domain(query)

        intent = self.detect_intent(query)

        knowledge_sources = (
            self.determine_knowledge_sources(intent)
        )

        expanded_query = self.expand_query(
            query=query,
            domain=domain,
            intent=intent
        )

        return {
            "original_query": query,
            "domain": domain,
            "intent": intent,
            "knowledge_sources": knowledge_sources,
            "expanded_query": expanded_query
        }