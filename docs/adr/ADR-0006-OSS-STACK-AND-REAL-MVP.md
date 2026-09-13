# ADR-0006：保留主流核心，发布真实 MVP

日期：2026-09-05；状态：纳入本轮授权设计基线，待实现。

## 背景

Q1C 要可真实使用的垂直闭环；旧 V1 只接 Fake。Q8 要成熟开源优先。本轮研究比较 21 个相关仓库的热度及官方能力/维护/许可。

## 决策

保留 LangGraph、FastAPI、Pydantic；复用 Dify 作为知识 Provider；新增持久任务支撑而不重写整个 Agent 平台。官方 MCP、OpenTelemetry 为稳定边界。LiteLLM/Langfuse/Ragas 按需，暂不叠加另一 Agent 框架、向量数据库、Redis、K8s 或第二知识入库管线。

多个 Feature 共同完成 V1：真实 KB/模型、只读能力、真实钉钉、简易 Web、人工暂停恢复与报告。Fake 阶段是内部里程碑，不能作为 V1 发布。

## 替代与重新评估

Pydantic AI + Temporal 为有力替代；Microsoft Agent Framework 对微软生态更有价值；AutoGen 维护模式不作新项目默认；CrewAI 角色协作非当前核心需要。只有业务需求或固定评测出现明显收益，才修改 ADR-0001 技术选择。

许可证、安装渠道和版本兼容都在实施 Plan 冻结；不把热度排序叫全球质量榜。依据：[完整选型审计](../research/2026-09-05-STACK-AUDIT.md)。
