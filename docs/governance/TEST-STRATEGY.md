# Test Strategy

## 1. 测试目标

主要验证“边界和流程”，而不仅是函数覆盖率。

## 2. Unit Tests

验证：

- domain models。
- policy rules。
- error mapping。
- deterministic workflow helpers。
- normalization。

不得依赖真实外部服务。

## 3. Contract Tests

这是插件架构的核心。

同一套 Knowledge Contract Test 应能运行于：

- Fake Provider。
- Dify Adapter。
- RAGFlow Adapter。
- Future Provider。

同一套 Model Contract Test 同理。

## 4. Workflow Tests

使用 fake plugins 对状态图进行确定性测试：

- happy path。
- no evidence。
- provider timeout。
- provider unavailable。
- invalid schema。
- verification failure。
- retry exhausted。

验证实际状态转移，不只验证最终文本。

## 5. Integration Tests

验证真实技术组合，例如：

```text
FastAPI + Harness + LangGraph + Test Provider
```

以及后续：

```text
Harness + Dify
Harness + DingTalk sandbox
```

## 6. E2E

从入口开始：

```text
Channel/API
 -> Thread/Turn
 -> Workflow
 -> Knowledge
 -> Model
 -> Verification
 -> Response
```

同时检查 Trace。

## 7. Failure Injection

必须主动测试：

- timeout。
- 429。
- 5xx。
- malformed response。
- empty evidence。
- duplicate channel delivery。
- model invalid structured output。

## 8. 性能

V1 在 Feature Spec 中冻结：

- p50/p95 latency。
- provider timeout。
- max workflow duration。
- max retries。

未冻结指标前，不在本文编造数字。
