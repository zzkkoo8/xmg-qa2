# XMG-QA2 Project Baseline

## 一句话

**xmg-qa2 = XMG Harness + LangGraph Runtime + Plugin Architecture + Knowledge Contract + SpecKit SDD。**

## 关键边界

```text
Channels
   |
Harness Gateway
   |
Workflow Runtime
   |
+-- Knowledge Contract --> Knowledge Providers
+-- Model Contract -----> Model Providers
+-- Tool Contract ------> Tool Providers
```

Knowledge Factory 是独立项目，不属于 xmg-qa2。

## 十条 Constitution 候选原则

1. Workflow First
2. External Capability via Plugin Contract
3. Knowledge Independence
4. Contract First
5. Dependency Direction Enforcement
6. Evidence First
7. Observable by Default
8. Deterministic Where Possible
9. Provider Neutrality
10. Spec Before Code

## 正式编码门禁

```text
Architecture Approval
  -> Constitution
  -> Specify
  -> Clarify
  -> Plan
  -> Checklist
  -> Tasks
  -> Analyze
  -> Human Approval
  -> Implement
  -> Converge
```

进入 Implement 前：

```text
Critical = 0
High = 0
```

## SpecKit 初始化

推荐在空目录执行：

```bash
mkdir -p /data/dev/xmg-qa2
cd /data/dev/xmg-qa2
specify init --here --integration codex --script sh
specify extension add git
git init -b main
```

然后再合入本项目基线文档。

不要在已有大量文件的目录里为了省事使用 `--force`。

完整步骤见 `docs/BOOTSTRAP.md`。
