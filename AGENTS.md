# AGENTS.md — xmg-qa2 AI 开发约束

本文件对 Codex 及其他 AI Coding Agent 生效。当前需求入口为 [需求基线](docs/requirements/REQUIREMENTS-BASELINE.md)，状态见 [开发门禁](docs/governance/DEVELOPMENT-GATES.md)。

## 1. 总原则

本项目采用 Spec-Driven Development。Agent 必须确保：

1. 需求有明确来源；
2. 设计经过人工授权或授权代理流程确认；
3. 模块边界可验证；
4. 实现可测试、可回退；
5. 每次完成结论都有实际证据；
6. GitHub 已提交内容优先于开发机未提交草稿、stash 和会话记忆。

规格产物可由两类执行者生成：

- 开发机通过仓库官方 Spec Kit skills/脚本生成；
- 经用户明确授权的第三方 GitHub Agent，按同一模板、Constitution、需求基线和门禁生成等价产物。

GitHub Agent 生成的文件必须记录来源，不得伪称开发机已执行 `$speckit-*` 命令。

## 2. 编码门禁

以下条件任一未满足时，禁止新增或修改业务实现代码：

- Constitution 未与当前需求一致；
- 当前 Feature `spec.md` 不完整或仍有关键歧义；
- Clarify 仍有关键未决项；
- `plan.md` 未冻结关键技术/契约/数据/测试边界；
- Checklist 存在阻断项；
- `tasks.md` 未完成拆分；
- Analyze 存在 Critical 或 High；
- `CODING-READINESS.md` 未明确标记 READY/OPEN；
- 用户尚未授权当前 Feature 实现范围。

当 `specs/<feature>/CODING-READINESS.md` 明确记录 `Critical=0`、`High=0`、Checklist 无设计阻塞、实现授权来源明确时，Codex 可开始当前 Feature，实现时无需重复已由 GitHub Agent 完成的规格阶段。

## 3. 架构硬约束

### 3.1 Workflow First

核心问答链路必须由显式 Workflow / State Graph 描述。禁止把是否检索、来源选择、重试、证据充分性、终止与无证据答案等关键决策完全交给无边界自由 Agent Loop。

### 3.2 外部能力全部经过契约

Channel、Knowledge、Model、Tool、Policy 不得被 Workflow 直接绑定到具体厂商，必须通过 Harness Contract / Registry 获取。

### 3.3 知识工程与 QA Runtime 解耦

xmg-qa2 不负责 PDF/PPT/Word 解析、OCR、清洗、去重、分类、切片、Embedding 批处理和知识库构建，只消费 Knowledge Contract。

### 3.4 依赖方向

依赖采用端口与适配器，按 [Dependency Rules](docs/architecture/DEPENDENCY-RULES.md) 执行：

- `domain` 不得 import LangGraph、FastAPI、Dify、RAGFlow、OpenAI SDK；
- `harness/contracts` 不得 import 具体 Provider；
- `workflow` 不得 import DingTalk、Dify、RAGFlow 等实现；
- `plugins` 可以依赖 contracts，但 contracts 不得反向依赖 plugins；
- `api/channels` 不得包含核心问答业务规则。

替换 Model / Knowledge / Channel / Tool Provider 不应要求修改 Harness Core；若必须修改 Core，先写 ADR。

## 4. Evidence First

知识、网页、API 和现场观察统一使用 [Knowledge Contract](docs/architecture/KNOWLEDGE-CONTRACT.md) 的 Evidence 定义。至少保留真实出处、内容引用/摘录、采集时间、授权范围及命题支持关系；`retrieval_score` 不等于事实置信度。

产品/现场结论证据不足时必须进入 fallback，不得编造。问答质量按 [QA Core](docs/architecture/QA-CORE.md) 和 [Answer Quality](docs/governance/ANSWER-QUALITY.md) 验收。

## 5. 可观测性

每个 Turn 至少应可关联 task_id / run_id / operation_id / trace_id / thread_id / turn_id / workflow/version / node / provider / latency / retry_count / evidence IDs / final outcome；Provider 支持时记录 token/cost。默认不保存隐藏思维链，不把原始秘密或客户日志写入普通日志。

## 6. Git 与唯一事实源

- GitHub 已提交内容是唯一协作事实源；开发机未提交文件、stash、未推送 Feature 和旧 Agent 会话不构成项目事实。
- **设计分支在审计通过并合并后，`main` 成为唯一权威设计基线。** 已合并设计分支可以删除。
- 禁止直接在 `main` 编码。实现必须从干净的 `origin/main` 创建 `feature/<number>-<slug>` 分支。
- 本轮 003 的设计合并后，开发机先强制同步 `origin/main`，再创建新的 `feature/003-support-foundation` 实现分支；分支名可复用，但内容必须从合并后的 main 起步。
- 用户明确授权“强制以 GitHub 为准”时，可放弃本地未保存文件、stash 和未推送分支；不得删除仓库外秘密、共享目录或其他项目数据。
- `git reset --hard <remote-ref>` 和 `git clean -fd` 仅在用户明确授权且已确认正确仓库时使用；禁止 `git clean -fdx`。
- 禁止 force-push 共享分支，除非用户对具体分支再次明确授权。
- 进入实现前必须确认本地 main HEAD 等于 `origin/main`，然后再创建实现 Feature 分支。

## 7. 实现工作规范

进入实现阶段后：

1. 先读当前 Feature 的 `CODING-READINESS.md`、`spec.md`、`plan.md`、`tasks.md`、相关 ADR；
2. 一次只执行当前 Task；
3. 优先测试驱动；
4. 修改后立即执行最小相关测试；
5. 再执行集成测试；
6. 失败时先定位根因；
7. 未实际运行验证命令，不得宣称已解决；
8. 如果代码需求与规格冲突，停止实现并回到 GitHub 规格修订，不在本地私自改变产品边界。

## 8. 完成定义

任何 Task 声称完成必须附：修改文件、验证命令、验证输出摘要、影响范围、剩余风险和 Git commit。“代码已写完”不等于完成。

## 9. 本轮固定产品边界

- V1 是真实 KB/模型、钉钉、只读能力、人工恢复和报告的垂直闭环；Fake 只用于测试；
- SupportTask 高于 Thread/Turn；等待须持久保存并释放 Worker；
- 客户目标仅 READ_ONLY；WRITE/UNKNOWN、任意 shell/未审核脚本默认拒绝；
- 人工“批准/继续”不解锁生产写；
- 模型可提供通用知识、假设与建议，但不得伪造产品/现场证据；
- 所有外发点执行数据策略；
- 本系统任务/报告写入和授权渠道通知与客户目标写权限分开；
- 优先成熟开源，不堆叠多个 Agent 框架或知识入库系统。

## 10. Web、模板与分发

- V1 包含 Chat/Admin；前端按 [Web Console](docs/architecture/WEB-CONSOLE.md)，不新建第二 Agent 后端或浏览器直连模型/KB；
- Admin 可写自有配置，但不能放宽客户目标只读权限；Case ACL 与管理员角色独立；
- HTML/MD/主题按 [Presentation Contract](docs/architecture/PRESENTATION-CONTRACT.md)；
- 开发、镜像、在线/离线包及回退按 [Distribution](docs/architecture/DISTRIBUTION-DEPLOYMENT.md)。

## 11. GitHub Agent → Codex 交接

GitHub Agent 完成 Feature 设计时至少提交：`spec.md`、`plan.md`、`research.md`、`data-model.md`、`quickstart.md`、`contracts/`、requirements/implementation checklist、`tasks.md`、`analyze.md`、`CODING-READINESS.md`。

本轮设计合并后，Codex 的标准交接顺序为：

```text
origin/main
  -> 强制同步开发机 main
  -> 验证 HEAD == origin/main
  -> 创建 feature/003-support-foundation 实现分支
  -> 阅读 specs/003-support-foundation/
  -> 从 T001 开始实现
```

`CODING-READINESS.md` 是开工入口；设计合并到 main 后，其中记录的 main 同步规则优先于历史 PR/分支路径。
