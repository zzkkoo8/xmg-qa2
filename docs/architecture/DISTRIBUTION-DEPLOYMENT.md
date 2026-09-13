# 开发、打包与部署交付

版本：1.0；日期：2026-09-05；状态：待实现产品交付规范。开发在开发机，部署到独立支持服务主机；不把 xmg-qa2 装入客户生产设备。

## 1. 默认交付形态

一个版本发布包 + OCI 应用镜像 + Docker Compose。应用镜像包含 Python 服务和已构建 Chat/Admin 静态资源，分别以 api/worker/dispatcher/dingtalk 入口运行。PostgreSQL/RabbitMQ 使用固定的官方镜像。可选的身份/TLS 网关在部署 profile 中明确计入依赖。

不强行做成单文件可执行程序：持久数据库、消息队列和多进程职责仍然存在。目标是使用者不需要在服务器拉 GitHub 源码、安装 Node/pnpm 或在线编译 Python 依赖，而非把必要服务隐藏起来。

| 环境 | 运行方法 | 范围 |
| --- | --- | --- |
| 开发机 | Python/uv 与 Node/pnpm；Vite HMR；PG/RabbitMQ 用 Compose | 代码、测试、构建；独立开发数据卷与 dev 身份 |
| 集成测试 | 完整 Compose 和测试身份入口 | 与发布相同应用镜像；真实组件的故障/恢复测试 |
| 在线部署 | 下载配置包，固定镜像后 pull/up | 用户只配置域名/端口/存储、身份和外部服务 |
| 离线/弱网部署 | 上传目标平台离线包，校验、load、迁移、up | 包含选定 profile 的全部镜像和静态资产；不现场访问 npm/PyPI/镜像仓库 |

Compose 支持多环境配置；生产配置应去掉源码挂载/开发服务。[Docker 生产部署](https://docs.docker.com/compose/how-tos/production/)

## 2. 目标工程与发布物

以下均为后续应创建的路径，目前不伪造文件或下载地址：

| 目标路径/产物 | 责任 |
| --- | --- |
| `web/`、`src/xmg_qa2/` | 前后端源码；一个仓库 |
| `pyproject.toml`/`uv.lock`、`web/package.json`/`pnpm-lock.yaml` | 依赖与工具版本锁定 |
| `deploy/Dockerfile` | Node 构建静态资源；Python 独立运行阶段，无 Node 运行依赖 |
| `deploy/compose.yaml`、`compose.dev.yaml`、`compose.offline.yaml` | 固定服务、开发覆盖、离线镜像映射 |
| `deploy/env.example`、`config/`、`templates/` | 无秘密的配置例子、内置配置和模板 |
| `scripts/doctor`、`install`、`backup`、`upgrade`、`restore` | 可重入交付工具；作用于本系统，不能变更客户目标 |
| `release-manifest.json`、`SHA256SUMS`、`sbom.*`、`THIRD_PARTY_NOTICES` | 版本、源码提交、平台、镜像 digest、配置/DB/checkpoint schema、依赖和来源 |
| `xmg-qa2-<version>-config.tar.gz` | 在线配置包与 QUICKSTART，不含源码构建依赖 |
| `xmg-qa2-<version>-linux-<arch>-offline.tar.gz` | 配置包 + images.tar + 完整镜像清单与校验；每 CPU 平台单独测试 |

默认首发 linux/amd64；linux/arm64 在镜像、原生包和恢复测试通过后才标为支持，不能因开发机是 Mac ARM 就承诺全部平台可用。Buildx 用于多平台构建；外部依赖也必须有对应平台。[多平台构建](https://docs.docker.com/build/building/multi-platform/)

发布建议 GitHub Release + GHCR，可配置内部 registry 镜像地址。仓库公开不等于容器包公开；公开 GHCR 镜像可匿名拉取，私有包需要部署侧授权。离线包用于缓解目标环境拉取慢，不能保证任何公网 registry 在国内都快。[GHCR 权限](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)

## 3. 安装和离线语义

目标主机已安装受支持 Docker Engine/Compose plugin；doctor 检查版本、平台、CPU/内存/磁盘、端口、卷权限、镜像清单、时钟和外部依赖。运行时缺失应输出对应发行版安装步骤；V1 应用包不默认替用户升级 Docker、改防火墙或网络。

安装工具在生成本地配置、身份初始化及依赖信息后，使用固定 release manifest 执行校验、数据库单次迁移、服务启动及健康检查。安装失败保留配置和日志，可重新执行；非交互模式提供显式参数，敏感值不进命令历史或日志。未来提供一条 install 命令作为入口，其内部并不是盲目 compose up。

离线工具先核验 SHA256SUMS/来源及平台，`docker image load` 导入完整 images.tar；离线 Compose 引用包内固定本地标签，manifest 记录其 image ID 与上游 digest 对应关系，禁止 build/pull。不能假设 save/load 自动保留远端 manifest-list digest 的引用语义。导入后核对 image ID，启动使用 `--pull never --no-build`，在断开 registry/npm/PyPI 后做安装测试。[save](https://docs.docker.com/reference/cli/docker/image/save/)、[load](https://docs.docker.com/reference/cli/docker/image/load/)

应用离线安装不等于公网搜索和公有 LLM 可以离线运行。外部 Dify/LLM/钉钉/搜索是否可达单独显示；可用内网 Provider 则接入，否则有关能力显式不可用。镜像包不夹带模型权重、用户原始知识库、私钥或既有 Case 数据。

## 4. 就绪、秘密与持久化

- liveness 检查进程；readiness 检查数据库迁移、checkpoint schema、队列和身份配置。KB/模型等能力健康单列，未配置可显示“等待接入”，不能误报真实问答可用。
- PG/RabbitMQ healthcheck 和一次性迁移成功后才启动应用服务；每个 API/Worker 不竞争自动迁移。depends_on 的启动顺序不代替实际 healthy 检查。[Compose 依赖就绪](https://docs.docker.com/compose/how-tos/startup-order/)
- PG、附件/报告、模板资产分别持久化；密钥由运行时 secrets/受保护文件注入。发布包、镜像层、构建参数、前端 VITE_* 和默认配置不带秘密；不交付通用默认管理员密码。
- V1 ArtifactStore 的静态加密由宿主加密卷或组织加密存储实现，普通 Docker volume 不自动加密；doctor 输出是否满足该前置要求，密钥恢复单独管理。调试环境使用合成数据并明确非生产合规状态。
- 备份覆盖业务表、图 checkpoint、人工恢复记录、模板与资产索引，以及 ArtifactStore 中附件、报告和模板资产的实际字节及校验和。先冻结新任务、已有 Case 补充、上传、Admin 发布等全部相关写入口并暂停调度，等待当前执行段和在途写入结束，再取得数据库与对象的一致性备份。未完成 quiesce 不报告一致快照；恢复后核对对象校验和、索引引用和版本完整性，再开放写入。恢复任务调度以业务 Outbox 为依据，不只恢复 RabbitMQ 消息。

## 5. 升级、回退和验收

升级：校验新版本/平台/迁移兼容矩阵 → 冻结相关写入口并停止调度 → 有界排空执行段与在途写入 → 取得数据库和对象一致备份 → 单次迁移 → 切镜像 → 就绪/恢复测试 → 开放流量。失败不删除卷，不执行 down -v。

回退应用前核对旧镜像能否读取新业务/检查点 schema；不兼容时保留旧镜像及迁移前一致备份，按 restore 手册恢复并明确备份后的写入损失边界，禁止承诺“换旧镜像永远可回退”。等待 Case 的图版本按既有协议保留/显式迁移；V1 必须验证旧图加载或安全暂停。

第一 Feature 即建立开发 Compose、基础 Dockerfile/CI 和无秘密配置；最终发布 Feature 才完成经过测试的 Release/OCI/离线包。验收：干净 Linux 主机在线安装、断网导入、无 Node/Python 开发工具、重复安装、端口/架构错误、健康失败、备份恢复、升级回退、72 小时等待恢复；逐项记录实际版本和结果，不以文档中的命令示例冒充安装器已交付。
