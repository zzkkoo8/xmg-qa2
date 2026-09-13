"""Deny-first policy-provider contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from xmg_qa2.harness.contracts.common import CapabilityDescriptor, InvocationContext


@dataclass(frozen=True, slots=True)
class PolicyRequest:
    descriptor: CapabilityDescriptor
    arguments: Mapping[str, Any]
    context: InvocationContext


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason_code: str
    safe_reason: str
    redacted_arguments: Mapping[str, Any] | None = None


class PolicyProvider(Protocol):
    async def authorize(self, request: PolicyRequest) -> PolicyDecision: ...
