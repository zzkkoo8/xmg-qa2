# ADR-0001: XMG Harness + LangGraph Runtime

Status: Accepted

## Context

xmg-qa2 需要：

- 可控流程。
- 状态持久化能力。
- 明确状态图。
- 可暂停/恢复。
- 人工补证据、接手与恢复能力（不含自动生产写审批）。
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

## 2026-09-05 复核

保留 LangGraph。持久运行语义由 [ADR-0004](ADR-0004-DURABLE-SUPPORT-TASK.md) 补充，权限边界由 [ADR-0005](ADR-0005-READONLY-EVIDENCE-WORKFLOW.md) 固定；本决定不代表业务实现或真实联调已完成。
