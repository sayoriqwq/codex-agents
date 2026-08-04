"""PROTOTYPE — terminal driver for the pure two-contract reducer."""

from __future__ import annotations

import sys
from typing import Any

from model import initial_state, reduce


BOLD = "\x1b[1m"
DIM = "\x1b[2m"
RESET = "\x1b[0m"

Action = tuple[str, str]

KEYS: dict[str, Action] = {
    "c": ("compile", "lead"),
    "h": ("retain_direct", "lead"),
    "d": ("dispatch", "lead"),
    "a": ("begin", "child"),
    "j": ("reject", "child"),
    "g": ("clean", "child"),
    "p": ("partial", "child"),
    "t": ("timeout", "runtime"),
    "b": ("breach", "child"),
    "e": ("evaluate_delegation", "lead"),
    "l": ("retain", "lead"),
    "x": ("redispatch", "lead"),
    "k": ("clarify", "lead"),
    "s": ("stop", "lead"),
    "w": ("lead_execute", "lead"),
    "o": ("prepare_return", "lead"),
    "v": ("evaluate_engagement", "lead"),
    "f": ("deliver", "lead"),
    "u": ("evaluate_delegation", "child"),
    "r": ("reset", "prototype_operator"),
}

COMMON_START: list[Action] = [
    ("compile", "lead"),
    ("dispatch", "lead"),
]

COMMON_LEAD_RECOVERY: list[Action] = [
    ("evaluate_delegation", "lead"),
    ("retain", "lead"),
    ("lead_execute", "lead"),
    ("prepare_return", "lead"),
    ("evaluate_engagement", "lead"),
    ("deliver", "lead"),
]

DEMOS: dict[str, list[Action]] = {
    "direct": [
        ("compile", "lead"),
        ("retain_direct", "lead"),
        ("lead_execute", "lead"),
        ("prepare_return", "lead"),
        ("evaluate_engagement", "lead"),
        ("deliver", "lead"),
    ],
    "clean": COMMON_START
    + [
        ("begin", "child"),
        ("clean", "child"),
        ("evaluate_delegation", "lead"),
        ("prepare_return", "lead"),
        ("evaluate_engagement", "lead"),
        ("deliver", "lead"),
    ],
    "partial": COMMON_START
    + [("begin", "child"), ("partial", "child")]
    + COMMON_LEAD_RECOVERY,
    "timeout": COMMON_START
    + [("begin", "child"), ("timeout", "runtime")]
    + COMMON_LEAD_RECOVERY,
    "breach": COMMON_START
    + [("begin", "child"), ("breach", "child")]
    + COMMON_LEAD_RECOVERY,
    "readiness": COMMON_START
    + [("reject", "child")]
    + COMMON_LEAD_RECOVERY,
}


def _items(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return "; ".join(str(item) for item in value) or "[]"
    if isinstance(value, dict):
        return "; ".join(f"{key}={_items(item)}" for key, item in value.items())
    return str(value)


def _sourced(field: dict[str, Any] | None) -> str:
    if field is None:
        return "—"
    return f"{_items(field['value'])}  ← {field['source']} ({field['basis']})"


def _line(label: str, value: Any, *, ansi: bool) -> str:
    if ansi:
        return f"{BOLD}{label:<22}{RESET} {_items(value)}"
    return f"{label:<22} {_items(value)}"


def _heading(text: str, *, ansi: bool) -> str:
    return f"{BOLD if ansi else ''}{text}{RESET if ansi else ''}"


def render(state: dict[str, Any], *, ansi: bool = True) -> str:
    engagement = state["engagement_contract"]
    placement = state["initial_placement"]
    delegation = state["delegation_contract"]
    signal = state["intervention_signal"]
    lines = [
        _heading("PROTOTYPE — TWO CONTRACT FLOW", ansi=ansi),
        _line("phase", state["phase"], ansi=ansi),
        _line("intervention signal", f"{signal['level']}: {_items(signal['signals'])}", ansi=ansi),
        _line("Lead disposition", state["lead_disposition"], ansi=ansi),
        "",
        _heading("Human prompt", ansi=ansi),
        state["raw_human_prompt"],
    ]

    if engagement:
        request = engagement["request"]
        parties = engagement["parties"]
        success = [f"{item['id']}: {item['text']}" for item in request["success_criteria"]]
        provenance = [f"{clause} ← {basis}" for clause, basis in engagement["clause_provenance"].items()]
        lines += [
            "",
            _heading("1. Engagement Contract — Human ↔ Lead", ansi=ansi),
            _line("authorities", parties, ansi=ansi),
            _line("readiness", engagement["readiness"], ansi=ansi),
            _line("context resolution", engagement["prompt_reference_resolution"], ansi=ansi),
            _line("current layer", request["current_layer"], ansi=ansi),
            _line("goal", request["goal"], ansi=ansi),
            _line("success criteria", success, ansi=ansi),
            _line("must stop", request["authority_and_constraints"]["must_stop"], ansi=ansi),
            _line("priority", request["priority_order"], ansi=ansi),
            _line("clause provenance", provenance, ansi=ansi),
            _line("Lead return", engagement["lead_return"], ansi=ansi),
        ]

    if placement:
        lines += [
            "",
            _heading("Placement Decision — runtime metadata outside both contracts", ansi=ansi),
            _line("decision", placement["decision"], ansi=ansi),
            _line("shape / profile", f"{placement['work_shape']} / {placement['selected_profile']}", ansi=ansi),
            _line("model affinity", placement["model_affinity"], ansi=ansi),
            _line("context fork", placement["context_fork"], ansi=ansi),
            _line("reason", placement["reason"], ansi=ansi),
        ]

    if delegation:
        expected = delegation["expectation"]
        observed = delegation["observation"]
        lines += [
            "",
            _heading("2. Delegation Contract — Lead ↔ Child", ansi=ansi),
            _line("contract", delegation["contract_id"], ansi=ansi),
            _line("owner / acceptance", f"{delegation['owner']} / {delegation['acceptance_authority']}", ansi=ansi),
            _line("execution custody", delegation["execution_custody"], ansi=ansi),
            _line("Child readiness", delegation["child_readiness"], ansi=ansi),
            _line("target", expected["target_state"]["summary"], ansi=ansi),
            _line("required", expected["target_state"]["required_conditions"], ansi=ansi),
            _line("forbidden", expected["custody_bounds"]["forbidden"], ansi=ansi),
            _line("evidence demand", expected["evidence_demand"], ansi=ansi),
        ]
        if observed:
            lines += [
                "",
                _heading("Provisional delegation-return event", ansi=ansi),
                _line("metadata", state["delegation_return_metadata"], ansi=ansi),
                _line("state label", _sourced(observed["current_state"]["label"]), ansi=ansi),
                _line("conditions", _sourced(observed["current_state"]["observed_conditions"]), ansi=ansi),
                _line("open conditions", _sourced(observed["current_state"]["open_conditions"]), ansi=ansi),
                _line("findings", _sourced(observed["basis_findings"]), ansi=ansi),
                _line("state delta", _sourced(observed["state_delta"]), ansi=ansi),
                _line("tests", _sourced(observed["observed_evidence"]["targeted_tests"]), ansi=ansi),
                _line("artifacts", _sourced(observed["observed_evidence"]["artifact_refs"]), ansi=ansi),
                _line("boundary breaches", _sourced(observed["boundary_breaches"]), ansi=ansi),
            ]

    if state["delegation_evaluation"]:
        evaluation = state["delegation_evaluation"]
        lines += [
            "",
            _heading("Lead evaluation of Delegation", ansi=ansi),
            _line("accepted by Lead", evaluation["accepted_by_lead"], ansi=ansi),
            _line("outcome gap", evaluation["outcome_gap"], ansi=ansi),
            _line("evidence gap", evaluation["evidence_gap"], ansi=ansi),
            _line("unknown fields", evaluation["unknown_fields"], ansi=ansi),
            _line("boundary breach", evaluation["boundary_breaches"], ansi=ansi),
            _line("routing tendency", evaluation["routing_tendency"], ansi=ansi),
        ]

    if state["placement_reconsideration"]:
        lines += [
            "",
            _heading("Lead Placement reconsideration", ansi=ansi),
            _line("decision record", state["placement_reconsideration"], ansi=ansi),
        ]

    if state["lead_resolution"]:
        resolution = state["lead_resolution"]
        lines += [
            "",
            _heading("Lead-produced work state", ansi=ansi),
            _line("conditions", _sourced(resolution["current_state"]["observed_conditions"]), ansi=ansi),
            _line("state delta", _sourced(resolution["state_delta"]), ansi=ansi),
            _line("tests", _sourced(resolution["observed_evidence"]["targeted_tests"]), ansi=ansi),
            _line("boundary breaches", _sourced(resolution["boundary_breaches"]), ansi=ansi),
        ]

    if state["engagement_evaluation"]:
        lines += [
            "",
            _heading("Lead evaluation of Engagement", ansi=ansi),
            _line("evaluation", state["engagement_evaluation"], ansi=ansi),
        ]

    lines += ["", _line("last event", state["events"][-1], ansi=ansi)]
    if ansi:
        lines += [
            "",
            f"{BOLD}[c/h/d]{RESET} compile/retain/dispatch  {BOLD}[a/j]{RESET} Child begin/reject  "
            f"{BOLD}[g/p/t/b]{RESET} clean/partial/timeout/breach",
            f"{BOLD}[e]{RESET} evaluate Delegation  {BOLD}[l/x/k/s]{RESET} retain/redispatch/clarify/stop  "
            f"{BOLD}[w]{RESET} Lead executes",
            f"{BOLD}[o/v/f]{RESET} prepare/evaluate Engagement/deliver  "
            f"{BOLD}[u]{RESET} unauthorized actor demo  {BOLD}[r/q]{RESET} reset/quit",
            f"{DIM}Every key dispatches one actor-attributed reducer action and redraws all state.{RESET}",
        ]
    return "\n".join(lines)


def run_demo(name: str) -> None:
    state = initial_state()
    print(f"=== initial ({name}) ===")
    print(render(state, ansi=False))
    for action, actor in DEMOS[name]:
        state = reduce(state, action, actor)
        print(f"\n=== actor: {actor} | action: {action} ===")
        print(render(state, ansi=False))


def run_interactive() -> None:
    state = initial_state()
    while True:
        print("\x1b[2J\x1b[H", end="")
        print(render(state))
        key = input("\n> ").strip().lower()
        if key == "q":
            return
        action, actor = KEYS.get(key, (key, "human"))
        state = reduce(state, action, actor)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--demo" and sys.argv[2] in DEMOS:
        run_demo(sys.argv[2])
    else:
        run_interactive()
