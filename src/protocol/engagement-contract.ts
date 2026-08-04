import * as z from "zod";

export const ENGAGEMENT_CONTRACT_SCHEMA_VERSION = "1.0.0" as const;

const nonEmptyString = z
  .string()
  .min(1)
  .refine((value) => value.trim().length > 0, "must contain non-whitespace text");

const explicitProvenanceSchema = z.strictObject({
  kind: z.literal("explicit"),
  basis: nonEmptyString,
});

const inferredProvenanceSchema = z.strictObject({
  kind: z.literal("inferred"),
  basis: nonEmptyString,
  context_reference_id: nonEmptyString,
});

const defaultedProvenanceSchema = z.strictObject({
  kind: z.literal("defaulted"),
  basis: nonEmptyString,
});

const clauseProvenanceSchema = z.discriminatedUnion("kind", [
  explicitProvenanceSchema,
  inferredProvenanceSchema,
  defaultedProvenanceSchema,
]);

const clauseSchema = <T extends z.ZodType>(valueSchema: T) =>
  z.strictObject({
    value: valueSchema,
    provenance: clauseProvenanceSchema,
  });

const resolvedContextReferenceSchema = z.strictObject({
  reference_text: nonEmptyString,
  status: z.literal("resolved"),
  reference_id: nonEmptyString,
  artifact_refs: z.array(nonEmptyString).min(1),
});

const unresolvedContextReferenceSchema = z.strictObject({
  reference_text: nonEmptyString,
  status: z.literal("unresolved"),
  materiality: z.enum(["material", "non_material"]),
  reason: nonEmptyString,
});

const contextReferenceSchema = z.discriminatedUnion("status", [
  resolvedContextReferenceSchema,
  unresolvedContextReferenceSchema,
]);

const successCriterionSchema = clauseSchema(
  z.strictObject({
    id: nonEmptyString,
    text: nonEmptyString,
  }),
);

const authorityBoundariesSchema = z.strictObject({
  allowed_actions: z.array(clauseSchema(nonEmptyString)),
  approval_requirements: z.array(
    clauseSchema(
      z.strictObject({
        action: nonEmptyString,
        approving_authority: nonEmptyString,
      }),
    ),
  ),
  prohibited_actions: z.array(clauseSchema(nonEmptyString)),
});

const requiredLeadOutputSchema = z.enum([
  "observed_outcome",
  "changes",
  "validation_evidence",
  "material_caveats",
  "work_state_source",
]);

const readyToActSchema = z.strictObject({
  status: z.literal("ready_to_act"),
  material_ambiguities: z.array(z.never()).max(0),
});

const clarificationRequiredSchema = z.strictObject({
  status: z.literal("clarification_required"),
  material_ambiguities: z.array(nonEmptyString).min(1),
});

const readinessSchema = z.discriminatedUnion("status", [
  readyToActSchema,
  clarificationRequiredSchema,
]);

const leadSourcedSchema = <T extends z.ZodType>(valueSchema: T) =>
  z.strictObject({
    value: valueSchema,
    source: z.literal("lead"),
    basis: nonEmptyString,
  });

const validationEvidenceSchema = z.strictObject({
  check: nonEmptyString,
  result: z.enum(["passed", "failed", "not_run"]),
  basis: nonEmptyString,
  artifact_refs: z.array(nonEmptyString),
});

const leadReturnSchema = z.strictObject({
  work_state_source: z.literal("lead"),
  observed_outcome: leadSourcedSchema(nonEmptyString),
  changes: leadSourcedSchema(z.array(nonEmptyString)),
  validation_evidence: z.array(validationEvidenceSchema).min(1),
  material_caveats: leadSourcedSchema(z.array(nonEmptyString)),
  delivery_status: z.enum(["draft", "reported_to_human"]),
});

const engagementContractV1WireShapeSchema = z.strictObject({
  contract_type: z.literal("engagement_contract"),
  schema_version: z.literal(ENGAGEMENT_CONTRACT_SCHEMA_VERSION),
  contract_id: nonEmptyString,
  compiled_by: z.literal("lead"),
  raw_human_request: nonEmptyString,
  context_references: z.array(contextReferenceSchema),
  current_work_layer: clauseSchema(nonEmptyString),
  goal: clauseSchema(nonEmptyString),
  success_criteria: z.array(successCriterionSchema).min(1),
  authority_boundaries: authorityBoundariesSchema,
  priority_order: z.array(clauseSchema(nonEmptyString)).min(1),
  evidence_requirements: z.array(clauseSchema(nonEmptyString)).min(1),
  required_lead_output: z.array(clauseSchema(requiredLeadOutputSchema)).min(1),
  stop_rules: z.array(clauseSchema(nonEmptyString)).min(1),
  readiness: readinessSchema,
  lead_return: leadReturnSchema.nullable(),
});

type Provenance = z.infer<typeof clauseProvenanceSchema>;

function allClauseProvenances(
  contract: z.infer<typeof engagementContractV1WireShapeSchema>,
): Provenance[] {
  return [
    contract.current_work_layer.provenance,
    contract.goal.provenance,
    ...contract.success_criteria.map((item) => item.provenance),
    ...contract.authority_boundaries.allowed_actions.map((item) => item.provenance),
    ...contract.authority_boundaries.approval_requirements.map((item) => item.provenance),
    ...contract.authority_boundaries.prohibited_actions.map((item) => item.provenance),
    ...contract.priority_order.map((item) => item.provenance),
    ...contract.evidence_requirements.map((item) => item.provenance),
    ...contract.required_lead_output.map((item) => item.provenance),
    ...contract.stop_rules.map((item) => item.provenance),
  ];
}

export const engagementContractV1Schema = engagementContractV1WireShapeSchema.superRefine(
  (contract, context) => {
    const materialUnresolvedReferences = contract.context_references.filter(
      (reference) => reference.status === "unresolved" && reference.materiality === "material",
    );

    if (contract.readiness.status === "ready_to_act" && materialUnresolvedReferences.length > 0) {
      context.addIssue({
        code: "custom",
        path: ["readiness", "status"],
        message: "ready_to_act cannot coexist with an unresolved material context reference",
      });
    }

    if (contract.readiness.status === "clarification_required" && contract.lead_return !== null) {
      context.addIssue({
        code: "custom",
        path: ["lead_return"],
        message: "lead_return must remain null while material clarification is required",
      });
    }

    const resolvedReferenceIds = new Set(
      contract.context_references
        .filter((reference) => reference.status === "resolved")
        .map((reference) => reference.reference_id),
    );

    for (const provenance of allClauseProvenances(contract)) {
      if (
        provenance.kind === "inferred" &&
        !resolvedReferenceIds.has(provenance.context_reference_id)
      ) {
        context.addIssue({
          code: "custom",
          path: ["context_references"],
          message: `inferred clause references unresolved context: ${provenance.context_reference_id}`,
        });
      }
    }
  },
);

export type EngagementContractV1 = z.infer<typeof engagementContractV1Schema>;

/**
 * Structural JSON Schema for transport tooling. It does not encode referential
 * or cross-field invariants; use parseEngagementContractV1 at trust boundaries.
 */
export const engagementContractV1StructuralJsonSchema = z.toJSONSchema(
  engagementContractV1WireShapeSchema,
);

export function parseEngagementContractV1(input: unknown): EngagementContractV1 {
  return engagementContractV1Schema.parse(input);
}

export function safeParseEngagementContractV1(input: unknown) {
  return engagementContractV1Schema.safeParse(input);
}
