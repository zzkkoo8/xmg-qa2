# xmg-qa2 分支合并就绪审计

日期：2026-09-12  
审计对象：`main`、`docs/001-support-agent-design`、`backup/001-before-speckit-resume-20260912`、`feature/002-support-agent-baseline`、`feature/003-support-foundation`，以及 PR #1/#2/#3。

## 1. 结论

仓库当前可以进入“设计合并与分支收敛”阶段，但合并顺序和方式必须受控：

1. PR #2 先以 **merge commit** 合并到 `main`；
2. PR #3 再把 base 从 `feature/002-support-agent-baseline` 调整到 `main`；
3. 复核 PR #3 差异仅包含 003 Feature 设计/治理产物；
4. PR #3 再以 merge commit 合并到 `main`；
5. 删除所有已合并/废弃的非 `main` 远端分支；
6. 合并后的 `origin/main` 成为开发机唯一权威设计基线；
7. 开发机强制同步 `origin/main` 后，再从 main 创建新的 `feature/003-support-foundation` 实现分支并从 T001 开始编码。

本审计只证明设计与 Git 分支合并就绪，不证明运行时代码、构建、CI、真实 Provider 或生产验收通过。

## 2. 当前分支拓扑

当前远端分支：

- `main` @ `a2c5399f7c86c19913ca857e7745544e30e0f6c5`
- `feature/002-support-agent-baseline` @ `4c7c26af5495f3ce92d58265c61a7d5ed4155efd`
- `feature/003-support-foundation` @ 003 设计最新提交
- `docs/001-support-agent-design` @ `0050485cce9e1a37e0df1f06ae1dd80e97d20c7b`
- `backup/001-before-speckit-resume-20260912` @ `5bcf0b7d99efa8b8ca9239e91c45f22cef4f3273`
- 临时清理项 `tmp-noop`（审计期间误创建，无独立业务内容；必须与其它非 main 分支一起删除）

拓扑关系：

```text
5bcf0b7  bootstrap
   |
   +-- main a2c5399
         |
         +-- feature/002-support-agent-baseline (+4 commits)
               |
               +-- feature/003-support-foundation (+20+ design commits)
```

`feature/002-support-agent-baseline` 相对 main：ahead 4 / behind 0。  
`feature/003-support-foundation` 相对 002：ahead 20（审计准备修订后继续前进）/ behind 0。

因此 002 → 003 是线性堆叠关系，没有倒挂或双向漂移。

## 3. PR 状态

### PR #1

`docs/001-support-agent-design → main`

- 已 merged；
- 对应内容已进入 main；
- 分支提交图与 main 可能因历史 merge/squash 方式不保持直接祖先关系，但 PR 已完成，不应继续作为开发基线；
- 分支可在最终清理时删除。

### PR #2

`feature/002-support-agent-baseline → main`

- Open + Draft；
- mergeable；
- 35 个设计/治理文件变更；
- 主要内容：需求 1.2、Constitution 1.2、Architecture/Workflow/Contracts、QA Core、Web/交付、开发门禁、企业级就绪审计；
- 没有业务实现代码。

**必须使用 merge commit。** 原因：PR #3 的提交直接以 002 head 为祖先。如果 PR #2 使用 squash/rebase merge，main 会得到等价内容但丢失原祖先关系，PR #3 retarget 到 main 后可能重新展示 002 的大批变更，增加误合并和冲突风险。

### PR #3

`feature/003-support-foundation → feature/002-support-agent-baseline`

- Open + Draft；
- mergeable；
- 设计了第一运行时 Feature 的完整 Spec/Plan/Contracts/Tasks/Analyze/Coding Readiness；
- 没有运行时代码；
- Analyze：Critical=0 / High=0；
- 实现阶段仍由 T001-T013 产生真实测试与运行证据。

PR #2 merge 后，将 PR #3 base 改为 `main`，重新检查 diff 后再 merge。

## 4. 003 设计审计

### 4.1 需求与范围

`spec.md` 将首个 Feature 收敛为 Support Foundation：

- 高质量 QA 控制骨架；
- 持久 SupportTask / wait / resume；
- Harness Contracts / Registry / deny-first Policy；
- PostgreSQL / LangGraph Checkpoint / Celery / RabbitMQ 可靠性验证；
- 最小 Task API；
- 最小 React Chat/Admin 壳；
- 打包与 CI 基础。

真实 Dify、真实模型、钉钉、真实只读 API/MCP 明确属于后续 V1 Feature，不允许 Fake 验收冒充真实接入。

判断：范围适合作为第一可执行 Feature，没有把完整 V1 一次性塞入首个开发任务。

### 4.2 架构一致性

通过项：

- Workflow First：显式有界状态图，不采用无限自由 Agent Loop；
- Evidence First：产品/版本事实要求适用 Evidence；
- Provider Neutral：Model/Knowledge/Tool 通过 Harness contract/registry；
- deny-first：客户目标 WRITE/UNKNOWN 在 provider invoke 前拒绝；
- durable task：业务状态、队列和 checkpoint 职责分离；
- resume：HumanRequest / ResumeAttempt 绑定 request/version/interrupt；
- GitHub Agent 等价 Spec Kit 流程已在 Constitution 1.3.0 中获得授权。

未发现需要推翻整体架构的 Critical/High 设计冲突。

### 4.3 数据与 API

`data-model.md` 已定义 SupportTask、Run、QuestionFrame、HumanRequest、ResumeAttempt、Evidence、AnswerDraft/Check、CapabilityDescriptor、OperationCommit、Inbox/Outbox/Audit 等核心实体。

`openapi.yaml` 已覆盖：

- health/ready；
- login；
- task create/list/detail；
- reply；
- cancel；
- events；
- admin authorization probe。

API 只作为第一 Feature 最小面，不冒充完整 V1 Admin/Channel API。

### 4.4 任务可执行性

`tasks.md` 已拆为 T001-T013：

- T001 锁定真实可兼容工具链/依赖；
- T002-T006 完成 domain/contracts/fake/QA workflow；
- T007-T008 完成真实 queue/checkpoint/recovery/wait-resume；
- T009-T011 完成 API/auth/ACL/observability/Web；
- T012 完成真实容器化 E2E；
- T013 converge 与完整验证。

T001 明确要求实际兼容性探测后再锁版本，因此设计文件没有虚构未经安装验证的精确 package patch 版本，这是合理的实现风险前置方式。

## 5. 合并前发现并修正的问题

### M01：合并后分支指令会失效

原 003 文档要求开发机直接同步 `origin/feature/003-support-foundation`。用户现在要求设计合并后 GitHub 只保留 main，因此原交接方式会变成无效路径。

已在 003 分支修订：

- `AGENTS.md`
- `docs/governance/DEVELOPMENT-GATES.md`
- `docs/governance/SPECKIT-WORKFLOW.md`
- `specs/003-support-foundation/CODING-READINESS.md`

新规则：设计合并后 `origin/main` 是唯一设计基线；开发机先强制同步 main，再创建干净的 `feature/003-support-foundation` 实现分支，禁止直接在 main 编码。

### M02：PR #2 合并方法影响 PR #3 差异

必须采用 merge commit 合并 PR #2，以保留 `4c7c26a` 祖先关系。此项已写入开发门禁与 Spec Kit Workflow。

### M03：无 CI/status checks

PR #2 与 PR #3 当前 commit status 均没有 CI status。两者目前仍是设计/规格变更，没有可执行运行时实现，因此不能用“测试通过”作为合并依据。

合并依据只能是：

- diff/拓扑可控；
- 设计审计无 Critical/High；
- 文档明确区分设计与运行时验证；
- 后续 T001-T013 会建立 CI 与真实实现测试。

不得在 PR/README 中把本次设计合并描述为 runtime tests passed 或 production ready。

## 6. 最终远端清理清单

当 PR #2/#3 都已进入 main 后，删除：

```text
backup/001-before-speckit-resume-20260912
docs/001-support-agent-design
feature/002-support-agent-baseline
feature/003-support-foundation
tmp-noop
```

最终 GitHub 分支只保留：

```text
main
```

删除前再次确认 PR #1/#2/#3 已 merged 且 main tree 包含对应设计文件。

## 7. 开发机后续强制同步

远端清理完成后，开发机执行：

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

读取 `specs/003-support-foundation/CODING-READINESS.md`，从 T001 开始；不要重跑已完成的设计门禁。

## 8. 当前审计判断

**MERGE PREPARATION: READY WITH ORDERED MERGE REQUIREMENT**

没有发现阻止设计进入 main 的 Critical/High 内容问题。仍必须按“PR #2 merge commit → PR #3 retarget/review → PR #3 merge commit → 删除非 main 分支”的顺序执行，且不把设计合并冒充运行时验收。
