"""Durable business-state schema for Support Foundation."""

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from xmg_qa2.infrastructure.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class SupportTaskRow(TimestampMixin, Base):
    __tablename__ = "support_task"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    case_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), index=True)
    customer_id: Mapped[str] = mapped_column(String(200))
    project_id: Mapped[str | None] = mapped_column(String(200))
    created_by_principal: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(30))
    state_version: Mapped[int] = mapped_column(Integer)
    workflow_name: Mapped[str] = mapped_column(String(200))
    workflow_version: Mapped[str] = mapped_column(String(100))
    question_text: Mapped[str] = mapped_column(Text)
    current_question_frame_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    current_run_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RunRow(TimestampMixin, Base):
    __tablename__ = "run"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"), index=True)
    status: Mapped[str] = mapped_column(String(30))
    workflow_version: Mapped[str] = mapped_column(String(100))
    lease_epoch: Mapped[int] = mapped_column(Integer)
    expected_task_version: Mapped[int] = mapped_column(Integer)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    stop_reason: Mapped[str | None] = mapped_column(String(200))
    trace_id: Mapped[str] = mapped_column(String(200), index=True)


class QuestionFrameRow(TimestampMixin, Base):
    __tablename__ = "question_frame"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"))
    version: Mapped[int] = mapped_column(Integer)
    original_question: Mapped[str] = mapped_column(Text)
    goal: Mapped[str] = mapped_column(Text)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class HumanRequestRow(TimestampMixin, Base):
    __tablename__ = "human_request"
    __table_args__ = (UniqueConstraint("task_id", "interrupt_id", "request_version"),)
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"))
    run_id: Mapped[UUID] = mapped_column(ForeignKey("run.id", ondelete="RESTRICT"))
    request_version: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30))
    interrupt_id: Mapped[str] = mapped_column(String(200))
    target_task_version: Mapped[int] = mapped_column(Integer)
    request_type: Mapped[str] = mapped_column(String(100))
    prompt: Mapped[str] = mapped_column(Text)
    required_fields: Mapped[dict[str, Any]] = mapped_column(JSON)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    superseded_by_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    satisfied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ResumeAttemptRow(TimestampMixin, Base):
    __tablename__ = "resume_attempt"
    __table_args__ = (UniqueConstraint("human_request_id", "reply_id"),)
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    human_request_id: Mapped[UUID] = mapped_column(ForeignKey("human_request.id", ondelete="RESTRICT"))
    reply_id: Mapped[str] = mapped_column(String(200))
    principal_id: Mapped[str] = mapped_column(String(200))
    target_task_version: Mapped[int] = mapped_column(Integer)
    target_interrupt_id: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(30))
    reason: Mapped[str | None] = mapped_column(String(300))
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    applied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EvidenceRow(TimestampMixin, Base):
    __tablename__ = "evidence"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"), index=True)
    kind: Mapped[str] = mapped_column(String(50))
    source_name: Mapped[str] = mapped_column(String(300))
    source_locator: Mapped[str | None] = mapped_column(Text)
    content_excerpt: Mapped[str | None] = mapped_column(Text)
    artifact_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    product: Mapped[str | None] = mapped_column(String(200))
    product_version: Mapped[str | None] = mapped_column(String(100))
    scope: Mapped[dict[str, Any]] = mapped_column(JSON)
    provenance: Mapped[dict[str, Any]] = mapped_column(JSON)
    hash: Mapped[str | None] = mapped_column(String(200))
    retrieval_score: Mapped[float | None] = mapped_column(Float)
    validated: Mapped[bool] = mapped_column(Boolean)


class ClaimEvidenceLinkRow(TimestampMixin, Base):
    __tablename__ = "claim_evidence_link"
    __table_args__ = (UniqueConstraint("task_id", "claim_id", "evidence_id", "relation"),)
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"))
    claim_id: Mapped[str] = mapped_column(String(200))
    evidence_id: Mapped[UUID] = mapped_column(ForeignKey("evidence.id", ondelete="RESTRICT"))
    relation: Mapped[str] = mapped_column(String(30))
    applicability: Mapped[dict[str, Any]] = mapped_column(JSON)


class AnswerDraftRow(TimestampMixin, Base):
    __tablename__ = "answer_draft"
    __table_args__ = (UniqueConstraint("task_id", "version"),)
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"))
    run_id: Mapped[UUID] = mapped_column(ForeignKey("run.id", ondelete="RESTRICT"))
    version: Mapped[int] = mapped_column(Integer)
    answer_kind: Mapped[str] = mapped_column(String(30))
    body_markdown: Mapped[str] = mapped_column(Text)
    covered_subquestion_ids: Mapped[list[str]] = mapped_column(JSON)
    pending_items: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
    citation_map: Mapped[dict[str, Any]] = mapped_column(JSON)
    draft_hash: Mapped[str] = mapped_column(String(200))


class AnswerCheckRow(TimestampMixin, Base):
    __tablename__ = "answer_check"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"))
    answer_draft_id: Mapped[UUID] = mapped_column(ForeignKey("answer_draft.id", ondelete="RESTRICT"))
    draft_hash: Mapped[str] = mapped_column(String(200))
    evidence_set_hash: Mapped[str] = mapped_column(String(200))
    passed: Mapped[bool] = mapped_column(Boolean)
    issues: Mapped[dict[str, Any]] = mapped_column(JSON)
    required_action: Mapped[str] = mapped_column(String(30))


class OperationCommitRow(TimestampMixin, Base):
    __tablename__ = "operation_commit"
    __table_args__ = (UniqueConstraint("task_id", "operation_id"),)
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"))
    run_id: Mapped[UUID] = mapped_column(ForeignKey("run.id", ondelete="RESTRICT"))
    operation_id: Mapped[str] = mapped_column(String(200))
    lease_epoch: Mapped[int] = mapped_column(Integer)
    task_version_before: Mapped[int] = mapped_column(Integer)
    task_version_after: Mapped[int] = mapped_column(Integer)
    operation_type: Mapped[str] = mapped_column(String(100))
    result_digest: Mapped[str] = mapped_column(String(200))
    committed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class EventRow(TimestampMixin):
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID | None] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"))
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class InboxEventRow(EventRow, Base):
    __tablename__ = "inbox_event"
    __table_args__ = (UniqueConstraint("source_connection", "source_event_id"),)
    source_connection: Mapped[str] = mapped_column(String(200))
    source_event_id: Mapped[str] = mapped_column(String(200))


class OutboxEventRow(EventRow, Base):
    __tablename__ = "outbox_event"
    topic: Mapped[str] = mapped_column(String(200))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AuditEventRow(EventRow, Base):
    __tablename__ = "audit_event"
    principal_id: Mapped[str] = mapped_column(String(200))
    action: Mapped[str] = mapped_column(String(200))
    result: Mapped[str] = mapped_column(String(100))
    trace_id: Mapped[str] = mapped_column(String(200))


class ArtifactRow(TimestampMixin, Base):
    __tablename__ = "artifact"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("support_task.id", ondelete="RESTRICT"))
    kind: Mapped[str] = mapped_column(String(100))
    storage_locator: Mapped[str] = mapped_column(Text)
    mime_type: Mapped[str] = mapped_column(String(200))
    size_bytes: Mapped[int] = mapped_column(Integer)
    sha256: Mapped[str] = mapped_column(String(64))
    scope: Mapped[dict[str, Any]] = mapped_column(JSON)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
