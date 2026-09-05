# 架构决策记录

| ADR | 决定 | 状态 |
| --- | --- | --- |
| [0001](ADR-0001-XMG-HARNESS-LANGGRAPH.md) | XMG 薄业务控制层 + LangGraph | 原方向保留；本轮复核 |
| [0002](ADR-0002-KNOWLEDGE-DECOUPLING.md) | 知识工程与 QA 解耦 | 保留；Dify 适配边界见契约 |
| [0003](ADR-0003-WORKFLOW-FIRST.md) | 显式工作流、语义节点使用 Agent | 保留；配置细节由 0005 补充 |
| [0004](ADR-0004-DURABLE-SUPPORT-TASK.md) | 持久 SupportTask / Worker / 恢复 | 本轮设计基线，待实现 |
| [0005](ADR-0005-READONLY-EVIDENCE-WORKFLOW.md) | 只读、动态证据、配置能力 | 本轮设计基线，待实现 |
| [0006](ADR-0006-OSS-STACK-AND-REAL-MVP.md) | 主流组件、真实 V1、按需扩展 | 本轮设计基线，待实现 |
| [0007](ADR-0007-WEB-DELIVERY-PERSONALIZATION.md) | Chat/Admin、分发、模板与展示扩展 | 增补设计基线，待实现 |

决策变化保留历史原因并用新 ADR 明确补充/替代关系，不删除历史以伪造从未发生过变化。产品范围始终指向 [Requirements Baseline](../requirements/REQUIREMENTS-BASELINE.md)。
