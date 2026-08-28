# ADR-0001: XMG Harness + LangGraph Runtime

Status: Accepted

## Context

xmg-qa2 需要：

- 可控流程。
- 状态持久化能力。
- 明确状态图。
- 可暂停/恢复。
- 人工审批扩展能力。
- 可观测节点执行。

同时需要避免整个业务架构绑定某个 Agent Framework。

## Decision

采用：

```text
XMG Harness = stable product architecture
LangGraph = workflow runtime engine
```

Domain / Contract 不依赖 LangGraph。

## Consequences

优点：

- 复用成熟状态图运行时。
- 不自研 Agent loop。
- Workflow 可测试。
- 保留未来替换引擎空间。

代价：

- 需要一层 Harness State 与 LangGraph State 的边界。
- 团队需要学习 LangGraph。
