"""Runtime orchestration ports that enforce policy-before-tool ordering."""

from xmg_qa2.harness.contracts.common import CapabilityDescriptor
from xmg_qa2.harness.contracts.policy import PolicyDecision, PolicyProvider, PolicyRequest
from xmg_qa2.harness.contracts.tool import ToolProvider, ToolRequest, ToolResult


class AuthorizedToolInvoker:
    def __init__(self, policy: PolicyProvider) -> None:
        self._policy = policy

    async def invoke(
        self,
        descriptor: CapabilityDescriptor,
        provider: ToolProvider,
        request: ToolRequest,
    ) -> tuple[PolicyDecision, ToolResult | None]:
        decision = await self._policy.authorize(
            PolicyRequest(descriptor, request.arguments, request.context)
        )
        if not decision.allowed:
            return decision, None
        return decision, await provider.invoke(request)
