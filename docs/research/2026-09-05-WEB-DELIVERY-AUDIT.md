# Web、分发与扩展审计补充

日期：2026-09-05。基于设计提交 7ec2e205，回答用户本轮五项问题；补充而不重跑上一轮 21 项组件调查。下列能力事实来自官方资料，适合本项目与否属于工程判断；没有实际构建/部署证明。

## 1. 审计结论

| 用户问题 | 原方案缺口 | 本轮决定 |
| --- | --- | --- |
| Chat/Admin Web | 只有简易任务页，未定义 Admin | 统一 React/TS/Vite + Tailwind/shadcn，聊天复用 assistant-ui；Admin 提供连接、能力、工作流、模板、权限与审计 |
| 开发/打包/分发/部署 | 只有 Compose 方向，无发布包/离线和升级协议 | 一份源码、构建镜像；在线配置包与每平台离线包；开发工具不进入部署前置条件 |
| 插件/工作流/个性化 | Provider 可插拔，但页面与模板未形成 Contract | 配置、代码插件、UI 扩展、模板分层；版本化发布，保持只读及数据权限 |
| 能否开始编码 | 无运行时 spec/plan/tasks、锁文件或验证环境 | 产品级方案补齐，可交开发机 Codex启动第一 Feature；正式编码前须完成该 Feature 的规定门禁 |
| 再次推送 | 上轮 PR 尚未合并 | 沿同一设计分支更新 PR；不直接改 main，不将草稿合并视为已授权 |

## 2. Web 三条路线

| 路线 | 优点 | 本项目代价 | 决定 |
| --- | --- | --- | --- |
| 统一 React SPA + 可复用聊天/Admin 组件 | 保持现有后端；静态交付；Task/ACL/UI 完全可控 | 需编写事件 Adapter、业务表单和权限交互 | 采用 |
| 完整引入 FastAPI 全栈模板或 React-admin | 登录、CRUD、客户端、测试已有范式 | 整套模板会引入另一套数据/账户/部署选择；React-admin 自有 dataProvider/authProvider 与 UI 体系需整合 | 选择性复用工程结构，保留其作为 CRUD 密集阶段候选 |
| Open WebUI 等成品聊天平台作主 UI | 普通模型聊天可快速使用 | 仍须适配 Case/人工恢复/Admin 工作流；新会话/权限/工具入口可能重复；品牌许可需核验 | 可做演示或单独入口，不作为本项目的默认产品壳 |

不以“AI 天生更会某个框架”或 Stars 宣称最佳。React SPA 的推荐来自当前 Python 后端、内部控制台、类型化接口、复用组件和无需 SSR 的需求。Next.js 也可实现，但此时没有额外框架功能收益足以支持更换既有 Vite 方向。

## 3. 可核查的组件依据

| 官方来源 | 本轮核验事实与使用方式 |
| --- | --- |
| [FastAPI 全栈模板](https://github.com/fastapi/full-stack-fastapi-template) / [官方介绍](https://fastapi.tiangolo.com/project-generation/) | React、TypeScript、Vite、Tailwind、shadcn、生成客户端、Playwright、Compose；源码 MIT。借用布局/工程范式，不覆盖现有领域模型 |
| [assistant-ui](https://github.com/assistant-ui/assistant-ui) / [ExternalStoreRuntime](https://www.assistant-ui.com/docs/runtimes/custom/external-store) | React/TS 聊天组件与自有状态 Adapter，MIT；Cloud 可选。只用本地组件，自有 Case 仍是唯一业务状态；Vite 项目不照抄 Next 新建命令 |
| [shadcn-admin](https://github.com/satnaing/shadcn-admin) | MIT 的 Vite/TanStack Admin UI；作者明确不是完整 starter/template。复用样式和布局不等于获得后台 API/RBAC |
| [React-admin](https://github.com/marmelab/react-admin) / [文档](https://marmelab.com/react-admin/Readme.html) | MIT 前端框架、dataProvider/authProvider 模型；只作为替代，不叠加到默认 shadcn 表单上形成双套 UI |
| [Open WebUI 许可](https://docs.openwebui.com/license/) / [仓库](https://github.com/open-webui/open-webui) | 当前存在品牌条款与特定例外，不能视为任意规模都可自由去品牌；本项目也没有因品牌定制另建聊天后端的必要 |
| [FastAPI 认证](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) | 官方使用 pwdlib/Argon2 与 PyJWT。本项目增加 HttpOnly cookie、会话撤销和 CSRF 等应用约束，不能把教学样例当完整安全验收 |

未采集新的 Stars 排名：这次问题需要判断双面板/部署适配，排行榜不会验证 Case API 或模板隔离。版本不写浮动 latest；实施时固定组件和复制源码 commit，保留 LICENSE/NOTICE。

## 4. 交付与模板依据

Docker 官方确认 Compose 可用于生产并采用环境覆盖；Buildx 多平台能力不等于依赖全部跨平台；save/load 可用于离线搬运镜像，包内仍要列全服务。GHCR 的容器包有独立可见性，公开容器可匿名拉取。这些支持“预构建镜像 + 配置/离线包”的决定，但不证明本项目已可一键安装。[Compose](https://docs.docker.com/compose/how-tos/production/)、[多平台](https://docs.docker.com/build/building/multi-platform/)、[save](https://docs.docker.com/reference/cli/docker/image/save/)、[load](https://docs.docker.com/reference/cli/docker/image/load/)、[GHCR](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)

Jinja 官方指出沙箱不能独自解决资源耗尽，HTML 还需后处理。采用受限模板语法、独立受限进程、nh3 清洗及浏览器 sandbox/CSP；Markdown 默认不执行原生 HTML。此处是根据官方边界形成的组合设计，必须单独验收。[Jinja](https://jinja.palletsprojects.com/en/stable/sandbox/)、[nh3](https://nh3.readthedocs.io/)、[react-markdown](https://github.com/remarkjs/react-markdown)、[iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe)

## 5. 完成范围与剩余验证

已搜索并读取相关官方项目/文档，补齐 [Web](../architecture/WEB-CONSOLE.md)、[分发部署](../architecture/DISTRIBUTION-DEPLOYMENT.md)、[模板契约](../architecture/PRESENTATION-CONTRACT.md)，与原需求/架构/交付路线统一。没有安装成品 UI、构建容器、生成 Release、上机登录客户设备或执行业务测试。

剩余验证明确落入 [编码就绪与交接](../plans/IMPLEMENTATION-READINESS.md)：第一 Feature 的版本/Spec Kit/开发环境，后续真实 KB、模型、钉钉/API 与发布平台。继续泛搜不能替代这些实测，故停止扩散候选。

## 文档验证记录

本轮仅更新设计与治理 Markdown。独立只读复核发现的备份对象完整性/写入冻结顺序和 SSE 存续期间撤权语义已补齐；链接、代码围栏、YAML 示例和 diff 空白检查通过。未执行业务测试、安装、镜像构建或部署；这些仍为对应 Feature 的验收门禁。
