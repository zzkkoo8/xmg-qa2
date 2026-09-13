"""Scenario-keyed fake Knowledge Contract implementation."""

from collections.abc import Mapping, Sequence
from typing import Any

from xmg_qa2.harness.contracts.knowledge import (
    EvidenceCandidate,
    KnowledgeQuery,
    KnowledgeSearchResult,
)


class FakeKnowledgeProvider:
    def __init__(self, results: Mapping[str, Sequence[Mapping[str, Any]]]) -> None:
        self._results = results

    async def search(self, request: KnowledgeQuery) -> KnowledgeSearchResult:
        scenario = request.filters.get("scenario")
        items = self._results.get(str(scenario), ())[: request.limit]
        candidates = tuple(
            EvidenceCandidate(
                source_name=str(item["source_name"]),
                source_locator=item.get("source_locator"),
                excerpt=str(item["excerpt"]),
                collected_at=str(item.get("collected_at", "2026-09-14T00:00:00Z")),
                product=item.get("product"),
                product_version=item.get("product_version"),
                retrieval_score=item.get("retrieval_score"),
                provenance={"evidence_id": item["id"], **item.get("provenance", {})},
            )
            for item in items
        )
        return KnowledgeSearchResult(candidates, f"fake-knowledge:{scenario}", not candidates)
