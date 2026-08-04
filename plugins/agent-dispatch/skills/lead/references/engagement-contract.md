# Engagement Contract

Compile one Lead-owned Engagement Contract from the Human request and concrete governing context. Treat it as an auditable working interpretation, not as a Human acknowledgement of clauses the Lead inferred or defaulted.

## Required fields

| Field | Meaning |
| --- | --- |
| Raw Human request | Preserve the request verbatim as the source record. |
| Context references | Resolve phrases such as “the design we agreed” to concrete conversation turns or artifacts. |
| Current work layer | State whether the request is exploring, deciding, specifying, executing, validating, or reporting. |
| Goal | State the user-visible outcome before describing a method. |
| Success criteria | List observable conditions that would establish the outcome. |
| Authority boundaries | Separate allowed actions, approval requirements with their approving authority, and prohibited actions. A requirement never means approval was granted. |
| Priority order | Order correctness, evidence, latency, cost, and other material trade-offs. |
| Evidence requirements | State what the Lead must inspect or run before reporting. |
| Required Lead output | Require observed outcome, changes, validation evidence, material caveats, and work-state source as applicable. |
| Stop rules | State when to clarify, abstain, report a blocker, or stop. |
| Readiness | Use `ready_to_act` or `clarification_required` with material ambiguities. |
| Lead return | Record only Lead-sourced facts and `draft` or `reported_to_human` delivery status. |

## Clause provenance

- Use `explicit` only for a clause stated by the Human.
- Use `inferred` only when its basis names a resolved context reference.
- Use `defaulted` only for standing developer authority, safety policy, or workflow invariants already available to the Lead.
- Keep unresolved material references unresolved. Do not convert them into empty context or a guessed requirement.

## Readiness

Set `clarification_required` and stop when an unresolved fact could materially change the goal, Work Shape, scope, authority, success criteria, or evidence demand. Non-material implementation choices may remain open for the executing Lead.

## Evaluation and delivery

Before delivery, compare the Lead-sourced work state against every success criterion, authority boundary, evidence requirement, required output field, and stop rule. Report gaps rather than filling them with claims. Delivery means only that the Lead reported to the Human; the Human response remains outside the Contract until actually expressed.

The versioned wire shape and public validator live in the plugin source repository's TypeScript protocol Module and are not guaranteed to be available in the active workspace; the plugin does not currently expose that validator as a runtime tool. Its structural JSON Schema proves transport shape only. `parseEngagementContractV1` and `safeParseEngagementContractV1` additionally enforce the mechanically expressible readiness and provenance invariants; neither proves semantic truth.
