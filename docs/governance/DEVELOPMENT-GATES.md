# 开发门禁

状态日期：2026-09-12。状态必须以实际产物和授权为准，不把“设计完成”写成“实现完成”或“生产就绪”。

当前首个运行时 Feature：`feature/003-support-foundation`。其规格由经用户授权的 `external-github-agent` 按仓库 Spec Kit 等价流程在 GitHub 中生成；开发机 Codex 不需要重复执行已完成的 specify/plan/tasks，而是以 GitHub 已提交 Feature 为唯一事实源。

| Gate | 通过条件 | 当前状态 |
| --- | --- | --- |
| 0 需求/架构方向 | 已知需求、默认项及取舍有来源；用户授权形成设计 | **PASS**：需求 1.2 + `feature/002-support-agent-baseline` 设计基线 |
| 1 Constitution | 与当前需求一致，无占位符/冲突，授权可追溯 | **PASS**：Constitution 1.3.0，增加 GitHub-Agent 规格路径与 GitHub 事实源规则 |
| 2 Feature Spec | 场景/FR/非目标/成功标准明确，关键歧义解决 | **PASS**：`specs/003-support-foundation/spec.md` + `clarifications.md` |
| 3 Plan/Checklist/Tasks | 模块/Schema/API/安全/测试/恢复齐全，任务可执行 | **PASS TO START**：plan/data-model/contracts/checklists/tasks 齐全；实现清单剩余项由 T001-T013 实测关闭 |
| 4 Analyze | Critical=0、High=0；Medium 有决定；Checklist 无设计阻塞 | **PASS**：`analyze.md` Critical=0 / High=0 |
| 5 Coding Authorization | 用户明确批准对应 Feature 实现 | **PASS**：用户明确要求 GitHub Agent 设计到 Codex 可直接编码，并要求 Codex 放弃本地未保存进度、强制以 GitHub 为准 |
| 6 Task Verification | 每 Task 有真实验证输出、变更范围、commit | **PENDING IMPLEMENTATION**：Codex 从 T001 开始逐项提供证据 |
| 7 Integration | 真实 KB/模型/钉钉/只读能力 + 持久恢复和失败测试 | **PARTIAL BY DESIGN**：本 Feature 只要求真实 PG/checkpointer/RabbitMQ 恢复测试；真实外部 Provider 属后续 V1 Feature |
| 8 V1 Acceptance | 完整真实闭环、SLO/安全/回退、converge 与用户验收 | **NOT STARTED** |

## 当前 Coding Gate

`feature/003-support-foundation` 的 Coding Gate 为 **OPEN**。

Codex 开工前必须：

1. `git fetch origin --prune`；
2. 切换 `feature/003-support-foundation`；
3. 按用户授权执行 `git reset --hard origin/feature/003-support-foundation` 与 `git clean -fd`；
4. 不使用 `git clean -fdx`；
5. 不恢复旧 stash / `001-core-harness-product-qa`；
6. 确认本地 HEAD == 远端 Feature HEAD；
7. 阅读 `specs/003-support-foundation/CODING-READINESS.md`；
8. 从 `tasks.md` 的 T001 开始。

完整同步与授权边界见 [`CODING-READINESS.md`](../../specs/003-support-foundation/CODING-READINESS.md)。

## 仍然禁止的推断

Coding Gate OPEN 只表示当前 `support-foundation` Feature 可以实现，不表示：

- 企业生产就绪；
- V1 全部完成；
- 已通过真实 Dify/LLM/钉钉/MCP 联调；
- 可以执行客户生产写操作；
- 可以自动 merge main 或正式部署。

T001-T013 完成后必须按实现清单和真实测试证据 converge；真实 Provider 与发布验收继续由后续 Feature 关闭。
