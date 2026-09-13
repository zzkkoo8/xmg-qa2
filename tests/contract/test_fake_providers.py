import pytest

from xmg_qa2.domain.errors import ProviderMalformedResponse, ProviderRateLimited, ProviderTimeout
from xmg_qa2.harness.contracts.common import InvocationContext
from xmg_qa2.harness.contracts.knowledge import KnowledgeQuery
from xmg_qa2.harness.contracts.model import ModelRequest
from xmg_qa2.harness.contracts.tool import ToolRequest
from xmg_qa2.plugins.fake.knowledge import FakeKnowledgeProvider
from xmg_qa2.plugins.fake.model import FakeModelProvider
from xmg_qa2.plugins.fake.tool import FakeToolProvider


def context() -> InvocationContext:
    return InvocationContext("task", "case", "customer", None, "principal", "run", "op", "trace")


@pytest.mark.asyncio
async def test_fake_model_is_keyed_by_explicit_scenario() -> None:
    provider = FakeModelProvider({"ok": {"answer": "bounded"}})
    result = await provider.generate_structured(ModelRequest("model", "", {"scenario": "ok"}, {}, None, context()))
    assert result.structured_output == {"answer": "bounded"}
    assert result.usage.cost is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("scenario", "failure"),
    [("model-malformed-output", ProviderMalformedResponse), ("provider-timeout", ProviderTimeout), ("provider-rate-limit", ProviderRateLimited)],
)
async def test_fake_model_has_deterministic_failure_modes(scenario: str, failure: type[Exception]) -> None:
    with pytest.raises(failure):
        await FakeModelProvider({}).generate_structured(ModelRequest("model", "", {"scenario": scenario}, {}, None, context()))


@pytest.mark.asyncio
async def test_fake_knowledge_and_tool_preserve_provider_neutral_dtos() -> None:
    knowledge = FakeKnowledgeProvider({"product-evidence-answer": [{"source_name": "fixture", "excerpt": "fact", "id": "doc-current"}]})
    result = await knowledge.search(KnowledgeQuery("knowledge", "q", None, None, {"scenario": "product-evidence-answer"}, 3, context()))
    tool = await FakeToolProvider({"readonly-tool-observation": "healthy"}).invoke(ToolRequest("tool", {"scenario": "readonly-tool-observation"}, context()))
    assert result.items[0].provenance["evidence_id"] == "doc-current"
    assert tool.observation.summary == "healthy"
