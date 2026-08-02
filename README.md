# Codex 模型资源 Profiles

这个仓库托管 sayoriqwq 的个人 Codex Custom Agent 配置。V1 只解决一件事：让 Lead
显式选择不同成本与能力的 Codex 模型，不预先固化 Researcher、Worker、Reviewer 等任务
角色。

## V1 Profiles

| Profile | 模型 | 适用边界 |
| --- | --- | --- |
| `sol` | `gpt-5.6-sol` | 仍有歧义、取舍、跨域理解或高风险判断 |
| `luna` | `gpt-5.6-luna` | 目标与验收清楚、无需开放式判断 |
| `spark` | `gpt-5.3-codex-spark` | 局部、机械、容易快速验证的代码变换 |

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

## 安装

执行：

```fish
./bin/link-agents
```

脚本只会在个人 Codex Agent 目录中建立 `sol.toml`、`luna.toml` 和 `spark.toml` 链接。若
目标位置存在其他文件，脚本不会覆盖。全局配置片段需要精确合并到个人 `config.toml`；它
只是声明来源，不会被 Codex 自动加载。

Custom Agent 或全局配置发生变化后，需要启动一个新 Codex 任务才能可靠加载。

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
