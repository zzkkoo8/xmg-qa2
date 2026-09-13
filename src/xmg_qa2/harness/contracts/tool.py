"""Read-oriented tool-provider contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from xmg_qa2.harness.contracts.common import InvocationContext


@dataclass(frozen=True, slots=True)
class ToolRequest:
    capability_id: str
    arguments: Mapping[str, Any]
    context: InvocationContext


@dataclass(frozen=True, slots=True)
class ToolObservation:
    summary: str
    raw_reference: str | None
    observed_at: str
    metadata: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class ToolResult:
    observation: ToolObservation
    provider_request_id: str | None


class ToolProvider(Protocol):
    async def invoke(self, request: ToolRequest) -> ToolResult: ...
