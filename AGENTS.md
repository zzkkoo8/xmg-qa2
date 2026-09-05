# AGENTS.md — xmg-qa2 AI 开发约束

本文件对 Codex 及其他 AI Coding Agent 生效。当前需求入口为 [需求基线](docs/requirements/REQUIREMENTS-BASELINE.md)，状态见 [开发门禁](docs/governance/DEVELOPMENT-GATES.md)。

## 1. 总原则

本项目采用 Spec-Driven Development。Agent 的职责不是“尽快写代码”，而是确保：

1. 需求有明确来源。
2. 设计经过人工确认。
3. 模块边界可验证。
4. 实现可测试、可回退。
5. 每次结论都有证据。

## 2. 禁止提前编码

以下条件任一未满足时，禁止新增或修改业务实现代码：

- Constitution 未批准。
- 当前 Feature Spec 未批准。
- Clarify 仍有关键未决项。
- Plan 未批准。
- Checklist 存在阻断项。
- Tasks 未完成拆分。
- Analyze 存在 Critical 或 High 冲突。
- 用户尚未明确授权进入实现阶段。

允许在编码门禁前修改的内容仅包括：

- Markdown 需求/设计/ADR 文档。
- Spec Kit 生成的规格与计划文件。
- 纯配置模板且不改变运行行为的文档性内容。

## 3. 架构硬约束

### 3.1 Workflow First

核心问答链路必须由显式 Workflow / State Graph 描述。

禁止把以下关键决策完全交给一个自由 Agent Loop：

- 是否检索知识库。
- 使用哪个知识源。
- 重试次数。
- 证据是否充分。
- 何时终止。
- 是否输出无证据答案。

### 3.2 外部能力全部经过契约

以下模块不得被 Workflow 直接绑定到具体厂商：

- Channel
- Knowledge
- Model
- Tool
- Policy

必须通过 Harness Contract / Registry 获取。

### 3.3 知识工程与 QA Runtime 解耦

xmg-qa2 不负责：

- PDF/PPT/Word 解析。
- OCR。
- 清洗。
- 去重。
- 分类。
- 切片。
- Embedding 批处理。
- 知识库构建。

xmg-qa2 只消费 Knowledge Contract。

### 3.4 依赖方向

依赖采用端口与适配器，按 [Dependency Rules](docs/architecture/DEPENDENCY-RULES.md) 的矩阵执行；composition root 装配具体实现，禁止循环依赖。

强制规则：

- `domain` 不得 import LangGraph、FastAPI、Dify、RAGFlow、OpenAI SDK。
- `harness/contracts` 不得 import 任何具体 Provider。
- `workflow` 不得 import DingTalk、Dify、RAGFlow 等实现。
- `plugins` 可以依赖 contracts，但 contracts 不得反向依赖 plugins。
- `api/channels` 不得包含核心问答业务规则。

### 3.5 Provider Neutral

替换以下任一 Provider，不应要求修改 Harness Core：

- LLM
- Knowledge Store
- Channel
- Tool

如果替换 Provider 需要修改 Core，视为架构缺陷，必须先写 ADR。

## 4. Evidence First

知识、网页、API 和现场观察统一使用 [Knowledge Contract](docs/architecture/KNOWLEDGE-CONTRACT.md) 的 Evidence 定义；字段名称、适用范围、可空规则与版本语义以该契约为准。至少保留真实出处、内容引用/摘录、采集时间、授权范围及命题支持关系；非文档证据不伪造 document_id/chunk_id，retrieval_score 不等于事实置信度。

无证据或证据不足时，Workflow 必须进入明确定义的 fallback，不得编造答案。

产品首要目标是高质量回答问题；按 [QA Core](docs/architecture/QA-CORE.md) 理解子问题、选择补证动作、生成与检查答案，按 [Answer Quality](docs/governance/ANSWER-QUALITY.md) 验收。低风险稳定通用解释可经显式路由直答，产品事实仍内部知识优先。部分回答不得自动结案，工具数量/引用数量不能代替正确性。

## 5. 可观测性

每个 Turn 至少应可关联：

- task_id / run_id / operation_id
- trace_id
- thread_id
- turn_id
- workflow
- workflow_version
- node
- provider
- latency
- retry_count
- token/cost（Provider 支持时）
- evidence ids
- final outcome

记录模型/提示词版本、调用量、检索和错误分类；默认不导出原始 Prompt/客户日志，不保存隐藏思维链。必要审计内容按 case 权限和保留策略访问。

## 6. Git 规范

- 必须使用标准 Git；常规仓库为 `.git/`，标准 linked worktree 的 `.git` 文件同样有效。
- 禁止创建 `.git-data` 等非标准替代仓库，除非用户明确批准且有 ADR。
- 开始任何 Feature 前确认 `git status`。
- 一项 Feature 一个 Spec Kit Feature 分支：`feature/<number>-<slug>`。
- 不在 `main` 上直接开发。
- 变更前确保已有可回退提交。
- 不使用 `git reset --hard`、`git clean -fdx` 等破坏性命令，除非用户明确批准。
- 不擅自覆盖用户未提交文件。

## 7. 实现工作规范

进入实现阶段后：

1. 先读 `spec.md`、`plan.md`、`tasks.md`、相关 ADR。
2. 一次只执行当前 Task。
3. 优先测试驱动。
4. 修改后立即执行最小相关测试。
5. 再执行集成测试。
6. 失败时先定位根因，禁止无证据猜测式连续修改。
7. 未实际运行验证命令，不得宣称“已解决”。

## 8. 完成定义

任何 Task 声称完成必须附：

- 修改文件。
- 验证命令。
- 验证输出摘要。
- 影响范围。
- 已知剩余风险。
- Git commit（进入正式实现阶段后）。

“代码已写完”不等于完成。


## 9. 本轮固定的产品边界

- V1 是真实 KB/模型、钉钉、只读能力、人工恢复和报告的垂直闭环；Fake 只用于测试。
- SupportTask 高于 Thread/Turn；等待须持久保存并释放 Worker，恢复验证 case/request/version/ACL。
- 客户目标仅 READ_ONLY；WRITE/UNKNOWN、任意 shell/未审核脚本默认拒绝。人工“批准/继续”不解锁生产写。
- 模型可提供通用知识、假设与建议，不伪造产品/现场证据；动态裁决遵守命题类型、版本和时效。
- 所有外发点执行数据策略；包括公开搜索、模型、embedding/rerank、MCP 参数与遥测。
- 本系统任务/报告写入和授权渠道通知允许通过明确 system_effect 执行，不与客户目标写权限混淆。
- 优先成熟开源；核心只实现支持领域规则，不堆叠多个 Agent 框架或知识入库系统。
- 用户已授权本轮设计修订与推送；不因此推断业务编码、合并主分支或部署授权。

## 10. Web、模板与分发

- V1 包含 Chat/Admin；前端按 [Web Console](docs/architecture/WEB-CONSOLE.md)，不新建第二 Agent 后端或浏览器直连模型/KB。
- Admin 可写自有配置，但不能放宽客户目标只读权限；Case ACL 与管理员角色独立。
- HTML/MD/主题按 [Presentation Contract](docs/architecture/PRESENTATION-CONTRACT.md)；模板热发布不等于任意 JS/Python 热执行。
- 开发、镜像、在线/离线包及回退按 [Distribution](docs/architecture/DISTRIBUTION-DEPLOYMENT.md)；不能改坏开发机其他项目的工具链。
- 第一 Feature 起步与现有缺口见 [Implementation Readiness](docs/plans/IMPLEMENTATION-READINESS.md)。用户已明确授权的实现范围通过规定门禁后直接执行，不重复索要相同授权。
