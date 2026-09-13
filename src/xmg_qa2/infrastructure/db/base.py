"""SQLAlchemy base and engine helpers."""

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DEFAULT_DATABASE_URL = "postgresql+psycopg://xmg_qa2:xmg_qa2@localhost:5432/xmg_qa2"


class Base(DeclarativeBase):
    pass


def make_engine(url: str | None = None) -> Engine:
    resolved_url = url if url is not None else os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
    return create_engine(resolved_url)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)
