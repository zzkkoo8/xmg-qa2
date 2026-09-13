"""Scenario-keyed fake structured model."""

from collections.abc import Mapping
from typing import Any

from xmg_qa2.domain.errors import ProviderMalformedResponse, ProviderRateLimited, ProviderTimeout
from xmg_qa2.harness.contracts.model import ModelRequest, ModelResult, ModelUsage


class FakeModelProvider:
    def __init__(self, responses: Mapping[str, Mapping[str, Any]]) -> None:
        self._responses = responses

    async def generate_structured(self, request: ModelRequest) -> ModelResult:
        scenario = request.input_payload.get("scenario")
        if not isinstance(scenario, str):
            raise ProviderMalformedResponse("fake model requires explicit scenario")
        if scenario == "model-malformed-output":
            raise ProviderMalformedResponse(scenario)
        if scenario == "provider-timeout":
            raise ProviderTimeout(scenario)
        if scenario == "provider-rate-limit":
            raise ProviderRateLimited(scenario)
        response = self._responses.get(scenario)
        if response is None:
            raise ProviderMalformedResponse(f"unknown fake scenario: {scenario}")
        return ModelResult(response, f"fake-model:{scenario}", "fake-model", ModelUsage(None, None, None))
