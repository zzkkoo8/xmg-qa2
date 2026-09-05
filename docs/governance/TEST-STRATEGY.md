# 测试与评测策略

## 1. 先验证风险和边界

| 层 | 核心场景 | 证据 |
| --- | --- | --- |
| Unit | 状态转移、ACL、预算、命题类别、错误分类、模型动作 Schema | 不连外部系统的确定性测试 |
| Contract | Fake 与真实 Adapter 同约束；知识 scope、模型能力、工具权限、渠道回执 | 同一合约测试套件，可标记实际 Provider 限制 |
| Workflow | 内部优先、证据不足升级、冲突、无进展、取消、人工请求 | 节点/状态/事件与下一步判断 |
| Integration | PG/checkpointer/Celery/broker；发布与恢复崩溃窗口 | 实际进程重启/消息重投、唯一键和事件记录 |
| E2E | 钉钉 + 真实 KB/模型/只读能力 + 人工补充 + Web/报告 | 完整 task_id 链路；不能只用 TestProvider |
| Evaluation | 产品/通用/版本/多问题/现场/资料不足与动作轨迹 | 正确性、覆盖、证据支持、可行动、求助精确率/召回率；详见[问答质量](ANSWER-QUALITY.md) |
| Operations | Compose、迁移、备份恢复、升级/旧图回退 | 可复现运行命令、环境版本、输出与失败说明 |
| Web/Control Plane | Chat 事件重连、Admin 发布、登录/会话/角色/Case 权限 | TypeScript 构建、必要组件测试与 Playwright/API 越权测试 |
| Presentation | 模板版本、HTML/MD 清洗、必需输出、资源上限 | 恶意输入与跨客户样例、隔离失败与降级记录 |
| Distribution | 在线/离线包、全依赖镜像、平台、无开发工具安装 | 干净 Linux、断开 registry/npm/PyPI、重复安装和 schema 回退测试 |

## 2. 必须覆盖的故障

401/403、429、5xx、网络不可达、非法 Schema、空知识、冲突证据、恶意文档指令、敏感外发、同案双 Worker、重复入站/出站/恢复、Worker 强杀、图/业务双写间隙、旧图版本、通知回执丢失、部分人类回传、取消中的工具请求、资源上限与无进展循环。

集成测试必须验证 checkpoint 写入也受有效执行者约束，不能只验证业务表租约。禁止声称外部副作用 exactly-once。

人工恢复需故障注入覆盖 ResumeAttempt 接收后/图消费后/业务回执前，并推进到第二个 interrupt 再重复投递旧回复：验证定向恢复、消费对账与不确定状态暂停，旧回复不得满足新的等待条件。

## 3. 测量口径

以[需求基线](../requirements/REQUIREMENTS-BASELINE.md)第 5 节和[联合验收](../plans/V1-DELIVERY-PLAN.md)为准；所有数值为待测目标。记录硬件、依赖版本、样本数、并发、p50/p95、失败率、provider 时延与费用，不用纯 Fake 结果推算生产性能。

首个 Feature 建合成控制场景，真实 KB/模型 Feature 即交付质量基线，不等最终发布才评答案。不少于 100 个独立冻结人工标注案例，开发集另计；确定性安全和数据隔离场景零失败。引用覆盖不等于引用正确；Ragas/LLM 评分辅助人工复核，不单独决定上线。

## 4. 本轮文档变更的验证

本轮仅验证 Markdown 结构/本地链接、YAML 示例和 Git 配置、分支命名 dry-run、需求/权限/状态/引用的一致性及 git diff。没有运行代码时不创建镜像实现的空测试，不报告 Unit/E2E/部署已通过。

每个实现 Feature 只运行必要相关测试及规定门禁；发现具体风险再扩大范围，避免无意义重复测试。
