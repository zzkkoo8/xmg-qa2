"""LangGraph PostgreSQL checkpoint setup and operation marker storage."""

from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from langgraph.checkpoint.postgres import PostgresSaver


class PostgresCheckpointAdapter:
    def __init__(self, connection_url: str) -> None:
        self.connection_url = connection_url

    def setup(self) -> None:
        with PostgresSaver.from_conn_string(self.connection_url) as saver:
            saver.setup()
        with psycopg.connect(self.connection_url) as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS execution_checkpoint_marker (
                run_id uuid PRIMARY KEY, operation_id text, updated_at timestamptz DEFAULT now()
                )"""
            )

    def record_operation(self, run_id: str, operation_id: str | None) -> None:
        with psycopg.connect(self.connection_url) as connection:
            connection.execute(
                """INSERT INTO execution_checkpoint_marker(run_id, operation_id)
                VALUES (%s, %s) ON CONFLICT(run_id) DO UPDATE
                SET operation_id=excluded.operation_id, updated_at=now()""",
                (run_id, operation_id),
            )

    def operation(self, run_id: str) -> str | None:
        with psycopg.connect(self.connection_url) as connection:
            row = connection.execute(
                "SELECT operation_id FROM execution_checkpoint_marker WHERE run_id=%s", (run_id,)
            ).fetchone()
        return None if row is None else row[0]

    @contextmanager
    def saver(self) -> Iterator[PostgresSaver]:
        with PostgresSaver.from_conn_string(self.connection_url) as saver:
            yield saver
