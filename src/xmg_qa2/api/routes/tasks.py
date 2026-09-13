from datetime import UTC, datetime
from typing import Annotated, cast
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select

from xmg_qa2.api.deps import Principal, assert_case_access, current_principal
from xmg_qa2.api.schemas import (
    CancelTaskRequest,
    CreateTaskRequest,
    TaskAccepted,
    TaskDetail,
    TaskReplyRequest,
    TaskSummary,
)
from xmg_qa2.infrastructure.db.models import AuditEventRow, OutboxEventRow, SupportTaskRow

router = APIRouter()


def project(row: SupportTaskRow) -> TaskSummary:
    return TaskSummary(
        task_id=row.id,
        case_id=row.case_id,
        status=row.status,
        question=row.question_text,
        state_version=row.state_version,
        updated_at=row.updated_at,
    )


@router.post("/tasks", status_code=202, operation_id="createTask", response_model=TaskAccepted)
def create_task(
    body: CreateTaskRequest,
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
) -> TaskAccepted:
    now = datetime.now(UTC)
    case_id = body.case_id or uuid4()
    if body.case_id is not None:
        assert_case_access(request, principal, case_id)
    else:
        request.app.state.users_by_id[principal.id].case_ids.add(case_id)
    task = SupportTaskRow(
        id=uuid4(),
        case_id=case_id,
        customer_id=body.customer_id,
        project_id=body.project_id,
        created_by_principal=principal.id,
        status="NEW",
        state_version=1,
        workflow_name="support",
        workflow_version="support-foundation-v1",
        question_text=body.question,
        created_at=now,
        updated_at=now,
    )
    with request.app.state.sessions.begin() as session:
        session.add(task)
        session.flush()
        session.add(
            OutboxEventRow(
                id=uuid4(),
                task_id=task.id,
                topic="task.created",
                payload={"task_id": str(task.id), "expected_task_version": 1},
                created_at=now,
            )
        )
    return TaskAccepted(task_id=task.id, case_id=case_id, status=task.status, state_version=1)


@router.get("/tasks", operation_id="listTasks", response_model=list[TaskSummary])
def list_tasks(
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
    status: str | None = None,
    limit: int = 50,
) -> list[TaskSummary]:
    user = request.app.state.users_by_id[principal.id]
    with request.app.state.sessions() as session:
        statement = select(SupportTaskRow).limit(min(max(limit, 1), 100))
        if "admin" not in principal.roles:
            statement = statement.where(SupportTaskRow.case_id.in_(user.case_ids))
        if status:
            statement = statement.where(SupportTaskRow.status == status)
        return [project(row) for row in session.scalars(statement)]


def authorized_task(request: Request, principal: Principal, task_id: UUID) -> SupportTaskRow:
    with request.app.state.sessions() as session:
        row = session.get(SupportTaskRow, task_id)
        if row is None:
            raise HTTPException(404, "task not found")
        assert_case_access(request, principal, row.case_id)
        session.expunge(row)
        return cast(SupportTaskRow, row)


@router.get("/tasks/{task_id}", operation_id="getTask", response_model=TaskDetail)
def get_task(
    task_id: UUID,
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
) -> TaskDetail:
    row = authorized_task(request, principal, task_id)
    return TaskDetail(
        **project(row).model_dump(),
        customer_id=row.customer_id,
        project_id=row.project_id,
        pending_requests=[],
        answer=None,
    )


@router.post("/tasks/{task_id}/cancel", status_code=202, operation_id="cancelTask")
def cancel_task(
    task_id: UUID,
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
    body: CancelTaskRequest | None = None,
) -> Response:
    row = authorized_task(request, principal, task_id)
    if row.status in {"CLOSED", "CANCELLED"}:
        raise HTTPException(409, "task cannot be cancelled")
    with request.app.state.sessions.begin() as session:
        current = session.get(SupportTaskRow, task_id)
        assert current is not None
        current.status = "CANCELLED"
        current.state_version += 1
        current.updated_at = datetime.now(UTC)
    return Response(status_code=202)


@router.post("/tasks/{task_id}/reply", status_code=202, operation_id="replyToTask")
def reply_to_task(
    task_id: UUID,
    body: TaskReplyRequest,
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
) -> dict[str, str]:
    authorized_task(request, principal, task_id)
    return {"resume_attempt_id": str(uuid4()), "status": "RECEIVED"}


@router.get("/tasks/{task_id}/events", operation_id="listTaskEvents")
def list_events(
    task_id: UUID,
    request: Request,
    principal: Annotated[Principal, Depends(current_principal)],
    after: str | None = None,
) -> dict[str, object]:
    authorized_task(request, principal, task_id)
    with request.app.state.sessions() as session:
        events = list(
            session.scalars(select(AuditEventRow).where(AuditEventRow.task_id == task_id))
        )
    return {
        "events": [
            {
                "id": str(event.id),
                "type": event.action,
                "occurred_at": event.created_at,
                "safe_payload": event.payload,
            }
            for event in events
        ],
        "next_cursor": after,
    }
