# 主题、页面扩展与报告模板契约

版本：1.0；日期：2026-09-05；状态：待实现。对应 FR15/FR16；HTML/MD 指可定制展示与报告，不把模板当作执行任意代码的入口。

## 1. 个性化范围

| 层级 | V1 可调整 | 发布方式 |
| --- | --- | --- |
| 品牌主题 | 系统名称、Logo、主题色、字体枚举、深浅主题 | 受 Schema 约束的 theme 版本；不上传任意全局 CSS/JS |
| 消息/报告模板 | 摘要、诊断报告、人工请求的 Markdown/HTML 布局 | Admin 编辑/预览/验证/发布；无需重建应用镜像 |
| 信息页面 | 经清洗的 HTML/Markdown 帮助页、说明页 | 安全展示容器；不能执行脚本或获得 API 凭证 |
| 交互页面/工具卡片 | Chat/Admin 已注册 React 页面、侧栏项、证据/工具渲染组件 | UI 扩展清单 + 代码评审 + 构建发布，不热执行远端 JS |
| 业务规则 | 新节点、API、能力与领域功能 | 正式 Feature/Contract；模板不能替代它们 |

权限、恢复动作、引用解析与工具调用由系统组件掌控。模板可改变排版和允许文案，不隐藏必须说明的未确认项、证据或风险，不把建议标成已执行。模型提示词是独立版本化资源，模板文本不会自动成为系统提示词。

## 2. TemplateProvider

接口职责为 list/get/validate/render/publish/rollback；模板存储和渲染属于展示端口，不能作为目标 Tool 获得生产权限。RenderInput 仅包含已授权、结构化的 ReportSnapshot，不传入完整 ORM 对象、运行上下文、环境变量或任意函数。

| 字段 | 约束 |
| --- | --- |
| template_id/version/schema_version | 稳定 ID、不可变发布版本；发布时唯一 |
| kind/output_format/locale | answer/report/human_request/info_page；markdown/html；默认 zh-CN |
| input_schema/body/content_hash | 固定数据合同、模板源码与 hash |
| scope/owner/status | 客户/项目适用范围、操作者、draft/validated/published/retired |
| required_fields | 结论状态、证据、未确认项等不可删的输出部分 |
| limits/renderer_version/sanitizer_profile | 时间、输入/输出上限和固定渲染规则 |
| source/provenance | 原始来源、许可、审核记录；资产引用必须可访问 |

ReportSnapshot 固定 result_version、answer_kind、question_coverage、claims、evidence_refs、observed_at、recommendations、pending_items、execution_status；Artifact 记录 snapshot_hash/template_version/renderer_version。旧报告不随模板修改而变化，重新渲染创建新版本并标注，下载仍校验当前权限。

按[问答核心](QA-CORE.md)的答复类型选择短答、步骤或调查报告模板；通用解释允许 evidence_refs 为空并标明通用说明，不强迫虚构引用。必需的状态/待办/风险按实际内容展示，不能因空字段堆砌长报告。

内置模板随镜像只读提供；Admin 模板版本持久入库，资产存 ArtifactStore。优先级为获准项目配置 → 组织默认 → 内置默认，不能跨客户查找；发布前验证 fallback 也有同等数据范围。preview 使用合成样例，显式选真实 Case 时重新校验 ACL。

## 3. 渲染与隔离

采用 Jinja2 SandboxedEnvironment 作为成熟模板引擎，但只开放经过审核的变量/有限循环/条件子集。StrictUndefined、禁调用/私有属性/动态 include/import/自定义可执行 filter，允许 filter 清单固定；循环输入限制数量。预览与发布都进行相同校验。Jinja 官方说明沙箱本身不能解决资源耗尽或输出 HTML 的全部风险，因此还须隔离与输出清洗。[Jinja 沙箱](https://jinja.palletsprojects.com/en/stable/sandbox/)

- 渲染在独立受限子进程执行，无生产凭证/网络/任意文件访问；时间、内存、输入、输出均有上限，超限终止该次渲染，不拖住 API/调查 Worker。此子进程可由现有 Worker 管理，无需再部署模板平台。
- HTML autoescape 显式开启；变量仅在文本节点和审核过的属性使用，不提供 safe/raw 绕过。Markdown 文本插值经专用转义，引用 URL 由受控 Evidence 解析器生成。
- HTML 最终经服务器端 nh3 allowlist 清洗；预览在不带 allow-scripts/allow-same-origin 的 sandbox iframe，配禁止外联的 CSP。禁止脚本、事件属性、表单、嵌套 iframe、任意 CSS URL、外部字体/图片和主动内容；主题 CSS 由系统根据受限字段生成。
- HTML 下载产物使用同一清洗结果和内嵌安全样式/受控资产，不输出“下载后可执行”的原始模板。Markdown 下载本质为文本，但浏览器预览仍执行链接/资源限制。
- Chat Markdown 默认禁用原生 HTML；确需扩展时使用固定的 react-markdown 插件链与 rehype-sanitize，过滤危险 URL，禁止从任意远程地址自动加载图片。
- 模板不执行外部抓取或发送通知。渲染后重新检查必需段落、引用支持和用户权限；失败使用安全内置模板并记录降级，无法满足输出校验则不发布最终结果。

依据：[nh3](https://nh3.readthedocs.io/)、[react-markdown](https://github.com/remarkjs/react-markdown)、[浏览器 iframe 隔离](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe)。具体语法、限额和清洗允许标签在 Feature Plan 固定并测试，不声明当前已有安全实现。

## 4. 工作流与 UI 扩展衔接

Workflow 发布可引用 report_template_id/version，不允许任意路径。模板升级不改变状态转移。UI 扩展清单声明 extension_id/version、route/slot、required_scopes、所消费的 API schema；构建时注册，路由不覆盖 `/v1`/认证入口，页面隐藏不是授权检查。

新增插件遵循 Plugin Contract：配置可切换已注册 Provider；新代码经打包和兼容测试后才能启用；新业务规则走 Feature，不能仅改 YAML 注入 Python。普通功能扩展可新增模块与 API，保持依赖方向，不能承诺所有新功能都零代码完成。

验收包括：修改模板不重建镜像；发布/回退与旧报告一致；跨客户引用/资产被拒绝；HTML 脚本/外联、路径穿越、模板对象访问/资源耗尽被阻断；失效模板可降级；UI 注册项不能绕过权限。
