# 开发门禁

状态日期：2026-09-05。状态必须以实际产物和授权为准，不把“设计完成”写成“可以编码”。

| Gate | 通过条件 | 当前状态 |
| --- | --- | --- |
| 0 需求/架构方向 | 已知需求、默认项及取舍有来源；用户授权形成设计 | 需求 1.1，含 Chat/Admin、分发与模板；设计可交接 |
| 1 Constitution | 与当前需求一致，无占位符/冲突，授权可追溯 | 本轮增补到 1.1.0；不自动开放编码 |
| 2 Feature Spec | 官方 Spec Kit 生成，场景/FR/NFR/非目标明确，关键歧义解决 | 运行时 Feature 尚未创建 |
| 3 Plan/Checklist/Tasks | 模块/版本/Schema/错误/安全/测试/回退齐全，任务可执行 | 仅有产品交付路线；尚无获批运行时 Feature Plan |
| 4 Analyze | Critical=0、High=0；Medium 有决定；Checklist 无阻塞 | 本轮文档自审不冒充 Spec Kit Analyze；运行时门禁未通过 |
| 5 Coding Authorization | 用户明确批准对应 Feature 实现 | 未授权 |
| 6 Task Verification | 最小相关验证、真实输出、变更范围、关联需求 | 无业务代码，暂不适用 |
| 7 Integration | 真实 KB/模型/钉钉/只读能力 + 持久恢复和失败测试 | 未执行 |
| 8 V1 Acceptance | 完整真实闭环、SLO/安全/回退、converge 与用户验收 | 未执行 |

设计授权允许读取、研究、修订文档、ADR、必要 Git 治理配置与推送，不授权业务实现或生产操作。不伪造 spec/plan/tasks 文件以绕过命令；文档审计发现关闭也不代表运行时缺陷已修复。

涉及代码的新范围，仍遵守 AGENTS.md 和每 Feature 明确授权。仓库同步与合并按用户当次授权执行；本次仅推送设计分支并提供可审阅 PR。

当前可进入第一 Feature 的规格与环境验证准备；不能直接宣称全部业务编码门禁通过。具体差距、独立可推进项及开发机授权提示词见 [Implementation Readiness](../plans/IMPLEMENTATION-READINESS.md)。用户发送明确范围的实现授权后，门禁满足即执行，不重复索要同一授权。
