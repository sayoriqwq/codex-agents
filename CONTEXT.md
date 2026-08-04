# Agent Dispatch

Agent Dispatch describes how a user-selected Lead delegates bounded work to Children while balancing model capability, latency, cost, and error amplification. It keeps dispatch topology, cognitive responsibility, workflow structure, model resources, and reusable agent definitions distinct.

## Dispatch topology

**Topology Position**:
An agent's location in a dispatch graph. The canonical positions are Lead and Child.
_Avoid_: Role, agent role, task role

**Lead**:
The user-selected agent that owns intent, delegation, authority decisions, integration, and final acceptance for the current work.
_Avoid_: Lead role, orchestrator profile

**Child**:
An agent created by a Lead to return one bounded, independently consumable result.
_Avoid_: Worker role, leaf profile

**Dispatch**:
One creation of a Child by a Lead for a bounded result.
_Avoid_: Task, workflow step

**Delegation Contract**:
The Lead-owned, bidirectional semantic contract for one Dispatch, pairing what the Child is expected to achieve and substantiate with the work state and evidence returned to the Lead.
_Avoid_: Handoff Contract, task packet, return protocol

**Placement Decision**:
The Lead's choice to retain a Delegation Unit or create a Dispatch after comparing expected total completion cost.
_Avoid_: Model selection, routing decision

**Handoff Cost**:
The expected context reconstruction, latency, coordination, and verification overhead required to transfer a Delegation Unit to a Child.
_Avoid_: Model cost, token cost

**Handoff-Ready**:
A state in which a Delegation Unit has enough fixed intent, evidence, scope, and acceptance criteria to be transferred without relying on the Lead's private context.
_Avoid_: Fully documented, context-free

**Handoff**:
The transfer of Execution Custody for a Handoff-Ready Delegation Unit from a Lead to a Child. Acceptance Authority remains with the Lead.
_Avoid_: Responsibility transfer, task assignment

**Execution Custody**:
The Child's temporary responsibility to perform a Delegation Unit within its granted scope and return the result with evidence.
_Avoid_: Outcome ownership, acceptance authority

**Acceptance Authority**:
The Lead's retained authority to decide whether a returned result satisfies the governing intent and acceptance criteria.
_Avoid_: Child completion, execution custody

**Readiness Check**:
The Child's initial determination, before its first effective action, that a Delegation Unit is understandable and executable within its Work Shape, scope, authority, and acceptance criteria.
_Avoid_: Positive acknowledgement, full task analysis

**Implicit Acceptance**:
The Child's first effective action after a successful Readiness Check, which completes the Handoff and takes Execution Custody.
_Avoid_: Acceptance Authority, affirmative ACK

**Handoff-Back**:
The sole return transition from a Child or its execution environment to the Lead, carrying Return State regardless of whether the work is claimed complete, rejected, partial, failed, or interrupted.
_Avoid_: Completion result, failure result, custody return

**Return State**:
The observable current delta, evidence, checks, unresolved conditions, and Child assessment carried by a Handoff-Back. The Lead decides whether it constitutes accepted completion.
_Avoid_: Final outcome, success declaration

**Clarification**:
Additional information supplied after Implicit Acceptance that does not change the Delegation Unit's Work Shape, scope, authority, or acceptance criteria. Execution Custody remains with the Child.
_Avoid_: Scope expansion, new requirement

## Work classification

**Delegation Unit**:
The smallest bounded result to which the Lead assigns one Work Shape and makes one Placement Decision.
_Avoid_: Task, workflow step, prompt

**Work Shape**:
The kind and extent of cognitive responsibility carried by one unit of work, independent of its domain label or workflow name.
_Avoid_: Role, task type, agent type

**Judgment**:
A Work Shape that must form an interpretation, compare viable alternatives, or produce a decision recommendation.
_Avoid_: Research, review, discovery

**Execution**:
A Work Shape that realizes fixed intent and acceptance criteria while retaining bounded local semantic judgment.
_Avoid_: Implementation, worker task, routine work

**Mechanical**:
A Work Shape governed by a complete, enumerable rule whose exceptions require handoff instead of semantic judgment.
_Avoid_: Simple task, small task, low-value work

**Routing Factor**:
A fact about the current work that may adjust its default model preference, such as ambiguity, error consequence, context needs, latency, or verifiability.
_Avoid_: Work Shape, model tier

## Model selection

**Model Profile**:
A named model resource with a characteristic capability, latency, and cost tendency. Sol, Luna, and Spark are Model Profiles.
_Avoid_: Agent, role, tier

**Model Affinity**:
The strong default preference for a Model Profile derived from Topology Position and Work Shape before Routing Factors are applied.
_Avoid_: Model binding, hard-coded model

**Affinity Override**:
An observable departure from Model Affinity that names the Routing Factor and accepted trade-off behind the different Model Profile choice.
_Avoid_: Free model choice, silent model fallback

**Lead Selection**:
The user's explicit choice of Model Profile for the Lead. It remains stable while the Lead owns the current work.
_Avoid_: Automatic Lead routing, Lead Profile

## Reusable structure

**Workflow Step**:
A named stage inside a reusable workflow. A Workflow Step does not imply a Model Profile or an Agent Definition.
_Avoid_: Role, Agent, Work Shape

**Agent Definition**:
A reusable agent environment whose stable instructions or capabilities justify an identity beyond model selection alone.
_Avoid_: Model Profile, workflow step, task name
