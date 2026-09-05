# 模块依赖规则

日期：2026-09-05。采用端口与适配器，不用一条线性箭头暗示所有插件必须依赖业务 Runtime。

| 模块 | 可以依赖 | 禁止依赖 |
| --- | --- | --- |
| domain | Python 标准库与领域值对象 | LangGraph、FastAPI、SDK、数据库/队列客户端 |
| harness/contracts | domain、Pydantic 等契约验证 | 具体 Provider、API、工作流实现 |
| harness/registry | contracts、基础配置接口 | 厂商业务分支、外部动态安装器 |
| workflows | domain、contracts、LangGraph 图构建 API | Dify/钉钉/产品 SDK、数据库连接 |
| runtime | contracts、workflows、LangGraph、持久化端口 | 入口 payload 私有结构；插件私有业务逻辑 |
| plugins | contracts、各自 SDK/HTTP 客户端、必要基础设施 | 核心 Workflow 业务规则、其他 Provider 私有实现 |
| infrastructure | 持久化/队列/对象存储端口、官方客户端 | channel 业务、模型决定权限 |
| api / channel | 应用服务接口、contracts | 证据裁决、调查逻辑、直接修改图内部状态 |
| composition root | 装配具体 runtime、plugins、infrastructure | 业务策略 |
| observability | 事件契约、OTel | 作为业务状态真相 |

workflows 可使用 LangGraph，但图私有 State 不暴露给 domain/HTTP/Provider。数据操作经明确端口，运行引擎通过适配器接 checkpoint；SQLAlchemy Session 不跨并发任务共享。

实施阶段采用 Import Linter 的 forbidden/layers/independence 合约和 CI 验证，先为可运行包结构定义规则；本轮不创建形式化空测试。[Import Linter 官方说明](https://github.com/seddonym/import-linter)

代码位置目标复用现有 src/xmg_qa2 下目录；需要新目录的具体文件在 Feature Plan 冻结，不为了目录美观创建一批空模块。违反依赖方向必须先 ADR、更新相关设计、执行 Analyze，再取得相应实现授权。
