# XMG-QA2 项目基线

日期：2026-09-05。

**小马哥 = 持久 SupportTask + 显式调查工作流 + 动态证据裁决 + 获准只读能力 + 人工协助与恢复。**

## 状态

需求 Q1–9 已确认；剩余项按用户授权形成默认方案；完成当前开源组件研究与设计一致性修订。仓库仍为 Pre-Implementation，不包含已运行服务或通过真实联调的主张。

## 唯一来源

- 产品范围与目标：[Requirements Baseline](docs/requirements/REQUIREMENTS-BASELINE.md)。
- 组件与职责：[Architecture Baseline](docs/architecture/ARCHITECTURE-BASELINE.md)。
- 技术事实与选型理由：[Stack Audit](docs/research/2026-09-05-STACK-AUDIT.md)。
- 状态、能力、证据：docs/architecture 对应契约。
- 实施顺序：[V1 Delivery Plan](docs/plans/V1-DELIVERY-PLAN.md)。
- 约束：[Constitution](.specify/memory/constitution.md)、AGENTS.md 和开发门禁。

## 已定技术方向

模块化单体代码库；中央 API + Worker；LangGraph、PostgreSQL、Celery/RabbitMQ；已有 Dify 只作 Knowledge Provider；官方 MCP；配置驱动能力；OpenTelemetry；Compose 起步。

## 当前下一步

使用 Spec Kit 创建交付计划中的第一个运行时 Feature，完成 spec/clarify/plan/checklist/tasks/analyze；获取真实依赖接入资料并验证。在用户明确批准业务编码前不进入 implement。

本次设计修订分支为 feature/002-support-agent-baseline；001 为已有历史设计分支编号。运行时 Feature 编号由 Spec Kit 在创建时检查远端占用，路线图编号仅为建议。
