# 编码就绪判断与开发机 Codex 交接

日期：2026-09-05。结论：产品级设计已补齐，可以让开发机 Codex 开始第一 Feature 的规格、版本验证和实现准备；当前还不能报告“全部实施门禁通过”。本轮用户要求审阅方案后推送，不把这一问题自动等同于授权所有 Feature 编码/部署。

## 1. 当前就绪矩阵

| 项目 | 当前证据 | 判断/下一动作 |
| --- | --- | --- |
| 需求与主要架构 | 需求 1.2、问答核心/评测、Web/分发/模板契约、ADR-0008 | 设计可交接，无需重新访谈 Q1–9 |
| 插件/工作流/HTML/MD 个性化 | 已定义能力与 UI/模板边界、版本发布和验收 | 待对应 Feature 实现，不是现成可用功能 |
| 第一 Feature spec/plan/checklist/tasks/analyze | `specs/` 当前仅说明，尚未生成运行时产物 | 开发机通过已安装 Spec Kit skills 完成，不能用本文件冒充 |
| 构建版本与工具 | 没有锁文件或已验证 Dockerfile/Compose | 开发机检测实际环境，验证 Python/Node/包/数据库/checkpointer 组合后锁定 |
| 第一 Feature 编码授权 | 本轮仅设计修订；下方是可发送的授权文本 | 用户把执行文本发给开发机后，按其明确范围及门禁实施 |
| 真实接入资料 | Dify/模型/钉钉/产品端点未在此会话验证 | 只阻塞相应集成；不阻塞持久任务、UI 壳和合约测试 |
| 发布包 | 尚无 OCI/在线/离线成品 | 先建立构建管线，最终 Feature 实测后交付 |

这里的差距是实现准备与验证，不需要再做一轮无边界全局架构重写。首个 Feature 完成也不能宣称整体 V1 已完成。

## 2. 第一 Feature 的具体范围

建议短名 `support-foundation`；编号由 Spec Kit 检查现有远端/规格后分配，不硬编码 003。基于已审查设计分支或其已合并的 main，新建独立运行时 Feature 分支，禁止在设计分支写业务实现。

- 验证并锁定 Python 3.12 候选、Node LTS/pnpm、React/Vite、FastAPI/Pydantic、PG/SQLAlchemy/psycopg、LangGraph/checkpointer 与 Celery/RabbitMQ 的可用组合。
- 创建最小可运行包、OpenAPI、开发 Compose、基础 Dockerfile/CI；沿已存在目录落实文件，不再做空目录工程。
- 建立 QuestionFrame/AnswerDraft/AnswerCheck 与显式路由/缺口/停止规则，至少 20 个合成控制场景和评测结果 Schema；具体语义以 QA Core 为准，不能用 Fake 证明答案质量。
- 实现 SupportTask/Run/HumanRequest/ResumeAttempt、持久中断/定向恢复、幂等与关键崩溃窗口。
- 建立同一 React SPA 的 Chat/Admin 路由壳、本地登录/角色与 Case 权限、任务输入/状态展示；本阶段不实现全部配置与模板编辑器。
- Fake Knowledge/Model/Tool 仅用于可重复测试；PG/checkpointer/broker 必须是真实进程。提供 API 创建 → 等待 → 重启 → 回传 → 恢复 的可运行演示。

具体表结构、OpenAPI、源码任务与安装版本由该 Feature Plan 冻结；调用失败时优先查兼容错误，不无限更换组件。确需改变核心选择则追加 ADR 并同步规格。

## 3. 发给开发机 Codex 的执行提示词

下面的文字由用户发送后才形成对应执行授权；当前保存文档不会自行启动编码，也不授权后续全部 Feature。

```text
在现有 /data/dev/xmg-qa2 开发机仓库继续工作（目录不存在则定位现有克隆，不覆盖或重新初始化）。我授权你完成第一个 support-foundation Feature 的开发环境组件搭建、代码实现和测试；仅限开发/测试环境，不接管客户生产机、不执行生产写、不合并 main 或部署正式环境。

先检查 git status/远端，保护未提交内容，读取 AGENTS.md、Constitution、需求基线及 IMPLEMENTATION-READINESS.md。同步 feature/002-support-agent-baseline 最新设计；如果已合并，则用包含同等设计的 main；保留本地独有提交，禁止强制覆盖。通过仓库官方 Spec Kit skills 创建独立 Feature 分支及规格；按 specify→clarify→plan→checklist→tasks→analyze 完成门禁，复用已定决策，只询问实质阻塞。允许你完成这些准备，Analyze 无 Critical/High、Checklist 无阻塞后，当前 Feature 无需再次索要相同编码授权，直接 implement。

范围按该文档第2节：问答理解/路由/答案检查骨架、20 个合成控制场景与评测结构、锁定并验证版本、持久任务/恢复、真实 PG/checkpointer/broker、React Chat/Admin 壳及最小本地认证/权限、开发 Compose/镜像/CI。优先成熟开源，复用组件但不整仓覆盖或引入第二套 Agent/数据库业务模型。测试覆盖问答路径/最小澄清/无进展以及恢复幂等、权限与实际进程故障；Fake 仅用于外部 Provider 测试。模型/KB等真实资料缺失只阻塞相关集成，不阻塞独立工作；若替换包源/模型，保持秘密和数据授权范围。

安装仅限项目虚拟环境、容器和明确缺少的开发依赖；不得覆盖其他项目的 Node/npm、升级共享 Docker 或擅改主机网络。遇环境/权限阻塞保存状态、说明证据及最小协助要求。完成后执行 converge、独立只读复核、相关测试，提交推送 Feature 分支和 PR，返回变更、验证、启动方法与剩余阻塞，不伪报 V1 已发布。
```

首个 Feature 交付问答控制骨架，下一真实 KB/模型 Feature 必须交付[答案质量基线](../governance/ANSWER-QUALITY.md)，再扩展自主取证；不将完整 Admin/模板编辑器放到核心问答质量之前。

## 4. 后续资料与停止点

真实接入需：Dify 地址/安装版本/授权 dataset、模型 endpoint/能力及数据范围、钉钉应用与收件映射、至少一种产品只读 API/MCP、脱敏测试题集。秘密仅从开发机既有配置/秘密引用取用，不要求写入公开仓库或聊天记录。

最终发布需：目标 OS/CPU、Docker/Compose、身份模式/管理员初始化、TLS、加密持久存储、镜像渠道及备份目标。每个 Feature 完成独立验收；上一阶段可用不能替代这些接入/发布条件。
