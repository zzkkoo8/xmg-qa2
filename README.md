# xmg-qa2 · 小马哥数字人

面向企业技术支持的只读调查 Agent：理解问题，融合产品知识与通用技术，调用获准的 API/MCP/工具验证，必要时请求工程师补充，跨天恢复同一任务，输出有依据的答案与报告。

当前状态：**2026-09-05 需求 1.1 与架构补全；包含 Chat/Admin、分发与模板设计。业务代码尚未实现，首个 Feature 门禁尚待执行。**

## 先读这几份

| 文档 | 用途 |
| --- | --- |
| [需求基线](docs/requirements/REQUIREMENTS-BASELINE.md) | 已确认 Q1–9、剩余默认选择、V1 范围、验收目标 |
| [技术支持 Agent 设计](docs/design/XMG-QA2-SUPPORT-AGENT-DESIGN.md) | 产品行为、示例和总览 |
| [开源选型与架构审计](docs/research/2026-09-05-STACK-AUDIT.md) | 21 个仓库热度快照、官方依据、取舍与限制 |
| [架构基线](docs/architecture/ARCHITECTURE-BASELINE.md) | API/Worker、组件职责、持久化与部署 |
| [任务与事件](docs/architecture/SESSION-EVENT-MODEL.md) | SupportTask、暂停恢复、幂等与崩溃窗口 |
| [工作流](docs/architecture/WORKFLOW-MODEL.md) | 能力优先级、证据裁决、失败与人工协助 |
| [知识契约](docs/architecture/KNOWLEDGE-CONTRACT.md) / [插件契约](docs/architecture/PLUGIN-CONTRACT.md) | Provider、Evidence、权限和扩展 |
| [V1 交付计划](docs/plans/V1-DELIVERY-PLAN.md) | 多 Feature 交付顺序、具体产物与验收 |
| [开发门禁](docs/governance/DEVELOPMENT-GATES.md) | 设计、编码、验证与发布状态 |
| [Chat/Admin](docs/architecture/WEB-CONSOLE.md) | Web 组件、页面、认证权限与事件恢复 |
| [分发部署](docs/architecture/DISTRIBUTION-DEPLOYMENT.md) | 开发/构建、在线/离线包、安装升级与回退 |
| [模板与展示扩展](docs/architecture/PRESENTATION-CONTRACT.md) | HTML/MD、主题、UI 插件与安全边界 |
| [本轮 Web/交付审计](docs/research/2026-09-05-WEB-DELIVERY-AUDIT.md) | 五项问题的结论、开源复用与官方依据 |
| [编码就绪与 Codex 交接](docs/plans/IMPLEMENTATION-READINESS.md) | 实际缺口、第一 Feature 范围、可直接发送的执行提示词 |

## V1 必须真正可用

真实钉钉入口 + REST/Chat → 持久 SupportTask → 真实 xmg-kb/模型 → 必要的只读检索或 API/MCP → 人工补充与恢复 → 证据化答案/MD 与安全 HTML 报告。Admin 配置能力、工作流、账号权限、模板与主题；最终提供经过验证的在线/离线部署包。

V1 分为多个小 Feature，最后做联合验收。Fake Provider 是测试工具，不能代替真实闭环。

技术路线：Python、FastAPI、Pydantic、LangGraph、PostgreSQL、Celery/RabbitMQ、Dify Knowledge Adapter、官方 MCP SDK、OpenTelemetry；V1 Docker Compose。LiteLLM/Langfuse 等按需启用。

Web 路线：React/TypeScript/Vite + Tailwind/shadcn + TanStack；聊天优先 assistant-ui，选择性复用 FastAPI 官方全栈模板与 Admin 布局。发布使用预构建静态资源，目标服务器不需 Node/pnpm。

## 核心边界

- 只读客户目标；写操作只给工程师建议，人工回复不能解锁 Agent 生产写权限。
- 任务可暂停数天；等待不占 Worker，恢复保留证据、假设和待办。
- 知识优先，能力选择由版本化工作流与 Policy 控制；通用推理贯穿全过程。
- xmg-kb 独立负责批量文档解析、清洗和建索引；xmg-qa2 消费统一 Evidence。
- 任务按客户/项目隔离；外发先脱敏，不能把原始日志送公网后才遮蔽。
- 所有组件替换经过 Contract 与能力测试，不承诺各厂商功能天然等价。

## 开发规则

遵守 [AGENTS.md](AGENTS.md)、[Constitution](.specify/memory/constitution.md) 和 [Spec Kit 流程](docs/governance/SPECKIT-WORKFLOW.md)：

constitution → specify → clarify → plan → checklist → tasks → analyze → 明确编码授权 → implement → converge。

每项 Feature 使用 feature/<number>-<slug> 分支，不在 main 直接开发。设计文档推送不等于运行时已实现、测试通过或已获编码授权。

[项目基线](XMG-QA2-PROJECT-BASELINE.md) · [ADR 索引](docs/adr/README.md) · [初始化历史说明](docs/BOOTSTRAP.md)
