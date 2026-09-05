# Knowledge / Evidence Contract

版本：1.0；日期：2026-09-05。xmg-qa2 消费发布的知识服务，文档解析、清洗、去重、分类、切片、Embedding 和建索引仍属于 xmg-kb。

## 1. 提供方能力

health()、capabilities()、search() 必需；fetch_evidence()/retrieve_document() 为声明式可选能力，不要求所有 Provider 都能按历史版本取回全文。

capabilities 声明：contract_version、supported_filters、tenant_scope、snapshot_support、document_fetch、score_semantics、max_query_length、timeout/cancel 支持。不支持的强制过滤返回 UnsupportedCapability/PermissionDenied，禁止忽略后扩大数据范围。

## 2. 请求

| 字段 | 规则 |
| --- | --- |
| request_id / task_id / principal | 服务端生成和验证 |
| customer_id / project_id / allowed_namespaces | 从身份与任务推导，不接受模型任意指定 |
| query / top_k | 最小必要问题；query 长度由 Adapter 验证，不能直接上传全部对话 |
| filters | 产品、版本、文档类型、有效日期等规范化条件；与 ACL 区分 |
| knowledge_version | 要求快照时必须确认提供方支持；不支持则明确返回 |
| data_classification / egress_profile | 影响检索、embedding、rerank 与模型调用 |
| deadline / trace_context | 跨层共享截止时间，不无限增加预算 |

ACL 必须在检索和第三方 rerank/LLM 之前落实，返回后再复核。相关性过滤不是权限隔离。缓存键至少包含授权范围、provider、知识版本/observation、query 与过滤，不跨客户复用检索结果。

## 3. 统一 Evidence

| 字段 | 内容 |
| --- | --- |
| evidence_id / source_type / provider_id | KB、official_doc、api、tool、user_statement、human_verified 等；模型推理另存 hypothesis，不虚构出处 |
| title / content_ref / content_excerpt / content_hash | 摘录与原件引用，hash 检测变化；hash 不证明来源真实 |
| source_uri / document_id / chunk_id / locator | 文档、页、节、行或资源标识；不适用字段明确 null，不伪造 |
| observed_at / published_at / updated_at | 采集时间与文档时间分离；未知为 null |
| product / version_scope / environment_scope | 适用产品版本和现场；缺失不能默认匹配 |
| knowledge_version / version_kind | 原生 release/snapshot 优先；无版本仅 observation/content-hash，不宣称快照可重放 |
| auth_scope / classification | tenant/customer/project/case 与数据等级 |
| retrieval_score / score_semantics | 相关度及提供方定义，不直接转换成置信度 |
| verification_status / method / result | 是否人工/工具验证、验证什么、结果和限制 |
| claim_links / conflicts / supersedes | 支持或反驳的命题、冲突与替代关系 |

动态证据裁决按命题类型和适用性综合判断，不使用“现场 > 内部 > 官网”的绝对排名。用户陈述保留原意、状态和时间；外部网站和检索片段中的指令只作为数据，不改变系统 Policy。

按子问题查询、去重、补原文上下文、保留反证和有界证据包见 [QA Core](QA-CORE.md)。混合搜索/重排只使用提供方声明的能力；新增适配策略先比较冻结题集收益，不以相关度替代最终答案质量。

## 4. Dify 首个适配器

采用纯检索 API，不调用 Dify Chat API 生成第二份答案。当前官方定义为 POST /datasets/{dataset_id}/retrieve，query 最大 250 字符，返回 records/segment/document/score。完整 base URL 和字段以实际安装版本核验。[Dify 检索 API](https://docs.dify.ai/en/api-reference/knowledge-bases/retrieve-chunks-from-a-knowledge-base-test-retrieval)

- 服务器映射 customer/project → 允许 dataset 集合，Key 只在服务端。
- 当前公开接口文档未足以证明用户实例的细粒度 ACL/元数据过滤能力。先能力探测与越权测试；不可证明时使用按授权隔离的数据集或受控检索入口，不能检索全部后才过滤。
- 当知识库不支持发布快照，记录 document/chunk ID、内容 hash、时间和自有 observation_id；答案引用保留摘录，但不得声称能恢复整个旧索引。
- /health 可用不代表 dataset Key 可读，发布前用最小实际检索验证。
- 不同提供方分数不可直接相加；必要重排只在已授权证据范围内进行。
- KB 不可达或鉴权失败须返回明确错误，不假装没有答案。

## 5. 错误与验证

统一错误：NoResult、InvalidQuery、UnsupportedCapability、ConfigurationError、AuthenticationError、PermissionDenied、Timeout、RateLimit、ProviderUnavailable、InvalidResponse、ContractViolation。

同一 Contract Suite 运行于 Fake 和真实适配器，验证过滤、错误分类、版本、引用定位、超时、取消、数据隔离。新增 RAGFlow/Haystack/LlamaIndex 必须先在同一人工题集证明质量收益，不改变 Workflow 对 Evidence 的理解。
