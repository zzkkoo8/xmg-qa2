"""Structured model-provider contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from xmg_qa2.harness.contracts.common import InvocationContext


@dataclass(frozen=True, slots=True)
class ModelRequest:
    capability_id: str
    system_instructions: str
    input_payload: Mapping[str, Any]
    output_schema: Mapping[str, Any]
    max_output_tokens: int | None
    context: InvocationContext


@dataclass(frozen=True, slots=True)
class ModelUsage:
    input_tokens: int | None
    output_tokens: int | None
    cost: float | None


@dataclass(frozen=True, slots=True)
class ModelResult:
    structured_output: Mapping[str, Any]
    provider_request_id: str | None
    model_name: str
    usage: ModelUsage


class ModelProvider(Protocol):
    async def generate_structured(self, request: ModelRequest) -> ModelResult: ...
