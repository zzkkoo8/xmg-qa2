"""Scenario-keyed fake Tool Contract implementation."""

from collections.abc import Mapping

from xmg_qa2.domain.errors import ProviderMalformedResponse
from xmg_qa2.harness.contracts.tool import ToolObservation, ToolRequest, ToolResult


class FakeToolProvider:
    def __init__(self, observations: Mapping[str, str]) -> None:
        self._observations = observations

    async def invoke(self, request: ToolRequest) -> ToolResult:
        scenario = request.arguments.get("scenario")
        summary = self._observations.get(str(scenario))
        if summary is None:
            raise ProviderMalformedResponse(f"unknown fake scenario: {scenario}")
        return ToolResult(
            ToolObservation(
                summary=summary,
                raw_reference=None,
                observed_at="2026-09-14T00:00:00Z",
                metadata={"scenario": scenario},
            ),
            f"fake-tool:{scenario}",
        )
