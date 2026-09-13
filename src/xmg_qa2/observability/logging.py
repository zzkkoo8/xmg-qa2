"""Correlation and recursive secret redaction helpers."""

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Any

_correlation: ContextVar[dict[str, str] | None] = ContextVar(
    "xmg_qa2_correlation", default=None
)
_SECRET_KEYS = frozenset(
    {
        "password",
        "authorization",
        "api_key",
        "token",
        "credentials",
        "chain_of_thought",
        "prompt_raw",
    }
)


def redact(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): "[REDACTED]" if str(key).lower() in _SECRET_KEYS else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple, set)):
        return tuple(redact(item) for item in value)
    return value


@contextmanager
def correlation(**fields: str) -> Iterator[None]:
    token: Token[dict[str, str] | None] = _correlation.set(dict(fields))
    try:
        yield
    finally:
        _correlation.reset(token)


def current_correlation() -> dict[str, str]:
    return dict(_correlation.get() or {})
