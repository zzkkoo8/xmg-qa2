# xmg-qa2 Architecture Baseline

Status: **Gate 0 Approved / Pre-Implementation**

## 1. 架构目标

xmg-qa2 是企业问答 Harness。它必须把“控制流程”和“能力 Provider”分开。

系统核心只负责：

- Runtime
- Workflow
- Plugin Registry
- Context
- Session
- Events
- Policy
- Observability

外部能力通过插件接入：

- Channels
- Knowledge
- Models
- Tools
- Policies

## 2. 逻辑架构

```text
DingTalk / REST / Web / Future Channel
                  |
             Channel Adapter
                  |
                  v
           Harness Gateway
                  |
       Session + Auth + Policy
                  |
                  v
          Workflow Router
                  |
                  v
          LangGraph Runtime
                  |
       +----------+----------+
       |          |          |
       v          v          v
   Knowledge     Model      Tool
   Registry      Registry   Registry
       |          |          |
   Providers   Providers   Providers
```

跨层能力：

```text
Config / Trace / Metrics / Audit / Retry / Timeout / Circuit Breaker
```

## 3. Harness Core

Harness Core 应保持薄。

### Runtime

负责：

- 启动 Workflow。
- 传递 Context。
- 持久化/恢复 Workflow State。
- 统一超时与取消。
- 输出 Runtime Event。

### Plugin Registry

负责：

- 注册。
- 能力发现。
- 生命周期。
- 健康状态。
- Provider 选择。

Registry 不包含业务问答规则。

### Context

Workflow 通过 Context 获取：

- Knowledge client
- Model client
- Tool client
- Policy
- Trace
- Session

Context 暴露契约，不暴露 Provider 实现。

### Event Bus

统一表达：

- TurnStarted
- NodeStarted
- RetrievalRequested
- RetrievalCompleted
- ModelRequested
- ModelCompleted
- ToolRequested
- ToolCompleted
- VerificationCompleted
- TurnCompleted
- TurnFailed

## 4. Workflow First

V1 Product QA 参考状态图：

```text
Input
  |
Normalize
  |
Policy Check
  |
Intent Route
  |
Retrieval Strategy
  |
Knowledge Retrieve
  |
Evidence Gate -------- insufficient ------> Fallback
  |
Answer Generate
  |
Grounding / Citation Verify
  |
Output Policy
  |
Response
```

关键控制点必须显式：

- 最大重试次数。
- 每个 Provider timeout。
- Evidence 最低门槛。
- 无证据策略。
- 降级策略。
- 最终失败策略。

## 5. LangGraph 边界

LangGraph 是 Runtime Engine，不是领域模型。

因此：

- Domain 不依赖 LangGraph。
- Knowledge Contract 不依赖 LangGraph。
- Channel Contract 不依赖 LangGraph。
- Workflow 实现层可以使用 LangGraph。
- Harness 可以将 LangGraph State 转换为自己的稳定状态模型。

这样未来替换执行引擎时，不破坏领域与 Provider 契约。

## 6. 模块依赖

目标依赖方向：

```text
domain
  ^
harness/contracts
  ^
workflows + runtime
  ^
plugins + infrastructure
  ^
api + channels
```

禁止：

```text
domain -> langgraph
domain -> fastapi
workflow -> dify SDK
workflow -> dingtalk SDK
harness/contracts -> provider implementation
knowledge plugin -> workflow business rule
```

## 7. Provider Failure

每个 Provider 必须统一映射错误类型：

- ConfigurationError
- AuthenticationError
- TimeoutError
- RateLimitError
- ProviderUnavailable
- InvalidResponse
- ContractViolation

Workflow 只能依据稳定错误类型制定策略，不分析某厂商原始异常字符串。

## 8. V1 成功标准

### 架构

- 替换 Knowledge Provider 不修改 Workflow 业务代码。
- 替换 LLM Provider 不修改 Workflow 业务代码。
- 增加 Channel 不修改核心问答 Workflow。
- 每个插件可独立 contract test。

### 流程

- 每次问答能够输出完整状态节点轨迹。
- 每个重试有上限。
- 无无限 Agent Loop。
- Workflow 可恢复或至少可明确重放。

### 知识问答

- 回答能够关联 Evidence。
- Evidence 不足时明确 fallback。
- Provider 返回异常不被伪装成“无知识”。

### 工程

- SpecKit 全流程通过。
- 关键依赖规则由 CI 验证。
- 单元、契约、集成、E2E 测试分层存在。

## 9. 非目标

V1 不追求：

- 自主规划型通用 Agent。
- 多 Agent 协作平台。
- 通用低代码工作流 UI。
- 知识清洗平台。
- Prompt 管理 SaaS。
- 自研向量数据库。
