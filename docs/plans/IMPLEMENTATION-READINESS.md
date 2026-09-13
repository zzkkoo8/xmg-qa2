# 编码就绪判断与开发机 Codex 交接

更新：2026-09-12。

## 1. 当前结论

首个运行时 Feature `003-support-foundation` 已由经用户授权的 GitHub Agent 完成完整设计门禁，当前状态：

**READY FOR CODEX IMPLEMENTATION AFTER DESIGN MERGE**

当前物理设计来源仍在 `feature/003-support-foundation`，但用户已经决定先把 PR #2/#3 合并到 `main`、清理非 main 远端分支，再让开发机以合并后的 `origin/main` 为唯一设计事实源。

本结论仅开放 `support-foundation` Feature 编码，不代表完整 V1、生产部署或真实外部 Provider 已验收。

## 2. 已完成的设计门禁

Feature 目录：[`specs/003-support-foundation/`](../../specs/003-support-foundation/)

已完成：

- `spec.md`：用户场景、FR、非目标、成功标准；
- `clarifications.md`：关键歧义关闭；
- `research.md`：运行时、持久化、Harness、测试等实现决策；
- `data-model.md`：SupportTask/Run/HumanRequest/ResumeAttempt/Evidence/Answer 等数据契约；
- `contracts/provider-contracts.md`：Model/Knowledge/Tool/Policy/Registry 契约；
- `contracts/openapi.yaml`：Foundation API 契约；
- `plan.md`：源码布局、事务/恢复/API/Web/CI/安全实施计划；
- `checklists/requirements.md`：需求质量 PASS；
- `checklists/implementation.md`：编码前门禁 PASS，运行时项待实现验证；
- `tasks.md`：T001-T013 可执行开发任务；
- `analyze.md`：Critical=0、High=0；
- `CODING-READINESS.md`：Codex 同步、权限、停止条件和第一个 Task。

Constitution 已升级至 1.3.0，AGENTS/Spec Kit Workflow/Development Gates 已同步 GitHub-Agent 设计模式和 main-first 合并后交接模式。

## 3. 当前 Feature 实现范围

`support-foundation` 交付第一套真正可运行的基础闭环：

- Python/Node/容器依赖锁定和可复现构建；
- QuestionFrame、AnswerDraft、AnswerCheck 及有界 QA Workflow；
- Model/Knowledge/Tool/Policy Harness Contracts 与 Registry；
- customer-target READ_ONLY/WRITE/UNKNOWN 硬边界；
- SupportTask/Run/HumanRequest/ResumeAttempt 持久业务状态；
- PostgreSQL + LangGraph PostgreSQL checkpoint + Celery/RabbitMQ 真实恢复/幂等验证；
- 至少 20 个确定性问答/控制测试场景；
- 最小认证、Case ACL、REST Task API；
- React Chat/Admin 最小壳；
- Docker/Compose、CI、结构化可观测性；
- create → wait → restart → reply → resume → checked answer 的 Foundation E2E。

Fake Model/Knowledge/Tool 仅用于可重复控制测试。

## 4. 后续 V1 但不属于当前 Feature 的内容

完成 Foundation 后仍需独立 Feature 落地并真实验收：

- Dify Knowledge/xmg-kb；
- 真实模型与答案质量冻结题集；
- 钉钉入口/出站通知；
- 至少一种真实产品 READ_ONLY API/MCP 能力；
- 完整 Admin/模板/插件管理体验；
- 在线/离线发布包和目标 OS 回退/恢复实测。

因此 Foundation 完成不能宣称 V1 或企业生产发布完成。

## 5. 合并与 Codex 开工入口

先完成设计收敛：

1. PR #2 使用 merge commit 合并到 `main`；
2. PR #3 retarget 到 `main` 并复核只剩 003 设计差异；
3. PR #3 使用 merge commit 合并；
4. 删除已合并/废弃的非 main 远端分支；
5. 合并后的 `origin/main` 成为唯一权威设计基线。

随后开发机先执行：

```bash
git fetch origin --prune
git switch main
git reset --hard origin/main
git clean -fd
git status
git rev-parse HEAD
git rev-parse origin/main
```

两个 SHA 必须一致，工作区必须 clean。禁止 `git clean -fdx`。

然后创建实现分支：

```bash
git switch -C feature/003-support-foundation main
```

Codex 不重新执行 `$speckit-specify → plan → tasks`，而是依次读取：

1. `AGENTS.md`
2. `.specify/memory/constitution.md`
3. `specs/003-support-foundation/CODING-READINESS.md`
4. `specs/003-support-foundation/spec.md`
5. `specs/003-support-foundation/plan.md`
6. `specs/003-support-foundation/tasks.md`

然后从 T001 开始开发。禁止直接在 main 编码。

## 6. 风险停止条件

以下情况才停止对应 Task 并请求重新设计/ADR：

- 既定核心组件组合经真实兼容测试不能工作，需要替换组件家族；
- 无法实现 lease/state-version fencing 或 checkpoint/business-state 对账；
- 实现必须突破客户目标只读边界；
- 发现当前 spec/plan 的 Critical/High 矛盾；
- 必须修改开发机其他项目或共享基础设施才能继续。

普通代码错误、依赖小版本调整、测试失败属于 Codex 调试范围，不应重新启动整套需求访谈。

## 7. 最终原则

**main 定义已接受设计，Feature 分支承载实现，Codex 按 Tasks 实现并提供真实验证证据。**

设计文件不能代替运行时证明；运行时实现也不能私自改变已确认的需求/安全边界。
