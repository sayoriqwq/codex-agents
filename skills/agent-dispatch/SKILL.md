---
name: agent-dispatch
description: Operate as the user-selected Lead for an auditable Agent Dispatch workflow. Compile the Human request into an Engagement Contract, resolve material context, compare Handoff Cost, and either retain the work or identify a bounded Dispatch candidate. Use only when the user explicitly invokes $agent-dispatch.
---

# Agent Dispatch

Remain the user-selected Lead. Own intent, authority decisions, integration, verification, and final delivery; do not change the Lead's Model Profile.

## Run the workflow

1. Read [engagement-contract.md](references/engagement-contract.md) and compile the current Human request plus resolved governing context into one Engagement Contract.
2. Keep the raw Human request as the source record. Mark every added clause as explicit, inferred from one resolved context reference, or defaulted from standing authority.
3. Stop before action when a material reference, requirement, or authority boundary remains unresolved. Ask one focused clarification question and do not invent the missing context.
4. Read [placement.md](references/placement.md), identify the smallest Delegation Unit and its Work Shape, then compare Handoff Cost with the expected benefit of a Child.
5. Before the first effective action, emit one concise gate line: `Lead gate — readiness: <status>; placement: <retain|dispatch-candidate>; basis: <decisive factors>.`
6. Retain the work when coordination and verification would cost at least as much as direct Lead execution. Then inspect, change, and verify within the Engagement Contract.
7. Preserve a Lead-sourced work state containing the observed outcome, changes, validation evidence, material caveats, and basis for each fact.
8. Evaluate the result against the Engagement Contract before reporting. Delivery records only `reported_to_human`; never infer Human acknowledgement, approval, or issue closure.

Do not dump the full Contract into conversation unless the Human asks for it or auditing requires it. Surface readiness, the Placement Decision, material assumptions, and final evidence in concise language.

End with six compact fields, using `none` rather than omitting an empty field: `Outcome`, `Placement`, `Changes`, `Validation evidence`, `Material caveats`, and `Work-state source`. This keeps the Placement Decision observable even on surfaces that do not retain progress commentary.

## Current implementation frontier

This version implements clarification and direct Lead retention. If Dispatch has the lower expected completion cost, do not improvise an incomplete Child protocol or claim Handoff-Ready. Return a bounded summary with `dispatch_candidate_not_executed`, explain that the Delegation Contract slice is not installed yet, and stop.

Read [direct-retain-example.md](references/direct-retain-example.md) when the retain gate or output shape is unclear.
