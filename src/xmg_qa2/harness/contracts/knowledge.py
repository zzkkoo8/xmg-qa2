"""Evidence-producing knowledge-provider contract."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from xmg_qa2.harness.contracts.common import InvocationContext


@dataclass(frozen=True, slots=True)
class KnowledgeQuery:
    capability_id: str
    query: str
    product: str | None
    product_version: str | None
    filters: Mapping[str, Any]
    limit: int
    context: InvocationContext


@dataclass(frozen=True, slots=True)
class EvidenceCandidate:
    source_name: str
    source_locator: str | None
    excerpt: str
    collected_at: str
    product: str | None
    product_version: str | None
    retrieval_score: float | None
    provenance: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class KnowledgeSearchResult:
    items: Sequence[EvidenceCandidate]
    provider_request_id: str | None
    exhausted: bool


class KnowledgeProvider(Protocol):
    async def search(self, request: KnowledgeQuery) -> KnowledgeSearchResult: ...
