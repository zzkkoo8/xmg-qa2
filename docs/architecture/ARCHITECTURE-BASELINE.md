# xmg-qa2 Architecture Baseline

Status: **Gate 0 Approved / Pre-Implementation**

## 1. 架构目标

xmg-qa2 是企业技术支持问题回答专家 Agent 的可控 Harness / Runtime。

它必须把“控制流程”和“能力 Provider”分开，并支持在受控边界内进行多步自动调查。

系统核心只负责：

- Runtime
- Workflow
- Capability / Plugin Registry
- Context
- Session / Investigation State
- Events
- Policy
- Observability

外部能力通过稳定 Contract / Plugin 接入：

- Channels
- Knowledge
- Models
- Tools / Product APIs / MCP
- Policies

完整的人类可读设计稿见：

- [`../design/XMG-QA2-SUPPORT-AGENT-DESIGN.md`](../design/XMG-QA2-SUPPORT-AGENT-DESIGN.md)

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
           Support Workflow
                  |
       +----------+-----------+
       |                      |
       v                      v
Initial Knowledge       Controlled Agentic
   Retrieval              Investigation
       |                      |
       |             +--------+--------+
       |             |        |        |
       v             v        v        v
   Knowledge       API      MCP      Tool
   Registry       Tools    Tools     Tools
       |             |        |        |
       +-------------+--------+--------+
                     |
                     v
              Evidence Workspace
                     |
            Hypothesis / Verify
                     |
                     v
          Answer / Technical Report
```

跨层能力：

```text
Config / Secrets / Trace / Metrics / Audit
Retry / Timeout / Circuit Breaker / Rate Limit
```

## 3. Harness Core

Harness Core 应保持薄。

### Runtime

负责：

- 启动和恢复 Workflow。
- 传递 Context。
- 持久化/恢复 Workflow State。
- 统一 timeout、retry、cancel 和 termination。
- 输出 Runtime Event。

### Capability / Plugin Registry

负责：

- 注册。
- capability 发现。
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
- Session / Investigation

Context 只暴露稳定契约，不暴露 Provider 实现。

### Event Bus

至少统一表达：

- TurnStarted
- InvestigationStarted
- NodeStarted
- RetrievalRequested
- RetrievalCompleted
- ToolRequested
- ToolCompleted
- EvidenceCollected
- HypothesisUpdated
- VerificationCompleted
- TurnCompleted
- TurnFailed

## 4. Workflow First + Controlled Agentic Investigation

外层核心流程必须是显式 Workflow / State Graph。

```text
Input
  |
Normalize
  |
Policy Check
  |
Understand Problem
  |
Initial Retrieve
  |
Evidence Gate ---- sufficient ----> Answer / Report
  |
insufficient
  |
Plan Next Action
  |
Execute Authorized Capability
  |
Collect Evidence
  |
Verify / Update Hypothesis
  |
Continue? ---- yes ----> Plan Next Action
  |
  no
  |
Answer / Fallback / Ask User
```

Agent 可以在 `Plan Next Action` 等语义节点中参与决策，但整个 Investigation 必须受以下硬边界约束：

- `max_steps`
- `max_duration`
- `tool_allowlist`
- permission / approval policy
- Provider timeout
- retry limit
- token / cost budget
- explicit termination condition

禁止无限自由 Agent Loop。

## 5. Evidence First

Knowledge、API、MCP 和 Tool 的结果统一形成 Evidence。

任何重要结论必须能够追溯到 Evidence；Evidence 不足时必须明确降级或说明不确定性。

`ProviderUnavailable`、`Timeout`、`PermissionDenied` 等错误绝不能伪装成 `NoResult`。

## 6. xmg-kb 边界

xmg-kb 是独立知识工程项目和 Knowledge Provider。

xmg-qa2 不负责：

- 原始 PDF/PPT/Word 解析
- OCR
- 文档清洗
- 去重
- 分类
- 切片
- Embedding 批处理
- 知识库构建

xmg-qa2 只消费统一 Knowledge Contract，并记录实际使用的 knowledge version。

## 7. LangGraph 边界

LangGraph 是 Runtime Engine，不是领域模型。

因此：

- Domain 不依赖 LangGraph。
- Knowledge / Tool / Channel Contract 不依赖 LangGraph。
- Workflow 实现层可以使用 LangGraph。
- Harness 负责把 LangGraph State 映射到自身稳定状态模型。

这样未来替换 Runtime Engine 时，不破坏 Domain 和 Provider Contracts。

## 8. 模块依赖

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
workflow -> concrete product API SDK
harness/contracts -> provider implementation
knowledge/tool plugin -> workflow business rule
```

## 9. Provider Failure

所有 Provider 必须统一映射稳定错误类型：

- NoResult
- ConfigurationError
- AuthenticationError
- PermissionDenied
- TimeoutError
- RateLimitError
- ProviderUnavailable
- InvalidResponse
- ContractViolation
- ToolExecutionFailed

Workflow 只能依据稳定错误类型制定策略，不解析某厂商原始异常字符串。

## 10. V1 成功标准

### 架构

- 替换 Knowledge Provider 不修改核心 Workflow。
- 替换 LLM Provider 不修改核心 Workflow。
- 增加 Tool/API Provider 不修改 Harness Core。
- 增加 Channel 不修改核心技术支持 Workflow。
- 每个插件可独立 Contract Test。

### 流程

- 简单问题能够快速结束。
- Evidence 不足时能够进入受控 Investigation。
- 每个调查步骤、重试和 Tool Call 都有上限和 Trace。
- Agent 达到预算/步骤/时间限制后一定能够终止。
- Workflow 可恢复或至少可明确重放。

### 问题回答

- 最终结论能够关联 Evidence。
- 可以区分无结果、Provider 故障和权限失败。
- 多 Evidence 冲突和 Evidence 不足都有明确策略。
- 复杂问题能够输出 Technical Report。

### 工程

- SpecKit 全流程通过。
- 关键依赖规则由 CI 验证。
- Unit、Contract、Workflow、Integration、E2E 测试分层存在。

## 11. V1 非目标

V1 不追求：

- 真实 xmg-kb 生产接入。
- DingTalk 生产接入。
- 真实高风险自动执行 Tool。
- 通用自主规划型 Agent。
- Multi-Agent Supervisor 平台。
- 通用低代码工作流 UI。
- 知识清洗平台。
- Prompt 管理 SaaS。
- 自研向量数据库。
