# XMG-QA2 项目基线

日期：2026-09-05。

**核心目标：高质量回答问题；以问题理解、证据、自主调查和答案验证实现，以任务/Web/插件/部署支撑。**

## 状态

需求 Q1–9 已确认；本轮追加 Chat/Admin、便捷分发与 HTML/MD 模板要求，最新明确问答优先，需求/Constitution 升到 1.2。已补问答核心、质量评测及 Web/分发/模板设计与开发机交接。仓库仍为 Pre-Implementation，不包含已运行服务或通过真实联调的主张。

## 唯一来源

- 产品范围与目标：[Requirements Baseline](docs/requirements/REQUIREMENTS-BASELINE.md)。
- 组件与职责：[Architecture Baseline](docs/architecture/ARCHITECTURE-BASELINE.md)。
- 技术事实与选型理由：[Stack Audit](docs/research/2026-09-05-STACK-AUDIT.md)。
- 本轮五项审计：[Web/Delivery Audit](docs/research/2026-09-05-WEB-DELIVERY-AUDIT.md)。
- 问答主线：[QA Core](docs/architecture/QA-CORE.md)、[Answer Quality](docs/governance/ANSWER-QUALITY.md)。
- 状态、能力、证据：docs/architecture 对应契约。
- 实施顺序：[V1 Delivery Plan](docs/plans/V1-DELIVERY-PLAN.md)。
- 约束：[Constitution](.specify/memory/constitution.md)、AGENTS.md 和开发门禁。

## 已定技术方向

模块化单体代码库；中央 API + Worker；LangGraph、PostgreSQL、Celery/RabbitMQ；已有 Dify 只作 Knowledge Provider；官方 MCP；配置驱动能力；OpenTelemetry；Compose 起步。

## 当前下一步

按 [编码就绪与交接](docs/plans/IMPLEMENTATION-READINESS.md) 在开发机创建首个 support-foundation Feature，完成版本验证与 Spec Kit 门禁，按用户发送的明确授权进入实现。真实依赖缺失只阻塞对应集成，不重做全局架构或阻塞独立开发。

本次设计修订分支为 feature/002-support-agent-baseline；001 为已有历史设计分支编号。运行时 Feature 编号由 Spec Kit 在创建时检查远端占用，路线图编号仅为建议。
