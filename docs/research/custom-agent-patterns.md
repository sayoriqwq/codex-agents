# Custom Agent 作为派发模式沉淀 Seam：一手资料研究

> 日期：2026-08-03  
> 研究问题：何时应把重复派发沉淀为 Custom Agent，何时应继续使用 Skill / workflow、recipe / 自包含任务包或模型 Profile？  
> 证据规则：只采用当前官方产品文档与项目维护者的一手仓库资料；“事实”和“推断”分开标注。

## 结论先行

Custom Agent 最适合沉淀的是一个**可独立运行的执行环境契约**：同一种工作反复需要隔离上下文、稳定的系统指令、受限工具或权限、专属 MCP / Skill 集合，或稳定的模型默认值。它不适合单独承载阶段顺序、输入发现、重试、交接、聚合、人工 gate 等完整 workflow。

因此，Issue #2 不应从 session 中出现过的 `task_name` 直接反推 Agent。应先确认重复的是“执行环境契约”还是“workflow 内部的一段 prompt”。对于现有 Matt `code-review` Skill，Standards / Spec 更像双轴 workflow 的内部 leaf role；现有证据不足以支持两个全局 Custom Agent。

| 载体 | 最合适的稳定部分 | 不应由它承担 |
| --- | --- | --- |
| 模型 Profile | 模型身份与少量模型级默认值 | 任务角色、workflow、repo 规范 |
| Custom Agent | 独立上下文、系统指令、工具/权限/MCP/Skill 配置 | 多阶段顺序、动态任务包、跨阶段聚合 |
| Skill / workflow | 触发条件、步骤、输入发现、并行/串行、验证、失败返回 | 强安全隔离；仅靠提示词不能形成强制权限 |
| recipe / 自包含任务包 | 低频、动态、尚未稳定的派发结构 | 跨 session 的自动复用与治理 |

## 1. Custom Agent 解决什么痛点

### 1.1 隔离主线程噪声，并固定执行环境

**官方事实。** Codex 将 subagent 用于把探索、测试、日志分析等高噪声工作移出主线程，只把摘要送回；并行 subagent 会增加 token 消耗。Codex Custom Agent 是 spawned session 的配置层，可在个人 `~/.codex/agents/` 或项目 `.codex/agents/` 中定义，并覆盖 `model`、`model_reasoning_effort`、`sandbox_mode`、`mcp_servers` 和 `skills.config`；未声明项从父线程继承。[OpenAI Codex — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

**官方事实。** Claude Code 同样把 Skill 定义为可复用内容，把 subagent 定义为独立 worker；其建议在需要隔离大量输出、专门工具限制或可独立返回摘要时使用 subagent，在需要主线程中的可复用 prompt/workflow 时优先 Skill。[Anthropic — Extend Claude Code](https://code.claude.com/docs/en/features-overview) Claude 的 agent 文件还可声明工具、拒绝工具、模型、permission mode、MCP、预加载 Skills、hook 和 worktree isolation。[Anthropic — Create custom subagents](https://code.claude.com/docs/en/sub-agents)

**官方事实。** GitHub Copilot 将 Custom Agent 描述为带专属 prompt、tools 和 MCP servers 的 specialized Copilot；agent profile 被实例化后执行任务。[GitHub Docs — About custom agents](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents)

**分析推断。** 三家共同指向同一个高价值 Seam：Custom Agent 的核心不是“有一个角色名字”，而是让反复出现的 worker 获得与主线程显著不同且稳定的执行环境。若唯一稳定项只是“这次关注 Spec”，一段 workflow 内部 prompt 已经足够，新增 Agent 的收益很薄。

### 1.2 显式能力收缩与成本默认值

**官方事实。** Codex 允许 Agent 文件固定模型、effort、sandbox、MCP 与 Skills，但父 turn 的 live sandbox / approval override 会在 child 创建时重新应用；这意味着 Agent 可以给出更窄的默认值，却不是越过父级安全策略的权限容器。[OpenAI Codex — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

**官方事实。** Claude Code 可通过 `tools`、`disallowedTools` 和 `permissionMode` 收缩能力，但部分父权限模式优先于子 agent 配置；GitHub Copilot 也允许 agent profile 显式列出可用工具，省略时默认可能得到全部工具。[Anthropic — Create custom subagents](https://code.claude.com/docs/en/sub-agents) [GitHub Docs — Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)

**分析推断。** “默认只读”“只能查官方文档”“只准使用某个 MCP”是 Custom Agent 的强候选信号；“每次都用同一昂贵模型”则不是，除非用户明确愿意牺牲 V1 的动态成本选择。当前仓库已经用 `sol` / `luna` / `spark` Profile 分离了模型资源，因此 V2 Agent 不应再次绑定模型角色。[本仓库 README](../../README.md)

### 1.3 当前仓库的组合约束：任务角色与模型 Profile 争用同一个选择位

**官方事实。** Codex 每次 spawn 选择一个 `agent_type`；事件模型也把它表述为 “subagent type or profile”。每个 Custom Agent 文件又是一份完整的 spawned-session configuration layer。官方文档描述了单个 Agent 内各字段的覆盖与继承，但没有提供把两个命名 Agent/Profile 组合成一个 child 的 mixin 机制。[OpenAI Codex — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

**分析推断。** 这对本仓库尤其关键：`sol` / `luna` / `spark` 已占用同一个选择维度来表达模型资源。若再选择 `standards-reviewer`，就不能同时“选择 `sol` Profile”；只剩四种不理想方案：让 reviewer 继承 parent model、在每次 spawn 直接写 model、为 role × model 生成矩阵，或把 role 指令复制进三个 Profile。前三者分别削弱 V1 的显式 Profile 约定或增加调度分支，最后一种会直接制造漂移。因此在 Codex 提供可组合配置之前，**Skill / dispatch recipe + 模型 Profile** 是任务模式与模型选择最干净的组合方式。

## 2. Custom Agent 不解决什么

### 2.1 不自动形成可靠 workflow

**官方事实。** Codex 明确把 orchestration（spawn、follow-up、wait、close 与汇总）交给 ChatGPT/Codex 主线程，并允许 prompt、`AGENTS.md` 或 Skill 触发 delegation；Custom Agent 文件只定义 child session 的配置。[OpenAI Codex — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

**官方事实。** OpenAI 将 Skill 定义为 reusable workflow 的 authoring format，支持 instructions、references 和 scripts，并通过 progressive disclosure 仅在命中时加载完整内容。[OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills) GitHub 也建议把几乎每次都适用的简单规范放进 custom instructions，把只在相关任务中需要的详细步骤放进 Skills。[GitHub Docs — Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)

**分析推断。** Spec 来源发现、固定点校验、两个 reviewer 的并行启动、结果分轴、失败降级和最终汇总都属于 workflow。把 Standards / Spec 写成两个 Agent 并不会自动得到这些语义；Lead 仍需重复编排，或另建 Skill。若 Agent 只被一个 Skill 调用，且没有独立的环境隔离收益，Agent 只是多了一处易漂移的 prompt 副本。

### 2.2 不保证正确性、合规性或可测试性

**官方事实。** Codex Skill 官方建议用测试 prompts 验证 description 是否在正确任务触发；Claude 文档也把 prompt instructions 与 hooks 区分开：需要确定执行的机械约束应由 hook 等机制强制，而不是依赖模型解释。[OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills) [Anthropic — Extend Claude Code](https://code.claude.com/docs/en/features-overview)

**社区一手事实。** Superpowers 把完整开发方法实现为可组合 Skills，再由 Skill 派发 fresh subagent；其 subagent-driven-development Skill 显式维护任务输入、review package、修复轮次、阻塞条件和最终 review，而不是只提供 reviewer 名称。[Superpowers README](https://github.com/obra/superpowers/blob/main/README.md) [Subagent-driven development Skill](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md) 项目还用 RED / GREEN / REFACTOR pressure scenarios 测试 Skills。[Testing Skills With Subagents](https://github.com/obra/superpowers/blob/main/skills/writing-skills/testing-skills-with-subagents.md)

**分析推断。** Agent 配置通过 TOML/Markdown 解析只说明“能加载”，不能说明它会在真实压力下遵守输出契约。任何沉淀都需要行为探针：正确触发、错误不触发、缺输入会返回 Lead、权限确实受限、结果满足 schema。

## 3. 作用域与包装：global 是高门槛，不是默认

**官方事实。** Codex Agent 有个人级 `~/.codex/agents/` 与项目级 `.codex/agents/`；Skills 有用户级 `$HOME/.agents/skills` 和仓库级 `.agents/skills`，需要跨用户分发时可打包为 Plugin。[OpenAI Codex — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)

**官方事实。** Claude Code 同样区分个人 `~/.claude/agents/` 与项目 `.claude/agents/`；GitHub Copilot 进一步提供 user、repository、organization、enterprise 四层，并定义同名覆盖次序。[Anthropic — Create custom subagents](https://code.claude.com/docs/en/sub-agents) [GitHub Docs — Invoking custom agents](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents)

**官方事实。** Cursor 的 Rules 也区分全局 User Rules 与可版本控制的 `.cursor/rules` Project Rules，说明“个人通用”与“repo 约束”是普遍存在的两种作用域，而不是 Custom Agent 特例。[Cursor Docs — Rules](https://cursor.com/docs/rules)

**分析推断。** 只要 role 的标准、输入或验证依赖某个 repo，就先放项目 Skill / Agent；只有在至少多个 repo 中合同相同、且不携带 repo 术语时，才有资格成为 global Agent。全局文件不随业务 repo 的 PR 一起评审，prompt/contract drift 风险更高；本仓库以 Git 管理个人配置能缓解版本问题，但不能消除跨 Skill 的重复定义。

## 4. Prompt / contract drift、可观察性与版本治理

### 4.1 Drift

**官方事实。** Codex 官方提醒 Custom Agent 文件是完整 session configuration layer，形态比专用 manifest 更重，格式可能随 authoring/sharing 成熟而演进。[OpenAI Codex — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) GitHub Copilot 的同一 agent profile 在不同 surface 也存在字段差异，例如 cloud agent 会忽略部分 IDE 字段。[GitHub Docs — Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)

**分析推断。** 合同的单一事实源应在 workflow Skill：Agent 只保留跨 workflow 不变的 system-level contract。动态输入、验收和返回格式由每次 dispatch task package 提供。若同一句规范同时出现在 Agent、Skill 和 `AGENTS.md`，应删除副本或改为引用；否则更新一处会产生静默 drift。

### 4.2 可观察性

**官方事实。** Codex App/CLI/IDE 可查看 subagent thread、状态与返回摘要；Claude Code 提供 `SubagentStart` / `SubagentStop` 和 tool hooks，且保存独立 transcript；GitHub Copilot SDK 可把 subagent lifecycle events 流回 parent session。[OpenAI Codex — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) [Anthropic — Create custom subagents](https://code.claude.com/docs/en/sub-agents) [GitHub Copilot SDK — Custom agents and sub-agent orchestration](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents)

**分析推断。** “看得到 agent 名称和完成状态”不等于“知道合同是否满足”。V2 应记录最小、脱敏的观测字段：workflow、leaf role、所用 Profile、只读/可写、结果状态、验证状态、是否续派；不要把原始 session prompt 作为长期分析资产。统计时至少拆成三张视图：workflow demand、leaf execution volume、direct named-agent demand。重试与续派附着到原 dispatch，不能重复算作新的模式需求；来源不明就保持 `unknown`，不能默认成用户直接需要某 Agent。

若后续建立结构化记录，最小 provenance 可包含：`spawn_call_id`、`workflow_run_id`、`origin_kind`（`user_direct | skill_leaf | orchestrator_leaf | unknown`）、`origin_artifact_id/version`、`workflow_step_id`、`requested_agent_type`、`resolved_definition_id/version`、`model`、`effort`、`context_mode`、`success` 与 `retry_of`。这些字段记录因果来源和实际解析结果，不保存敏感任务正文。

### 4.3 测试与版本

建议每个持久项与其声明一起版本控制，并具备：

1. schema/load test；
2. 正向触发与负向不触发场景；
3. 一次真实 App/交互式 CLI probe；
4. 权限、工具、模型和 effort 的观测断言；
5. 缺输入、外部系统不可用、输出不合约的失败场景；
6. 修改合同后的回归 transcript 摘要，而非敏感原文。

## 5. 社区项目给出的边界信号

**社区一手事实。** Superpowers 以 Skills 作为跨 harness 的主要 workflow 单元，Skill 内部构造精确任务包并派发 fresh subagent；它证明 leaf worker 可以是临时的，而复杂性集中在 workflow。[Superpowers README](https://github.com/obra/superpowers/blob/main/README.md)

**厂商一手实现事实。** Anthropic 自己的 Claude Code `code-review` Plugin 也把 preflight、repo 指令发现、PR 摘要、四路并行 review、逐 finding 验证、false-positive 过滤和可选评论统一写在一个 command/workflow 中；并行 leaf 由 workflow 当场指定关注点与模型，而不是注册成四个持久 Agent。[Claude Code — code-review command](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md) [Code Review Plugin README](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md)

**社区一手事实。** oh-my-codex 将 prompt 定义、Skills、hooks、runtime state、routing 与 drift checks 作为一套系统维护，并用共享 contract 与回归检查约束不同 harness wrapper 的一致性；稳定身份来自 canonical agent id，而不是一次派发的 role/task label。[Prompt guidance contract](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/prompt-guidance-contract.md) [Codex native hooks](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/codex-native-hooks.md) [Contributing](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/CONTRIBUTING.md)

**社区一手事实。** wshobson/agents 也显式区分 domain-expert agents、渐进加载的 Skills，以及负责顺序与协作的 commands/orchestrators；项目从一套 `plugins/` 来源生成多种 harness 适配，并用 validation 与 PluginEval 做治理。[Architecture](https://github.com/wshobson/agents/blob/main/docs/architecture.md) [Harness adapters](https://github.com/wshobson/agents/blob/main/docs/harnesses.md) [PluginEval](https://github.com/wshobson/agents/blob/main/docs/plugin-eval.md)

**分析推断。** Anthropic 与 Superpowers 两个 code-review 一手实现都支持同一判断：一次 workflow 生成多个 reviewer leaf，只证明 workflow 有并行采样需求，不证明用户对多个持久角色有独立需求。oh-my-codex 与 wshobson/agents 的效果也不是“多建几个 Agent 就能获得”，而是 agent、workflow、runtime、适配器、验证与可观察性共同作用的结果。Issue #2 已明确不建设完整角色树、自动路由和 dashboard，因此不应只复制其 Agent catalog；这会拿到表面角色数量，却拿不到支撑它的状态与治理系统。

## 6. Matt `code-review` Skill：为什么两个 leaf role 暂不应成为全局 Agent

现有 `mattpocock-skills:code-review` Skill 已经定义：

- caller 提供 fixed point；workflow 统一校验 ref、三点 diff 与 commit list；
- workflow 按固定优先级发现 Spec，并发现 repo Standards；
- workflow 构造两份不同的任务包，明确用两个 `general-purpose` subagent 临时并行派发 Standards 与 Spec；
- 两轴独立呈现，禁止合并重排，并由 Lead 汇总。

Session 中重复出现 `standards` / `spec` task name，与这个既有 workflow 的叶子职责一致；但当前 Skill 明确使用 `general-purpose`，所以历史中的 `standards_reviewer` / `spec_reviewer` agent_type 不能在缺少 provenance 时归因给它。多数 dispatch message 又不可读，无法证明这些 leaf role 被其他 workflow 独立复用。

按 Session 证据强度，应把三层内容分开：`spawn_agent` / `agent_type` / `call_id` 计数是确定性工具事实；把 task name 聚成 Standards、Spec 或 audit 是 evaluator 判断；缺少 origin workflow 与可读任务正文是中性限制。即使某个 `agent_type` 被直接记录，也只能证明该配置被选中过，不能单独证明它由用户直接需要、存在独立调用方，或值得长期沉淀。

**分析推断。** 当前最小正确沉淀是继续深化 `code-review` Skill，把 leaf prompt、输出 schema 与错误处理留在 Skill 内。建立 `standards-reviewer` / `spec-reviewer` 全局 Agent 会产生四个问题：

1. 将一个 workflow 的内部实现误当成跨 workflow 身份；
2. 在 Agent 与 Skill 两处复制 source precedence、证据规则和输出合同；
3. 诱导固定模型/effort，破坏 V1 Profile 的动态成本选择；
4. 单独调用 leaf Agent 时缺少 fixed point、Spec 来源和聚合上下文，仍需 Lead 重写任务包。

只有当未来观察到同一 leaf contract 被至少两个独立 workflow 使用，并且确实需要相同的只读工具/MCP/权限隔离时，才重新评估项目级 Agent；即使通过，也不应默认 global。

## 7. Extraction gates

候选模式必须全部通过以下 gate，才进入 Custom Agent 实验：

| Gate | 可验证条件 | 未通过时的载体 |
| --- | --- | --- |
| 真实重复 | 至少 3 次可解读的真实派发，不能只靠相同 `task_name`；最好跨 2 个 workflow | recipe / 自包含任务包 |
| 合同稳定 | 输入、输出、权限、停止条件可一句话说明，样本无实质冲突 | Skill 中继续迭代 |
| 隔离收益 | 至少一种稳定差异：专属工具/MCP、只读权限、独立上下文或固定 system contract | Skill / workflow |
| 编排独立 | Agent 不需要知道前后阶段、重试轮次、汇总规则；这些由 Lead/Skill 持有 | workflow Skill |
| 成本解耦 | Agent 不绑定 `sol` / `luna` / `spark`；Lead 仍能显式选择 Profile/effort | 模型 Profile + task package |
| 作用域证据 | global 候选需在多个 repo 合同一致；repo 特有规范只能 project-scoped | 项目 Skill / Agent |
| 可测试 | 有正/负触发、权限、失败与真实运行 probe | 暂不持久化 |
| 可治理 | 单一合同来源、Git 版本、owner、变更说明与脱敏观测字段明确 | 暂不持久化 |

## 8. 对 Issue #2 的可执行建议

1. **首批不新增任务型 Custom Agent。** 保留 `sol` / `luna` / `spark` 为模型 Profile；把本轮 session 表格视为候选发现，不视为 Agent 使用量证明。
2. **将 `code-review` 判定为已沉淀的 workflow Skill。** `standards` / `spec` 保留为内部临时 task name，不建立全局 Agent。
3. **建立候选台账而非角色目录。** 每项记录真实样本、稳定/动态字段、隔离收益、调用它的 workflow 数量、建议作用域和 gate 状态。
4. **优先沉淀 dispatch recipe。** 对重复但证据仍弱的模式，先用自包含模板运行 3–5 次；每次显式选择 Profile、effort 和上下文。
5. **第一个 Agent 实验应选择“环境差异明显”的候选。** 例如始终只读、只用特定文档 MCP、输出固定证据格式，且在多个 workflow 复用；先项目级，再评估全局。
6. **保持 Lead 的 orchestration ownership。** 由 Lead/Skill 决定 spawn、并发、续派、重试、聚合和停止；Agent 不嵌套派生，不做隐式模型 fallback。
7. **用真实 probe 验收，不只解析配置。** 至少验证实际模型/effort、工具与权限、触发边界、失败返回和主线程可见结果。

最终判断：**Custom Agent 是“稳定 worker environment”的 Seam；Skill/workflow 是“稳定过程”的 Seam；Profile 是“模型资源”的 Seam；recipe 是尚未稳定模式的孵化器。** Issue #2 当前最有价值的动作是深化已有 Skill 与收集可解读样本，而不是从加密 session 的重复标签直接生成全局角色。
