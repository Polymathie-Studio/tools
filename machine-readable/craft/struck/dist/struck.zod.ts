import { z } from "zod";

// Generated from struck.schema.json. Do not edit by hand; run generate.py.
export const EvidenceGradeOutput = z.object({
  "claim": z.string().describe("The conclusion the output asserts."),
  "conformance": z.object({
  "chains_labeled": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("S7. Per-obligation answer; silence is not one of the values."),
  "contest_represented": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("S7. Per-obligation answer; silence is not one of the values."),
  "graded_evidence_exposed": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("S7. Per-obligation answer; silence is not one of the values."),
  "refutation_stated": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("S7. Per-obligation answer; silence is not one of the values."),
  "worth_left_to_consumer": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("S7. Per-obligation answer; silence is not one of the values.")
}).strict().describe("S7. The five conformance questions answered on the face. There is deliberately no overall or total field: conformance is per-obligation, mirroring the refusal to combine grades (S2.4) and the SLSA Verification-Summary-Attestation shape."),
  "contested_regions": z.array(z.object({
  "disputed": z.string(),
  "resolution_basis": z.string().describe("S4.4. The basis of any resolution the producer made.").optional(),
  "retained_losing_position": z.string().describe("S4.4. The losing position retained in the record.").optional(),
  "support_each_side": z.array(z.string()).optional(),
  "turns_on": z.string().optional(),
  "unexamined": z.boolean().describe("S4.5. True where absence of contest is an unexamined state, not agreement.").optional()
}).strict()).describe("STRUCK Section 4. Regions of disagreement in the support, represented rather than averaged.").optional(),
  "derivation_chains": z.array(z.object({
  "converges_with": z.array(z.string()).describe("S5.5. Other chains this one converges with on the same origin.").optional(),
  "rungs": z.array(z.object({
  "identifier": z.string(),
  "restates": z.string().describe("S5.1. The named source this rung restates, if role is restatement.").optional(),
  "role": z.enum(["originating_observation", "primary_record", "aggregator", "secondary_reporting", "review", "restatement"]).describe("S5.2. The role a derivation rung actually holds.")
}).strict()),
  "stop_reason": z.string().optional(),
  "stopped_at": z.string().describe("S5.3. Where the walk to origin stopped, if it could not be completed.").optional()
}).strict()).describe("STRUCK Section 5. Support traced to ultimate origin, rungs labeled by role."),
  "graded_evidence": z.object({
  "joint_support_flag": z.boolean().describe("S2.3. Separately admitted sources not distinct in effective origin.").optional(),
  "open_posture_ungraded": z.boolean().describe("S2.2. True if the output rests on ungraded material admitted under an Open posture, declared on the face.").optional(),
  "per_dimension": z.array(z.object({
  "dimension": z.string(),
  "flags": z.array(z.string()).optional(),
  "weakest_assessment": z.string().describe("The weakest assessment present anywhere in the support for this dimension.")
}).strict())
}).strict().describe("Per-dimension grade of the support; no combined figure (S2.4)."),
  "refutation": z.object({
  "conditions": z.array(z.object({
  "world_observable": z.string().describe("S3.1/S3.2. The refuting thing, stated in terms of what could be found in the world.")
}).strict()).optional(),
  "unfalsifiability": z.object({
  "reason": z.enum(["definitional", "domain_limited", "impressionistic"]).describe("S3.3.")
}).strict().optional()
}).strict().describe("S3. Either world-terms refutation conditions, or a declared unfalsifiability that names a reason. The \"if unfalsifiable then a reason is required\" obligation is modeled as native nested-required (reason is required inside the unfalsifiability object), and the \"conditions or a declaration, never silence\" obligation as a presence-based rule. Both are enforced by a standard JSON Schema validator."),
  "worth_judgment": z.object({
  "consumer_facing": z.boolean().optional(),
  "cost_to_raise_confidence": z.string().describe("S6.2. Optional. What it would take to raise confidence and what it would cost.").optional()
}).strict().describe("S6. The sufficiency judgment left to the consumer; no adequacy assertion.")
}).strict();

export type EvidenceGradeOutput = z.infer<typeof EvidenceGradeOutput>;
