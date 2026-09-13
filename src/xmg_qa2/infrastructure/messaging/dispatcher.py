"""Outbox dispatcher publishing ID/version-only execution messages."""

from celery import Celery

from xmg_qa2.runtime.execution_service import ExecutionMessage


class Dispatcher:
    def __init__(self, app: Celery) -> None:
        self.app = app

    def publish(self, message: ExecutionMessage) -> str:
        result = self.app.send_task("xmg_qa2.execute_workflow_segment", args=[message.to_payload()])
        return str(result.id)
