from datetime import UTC, datetime
from uuid import uuid4

import pytest

from xmg_qa2.domain.errors import DraftHashMismatch
from xmg_qa2.domain.qa import AnswerCheck, AnswerDraft, AnswerKind, RequiredAction


def test_answer_check_must_match_draft_hash() -> None:
    task_id = uuid4()
    draft = AnswerDraft(
        id=uuid4(),
        task_id=task_id,
        run_id=uuid4(),
        version=1,
        answer_kind=AnswerKind.COMPLETE,
        body_markdown="A supported answer.",
        draft_hash="draft-a",
        created_at=datetime.now(UTC),
    )
    check = AnswerCheck(
        id=uuid4(),
        task_id=task_id,
        answer_draft_id=draft.id,
        draft_hash="draft-b",
        evidence_set_hash="evidence-a",
        passed=True,
        required_action=RequiredAction.PASS,
        created_at=datetime.now(UTC),
    )

    with pytest.raises(DraftHashMismatch):
        check.validate_for(draft)


def test_matching_answer_check_is_accepted() -> None:
    task_id = uuid4()
    run_id = uuid4()
    draft_id = uuid4()
    draft = AnswerDraft(
        id=draft_id,
        task_id=task_id,
        run_id=run_id,
        version=1,
        answer_kind=AnswerKind.PARTIAL,
        body_markdown="A partial answer.",
        draft_hash="same",
        created_at=datetime.now(UTC),
    )
    check = AnswerCheck(
        id=uuid4(),
        task_id=task_id,
        answer_draft_id=draft_id,
        draft_hash="same",
        evidence_set_hash="evidence-a",
        passed=False,
        required_action=RequiredAction.INVESTIGATE,
        created_at=datetime.now(UTC),
    )

    check.validate_for(draft)
