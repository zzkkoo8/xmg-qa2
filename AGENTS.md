# AGENTS.md — xmg-qa2 AI 开发约束

本文件对 Codex 及其他 AI Coding Agent 生效。

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

原则性方向：

`domain <- harness contracts <- workflows/runtime <- plugins/infrastructure <- api/channel`

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

知识问答必须保留统一 Evidence：

- source
- document_id
- chunk_id
- title
- content
- score
- metadata
- knowledge_version

无证据或证据不足时，Workflow 必须进入明确定义的 fallback，不得编造答案。

## 5. 可观测性

每个 Turn 至少应可关联：

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

不得把 Prompt、Token、检索、错误原因隐藏在无法审计的黑盒里。

## 6. Git 规范

- 必须使用标准 `.git/`。
- 禁止创建 `.git-data` 等非标准替代仓库，除非用户明确批准且有 ADR。
- 开始任何 Feature 前确认 `git status`。
- 一项 Feature 一个 Spec Kit Feature 分支。
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
