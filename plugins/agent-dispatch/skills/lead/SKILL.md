---
name: lead
description: Run an auditable Human-to-Lead engagement and retain-or-dispatch gate with explicit Model Profile selection. Use only when the user invokes $agent-dispatch:lead.
---

# Agent Dispatch

Keep the Human-selected Lead and its Model Profile stable while the Lead owns the work. The Lead owns intent, authority decisions, integration, verification, and final delivery.

## Run

1. Read [engagement-contract.md](references/engagement-contract.md). Compile the raw Human request and resolved governing context into one Engagement Contract. Complete this step only when every added clause has provenance and readiness is either `ready_to_act` or `clarification_required` with every material ambiguity named.
2. When clarification is required, emit the gate with `placement: none; profile: none; model: none`, ask one focused question, and stop. Complete this branch before any effective action.
3. When ready, read [placement.md](references/placement.md). Identify the smallest independently verifiable Delegation Unit, its Work Shape, and the decisive Handoff Cost factors. Complete this step only when the record supports exactly one Placement Decision: `retain` or `dispatch-candidate`.
4. Route the decision. For `retain`, record `profile: Lead Selection unchanged; model: Lead Selection unchanged`. For `dispatch-candidate`, read [profile-selection.md](references/profile-selection.md) and complete its Profile Selection record. Complete this step only when every ready Placement Decision has explicit profile and model values, including the exact Child model for a candidate.
5. Before the first effective action, emit: `Lead gate — readiness: <status>; placement: <decision>; profile: <profile>; model: <model>; basis: <decisive factors>.`
6. Follow exactly one branch:
   - `retain`: inspect, change, and verify within the Engagement Contract.
   - `dispatch-candidate`: leave Execution Custody with the Lead and perform no Child work. Record `dispatch_candidate_not_executed`, the bounded Delegation Unit, and its Profile Selection. This release has no installed Delegation Contract or Handoff-Back branch.
7. Preserve a Lead-sourced work state containing the observed outcome, changes, validation evidence, material caveats, and basis for every fact.
8. Evaluate that work state against every Contract success criterion, authority boundary, evidence requirement, required output, and stop rule. Complete this step only when each item is satisfied or reported as a gap.
9. Report delivery as `reported_to_human`. Human acknowledgement, approval, and issue closure remain unclaimed until the Human expresses them.

Keep the full Contract internal unless the Human asks for it or auditing requires it. Surface readiness, the Placement Decision, material assumptions, and final evidence in concise language.

End with six compact fields, using `none` rather than omitting an empty field: `Outcome`, `Placement`, `Changes`, `Validation evidence`, `Material caveats`, and `Work-state source`. In `Placement`, include the decision, Work Shape, profile, exact Child model when applicable, and any Affinity Override so routing remains observable when progress commentary is unavailable.

Read [direct-retain-example.md](references/direct-retain-example.md) when the retain gate or output shape is unclear.
