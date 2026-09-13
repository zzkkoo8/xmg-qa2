import pytest

from xmg_qa2.domain.capability import CapabilityDescriptor, CapabilityEffect


@pytest.mark.parametrize("effect", [CapabilityEffect.WRITE, CapabilityEffect.UNKNOWN])
def test_customer_target_rejects_unsafe_effects(effect: CapabilityEffect) -> None:
    descriptor = CapabilityDescriptor(
        capability_id="customer.tool",
        provider_kind="TOOL",
        provider_id="fake",
        version="1",
        schema_hash="sha256:test",
        effect=effect,
        enabled=True,
        timeout_seconds=5,
    )
    assert not descriptor.is_executable_for_customer_target


@pytest.mark.parametrize(
    "effect", [CapabilityEffect.READ_ONLY, CapabilityEffect.SYSTEM_EFFECT]
)
def test_customer_target_accepts_non_write_effects(effect: CapabilityEffect) -> None:
    descriptor = CapabilityDescriptor(
        capability_id="customer.tool",
        provider_kind="TOOL",
        provider_id="fake",
        version="1",
        schema_hash="sha256:test",
        effect=effect,
        enabled=True,
        timeout_seconds=5,
    )
    assert descriptor.is_executable_for_customer_target
