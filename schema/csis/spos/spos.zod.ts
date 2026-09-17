import { z } from "zod";

// Generated from spos.schema.json. Do not edit by hand; run generate.py.
export const SPOSPowerRecord = z.object({
  "architecture": z.object({
  "adopted_tier": z.enum(["assessed", "operational", "instrumented", "loop_closed", "auditable"]).describe("Section 7. The adoption tiers."),
  "detection_disclosed": z.boolean().describe("Section 6.4. The detection surface is disclosed to participants; an undisclosed surface is a consent failure.").optional(),
  "monitor_all_dimensions": z.boolean().describe("Section 4.3. Continuous detection across all three dimensions.").optional()
}).strict().describe("The system-level detection architecture and tier. Higher-tier fields are optional in the schema; the checker requires them at the tiers the register specifies."),
  "authorized_profile_established": z.boolean().describe("Section 4.1. The authorized distribution profile exists; its absence is itself a finding."),
  "conformance": z.object({
  "authorize_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "distribute_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "monitor_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values.")
}).strict().describe("Section 4. The three invariant answers on the face. There is deliberately no overall or total field: conformance is per-invariant, mirroring the suite's refusal to collapse a profile into a single number."),
  "detected_shifts": z.array(z.object({
  "classification": z.object({
  "detection_signature": z.string().describe("The observable signature that distinguishes this classification."),
  "id": z.string().describe("The classification handle (drift, coherent_evolution, strategic_pivot, capture)."),
  "name": z.string(),
  "response_obligation": z.string().describe("The response the classification triggers.")
}).strict().describe("Section 5.1. One change classification, individuated by its detection signature and its response obligation, not by a label."),
  "dimensions_implicated": z.array(z.string()).describe("Which of the three dimensions the shift implicates."),
  "review_completed": z.boolean().describe("Whether the response obligation for the classification was completed.").optional()
}).strict()).describe("Section 5. Concentration shifts detected and classified.").optional(),
  "dimensions": z.array(z.object({
  "authorized_level": z.string().describe("The authorized distribution profile in this dimension.").optional(),
  "current_concentration": z.string().describe("The current distribution profile in this dimension."),
  "dimension": z.object({
  "detection_surface": z.array(z.string()).describe("Section 6. The primary, secondary, and tertiary signals that instrument the dimension."),
  "id": z.string().describe("The dimension handle (authority, coordination, specialization)."),
  "independent_by_design": z.boolean().describe("Section 2.3. True, because the three dimensions vary independently and are assessed independently.").optional(),
  "name": z.string(),
  "normative_benchmark": z.string().describe("The normative reference the dimension is assessed against (for example Ostrom's third principle, subsidiarity, Lukes' three dimensions).").optional(),
  "power_concern": z.string().describe("The distinct structural power concern of the dimension.")
}).strict().describe("Section 2.2, 3. One power dimension, a distinct relational-topological axis individuated by its power concern and its detection surface, not by a label. A dimension with no detection surface cannot be instrumented, so detection_surface is required."),
  "gap": z.string().describe("The gap between current and authorized in this dimension.").optional()
}).strict()).describe("Section 3, 4.1. The per-dimension assessment (current versus authorized profile and the gap), across all three dimensions."),
  "override_assessment": z.array(z.object({
  "active": z.boolean().describe("Whether the class is active; a not-active determination requires a named rationale."),
  "addressability": z.string().describe("Whether the structural condition can still be redesigned before it becomes load-bearing, or can only be disclosed and monitored.").optional(),
  "exposure_disclosure": z.string().describe("A structural exposure disclosure, required for an active class that is no longer addressable.").optional(),
  "not_active_rationale": z.string().describe("Required in prose when active is false, a named rationale rather than a default omission.").optional(),
  "override_class": z.object({
  "detection_instrument": z.string().describe("The instrument that detects the class."),
  "id": z.string().describe("The class handle (financial, military, regulatory, platform, epistemic, normative, relational)."),
  "mechanism": z.string().describe("The distinct structural mechanism of the override."),
  "name": z.string()
}).strict().describe("Section 4.5. One external-override class, a distinct structural mechanism through which an external actor can supersede internal outcomes, individuated by its mechanism and its detection instrument.")
}).strict()).describe("Section 4.5. The assessment of the seven external-override classes, active or not, with addressability.")
}).strict();

export type SPOSPowerRecord = z.infer<typeof SPOSPowerRecord>;
