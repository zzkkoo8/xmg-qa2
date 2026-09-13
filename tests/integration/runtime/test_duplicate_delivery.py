from uuid import uuid4

from xmg_qa2.infrastructure.messaging.celery_app import create_celery_app
from xmg_qa2.infrastructure.messaging.dispatcher import Dispatcher
from xmg_qa2.runtime.execution_service import ExecutionMessage


def test_publish_then_crash_can_redeliver_same_bounded_payload() -> None:
    app = create_celery_app()
    with app.connection_for_write() as connection:
        connection.ensure_connection(max_retries=3)
    dispatcher = Dispatcher(app)
    message = ExecutionMessage(str(uuid4()), str(uuid4()), 3, 2, "support-foundation-v1")
    first_delivery = dispatcher.publish(message)
    duplicate_delivery = dispatcher.publish(message)
    assert first_delivery != duplicate_delivery
    assert message.to_payload().keys() == {
        "task_id", "run_id", "expected_task_version", "lease_epoch", "workflow_version"
    }
