"""Provider-neutral capability metadata."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class CapabilityEffect(StrEnum):
    READ_ONLY = "READ_ONLY"
    SYSTEM_EFFECT = "SYSTEM_EFFECT"
    WRITE = "WRITE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class CapabilityDescriptor:
    capability_id: str
    provider_kind: str
    provider_id: str
    version: str
    schema_hash: str
    effect: CapabilityEffect
    enabled: bool
    timeout_seconds: int
    scope_rules: Mapping[str, Any] = field(default_factory=dict)
    retry_policy: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def is_executable_for_customer_target(self) -> bool:
        return self.enabled and self.effect in {
            CapabilityEffect.READ_ONLY,
            CapabilityEffect.SYSTEM_EFFECT,
        }
