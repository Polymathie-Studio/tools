import { z } from "zod";

// Generated from css.schema.json. Do not edit by hand; run generate.py.
export const CoordinationScalingRecord = z.object({
  "adoption_level": z.enum(["assessed", "operational", "instrumented", "loop_closed", "auditable"]).describe("Section 12. The five adoption levels."),
  "conformance": z.object({
  "effective_radius_assessed": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "maximum_conditions_absent": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "minimum_conditions_present": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values."),
  "sequential_build_respected": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-condition answer; silence is not one of the values.")
}).strict().describe("The scaling conformance answers on the face. There is deliberately no overall or total field: conformance is per-condition across crossed thresholds, mirroring the suite's refusal to collapse a profile into a single number."),
  "crossed_thresholds": z.array(z.object({
  "interface_conditions_documented": z.boolean().describe("Section (Radius).5. Whether the Radius's interface conditions are documented and externally legible.").optional(),
  "maximum_conditions": z.array(z.object({
  "condition": z.string().describe("The condition, stated operationally."),
  "detection_signal": z.string().describe("A computable signal that indicates where to look for the condition's presence or absence; it locates the check, it does not by itself prove installation.").optional(),
  "status": z.enum(["present", "absent", "not_applicable"]).describe("The status of a minimum or maximum condition; silence is not one of the values.")
}).strict()).describe("The Radius's maximum conditions, each with whether it is absent (the capture vector closed) or present (a conformance failure)."),
  "minimum_conditions": z.array(z.object({
  "condition": z.string().describe("The condition, stated operationally."),
  "detection_signal": z.string().describe("A computable signal that indicates where to look for the condition's presence or absence; it locates the check, it does not by itself prove installation.").optional(),
  "status": z.enum(["present", "absent", "not_applicable"]).describe("The status of a minimum or maximum condition; silence is not one of the values.")
}).strict()).describe("The Radius's minimum conditions, each with its installed status. These are the floor at this threshold, the compressive bound on generative scaling: a hard lower bound that must be present, so a single absent minimum condition is a conformance breach that does not aggregate away against conditions met elsewhere (the floor-aware, non-averaging discipline). This is also the structural weld: a crossed Radius cannot claim conformance while silent on its minimum conditions."),
  "radius": z.object({
  "attack_surface": z.string().describe("The exploitation vector that opens when this threshold is crossed without its minimum conditions."),
  "function_break": z.string().describe("The coordination function that breaks at this threshold."),
  "provisional": z.boolean().describe("Whether this Radius is provisional in the standard (true for Radius 500 and Radius 1500).").optional(),
  "radius": z.enum(["radius_5", "radius_15", "radius_50", "radius_150", "radius_500", "radius_1500"]).describe("Section 2. The six defined Radii, by approximate relational threshold.")
}).strict().describe("One Dunbar-scale threshold rendered as a typed structure. Individuated by the coordination function that breaks at it and the attack surface that opens, not by its number alone. The number, the function break, and the attack surface are required; a Radius reduced to its number has dropped the structure that individuates it.")
}).strict()).describe("Sections 4 to 9. One entry per crossed Radius, carrying the Radius and the status of its minimum, maximum, and interface conditions. A crossed Radius is present here iff its function break is recorded in the effective-Radius assessment; a record that names a crossed threshold without enumerating its conditions is rejected."),
  "effective_radius": z.object({
  "aggregate_factors": z.array(z.object({
  "name": z.string().describe("The factor name (member_count, interaction_quality, shared_context_depth, medium_mix, or a substrate-specific factor)."),
  "value": z.string().describe("The assessed value or level of the factor, as the assessor records it.")
}).strict()).describe("Section 2. The factors the effective Radius aggregates, as an open named set (at minimum member count, interaction frequency and quality, shared context depth, and communication medium mix); a consumer on a different scale substrate supplies its own factors here."),
  "contextual_baseline": z.string().describe("Section 11 (Precision-First Design Standard Corollary 9). A statement of the unit's structural context where it diverges from the research-derived anchor contexts, since the threshold numbers are approximations and the functional questions are primary.").optional(),
  "function_breaks": z.array(z.object({
  "approach_noted": z.boolean().describe("Section 11. Whether the function is stressed or unreliable while not yet broken, which is threshold approach, not a conformance finding, but a trigger for the next founding window.").optional(),
  "broken": z.boolean().describe("Whether the function has broken (the threshold is crossed) or still holds."),
  "function": z.string().describe("The coordination function assessed (for example state_legibility at Radius 5, sympathy_network at Radius 15, capacity_inventory at Radius 50, reputation_norm_response at Radius 150, single_narrative at Radius 500)."),
  "radius": z.enum(["radius_5", "radius_15", "radius_50", "radius_150", "radius_500", "radius_1500"]).describe("Section 2. The six defined Radii, by approximate relational threshold.")
}).strict()).describe("Section 11. One entry per assessed coordination function, recording whether it has broken. The set of broken functions determines which thresholds are crossed; this is the operative instrument, not the numeric threshold."),
  "nominal_effective_radius": z.enum(["radius_5", "radius_15", "radius_50", "radius_150", "radius_500", "radius_1500"]).describe("Section 2. The six defined Radii, by approximate relational threshold."),
  "robust_effective_radius": z.enum(["radius_5", "radius_15", "radius_50", "radius_150", "radius_500", "radius_1500"]).describe("Section 2. The six defined Radii, by approximate relational threshold.")
}).strict().describe("Section 11. The determination of the unit's effective Radius by the functional breaks, the primary instrument in all contexts, with the numeric Radius derived from them. Carries the aggregate factors as an open set and the nominal-versus-robust distinction."),
  "reach": z.object({
  "above_reach_ceiling": z.boolean().describe("Section 10.2. Whether the affected population exceeds what the unit can identify and reach through channels it maintains, so its knowledge is impressionistic (the ceiling crossed)."),
  "constituency_not_unilaterally_controlled": z.boolean().describe("Section 10.5. Whether the affected-party constituency is one the unit does not unilaterally define to its convenience.").optional(),
  "proxy_or_guardian_channel": z.boolean().describe("Section 10.4. Above the ceiling, whether a structurally authorized proxy or guardian channel is operative (not disclosure-only). A minimum condition when above the ceiling.").optional()
}).strict().describe("Section 10 (provisional). The affected-party reach-axis assessment, if the unit has made one.").optional(),
  "subject": z.string().describe("The coordination unit under assessment (a project, organization, protocol, working group, or agent unit).")
}).strict();

export type CoordinationScalingRecord = z.infer<typeof CoordinationScalingRecord>;
