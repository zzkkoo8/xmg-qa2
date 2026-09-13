import pytest

from xmg_qa2.harness.contracts.common import (
    CapabilityDescriptor,
    CapabilityEffect,
    InvocationContext,
)
from xmg_qa2.harness.contracts.policy import PolicyRequest
from xmg_qa2.harness.contracts.tool import ToolRequest
from xmg_qa2.harness.policy import DenyFirstPolicy
from xmg_qa2.runtime.ports import AuthorizedToolInvoker


def context() -> InvocationContext:
    return InvocationContext("task", "case", "customer", None, "principal", "run", "op", "trace")


def descriptor(effect: CapabilityEffect, **metadata: object) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        "tool.health", "TOOL", "fake", "1", "schema", effect, True, 5, metadata
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("effect", "reason"),
    [
        (CapabilityEffect.WRITE, "WRITE_NOT_ALLOWED"),
        (CapabilityEffect.UNKNOWN, "UNKNOWN_EFFECT"),
    ],
)
async def test_policy_denies_unsafe_customer_effects(
    effect: CapabilityEffect, reason: str
) -> None:
    decision = await DenyFirstPolicy().authorize(PolicyRequest(descriptor(effect), {}, context()))
    assert not decision.allowed
    assert decision.reason_code == reason


@pytest.mark.asyncio
async def test_policy_denies_scope_and_export_violations() -> None:
    policy = DenyFirstPolicy()
    denied_scope = await policy.authorize(
        PolicyRequest(descriptor(CapabilityEffect.READ_ONLY, allowed_case_ids=["other"]), {}, context())
    )
    denied_export = await policy.authorize(
        PolicyRequest(
            descriptor(CapabilityEffect.READ_ONLY, allow_external_data_export=False),
            {"external_data_export": True},
            context(),
        )
    )
    assert denied_scope.reason_code == "CASE_SCOPE_DENIED"
    assert denied_export.reason_code == "DATA_EXPORT_DENIED"


class RecordingTool:
    def __init__(self) -> None:
        self.called = False

    async def invoke(self, request: ToolRequest):  # type: ignore[no-untyped-def]
        self.called = True
        raise AssertionError("denied tool must not run")


@pytest.mark.asyncio
async def test_authorized_invoker_does_not_call_provider_when_denied() -> None:
    tool = RecordingTool()
    invoker = AuthorizedToolInvoker(DenyFirstPolicy())
    request = ToolRequest("tool.health", {}, context())
    decision, result = await invoker.invoke(descriptor(CapabilityEffect.WRITE), tool, request)
    assert decision.reason_code == "WRITE_NOT_ALLOWED"
    assert result is None
    assert not tool.called
