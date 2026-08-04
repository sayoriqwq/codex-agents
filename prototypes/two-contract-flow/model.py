"""PROTOTYPE — pure state model for a Human→Lead→Child two-contract flow.

Question: can one concrete request preserve Human intent in an Engagement
Contract while a Lead independently owns a bidirectional Delegation Contract,
including readiness, runtime-synthesized returns, and separate acceptance?
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable


HUMAN_PROMPT = (
    "把刚才定下来的 Child timeout 方案做掉。public dispatch API 不要动，"
    "尽快，但验证不能省。"
)

REQUIRED_CONDITIONS = [
    "timeout_adapter_implemented",
    "runtime_provenance_verified",
    "public_api_unchanged",
]


def initial_state() -> dict[str, Any]:
    return {
        "prototype": "THROWAWAY — two-contract-flow",
        "question": "Can two nested contracts keep intent, execution, and acceptance separate?",
        "phase": "human_prompt_received",
        "raw_human_prompt": HUMAN_PROMPT,
        "available_lead_context": {
            "accepted-context:timeout-return-v1": {
                "status": "resolved",
                "prompt_reference": "刚才定下来的 Child timeout 方案",
                "claims": [
                    "every Child exit returns custody through one transition",
                    "runtime synthesizes a minimal sourced observation when no Child report exists",
                ],
                "artifact_refs": [
                    "docs/adr/0003-all-child-exits-use-handoff-back.md",
                    "docs/research/openai-lead-child-protocol.md:133",
                ],
            },
        },
        "engagement_contract": None,
        "engagement_evaluation": None,
        "initial_placement": None,
        "delegation_contract": None,
        "delegation_return_metadata": None,
        "delegation_evaluation": None,
        "intervention_signal": {"level": "baseline", "signals": []},
        "placement_reconsideration": None,
        "lead_resolution": None,
        "lead_disposition": None,
        "events": ["Human prompt received; no semantic contract compiled yet."],
    }


def _event(state: dict[str, Any], message: str) -> dict[str, Any]:
    state["events"].append(message)
    return state


def _guard(state: dict[str, Any], phases: set[str], action: str) -> bool:
    if state["phase"] in phases:
        return True
    _event(state, f"Rejected {action}: illegal while phase={state['phase']}.")
    return False


def _sourced(value: Any, source: str, basis: str) -> dict[str, Any]:
    return {"value": value, "source": source, "basis": basis}


def _value(field: dict[str, Any]) -> Any:
    return field["value"]


def compile_engagement(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"human_prompt_received"}, "compile_engagement"):
        return state

    referenced_context_id = "accepted-context:timeout-return-v1"
    referenced_context = state["available_lead_context"].get(referenced_context_id)
    context_resolved = referenced_context is not None and referenced_context["status"] == "resolved"
    material_ambiguities = [] if context_resolved else [
        "The phrase '刚才定下来的 Child timeout 方案' has no resolvable Lead context."
    ]

    state["engagement_contract"] = {
        "contract_name": "Engagement Contract",
        "parties": {
            "request_authority": "human",
            "contract_owner": "lead",
            "execution_owner": "lead",
            "reporting_authority": "lead",
        },
        "readiness": {
            "status": "ready_to_act" if context_resolved else "clarification_required",
            "material_ambiguities": material_ambiguities,
        },
        "prompt_reference_resolution": {
            "phrase": "刚才定下来的 Child timeout 方案",
            "context_id": referenced_context_id,
            "status": "resolved" if context_resolved else "unresolved",
            "artifact_refs": referenced_context["artifact_refs"] if context_resolved else [],
        },
        "request": {
            "current_layer": "implementation",
            "goal": "Implement the agreed timeout-return behavior with runtime provenance.",
            "success_criteria": [
                {"id": "timeout_adapter_implemented", "text": "timeout adapter implements the agreed return"},
                {"id": "runtime_provenance_verified", "text": "runtime provenance is verified"},
                {"id": "public_api_unchanged", "text": "public dispatch API remains unchanged"},
                {"id": "targeted_tests_passed", "text": "targeted timeout validation passes"},
            ],
            "governing_context": (
                [f"{referenced_context_id}: {claim}" for claim in referenced_context["claims"]]
                if context_resolved
                else []
            ),
            "authority_and_constraints": {
                "allowed": ["inspect local code", "edit in-scope implementation", "run local tests"],
                "must_stop": ["public API change", "external write", "destructive action", "scope expansion"],
            },
            "priority_order": ["correctness and evidence", "wall-clock time", "token/cost efficiency"],
            "required_lead_output": [
                "observed_outcome",
                "changes",
                "validation_evidence",
                "material_caveats",
            ],
            "stop_rules": [
                "ask only if ambiguity materially changes outcome or authority",
                "report a blocker if the public API must change",
            ],
        },
        "clause_provenance": {
            "public_api_unchanged": "explicit: Human prompt",
            "latency_after_validation": "explicit: Human prompt",
            "runtime_provenance": f"inferred: {referenced_context_id}",
            "safe_local_authority": "defaulted: developer autonomy policy",
        },
        "lead_return": None,
    }
    state["phase"] = "engagement_ready"
    message = (
        "Lead compiled explicit, inferred, and defaulted clauses from a resolved context reference."
        if context_resolved
        else "Lead compiled the known clauses but marked the unresolved context reference for clarification."
    )
    return _event(state, message)


def retain_direct(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"engagement_ready"}, "retain_direct"):
        return state
    if state["engagement_contract"]["readiness"]["status"] != "ready_to_act":
        return _event(state, "Placement blocked: Engagement Contract requires Human clarification.")

    state["initial_placement"] = {
        "decision": "retain",
        "work_shape": "Execution",
        "selected_profile": "Lead Selection (unchanged)",
        "model_affinity": "Lead Selection remains stable while the Lead owns the work",
        "context_fork": "none",
        "handoff_cost": {
            "assessment": "outweighs expected Child benefit",
            "factors": [
                "Lead already holds the accepted design history",
                "a Child would reconstruct the same context",
                "Lead must repeat semantic verification before delivery",
            ],
        },
        "reason": "direct Lead execution has the lowest expected total completion cost",
    }
    state["lead_disposition"] = "retain"
    state["phase"] = "lead_has_custody"
    return _event(state, "Lead retained the Handoff-Ready unit after an explicit Placement Decision.")


def dispatch(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"engagement_ready"}, "dispatch"):
        return state
    if state["engagement_contract"]["readiness"]["status"] != "ready_to_act":
        return _event(state, "Dispatch blocked: Engagement Contract requires Human clarification.")

    state["initial_placement"] = {
        "decision": "dispatch",
        "work_shape": "Execution",
        "selected_profile": "Luna",
        "model_affinity": "Execution → Luna",
        "context_fork": "bounded artifact references",
        "reason": "intent and acceptance are stable; the implementation boundary is narrow",
    }
    state["delegation_contract"] = {
        "contract_id": "dc-1",
        "owner": "lead",
        "acceptance_authority": "lead",
        "execution_custody": "not_acquired",
        "child_readiness": None,
        "expectation": {
            "target_state": {
                "summary": "A timeout adapter emits the agreed return shape with runtime provenance.",
                "required_conditions": REQUIRED_CONDITIONS,
            },
            "governing_basis": [
                "ADR-0003 is fixed",
                "runtime-synthesized provenance is fixed",
                "the existing public dispatch API is fixed",
            ],
            "custody_bounds": {
                "current_layer": "implementation",
                "allowed": ["timeout adapter", "targeted tests", "local validation"],
                "forbidden": ["public dispatch API", "scheduler refactor", "external writes"],
                "return_when": ["target reached", "validation fails", "boundary encountered", "interrupted"],
            },
            "evidence_demand": [
                "targeted timeout tests pass",
                "changed artifacts are named",
                "public dispatch API surface is compared",
                "unknown or unrun checks retain provenance",
            ],
        },
        "observation": None,
    }
    state["phase"] = "delegation_offered"
    return _event(state, "Lead created a Child and offered dc-1; Execution Custody has not transferred.")


def child_begin(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"delegation_offered"}, "child_begin"):
        return state
    contract = state["delegation_contract"]
    contract["child_readiness"] = {
        "status": "ready",
        "basis": ["target understandable", "scope and authority bounded", "evidence demand executable"],
    }
    contract["execution_custody"] = "child"
    state["phase"] = "child_active"
    return _event(state, "Child performed its first effective action: Implicit Acceptance transferred Execution Custody.")


def _return_observation(
    state: dict[str, Any],
    *,
    source: str,
    trigger: str,
    label: str,
    conditions: list[str] | None,
    open_conditions: list[str],
    findings: list[str] | None,
    delta: list[str] | None,
    tests: str | None,
    artifacts: list[str] | None,
    unrun_checks: list[str] | None,
    boundary_breaches: list[str] | None,
    basis: str,
    allowed_phases: set[str],
) -> dict[str, Any]:
    if not _guard(state, allowed_phases, trigger):
        return state

    contract = state["delegation_contract"]
    custody_acquired = contract["execution_custody"] == "child"
    contract["observation"] = {
        "current_state": {
            "label": _sourced(label, source, basis),
            "observed_conditions": _sourced(conditions, source, basis),
            "open_conditions": _sourced(open_conditions, source, basis),
        },
        "basis_findings": _sourced(findings, source, basis),
        "state_delta": _sourced(delta, source, basis),
        "observed_evidence": {
            "targeted_tests": _sourced(tests, source, basis),
            "artifact_refs": _sourced(artifacts, source, basis),
            "unrun_checks": _sourced(unrun_checks, source, basis),
        },
        "boundary_breaches": _sourced(boundary_breaches, source, basis),
    }
    contract["execution_custody"] = "lead"
    state["delegation_return_metadata"] = {
        "source": source,
        "trigger": trigger,
        "contract_id": contract["contract_id"],
        "custody_acquired": custody_acquired,
    }
    state["phase"] = "delegation_returned"
    return _event(state, f"One provisional delegation-return event arrived: source={source}, trigger={trigger}.")


def readiness_reject(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"delegation_offered"}, "readiness_reject"):
        return state
    state["delegation_contract"]["child_readiness"] = {
        "status": "rejected",
        "basis": ["required implementation artifact was not identified"],
    }
    return _return_observation(
        state,
        source="child",
        trigger="readiness_rejected",
        label="not_started",
        conditions=[],
        open_conditions=REQUIRED_CONDITIONS,
        findings=["The contract lacks the implementation artifact entry point."],
        delta=[],
        tests="not_run",
        artifacts=[],
        unrun_checks=["all: readiness failed before first effective action"],
        boundary_breaches=[],
        basis="Child readiness report",
        allowed_phases={"delegation_offered"},
    )


def child_clean(state: dict[str, Any]) -> dict[str, Any]:
    return _return_observation(
        state,
        source="child",
        trigger="claimed_complete",
        label="target_reached",
        conditions=REQUIRED_CONDITIONS,
        open_conditions=[],
        findings=["The adapter boundary was sufficient; no governing assumption changed."],
        delta=["timeout_adapter.py", "test_timeout_return.py"],
        tests="passed",
        artifacts=["targeted-test-log:timeout-return", "api-surface-diff:none"],
        unrun_checks=["full suite: outside bounded change"],
        boundary_breaches=[],
        basis="Child final report with artifact references",
        allowed_phases={"child_active"},
    )


def child_partial(state: dict[str, Any]) -> dict[str, Any]:
    return _return_observation(
        state,
        source="child",
        trigger="validation_failed",
        label="partial",
        conditions=["timeout_adapter_implemented", "public_api_unchanged"],
        open_conditions=["runtime_provenance_verified", "targeted timeout validation"],
        findings=["The existing serializer drops runtime provenance."],
        delta=["timeout_adapter.py"],
        tests="failed",
        artifacts=["targeted-test-log:provenance-failure"],
        unrun_checks=["full suite: targeted test failed first"],
        boundary_breaches=[],
        basis="Child validation report",
        allowed_phases={"child_active"},
    )


def runtime_timeout(state: dict[str, Any]) -> dict[str, Any]:
    return _return_observation(
        state,
        source="runtime",
        trigger="timeout",
        label="timed_out",
        conditions=None,
        open_conditions=["implementation state unknown", "validation state unknown"],
        findings=["Runtime observed a timeout and no Child final message."],
        delta=None,
        tests=None,
        artifacts=None,
        unrun_checks=None,
        boundary_breaches=None,
        basis="Runtime timeout event; no checkpoint or workspace snapshot was available",
        allowed_phases={"delegation_offered", "child_active"},
    )


def child_boundary_breach(state: dict[str, Any]) -> dict[str, Any]:
    return _return_observation(
        state,
        source="child",
        trigger="claimed_complete",
        label="target_claimed_with_boundary_breach",
        conditions=["timeout_adapter_implemented", "runtime_provenance_verified"],
        open_conditions=["public API must be restored"],
        findings=["Child chose to add source to the public dispatch result."],
        delta=["public_dispatch_api.py", "test_timeout_return.py"],
        tests="passed",
        artifacts=["targeted-test-log:timeout-return"],
        unrun_checks=[],
        boundary_breaches=["public dispatch API"],
        basis="Child final report and diff reference",
        allowed_phases={"child_active"},
    )


def evaluate_delegation(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"delegation_returned"}, "evaluate_delegation"):
        return state

    contract = state["delegation_contract"]
    observation = contract["observation"]
    conditions = _value(observation["current_state"]["observed_conditions"])
    outcome_gap = sorted(set(REQUIRED_CONDITIONS) - set(conditions or []))

    unknown_fields: list[str] = []
    if conditions is None:
        unknown_fields.append("observed_conditions")
    if _value(observation["state_delta"]) is None:
        unknown_fields.append("state_delta")
    if _value(observation["observed_evidence"]["targeted_tests"]) is None:
        unknown_fields.append("targeted_tests")
    if _value(observation["boundary_breaches"]) is None:
        unknown_fields.append("boundary_breaches")

    evidence_gap: list[str] = []
    if _value(observation["observed_evidence"]["targeted_tests"]) != "passed":
        evidence_gap.append("targeted timeout tests are not proven passing")
    artifact_refs = _value(observation["observed_evidence"]["artifact_refs"])
    if not artifact_refs:
        evidence_gap.append("no validation artifact reference is available")
    if not artifact_refs or "api-surface-diff:none" not in artifact_refs:
        evidence_gap.append("public dispatch API surface is not proven unchanged")

    boundary_breaches = _value(observation["boundary_breaches"])
    accepted = not outcome_gap and not evidence_gap and not boundary_breaches and not unknown_fields

    signals: list[str] = []
    if state["delegation_return_metadata"]["source"] == "runtime":
        signals.append("runtime_synthesized_return")
    if state["delegation_return_metadata"]["trigger"] != "claimed_complete":
        signals.append("non_clean_exit")
    if evidence_gap:
        signals.append("missing_or_failed_evidence")
    if boundary_breaches:
        signals.append("custody_boundary_breach")
    if unknown_fields:
        signals.append("unknown_execution_state")

    if "runtime_synthesized_return" in signals or "custody_boundary_breach" in signals or len(signals) >= 2:
        level = "strong"
    elif signals:
        level = "raised"
    else:
        level = "baseline"

    state["intervention_signal"] = {"level": level, "signals": signals}
    state["delegation_evaluation"] = {
        "accepted_by_lead": accepted,
        "outcome_gap": outcome_gap,
        "evidence_gap": evidence_gap,
        "boundary_breaches": boundary_breaches,
        "unknown_fields": unknown_fields,
        "placement_reconsideration_required": not accepted,
        "routing_tendency": {
            "retain_with_lead": "high" if level == "strong" else "available",
            "redispatch": "available",
            "clarify": "available",
            "stop": "available",
        },
    }
    state["phase"] = "delegation_evaluated"
    return _event(state, "Lead evaluated dc-1; intervention is an observable routing factor, not a decision.")


def _reconsider(state: dict[str, Any], choice: str) -> dict[str, Any]:
    if not _guard(state, {"delegation_evaluated"}, f"reconsider:{choice}"):
        return state
    if state["delegation_evaluation"]["accepted_by_lead"]:
        return _event(state, "Placement reconsideration unnecessary: dc-1 was accepted by Lead.")

    state["placement_reconsideration"] = {
        "options": ["retain", "redispatch", "clarify", "stop"],
        "chosen": choice,
        "intervention_signal": state["intervention_signal"],
        "note": "The signal changed tendency; Lead still made the Placement Decision.",
    }
    state["lead_disposition"] = choice
    phase_by_choice = {
        "retain": "lead_has_custody",
        "redispatch": "redispatch_selected",
        "clarify": "clarification_required",
        "stop": "stopped",
    }
    state["phase"] = phase_by_choice[choice]
    return _event(state, f"Lead reconsidered Placement and explicitly chose {choice}.")


def retain(state: dict[str, Any]) -> dict[str, Any]:
    return _reconsider(state, "retain")


def redispatch(state: dict[str, Any]) -> dict[str, Any]:
    return _reconsider(state, "redispatch")


def clarify(state: dict[str, Any]) -> dict[str, Any]:
    return _reconsider(state, "clarify")


def stop(state: dict[str, Any]) -> dict[str, Any]:
    return _reconsider(state, "stop")


def lead_execute(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"lead_has_custody"}, "lead_execute"):
        return state

    state["lead_resolution"] = {
        "current_state": {
            "observed_conditions": _sourced(REQUIRED_CONDITIONS, "lead", "Lead inspection after retaining custody"),
        },
        "state_delta": _sourced(
            ["timeout_adapter.py", "test_timeout_return.py"],
            "lead",
            "Lead diff inspection",
        ),
        "observed_evidence": {
            "targeted_tests": _sourced("passed", "lead", "targeted-test-log:lead-timeout-return"),
            "artifact_refs": _sourced(
                [
                    "targeted-test-log:lead-timeout-return",
                    "diff:timeout-adapter",
                    "api-surface-diff:none",
                ],
                "lead",
                "Lead validation run",
            ),
        },
        "boundary_breaches": _sourced([], "lead", "Lead diff inspection"),
    }
    state["phase"] = "lead_work_ready"
    return _event(state, "Lead executed after retaining custody and produced a sourced delta with evidence.")


def _final_work_state(state: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    if state["lead_resolution"] is not None:
        return state["lead_resolution"], "lead_resolution"
    if state["delegation_evaluation"] and state["delegation_evaluation"]["accepted_by_lead"]:
        return state["delegation_contract"]["observation"], "accepted_delegation"
    return None, None


def prepare_human_return(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"delegation_evaluated", "lead_work_ready"}, "prepare_human_return"):
        return state
    work_state, source = _final_work_state(state)
    if work_state is None:
        return _event(state, "Cannot draft Human return: no accepted or Lead-produced final work state.")

    delta = work_state["state_delta"]
    tests = work_state["observed_evidence"]["targeted_tests"]
    artifact_refs = work_state["observed_evidence"]["artifact_refs"]
    artifact_values = _value(artifact_refs)
    caveats = []
    if source == "lead_resolution" and state["delegation_contract"] is not None:
        caveats.append("The Child attempt was not accepted; Lead retained and completed the work.")

    state["engagement_contract"]["lead_return"] = {
        "observed_outcome": _sourced(
            "Timeout return behavior is implemented with runtime provenance.",
            "lead",
            f"Lead synthesis from {source}",
        ),
        "changes": delta,
        "validation_evidence": {
            "targeted_tests": tests,
            "artifact_refs": artifact_refs,
            "public_api": _sourced(
                "unchanged"
                if artifact_values and "api-surface-diff:none" in artifact_values
                else "not_proven",
                artifact_refs["source"],
                f"{artifact_refs['basis']}; api-surface-diff:none",
            ),
        },
        "material_caveats": caveats,
        "work_state_source": source,
        "delivery_status": "draft",
    }
    state["phase"] = "human_return_drafted"
    return _event(state, "Lead drafted its Human-facing return from an explicit final work-state source.")


def evaluate_engagement(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"human_return_drafted"}, "evaluate_engagement"):
        return state
    work_state, source = _final_work_state(state)
    report = state["engagement_contract"]["lead_return"]
    conditions = set(_value(work_state["current_state"]["observed_conditions"]) or [])
    criteria_gap = sorted(set(REQUIRED_CONDITIONS) - conditions)
    if _value(work_state["observed_evidence"]["targeted_tests"]) != "passed":
        criteria_gap.append("targeted_tests_passed")

    breaches = _value(work_state["boundary_breaches"])
    authority_breaches = breaches if breaches is not None else ["boundary state unknown"]
    required_output = state["engagement_contract"]["request"]["required_lead_output"]
    output_gap = [field for field in required_output if field not in report or report[field] is None]
    evidence = report["validation_evidence"]
    evidence_gap: list[str] = []
    if _value(evidence["targeted_tests"]) != "passed":
        evidence_gap.append("targeted timeout tests are not reported passing")
    if not _value(evidence["artifact_refs"]):
        evidence_gap.append("validation artifact references are absent")
    if _value(evidence["public_api"]) != "unchanged":
        evidence_gap.append("public dispatch API is not evidenced unchanged")

    ready = not criteria_gap and not authority_breaches and not output_gap and not evidence_gap
    state["engagement_evaluation"] = {
        "ready_to_report": ready,
        "work_state_source": source,
        "criteria_gap": criteria_gap,
        "authority_breaches": authority_breaches,
        "output_gap": output_gap,
        "evidence_gap": evidence_gap,
    }
    state["phase"] = "engagement_evaluated"
    return _event(state, "Lead independently evaluated the Engagement Contract; Delegation acceptance was not enough.")


def deliver(state: dict[str, Any]) -> dict[str, Any]:
    if not _guard(state, {"engagement_evaluated"}, "deliver"):
        return state
    if not state["engagement_evaluation"]["ready_to_report"]:
        return _event(state, "Delivery blocked: Engagement Contract still has a gap.")

    state["engagement_contract"]["lead_return"]["delivery_status"] = "reported_to_human"
    state["phase"] = "reported_to_human"
    state["lead_disposition"] = "reported_to_human"
    return _event(state, "Lead delivered a contract-checked report; no Human response was inferred.")


ActionHandler = Callable[[dict[str, Any]], dict[str, Any]]


def reset_prototype(_: dict[str, Any]) -> dict[str, Any]:
    return initial_state()

ACTIONS: dict[str, tuple[str, ActionHandler]] = {
    "compile": ("lead", compile_engagement),
    "retain_direct": ("lead", retain_direct),
    "dispatch": ("lead", dispatch),
    "begin": ("child", child_begin),
    "reject": ("child", readiness_reject),
    "clean": ("child", child_clean),
    "partial": ("child", child_partial),
    "timeout": ("runtime", runtime_timeout),
    "breach": ("child", child_boundary_breach),
    "evaluate_delegation": ("lead", evaluate_delegation),
    "retain": ("lead", retain),
    "redispatch": ("lead", redispatch),
    "clarify": ("lead", clarify),
    "stop": ("lead", stop),
    "lead_execute": ("lead", lead_execute),
    "prepare_return": ("lead", prepare_human_return),
    "evaluate_engagement": ("lead", evaluate_engagement),
    "deliver": ("lead", deliver),
    "reset": ("prototype_operator", reset_prototype),
}


def reduce(state: dict[str, Any], action: str, actor: str) -> dict[str, Any]:
    """Return a new state after one actor-attributed prototype action."""

    next_state = deepcopy(state)
    definition = ACTIONS.get(action)
    if definition is None:
        return _event(next_state, f"Rejected unknown action: {action}.")
    required_actor, handler = definition
    if actor != required_actor:
        return _event(
            next_state,
            f"Rejected {action}: actor={actor}, required_actor={required_actor}.",
        )
    return handler(next_state)
