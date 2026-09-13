"""Short-lived project JWTs."""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt


class TokenCodec:
    def __init__(self, secret: str, lifetime_seconds: int = 3600) -> None:
        self.secret = secret
        self.lifetime_seconds = lifetime_seconds

    def issue(self, principal_id: str, username: str, roles: tuple[str, ...]) -> str:
        now = datetime.now(UTC)
        return jwt.encode(
            {
                "sub": principal_id,
                "username": username,
                "roles": list(roles),
                "iat": now,
                "exp": now + timedelta(seconds=self.lifetime_seconds),
            },
            self.secret,
            algorithm="HS256",
        )

    def decode(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self.secret, algorithms=["HS256"])
