# xmg-qa2 Constitution

Version: 1.0.0 | Adopted as design baseline: 2026-09-05 | Last amended: 2026-09-05

授权来源：用户已确认 Q1–9，并于 2026-09-05 授权剩余问题采用最佳方案、审计修订设计并推送。本文由未填写模板形成项目宪法；此授权不包含业务编码、部署或生产目标变更。

## I. 需求与规格先行

需求必须可追溯到 docs/requirements/REQUIREMENTS-BASELINE.md。未知事实明确标注，默认设计项不得冒充用户逐题答复。每个业务 Feature 执行 constitution → specify → clarify → plan → checklist → tasks → analyze；Critical/High 清零并获得对应实现授权后才编码。

## II. Workflow First 与能力可配置

核心支持链路使用显式 Workflow/State Graph。模型只在获准节点提出语义判断、假设、动作和答复。能力、优先级、条件、预算和终止规则配置化；组织 Policy 是不可被产品配置、模型、Skill 或外部内容放宽的上限。禁止无限 Agent Loop。

## III. 只读客户目标

小马哥集中运行，不在客户生产机部署 Agent。对客户目标仅使用已授权只读 API/MCP/Gateway/诊断；目标写、重启、安装、升级、删除、任意 shell 和未知动作不执行。人类协助用于补证据/接手，不能成为批准生产写操作的后门。

本系统必须能持久化任务、报告并发送授权通知；这些自有业务写入与目标系统写权限分开管理和审计。

## IV. 持久 SupportTask

Case 高于 Thread/Turn，调查跨轮保存。等待用户、工程师或外部条件必须持久化原因、所需资料、恢复条件和版本，释放 Worker。恢复验证归属、权限、请求和状态版本。采用幂等、唯一有效执行者、检查点对账，不宣称至少一次投递等于外部恰好一次执行。

## V. Evidence First 与动态裁决

区分产品官方支持、现场状态、通用解释和根因假设；按适用版本、时效、权威性、直接性、验证情况和冲突判断。检索 score/模型自信不是事实可信度。关键产品/现场结论有真实证据；缺证据时标注不确定并继续取证/求助。模型内置知识可推理，但不得伪造来源。

## VI. 知识生产与在线调查解耦

文档批量解析、清洗、去重、分类、切片、Embedding、索引发布属于独立 xmg-kb。xmg-qa2 通过 Knowledge Contract 消费知识，保留出处、权限、时间和版本；没有快照能力不得声称历史索引可恢复。

## VII. 开源复用与薄控制层

优先成熟、维护状态明确、许可适合的组件。主流程度用可核查信号判断，不用 Stars 代替质量。不自研通用队列、Agent 框架、向量库或低代码平台；仅自研支持任务、证据裁决、能力策略和领域适配。新增中间件须说明现有组件无法解决的具体问题。

## VIII. Contract 与依赖隔离

Channel、Knowledge、Model、Tool、Policy 经稳定契约；Provider 私有类型不得进入 domain/公共接口。域模型不依赖 LangGraph/FastAPI/SDK/数据库。Runtime、Workflow、Provider 经端口与 composition root 装配，遵循 docs/architecture/DEPENDENCY-RULES.md。替换 Provider 通过能力测试，不假定厂商能力等价。

## IX. 数据范围与外发

所有 Case、证据、缓存、报告、恢复动作按客户/项目权限隔离。公网检索、模型、embedding/rerank、工具、遥测都在外发前做数据策略。秘密不进仓库、prompt、checkpoint、队列或普通日志。MCP annotation、Skill allowed-tools、检索内容和用户转发材料不能授予权限。

## X. 可观测与证据化完成

关联 task_id、run_id、turn_id、operation_id、trace_id、版本、耗时、重试、证据和结果。记录必要的决策摘要，不要求或保存模型隐藏思维链。usage/cost 不可用则明确标记，不伪造 0。未运行的测试、部署、真实连接不得报告成功。

## 开发与 Git 治理

- 使用标准 Git；允许标准 linked worktree 的 .git 文件，禁止自造 .git-data 替代。
- 开始变更检查 git status；保护用户未提交内容，保留可回退基线。
- 每 Feature 一个 feature/<number>-<slug> 分支，禁止 main 直接开发。
- Spec Kit 生成的技能/脚本不手工改写；规格通过官方命令创建。
- 设计修订允许文档、ADR 及必要治理配置；不得由“同意架构”推断业务实现授权。
- 不使用未授权的 destructive reset/clean/force-push。
- V1 必须有真实 KB、模型、钉钉和只读能力闭环；Fake 仅用于测试里程碑。

## 变更规则

宪法变更必须说明来源、影响、对应 ADR/需求与迁移，同步 AGENTS、Architecture、Workflow、Contracts 和门禁；破坏性范围提高主版本，兼容增补提高次版本，澄清提高补丁版本。遵守当次用户明确授权，不虚构已批准状态。

本次同步：替换空模板；落实只读、持久任务、配置能力、真实 V1、开源复用和外发边界。未开放 Coding Gate。后续实施状态见 docs/governance/DEVELOPMENT-GATES.md。
