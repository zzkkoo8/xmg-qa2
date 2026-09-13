"""Runtime dependency assembly without provider-specific branching."""

from dataclasses import dataclass

from celery import Celery

from xmg_qa2.infrastructure.checkpoint.postgres import PostgresCheckpointAdapter
from xmg_qa2.infrastructure.messaging.dispatcher import Dispatcher


@dataclass(frozen=True, slots=True)
class RuntimeComponents:
    dispatcher: Dispatcher
    checkpoint: PostgresCheckpointAdapter


def bootstrap_runtime(app: Celery, database_url: str) -> RuntimeComponents:
    return RuntimeComponents(Dispatcher(app), PostgresCheckpointAdapter(database_url))
