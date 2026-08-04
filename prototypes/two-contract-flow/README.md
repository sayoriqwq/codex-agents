# PROTOTYPE — Two-contract Lead flow

> Throwaway logic prototype. This is not production code or a committed protocol.

## Question

Can one concrete Human request move through two nested contracts without confusing intent, model/runtime routing, execution custody, factual provenance, and acceptance authority?

The example starts from this deliberately underspecified prompt:

> 把刚才定下来的 Child timeout 方案做掉。public dispatch API 不要动，尽快，但验证不能省。

The state machine exercises:

1. a provisional **Engagement Contract** compiled by the Lead from explicit, inferred, and defaulted clauses in the Human request;
2. a separate **Placement Decision**, where the Lead chooses `Execution → Luna` without leaking model/profile metadata into either semantic contract;
3. a confirmed **Delegation Contract** whose outcome acceptance is owned only by the Lead for one Child Dispatch;
4. readiness rejection or the Child's Implicit Acceptance of Execution Custody before work begins;
5. clean, partial, timeout, and boundary-breach exits through one provisional return-event shape;
6. field-level provenance, including `unknown` for facts a timeout-observing runtime cannot know;
7. an explicit Lead Placement reconsideration after a failed Delegation, with intervention pressure treated as a routing signal rather than an automatic decision;
8. an independent Engagement evaluation before the Lead reports to the Human, while Human acceptance remains unset.

## Why the Human → Lead package has this shape

The **Engagement Contract** name is provisional, but its slots deliberately compile the official [GPT-5.6 prompting guidance](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6) into observable state:

| GPT-5.6 concern | Prototype field |
| --- | --- |
| outcome first and success criteria | `goal`, `current_layer`, `success_criteria` |
| autonomy and approval boundaries | `authority_and_constraints` |
| relevant context without replaying everything | `prompt_reference_resolution`, `governing_context` |
| quality, latency, and cost trade-offs | `priority_order` |
| verifiable delivery | `required_lead_output`, sourced `validation_evidence` |
| ask, abstain, and stop behavior | `readiness`, `stop_rules` |

This is a project-level compilation model, not an OpenAI-defined protocol. The raw Human prompt remains the source record; every added clause is marked explicit, inferred from a resolved context artifact, or defaulted from standing authority. An unresolved material reference blocks dispatch instead of being silently invented.

## Run

This repository has no application runtime or task runner, so the prototype uses the workstation Python and only the standard library.

```fish
/etc/profiles/per-user/sayori/bin/python prototypes/two-contract-flow/tui.py
```

Run the hardest scripted path:

```fish
/etc/profiles/per-user/sayori/bin/python prototypes/two-contract-flow/tui.py --demo timeout
```

Available demos are `clean`, `partial`, `timeout`, `breach`, and `readiness`.

## What a successful run demonstrates

- The two contracts require two independent comparisons: a Delegation can fail, then the Lead can retain custody and still satisfy the Engagement.
- A Child result, a runtime observation, Lead acceptance, and Human acceptance are four distinct facts.
- Runtime/profile selection belongs to Placement metadata, not the semantic task contracts.
- Readiness and the first effective Child action make the custody transition visible.
- A runtime timeout can force a return transition without inventing the Child's delta, test result, boundary status, or completion state.
- Actor-attributed reducer actions enforce that the Child cannot accept its own Delegation or report on behalf of the Lead.

This prototype cannot prove prompt quality, model reliability, or routing economics. Those require representative real traces and evals after the state semantics are accepted.
