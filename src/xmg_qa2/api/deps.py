"""Authentication and Case ACL dependencies."""

from dataclasses import dataclass, field
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from xmg_qa2.infrastructure.auth.tokens import TokenCodec

bearer = HTTPBearer(auto_error=False)


@dataclass(slots=True)
class UserRecord:
    id: str
    username: str
    password_hash: str
    roles: tuple[str, ...] = ()
    case_ids: set[UUID] = field(default_factory=set)


@dataclass(frozen=True, slots=True)
class Principal:
    id: str
    username: str
    roles: tuple[str, ...]


def current_principal(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> Principal:
    if credentials is None:
        raise HTTPException(401, "authentication required")
    codec: TokenCodec = request.app.state.token_codec
    try:
        payload = codec.decode(credentials.credentials)
    except Exception as error:
        raise HTTPException(401, "invalid token") from error
    return Principal(str(payload["sub"]), str(payload["username"]), tuple(payload["roles"]))


def require_admin(principal: Annotated[Principal, Depends(current_principal)]) -> Principal:
    if "admin" not in principal.roles:
        raise HTTPException(403, "admin role required")
    return principal


def assert_case_access(request: Request, principal: Principal, case_id: UUID) -> None:
    user: UserRecord = request.app.state.users_by_id[principal.id]
    if "admin" not in principal.roles and case_id not in user.case_ids:
        raise HTTPException(403, "case scope denied")
