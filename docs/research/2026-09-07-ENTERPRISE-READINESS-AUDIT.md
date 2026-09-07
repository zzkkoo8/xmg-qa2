# 企业级 QA 与编码开工审计

审阅时间：2026-09-06 至 2026-09-07（UTC）。性质：仓库设计审计、官方资料核验、独立只读复核；不是业务测试、安全认证或生产验收。本次只新增审计与交接索引，不把建议冒充已修复的实现。

## 1. 结论与实际版本

**可以开始首个 Feature 的规格与实现准备；不能跳过 Feature 门禁直接全面编码；不能宣称企业生产就绪。保留主要架构，不需要推倒重选全部组件。**

审计对象是 `zzkkoo8/xmg-qa2` 的 `feature/002-support-agent-baseline`，提交 `fd5e19c813aa86e8c56830fdb0cd197f28b85c9f`。核验时 `main` 为 `a2c5399f7c86c19913ca857e7745544e30e0f6c5`；[PR #2](https://github.com/zzkkoo8/xmg-qa2/pull/2) 仍为 Draft、未合并。只克隆 main 不会获得这套最新设计；实施应基于经审查的设计分支，或后来包含同等设计的 main。

逐份阅读 35 份产品/治理 Markdown，并检查目录和 Spec Kit 配置。`src/xmg_qa2` 与 `tests` 只有占位文件；`specs` 只有 README；没有运行时 Feature spec/plan/tasks/analyze、依赖锁文件、应用构建包或 CI。它们是当前开发阶段的真实缺项，不能仅据此倒推出架构错误，也不能把文稿中的目标指标当作实测成绩。

| 判断对象 | 结论 | 边界 |
| --- | --- | --- |
| 高质量问答产品方向 | 基本满足设计要求 | 质量正确与否仍需真实题集、模型和知识库验证 |
| 企业内部 MVP 架构 | 有条件通过 | 范围是单运营组织、客户/项目隔离，不是多租户 SaaS 或主机高可用承诺 |
| Codex 开始工作 | 可以开始首个 Feature 的规格和准备 | 使用既定 Spec Kit 流程，不重复访谈已确认需求 |
| 当前直接全面编码 | 不具备门禁完成证据 | 对当前 Feature 明确授权并完成其门禁后才实现；本次审计不自动授权编码 |
| 插件化与个性化 | 设计支持，尚未实现 | 还需实际接口、参考插件和契约测试；不承诺全部功能零代码 |
| 企业生产发布 | 尚不具备条件 | 真实接入、质量、权限、恢复、安装及运维验收均待实施 |

## 2. 已经做对的部分

- **问答优先**：QA Core 将问题理解、子问题覆盖、最小澄清、检索恢复、按缺口选动作、答案检查放到核心；工具不是越多越好。稳定低风险通用问题可显式直答，产品事实仍知识优先。
- **证据裁决**：版本匹配、时效、来源、直接性和反证共同参与判断；“现场能运行”不自动等于“官方支持”。引用由服务端解析，不信模型编造的链接或 ID。
- **持续调查与求助**：SupportTask 高于 Turn，缺信息、服务故障、无进展可暂停；回传和恢复有 request/interrupt 关联，不丢此前已收集材料。
- **权限与外发**：客户目标只读、未知动作默认拒绝；知识进入模型前检查范围；搜索、模型、工具、观测均经过外发策略。人工补充不能解锁 Agent 的生产写权限。
- **工程边界**：端口与适配器、配置驱动工作流、能力注册、核心与 Provider 解耦；Dify 不承担第二套任务/Agent 中枢。
- **质量验收**：20 个合成控制场景在第一 Feature；真实问答阶段至少 100 个冻结标注题，与单次 RAG 对照。覆盖、引用支持、正确回答、合理求助和调查成功都有分母，避免靠拒答刷分。
- **Web 与交付**：同一 React SPA 的 Chat/Admin、后端权限、模板隔离、在线/离线包、数据库与附件字节一致备份已有设计。不能把这些已覆盖内容重新写成“完全缺失”。

依据：[QA Core](../architecture/QA-CORE.md)、[答案质量](../governance/ANSWER-QUALITY.md)、[任务协议](../architecture/SESSION-EVENT-MODEL.md)、[展示契约](../architecture/PRESENTATION-CONTRACT.md)、[分发设计](../architecture/DISTRIBUTION-DEPLOYMENT.md)。

## 3. 问题清单与关闭阶段

下列编号用于后续 Feature 跟踪；本报告没有把任何一项标记为实现完成。Important 表示会影响相应功能验收，不代表必须停止一切规格工作；未发现需要停止全部设计/规格工作的 Critical。

### A01：运行时规格与可执行契约尚未生成——开工准备项

证据：`specs/` 尚无运行时 Feature；[交接文档](../plans/IMPLEMENTATION-READINESS.md) 已如实列出缺口。现有 Contract 是设计文稿，不是已安装的 Python/TypeScript SDK。

关闭条件：首个 Feature 生成 spec、plan、checklist、tasks、analyze，冻结最小数据模型、迁移、OpenAPI、错误码、版本锁和测试任务。不要先写全部业务代码再补规格；也无需用户手工撰写这些技术产物。

### A02：持久执行组合需要真实兼容验证——Important，首个 Feature 验收项

证据：[任务协议](../architecture/SESSION-EVENT-MODEL.md) 第 66–98 行已经定义锁/epoch、checkpoint 写保护、ResumeAttempt 和崩溃窗口，但尚无真实测试。LangGraph、Celery、PostgreSQL 各自成熟，不能自动证明三者之间的事务和恢复组合正确。

LangGraph 恢复会重新执行中断节点开头的代码；Celery 的 `acks_late` 也不等于所有子进程退出都会重投。因此业务幂等、重投策略、连接生命周期及持久恢复必须联合验证。[LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)

关闭条件：在获准的首个 Feature 内，以真实 PG/checkpointer/broker 验证进程死亡、重复消息、双 Worker、旧 epoch 拒写、连接断开、证据已保存而 checkpoint 未更新、旧回复已消费后到下一 interrupt 等窗口。区分 ACK、执行成功和业务完成；不宣称 exactly-once。该验证应是首个 Feature 的早期风险验证与退出门禁，而非要求在任何代码出现前已有集成测试结果。

若受支持的 checkpointer 扩展无法可靠落实 fencing，应停止后续依赖工作、形成 ADR 再调整执行方案；不能跳过检查，也不应仅凭尚未测试就断言当前方案不可行。

### A03：流式草稿的内容外发检查顺序不明确——Important，真实答案展示前关闭

证据：[Web](../architecture/WEB-CONSOLE.md) 第 20、57 行允许未完成验证的草稿流；第 55 行已校验每次 SSE 发送及重放的当前会话与 Case ACL。[QA Core](../architecture/QA-CORE.md) 第 82–84 行则在生成后检查答案。这里缺的是**草稿内容是否允许展示**，不是完全缺少订阅者鉴权。

风险：将内容标为草稿，不能收回已经暴露的秘密、越权引用或不允许发布的建议。最终答案检查不能替代首次字节外发前的安全检查。

建议默认：先流式展示受控进度与等待信息，答案缓冲检查后再发布；若需要逐段答案流，只放行完成相应内容/权限检查的片段，并处理跨片段秘密匹配。事实完整性仍在最终答案检查，不能把“安全过滤”误写成保证事实全对。[OWASP AI Agent 安全指导](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)

验收：模型先产出含秘密或越权引用的草稿、最终检查拒绝时，浏览器与事件重放均不得先看到禁止内容。归入真实问答和完整 Chat Feature；首个 Feature 的事件契约预留该边界。

### A04：群聊发送缺少完整受众语义——Important，钉钉出站前关闭

证据：[需求](../requirements/REQUIREMENTS-BASELINE.md) 第 47 行默认原会话/支持队列通知；[任务协议](../architecture/SESSION-EVENT-MODEL.md) 第 10 行允许同群多案，第 64 行规定 destination 幂等；[工作流](../architecture/WORKFLOW-MODEL.md) 第 113 行要求配置收件映射。FR07 已要求输出权限检查，但没有具体说明群目的地与 Case 授权受众的对应规则。

风险：提问者能读某 Case，不代表群内所有人都能读。支持队列同样可能跨客户；通知正文、任务标题、摘要和链接描述都可能包含敏感信息。

关闭条件：Channel 出站契约定义受管理的 `audience_scope`，发送和重试前复核当前授权。可用受管理的授权群范围或成员校验，不要求不现实的每次全量枚举。无法确认群范围、混合客户或授权变化时，默认无敏感内容通知加登录后受控链接，或转授权私聊；已发出的群消息不能承诺事后可靠撤回。测试“获准用户在未获准群提问”及排队后授权变化。

### A05：插件执行隔离和远端清单变更需落地——Important，自主取证 Feature

证据：[插件契约](../architecture/PLUGIN-CONTRACT.md) 第 13–22、30–40 行已有版本/hash、来源审核、独立进程/容器、不信 annotations、SSRF/鉴权要求。不能将其描述为“任意插件可执行”或“没有沙箱要求”。但实际执行 profile 和远端工具变化后的重新准入仍待冻结。

关闭条件：明确文件挂载、网络出口、凭证可见范围、CPU/内存/时限及异常隔离；独立进程本身不等于安全沙箱。远端 MCP 的工具集合可随时间和授权变化，内部已审核 capability 应绑定相应服务/授权范围及工具 Schema 等审核指纹；新增或不兼容变更不得自动扩权，必须重验或暂停。列表变化通知是线索，不是授权依据。[MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)

同时验证 token 受众与不同服务的凭证边界，不把 Chat 会话 token 直接透传给任意 MCP/下游服务；工具清单缓存不能跨授权范围复用。测试同名工具变更、删除/新增、旧 Case 恢复时能力已禁用、插件超时或尝试越界。[MCP 安全最佳实践](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)

### A06：附件接收与解析范围待冻结——Important，日志/附件 Feature

证据：[任务协议](../architecture/SESSION-EVENT-MODEL.md) 第 19 行已有 Artifact MIME/大小/hash/权限；[QA Core](../architecture/QA-CORE.md) 第 72 行已有大日志有界处理和不支持格式 fallback。缺的是格式、字节/数量/配额、真实类型检查、暂存状态、解析失败及压缩包策略的具体契约。

建议 V1 先接受受限文本日志/配置片段，不支持的格式明确拒绝或请用户提供文本；若增加解析 Provider，先解释与 AGENTS 3.3“QA 不负责 PDF/PPT/Word 解析”的关系，不在 Chat 内偷偷搭第二套知识入库管线。必须限制大小和展开量、避免路径穿越和危险文件名；仅信客户端 MIME 不够。[OWASP 文件上传指导](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

验收：超限、伪装类型、异常编码、压缩炸弹/禁止压缩格式、跨 Case 引用、解析故障不拖死 Worker；未经允许的附件不进入模型、搜索或解析器。

### A07：插件作者交付件尚未形成——对应 Feature 的开发项

闭合方式：实现稳定的 Protocol/Pydantic 数据契约、最小 Manifest 示例、参考 Adapter、注册说明和可运行合约测试套件。内置 Provider 在 composition root 装配；确有独立安装的可信 Python 插件需求时可采用标准 entry points，发现机制不代替审批/权限。不要自研包管理器。[Python Packaging 插件发现](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/)

验收：新增一个测试 Knowledge/Tool Provider 只改插件和注册/配置，不改核心工作流；不兼容契约明确拒绝；禁用后旧任务也不能调用。UI 插件仍是构建期代码，不伪称热加载任意 JS。

### A08：真实质量与生产运维证据待补——集成/发布门禁，不阻塞起步

真实 KB/模型/钉钉/只读端点和冻结题集尚未在本仓库验证。先完成真实问答基线再扩充 Admin；100 题是 V1 下限，不代表能覆盖所有企业场景。题目按实际产品/版本/故障分布扩展，失败样本进入开发集而非反复调整冻结集。

发布前由部署组织确认身份模式及是否强制 SSO/MFA、数据范围、保留/删除要求、备份频率和主机灾难 RPO/RTO、告警接手人、凭证轮换及审计导出。需求中的进程故障恢复时间不能当作主机灾难 RTO。保留策略应覆盖附件、证据、检查点、报告、缓存及备份中的派生副本，明确哪些仅到备份过期后消除。

现有分发文稿已要求一致备份包含真实附件字节、冻结所有写入口和恢复验证；这里补的是组织目标与实测证据，不是“完全没有备份”。Compose 单机不是主机高可用；若组织提出 HA/多站点或更严格合规要求，另建需求/ADR，不自动添加 Kubernetes、计费系统或通用 IdP。

### A09：门禁文案有时间语义歧义——Minor，首个 Plan 澄清

[Spec Kit 流程](../governance/SPECKIT-WORKFLOW.md) 第 32 行写“展示产物后批准编码”，交接执行文本则允许事先对一个明确 Feature 授权、通过门禁后不重复批准。应在开工记录明确当次授权范围及生效条件，不能用旧文稿抹去新的明确授权，也不能将“审计/继续”解释为批准所有实现。A02 的“实现前集成验收”同样应明确为首 Feature 内早期验证、阻塞其退出/后续依赖，而非不可执行的循环前置。

## 4. 技术栈核验：适合保留，不宣称唯一最成熟

“最主流”“AI 最擅长”“企业最佳”没有跨场景统一排行榜。采用支持状态、功能匹配、公开实现、运维负担和替换边界判断；先前 Stars 快照仅说明当时热度，不是当前质量排名。以下保留/替换结论是结合官方能力与本项目需求的工程判断，不是厂商认证。

| 层次 | 当前选择与判断 | 依据及注意事项 |
| --- | --- | --- |
| API/Schema/数据库 | 保留 FastAPI、Pydantic、SQLAlchemy/Alembic、PostgreSQL | 适合类型化接口与事务领域；选受支持 PG 主版本，兼容测试后锁版本。[FastAPI 模板](https://fastapi.tiangolo.com/project-generation/)、[PG 支持政策](https://www.postgresql.org/support/versioning/) |
| Agent 工作流 | 保留 LangGraph | 显式图、持久中断适合人类协助；不把图 checkpoint 当业务事务。[持久化](https://docs.langchain.com/oss/python/langgraph/persistence) |
| 后台调度 | 有条件保留 Celery + RabbitMQ | 成熟任务生态，不自动提供整个 Case 的可靠执行语义；以 A02 验证组合，不叠加第二执行中枢。[Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html) |
| 知识库 | 保留既有 Dify 的 Knowledge Adapter | 有正式 retrieval API；客户部署版本/过滤与权限需实测。现有资产和解耦是选择理由，不是认定其检索效果必然第一。[Dify 检索 API](https://docs.dify.ai/en/api-reference/knowledge-bases/retrieve-chunks-from-a-knowledge-base-test-retrieval) |
| MCP/插件 | 官方 MCP Python SDK + 内部稳定 Contract | 核验时 SDK v2 为稳定线、v1 保留关键修复；接口在演进，禁止不锁版本照搬旧样例。协议协商不等于安全准入。[官方 SDK](https://github.com/modelcontextprotocol/python-sdk) |
| Chat/Admin | 保留 React/TypeScript/Vite、Tailwind/shadcn、TanStack；选择性复用 assistant-ui | FastAPI 官方模板采用同类前端组合；ExternalStoreRuntime 可对接自有状态，不提供本产品全部鉴权/任务机制。[FastAPI 模板](https://fastapi.tiangolo.com/project-generation/)、[assistant-ui](https://www.assistant-ui.com/docs/runtimes/custom/external-store) |
| 部署/观测 | 保留 OCI + Compose、OpenTelemetry 接口 | 契合单机首发；真正成熟度靠安装/恢复演练证明。Langfuse/LiteLLM 等仍按实际需求启用，避免为热门而增加必选依赖 |

没有发现必须换成 Dify Agent、全套聊天平台或另一套 RAG 框架的证据。若 A02 验证显示自定义持久调度维护成本不可接受，可在 ADR 中比较 Temporal 等专用持久执行方案；这是替代评估而非与现有执行层全量叠加。[Temporal AI 场景](https://docs.temporal.io/ai)

## 5. 插件化到底能扩展到什么程度

| 用户需求 | 设计方式 | 是否通常需要代码/构建 |
| --- | --- | --- |
| 换已支持模型/知识库连接、调能力优先级 | Provider 配置 + 版本化 Workflow/Policy | 同一契约支持的能力通常改配置；仍需校验和发布 |
| 接入新的厂商 API/知识接口 | 新 Adapter，注册能力和 Schema | 需要插件代码/合约测试；不应改 Harness Core |
| 接入远端 MCP | 通用 MCP Adapter + 审核后的工具绑定 | 已实现通用适配范围内可配置接入；不能自动信任全部远端工具 |
| 调整工作流条件/顺序/预算 | YAML/JSON、已注册节点和谓词 | 改已有组合不改代码；新业务节点/语义需要 Feature |
| 扩展工程师操作指南 | 审核后的 Skill/资源包 | 文本可配置；脚本仍需执行策略和隔离，不扩权 |
| 改 HTML/MD 报告、主题 | 受限 TemplateProvider/主题配置 | 受支持字段与样式可配置；任意代码不可配置执行 |
| 新 Admin 页面、可交互控件 | 构建期 UI 扩展 | 需要前端代码与重建；后端 API/权限变化独立评审 |

结论：当前是合理的可插拔架构设计，不是现成插件平台。A07 完成后才能用实际接入测试证明“不改核心即可扩展”。

## 6. Codex 的最短开工路线与人工输入

1. 同步包含本次审计的设计，保护开发机独有改动；为首个运行时 Feature 建新分支，不在当前设计分支写业务实现。
2. 通过已安装 Spec Kit skills 生成并审查该 Feature 规格，把 A01/A02/A09 和 A03 的事件边界纳入 Plan/Checklist。明确编码授权后再实施，不拿本报告替代 Spec/Analyze。
3. 优先验证版本与崩溃恢复，再完成最小问答控制、20 个合成场景、基础认证、Chat/Admin 壳及构建。测试 PG/checkpointer/broker 用真实进程，外部 Provider 可用 Fake。
4. 下一 Feature 交付真实 KB/模型答案基线及 A03；随后自主取证关闭 A05/A07，渠道/附件关闭 A04/A06，最后联合发布关闭 A08。编号由 Spec Kit 现场分配，沿用[交付计划](../plans/V1-DELIVERY-PLAN.md)的先后逻辑。

**不需要用户再手工补一整套技术方案。** Codex 可以完成表结构、接口、包版本验证、锁文件、开发环境和测试设计。需要人工提供/确认的只在相应阶段：

- 真实集成：可访问端点/版本、授权 dataset/数据范围、钉钉受众映射、模型与只读工具凭证引用；秘密不进仓库或聊天。
- 质量验收：产品工程师确认题目、必需事实、来源、可接受建议和应求助标签；AI 可辅助整理，不能自己证明自己答案正确。
- 生产发布：身份/数据/备份目标及告警负责人等 A08 组织决策；没有这些不发生产，但可先做独立开发测试。

## 7. 审阅范围与验证限制

35 份逐读文稿：根目录 README、AGENTS、项目基线；Constitution；specs/README；docs 下 BOOTSTRAP、8 份 ADR 与 ADR 索引、10 份 architecture 文稿、design 总设计、4 份 governance 文稿、2 份 plans、requirements 基线和2份既有 research。另检查 Spec Kit 初始化/扩展配置、目录树及远端分支/PR状态；未修改官方工具脚本。

独立只读复核交叉检查了 Web/群聊输出、附件、插件、模板、恢复与分发，确认 A03/A04 为需闭合的设计语义，其他主要是 Feature 落实与部署选择。未运行真实模型/知识库、业务测试、破坏性故障试验或客户设备命令；因此不提供虚构的正确率、吞吐或安全通过率。

本次交付验证限于 Markdown/本地链接/示例 YAML、变更范围与 Git 远端一致性；具体完成结果随提交交付说明记录。所有行号引用均指本报告第 1 节的被审计提交，不随以后编辑自动更新。
