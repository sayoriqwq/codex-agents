import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import {
  ENGAGEMENT_CONTRACT_SCHEMA_VERSION,
  engagementContractV1StructuralJsonSchema,
  parseEngagementContractV1,
  safeParseEngagementContractV1,
} from "../dist/index.js";

function fixture(name) {
  return JSON.parse(
    readFileSync(new URL(`./fixtures/${name}`, import.meta.url), "utf8"),
  );
}

test("parses a complete direct-retain Engagement Contract", () => {
  const contract = parseEngagementContractV1(
    fixture("engagement-contract-ready.json"),
  );

  assert.equal(contract.schema_version, ENGAGEMENT_CONTRACT_SCHEMA_VERSION);
  assert.equal(contract.readiness.status, "ready_to_act");
  assert.equal(contract.lead_return.delivery_status, "reported_to_human");
  assert.equal("human_acceptance" in contract, false);
});

test("preserves the raw Human request byte-for-byte", () => {
  const input = fixture("engagement-contract-ready.json");
  input.raw_human_request = `  ${input.raw_human_request}\n`;

  const contract = parseEngagementContractV1(input);

  assert.equal(contract.raw_human_request, input.raw_human_request);
});

test("parses a clarification-required Engagement Contract without a Lead return", () => {
  const contract = parseEngagementContractV1(
    fixture("engagement-contract-clarification.json"),
  );

  assert.equal(contract.readiness.status, "clarification_required");
  assert.equal(contract.lead_return, null);
});

test("rejects additional fields", () => {
  const input = fixture("engagement-contract-ready.json");
  input.claimed_human_approval = true;

  assert.equal(safeParseEngagementContractV1(input).success, false);
});

test("rejects ready_to_act with an unresolved material reference", () => {
  const input = fixture("engagement-contract-clarification.json");
  input.readiness = { status: "ready_to_act", material_ambiguities: [] };

  const result = safeParseEngagementContractV1(input);
  assert.equal(result.success, false);
  assert.match(
    result.error.issues.map((issue) => issue.message).join("\n"),
    /unresolved material context reference/,
  );
});

test("rejects an inferred clause whose context was not resolved", () => {
  const input = fixture("engagement-contract-ready.json");
  input.goal.provenance = {
    kind: "inferred",
    basis: "A missing design",
    context_reference_id: "missing-context",
  };

  const result = safeParseEngagementContractV1(input);
  assert.equal(result.success, false);
  assert.match(
    result.error.issues.map((issue) => issue.message).join("\n"),
    /references unresolved context/,
  );
});

test("rejects a Lead return while clarification is required", () => {
  const input = fixture("engagement-contract-clarification.json");
  input.lead_return = fixture("engagement-contract-ready.json").lead_return;

  const result = safeParseEngagementContractV1(input);
  assert.equal(result.success, false);
  assert.match(
    result.error.issues.map((issue) => issue.message).join("\n"),
    /lead_return must remain null/,
  );
});

test("requires an approving authority for each approval requirement", () => {
  const input = fixture("engagement-contract-ready.json");
  delete input.authority_boundaries.approval_requirements[0].value
    .approving_authority;

  assert.equal(safeParseEngagementContractV1(input).success, false);
});

test("exports a strict structural JSON Schema for transport tooling", () => {
  assert.equal(engagementContractV1StructuralJsonSchema.type, "object");
  assert.equal(
    engagementContractV1StructuralJsonSchema.additionalProperties,
    false,
  );
  assert.equal(
    engagementContractV1StructuralJsonSchema.properties.schema_version.const,
    ENGAGEMENT_CONTRACT_SCHEMA_VERSION,
  );
});
