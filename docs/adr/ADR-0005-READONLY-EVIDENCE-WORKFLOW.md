# ADR-0005：只读能力、动态证据与配置工作流

日期：2026-09-05；状态：纳入本轮授权设计基线，待实现。

## 背景

Q3A 禁止自动生产写；Q5B 要动态证据裁决；Q7 用户纠正为多能力、可设置工作流与优先级，Q8B 选择配置驱动。

## 决策

Workflow 控制阶段和终止，模型在获准能力中择下一步。默认内部知识优先，按所缺事实升级官方检索/API/MCP，无法推进时持久请求人工。模型通用推理贯穿，不强制 S1–S4 分类。

目标 WRITE/UNKNOWN 始终 DENY；MCP/Skill 不能授予权限。人工协助用于补证据和工程师接手，删除批准后自动生产写路径。本系统自身任务持久化/报告/授权通知单独声明 system_effect。

证据按具体命题、版本、时间与来源裁决；不以相似度或“现场绝对优先”代替。外发与客户权限检查发生在模型/工具/观测前。

## 后果

需版本化配置、严格 Schema、固定能力标识、命题支持关系与测试集。不能只靠提示词实现安全，也不追求 V1 通用低代码编辑器。

详细规则：[Workflow](../architecture/WORKFLOW-MODEL.md)、[Plugin Contract](../architecture/PLUGIN-CONTRACT.md)、[Knowledge Contract](../architecture/KNOWLEDGE-CONTRACT.md)。
