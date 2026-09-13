"""Explicit capability registry with no fallback routing."""

from collections.abc import Iterable

from xmg_qa2.domain.errors import (
    CapabilityDisabled,
    CapabilityNotFound,
    CapabilitySchemaMismatch,
)
from xmg_qa2.harness.contracts.common import CapabilityDescriptor


class InMemoryCapabilityRegistry:
    def __init__(self, descriptors: Iterable[CapabilityDescriptor]) -> None:
        self._entries = {
            (descriptor.capability_id, descriptor.version): descriptor
            for descriptor in descriptors
        }

    def get(
        self,
        capability_id: str,
        version: str | None = None,
        *,
        schema_hash: str | None = None,
    ) -> CapabilityDescriptor:
        matches = [
            descriptor
            for (entry_id, _), descriptor in self._entries.items()
            if entry_id == capability_id
        ]
        if not matches:
            raise CapabilityNotFound(capability_id)
        if version is None:
            if len(matches) != 1:
                raise CapabilitySchemaMismatch(f"version required for {capability_id}")
            descriptor = matches[0]
        else:
            versioned_descriptor = self._entries.get((capability_id, version))
            if versioned_descriptor is None:
                raise CapabilitySchemaMismatch(f"unsupported version {version}")
            descriptor = versioned_descriptor
        if not descriptor.enabled:
            raise CapabilityDisabled(capability_id)
        if schema_hash is not None and descriptor.schema_hash != schema_hash:
            raise CapabilitySchemaMismatch(f"schema mismatch for {capability_id}")
        return descriptor

    def list_available(
        self, *, provider_kind: str | None = None
    ) -> tuple[CapabilityDescriptor, ...]:
        return tuple(
            descriptor
            for descriptor in self._entries.values()
            if descriptor.enabled
            and (provider_kind is None or descriptor.provider_kind == provider_kind)
        )
