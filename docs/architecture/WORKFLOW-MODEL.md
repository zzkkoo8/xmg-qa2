# 可配置支持工作流

版本：1.0；日期：2026-09-05。需求：FR02/03/05/06/08/09。

## 1. 工作流控制什么

外层状态图约束阶段、允许能力、状态转移、证据门禁和终止；模型在这些边界内理解问题、提出假设和下一动作。通用模型能力贯穿各节点，不是固定排在“外部知识之后”的一个步骤。

默认先检索内部知识。结果充足直接回答；不足时根据所缺事实选择官方检索、产品 API/MCP、已注册诊断，或向用户/工程师索取资料。优先级是同等合规、适用候选中的偏好，不能迫使每个任务跑遍全部工具。

~~~mermaid
flowchart TD
    I["输入 / 关联 Case / 权限检查"] --> K["内部检索"]
    K --> E["证据充分性与冲突判断"]
    E -->|"足够"| A["生成答案 / 报告"]
    A --> V["引用 / 支持关系 / 输出权限检查"]
    V -->|"通过"| R["发布结果"]
    V -->|"不通过且可补证"| P["选择下一获准能力"]
    E -->|"不足或冲突"| P
    P -->|"需要外部取证"| X["Policy 后执行"]
    X --> O["记录证据 / 更新假设"]
    O --> E
    P -->|"缺现场条件"| H["持久人工请求 / 暂停"]
    H -->|"补充满足条件"| E
    P -->|"预算或无进展"| S["保存阶段结论 / 暂停"]
~~~

## 2. 配置示例与语义

下列为设计配置示例，不是已实现运行配置。启动时由 Schema 验证；产品配置只能收紧组织最高权限。

~~~yaml
schema_version: 1
workflow_id: support.default
workflow_version: "1.0.0"
initial_stage: internal_knowledge
capabilities:
  - id: knowledge.internal
    priority: 100
    when: product_or_technical_question
  - id: web.official
    priority: 90
    when: evidence_missing_or_outdated
    egress_profile: public_redacted
  - id: api.product_read
    priority: 80
    when: live_state_needed
  - id: mcp.approved_diagnostics
    priority: 70
    when: hypothesis_needs_observation
  - id: human.assistance
    priority: 10
    when: missing_access_or_evidence_or_progress
permissions:
  target_effects: [READ_ONLY]
  unknown_capability: DENY
  dynamic_remote_shell: DENY
  production_write: DENY
limits:
  max_steps_per_run: 20
  max_active_seconds: 600
  max_total_tokens_per_run: 40000
  max_provider_retries: 2
  no_progress_rounds: 3
on_budget_exhausted: PAUSED
on_unresolved_evidence_conflict: WAITING_FOR_HUMAN
~~~

when 只引用注册的条件谓词，不接受 Python 表达式、shell、动态 import 或模型生成代码。priority 值越大越优先；先过滤 ACL、风险、健康状态、数据外发范围、适用版本和条件，再择优。跳过更高优先级须记录简短理由，如“问题需要现场版本，网页不能提供”。

配置可改变能力优先级/允许条件，不得配置解除 production_write=DENY。新状态转移/新节点语义是代码和 Contract 变更，需要独立 Feature/ADR。配置发布时固定 config_hash；进行中 Case 不自动使用新配置。

Admin 提供表单和 YAML/JSON 编辑、差异、validate、publish、rollback；仍不做拖拽图编辑器。发布验证引用的能力/模板版本、Schema 与组织策略；草稿不能直接生效。当前权限撤销、禁用能力等收紧策略在下一次调用前立即检查，不能因 Case 固定旧配置而绕过。具体控制面见 [Web Console](WEB-CONSOLE.md)。

## 3. 证据门禁

1. 识别待回答命题：产品官方支持、现场状态、通用机制、根因假设、操作建议。
2. 验证 Evidence 的授权范围、产品/版本、时间与真实出处；不合适的证据不能靠高相似度补救。
3. 给关键命题建立 supports / contradicts / insufficient 关系；记录依据。模型自信值、向量相似度、Ragas 分数均不是事实可信度。
4. 官方支持矩阵回答“受支持吗”；现场探测回答“此刻运行如何”。来源不同不必互相覆盖。
5. 重大冲突继续补证，无法消除则列出冲突、阶段性结论和所需资料，暂停或请求人工。禁止用排名最高来源直接抹掉反证。
6. 低风险通用知识可明确标注为通用说明；涉及产品承诺、现场根因或危险变更的确定断言必须有相应证据。模型内置知识不生成虚假 citation。
7. 最终生成后验证引用存在、当前用户可访问、引用确实支持对应主张；不通过最多一次修正，仍失败改为受限阶段答复/人工请求。

## 4. 失败与终止

| 情况 | 处理 |
| --- | --- |
| NoResult | 调整检索或升级可用能力；不是基础设施告警 |
| AuthenticationError / PermissionDenied | 不重复撞库、不换账户绕过；等待授权资料或人工接手 |
| RateLimit / Timeout / ProviderUnavailable | 最多两次重试，退避 + jitter，尊重 Retry-After；超段截止时间则持久外部等待 |
| InvalidResponse / ContractViolation | 隔离 Provider，记录结构化错误；不把原始异常给模型当成功证据 |
| 模型动作 Schema 无效 | 一次结构化修正；仍失败暂停，不解析成任意动作 |
| 相同动作/查询没有新增有效证据三轮 | no_progress；阶段总结 + 人工请求，阻止无意义循环 |
| 预算达到上限 | 保存调查进度并 PAUSED；已确认事实可以输出，但不包装成已解决 |
| 人类未回复 | 保持等待，不占 Worker；默认不无限催促 |
| 取消 | 使当前运行版本失效；后续动作拒绝，记录已经进行中的调用 |
| 未知内部异常 | FAILED + 诊断摘要/trace_id + 持久接手待办，不丢案 |

重试只由指定一层掌控：短暂 Provider 重试在执行器；任务级基础设施恢复在调度层。禁止 SDK、网关、图和 Celery 各自无限重试相乘。每次重试计入调用、时间和费用。

## 5. 人工协助

HumanRequest 至少说明：已知道什么、仍缺什么、已排除什么、建议人类执行的命令/检查、风险、期待回传格式、恢复条件。部分补充不应丢失，也不必反复索要已经提供的信息。

模型生成的修改建议可以由工程师独立评估执行；Runtime 永远不因“批准”“继续”激活生产写工具。若提供只读诊断建议，也不能只凭命令名称判断安全，例如抓包、全盘扫描、无限日志读取可影响业务或泄露数据。

人工请求出站复用系统通知 Contract、持久 Outbox 和已配置收件映射；未配置队列时至少原会话与 Web 待办可见。实际联系第三人需要项目部署的授权映射，不从日志或网页猜收件人。
