"""Framework-independent question and answer records."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from xmg_qa2.domain.errors import DraftHashMismatch


class SubquestionStatus(StrEnum):
    OPEN = "OPEN"
    ANSWERED = "ANSWERED"
    PARTIAL = "PARTIAL"
    BLOCKED = "BLOCKED"


class AnswerKind(StrEnum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    NEEDS_INPUT = "NEEDS_INPUT"
    UNABLE_TO_CONCLUDE = "UNABLE_TO_CONCLUDE"


class RequiredAction(StrEnum):
    PASS = "PASS"
    REVISE = "REVISE"
    INVESTIGATE = "INVESTIGATE"
    REQUEST_INPUT = "REQUEST_INPUT"
    FAIL = "FAIL"


@dataclass(frozen=True, slots=True)
class Subquestion:
    id: str
    text: str
    status: SubquestionStatus
    critical: bool = False
    required_claims: tuple[str, ...] = ()

    @property
    def is_pending(self) -> bool:
        return self.status is not SubquestionStatus.ANSWERED


@dataclass(frozen=True, slots=True)
class QuestionFrame:
    id: UUID
    task_id: UUID
    version: int
    original_question: str
    goal: str
    environment: Mapping[str, Any] = field(default_factory=dict)
    known_facts: tuple[Mapping[str, Any], ...] = ()
    unknowns: tuple[Mapping[str, Any], ...] = ()
    subquestions: tuple[Subquestion, ...] = ()
    answer_conditions: tuple[Mapping[str, Any], ...] = ()
    user_preferences: Mapping[str, Any] = field(default_factory=dict)
    source_event_ids: tuple[UUID, ...] = ()
    created_at: datetime | None = None

    @property
    def has_critical_pending_subquestions(self) -> bool:
        return any(item.critical and item.is_pending for item in self.subquestions)


@dataclass(frozen=True, slots=True)
class AnswerDraft:
    id: UUID
    task_id: UUID
    run_id: UUID
    version: int
    answer_kind: AnswerKind
    body_markdown: str
    draft_hash: str
    created_at: datetime
    covered_subquestion_ids: tuple[str, ...] = ()
    pending_items: tuple[Mapping[str, Any], ...] = ()
    citation_map: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AnswerCheck:
    id: UUID
    task_id: UUID
    answer_draft_id: UUID
    draft_hash: str
    evidence_set_hash: str
    passed: bool
    required_action: RequiredAction
    created_at: datetime
    coverage_issues: tuple[Mapping[str, Any], ...] = ()
    unsupported_claims: tuple[Mapping[str, Any], ...] = ()
    policy_issues: tuple[Mapping[str, Any], ...] = ()
    version_conflicts: tuple[Mapping[str, Any], ...] = ()

    def validate_for(self, draft: AnswerDraft) -> None:
        if (
            self.answer_draft_id != draft.id
            or self.task_id != draft.task_id
            or self.draft_hash != draft.draft_hash
        ):
            raise DraftHashMismatch("answer check does not match answer draft")
