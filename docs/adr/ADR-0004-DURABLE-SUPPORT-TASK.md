# ADR-0004：持久 SupportTask 与中央 Worker

日期：2026-09-05；状态：纳入本轮授权设计基线，待实现。

## 背景

Q4B/Q9B 要求跨天恢复、中央服务 + Worker。旧 Turn 级 Investigation、可重放表述和未明确队列/存储无法满足该目标。

## 决策

SupportTask 为业务生命周期；Run 为有界执行段；LangGraph 使用 PostgreSQL checkpoint；Celery + RabbitMQ 分发执行段，PostgreSQL 业务表保存 Case/证据/人工请求。使用 Inbox/Outbox、operation_id、状态版本、租约互斥与检查点对账。等待人时退出执行，不用长 ETA 或阻塞 Worker 模拟暂停。

## 替代与后果

Postgres-only 队列可减少依赖，但本项目优先成熟分布式 Worker 生态；Temporal 在已有平台或跨服务持久编排需求显著时重评。当前组合不自动提供业务双写原子性或外部 exactly-once，必须实现并验证崩溃窗口。

依据和完整协议：[选型审计](../research/2026-09-05-STACK-AUDIT.md)、[任务模型](../architecture/SESSION-EVENT-MODEL.md)。V1 Compose 不承诺主机高可用。
