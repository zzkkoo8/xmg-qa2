# xmg-qa2

## 项目定位

xmg-qa2 是一个面向企业知识问答场景的 **可控 Harness / Runtime**，而不是单一“知识库机器人”。

目标是把上游渠道、工作流、模型、工具和知识库解耦，使系统具备：

- 流程可控：核心问答走显式 Workflow / State Graph，不依赖无限自由 Agent Loop。
- 功能可拔插：Channel、Knowledge、Model、Tool、Policy 均通过插件契约接入。
- 知识库独立：文档解析、清洗、去重、分类、切片、索引由独立知识工程项目负责。
- Provider Neutral：Dify、RAGFlow、Elasticsearch、向量库、HTTP 服务等可替换。
- 可观测：Thread / Turn / Node / Model / Retrieval / Tool 全链路可追踪。
- Spec Driven：严格执行 GitHub Spec Kit，正式编码前必须完成需求、架构、计划和一致性检查。

## V1 范围

V1 只建立最小但生产可演进的闭环：

1. REST/API Channel。
2. DingTalk Channel。
3. Product QA Workflow。
4. 至少一个 Knowledge Provider Adapter。
5. 至少一个 OpenAI-Compatible Model Adapter。
6. Evidence / Citation 统一模型。
7. Thread / Turn / Event 状态模型。
8. Trace / Metrics / Audit 基线。
9. Unit / Contract / Integration / E2E 测试体系。

## 明确不属于 V1

- 原始文档解析与清洗。
- 文档去重、分类和知识库构建。
- 通用多 Agent Supervisor。
- 自由无限 Agent Loop。
- 为单一 Dify / RAGFlow / LLM 厂商定制 Core。
- 大规模管理后台 UI。
- 与问答主链路无关的复杂工具生态。

## 核心技术方向

- Harness：XMG Harness（项目自身薄控制层）
- Workflow Runtime：LangGraph
- API：FastAPI
- Schema：Pydantic
- Observability：OpenTelemetry 兼容
- SDD：GitHub Spec Kit
- Git：标准 `.git/` 仓库 + Spec Kit git extension

## 编码门禁

在以下产物全部完成并人工批准前，不得实现业务代码：

`constitution → specify → clarify → plan → checklist → tasks → analyze`

只有 `analyze` 达到 **0 Critical / 0 High** 且人工批准后，才允许进入 `implement`。

详见：

- `docs/architecture/ARCHITECTURE-BASELINE.md`
- `docs/governance/SPECKIT-WORKFLOW.md`
- `docs/governance/DEVELOPMENT-GATES.md`
- `AGENTS.md`
