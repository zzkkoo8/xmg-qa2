"""Evidence and claim linkage owned by the support domain."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID


class EvidenceKind(StrEnum):
    DOCUMENT = "DOCUMENT"
    WEB = "WEB"
    API = "API"
    TOOL_OBSERVATION = "TOOL_OBSERVATION"
    USER_PROVIDED = "USER_PROVIDED"
    SYSTEM_RECORD = "SYSTEM_RECORD"


class EvidenceRelation(StrEnum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    CONTEXT = "CONTEXT"


@dataclass(frozen=True, slots=True)
class Evidence:
    id: UUID
    task_id: UUID
    kind: EvidenceKind
    source_name: str
    collected_at: datetime
    scope: Mapping[str, Any]
    provenance: Mapping[str, Any]
    created_at: datetime
    source_locator: str | None = None
    content_excerpt: str | None = None
    artifact_id: UUID | None = None
    product: str | None = None
    product_version: str | None = None
    hash: str | None = None
    retrieval_score: float | None = None
    validated: bool = False


@dataclass(frozen=True, slots=True)
class ClaimEvidenceLink:
    id: UUID
    task_id: UUID
    claim_id: str
    evidence_id: UUID
    relation: EvidenceRelation
    created_at: datetime
    applicability: Mapping[str, Any] = field(default_factory=dict)
