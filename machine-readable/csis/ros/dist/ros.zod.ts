import { z } from "zod";

// Generated from ros.schema.json. Do not edit by hand; run generate.py.
export const RegenerativeObligationRecord = z.object({
  "adopted_tier": z.enum(["extraction_visibility", "return_architecture", "full_conformance"]).describe("Section 7. The three named ROS tiers."),
  "conformance": z.object({
  "extraction_visible": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "no_retroactive_reclassification": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "stance_declared": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "three_conditions_met": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values.")
}).strict().describe("Section 2.2. The four invariant answers on the face. There is deliberately no overall or total field: conformance is per-invariant, mirroring the suite's refusal to collapse a profile into a single number."),
  "disqualifiers": z.array(z.object({
  "id": z.string().describe("The disqualifier handle (additionality, geographical, temporal_deferral, sroi)."),
  "mechanism": z.string().describe("The structural mechanism by which the architecture fails the proximity condition."),
  "name": z.string(),
  "why_categorical": z.string().describe("Why the failure is categorical (structural, not a failure of degree that better measurement fixes).")
}).strict()).describe("Section 3.2. The categorical disqualifiers the system screens returns against, each a structural wrong-architecture mechanism."),
  "extraction_visible": z.boolean().describe("Section 2.2. Extraction is nameable, attributable, and recorded; invisibility presumes the standard unmet."),
  "harm_bearing_affiliations": z.array(z.object({
  "access_rights": z.array(z.string()).describe("The coordination access rights the standing confers (at minimum, to challenge the stance and to verify return).").optional(),
  "domain_of_action": z.string(),
  "extraction_class": z.string().describe("The class of extraction the standing applies to."),
  "satisfying_return_form": z.string().describe("The form of return that would satisfy the obligation, consulted with the registering party.").optional()
}).strict()).describe("Section 5. The affirmatively registered harm-bearing affiliations.").optional(),
  "returns": z.array(z.object({
  "clear_of_disqualifiers": z.boolean().describe("Section 3.2. True when the return trips none of the categorical disqualifiers."),
  "conditions_satisfied": z.array(z.string()).describe("Which validity conditions the return satisfies (all three are required for validity)."),
  "delivered_to_registered_party": z.boolean().describe("Section 5. Whether return delivery to a registered harm-bearing party is attested.").optional(),
  "description": z.string()
}).strict()).describe("The return assessments, each screened against the conditions and disqualifiers.").optional(),
  "stance": z.object({
  "challengers": z.array(z.string()).describe("The parties with standing to challenge the stance (defaulting to registered harm-bearing parties)."),
  "review_cycle_months": z.number().int().describe("The review cycle, a default maximum of twelve months."),
  "scope": z.string().describe("The domains, roles, and contribution types the declaration covers."),
  "stance": z.enum(["non_extractive", "more_regenerative_than_extractive"]).describe("Section 4. The two stances.")
}).strict().describe("Section 4. The declared stance and its minimum required contents."),
  "validity_conditions": z.array(z.object({
  "id": z.string().describe("The condition handle (non_fungibility, proximity, embeddedness)."),
  "name": z.string(),
  "register": z.string().describe("The structural register in which the condition operates (for example the register of the harm).").optional(),
  "test": z.string().describe("The verifiable test that distinguishes a return that satisfies the condition.")
}).strict()).describe("Section 3. The three-part validity condition rendered structurally (conjunctive).")
}).strict();

export type RegenerativeObligationRecord = z.infer<typeof RegenerativeObligationRecord>;
