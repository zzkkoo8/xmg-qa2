# xmg-qa2 架构基线

版本：1.0；日期：2026-09-05；状态：设计完成，Pre-Implementation。产品范围以[需求基线](../requirements/REQUIREMENTS-BASELINE.md)为准。

## 1. 架构决定

采用模块化单体代码库、中央 API 和独立 Worker 进程。LangGraph 负责调查图，Celery + RabbitMQ 负责有界执行段分发，PostgreSQL 负责业务任务和持久检查点。复用现有 Dify 知识服务，不重新构建知识平台。

“XMG Harness”仅是业务控制与适配边界，不自研通用 Agent 框架、消息队列、调度器、向量数据库或低代码平台。选型理由和替代方案见[审计报告](../research/2026-09-05-STACK-AUDIT.md)。

## 2. 部署关系

~~~mermaid
flowchart TD
    U["钉钉 / Web / REST"] --> A["入口与任务 API"]
    A --> P["PostgreSQL：任务 / Inbox / Outbox"]
    P --> D["调度进程：Outbox / 超时巡检"]
    D --> Q["RabbitMQ"]
    Q --> W["Celery Worker / LangGraph"]
    W --> P
    W --> C["PostgreSQL：LangGraph Checkpoint"]
    W --> G["能力网关：ACL / 只读 / 外发策略"]
    G --> K["xmg-kb：已有 Dify"]
    G --> E["官方检索 / API / MCP"]
    W --> H["人工请求 / 结果 Outbox"]
    H --> P
~~~

一个代码库可使用相同构建镜像启动 api、worker、dispatcher、dingtalk 四类进程；不是四个独立微服务项目。业务表与检查点可共用 PostgreSQL 实例，但使用独立 schema 和迁移责任。

最小部署服务：API、Worker、Dispatcher、DingTalk Adapter、PostgreSQL、RabbitMQ。简易 Web 静态资源由 API 提供。Dify/模型是已有外部依赖，不能把它们的资源成本遗漏后宣称“全栈轻量”。

## 3. 技术组件与职责

| 层 | 决策 | 边界 |
| --- | --- | --- |
| 语言/依赖 | Python 3.12 作为首轮兼容测试基线，uv + 锁文件 | 不使用浮动 latest；实际包版本在 Feature Plan 验证后冻结 |
| HTTP | FastAPI + Uvicorn + Pydantic | OpenAPI、请求验证、依赖注入；长调查不占 HTTP 请求或 BackgroundTasks |
| 数据 | PostgreSQL + SQLAlchemy + Alembic；psycopg 连接 | 业务事务、持久待办、证据索引、事件、幂等与版本；每任务独立 Session |
| 图执行 | LangGraph + 官方 PostgreSQL checkpointer | 关键阶段同步持久化；不把 SDK State 当外部 API |
| Worker | Celery + RabbitMQ | 发布确认、持久消息、晚确认、有限重试；任务载荷仅 ID 和版本，不携带凭证/原始日志 |
| 知识 | Dify Knowledge API Adapter | 只返回 Evidence；不嵌套 Dify Agent 或对话工作流 |
| 模型 | ModelProvider + 提供方官方 SDK | 单提供方可运行；LiteLLM 为可选网关，不叠加第二 Agent 框架 |
| 能力 | 官方 MCP SDK + HTTP 工具适配器 + 审核后 Skill 包 | 协议不是权限；内部 Capability ID 唯一，必须经服务端策略 |
| 配置 | YAML/JSON + Pydantic/JSON Schema | 声明阶段、优先级、条件、限制和版本；禁止 eval/任意导入 |
| 观测 | OpenTelemetry + 结构化日志 + 业务审计事件 | 可复用已有后端；Langfuse 为可选 profile，不阻断主流程 |
| 评测 | pytest + 人工标注题集；Ragas 可选离线依赖 | 确定性安全/恢复门禁优先，模型打分仅辅助 |
| Web | 简易 TypeScript/React + Vite 任务页 | 对话、任务、补充、报告；复用 API 鉴权，不做流程编辑器 |

当前未创建运行时代码、依赖锁文件或 Compose 部署文件；上述是实施选型，不是已部署状态。

## 4. 状态归属与可靠性

| 数据 | 唯一责任 | 不能误用为 |
| --- | --- | --- |
| SupportTask/Run/HumanRequest/Event | PostgreSQL 业务表 | 队列结果缓存 |
| 图执行位置、中间图状态 | LangGraph checkpoint | 客户权限或完整工单系统 |
| 可执行 job 的投递 | RabbitMQ/Celery | 跨天等待记录、业务真相 |
| Evidence 元数据与 claim 关系 | 业务库 | 模型自由记忆 |
| 大日志/附件/报告 | 受控 ArtifactStore；V1 加密持久卷，后续 S3 适配 | 每次复制进检查点的无界文本 |
| trace/metrics | 可观测后端 | 唯一审计凭证或恢复依据 |

接受至少一次投递，不承诺外部操作 exactly-once。入口事件、恢复事件、业务操作和最终输出分别用幂等键；同一任务只有一个有效运行者。具体 crash windows 与回收协议见[任务模型](SESSION-EVENT-MODEL.md)。

## 5. 组件间的事务规则

1. API 在同一 PostgreSQL 事务写入 Inbox、Turn/SupportTask 和待发布 Outbox，然后返回 ACK/202。数据库提交失败不得报告成功接收。
2. Dispatcher 只发布已提交的 Outbox；收到 broker confirm 才标记已投递。确认与标记之间崩溃会重复投递，由消费幂等处理。
3. Worker 读取 task_id/run_id/state_version，取得有效执行租约，并从固定图版本恢复。一个执行段到答案、暂停、取消或上限即结束。
4. 图检查点与业务表不是天然原子提交。每步使用稳定 operation_id，业务 StepCommit 与 Evidence/outbox 同事务；checkpoint 记录已提交 operation_id。恢复时对账，不靠两个表恰好同时写成功。
5. 进入等待状态必须已有可恢复 checkpoint，再提交等待记录和通知 outbox。崩溃巡检发现“图已中断但业务还在运行”时补齐等待状态。未持久 checkpoint 的人类请求不得发送。
6. 对同一有效 operation 的结果采用唯一键 upsert；已成功操作的结果先复用。外部请求成功但结果落库前崩溃，可能必须重查；旧证据保留采集时间，不伪装成同一次现场观察。
7. 人工回复经 case/principal/request/version 校验，满足补充条件后在同一事务保存 ResumeAttempt 与恢复 Outbox，再投递新的执行段。恢复意图绑定原 checkpoint/interrupt，图持久消费后才记 APPLIED；崩溃重试先对账，不能把旧回复用于下一 interrupt。晚到回复仅保存为授权补充；详细消费协议见任务模型。
8. Dispatcher 还负责已提交但未投递、失联运行和到期外部等待的对账。使用数据库和 Celery 能力，业务对账器不发展成通用任务框架。

上述是项目设计协议；LangGraph 的[检查点](https://docs.langchain.com/oss/python/langgraph/checkpointers)与[中断](https://docs.langchain.com/oss/python/langgraph/interrupts)并不自行提供全部业务事务保证。

## 6. 权限与扩展

只读限制针对客户目标系统。写入本系统的任务、证据、报告，以及向已配置渠道发出答案/协助请求，是必要业务动作，仍经授权和审计。

生产目标权限由 Registry、服务端 Policy、连接器路由/命令模板、目标账户共同约束。模型建议、MCP annotation、Skill 内容、人工回复都不能提升权限。禁止任何批准后自动执行生产写操作的分支。

所有外发点（检索、LLM、embedding/rerank、工具参数、日志/trace）先做数据策略。公开检索只发送脱敏泛化查询；不能仅在最终答案里打码。原始凭证不进入提示词、checkpoint、队列或普通日志。

扩展兼容依赖版本化 Contract 和能力测试；“Provider neutral”不意味着不同模型、MCP 服务和知识库能力完全相同。不支持的过滤、流式、取消和版本快照必须明确返回，不得默默降级。

## 7. 运维与扩容

- V1 Compose 单机是部署便利，不具备主机级高可用。持久卷、恢复备份和镜像回退必须在发布验收中实测。
- RabbitMQ 使用持久队列/消息及发布确认；V1 不把单节点 quorum 宣传为高可用。将来 HA 采用至少三个合适部署节点并单独设计 DB/存储容灾。
- 增加 Worker 前必须通过同 Case 并发与租约失联测试。每 case 限流，加全局/模型/工具并发配额，避免租户霸占资源。
- 先观察队列延迟、活跃槽、数据库连接、模型限流和恢复指标，再决定多机/K8s。没有这些证据不预先拆微服务。
- Temporal 仅在跨服务长事务、大量持久定时器或现有 Temporal 平台出现时重评；它可替换调度/恢复层，不能和 Celery 无边界重复调度。
- 默认不加 Redis、独立向量库、LangSmith 商业平台或同时部署多种 LLM 观测系统。
