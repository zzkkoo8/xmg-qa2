# Chat 与 Admin 控制台

版本：1.0；日期：2026-09-05；状态：待实现设计。来源：用户本轮明确要求 Chat/Admin 双面板；替代原“简易 Web 任务页”范围。

## 1. 技术选择

采用一个 React + TypeScript + Vite SPA，路由分为 `/chat` 与 `/admin`，共同消费现有 FastAPI。Tailwind CSS + shadcn/ui 统一样式；TanStack Router/Query 处理路由与服务端数据；React Hook Form + Zod 处理编辑表单。服务端验证和权限始终有效，前端 Schema 不替代它们。

聊天优先采用 assistant-ui 的组件和 ExternalStoreRuntime，由应用 Adapter 把 SupportTask 快照与事件映射到消息、证据、调查状态和人工待办。Admin 用相同 shadcn 组件实现必要列表/表单，可参考 satnaing/shadcn-admin 的布局。技术依据与替代方案见[本轮选型补充](../research/2026-09-05-WEB-DELIVERY-AUDIT.md)。

“AI 最擅长”没有可核查的通用排名。此处选择依据是类型明确、公开组件/范例丰富、可生成 API 客户端、能复用 Python 后端和静态打包；实际开发效率仍需在本仓库验证。

复用 FastAPI 官方全栈模板的前端布局、客户端生成、测试和构建做法，逐项记录来源 commit/许可；不重新生成覆盖仓库，不引入第二套 SQLModel 业务模型、用户库、Agent 或部署中枢。既有 SQLAlchemy/Alembic 与 Contract 保留。assistant-ui 安装到现有 Vite 工程，不使用默认创建 Next.js 新项目的入口；不启用 Assistant Cloud。

## 2. 页面与最小功能

| 区域 | V1 功能 | 数据与动作 |
| --- | --- | --- |
| Chat 侧栏 | 新问题、任务列表、搜索/状态筛选 | 只展示当前身份可访问 Case；保留 task_id，不以标题关联 |
| Chat 主面板 | 多轮消息、流式草稿、附件、错误重试提示 | 输入持久接收后显示已接收；草稿明确未完成验证 |
| 调查详情 | 证据引用、已知事实/假设、当前步骤、等待原因 | 展示决策摘要，不索取或暴露隐藏思维链 |
| 人工待办 | 已回传/缺失项、补充、恢复、取消、关闭 | 使用 request_id、expected_state_version、幂等键 |
| 报告 | 版本列表、MD/HTML 预览与下载 | 最终核验后发布；下载重新校验 Case ACL |
| Admin 概览 | Provider 健康、队列、运行/等待数、错误、用量 | 不显示原始秘密，指标不可用时明确标注 |
| Admin 连接与能力 | KB/模型/钉钉/API/MCP 配置、健康测试、启停 | 配置自有系统；仅启用审核过的插件，秘密只写不回显 |
| Admin 工作流 | 产品配置、优先级、条件、限额、差异、验证、发布/回退 | 表单 + YAML/JSON 编辑；V1 不做拖拽图编辑器 |
| Admin 模板与主题 | 模板编辑、样例预览、版本发布/回退；名称、Logo、主题色 | 规则见 Presentation Contract；不执行上传 JS/Python |
| Admin 权限与审计 | 本地账号、principal/角色/客户项目映射、变更与失败记录 | 管理应用账号与权限，不建设通用身份平台；系统管理员不自动读取所有 Case |

中文默认、响应式布局、键盘可操作、深浅主题；桌面优先，手机可查看任务、补充和恢复。屏幕不能只显示转圈，等待和失败必须说明下一步。

## 3. 身份与控制面权限

为便于独立安装，V1 默认提供最小本地登录：借鉴 FastAPI 官方模板认证结构，使用 pwdlib/Argon2 与 PyJWT，账号和可撤销会话记录放现有 PostgreSQL；不开发密码算法或单独身份服务。安装时通过受保护初始化流程创建首个管理员，无默认通用密码，关闭公开注册；密码重置先通过主机管理员 CLI，避免强制配置 SMTP。现有组织可切换可信身份网关/OIDC 适配器，启用前固定版本与身份映射，不静默关联同名账号。[FastAPI 认证组件依据](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

浏览器 JWT 放短效 HttpOnly cookie，服务端每请求校验固定算法、签发者、受众、过期时间以及对应 session_id 是否有效；禁用账号/改密/退出撤销会话。绝对与闲置期限在 Feature Plan 固定，角色/Case 权限以服务端当前数据为准。开发身份模拟仅在显式 dev profile，发布配置检测到模拟身份即启动失败。只有 localhost 绑定的无真实数据开发环境可用该模式。

若启用网关身份，网关剥离客户端伪造身份头，再通过受保护后端链路传递已验证 principal；API 不能同时暴露绕过网关的公网端口。本地认证模式忽略外部身份头。浏览器采用同源会话；HTTPS 下 cookie 使用 Secure/SameSite，登录及所有写请求校验 CSRF/Origin，登录限流与通用失败提示防枚举；不在 localStorage 或 URL 保存长期 token/Provider Key。生产登录需 HTTPS；无域名时支持组织证书/受信内网 TLS，不为便捷跳过传输保护。

| 角色 | 自有系统权限 | Case 数据范围 |
| --- | --- | --- |
| viewer | 查看消息、证据和报告 | 显式获准的 Case |
| engineer | 创建/补充/恢复/取消/确认关闭 | 显式获准的客户/项目 |
| admin | 配置、发布、角色映射与系统审计 | 仍须独立 Case 数据授权；提权映射有审计 |

所有 `/v1/admin/*` 请求在后端校验角色/范围、资源版本和审计。配置变更属于 system_effect；任何 admin 操作都不能取消客户目标 WRITE/UNKNOWN=DENY。

## 4. API、事件与一致性

- `/v1/tasks/*` 沿用任务模型；新增 `/v1/admin/providers`、`capabilities`、`workflows`、`templates`、`identity-mappings`、`audit-events` 资源族，具体 OpenAPI 在对应 Feature 冻结。
- 编辑采用 draft → validate → publish；发布需 expected_version，生成不可变版本/hash，记录操作者、差异和结果。冲突返回 409，未保存表单不得被后台刷新静默覆盖。
- Case 固定 workflow/config/template 版本；新发布用于新任务，已有任务必须显式迁移。权限撤销、凭证撤销、能力禁用等收紧措施在每次动作前按当前 Policy 生效，不能被旧版本固定绕过。
- 前端通过 OpenAPI 生成 TypeScript 客户端，领域 API 不暴露 LangGraph 私有对象。后台表单可按已注册 schema 渲染；未知 UI 控件不动态加载执行代码。
- 初次加载先取 Case/消息快照和 sequence，再订阅 SSE；事件携带 event_id/sequence/task_id/run_id，重连带 cursor/Last-Event-ID，去重且检测缺口。游标过期重新取快照，不重新创建任务。轮询快照作为降级，不作为模型重跑请求。
- SSE 建连、每次事件发送（包括重放）前复验当前会话有效性、token 到期和 Case ACL；空闲连接按有界心跳周期复验，失效立即断流，不再发送业务数据。撤销后重连必须重新鉴权。
- SSE 关闭只停止当前页面订阅；明确点击取消才调用任务取消 API。浏览器不能直接调用模型、Dify 或目标 MCP，刷新页面不能重复执行工具。
- 流式 token 属临时草稿，最终答案经引用/ACL/模板验证后才产生 published_result 事件；失败/取消时草稿不冒充最终报告。assistant-ui 的重生成、编辑分支、approve-tool 等入口默认关闭，只有映射到获准 Case 操作后才开放。

## 5. 工程与验收

目标目录 `web/src/{app,features/chat,features/admin,components/ui,lib/api,lib/task-stream}`；后端仍为 `src/xmg_qa2`。Node/pnpm 仅用于开发和构建，发布时 `web/dist` 随应用镜像由 API 提供，`/v1` 不被 SPA fallback 吞掉；带 hash 静态资源缓存，index.html 可及时更新。当前这些是目标路径，不是已存在文件。

首个 Feature 固定 React/Vite/shadcn 底层 primitive/assistant-ui 的兼容版本、pnpm lock、Node 引擎和生成客户端方案，禁止混用两个 primitive 家族的不可兼容代码。验证 `tsc`、构建、必要 Vitest/Testing Library 和 Playwright：

1. 真实任务刷新/重连/部分补充/跨天恢复，消息与 task_id 不丢且不重复调度。
2. viewer 直接调用 admin API、跨客户 URL/附件/报告、CSRF 和过期会话均被拒绝；订阅中退出、token 到期或撤销 Case 权限后不再收到业务事件，重放也不能绕过。
3. 配置发布冲突、回退、禁用能力、秘密掩码、审计与新旧 Case 版本行为正确。
4. HTML/Markdown 恶意内容、取消后草稿、状态错误提示、手机补充与键盘操作符合约定。
5. 开发 HMR 与发布静态资源使用相同 API 契约；生产服务器无 Node/npm 也可使用双面板。
