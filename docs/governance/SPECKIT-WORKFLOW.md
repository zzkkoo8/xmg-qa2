# SpecKit Workflow for xmg-qa2

## 1. 采用 Full Path

xmg-qa2 是生产级架构项目，不采用 Spec Kit 的短流程。

固定顺序：

```text
constitution
 -> specify
 -> clarify
 -> plan
 -> checklist
 -> tasks
 -> analyze
 -> HUMAN GATE
 -> implement
 -> converge
```

## 2. Gate 0：Architecture Baseline

已经确认的方向：

- XMG Harness。
- LangGraph 作为 Workflow Runtime。
- Workflow First。
- Provider Plugin Architecture。
- Knowledge Project 与 QA Runtime 解耦。
- SpecKit before code。

Gate 0 不代表可以直接写代码。

## 3. Constitution

Constitution 应吸收以下硬原则：

- Workflow First。
- External Capability via Contract。
- Knowledge Independence。
- Evidence First。
- Provider Neutral。
- Observable by Default。
- Deterministic Where Possible。
- Dependency Direction Enforcement。
- Spec Before Code。
- Evidence-based Completion。

## 4. Specify

第一个 Feature 不建议描述“整个 xmg-qa2”。

应拆为可交付 Feature。

推荐起点：

```text
001-core-harness-product-qa
```

包含：

- canonical request/response。
- Thread/Turn。
- plugin contracts。
- registry。
- Product QA baseline workflow。
- fake/in-memory providers for test。
- observability baseline。

DingTalk 和真实 Knowledge Provider 可作为后续 Feature，避免首个 Spec 过大。

## 5. Clarify

重点消除：

- Provider failover 的明确行为。
- Session persistence。
- Evidence threshold。
- Citation 输出要求。
- API sync/stream 行为。
- timeout。
- retry。
- knowledge version。
- multi-tenant 是否进入 V1。

不能用 “TBD” 穿过 Gate。

## 6. Plan

Plan 必须明确：

- 模块边界。
- package layout。
- LangGraph 使用边界。
- persistence。
- dependency rules。
- test pyramid。
- OpenTelemetry。
- config/secrets。
- error model。

## 7. Checklist

至少包括：

- Architecture
- Security
- Knowledge Contract
- Observability
- Testing
- Operations
- Rollback

## 8. Tasks

Task 必须足够小到：

- 可单独实现。
- 可单独测试。
- 可明确验收。
- 失败时能定位到单一边界。

## 9. Analyze

进入实现前必须：

```text
0 Critical
0 High
```

Medium 必须明确：

- 接受。
- 延后。
- 或修正。

不能静默忽略。

## 10. Human Gate

Agent 在 Analyze 完成后必须停止并向用户给出：

- 规格摘要。
- 计划摘要。
- 关键技术选择。
- 未解决风险。
- Analyze 结果。

用户明确说“批准实现”后，才进入 implement。

## 11. Implement

只能按 tasks.md 实施。

遇到架构冲突：

- 不现场发明新架构。
- 返回 Plan / ADR。
- 重新 Analyze。

## 12. Converge

实现后检查：

```text
Spec
vs
Plan
vs
Tasks
vs
Code
vs
Tests
```

发现 drift 必须：

- 补代码。
- 或补规格并重新审批。

不能只修改文档掩盖代码偏差。
