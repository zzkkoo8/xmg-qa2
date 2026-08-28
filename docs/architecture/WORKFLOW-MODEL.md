# Workflow State Model

## 1. 原则

Workflow 是 xmg-qa2 的控制平面。

它明确规定：

- 节点。
- 状态。
- 转移。
- 超时。
- 重试。
- fallback。
- 终止条件。

## 2. V1 Product QA Nodes

推荐基线：

```text
normalize_input
policy_check
route_intent
build_retrieval_request
retrieve_knowledge
evaluate_evidence
generate_answer
verify_grounding
apply_output_policy
finalize_response
```

异常分支：

```text
provider_fallback
insufficient_evidence
policy_reject
workflow_failure
```

## 3. State

Workflow State 概念字段：

```text
trace_id
thread_id
turn_id
workflow_id
workflow_version
input
normalized_input
intent
retrieval_request
evidence[]
draft_answer
verification
final_answer
status
error
retry_state
timestamps
```

## 4. Determinism

优先用代码/规则的场景：

- timeout。
- retry count。
- provider health。
- schema validation。
- citation id validation。
- evidence 数量。
- ACL。
- route allowlist。

可使用 LLM 的场景：

- 意图语义分类。
- Query rewrite。
- Evidence 语义评估。
- 回答生成。
- 复杂 grounding 判断。

即使使用 LLM，也必须有输入输出 schema 和失败策略。

## 5. Retry

Retry 必须：

- 有上限。
- 有可观测事件。
- 区分 transient 与 permanent error。
- 不重复执行已经确定成功且具有副作用的 Tool。

## 6. Fallback

Fallback 必须是显式状态。

例如：

```text
Primary Knowledge Provider failed
 -> Secondary Provider
 -> still failed
 -> degraded response / error
```

禁止 silently swallow。

## 7. Human-in-the-loop

V1 核心知识问答默认不要求人工审批。

以后若 Tool 具有高风险副作用，可在对应节点加入 interrupt / approval，而不是让整个系统都变成人工流程。

## 8. Workflow Versioning

每次生产执行记录：

```text
workflow_id
workflow_version
```

改变节点语义、关键 threshold 或 route 行为，应形成新版本。
