from datetime import UTC, datetime
from uuid import uuid4

import pytest

from xmg_qa2.domain.errors import InvalidTransition, StaleStateVersion
from xmg_qa2.domain.qa import QuestionFrame, Subquestion, SubquestionStatus
from xmg_qa2.domain.task import SupportTask, SupportTaskStatus, transition_task


def make_task(status: SupportTaskStatus = SupportTaskStatus.NEW) -> SupportTask:
    now = datetime.now(UTC)
    return SupportTask(
        id=uuid4(),
        case_id=uuid4(),
        customer_id="customer-1",
        project_id=None,
        created_by_principal="principal-1",
        status=status,
        state_version=1,
        workflow_name="support",
        workflow_version="1",
        question_text="Why is the service unavailable?",
        created_at=now,
        updated_at=now,
    )


@pytest.mark.parametrize("source", [SupportTaskStatus.NEW, SupportTaskStatus.RUNNING])
def test_task_cannot_close_without_resolution(source: SupportTaskStatus) -> None:
    with pytest.raises(InvalidTransition):
        transition_task(make_task(source), SupportTaskStatus.CLOSED, expected_state_version=1)


def test_transition_rejects_stale_state_version() -> None:
    with pytest.raises(StaleStateVersion):
        transition_task(make_task(), SupportTaskStatus.RUNNING, expected_state_version=2)


def test_critical_pending_subquestion_prevents_automatic_resolution() -> None:
    task = make_task(SupportTaskStatus.RUNNING)
    frame = QuestionFrame(
        id=uuid4(),
        task_id=task.id,
        version=1,
        original_question=task.question_text,
        goal="Restore availability",
        subquestions=(
            Subquestion(id="root-cause", text="What failed?", status=SubquestionStatus.OPEN, critical=True),
        ),
        created_at=datetime.now(UTC),
    )

    with pytest.raises(InvalidTransition):
        transition_task(
            task,
            SupportTaskStatus.RESOLVED,
            expected_state_version=1,
            question_frame=frame,
        )


def test_valid_transition_increments_version() -> None:
    transitioned = transition_task(
        make_task(), SupportTaskStatus.RUNNING, expected_state_version=1
    )
    assert transitioned.status is SupportTaskStatus.RUNNING
    assert transitioned.state_version == 2
