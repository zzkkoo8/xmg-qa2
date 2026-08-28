# Dependency Rules

## 1. 目的

架构规则必须尽可能由自动化检查，而不是只存在于文档中。

## 2. 允许依赖

```text
domain
harness/contracts -> domain
runtime -> harness/contracts, domain
workflows -> runtime/contracts, harness/contracts, domain
plugins -> harness/contracts, domain, infrastructure primitives
api -> runtime, harness/contracts
observability -> contracts/events
```

## 3. 禁止依赖

```text
domain -> fastapi
domain -> langgraph
domain -> provider SDK

harness/contracts -> dify
harness/contracts -> ragflow
harness/contracts -> openai
harness/contracts -> dingtalk

workflows -> concrete provider SDK
workflows -> channel SDK
```

## 4. CI 要求

正式实现阶段应引入自动依赖检查。

工具在 Plan 阶段确定，但必须能够检测：

- forbidden imports。
- layer cycles。
- Provider 泄漏到 Core。
- tests 之外的逆向依赖。

## 5. 架构变更

需要违反现有依赖方向时：

1. 停止编码。
2. 写 ADR。
3. 更新 Architecture Baseline。
4. 执行 SpecKit analyze。
5. 人工批准后再修改。
