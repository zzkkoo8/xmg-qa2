# SupportTask / Session / Event 模型

版本：1.0；日期：2026-09-05。替代旧 Thread → Turn → Investigation 单轮生命周期。

## 1. 对象与所有权

| 对象 | 关键字段 | 责任 |
| --- | --- | --- |
| SupportTask | task_id、tenant_id、customer_id、project_id、owner、status、state_version、environment、goal、created_at、updated_at | 一个问题的持久业务生命周期；全部访问验证 principal |
| Thread | thread_id、channel、external_conversation_id、principal 映射 | 沟通上下文；一个群可有多案，不能以群 ID 充当 case ID |
| Turn | turn_id、task_id、thread_id、source_event_id、input_ref、received_at | 一次输入；多个 Turn 可推进同一调查 |
| Investigation | investigation_id、task_id、hypotheses、evidence_refs、steps、decisions | 跨 Turn 调查工作区；记录支持/反驳/未决事实 |
| Run | run_id、task_id、workflow_version、config_hash、policy_version、model_profile、status、budget、lease_epoch | 一次有界执行段；暂停后释放 Worker，下次新 Run 恢复同一调查 |
| HumanRequest | request_id、task_id、kind、required_items、recipient_ref、pause_reason、resume_condition、status、interrupt_ref | 等待用户/工程师补证据；部分回传仍等待，不等同写操作审批 |
| ResumeAttempt | resume_event_id、request_id、runtime_key、source_checkpoint_id、interrupt_ref、payload_ref/hash、status、applied_checkpoint_id | 持久人工恢复意图与图消费回执；接收成功不等于图已恢复 |
| Evidence | evidence_id、scope、source、content_ref、hash、time、version、claim_links | 完整定义见 Knowledge Contract；不可被摘要覆盖 |
| StepCommit | operation_id、run_id、step_id、status、result_ref、evidence_ids、epoch | 业务结果幂等，衔接 checkpoint |
| Event | event_id、task_id、sequence、type、actor、payload_ref、occurred_at、trace_id | 追加业务事件；不保存模型隐藏思维链，仅存决策摘要和证据 |
| Artifact | artifact_id、task_id、hash、mime、size、storage_ref、retention | 日志、附件、报告；权限继承 case，下载时重新鉴权 |

LangGraph thread_id 是服务端生成的 runtime_key（task_id + investigation_id），不是外部钉钉 thread_id。checkpoint_id/checkpoint_ns 仅在 runtime 映射表中，不能充当访问凭证。

## 2. 生命周期

~~~mermaid
stateDiagram-v2
    [*] --> NEW
    NEW --> ANALYZING
    ANALYZING --> INVESTIGATING
    INVESTIGATING --> WAITING_FOR_USER
    INVESTIGATING --> WAITING_FOR_HUMAN
    INVESTIGATING --> WAITING_FOR_EXTERNAL
    INVESTIGATING --> PAUSED
    WAITING_FOR_USER --> INVESTIGATING: 补充满足条件
    WAITING_FOR_HUMAN --> INVESTIGATING: 工程师回传
    WAITING_FOR_EXTERNAL --> INVESTIGATING: 到期重试
    PAUSED --> INVESTIGATING: 合法恢复
    INVESTIGATING --> RESOLVED
    RESOLVED --> CLOSED: 用户确认
    RESOLVED --> INVESTIGATING: 追问重开
    CLOSED --> INVESTIGATING: 明确重开并记录事件
    INVESTIGATING --> FAILED: 不可恢复内部错误
    FAILED --> PAUSED: 人工修复后
    INVESTIGATING --> CANCELLED
    CANCELLED --> [*]
~~~

图展示主要路径；NEW、ANALYZING 和所有等待/暂停状态也允许合法取消。FAILED 必须包含可见原因与接手方式，不吞错。取消不能撤销已经完成的外部只读请求，但阻止后续调用和旧 Worker 提交有效结果。

运行状态与 Case 状态分开：一个 Run 可成功结束于 WAITING_FOR_HUMAN，SupportTask 仍未解决。等待超时最多触发提醒/接手，不自动标记 RESOLVED/CLOSED。已关闭的任务重开时重新核验权限和版本，不自动复活旧凭证。

QuestionFrame/AnswerPlan/NextAction 等[问答投影](QA-CORE.md)属于 Task/Investigation/StepCommit；不另设一套持久任务。结果 answer_kind（complete/partial/needs_input/unable_to_conclude）与 Case 状态分开：只有完整回答当前目标并通过检查才 RESOLVED，关键待办或故障待验证保持调查/等待/暂停。通用直答可在同一短 Run 经过 ANALYZING/INVESTIGATING 完成，不强制调用检索/工具。

## 3. 幂等与并发

| 环节 | 唯一约束或校验 |
| --- | --- |
| 入站 | UNIQUE(channel_instance, external_event_id)；REST 使用 principal + Idempotency-Key，并校验请求体 hash，重复但 body 不同返回冲突 |
| Case 绑定 | 显式 task_id/回复 request_id 优先；模糊新问题不得只按最后活跃群会话猜案 |
| 执行 | 同 task_id 一个 active Run；租约 state_version + 递增 epoch，所有业务写入包含匹配条件 |
| Step | UNIQUE(task_id, operation_id)；operation_id 在动作计划落库时分配，不能重试时随机重建 |
| 人工恢复 | UNIQUE(request_id, resume_event_id)；校验身份、case、仍等待的 request、expected_state_version |
| 图消费恢复 | ResumeAttempt 绑定原 checkpoint/interrupt；同一有效 interrupt 最多一个待应用恢复意图，不能把旧回复重新绑定到下一 interrupt |
| 出站 | UNIQUE(task_id, output_kind, result_version, destination)；记录 delivery state 与 provider receipt |

租约默认心跳 10 秒、失效 60 秒；Dispatcher 巡检间隔 15 秒；这些是待测配置。Worker 持有数据库 advisory lock 作为执行互斥，epoch 作为业务写入 fencing。租约失效不能直接让第二个 Worker 与仍存活的旧 Worker 并发写同一图：先确认互斥锁释放、旧 Run 失效，再取得新 epoch。失去数据库连接/租约的 Worker 必须在下一节点/调用前停止；若无法确认释放，PAUSED 并求助。

checkpoint adapter 必须同样处于任务执行锁保护内；旧 epoch 的检查点写入不得成为新的恢复头。否则只有业务表 fencing 仍可能出现图状态被旧 Worker 覆盖，此项是实现前必过的集成验收。

消息队列和网络发送无法承诺恰好一次。出站平台没有幂等接口且“已发出、回执丢失”时标记 DELIVERY_UNKNOWN，查询回执/有限人工处理，不无限重发轰炸用户。

## 4. 恢复与崩溃窗口

| 故障位置 | 恢复规则 |
| --- | --- |
| Inbox 事务未提交 | 不 ACK；上游重投 |
| Outbox 已提交、未发布 | Dispatcher 重发 |
| 发布已确认、Outbox 未标记 | 可重复 job，消费去重 |
| 外部取证完成、StepCommit 未提交 | 查询可重试；保留新 observation 时间，记录可能重复调用 |
| StepCommit 已提交、checkpoint 未写 | 查 operation_id 复用业务结果，不重复生成通知/报告 |
| checkpoint 已写、Case 状态未更新 | 对账图状态与 StepCommit，补业务投影 |
| 进入 interrupt 后 Worker 崩溃 | 同 runtime_key 恢复；等待记录和通知依据唯一 request_id 补齐 |
| ResumeAttempt 已接收、图尚未应用 | 持久恢复 Outbox 可重投；执行锁内重新验证原 interrupt，仅定向恢复该 ID |
| 图已消费回复、ResumeAttempt 未标记 APPLIED | 从 checkpoint 消费标记/持久恢复记录对账；已消费则补业务回执，不把同一 payload 再发给当前新 interrupt |
| 收到重复/旧人工回复 | 重复返回已有结果；旧回复保存为补充但不驱动失效中断 |
| 新部署不能加载旧图版本 | PAUSED(VERSION_INCOMPATIBLE)；用旧镜像完成或经测试迁移，不直接按新图起跑 |
| 后端或权限失效 | 显式等待/暂停；重新授权与健康检查后恢复，不静默更换数据范围 |

LangGraph 从发生 interrupt 的节点开头恢复，节点前置代码可能再执行；因此 HumanRequest 创建和通知在独立、幂等的步骤完成，不在 interrupt 前执行未经去重的发送操作。按 Architecture 的事务顺序，只有确认中断 checkpoint 已持久化，才允许通知 Outbox 发布。[官方中断语义](https://docs.langchain.com/oss/python/langgraph/interrupts)

人工恢复使用以下固定协议：

1. 完成身份、Case、request/version 和补充条件校验后，同一业务事务保存 ResumeAttempt（RECEIVED）与恢复 Outbox；绑定服务端确认的 runtime_key、原 checkpoint、interrupt_ref、resume_event_id 和 payload hash。重复事件先返回已有接收结果，不因它已改变 state_version 而误报冲突；body 不同仍拒绝。
2. Worker 取得该 Case 执行锁与有效 epoch 后，对账 ResumeAttempt 和图状态。只有确认原 interrupt 仍待恢复且该意图尚未消费，才使用 `Command(resume={interrupt_id: envelope})` 定向提交；envelope 包含 resume_event_id 与受控资料引用。禁止用裸值恢复当前任意 interrupt。
3. 中断节点验证 request/event 归属，以同一恢复操作标识幂等处理结果；消费标记随节点后续状态进入持久 checkpoint。确认对应 checkpoint 后，才将 ResumeAttempt 标记 APPLIED 并保存 applied_checkpoint_id。RECEIVED 只能报告“已接收”，不能报告“已恢复”。
4. 崩溃重试先核对 checkpoint、持久恢复写入及消费标记：已应用则补业务回执；明确尚未应用且原 interrupt 仍有效才重试同一意图；图已推进到另一 interrupt 时不得重发旧回复。若无法确认消费状态，进入 PAUSED(RESUME_STATE_UNCERTAIN) 并保留资料求助，不盲目重放。

checkpoint/恢复写入的读取方式取决于固定的 LangGraph/checkpointer 版本，必须在首个 Feature 通过“图刚消费完即强杀、随后到达第二个 interrupt、重复投递旧回复”的实际集成测试。本协议是待实现设计，不声称 SDK 自动提供业务恢复幂等。

## 5. 时间、预算与版本

Case 可持续多天；Run 只计算活跃耗时。等待不占 Worker、DB 事务或模型上下文连接。默认护栏见需求基线；每次恢复分配新段预算，同时累计 case 总调用/费用供 Policy 判断，不能靠不停恢复绕过上限。自动因运行分段而续跑必须继续扣同一预算；人为增加预算须有审计事件。

保留 workflow/config/policy/contract/model/skill 版本和知识 observation。内容过期可以补新证据，但不可改写旧证据。恢复先做 ACL、凭证可用性、能力注册状态和版本检查，再重新评估证据时效。

## 6. 最小 API 语义

| 操作 | 行为 |
| --- | --- |
| POST /v1/tasks | 持久化后 202，返回 task_id、turn_id、status、status_url |
| GET /v1/tasks/{id} | 当前状态、摘要、待办、版本；重新验证 case ACL |
| POST /v1/tasks/{id}/messages | 追加补充，携带 request_id/expected_state_version/Idempotency-Key |
| POST /v1/tasks/{id}/resume | 仅对匹配的等待条件或合法手动暂停有效；不能批准生产写 |
| POST /v1/tasks/{id}/cancel | 幂等取消，变更版本，停止后续调度 |
| POST /v1/tasks/{id}/close | 记录用户确认；不删除历史 |
| GET /v1/tasks/{id}/events | 带 cursor 的事件流/SSE；断线重连不重建任务 |
| GET /v1/tasks/{id}/reports/{version} | 按权限下载已发布报告 |

这些为设计接口；OpenAPI 和具体返回 Schema 在 Feature Spec 中冻结。钉钉回调 ACK 不等于业务已回答；跨天通知不能依赖可能已失效的临时 sessionWebhook，需适配器的持久收件标识与已授权发送 API。
