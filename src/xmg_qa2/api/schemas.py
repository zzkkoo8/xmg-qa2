"""HTTP request and projection schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class CreateTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=1, max_length=20_000)
    customer_id: str = Field(min_length=1)
    project_id: str | None = None
    case_id: UUID | None = None
    client_message_id: str | None = None


class TaskReplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: UUID
    request_version: int
    reply_id: str = Field(min_length=1)
    content: str = Field(min_length=1, max_length=20_000)


class CancelTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reason: str | None = Field(default=None, max_length=1000)


class TaskAccepted(BaseModel):
    task_id: UUID
    case_id: UUID
    status: str
    state_version: int


class TaskSummary(BaseModel):
    task_id: UUID
    case_id: UUID
    status: str
    question: str
    state_version: int
    updated_at: datetime


class TaskDetail(TaskSummary):
    customer_id: str
    project_id: str | None
    pending_requests: list[dict[str, object]]
    answer: dict[str, object] | None
