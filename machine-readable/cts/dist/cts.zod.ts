import { z } from "zod";

// Generated from cts.schema.json. Do not edit by hand; run generate.py.
export const ConflictTransformationRecord = z.object({
  "adoption_tier": z.enum(["declared", "structured", "instrumented", "loop_closed", "auditable"]).describe("Section 8. The five adoption tiers."),
  "conformance": z.object({
  "conflict_legible": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "engagement_recognized": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "graduated_architecture_present": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "proactive_disposition_protected": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "transformation_capacity_provisioned": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values.")
}).strict().describe("The per-invariant conformance answers. There is deliberately no overall or total field: conformance is per-invariant, mirroring the suite's refusal to collapse a profile into a single number."),
  "constitutional_precondition_established": z.boolean().describe("Section 4. Whether parties share sufficient foundational vocabulary about what the organization is to name what they are in conflict about; if not, the required first engagement is constitutional dialogue, not conflict transformation."),
  "invariants": z.array(z.object({
  "epistemic_tier": z.enum(["tier_a", "tier_b", "tier_c"]).describe("Section 4. The three epistemic tiers."),
  "id": z.string().describe("The invariant handle (for example legibility, graduated_engagement, proactive_disposition, capacity_provision, recognition)."),
  "name": z.string(),
  "satisfaction_status": z.enum(["satisfied", "violated", "partial", "not_applicable"]).describe("The status of a structural invariant against the system; silence is not one of the values."),
  "satisfaction_test": z.string().describe("The structural test that determines whether the invariant is satisfied, stated so an independent observer can apply it."),
  "signature": z.string().describe("The observed violation or satisfaction signature supporting the status; some signatures are computable from the coordination record.").optional()
}).strict()).describe("Section 4. The five structural invariants, each rendered as a typed object carrying its satisfaction status and epistemic tier. They are constitutive of a capacity declaration; a record that names no invariants could claim capacity while assessing nothing."),
  "scales_addressed": z.array(z.enum(["intra_organizational", "inter_organizational", "platform_level"])).describe("Section 5. The operational scales at which the record declares the invariants apply.").optional(),
  "subject": z.string().describe("The coordination system whose conflict-transformation capacity is declared.")
}).strict();

export type ConflictTransformationRecord = z.infer<typeof ConflictTransformationRecord>;
