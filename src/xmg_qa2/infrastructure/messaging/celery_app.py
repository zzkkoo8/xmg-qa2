"""Celery application configured as transport, never business truth."""

import os

from celery import Celery


def create_celery_app(broker_url: str | None = None) -> Celery:
    app = Celery(
        "xmg_qa2",
        broker=broker_url
        or os.environ.get("CELERY_BROKER_URL", "amqp://xmg_qa2:xmg_qa2@localhost:5672//"),
        include=["xmg_qa2.infrastructure.messaging.tasks"],
    )
    app.conf.update(
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        task_serializer="json",
        accept_content=["json"],
        result_backend=None,
    )
    return app


celery_app = create_celery_app()
