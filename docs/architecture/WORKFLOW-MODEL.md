# Workflow State Model

## 1. 原则

Workflow 是 xmg-qa2 的控制平面。

它明确规定：

- 节点
- 状态
- 转移
- timeout
- retry
- permission
- fallback
- cancellation
- budget
- termination condition

Agent 只能在 Workflow 允许的语义节点内做推理和下一步调查建议，不能拥有无限自由执行权。

## 2. Core Support Workflow

推荐基线：

```text
receive_input
normalize_input
policy_check
understand_problem
initial_retrieve
evaluate_evidence
plan_next_action
execute_action
collect_evidence
update_hypothesis
decide_continue
generate_answer
generate_report
verify_grounding
apply_output_policy
finalize_response
```

异常/降级分支：

```text
provider_fallback
insufficient_evidence
permission_required
ask_user
budget_exhausted
policy_reject
workflow_cancelled
workflow_failure
```

## 3. Controlled Agentic Investigation

当初始 Evidence 不足时进入 Investigation Loop：

```text
evaluate_evidence
      |
      +-- sufficient --> generate_answer/report
      |
      +-- insufficient
              |
       plan_next_action
              |
       execute_action
              |
       collect_evidence
              |
       update_hypothesis
              |
        decide_continue
           /       \
         yes       no
          |         |
          +----> answer / fallback / ask_user
```

每轮必须检查：

```text
step_count < max_steps
elapsed_time < max_duration
cost/token < budget
action in tool_allowlist
permission satisfied
termination_condition == false
```

任一硬限制触发后，不得继续自动循环。

## 4. State

Workflow State 概念字段：

```text
trace_id
thread_id
turn_id
investigation_id
workflow_id
workflow_version
input
normalized_input
intent/problem_type
retrieval_request
evidence[]
hypotheses[]
investigation_steps[]
next_action
budget_state
permission_state
retry_state
draft_answer
technical_report
verification
final_answer
status
error
timestamps
```

## 5. Determinism

优先由代码/规则执行：

- timeout
- retry count
- provider health
- schema validation
- citation/evidence id validation
- ACL / permission
- route/tool allowlist
- step count
- duration budget
- token/cost budget
- cancellation
- termination

可使用 LLM 的节点：

- 问题理解与分类
- Query rewrite
- Evidence 语义评估
- Hypothesis 生成/更新
- 下一调查动作建议
- 回答生成
- Technical Report 生成
- 复杂 grounding 判断

即使使用 LLM，也必须有：

- 明确输入 schema
- 明确输出 schema
- validation
- timeout
- fallback

## 6. Investigation Action

允许的下一步 Action 必须来自 Capability Registry，例如：

```text
search_knowledge
retrieve_document
rewrite_query
call_product_api
call_mcp_tool
run_readonly_diagnostic
ask_user
finish_with_answer
finish_with_report
finish_insufficient_evidence
```

V1 不允许 Agent 生成任意 shell/HTTP 动作后直接执行；必须先映射到已注册 capability。

## 7. Retry

Retry 必须：

- 有上限。
- 有可观测事件。
- 区分 transient 与 permanent error。
- 尊重整体 Investigation budget。
- 不重复执行已经成功且存在副作用的 Tool。

## 8. Fallback

Fallback 必须是显式状态。

例如：

```text
Primary Knowledge Provider failed
 -> Secondary Provider
 -> still failed
 -> degraded response / ask user / explicit error
```

禁止 silently swallow。

必须严格区分：

```text
NoResult
ProviderUnavailable
Timeout
PermissionDenied
InvalidResponse
```

## 9. Evidence Conflict

多个 Evidence 冲突时不得直接选择模型“更相信”的结果。

Workflow 应进入显式验证路径，例如：

```text
conflicting evidence
 -> identify conflict
 -> prefer authoritative/current source by policy
 -> request additional evidence if needed
 -> unresolved conflict => answer with uncertainty
```

## 10. Human-in-the-loop

知识检索和只读诊断默认可以自动执行，但仍受 Policy 控制。

具有副作用的 Tool 根据风险级别处理：

```text
READ_ONLY        -> policy 允许时自动
CONTROLLED_WRITE -> 按 Policy 决定是否审批
HIGH_RISK        -> 默认人工审批
```

## 11. Output Decision

推荐：

```text
simple + sufficient evidence
 -> direct answer

complex investigation / multiple steps / root cause analysis
 -> technical report

insufficient evidence
 -> explicit uncertainty + collected evidence + next recommendation
```

## 12. Workflow Versioning

每次生产执行记录：

```text
workflow_id
workflow_version
```

改变节点语义、关键 threshold、permission、budget 或 route 行为时，应形成新版本并可审计。
