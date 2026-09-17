import { z } from "zod";

// Generated from pfds.schema.json. Do not edit by hand; run generate.py.
export const PrecisionReview = z.object({
  "adoption_depth": z.enum(["auditing", "remediation", "design_time"]).describe("Section 6.1. The three adoption depths."),
  "conformance": z.object({
  "compliance_serves_purpose": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "deficits_mapped": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "method_structure_congruent": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "violations_detectable": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values.")
}).strict().describe("The invariant answers on the face. There is deliberately no overall or total field: conformance is per-condition, mirroring the suite's refusal to collapse a profile into a single number."),
  "congruence_checked": z.boolean().describe("Section 3. Method-Structure Congruence was assessed for the artifact's production."),
  "corollaries": z.array(z.object({
  "condition": z.string().describe("The iff condition the corollary specifies."),
  "corrective": z.string().describe("The corrective exemplar the standard cites.").optional(),
  "deficit_direction": z.string().describe("What under-specification fails to prevent."),
  "id": z.string().describe("The corollary handle (for example operational_definition, taxonomy_completeness)."),
  "imposition_direction": z.string().describe("What over-specification produces."),
  "name": z.string()
}).strict()).describe("Section 2. The ten corollaries, each a structured precision condition with its two failure directions. These are the standard's fixed reference set, identical across reviews, so a review MAY carry them for self-containment but is not required to restate them; requiring them would be the imposition the corollaries themselves forbid.").optional(),
  "deficits": z.array(z.object({
  "decision": z.string().describe("Section 6.5. The documented decision (remediation, acceptance with rationale, deferral, or not-a-deficit); required at Loop-Closed.").optional(),
  "location": z.string().describe("The document and location of the deficit."),
  "pattern": z.string().describe("The failure-pattern handle the deficit is keyed to.")
}).strict()).describe("Section 6.1. The precision deficit map, each deficit located and keyed to a failure pattern.").optional(),
  "failure_patterns": z.array(z.object({
  "id": z.string().describe("The pattern handle (for example normative_substitution, category_collapse)."),
  "name": z.string(),
  "response": z.string().describe("The response the pattern enables."),
  "structural_signature": z.string().describe("The observable signature that identifies the pattern.")
}).strict()).describe("Section 7. The precision-failure patterns, each a structured signature-and-response; the standard's fixed reference set, carried optionally for the same reason as the corollaries.").optional(),
  "obligation_tier": z.enum(["assessed", "operational", "instrumented", "loop_closed", "auditable"]).describe("Section 6.5. The five obligation-loop tiers."),
  "subject": z.string().describe("The governed artifact under review.")
}).strict();

export type PrecisionReview = z.infer<typeof PrecisionReview>;
