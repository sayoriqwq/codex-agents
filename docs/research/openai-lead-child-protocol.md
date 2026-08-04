# OpenAI 官方协议对 Lead–Child 单一双向契约的约束

> 状态：研究记录，不是规范；项目已据此将 Child 合同定名为 `Delegation Contract`，其他字段命名与落地格式仍需确认。
>
> 检索日期：2026-08-04（Asia/Shanghai）

## Source boundary

本文只把 OpenAI 官方公开资料作为“官方事实”的来源：`developers.openai.com` 的 API / Agents SDK 文档，以及 `learn.chatgpt.com` 的 Codex 文档。没有把社区文章、会话样本或本项目既有设计当作 OpenAI 协议事实。Responses Multi-agent 仍是 beta，item schema 可能变化，因此这里记录的是检索日可见边界，而不是永久兼容承诺。

下文严格区分：

- **官方事实**：可由就近链接直接核对的产品、模型或 API 行为。
- **本项目推断**：为 Lead-centered single bidirectional contract 做的设计解释，不代表 OpenAI 的命名或规范。

## 结论摘要

1. GPT-5.6 更适合“结果、约束、证据、完成标准明确，路径留给模型”的契约；不适合把 handoff 写成冗长步骤剧本。
2. 本地 Codex 与 Responses Multi-agent beta 是两个不同执行面：前者允许每个 custom agent 覆盖模型与推理强度，后者整棵 agent 树共享请求的模型与工具。
3. 若 Lead 必须保留最终接纳权，本项目语义更接近 Agents SDK 的 **agents-as-tools** 或 Responses Multi-agent 的 root synthesis，而不是 Agents SDK 的 **handoff**。
4. 单一 `Delegation Contract` 应同时表达“Lead 期望的终态/边界/证据”和“Child 实际达到的状态/变更/证据”；任何退出都返回可检查状态，不把 `completed` 字样等同于 Lead 接纳。
5. 协议需要结构化，但 JSON Schema 只保证形状，不保证事实正确；必须配套验证、trace 与 eval。

## 1. GPT-5.6 prompting guidance

### 官方事实

GPT-5.6 的官方指导首先要求简化 prompt：保留用户可见结果、成功标准、停止条件、安全/权限/证据约束、必要的工具路由与输出形状；删除重复规则、无行为差异的示例和无关工具。官方还强调冲突规则比缺少细节更容易制造不稳定。[Prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)

官方建议 outcome-first：描述“什么结果算好”，通常让模型自行选择搜索、工具和推理路径；绝对词只用于真正不变量，判断场景使用决策规则，并显式给出 retry、fallback、ask、abstain、stop 的条件。[Outcome-first prompts and stopping conditions](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#outcome-first-prompts-and-stopping-conditions)

自主性与批准边界应集中写一次，并区分 read/review/diagnose/plan 与 change/build/fix；外部写入、破坏性操作、购买或实质扩展范围应停下确认。长任务还应明确当前工作层，例如 research、design、implementation、review 或 external coordination。[Define autonomy and approval boundaries](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#define-autonomy-and-approval-boundaries)

复杂任务的推荐 prompt 骨架是短小的 Role、Personality、Goal、Success criteria、Constraints、Tools、Output、Stop rules。长任务应只在首个工具调用前和重大阶段变化时给稀疏进度更新，不逐步旁白；历史回放要保留 assistant `phase`，compaction 后保持 prompt 功能一致，并把 compacted item 当作 opaque state。[Suggested prompt structure](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#suggested-prompt-structure) [Long-running workflows and state](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#long-running-workflows-and-state)

推理强度不应全局拉高。官方建议先保持基线，在代表性任务上比较同档与低一档；`low` 用于质量不受损的延迟敏感任务，`medium` 是平衡起点，`high` / `xhigh` 只在 eval 显示显著收益时使用，`max` 留给最难的质量优先任务。[Reasoning effort](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#reasoning-effort)

完成前应提供可执行验证工具并说明验证标准；若验证无法运行，要说明原因和次优检查。[Check work before finishing](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#check-work-before-finishing)

### 本项目推断

- Lead→Child 不应规定一般性的逐步流程；核心应是终态、不可改写的依据、权限/范围/停止边界和接纳所需证据。
- “聪明模型放在高杠杆决策点，廉价模型做有界执行”与官方 reasoning-effort 建议一致，但具体 Sol/Luna/Spark affinity 必须靠本项目 eval 证明，不能从文档直接推出。
- 每次 Child 退出都应有 stop rule 和状态回传；否则 timeout、partial 或 validation failure 会落到自然语言猜测。

## 2. Codex local：subagents、custom agents 与 hooks

### 官方事实

Codex 的 subagent 适合并行、独立、边界清楚的探索、测试或实现工作；代价是每个 subagent 都会消耗自己的模型与工具 token。主线程应保留需求、决策和最终输出，Child 返回摘要而不是把噪声中间输出灌回主线程。[Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

本地 Codex 内置 `default`、`worker`、`explorer`。个人 custom agents 放在 `~/.codex/agents/`，项目级放在 `.codex/agents/`；每个 TOML 至少定义 `name`、`description`、`developer_instructions`。custom agent 可以覆盖普通 session config，包括 `model`、`model_reasoning_effort`、`sandbox_mode`、`mcp_servers` 和 skills 配置。[Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)

模型与推理强度按字段独立解析：custom agent 文件值优先；否则依次使用显式 spawn 值、`[agents]` 默认值、父 agent 值。显式 spawn model/effort 也可覆盖全局 subagent 默认值。因此本地 Codex **可以在同一 Lead 树中使用异构 model/profile**。[Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference#configtoml)

Codex hooks 是生命周期扩展点，可观测 `SubagentStart`、`SubagentStop`、`PreCompact`、`PostCompact`、`Stop` 等事件，也可用于日志、分析和停止时验证。多个匹配的 command hooks 会并发启动；hook 需要独立信任与安全边界，不能把它当成天然串行的事务协调器。[Codex Hooks](https://learn.chatgpt.com/docs/hooks)

`SubagentStart` 可以给 Child 增加 developer context；`SubagentStop` 能读取 Child 的 agent id/type、transcript path 和最后一条 assistant message，并可要求 Child 继续一次。官方同时说明 transcript 格式不是稳定接口，因此 hook 可以做 V1.1 的轻量回传校验与观测，但不应把 transcript JSONL 当成长期业务 schema。[SubagentStart](https://learn.chatgpt.com/docs/hooks#subagentstart) [SubagentStop](https://learn.chatgpt.com/docs/hooks#subagentstop)

`agents.interrupt_message` 默认开启，会把 turn 被中断这一事实写成模型可见消息；custom agent 未覆盖的 sandbox 等 session 设置从父级继承。[Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference#configtoml)

### 本项目推断

- V1.1 可以先把 custom agent 用作“模型/推理强度/权限/工具配置层”，而不是先沉淀大量 task-name reviewer。
- hooks 适合记录 Placement、spawn、stop、compact、validation 等事件，为成本、延迟和失败归因提供观测；语义接纳仍由 Lead 做，不能交给 hook 名称或 Child 的结束状态。
- 本地异构能力是本项目 model affinity 的直接执行基础；但 affinity override 原因需要额外记录，Codex 配置优先级本身不会解释为什么偏离默认。

## 3. Responses Multi-agent beta

### 官方事实

Responses Multi-agent 是 GPT-5.6 系列的 beta。root agent 可以生成 subagent 树，subagents 各有独立、聚焦的上下文；root 负责综合 Child 输出并生成最终回答。该模式适合独立并行工作，不适合严格顺序链、共享可变状态争用、单个慢外部操作或要求固定确定性执行图的任务。[Responses Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent)

关键限制：**整棵树共享同一个 Responses 请求的 model 和 available tools**。所有 agent 都能访问该请求配置的工具，不能像本地 Codex custom agent 那样给不同 Child 选择 Sol/Luna/Spark。[Responses Multi-agent quickstart](https://developers.openai.com/api/docs/guides/responses-multi-agent#quickstart) [How Multi-agent works](https://developers.openai.com/api/docs/guides/responses-multi-agent#how-multi-agent-works)

运行时提供 `spawn_agent`、`send_message`、`followup_task`、`wait_agent`、`interrupt_agent`、`list_agents` 六种 hosted coordination actions；应用不执行这些 `multi_agent_call`，但仍要执行任意 agent 发出的 developer-defined `function_call` 并回传匹配的 `function_call_output`。`interrupt_agent` 中断 active turn，但不删除该 agent 的上下文。[How Multi-agent works](https://developers.openai.com/api/docs/guides/responses-multi-agent#how-multi-agent-works)

Responses beta 新增 `multi_agent_call`、`multi_agent_call_output` 与 `agent_message` items；`call_id` 关联调用及其结果，`author` / `recipient` 记录消息方向。官方注入给 Child 的 developer instructions 只规定 final 会立即交付 parent，并没有规定 claimed-complete、partial、interrupted 等退出的统一业务 envelope。[New Multi-agent output items](https://developers.openai.com/api/docs/guides/responses-multi-agent#new-multi-agent-output-items) [Multi-agent prompt guidance](https://developers.openai.com/api/docs/guides/responses-multi-agent#prompt-guidance)

默认 `max_concurrent_subagents=3`，限制覆盖整个树的活跃 descendants，不含 root；文档未设固定树深或总创建数上限。启用 Multi-agent 时，会对 root 与每个 subagent 的独立上下文隐式启用 server-side compaction；`reasoning.summary` 当前不支持。[Responses Multi-agent limitations](https://developers.openai.com/api/docs/guides/responses-multi-agent#limitations)

HTTP 会等待所有 active agents 完成或暂停等待 client function call 后结束本次 response；WebSocket 可逐个注入 function outputs，使等待的 agent 更早恢复。官方因此认为多数多 agent 工作流 WebSocket 更可能降低端到端延迟。[Using Multi-agent in Responses API](https://developers.openai.com/api/docs/guides/responses-multi-agent#using-multi-agent-in-responses-api)

### 本项目推断

- Responses beta 可以承载“同模型的上下文隔离与并行”，不能承载本项目最关键的异构成本路由；若要 Sol Lead + Luna/Spark Child，需要本地 Codex 或应用自建多请求 orchestration。
- Responses 的 root synthesis 与“Lead 保留 Acceptance Authority”方向一致，但其 output item 不是本项目业务契约；仍需在 agent message 或 function schema 中承载期望与回传状态。
- 没有固定总 agent 数/深度不等于应该无限派发。本项目仍应由 Placement Gate、handoff cost 和 concurrency budget 约束。

## 4. Agents SDK：handoff 与 agents-as-tools

### 官方事实

Agents SDK 明确区分两种模式：

| 官方模式 | 回复所有权 |
| --- | --- |
| `handoff` | 控制转移到 specialist，specialist 接管该分支的下一响应 |
| `agent.as_tool()` / `agent.asTool()` | manager 保持控制，把 specialist 当作有界能力调用 |

当 manager 应综合最终回答、specialist 只做总结/分类等有界任务时，官方建议 agents-as-tools；只有 specialist 应真正接管对话分支时才用 handoff。官方也建议先从单 agent 开始，只有 capability isolation、policy isolation、prompt clarity 或 trace legibility 有实质改善时再增加 specialist。[Agents SDK orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration)

Agents SDK 的 run result 不只有 final output，还可包含 history、最后掌控 agent、server response id、interruptions 与 resumable state。审批导致的 interrupted run 可能没有 final output；它返回 pending interruptions 与可恢复 state，而不是假装完成。[Agents SDK results and state](https://developers.openai.com/api/docs/guides/agents/results)

### 命名冲突（必须保留）

本项目当前所说的 `Handoff` 是“Lead 把 Execution Custody 交给 Child，但 Lead 保留 Acceptance Authority”；Agents SDK 的 `handoff` 则是“回复/控制所有权转移到 specialist”。两者不是同义词。

Codex 产品词汇还把 `Handoff` 用于把一个 chat 及其工作在 Local 与 Worktree 之间移动。这是第三种官方语义，也与本项目的 Lead→Child custody transfer 不同。[Codex glossary](https://learn.chatgpt.com/docs/glossary) [Worktrees and Handoff](https://learn.chatgpt.com/docs/environments/git-worktrees)

### 本项目决策与推断

- 本项目已将 Lead↔Child 的单一双向合同改名为 `Delegation Contract`，不再使用 `Handoff Contract`。
- 从控制权结构看，本项目的单一双向契约更接近 agents-as-tools：Child 是 bounded capability，Lead 负责综合、验证与最终接纳。
- `Handoff` / `Handoff-Back` 等事件词是否一并替换仍是独立词汇决策，不能由合同改名自动推导。

## 5. Function calling 与 Structured Outputs

### 官方事实

function calling 的基本协议是：模型输出带 `call_id` 的 function call，应用执行工具，再返回与该调用匹配的 function call output，模型继续完成响应。函数工具输入由 JSON Schema 定义。[Function calling](https://developers.openai.com/api/docs/guides/function-calling)

官方建议函数工具启用 `strict: true`。strict object schema 要求所有 properties 都列入 `required`，每个 object 都设置 `additionalProperties: false`；需要表达可缺失值时用包含 `null` 的类型。这个约束适合统一 envelope 的机器形状，但不能代替 Lead 的语义验收。[Function calling strict mode](https://developers.openai.com/api/docs/guides/function-calling#strict-mode)

Structured Outputs 能约束输出遵守所给 JSON Schema，并支持显式、可程序检测的 refusal。官方建议：连接系统工具/数据时使用 function calling；约束模型最终用户响应时使用 `text.format` / JSON Schema response format。[Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

### 本项目推断

- 单一双向契约适合一个版本化 schema，而不是 Lead→Child 和 Child→Lead 两套漂移的自然语言模板。
- Schema 应能区分“指派侧字段”和“回传侧字段”，并容纳 partial、blocked、interrupted、validation-failed 等当前状态；但最终字段名仍待域模型确认。
- Structured Outputs 保证 schema adherence，不保证事实、证据质量或任务完成。Lead 必须用测试、文件 diff、引用或其他观测证据做接纳。

## 6. Conversation state、compaction 与 interruption

### 官方事实

Responses 可通过显式重放全部历史、`previous_response_id` 或 Conversations 管理状态。若应用自行重放 reasoning model 历史，应保留 response `output` 数组里的所有 items（包括 reasoning items）和 assistant `phase`；不能只保留最终文本。[Conversation state](https://developers.openai.com/api/docs/guides/conversation-state)

compaction 用于长交互中的质量、成本和延迟平衡。server-side compaction 返回 opaque encrypted compaction item；stateless chaining 必须继续携带它，standalone `/responses/compact` 的输出是 canonical next context，应原样传给下一次请求，不能自行摘要替换。[Compaction](https://developers.openai.com/api/docs/guides/compaction)

长响应可以用 background mode 异步执行、轮询并取消，避免连接中断等同于任务结果；终态需要从 response status 判断。[Background mode](https://developers.openai.com/api/docs/guides/background)

Agents SDK 的 approval interruption 返回 resumable state 而不是 final answer；Codex 的 agent interrupt 会保留 Child context，并可记录模型可见的 interruption message。[Agents SDK results and state](https://developers.openai.com/api/docs/guides/agents/results) [Responses Multi-agent coordination](https://developers.openai.com/api/docs/guides/responses-multi-agent#how-multi-agent-works) [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference#configtoml)

### 本项目推断

- “connection/turn ended”“Child 发出完成文本”“Lead 接纳”必须是三个不同状态。
- partial、timeout、interrupt、readiness rejection 与 validation failure 可以统一走同一个 Child→Lead 返回通道，因为运行时都能携带 current state；Lead 再决定 retain、redispatch、clarify 或 accept。
- timeout、crash 或外部终止时，Child 可能根本来不及生成回传。此时 orchestrator 应按同一 envelope 合成最小记录并标明 `source=runtime`，不能把运行时观察伪装成 Child 声明。
- compaction item 不是业务 handoff report。可恢复运行时状态与 Lead 接纳所需的业务证据应分层保存。

## 7. Tracing 与 evals

### 官方事实

Agents SDK 内建 traces 覆盖 model calls、tools、agents、guardrails 和 handoffs；Responses API 原生提供 response objects 与 API logs。[Agents SDK vs. Responses API](https://developers.openai.com/api/docs/guides/agents#compare-the-responses-api-and-agents-sdk)

Trace grading 对端到端 decisions、tool calls、reasoning steps 的 trace 赋结构化分数或标签；trace evals 用多条 graded traces 比较变更、发现回归并定位 orchestration/behavior 问题。官方建议对代表性运行建立 grader 和 eval run，而不只看最终文本。[Trace grading](https://developers.openai.com/api/docs/guides/trace-grading)

### 本项目推断

至少应观测：Placement 决策、Lead/Child profile、affinity override 及理由、上下文包大小、排队/执行/总延迟、token/cost、Child 退出状态、验证结果、Lead 最终处置、是否亲自介入。

评估必须同时覆盖：

- 质量：目标是否满足、证据是否足够、验证是否通过；
- 路由：是否该派、是否选对 profile、override 是否合理；
- 效率：端到端时间、模型思考时间、重试/再派发次数、token 与费用；
- 协议：Child 是否完整返回当前状态，Lead 是否把“claimed complete”错误当成 accepted。

若后续使用 Programmatic Tool Calling 或其他结构化执行面，还要分别验收原生 program/tool output 与最终 assistant message；官方明确指出前者正确并不保证后者保留了必需字段、引用或 caveat。[Assess the final answer](https://developers.openai.com/api/docs/guides/latest-model#assess-the-final-answer)

## 8. 对单一双向契约的映射（字段名待确认）

下面只是语义槽位，不在本研究里固化最终域词：

| Lead 发出时需要表达 | Child 返回时需要表达 | Lead 的比较问题 |
| --- | --- | --- |
| 期望终态 | 当前实际状态 | 哪些 postconditions 已达到，哪些仍缺失？ |
| 不可改写的规范、决策与证据基础 | 对基础材料的发现、冲突或缺口 | Child 是否在正确依据上执行？ |
| 工作形态、范围、权限与停止边界 | 实际变更、触碰范围与越界风险 | 执行 custody 是否保持有界？ |
| 接纳所需证据与验证标准 | 实际证据、检查结果与未运行项 | Lead 是否已经有足够依据接纳？ |

运行时参数（model/profile、reasoning effort、并发、context fork 方式、sandbox/tools）应与这四类业务语义分层：前者解释“用什么算力与环境执行”，后者解释“为什么派、要求什么、凭什么接纳”。这样既允许 Lead 在上下文转移成本过高时直接收口，也允许在 spec 已稳定、执行已 bounded 时把 custody 交给更快或更便宜的 Child。

## 9. 仍需项目决策的问题

1. Human↔Lead 的合同采用什么正式名称与字段？
2. 上表四组语义是 schema 的必填字段、条件必填字段，还是由 Work Shape 决定的 profile？
3. 哪些 Child 退出字段必须由运行时自动填充，避免 Child 自报状态造成证据污染？
4. Lead 介入权重如何记录：规则、可解释分数，还是仅作为 dispatcher 的决策因子？
5. V1.1 的执行面只支持本地 Codex 异构 profile，还是同时定义 Responses beta 的同模型降级路径？
