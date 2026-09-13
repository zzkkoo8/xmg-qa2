# 开发门禁

状态日期：2026-09-12。状态必须以实际产物和授权为准，不把“设计完成”写成“实现完成”或“生产就绪”。

当前首个运行时 Feature 为 `003-support-foundation`。其规格由经用户授权的 `external-github-agent` 按仓库 Spec Kit 等价流程在 GitHub 中生成；开发机 Codex 不需要重复执行已完成的 specify/plan/tasks，而应消费 GitHub 已提交的权威基线。

## Gate 状态

| Gate | 通过条件 | 当前状态 |
| --- | --- | --- |
| 0 需求/架构方向 | 已知需求、默认项及取舍有来源；用户授权形成设计 | **PASS**：需求 1.2 + `feature/002-support-agent-baseline` 设计基线 |
| 1 Constitution | 与当前需求一致，无占位符/冲突，授权可追溯 | **PASS**：Constitution 1.3.0 |
| 2 Feature Spec | 场景/FR/非目标/成功标准明确，关键歧义解决 | **PASS**：`specs/003-support-foundation/spec.md` + `clarifications.md` |
| 3 Plan/Checklist/Tasks | 模块/Schema/API/安全/测试/恢复齐全，任务可执行 | **PASS TO START**：plan/data-model/contracts/checklists/tasks 齐全；实现清单剩余项由 T001-T013 实测关闭 |
| 4 Analyze | Critical=0、High=0；Medium 有决定；Checklist 无设计阻塞 | **PASS**：`analyze.md` Critical=0 / High=0 |
| 5 Coding Authorization | 用户明确批准对应 Feature 实现 | **PASS**：用户要求 GitHub Agent 设计到 Codex 可直接编码，并授权本地放弃未保存进度、强制以 GitHub 为准 |
| 6 Task Verification | 每 Task 有真实验证输出、变更范围、commit | **PENDING IMPLEMENTATION** |
| 7 Integration | 真实 KB/模型/钉钉/只读能力 + 持久恢复和失败测试 | **PARTIAL BY DESIGN**：本 Feature 只要求真实 PG/checkpointer/RabbitMQ 恢复测试；真实外部 Provider 属后续 V1 Feature |
| 8 V1 Acceptance | 完整真实闭环、SLO/安全/回退、converge 与用户验收 | **NOT STARTED** |

## 当前 Coding Gate

`003-support-foundation` 的设计 Coding Gate 为 **OPEN**，但实现启动采用“合并后 main 为基线”的交接方式：

1. 先合并 PR #2 到 `main`；
2. 将 PR #3 的 base 调整为 `main` 并确认 diff 只包含 003 设计/治理产物；
3. 合并 PR #3；
4. 删除已完成/废弃的非 main 远端分支；
5. 此时 `origin/main` 是唯一权威设计基线；
6. 开发机强制同步到 `origin/main`，确认工作树干净且 SHA 一致；
7. Codex 从该 main 新建干净的 `feature/003-support-foundation` 实现分支；
8. 阅读 `specs/003-support-foundation/CODING-READINESS.md` 后从 T001 开始。

禁止直接在 `main` 编码。详细同步方式见 `specs/003-support-foundation/CODING-READINESS.md`。

## 合并方法约束

PR #3 当前堆叠在 PR #2 上。为保留祖先关系、避免 PR #3 在 PR #2 合并后重新显示整套 002 变更，**PR #2 应使用 merge commit 合并，不使用 squash/rebase merge**。随后再把 PR #3 retarget 到 `main` 并复核差异。

PR #3 合并后没有更下游堆叠分支，但为保留完整设计历史，同样优先使用 merge commit。

## 仍然禁止的推断

Coding Gate OPEN 只表示当前 `support-foundation` Feature 可以进入实现，不表示：

- 企业生产就绪；
- V1 全部完成；
- 已通过真实 Dify/LLM/钉钉/MCP 联调；
- 可以执行客户生产写操作；
- 当前设计分支上已经存在运行时代码或测试通过证据。

T001-T013 完成后必须按实现清单和真实测试证据 converge；真实 Provider 与发布验收继续由后续 Feature 关闭。
