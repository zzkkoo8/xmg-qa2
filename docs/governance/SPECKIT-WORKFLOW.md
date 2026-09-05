# Spec Kit 工作流

## 1. 唯一路径

constitution → specify → clarify → plan → checklist → tasks → analyze → 明确编码授权 → implement → converge。

规格通过仓库已有官方 Spec Kit skills/脚本生成；不手工伪造 Feature 产物，不重新初始化现有仓库，不重写 vendored skills 和脚本。需求与设计可以先行，但不能代替运行时 Feature 的完整门禁。

## 2. 本轮需求输入

读取[需求基线](../requirements/REQUIREMENTS-BASELINE.md)、[架构](../architecture/ARCHITECTURE-BASELINE.md)、相关 Contracts/ADR 和[交付路线](../plans/V1-DELIVERY-PLAN.md)。Q1–9 已确认，余项由用户授权采用文档默认方案；不要再次逐题访谈。

V1 为真实业务闭环。首个运行时 Feature 可以用 Fake 验证状态与恢复，但后续真实 KB/模型、只读能力、钉钉/Web 和联合验收均属于 V1 内部里程碑。

## 3. 分支

一项 Feature 一个 feature/<number>-<slug> 分支；编号在创建时检查远端、已有分支和 specs。现有 Git extension 的 branch_template 固定为 feature/{number}-{slug}，branch_prefix 留空，避免双前缀。使用 before_specify → speckit.git.feature 挂钩，不在 main 创建业务变更。

本轮 feature/002-support-agent-baseline 是架构/治理文档修订，未创建或伪称运行时 spec。003 起的实现编号只是路线图建议。

## 4. 各步骤要解决什么

| 步骤 | 关键产物/检查 |
| --- | --- |
| Constitution | 当前项目原则；需求来源、只读边界、持久任务、开源复用和证据要求 |
| Specify | 一项可交付 Feature；用户场景、FR/NFR、验收、非目标 |
| Clarify | 仅解决真实缺口；权限、持久化、外部接入、通知和恢复语义不可含糊 |
| Plan | 包/镜像版本、接口、数据迁移、模块、错误、测试、SLO、回退 |
| Checklist | 架构、安全、Evidence、恢复、观测、测试、运维 |
| Tasks | 依赖顺序明确、可独立验证的小任务 |
| Analyze | Spec/Plan/Tasks/Constitution 一致性；0 Critical/0 High |
| Human Gate | 展示具体产物和验证结果后，由用户明确批准当前 Feature 编码 |
| Implement | 按 Task 实现，变更与证据一并记录 |
| Converge | Spec/Plan/Tasks/Code/Tests 对照；不可只改文档掩盖代码偏差 |

## 5. 验证边界

脚本 paths-only 或 branch dry-run 成功只证明路径/分支命名，不证明 Analyze 或业务测试通过。Fake 测试只证明受测边界，真实 Provider 合同与 E2E 仍需独立记录。

长任务的失败、卡顿、人工补充与跨天恢复是 V1 验收必需项；不以普通同步聊天 E2E 代替。
