"""Bounded workflow-segment Celery entry point."""

from typing import Any

from xmg_qa2.infrastructure.messaging.celery_app import celery_app
from xmg_qa2.runtime.execution_service import ExecutionMessage


@celery_app.task(name="xmg_qa2.execute_workflow_segment")  # type: ignore[untyped-decorator]
def execute_workflow_segment(payload: dict[str, Any]) -> dict[str, Any]:
    message = ExecutionMessage.from_payload(payload)
    return message.to_payload()
