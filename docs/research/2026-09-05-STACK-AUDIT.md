# xmg-qa2 技术栈与架构审计

日期：2026-09-05；受众：项目负责人、架构与实施工程师。

审计基准：[main 提交 a2c5399](https://github.com/zzkkoo8/xmg-qa2/tree/a2c5399f7c86c19913ca857e7745544e30e0f6c5)。旧 docs/001-support-agent-design 分支逐文件 SHA 与该基线一致。本轮交付为研究与设计修订，不包含业务实现或实际部署测试。

## 1. 结论

现有 LangGraph + FastAPI + Pydantic + Provider Contract 的方向仍适合 xmg-qa2，无需追逐热门项目重写。真正不足的是产品需求与设计未同步，以及持久任务、只读权限、恢复与交付闭环没有落到可验证的协议。

建议采用：

- 核心：Python + FastAPI/Pydantic + LangGraph。
- 业务持久化：PostgreSQL + SQLAlchemy/Alembic；图检查点使用官方 PostgreSQL checkpointer。
- 后台执行：Celery + RabbitMQ，仅分发有界运行段；Case 跨天等待存数据库，释放 Worker。
- 知识：先复用现有 Dify 承载的 xmg-kb，经纯检索 Adapter 返回 Evidence。
- 扩展：官方 MCP SDK、已审核 Skill、HTTP/API 工具，统一经过能力 Registry 和服务端 Policy。
- 观测与评测：OpenTelemetry、结构化业务审计、人工题集；LiteLLM、Langfuse、Ragas 按需加入。
- 入口：真实钉钉 + REST + 简易 Web 任务页；V1 Compose，后续按负载扩 Worker。

这是基于已确认需求、已有基础和运维成本的首选，不是已被全行业基准证明的唯一最优方案。LangGraph 官方描述的状态化、确定性/Agent 混合工作流与此需求匹配；其客户采用名单属于官方自述，不构成本项目性能或成功率证明。[LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)

## 2. 如何使用排行榜

检索包括 GitHub Topics/按 Stars 排序入口、项目官方仓库、发布记录、功能文档、协议和许可证；搜索出现的商业比较文章只用于发现候选，不作为技术结论证据。[GitHub AI Agents Topics](https://github.com/topics/ai-agents?o=desc&s=stars)

未找到可用于证明“全球最佳技术支持 Agent 架构”的统一权威排行榜。因此以下呈现的是本次相关候选的热度快照，而非冒称全网完整排名：21 个指定仓库，GitHub REST API 返回的 stargazers_count 与 pushed_at，访问日 2026-09-05，同批查询并非严格同一秒。所有样本 archived=false，但未归档不等于持续新增功能。

Stars 衡量累计关注度，受项目年龄、语言、受众影响；最近 push 也不证明某特性稳定。不能把 Dify 平台、Pydantic 数据验证库、消息队列与 Agent 框架混成一个优劣总榜。API license 的 NOASSERTION 或自动识别值不代替读 LICENSE，AutoGen 就有代码和文档不同许可。

### Agent 编排框架

| 项目 | Stars | 最近推送（UTC） | 场景与许可提示 |
| --- | ---: | --- | --- |
| [microsoft/autogen](https://github.com/microsoft/autogen) | 60,800 | 2026-04-15 | 维护模式；新项目转向 MAF；代码 MIT/文档 CC-BY-4.0 |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 58,091 | 2026-09-04 | 角色团队、Crews/Flows；MIT |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 41,066 | 2026-09-03 | 显式状态图与持久中断；MIT |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 29,197 | 2026-09-02 | 轻量工具 Agent、交接、HITL；MIT |
| [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | 19,729 | 2026-09-05 | 类型化 Python Agent；MIT |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | 13,331 | 2026-09-05 | Python/.NET、图工作流与微软生态；MIT |

### 知识与检索平台/框架

| 项目 | Stars | 最近推送（UTC） | 场景与许可提示 |
| --- | ---: | --- | --- |
| [langgenius/dify](https://github.com/langgenius/dify) | 154,469 | 2026-09-04 | 现有知识服务；附加条件许可 |
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 90,055 | 2026-09-04 | 复杂文档与检索平台；Apache-2.0 |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 52,023 | 2026-09-03 | 数据连接器与索引框架；MIT 核心 |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 26,418 | 2026-09-04 | 模块化检索/生成管线；Apache-2.0 |

### 异步任务与持久工作流候选（不同类别，不作质量排名）

| 项目 | Stars | 最近推送（UTC） | 场景与许可提示 |
| --- | ---: | --- | --- |
| [celery/celery](https://github.com/celery/celery) | 28,860 | 2026-09-03 | 分布式任务队列；BSD |
| [temporalio/temporal](https://github.com/temporalio/temporal) | 22,829 | 2026-09-05 | 持久工作流服务；MIT |
| [taskiq-python/taskiq](https://github.com/taskiq-python/taskiq) | 2,319 | 2026-08-31 | Python async 任务队列；MIT |
| [procrastinate-org/procrastinate](https://github.com/procrastinate-org/procrastinate) | 1,376 | 2026-08-31 | PostgreSQL 任务队列；MIT |

### 其他相关组件（样本内按 Stars 排序）

| 项目 | Stars | 最近推送（UTC） | 场景与许可提示 |
| --- | ---: | --- | --- |
| [fastapi/fastapi](https://github.com/fastapi/fastapi) | 102,080 | 2026-09-01 | API；MIT |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 58,056 | 2026-09-05 | 模型网关；MIT 核心/enterprise 另有许可 |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | 34,207 | 2026-09-04 | LLM 观测；MIT 核心/ee 另有许可 |
| [pydantic/pydantic](https://github.com/pydantic/pydantic) | 28,716 | 2026-09-04 | 数据验证；MIT |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | 24,204 | 2026-09-05 | 官方 MCP SDK；MIT |
| [rabbitmq/rabbitmq-server](https://github.com/rabbitmq/rabbitmq-server) | 13,836 | 2026-09-05 | 消息 broker；以固定版本 LICENSE/NOTICE 为准 |
| [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | 11,330 | 2026-09-04 | LLM 观测/评测；Elastic License 2.0 |

## 3. 三条架构路线的取舍

| 路线 | 成立条件 | 优点 | 对本项目的代价 | 决定 |
| --- | --- | --- | --- | --- |
| A：LangGraph + 薄业务控制层 + Celery/PG | 需要显式调查图、配置能力、已有 LangGraph 设计 | 状态图、持久中断、Provider 隔离清晰 | 仍须补业务 Case、投递幂等、恢复对账 | 采用 |
| B：Pydantic AI + Temporal | 类型驱动开发，已有 Temporal 团队/平台，跨服务长流程多 | 强类型 Agent 与持久执行可组合 | 多一套服务运维，重建已有工作流边界 | 有力替代，条件触发再评估 |
| C：Dify/RAGFlow 平台为主要应用中枢 | 低代码、快速搭 RAG 应用优先 | 一体化配置、知识处理 | 定制 Case/租约/只读策略和开放契约仍需要外围系统；双中枢易冲突 | Dify 保留知识角色，不掌控 xmg-qa2 Case |

Pydantic AI 的官方持久执行能力包含 Temporal 等集成，不能将其描述为不能恢复；Temporal 本身提供持久 Workflow 与任务调度，但 Activity 仍需要考虑重复执行。多装一个引擎不会自动消除业务幂等问题。[Pydantic AI durable execution](https://pydantic.dev/docs/ai/capabilities/durable_execution/overview/)、[Temporal Activity definition](https://docs.temporal.io/activity-definition)、[Temporal 生产准备](https://docs.temporal.io/self-hosted-guide/production-checklist)

### 其他 Agent 框架为何不作为默认

| 候选 | 适用场景 | 对 xmg-qa2 的判断 |
| --- | --- | --- |
| CrewAI | 角色协作、内容生产、审批流 | Flows 实际支持持久化与人类反馈；不是不能用，但本项目核心是单一支持 Case，没有角色群协作收益 |
| OpenAI Agents SDK | 轻量工具调用、Agent handoff、HITL | 有 RunState 和持久执行集成，非仅限 OpenAI 模型；为本项目建立强显式图仍需额外工作 |
| Microsoft Agent Framework | Python/.NET、Microsoft 企业生态、图编排 | 已有 checkpoint 方案，不能沿用旧“预览版”标签；当前项目没有 .NET/Azure 绑定收益 |
| AutoGen | 存量项目维护 | 官方已明示维护模式；60,800 Stars 不足以抵消新项目选型风险 |

依据：[CrewAI Flows](https://docs.crewai.com/en/concepts/flows)、[Human feedback](https://docs.crewai.com/en/learn/human-feedback-in-flows)、[OpenAI Agents SDK HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/)、[SDK 仓库](https://github.com/openai/openai-agents-python)、[MAF checkpoints，2026-09-04 更新](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints)、[AutoGen README](https://github.com/microsoft/autogen)。

## 4. 最关键的可靠性结论

LangGraph 可通过持久检查点中断等待并恢复，但恢复会重新执行中断节点开头的代码，不能假定从某条 Python 指令继续。其同步/异步持久化也有不同崩溃窗口，生产不能沿用内存 Saver。项目应使用稳定 PostgreSQL 检查点、固定 runtime_key/图版本、幂等 StepCommit；大文件仅放引用。[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

Celery 的默认确认、晚确认和 Worker 丢失语义需要明确配置；重试无法保证外部调用只发生一次。RabbitMQ 是 Celery 支持的成熟 broker，发布确认和持久消息仍不能替代业务 Inbox/Outbox 对账。[Celery Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)、[Celery RabbitMQ](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html)

设计上选择 RabbitMQ 而暂不引入 Redis，是为了职责清晰，非声称 Redis 不可生产使用。Redis broker 的 visibility timeout/远期任务限制要求额外注意；本系统无论使用哪种 broker，等待工程师数天都应退出 Worker，把等待条件存 PG。[Celery Redis](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html)

Procrastinate 可复用 PostgreSQL 减少 broker，但官方文档目前公开寻求维护者，并说明强杀后 stalled jobs 必须处理；结合该项目优先主流生态的要求，暂不采用。Taskiq 保持 async 场景候选，不为减少一个服务而推翻成熟 Worker 方案。[Procrastinate 文档](https://procrastinate.readthedocs.io/)、[stalled jobs](https://procrastinate.readthedocs.io/en/stable/howto/production/retry_stalled_jobs.html)、[Taskiq](https://github.com/taskiq-python/taskiq)

单机 Compose 不等于高可用。未来 RabbitMQ quorum/PG 容灾需独立设计，不能通过“单容器持久化”推导出主机故障无损保证。[RabbitMQ Quorum Queues](https://www.rabbitmq.com/docs/quorum-queues)

## 5. 知识与插件结论

Dify 现有纯检索 API 返回片段、文档标识及相关度，足够作为首个 KnowledgeProvider。当前文档 query 长度上限为 250；未直接证明用户安装实例具备细粒度客户 ACL。Adapter 应先映射可访问 dataset，权限不明时拒绝扩大检索；不要将界面过滤能力当作 REST 权限保证。[Dify 检索接口，2026-09-01 更新](https://docs.dify.ai/en/api-reference/knowledge-bases/retrieve-chunks-from-a-knowledge-base-test-retrieval)

RAGFlow 适合复杂文档/检索，Haystack 适合自主掌控模块化管线，LlamaIndex 适合连接器/索引扩展。只在相同原文、标注问题、权限要求下评测出收益再迁移；本轮没有证据证明换引擎能修复已有杂乱数据或提高中文产品问答质量。RAGFlow 默认 API 页为开发文档时，字段不能直接套用到已安装版本。[RAGFlow 检索 API](https://ragflow.io/docs/http_api_reference#retrieve-chunks)、[Haystack](https://github.com/deepset-ai/haystack)、[LlamaIndex](https://github.com/run-llama/llama_index)

MCP 的 annotations 不是安全承诺，Skill 的 allowed-tools 也不是独立沙箱。用官方 SDK 解决协议，用项目 Policy、目标账号、路由和参数限制落实只读。知识片段/网页/工具内容作为数据，不自动拥有安装插件、调用凭证或改变工作流的权限。[MCP Tools 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)、[Agent Skills specification](https://agentskills.io/specification)

## 6. 模型、观测与许可证

| 组件 | 决策 | 依据和具体限制 |
| --- | --- | --- |
| FastAPI/Pydantic | 保留 | 类型验证、OpenAPI 和 DI 适合稳定接口；Pydantic 数据模型不等于再引入 Pydantic AI 框架 |
| LiteLLM | 可选 | 多厂商路由、集中额度有价值，但协议统一不保证所有模型同样支持 structured output/tool calling；fallback 必须保持数据授权范围 |
| OpenTelemetry | 必需接口 | 可跨后端追踪 task/run/tool，业务恢复不能依赖某遥测 SaaS |
| Langfuse | 可选 profile | 自托管 Compose 需要多项后端；不能写成只加一个轻量容器 |
| Phoenix | 替代调试候选 | 当前为 Elastic License 2.0，不应误标为 MIT/Apache |
| Ragas | 离线辅助 | faithfulness 衡量回答与上下文支持关系，错误/过时原文仍可获得高支持度分数 |

依据：[FastAPI features](https://fastapi.tiangolo.com/features/)、[LiteLLM 文档](https://docs.litellm.ai/docs/)、[LiteLLM fallback](https://docs.litellm.ai/docs/proxy/reliability)、[OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/)、[Langfuse Compose](https://langfuse.com/self-hosting/deployment/docker-compose)、[Phoenix LICENSE](https://github.com/Arize-ai/phoenix/blob/main/LICENSE)、[Ragas faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)。

Dify 为附加条件的 Apache 2.0，workspace 多租户/前端标识有额外条款；本项目在一个内部运营组织接入 KB，仍需在实际部署形态下确认条件，不把客户 case 数据隔离直接等同于许可证允许的多 workspace SaaS。Langfuse、LiteLLM 的 MIT 核心不涵盖全部企业目录。LangGraph 库与商业 LangSmith 也不是同一许可范围。[Dify LICENSE](https://github.com/langgenius/dify/blob/main/LICENSE)、[Langfuse LICENSE](https://github.com/langfuse/langfuse/blob/main/LICENSE)、[LiteLLM LICENSE](https://github.com/BerriAI/litellm/blob/main/LICENSE)、[LangSmith 自托管许可](https://docs.langchain.com/langsmith/self-hosted)

版本与安装渠道必须分开核验。例如 LiteLLM v1.99.1 官方说明为 2026-09-02 Docker-only 发布，不能写成同版本 pip 安装命令。MCP SDK 当前官方 README 已使用 v2 稳定线，不能照搬旧版本认知。本轮不制造“已兼容”的锁文件，实施 Plan 必须验证 Python、包、镜像 digest、数据库驱动、checkpointer 和协议组合。[LiteLLM v1.99.1 release](https://github.com/BerriAI/litellm/releases/tag/v1.99.1)、[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

钉钉首批采用官方 Stream SDK；官方 SDK 支持事件、机器人消息与卡片回调。长任务回复需要适配长期收件标识，不依赖短期回调 URL；真实机器人权限/联调由实施阶段确认。[DingTalk Stream Python SDK](https://github.com/open-dingtalk/dingtalk-stream-sdk-python)

## 7. 仓库审计发现与修订

| 级别 | 原设计证据（本轮基线） | 问题及处理 |
| --- | --- | --- |
| High | README/Architecture/Design 的 V1 排除真实 KB、钉钉、API | 与 Q1C 不符；改为多 Feature 完成真实垂直闭环，Fake 留在测试 |
| High | SESSION-EVENT-MODEL 仅 Thread/Turn；设计 Investigation 挂 Turn 下 | 增加 SupportTask/Run/HumanRequest，跨轮证据归属 Case |
| High | Workflow/Design 允许 CONTROLLED_WRITE/HIGH_RISK 经审批 | 与 Q3A 冲突；目标写动作始终拒绝，人工请求只补证据/接手 |
| High | Workflow 只记录 workflow_version 与基本限制 | 增加配置 hash、版本兼容、无进展终止、恢复权限检查 |
| High | 架构仅“可恢复或至少明确重放” | 升级为持久恢复验收，补 Inbox/Outbox、幂等、租约、checkpoint 对账 |
| High | Constitution 仍有 PROJECT_NAME/PRINCIPLE 占位符 | 写入真实项目宪法，明确设计授权不等于编码授权 |
| Medium | Knowledge 把 retrieve 列为必需又允许不支持 | 改为 search 必需、原文/快照能力显式可选 |
| Medium | 线性依赖箭头可能暗示 plugins 依赖 runtime 业务 | 改为端口与适配器矩阵、composition root，禁止循环/Provider 泄漏 |
| Medium | Git extension branch_template/prefix 为空 | 配置 feature/{number}-{slug}，使用现有脚本 dry-run 验证；不修改第三方脚本 |
| Medium | 无任务级数据外发、通知失败、验收题集口径 | 增加外发矩阵、HumanRequest/Outbox、质量与恢复验收 |

本表为文档审计，不冒充已执行 Spec Kit Analyze 或运行时安全审计。新的运行恢复协议是待实现设计，不能据此宣称问题已在软件运行中修复。

## 8. 证据缺口、反证与停止条件

| 判断 | 当前依据与把握 | 未解决部分 | 下一步 |
| --- | --- | --- | --- |
| LangGraph 适合有状态支持调查 | 官方能力明确，高；项目适配为工程判断，中高 | 性能/版本组合未安装验证 | Feature 中最小持久中断与双 Worker 故障测试 |
| Dify 应先保留 | 已有资产 + 官方纯检索 API，中高 | 实际版本/连通/ACL/内容质量未知 | 固定测试集、鉴权隔离、真实 retrieval |
| Celery/PG 能承接持久任务 | 组件能力明确；组合协议为设计判断 | 没有现成组件自动替项目完成双写一致性 | 验证 crash windows/租约/重投 |
| 热度反映主流关注 | 官方 API 精确快照，高 | 不是采用率、性能或全网总榜 | 不再追加相似营销榜单 |
| 只读/外发边界 | 需求明确，协议约束充分 | 具体产品只读 API 与账号未验证 | 注册前做操作风险/权限契约测试 |
| 成本与 SLO | 已提供可测默认目标 | 未拿到生产硬件、模型、请求规模 | 记录实际延迟、费用、队列和恢复指标 |

已完成首轮候选检索、官方能力跟进、许可证/版本反证、核心恢复语义复核和仓库逐文档核对；更多泛搜不太可能改变“保留 LangGraph、补真实闭环”的结论，因此停止扩散搜索。

范围限制：本轮无法证明穷尽“全网”；没有访问客户生产设备、用户 Dify 服务、钉钉应用或模型 Key；没有进行部署、负载、真实 KB 质量或 SDK 兼容性实测。钉钉部分官网页面未能展开，使用其官方 GitHub SDK 作为可核查来源。所有默认选项和待联调条件均保留于[需求基线](../requirements/REQUIREMENTS-BASELINE.md)与[交付计划](../plans/V1-DELIVERY-PLAN.md)。

## 9. 本轮文档验收记录

2026-09-05 完成独立只读复核：初次发现 1 项 Important（恢复回复持久接收与图消费之间的崩溃窗口）和 1 项 Minor（AGENTS 旧 Evidence 字段清单）。已补 ResumeAttempt、interrupt ID 定向恢复、检查点消费对账与对应故障注入验收；Evidence 字段统一引用 Knowledge Contract。定点复核确认两项关闭，未发现新增文档矛盾。

实际检查结果：

- Python 检查 25 份 Markdown 的代码围栏及 64 个本地链接，解析 1 个 YAML 示例与 Git 配置：0 错误。
- Git extension 执行 `--dry-run --json --number 2 --short-name support-agent-baseline`：返回 `feature/002-support-agent-baseline`，未创建运行时 Feature。
- `git diff --check HEAD`：通过；25 个变更文件均为文档、目录说明或 Git 治理配置，没有业务代码。
- 再次抽查 LangGraph 中断恢复、Celery Worker 丢失、MCP annotations 与 AutoGen 维护状态的上述官方依据，支持当前设计取舍。

以上是研究与文档验收；未执行 Unit/E2E、SDK 兼容性、实际服务部署或 Spec Kit Analyze，不能据此开放业务编码或宣称 V1 已交付。
