# xmg-qa2

## 项目定位

xmg-qa2 是一款面向企业客户技术支持场景的 **问题回答专家 Agent / 可控 Harness Runtime**。

它不是单一“知识库机器人”，也不是无限自由执行的 Agent Loop。目标是在时间、步骤、成本、权限和安全边界内，自动组合 `xmg-kb`、其他知识库、第三方产品 API、MCP、诊断工具和模型能力，持续获取 Evidence、验证 Hypothesis，并尽最大合理努力回答客户问题。

系统应具备：

- **流程可控**：外层核心问答走显式 Workflow / State Graph。
- **受控 Agentic Investigation**：复杂问题允许多步自动调查，但必须有 `max_steps`、`max_duration`、权限、工具 allowlist、timeout、retry、budget 和明确终止条件。
- **功能可拔插**：Channel、Knowledge、Model、Tool、Policy 均通过稳定 Contract / Plugin 接入。
- **知识库独立**：文档解析、清洗、去重、分类、切片、索引由独立知识工程项目负责；xmg-qa2 只消费知识服务。
- **Evidence First**：Knowledge/API/Tool 结果统一形成 Evidence，关键结论可追溯。
- **Provider Neutral**：替换 xmg-kb、Dify、RAGFlow、LLM、Channel 或 Tool 不要求修改 Harness Core。
- **可观测**：Thread / Turn / Investigation / Provider Call / Evidence / Answer 全链路可追踪。
- **Spec Driven**：严格执行 GitHub Spec Kit，正式编码前必须完成需求、架构、计划和一致性检查。

## 设计文档

- [xmg-qa2 技术支持专家 Agent 设计稿](docs/design/XMG-QA2-SUPPORT-AGENT-DESIGN.md)
- [Architecture Baseline](docs/architecture/ARCHITECTURE-BASELINE.md)
- [Workflow Model](docs/architecture/WORKFLOW-MODEL.md)
- [Knowledge Contract](docs/architecture/KNOWLEDGE-CONTRACT.md)
- [Plugin Contract](docs/architecture/PLUGIN-CONTRACT.md)

## V1 范围

V1 只建立最小但生产可演进的核心闭环：

1. Thread / Turn / Investigation 状态模型。
2. Evidence / Hypothesis 统一模型。
3. Knowledge / Model / Tool / Channel / Policy 稳定 Contracts。
4. Capability Registry。
5. Core Support Workflow。
6. Controlled Agentic Investigation。
7. Fake Knowledge / Tool / Model Providers，用于验证核心架构。
8. 最小 API 接口。
9. Trace / Metrics / Audit 基线。
10. Unit / Contract / Workflow / Integration / E2E 测试体系。

## 明确不属于 V1

- 原始文档解析与清洗。
- 文档去重、分类和知识库构建。
- 真实 xmg-kb 生产接入。
- DingTalk 生产接入。
- 真实产品 API 和高风险自动执行工具。
- 通用 Multi-Agent Supervisor。
- 自由无限 Agent Loop。
- 大规模管理后台 UI。

## 核心技术方向

- Harness：XMG Harness（项目自身薄控制层）
- Workflow Runtime：LangGraph，仅位于 runtime/workflow 层
- API：FastAPI
- Schema / Contract：Pydantic
- Observability：OpenTelemetry-compatible
- SDD：GitHub Spec Kit
- Git：标准 `.git/` 仓库 + Spec Kit git extension

## 编码门禁

在以下产物全部完成并人工批准前，不得实现业务代码：

`constitution → specify → clarify → plan → checklist → tasks → analyze`

只有 `analyze` 达到 **0 Critical / 0 High** 且人工明确批准后，才允许进入 `implement`。

详见：

- `docs/design/XMG-QA2-SUPPORT-AGENT-DESIGN.md`
- `docs/architecture/ARCHITECTURE-BASELINE.md`
- `docs/governance/SPECKIT-WORKFLOW.md`
- `docs/governance/DEVELOPMENT-GATES.md`
- `AGENTS.md`
