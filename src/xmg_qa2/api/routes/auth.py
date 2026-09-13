from fastapi import APIRouter, HTTPException, Request

from xmg_qa2.api.deps import UserRecord
from xmg_qa2.api.schemas import LoginRequest
from xmg_qa2.infrastructure.auth.passwords import verify_password

router = APIRouter()


@router.post("/auth/login", operation_id="login")
def login(body: LoginRequest, request: Request) -> dict[str, object]:
    user: UserRecord | None = request.app.state.users_by_name.get(body.username)
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "invalid credentials")
    token = request.app.state.token_codec.issue(user.id, user.username, user.roles)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": request.app.state.token_codec.lifetime_seconds,
        "principal": {"id": user.id, "username": user.username, "roles": user.roles},
    }
