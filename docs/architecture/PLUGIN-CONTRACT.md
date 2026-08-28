# Plugin Contract

## 1. 目的

Plugin Contract 解决“XMG Harness 如何使用能力”，而不是“Provider 如何实现能力”。

所有插件必须：

- 有稳定 `plugin_id`。
- 有 `plugin_type`。
- 有版本。
- 可报告 capabilities。
- 可健康检查。
- 有明确配置 schema。
- 可初始化和关闭。
- 不把 Provider 私有对象泄漏给调用方。

## 2. Plugin Types

V1 固定五种主要外部插件：

- `channel`
- `knowledge`
- `model`
- `tool`
- `policy`

`workflow` 属于可装配能力，但其生命周期由 Runtime 单独管理，不与外部 Provider 插件完全等价。

## 3. Common Metadata

概念字段：

```text
plugin_id
plugin_type
version
display_name
capabilities[]
enabled
health
config_schema_version
```

## 4. 生命周期

```text
discover
  -> validate_config
  -> initialize
  -> ready
  -> execute
  -> health
  -> shutdown
```

初始化失败不得进入 ready。

## 5. Registry 规则

Registry 必须支持：

- 按 type 查询。
- 按 id 查询。
- capability 匹配。
- default provider。
- 显式 provider override。
- unavailable 状态隔离。

Workflow 不允许写：

```text
if provider == "dify":
...
elif provider == "ragflow":
...
```

这种逻辑属于 Adapter。

## 6. 配置原则

Secrets 与普通配置分离。

禁止：

- API Key 写入代码。
- Provider URL 写入 Workflow。
- 把敏感配置记录进普通 trace。

## 7. Contract Versioning

Breaking change 必须提升 Contract major version。

Provider 插件声明其支持的 Contract version。

Core 启动时必须检查兼容性，不兼容则 fail fast。

## 8. Testing

每个插件必须通过统一 Contract Test Suite。

Contract Test 验证：

- 初始化。
- health。
- timeout。
- cancellation。
- 错误映射。
- schema。
- 返回类型。
- 资源释放。
