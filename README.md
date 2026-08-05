# Agent Dispatch for Codex

这个仓库托管 sayoriqwq 的个人 Agent Dispatch 协议、Codex Model Profile Pack 和 Lead
Skill。V1 让 Lead 显式选择不同成本与能力的模型，不预先固化 Researcher、Worker、Reviewer
等任务角色；V1.1 增量加入可审计的 Lead-centered 派发协议。

## V1 Profiles

| Profile | 模型 | 适用边界 |
| --- | --- | --- |
| `sol` | `gpt-5.6-sol` | 仍有歧义、取舍、跨域理解或高风险判断 |
| `luna` | `gpt-5.6-luna` | 目标与验收清楚、无需开放式判断 |
| `spark` | `gpt-5.3-codex-spark` | 局部、机械、容易快速验证的代码变换 |

## V1.1 Agent Dispatch

V1.1 在 Profile Pack 之外增加一个显式调用的 Lead Skill。当前 tracer bullet 支持三条路径：

- 将 Human 请求和已解析上下文编译为 `Engagement Contract`；
- 重要上下文未解析时请求澄清，或者在 Handoff Cost 不利时由 Lead 直接完成、验证并交付；
- 当 Child 更合适时，完成显式 Profile Selection 并报告 `dispatch_candidate_not_executed`。

Child Dispatch、统一 Handoff-Back 和 observe-only hooks 会按后续 tickets 增量加入；当前 Skill
不会用不完整协议创建 Child，也不会用任务角色或未知默认模型替代 `sol`、`luna`、`spark`。

Engagement Contract 的版本化 TypeScript validator 是机械 wire seam。Structural JSON Schema
只描述 transport shape；公开的 `parse/safeParse` 还验证版本、额外字段、Readiness 和
provenance 的可表达跨字段不变量。两者都不替 Lead 判断语义是否正确。当前 package 是仓库
内部的 private Module，不声明已经发布为可安装的 npm package。

Profile 只固定模型。推理强度、上下文策略、任务行为、验收方式和是否允许修改，都由 Lead
在每次派发时决定。三个 Profile 都继承父线程的 sandbox、MCP 和 Skills。

## 全局约定

全局配置片段位于 `config/agents.fragment.toml`：

- 启用 multi-agent；
- 每个主线程最多同时打开 3 个子线程；
- 未显式指定时，子代理推理强度使用 `medium`；
- 不设置默认子代理模型，模型必须通过 Profile 显式选择。

每个 Profile 都关闭自己的 multi-agent 能力。子代理需要继续拆分时必须返回 Lead，不得继续
创建下一层子代理。

## 安装 Model Profiles

执行：

```fish
./bin/link-agents
```

🔗 将三个 Model Profile 安装为个人 Codex Agent 链接。

脚本只会在个人 Codex Agent 目录中建立 `sol.toml`、`luna.toml` 和 `spark.toml` 链接。若
目标位置存在其他文件，脚本不会覆盖。全局配置片段需要精确合并到个人 `config.toml`；它
只是声明来源，不会被 Codex 自动加载。

Custom Agent 或全局配置发生变化后，需要启动一个新 Codex 任务才能可靠加载。Model
Profiles 仍是独立安装资源，不由 plugin manifest 承载。

## 安装 Agent Dispatch plugin

将当前仓库登记为本地 marketplace 并安装 plugin：

```fish
./bin/remove-legacy-skill
codex plugin marketplace add .
codex plugin add agent-dispatch@codex-agents
```

🧭 从当前仓库安装受 Git 管理的 Agent Dispatch plugin。

第一条命令是幂等迁移：新安装不会发生变化；旧安装只会在 symlink 精确指向本仓库已经退役的
`skills/agent-dispatch` 路径时删除它。普通目录或其他来源的链接会被拒绝，不会覆盖。

plugin 的 marketplace 入口是 `.agents/plugins/marketplace.json`，本体位于
`plugins/agent-dispatch`。当前只打包 Lead workflow；新任务中使用
`$agent-dispatch:lead` 显式调用，`agents/openai.yaml` 已关闭 implicit invocation。安装或更新
plugin 后必须启动一个新 Codex 任务。

plugin 不承载 Sol、Luna、Spark Model Profiles，也没有把根目录 TypeScript validator 暴露为
runtime tool。Profiles 继续由 `./bin/link-agents` 安装；validator 当前仍是开发与验证 seam。

安装 Node 依赖并验证 TypeScript 协议：

```fish
npm install
npm test
```

✅ 安装锁定依赖并验证 TypeScript 协议 Module。

## Plugin 验证结果

2026-08-04 使用 Codex CLI `0.146.0` 验证了 repo marketplace 和安装后的 fresh process：

- `codex-agents` marketplace 从仓库根目录成功登记；
- `agent-dispatch@codex-agents` 以 `0.1.0+codex.packaging-v1` 安装并进入 Codex plugin cache；
- ephemeral、read-only 的新进程显式加载 `$agent-dispatch:lead`；
- 新进程读取了 `engagement-contract.md` 和 `placement.md`，确认 explicit-only policy，并输出
  Lead gate 与六字段结果；
- 旧 `$HOME/.agents/skills/agent-dispatch` standalone 链接在验证后移除，避免同一能力出现两个
  正式入口。

## V1.1 direct-retain 验证结果

2026-08-04 在 plugin 打包之前，使用 Codex CLI `0.146.0` 对 standalone Skill tracer bullet
做了 fresh-process 验证：

- ephemeral、read-only 的新进程从 `$HOME/.agents/skills/agent-dispatch` 自动发现 Skill；
- 显式 `$agent-dispatch` 在 `gpt-5.6-sol low` Lead 上加载完整 Skill 和两个直接引用；该调用名
  属于历史 standalone 安装，plugin 的正式入口是 `$agent-dispatch:lead`；
- 在首个有效检查前输出 `Lead gate — readiness: ready_to_act; placement: retain`；
- 最终输出 Outcome、Placement、Changes、Validation evidence、Material caveats 和
  Work-state source，没有把 Lead delivery 表述为 Human acknowledgement；
- 独立 forward-test 中，悬空的“刚才那个方案”在任何修改前请求了具体上下文；
- `policy.allow_implicit_invocation: false` 通过 Skill validator，并由当前 OpenAI Skills 文档定义
  为只允许显式调用。

静态验证覆盖 9 个 TypeScript public-seam tests、6 个 prototype demos、Skill quick validation、
Fish 语法、个人安装幂等性和冲突保护。

## V1 验证结果

2026-08-03 使用 Codex CLI `0.146.0` 的交互式任务完成运行时探针：

- `luna` 实际加载为 `gpt-5.6-luna`，Lead 显式指定的 `low` 覆盖了全局默认值；
- `sol` 与 `spark` 未指定推理强度时，分别加载为 `gpt-5.6-sol medium` 与
  `gpt-5.3-codex-spark medium`；
- 主线程已经打开 3 个子线程后，第 4 次创建被拒绝并返回
  `agent thread limit reached`；
- 子线程中不存在继续创建子线程的工具，确认不会产生下一层代理。

静态验证同时覆盖 TOML 解析、Fish 脚本语法、链接安装的幂等性与冲突保护，以及 Codex
严格配置加载。运行时探针应从 Codex App 或交互式 CLI 发起；本次未把非交互式
`codex exec` 当作子代理能力的验证入口。

## 派发原则

模型按任务剩余歧义选择，而不是按改动文件数选择：

```text
仍需判断、取舍或承担高错误成本
    → sol

目标、范围和验收已经清楚
    → luna

纯机械、局部、可快速验证
    → spark
```

Spark 当前不可用时，由 Lead 明确改派 Luna；V1 不提供自动 fallback。

默认使用零历史加自包含任务包。Lead 可以按任务需要改用最近若干轮或完整上下文，但上下文
策略不属于 Profile。
