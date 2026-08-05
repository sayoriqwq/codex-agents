# Profile Selection

Read this reference only after Placement is `dispatch-candidate` and before emitting the Lead gate. A Profile is a model resource; place the Child's task role inside its bounded task package.

## Route by affinity

Start from the Delegation Unit's Work Shape:

| Work Shape | Model Affinity | Expected model | Use when |
| --- | --- | --- | --- |
| `Judgment` | `sol` | `gpt-5.6-sol` | Interpretation, trade-offs, cross-domain understanding, or high-consequence decisions remain. |
| `Execution` | `luna` | `gpt-5.6-luna` | Goal, scope, authority, and acceptance are fixed; only bounded local judgment remains. |
| `Mechanical` | `spark` | `gpt-5.3-codex-spark` | The rule is complete and enumerable, and the result is quickly verifiable. |

Apply concrete Routing Factors after affinity. Ambiguity, high error consequence, broad context reconstruction, or unresolved semantic judgment can move a unit to `sol`. A fully fixed and bounded unit can move from `sol` to `luna`. Record every departure as an Affinity Override with its factor and accepted trade-off.

Use an installed Profile—`sol`, `luna`, or `spark`—as the Child agent type. Confirm that its installed definition resolves to the expected model in the table; a Profile name alone is not model evidence. If the Profile is unavailable or its model cannot be confirmed, report that gap and stop at `dispatch_candidate_not_executed`. When only `spark` is unavailable, an explicit `luna` fallback is valid if the unit still satisfies the `Execution` boundary; record the fallback as an Affinity Override.

## Keep runtime choices explicit

Choose reasoning effort independently from Profile. Default to zero inherited history plus a self-contained task package. Use recent or full history only when it reduces reconstruction cost enough to justify the larger context.

A complete Profile Selection record contains every field:

- `model_affinity`: the Work Shape mapping above;
- `selected_profile`: exactly one installed Profile name;
- `selected_model`: the exact model ID confirmed from the installed Profile definition;
- `reasoning_effort`: an explicit effort value;
- `context_strategy`: zero-history, recent-history, or full-history, with a reason for non-default history;
- `routing_factors`: the concrete facts considered;
- `affinity_override`: `none` or the factor and accepted trade-off;
- `availability_evidence`: how the Lead confirmed both Profile callability and its model mapping.

Profile Selection is complete only when all eight fields are present, `selected_model` matches the installed Profile, and the task role remains in the Delegation Unit rather than replacing `selected_profile`.
