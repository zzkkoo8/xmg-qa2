# ADR-0007：双面板、便捷分发与展示扩展

日期：2026-09-05；状态：本轮授权形成的设计基线，待实现。补充 ADR-0006；替代“V1 只有简易 Web 任务页”的范围。

## 背景与决定

用户要求 Chat/Admin Web、开发机开发与便捷部署，以及插件/工作流/HTML/MD 个性化。采用统一 React/TypeScript/Vite/Tailwind/shadcn SPA；assistant-ui 负责聊天组件，自有 Task API 负责状态。选择性复用 FastAPI 全栈模板和 shadcn-admin，保持原后端和 SQLAlchemy 模型。

为独立安装提供基于成熟认证组件的最小本地账户，组织网关/OIDC 可选；应用账户管理不扩张为通用身份平台。后端角色与 Case 数据授权独立，Admin 也不能放宽客户目标只读边界。

采用预构建 OCI 镜像 + Compose 在线/离线包；开发从第一 Feature 即建设基础打包，升级/回退/离线验证归发布验收。模板采用版本化 TemplateProvider 与受限 Jinja 渲染/HTML 清洗；品牌配置和安全信息页面可热更新，交互 React 页面仍须构建发布。

## 替代与后果

不整体替换为成品聊天平台，不叠加第二后端/会话库，也不为内部控制台引入无明确收益的 SSR。完整 React-admin 保留为未来 CRUD 密集场景候选。新增模板/控制面/交付测试，按 003–008 建议阶段拆分；没有因此通过运行时 Spec Kit 门禁或触发实现。

依据：[本轮研究](../research/2026-09-05-WEB-DELIVERY-AUDIT.md)。规范入口：[Web](../architecture/WEB-CONSOLE.md)、[交付](../architecture/DISTRIBUTION-DEPLOYMENT.md)、[模板](../architecture/PRESENTATION-CONTRACT.md)、[编码交接](../plans/IMPLEMENTATION-READINESS.md)。
