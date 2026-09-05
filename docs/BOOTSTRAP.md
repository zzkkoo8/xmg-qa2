# xmg-qa2 Bootstrap Guide（历史初始化记录）

> 本文记录 2026-08-28 的初始化流程与当时版本，不是当前仓库的续接步骤。仓库已初始化，Constitution 已于 2026-09-05 形成设计基线；不要重跑 init、覆盖现有配置或重复生成宪法。后续按 [当前 Spec Kit 流程](governance/SPECKIT-WORKFLOW.md) 和 [交付计划](plans/V1-DELIVERY-PLAN.md) 进入新 Feature。历史命令未在本轮重新验证。

## 目的

在一个全新的空目录中，以 **官方 Spec Kit + Codex skills + 标准 Git 仓库** 初始化 xmg-qa2。

基线验证日期：2026-08-28。

## 推荐顺序

### 0. 前提检查

```bash
python3 --version
git --version
codex --version
specify version
```

推荐 Python 3.11+。

如果尚未安装 Spec Kit，可使用官方 PyPI 包并固定版本：

```bash
uv tool install specify-cli==1.0.1
specify version
```

如果机器已经安装 Spec Kit，不要无理由重复安装；先运行：

```bash
specify version
specify self check
```

## 1. 创建全新项目目录

```bash
mkdir -p /data/dev/xmg-qa2
cd /data/dev/xmg-qa2
```

必须确认目录不存在历史业务代码：

```bash
pwd
find . -maxdepth 2 -mindepth 1 -print
```

理想状态为空。

## 2. 初始化 Spec Kit

推荐：

```bash
specify init --here --integration codex --script sh
```

说明：

- `--here`：初始化当前目录。
- `--integration codex`：明确使用 Codex，避免非交互环境落到其他默认 integration。
- `--script sh`：Linux 环境明确使用 Bash 脚本。
- Codex 当前默认使用 skills 模式，因此通常不需要额外写 `--integration-options="--skills"`。

### 不推荐

不要在一个已放入大量项目文件的目录中直接执行：

```bash
specify init --here --force ...
```

`--force` 是合并/覆盖模式。新项目没有必要承担这个风险。

## 3. 安装 Spec Kit Git Extension

Spec Kit 当前不会默认启用 Git 工作流，因此执行：

```bash
specify extension add git
```

验证：

```bash
specify extension list
```

## 4. 建立标准 Git 仓库

为避免出现历史项目中的 `.git-data` 非标准状态，本项目明确要求标准 `.git/`。

如果当前还不是 Git 仓库：

```bash
git init -b main
```

检查：

```bash
test -d .git
git rev-parse --show-toplevel
git status
```

必须确认 `.git/` 是真实 Git metadata 目录，不是空挂载点。

> Spec Kit git extension 自身也具备初始化 Git 的能力；这里显式 `git init -b main` 是为了在 xmg-qa2 开局就固定标准仓库形态。扩展检测到已有 Git 仓库后应复用现有仓库。

## 5. 放入本基线文档

把本压缩包内容合入项目根目录。

注意：

- 不覆盖 `.specify/`。
- 不覆盖 `.agents/skills/`。
- 不手工创建任何 `speckit-*` skill。
- 本包中的 `src/`、`tests/` 只有目录占位，不含业务代码。

## 6. 初始化提交

检查：

```bash
git status
git diff --check
```

确认后：

```bash
git add .
git commit -m "chore: bootstrap xmg-qa2 architecture baseline"
```

## 7. Spec Kit 文件验收

至少确认：

```bash
test -d .specify
test -d .agents/skills
find .agents/skills -maxdepth 2 -name 'SKILL.md' -print | sort
```

应能看到 Spec Kit 的 Codex skills。

## 8. 第一次正式 SpecKit 工作流

不要直接 implement。

第一阶段只执行：

```text
$speckit-constitution
```

输入应基于：

- `README.md`
- `AGENTS.md`
- `docs/architecture/*`
- `docs/governance/*`
- `docs/adr/*`

Constitution 生成后必须人工审阅。

随后对 V1 第一个 Feature 执行：

```text
$speckit-specify
$speckit-clarify
$speckit-plan
$speckit-checklist
$speckit-tasks
$speckit-analyze
```

直到：

- 0 Critical
- 0 High
- 人工明确批准

才允许：

```text
$speckit-implement
```

实现后：

```text
$speckit-converge
```

## 9. Gate 1 验收

在任何业务编码开始前应满足：

- [ ] `.specify/` 来自官方 CLI 初始化。
- [ ] `.agents/skills/` 存在 Codex Spec Kit skills。
- [ ] 标准 `.git/` 正常。
- [ ] git extension 已启用。
- [ ] Architecture Baseline 已人工批准。
- [ ] Constitution 已人工批准。
- [ ] V1 Feature Spec 已人工批准。
- [ ] Plan 已人工批准。
- [ ] Checklist 无阻断项。
- [ ] Analyze 为 0 Critical / 0 High。
