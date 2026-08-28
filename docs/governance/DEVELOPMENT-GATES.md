# Development Gates

## Gate 0 — Architecture Direction

通过条件：

- 项目定位明确。
- Harness / Workflow / Plugin / Knowledge 边界明确。
- 技术路线得到人工批准。

当前状态：**Approved**

## Gate 1 — Constitution

通过条件：

- Constitution 与 Architecture Baseline 一致。
- 无相互矛盾规则。
- 明确禁止提前编码。
- 人工批准。

## Gate 2 — Feature Specification

通过条件：

- 明确 User Scenarios。
- 明确 Functional Requirements。
- 明确 Non-Functional Requirements。
- 明确 Out of Scope。
- 所有 Critical ambiguity 已 clarify。
- 人工批准。

## Gate 3 — Implementation Plan

通过条件：

- 模块边界明确。
- Contracts 明确。
- Data/State model 明确。
- Error model 明确。
- Observability 明确。
- Test strategy 明确。
- Migration/rollback 明确。
- 人工批准。

## Gate 4 — Analyze

通过条件：

- 0 Critical。
- 0 High。
- Medium 有处理决定。
- Checklist 无 blocker。
- Tasks 可执行。

## Gate 5 — Coding Authorization

必须由用户明确批准。

Agent 不得根据“前面已经同意架构”推断获得编码授权。

## Gate 6 — Task Verification

每个 Task 完成必须有：

- 自动化测试。
- 命令输出。
- git diff review。
- 无新增未解释 warning。
- 关联 Spec requirement。

## Gate 7 — Integration

通过：

- contract tests。
- integration tests。
- workflow tests。
- provider failure tests。
- observability checks。

## Gate 8 — Acceptance

通过：

- E2E。
- 性能基线。
- 故障降级。
- rollback。
- SpecKit converge。
- 用户验收。
