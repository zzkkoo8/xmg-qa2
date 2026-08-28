# ADR-0002: Knowledge Engineering Decoupled from xmg-qa2

Status: Accepted

## Context

历史系统把文档处理、知识库产品和问答 Runtime 混杂，会导致：

- 更换 RAG 平台影响问答服务。
- 清洗流程故障影响在线服务。
- 数据版本不可追踪。
- Provider 私有字段进入业务逻辑。

## Decision

将 Knowledge Factory 作为独立项目。

xmg-qa2 只消费 Knowledge Contract。

## Consequences

必须：

- 定义 Evidence。
- 定义 Knowledge Version。
- 为每个知识库实现 Adapter。
- 建立 Contract Tests。

但在线 QA 与离线知识生产实现彻底解耦。
