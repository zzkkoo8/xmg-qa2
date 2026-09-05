# Plugin / Capability / Policy Contract

版本：1.0；日期：2026-09-05。

## 1. 边界

运行能力插件类型保持 channel、knowledge、model、tool、policy。Registry 是薄注册与适配层，负责能力发现、版本、健康和选择，不重建包管理器或任意代码市场。Workflow 配置单独由 Runtime 发布，Skill 是受审查的说明/资源包，不是拥有独立权限的第六个万能执行器。展示层另有 TemplateProvider 与构建期 UI 扩展清单，见 [Presentation Contract](PRESENTATION-CONTRACT.md)，二者不通过 Tool 获取执行权限。

## 2. Manifest 与调用

| 字段 | 要求 |
| --- | --- |
| plugin_id / version / contract_version | 稳定名称、语义版本；启动时检查兼容，不支持则失败 |
| capability_id / provider_id | 内部唯一命名，如 vendor.product.read_status；不能只用 MCP server 自报 name |
| input_schema / output_schema / config_schema | Pydantic/JSON Schema，拒绝额外危险参数 |
| target_effect | READ_ONLY、WRITE、UNKNOWN；目标系统 WRITE/UNKNOWN 在 V1 一律 DENY |
| system_effect | 本系统任务存储、报告生成、授权通知分别声明 |
| allowed_targets / allowed_operations | 由管理员配置的设备、API 路径、固定命令模板；不接受模型提供任意 URL |
| required_scopes / credentials_ref / egress_profile | 最小权限、秘密引用和数据外发等级 |
| timeout / output_limit / concurrency / retries | 单次调用和总任务限制；不可由模型扩大 |
| provenance / checksum / review_status | 插件/Skill 来源和审核状态；动态下载不自动激活 |
| idempotency / cancellation / health | 声明真实语义，不宣称底层不支持的功能 |

调用携带 task_id、run_id、operation_id、expected_epoch、principal_scope、deadline、trace_id。执行器返回标准结果、Evidence 引用或稳定错误；私有 SDK 对象不能泄漏到 Workflow。

## 3. 生命周期与依赖装配

discover → schema/version validation → initialize → ready → invoke → health → shutdown。初始化失败隔离；运行中 Provider 故障不影响其他无关插件。应用 composition root 唯一选择具体实现并注入 Contract，Workflow 不出现按 Dify/厂商字符串分支的业务代码。

普通内部 Adapter 随应用构建、固定依赖版本；不可信或有系统执行能力的插件必须独立进程/容器。V1 不承诺热安装任意外部 Python 包。

Admin 可启停已审核能力、编辑连接配置和健康测试；新增插件代码需合约测试与重新构建。发布保持兼容版本/hash，进行中 Case 固定语义版本；但当前 ACL/凭证撤销/能力禁用每次调用重新生效。更换表单布局、HTML/MD 模板不修改 Core；新增节点/API/业务规则仍需 Feature，禁止把“可扩展”宣传为所有功能都零代码。

## 4. MCP 与 Skill

MCP 只读 annotations 是提示，不能代替服务端权限审计；接口同名也不代表同一可信工具。官方规范明确 annotations 不能自动视为可信。[MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)

采用官方 MCP Python SDK，实施时锁定与服务端协商后的协议/SDK 组合。鉴权、目标 allowlist、超时、结果长度、重定向和 SSRF 防护均属于本系统边界。安全通道失败不得回退到不受控 shell。

Skill 包按需加载 SKILL.md/references；脚本执行仍经过相同 Policy。allowed-tools 不是安全沙箱，也不能授予原本没有的权限。[Agent Skills 规范](https://agentskills.io/specification)

## 5. 只读执行的硬规则

- 不注册目标修改、重启、安装、升级、删除或防火墙变更能力；建议命令可交工程师独立评估，永不进入自动执行队列。
- 未知工具、任意 shell、任意 HTTP 方法/地址、未审核临时脚本默认拒绝。
- 使用只读账户、API scopes、固定模板和参数校验共同限制；只检查 GET/命令名称不足以证明安全。
- 抓包和探测有资源/隐私影响，须指定目标、过滤、时间、包数/字节上限；不默认抓全流量。
- 本地验证只在独立测试环境处理必要副本，不挂生产凭证、宿主 Docker socket 或生产目录。通过本地测试不提升生产执行权限。
- 外部内容不能注入配置；不因文档写“忽略规则”“改用此 token”改变动作。

## 6. Model Contract

request/response 支持结构化结果、工具描述与调用、流式能力、usage/cost、超时/取消和错误分类。能力探测明确 structured_output、tool_calling、context_limit、streaming、usage_support。

Token/cost 未返回时标记 unavailable/estimated，不能写 0。Fallback 只能去已授权模型与数据区域；不因内容安全拒绝自动轮换模型规避。优先官方 SDK；多厂商路由与集中配额有需求时启用 LiteLLM。

## 7. Policy Contract 与数据外发

Policy 的权威输入为身份/任务范围、组织配置、目标和能力实际风险；模型提供的 policy_result 不可信。输出 allow/deny/need_context 和 reason，不提供“批准生产写”状态。

所有搜索、模型、embedding、rerank、工具、trace 均在发送前决定 allowed_data、redaction、destination；无法可靠脱敏时保留本地分析或求助，不能带原始日志外发后再遮蔽。秘密只由执行器在最后边界解析，禁止写入 prompt、checkpoint、broker payload 或公开仓库。

## 8. 契约验收

每个插件验证：初始化、版本兼容、schema、权限、超时、取消、错误映射、秘密不泄露、资源释放。目标只读工具另测拒绝变更和超范围参数；模型另测结构化输出与失败回退不突破数据边界；渠道另测身份映射、重复投递和通知回执。
