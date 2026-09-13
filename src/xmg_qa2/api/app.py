from collections.abc import Iterable

from fastapi import FastAPI
from sqlalchemy.orm import Session, sessionmaker

from xmg_qa2.api.deps import UserRecord
from xmg_qa2.api.routes import admin, auth, health, tasks
from xmg_qa2.infrastructure.auth.tokens import TokenCodec


def create_app(
    sessions: sessionmaker[Session], users: Iterable[UserRecord], jwt_secret: str
) -> FastAPI:
    app = FastAPI(title="xmg-qa2 Support Foundation API", version="0.1.0")
    records = tuple(users)
    app.state.sessions = sessions
    app.state.users_by_name = {user.username: user for user in records}
    app.state.users_by_id = {user.id: user for user in records}
    app.state.token_codec = TokenCodec(jwt_secret)
    for router in (health.router, auth.router, tasks.router, admin.router):
        app.include_router(router, prefix="/api/v1")
    return app
