# specs/

本目录保存运行时 Feature 的规格、计划、任务、门禁与实施证据，是 Codex 开发的重要事实来源。

## 合法生成方式

Feature 规格有两种合法来源：

1. 开发机通过仓库已有官方 Spec Kit skills/脚本执行；
2. 经用户明确授权的第三方 GitHub Agent，严格按同一模板、Constitution、需求基线和门禁生成 Spec Kit 等价产物。

GitHub Agent 模式必须：

- 标记 `generated-by: external-github-agent`；
- 不伪称开发机执行过 `$speckit-*`；
- 生成 spec / plan / checklist / tasks / analyze / CODING-READINESS 等完整门禁；
- Critical=0、High=0、编码前 Checklist 无阻塞后才能开放 Coding Gate。

## 当前首个运行时 Feature

- [`003-support-foundation/`](003-support-foundation/)：第一套可执行 QA / 持久任务 / Harness / API / Web / CI 基础，状态见其中 `CODING-READINESS.md`。

## 通用规则

- 一项 Feature 对应一个 `feature/<number>-<slug>` 分支。
- 架构级长期决策同时写入 `docs/adr/`。
- GitHub 已提交 Feature 是开发事实源；本地未提交文件、stash 和旧 Agent 会话不能覆盖它。
- 发现代码与 Spec 漂移时使用 converge 流程处理。
- 未实际运行的实现测试、真实 Provider 联调或部署不得写成已通过。
