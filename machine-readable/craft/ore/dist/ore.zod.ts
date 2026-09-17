import { z } from "zod";

// Generated from ore.schema.json. Do not edit by hand; run generate.py.
export const GradedSource = z.object({
  "conformance": z.object({
  "no_grade_as_worth_verdict": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("ORE Section 8. Per-obligation answer; silence is not one of the values."),
  "outputs_expose_grade_profile": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("ORE Section 8. Per-obligation answer; silence is not one of the values."),
  "posture_declared_and_enforced": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("ORE Section 8. Per-obligation answer; silence is not one of the values."),
  "sources_graded_on_dimensions": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("ORE Section 8. Per-obligation answer; silence is not one of the values.")
}).strict().describe("ORE Section 8. The four conformance questions answered on the face. There is deliberately no overall or total field: conformance is per-obligation, mirroring the refusal to combine grades (Section 2) and the Verification-Summary-Attestation shape."),
  "grade": z.object({
  "confirmation_architecture": z.object({
  "basis": z.string().describe("The basis for the confirmation-architecture reading."),
  "independence_flag": z.string().describe("ORE Section 3.3 party-count limit. Set where effective independence cannot be assessed; party count is never a substitute.").optional(),
  "modes": z.array(z.enum(["trustless_single_party", "trustless_multi_party", "trust_based_single_party", "trust_based_multi_party", "unconfirmed"])).describe("One or more confirmation modes present when the source produced its output.")
}).strict().describe("ORE Section 3.3. Records each confirmation mode present rather than forcing one cell. Party count is not a substitute for independence; where effective independence cannot be assessed, that is recorded as a named flag."),
  "epistemic_soundness": z.object({
  "assessment": z.string().describe("The uncertainty assessment on this dimension. Not a quality rank."),
  "basis": z.string().describe("The basis on which the assessment was made."),
  "flag": z.string().describe("A named limitation where a sub-assessment could not be computed. Never a silent default.").optional()
}).strict().describe("ORE Section 3. A dimension records an assessment and the basis on which it was made. Any sub-assessment that could not be computed is a named flag, never a silent default or an assumed middle value."),
  "independence": z.object({
  "graded": z.object({
  "assessment": z.string().describe("The uncertainty assessment on this dimension. Not a quality rank."),
  "basis": z.string().describe("The basis on which the assessment was made."),
  "flag": z.string().describe("A named limitation where a sub-assessment could not be computed. Never a silent default.").optional()
}).strict().describe("The grading of this extension, where the system grades it.").optional(),
  "not_applicable_reason": z.string().describe("ORE Section 7. Where the extension is not graded, the named reason (a genesis limitation for a new source, a permanent property of the source class, or a declared choice not to grade).").optional(),
  "resolves_with_history": z.boolean().describe("ORE Section 7.3. Whether the limitation is expected to resolve as history accumulates.").optional()
}).strict().describe("ORE Section 3.4 and Section 7. A declared extension dimension is either graded (with a basis) or its absence is declared with a named reason. The \"if not graded then a reason is required\" obligation is modeled as a presence-based rule and enforced by a standard JSON Schema validator, so an extension can never fall silent or default to a middle value."),
  "provenance_integrity": z.object({
  "assessment": z.string().describe("The uncertainty assessment on this dimension. Not a quality rank."),
  "basis": z.string().describe("The basis on which the assessment was made."),
  "flag": z.string().describe("A named limitation where a sub-assessment could not be computed. Never a silent default.").optional()
}).strict().describe("ORE Section 3. A dimension records an assessment and the basis on which it was made. Any sub-assessment that could not be computed is a named flag, never a silent default or an assumed middle value."),
  "track_record": z.object({
  "graded": z.object({
  "assessment": z.string().describe("The uncertainty assessment on this dimension. Not a quality rank."),
  "basis": z.string().describe("The basis on which the assessment was made."),
  "flag": z.string().describe("A named limitation where a sub-assessment could not be computed. Never a silent default.").optional()
}).strict().describe("The grading of this extension, where the system grades it.").optional(),
  "not_applicable_reason": z.string().describe("ORE Section 7. Where the extension is not graded, the named reason (a genesis limitation for a new source, a permanent property of the source class, or a declared choice not to grade).").optional(),
  "resolves_with_history": z.boolean().describe("ORE Section 7.3. Whether the limitation is expected to resolve as history accumulates.").optional()
}).strict().describe("ORE Section 3.4 and Section 7. A declared extension dimension is either graded (with a basis) or its absence is declared with a named reason. The \"if not graded then a reason is required\" obligation is modeled as a presence-based rule and enforced by a standard JSON Schema validator, so an extension can never fall silent or default to a middle value.")
}).strict().describe("ORE Section 3. The per-dimension grade. Three dimensions are required (provenance integrity, epistemic soundness, confirmation architecture); two are declared extensions (track record, independence) that must each be addressed, graded or with a declared absence. There is deliberately no combined figure: the closed schema forbids one, which enforces the Section 2 refusal to merge into a single confidence number by absence."),
  "monitoring": z.string().describe("ORE Section 4. The monitoring obligation attached to an admitted opaque or flagged source.").optional(),
  "posture": z.enum(["screened", "graded", "open"]).describe("ORE Section 6. The intake posture: when grading happens and what ungraded material may touch."),
  "source_identifier": z.string().describe("What source this grades."),
  "standing_loss": z.object({
  "basis": z.string().describe("The basis for the decision."),
  "decision": z.string().describe("The eligibility decision taken."),
  "evidence": z.string().describe("The evidence on which standing was reduced or withdrawn.")
}).strict().describe("ORE Section 6. The documented, evidence-based record where this source's eligibility was reduced or withdrawn.").optional()
}).strict();

export type GradedSource = z.infer<typeof GradedSource>;
