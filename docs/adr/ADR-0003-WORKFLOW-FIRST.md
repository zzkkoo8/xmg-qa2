# ADR-0003: Workflow First, Agent Where Needed

Status: Accepted

## Context

企业知识问答要求可预测、可审计、可定位。

自由 Agent Loop 会引入：

- 不稳定执行路径。
- 无限/高额循环风险。
- 失败难以重放。
- Provider 使用不可预测。
- 测试覆盖困难。

## Decision

核心问答由显式 Workflow State Graph 控制。

LLM/Agent 只用于适合语义推理的节点。

## Consequences

必须显式定义：

- route。
- retry。
- timeout。
- evidence gate。
- fallback。
- completion condition。

V1 不建立通用 Supervisor Multi-Agent 系统。
