import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

function readRepoFile(path) {
  return readFileSync(new URL(`../${path}`, import.meta.url), "utf8");
}

const skill = readRepoFile("plugins/agent-dispatch/skills/lead/SKILL.md");
const profiles = readRepoFile(
  "plugins/agent-dispatch/skills/lead/references/profile-selection.md",
);

test("routes every ready placement through an explicit profile value", () => {
  const placement = skill.indexOf("[placement.md]");
  const profileSelection = skill.indexOf("[profile-selection.md]");
  const gate = skill.indexOf("Lead gate — readiness:");

  assert.ok(placement >= 0);
  assert.ok(profileSelection > placement);
  assert.ok(gate > profileSelection);
  assert.match(
    skill,
    /placement: <decision>; profile: <profile>; model: <model>/,
  );
  assert.match(skill, /explicit profile and model values/);
});

test("keeps the current dispatch frontier explicit", () => {
  assert.match(skill, /leave Execution Custody with the Lead/);
  assert.match(skill, /dispatch_candidate_not_executed/);
  assert.match(skill, /no installed Delegation Contract or Handoff-Back branch/);
});

test("maps work shapes to model profiles instead of task roles", () => {
  assert.match(profiles, /`Judgment` \| `sol` \| `gpt-5\.6-sol`/);
  assert.match(profiles, /`Execution` \| `luna` \| `gpt-5\.6-luna`/);
  assert.match(profiles, /`Mechanical` \| `spark` \| `gpt-5\.3-codex-spark`/);
  assert.match(profiles, /task role remains in the Delegation Unit/);
});

test("requires a complete and auditable Profile Selection record", () => {
  for (const field of [
    "model_affinity",
    "selected_profile",
    "selected_model",
    "reasoning_effort",
    "context_strategy",
    "routing_factors",
    "affinity_override",
    "availability_evidence",
  ]) {
    assert.ok(profiles.includes(`\`${field}\``));
  }
});
