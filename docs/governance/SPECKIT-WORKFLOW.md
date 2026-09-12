# Spec Kit 工作流

## 1. 唯一路径

逻辑门禁保持：

constitution → specify → clarify → plan → checklist → tasks → analyze → Coding Gate → implement → converge。

规格产物有两种合法生成方式：

1. **开发机 Spec Kit 模式**：通过仓库已有官方 Spec Kit skills/脚本执行；
2. **GitHub Agent 模式**：经用户明确授权的第三方 GitHub Agent，直接在 GitHub Feature 分支中按照同一模板、Constitution、需求基线和质量门禁生成等价产物。

GitHub Agent 模式不得伪称执行过 `$speckit-*` 命令；必须在 `CODING-READINESS.md` 和 `analyze.md` 中标记 `generated-by: external-github-agent`。判断是否可编码，以完整产物、可追溯性、Analyze 和 Checklist 结果为准，而不是依赖某台开发机的命令历史。

需求与设计可以先行，但不能代替运行时 Feature 的完整门禁。

## 2. 本轮需求输入

读取[需求基线](../requirements/REQUIREMENTS-BASELINE.md)、[架构](../architecture/ARCHITECTURE-BASELINE.md)、相关 Contracts/ADR 和[交付路线](../plans/V1-DELIVERY-PLAN.md)。Q1–9 已确认，余项由用户授权采用文档默认方案；不要再次逐题访谈。

V1 为真实业务闭环。首个运行时 Feature 可以用 Fake Provider 验证状态与恢复，但后续真实 KB/模型、只读能力、钉钉/Web 和联合验收均属于 V1 内部里程碑。

## 3. 分支与事实源

一项 Feature 一个 `feature/<number>-<slug>` 分支；编号在创建时检查远端、已有分支和 specs。

- GitHub 已提交分支是唯一开发事实源。
- `feature/002-support-agent-baseline` 是当前架构/治理设计基线，未包含业务实现。
- 首个运行时 Feature 为 `feature/003-support-foundation`，从 `feature/002-support-agent-baseline` 建立。
- GitHub Agent 在 `feature/003-support-foundation` 生成完整设计门禁后，Codex 只消费该分支；开发机本地未提交文件、stash、旧 `001` Feature 和旧会话全部视为废弃历史。
- 若 PR #2 后续合并 main，可将 003 的 PR base 调整到 main；不得因此重建另一套 003 规格。

## 4. 各步骤要解决什么

| 步骤 | 关键产物/检查 |
| --- | --- |
| Constitution | 当前项目原则；需求来源、只读边界、持久任务、开源复用、证据要求、GitHub 事实源 |
| Specify | 一项可交付 Feature；用户场景、FR/NFR、验收、非目标 |
| Clarify | 仅解决真实缺口；权限、持久化、外部接入、通知和恢复语义不可含糊 |
| Plan | 包/镜像版本、接口、数据迁移、模块、错误、测试、SLO、回退 |
| Checklist | 架构、安全、Evidence、恢复、观测、测试、运维 |
| Tasks | 依赖顺序明确、可独立验证的小任务；每项含文件、测试和完成条件 |
| Analyze | Spec/Plan/Tasks/Constitution 一致性；Critical=0、High=0 |
| Coding Readiness | 汇总授权、基线 SHA、清单、同步命令、第一个 Task |
| Implement | Codex 按 Task 实现，变更与证据一并记录 |
| Converge | Spec/Plan/Tasks/Code/Tests 对照；不可只改文档掩盖代码偏差 |

## 5. GitHub Agent 模式完成条件

GitHub Agent 至少生成：

```text
specs/<feature>/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
├── checklists/
│   ├── requirements.md
│   └── implementation.md
├── tasks.md
├── analyze.md
└── CODING-READINESS.md
```

要求：

- 无 `TBD`、`TODO`、未决 `[NEEDS CLARIFICATION]`；
- 需求、计划、任务均可追溯到需求基线/架构/ADR；
- Critical=0、High=0；
- Checklist 无阻塞；
- 真实未验证项必须标为实施验证任务，不能写成已通过；
- 不把 Fake Provider 测试冒充真实 KB/模型/钉钉验收；
- Coding Gate 只对当前 Feature 开放，不代表整体 V1 或生产发布就绪。

## 6. Codex 开发机同步规则

当用户已明确授权“放弃本地一切未保存进度，以 GitHub 为准”，且 `CODING-READINESS.md` 标记 READY 后，Codex 先确认仓库路径和 remote，再执行：

```bash
git fetch origin --prune
git switch feature/003-support-foundation
git reset --hard origin/feature/003-support-foundation
git clean -fd
git status
git rev-parse HEAD
git rev-parse origin/feature/003-support-foundation
```

约束：

- 禁止 `git clean -fdx`；
- 不恢复 stash；
- 不恢复旧 `001-core-harness-product-qa`；
- 不把本地未提交文件拷回新 Feature；
- HEAD 与远端 SHA 不一致时禁止编码；
- 编码前先阅读 `CODING-READINESS.md`、`spec.md`、`plan.md`、`tasks.md`。

## 7. 验证边界

脚本 paths-only 或 branch dry-run 成功只证明路径/分支命名，不证明 Analyze 或业务测试通过。Fake 测试只证明受测边界，真实 Provider 合同与 E2E 仍需独立记录。

长任务的失败、卡顿、人工补充与跨天恢复是 V1 验收必需项；不以普通同步聊天 E2E 代替。
