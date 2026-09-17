import { z } from "zod";

// Generated from fbcs.schema.json. Do not edit by hand; run generate.py.
export const FourBatteriesRecord = z.object({
  "batteries": z.array(z.object({
  "battery": z.enum(["personal", "relational", "contribution", "mission"]).describe("Section 2. The four batteries."),
  "charge_state": z.enum(["full", "partial", "depleted"]).describe("Section 2. The charge state of a battery; silence is not one of the values."),
  "developmental_state": z.object({
  "breadth": z.string().describe("The inclusivity of the frame, how many distinct perspectives it can hold simultaneously without collapsing to a dominant one.").optional(),
  "depth": z.string().describe("Precision of interpretive capacity, built through transclusion events that move a prior position from ceiling to floor.").optional(),
  "durability": z.string().describe("The persistence of developmental state under conditions that would reverse or suppress it.").optional()
}).strict().describe("Section 2. The permanent axis, when the organization tracks it, across depth, breadth, and durability.").optional()
}).strict()).describe("Section 2. The four batteries, each rendered as a typed object carrying its charge state and, when tracked, its developmental state. They are constitutive of a capacity declaration; a record naming no batteries could claim capacity while assessing nothing."),
  "checking_practice": z.object({
  "adverse_result_integrity": z.boolean().describe("A low or declining result is demonstrably received and responded to."),
  "regularity": z.boolean().describe("The check happens on a defined cadence, not only when prompted by crisis."),
  "specificity": z.boolean().describe("The check produces a result specific enough to be wrong."),
  "structural_embeddedness": z.boolean().describe("The check is embedded in coordination activity rather than appended as a separate periodic review.")
}).strict().describe("Section 7.2. The four conditions that make a battery check genuine rather than theater. Conformance is defined by the quality of the checking practice, not the level it reveals."),
  "conformance": z.object({
  "checking_practice_genuine": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "contribution_battery_charged": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "mission_battery_charged": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "personal_battery_charged": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "relational_battery_charged": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "scope_conditions_present": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values.")
}).strict().describe("The conformance answers on the face. There is deliberately no overall or total field: conformance is per-battery at the charge layer plus the checking practice and the scope conditions, mirroring the suite's refusal to collapse a profile into a single number. The developmental-state axis is transparency-based and is not a conformance threshold."),
  "scope_adoption_tier": z.enum(["scope_visibility", "structural_review", "full_conformance"]).describe("Section 8.6. The three scope-and-delegation adoption tiers.").optional(),
  "scope_conditions": z.array(z.object({
  "condition": z.string().describe("The scope-and-delegation condition, stated operationally."),
  "status": z.enum(["present", "absent", "not_applicable"]).describe("The status of a scope-and-delegation condition; silence is not one of the values.")
}).strict()).describe("Section 8.2. The four scope-and-delegation conditions, each with its status.").optional(),
  "subject": z.string().describe("The coordination unit or organization whose capacity is declared.")
}).strict();

export type FourBatteriesRecord = z.infer<typeof FourBatteriesRecord>;
