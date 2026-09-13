import pytest

from xmg_qa2.domain.errors import (
    CapabilityDisabled,
    CapabilityNotFound,
    CapabilitySchemaMismatch,
)
from xmg_qa2.harness.contracts.common import CapabilityDescriptor, CapabilityEffect
from xmg_qa2.harness.registry.registry import InMemoryCapabilityRegistry


def descriptor(*, enabled: bool = True, version: str = "1") -> CapabilityDescriptor:
    return CapabilityDescriptor(
        capability_id="tool.health",
        provider_kind="TOOL",
        provider_id="fake",
        version=version,
        schema_hash=f"schema-{version}",
        effect=CapabilityEffect.READ_ONLY,
        enabled=enabled,
        timeout_seconds=5,
        metadata={},
    )


def test_registry_never_falls_back_for_missing_capability() -> None:
    registry = InMemoryCapabilityRegistry([])
    with pytest.raises(CapabilityNotFound):
        registry.get("missing")


def test_registry_rejects_disabled_capability() -> None:
    registry = InMemoryCapabilityRegistry([descriptor(enabled=False)])
    with pytest.raises(CapabilityDisabled):
        registry.get("tool.health")


def test_registry_rejects_version_and_schema_mismatch() -> None:
    registry = InMemoryCapabilityRegistry([descriptor()])
    with pytest.raises(CapabilitySchemaMismatch):
        registry.get("tool.health", version="2")
    with pytest.raises(CapabilitySchemaMismatch):
        registry.get("tool.health", schema_hash="wrong")


def test_registry_filters_available_capabilities() -> None:
    registry = InMemoryCapabilityRegistry([descriptor(), descriptor(enabled=False, version="2")])
    assert registry.list_available(provider_kind="TOOL") == (descriptor(),)
