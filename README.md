# xmg-qa2 · 小马哥数字技术支持员工

xmg-qa2 是“小马哥数字员工（xmg 系列）”中的首个企业级数字员工角色：**数字技术支持工程师**。它不是传统问答机器人，也不是通用多 Agent 平台；它以持久任务为工作单位，理解问题、融合产品知识与通用技术、调用获准的 API/MCP/工具取证，必要时请求工程师补充，跨轮次和跨天恢复同一任务，最终输出可追溯的答案与报告。

其中：**数字员工是产品定位，技术支持是首个员工角色，问答/调查是该角色的领域核心能力；Task Engine、Workflow、XMG Harness、Policy、Evidence、Human-in-the-loop 与 Observability 构成可复用的数字员工运行基础。** 当前实现只服务 xmg-qa2，不提前抽象成通用平台，也不为了“数字员工”概念滥用 Multi-Agent。

当前状态：**2026-09-13：003 Support Foundation 的 Spec / Plan / Tasks / Analyze / Coding Readiness 已完成并合入 `main`；业务代码尚未实现，下一步由开发机 Codex 从 `main` 创建实现分支并执行 T001–T013。** 这表示设计门禁已开放，不代表 V1、真实 Provider 联调或企业生产发布已经完成。

2026-09-07 企业级开工审计仍有效：流式输出、群聊受众等边界及版本/恢复验证须在对应阶段关闭，尚非企业生产就绪。详见[企业级开工审计](docs/research/2026-09-07-ENTERPRISE-READINESS-AUDIT.md)。

## 产品与架构定位

```text
小马哥数字员工体系（xmg）
        │
        ├── 可复用运行基础
        │   ├── Task lifecycle / pause / resume / retry
        │   ├── Workflow
        │   ├── XMG Harness / Registry / Adapter
        │   ├── Knowledge / Model / Tool / MCP / Skill
        │   ├── Policy / ACL / Human-in-the-loop
        │   ├── Evidence / Artifact / Audit
        │   └── Observability
        │
        └── xmg-qa2
            └── 数字技术支持员工
                ├── QuestionFrame
                ├── 技术调查 / 假设验证
                ├── AnswerDraft / AnswerCheck
                └── 技术支持领域 Workflow
```

`QA Core` 是 **xmg-qa2 的 Support Domain Core**，不是整个 xmg 数字员工平台的通用 Core。未来如出现 xmg-ops、xmg-dev、xmg-data、xmg-doc 等角色，可以复用成熟的任务生命周期、Harness、Policy、Evidence、HITL 和观测语义，但应拥有自己的 Domain 和 Workflow；当前 Feature 不提前建设这些未来角色。

## 先读这几份

| 文档 | 用途 |
| --- | --- |
| [需求基线](docs/requirements/REQUIREMENTS-BASELINE.md) | 已确认 Q1–9、数字员工定位、V1 范围、验收目标 |
| [问答核心](docs/architecture/QA-CORE.md) / [答案质量](docs/governance/ANSWER-QUALITY.md) | 数字技术支持员工如何理解问题、自主补证、生成验证答案及评测 |
| [技术支持 Agent 设计](docs/design/XMG-QA2-SUPPORT-AGENT-DESIGN.md) | 技术支持员工的产品行为、示例和总览 |
| [开源选型与架构审计](docs/research/2026-09-05-STACK-AUDIT.md) | 21 个仓库热度快照、官方依据、取舍与限制 |
| [架构基线](docs/architecture/ARCHITECTURE-BASELINE.md) | 数字员工运行基础、Support Domain、API/Worker、持久化与部署 |
| [任务与事件](docs/architecture/SESSION-EVENT-MODEL.md) | SupportTask、暂停恢复、幂等与崩溃窗口 |
| [工作流](docs/architecture/WORKFLOW-MODEL.md) | 能力优先级、证据裁决、失败与人工协助 |
| [知识契约](docs/architecture/KNOWLEDGE-CONTRACT.md) / [插件契约](docs/architecture/PLUGIN-CONTRACT.md) | Provider、Evidence、权限和扩展 |
| [V1 交付计划](docs/plans/V1-DELIVERY-PLAN.md) | 多 Feature 交付顺序、具体产物与验收 |
| [开发门禁](docs/governance/DEVELOPMENT-GATES.md) | 设计、编码、验证与发布状态 |
| [Chat/Admin](docs/architecture/WEB-CONSOLE.md) | Web 组件、页面、认证权限与事件恢复 |
| [分发部署](docs/architecture/DISTRIBUTION-DEPLOYMENT.md) | 开发/构建、在线/离线包、安装升级与回退 |
| [模板与展示扩展](docs/architecture/PRESENTATION-CONTRACT.md) | HTML/MD、主题、UI 插件与安全边界 |
| [本轮 Web/交付审计](docs/research/2026-09-05-WEB-DELIVERY-AUDIT.md) | 五项问题的结论、开源复用与官方依据 |
| [编码就绪与 Codex 交接](docs/plans/IMPLEMENTATION-READINESS.md) | 当前 003 编码门禁、第一 Feature 范围与开发机交接 |

## V1 必须真正可用

真实钉钉入口 + REST/Chat → 持久 SupportTask → 真实 xmg-kb/模型 → 必要的只读检索或 API/MCP → 人工补充与恢复 → 证据化答案/MD 与安全 HTML 报告。Admin 配置能力、工作流、账号权限、模板与主题；最终提供经过验证的在线/离线部署包。

V1 分为多个小 Feature，最后做联合验收。Fake Provider 是测试工具，不能代替真实闭环。

技术路线：Python、FastAPI、Pydantic、LangGraph、PostgreSQL、Celery/RabbitMQ、Dify Knowledge Adapter、官方 MCP SDK、OpenTelemetry；V1 Docker Compose。LiteLLM/Langfuse 等按需启用。

Web 路线：React/TypeScript/Vite + Tailwind/shadcn + TanStack；聊天优先 assistant-ui，选择性复用 FastAPI 官方全栈模板与 Admin 布局。发布使用预构建静态资源，目标服务器不需 Node/pnpm。

## 核心边界

- xmg-qa2 是数字技术支持员工，不是通用多 Agent 编排平台；简单问题优先单 Workflow + Knowledge/Tool，只有未来出现独立职责和独立生命周期时才考虑 Agent-to-Agent。
- 只读客户目标；写操作只给工程师建议，人工回复不能解锁数字员工生产写权限。
- 任务可暂停数天；等待不占 Worker，恢复保留证据、假设和待办。
- 知识优先，能力选择由版本化工作流与 Policy 控制；通用推理贯穿全过程。
- xmg-kb 独立负责批量文档解析、清洗和建索引；xmg-qa2 消费统一 Evidence。
- 任务按客户/项目隔离；外发先脱敏，不能把原始日志送公网后才遮蔽。
- 所有组件替换经过 Contract 与能力测试，不承诺各厂商功能天然等价。

## 开发规则

遵守 [AGENTS.md](AGENTS.md)、[Constitution](.specify/memory/constitution.md) 和 [Spec Kit 流程](docs/governance/SPECKIT-WORKFLOW.md)：

constitution → specify → clarify → plan → checklist → tasks → analyze → 明确编码授权 → implement → converge。

每项 Feature 使用 feature/<number>-<slug> 分支，不在 main 直接开发。设计文档推送不等于运行时已实现、测试通过或生产就绪。

[项目基线](XMG-QA2-PROJECT-BASELINE.md) · [ADR 索引](docs/adr/README.md) · [初始化历史说明](docs/BOOTSTRAP.md)