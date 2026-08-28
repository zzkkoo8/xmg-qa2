# Thread / Turn / Event Model

## 1. 目的

参考成熟 Harness 将客户端和核心 Runtime 解耦的思路，xmg-qa2 使用稳定会话模型承接 DingTalk、Web、API 等不同入口。

## 2. Thread

Thread 表示一个长期对话上下文。

概念字段：

```text
thread_id
channel
external_conversation_id
principal
created_at
updated_at
metadata
```

## 3. Turn

一次用户输入触发一个 Turn。

```text
turn_id
thread_id
input
status
workflow_id
workflow_version
started_at
completed_at
result
```

Turn 状态建议：

```text
queued
running
waiting
completed
failed
cancelled
```

## 4. Item / Event

运行过程以 Event 形式记录。

典型 Event：

```text
UserMessageReceived
WorkflowSelected
NodeStarted
NodeCompleted
RetrievalRequested
EvidenceReceived
ModelRequested
ModelCompleted
VerificationCompleted
AssistantMessageProduced
TurnFailed
```

## 5. Client Separation

DingTalk Adapter 负责：

```text
DingTalk payload <-> XMG canonical message
```

它不负责：

- Query rewrite。
- 知识库检索。
- Prompt。
- Answer verification。

## 6. Correlation

所有事件至少能通过以下字段关联：

```text
trace_id
thread_id
turn_id
event_id
timestamp
```

Provider 调用增加：

```text
provider_id
operation_id
```

## 7. Idempotency

上游 Channel 可能重复投递。

Ingress 必须支持幂等标识，避免一个 DingTalk 消息触发两个 Turn。

具体 idempotency key 的生成规则在 Feature Spec 中冻结。
