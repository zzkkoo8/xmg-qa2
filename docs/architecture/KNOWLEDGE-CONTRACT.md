# Knowledge Contract

## 1. 边界

知识工程项目：

```text
Raw Documents
 -> Parse
 -> Clean
 -> Deduplicate
 -> Classify
 -> Chunk
 -> Index
 -> Publish
```

xmg-qa2：

```text
Query
 -> Knowledge Contract
 -> Evidence[]
```

xmg-qa2 不理解上游文档如何被清洗和入库。

## 2. V1 必需能力

Knowledge Provider 至少提供：

```text
health()
capabilities()
search()
retrieve()
```

如果某 Provider 不支持 `retrieve()`，必须通过 capabilities 明确说明，不能运行时猜测。

## 3. Search Request

概念字段：

```text
query
top_k
filters
namespace
knowledge_version
request_context
```

`filters` 使用统一 schema；Provider Adapter 负责翻译为 Dify/RAGFlow/ES 等私有过滤语法。

## 4. Evidence

统一 Evidence 至少包含：

```text
evidence_id
content
title
source
uri
document_id
chunk_id
score
metadata
knowledge_version
provider_id
```

可选：

```text
page
section
mime_type
published_at
updated_at
rerank_score
```

## 5. Score

不同 Provider score 定义可能不同。

禁止 Workflow 假设所有 Provider 的 `score` 数值完全可比较。

Provider 必须额外声明：

- score_semantics
- score_range
- higher_is_better

如果跨 Provider 聚合，必须经过标准化或 rerank 层。

## 6. Provenance

Evidence 必须可回溯。

最少能回答：

- 来自哪个 Provider。
- 来自哪个知识版本。
- 来自哪个文档。
- 来自哪个片段。
- 原始来源是什么。

## 7. Knowledge Version

Knowledge Factory 每次正式发布应提供可识别版本。

一个 Turn 的 Evidence 必须记录实际使用的 knowledge_version，避免知识库更新后无法重现历史答案。

## 8. 错误语义

以下情况必须区分：

```text
NoResult
ProviderUnavailable
Timeout
AuthenticationError
InvalidQuery
ContractViolation
```

`ProviderUnavailable` 绝不能伪装为 `NoResult`。

## 9. Provider 示例

未来可以实现：

```text
DifyKnowledgeProvider
RAGFlowKnowledgeProvider
ElasticsearchKnowledgeProvider
HttpKnowledgeProvider
McpKnowledgeProvider
```

它们必须返回相同 Evidence Contract。
