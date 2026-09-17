import { z } from "zod";

// Generated from sms.schema.json. Do not edit by hand; run generate.py.
export const SensemakingRecord = z.object({
  "action_invariants": z.array(z.object({
  "action": z.enum(["residue", "direction", "phase"]).describe("Section 5. The three action invariants."),
  "assessment": z.string().describe("What the record observed against the marker.").optional(),
  "observable_marker": z.string().describe("Section 5. The marker in the coordination record by which the action invariant is assessed.")
}).strict()).describe("Section 5. The three action invariants (residue, direction, phase), each rendered as a typed object carrying its observable marker. An action invariant named without its observable marker is a label, not a structural property.").optional(),
  "architecture": z.object({
  "adopted_tier": z.enum(["assessed", "operational", "instrumented", "loop_closed", "auditable"]).describe("Section 9. The five adoption tiers."),
  "adoption_condition": z.enum(["constitutional", "remedial_born_without", "remedial_crossed_below"]).describe("Section 9. Which adoption condition the adopter is in.").optional(),
  "capacity_assessment": z.object({
  "alignment_conditions_assessed": z.boolean().describe("Section 6.1. Whether the alignment between participants and the purpose is assessed."),
  "bilateral_obligation_present": z.boolean().describe("Section 6.2. Whether the bilateral obligation holds (structural adjustment when depleted, accountability when charged)."),
  "conformant_framework": z.string().describe("The named capacity framework satisfying the obligation when one is used (the Four Batteries Capacity Standard is one).").optional(),
  "contribution_conditions_assessed": z.boolean().describe("Section 6.1. Whether the conditions of participants' recognized contributions are assessed."),
  "individual_states_assessed": z.boolean().describe("Section 6.1. Whether the inner states of individual participants are assessed."),
  "method": z.string().describe("The agreed-upon method for making participants' capacity states legible to each other."),
  "participant_consent": z.boolean().describe("Section 6.1. Whether participants consented to the assessment method rather than it being imposed by management."),
  "relational_conditions_assessed": z.boolean().describe("Section 6.1. Whether the quality of working relationships is assessed.")
}).strict().describe("Section 6. The capacity obligation, required by the checker at SMS-Instrumented and above. Deferred to a conformant capacity framework; names the four capacity categories, the bilateral obligation, and participant consent without prescribing an instrument.").optional(),
  "independent_auditability": z.boolean().describe("Section 9.5. Whether the complete sensemaking record is verifiable by an independent auditor without operator cooperation (required by the checker at SMS-Auditable).").optional(),
  "loop_closure_present": z.boolean().describe("Section 9.4. Whether the closed coordination loop is in place, so a detected sensemaking failure produces a mandatory documented review and the absence of a review is structurally visible (required by the checker at SMS-Loop-Closed and above).").optional(),
  "structural_assumptions_acknowledged": z.boolean().describe("Section 7.1, 9.6. Whether the three named structural assumptions (agent-priority, human-scope, separability) are acknowledged; constitutive, so required.")
}).strict().describe("The system-level SMS context the record declares against. The adopted tier, the adoption condition, the acknowledged structural assumptions, the capacity assessment, and the higher-tier loop-closure and auditability blocks. The higher-tier blocks are optional in the schema; the checker requires them at the tiers the register specifies."),
  "conformance": z.object({
  "action_entangled_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "disruption_occasioned_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "particular_to_general_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "sufficiency_oriented_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values."),
  "temporally_structured_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-invariant answer; silence is not one of the values.")
}).strict().describe("Section 3. The five per-process invariant answers on the face. There is deliberately no overall or total field: conformance is per-invariant, and the joint condition is the non-averaging conjunction of the five (a single violated invariant does not average away against the others), mirroring the suite's refusal to collapse a profile into a single number."),
  "disruption": z.object({
  "description": z.string().describe("What stopped making sense, the surprise, gap, or expectation violation that broke intelligibility."),
  "recorded_as_initiating": z.boolean().describe("Section 3.1. Whether the disruption is recorded as the initiating event rather than reconstructed after the fact.").optional(),
  "specifiable": z.boolean().describe("Section 3.1. Whether the specific disruption event can be identified and the process would not have run in its absence.")
}).strict().describe("Section 3.1. The disruption-occasioned invariant realized: an event that cannot be accounted for by the current operative frame without revising it. A disruption with no specifiable initiating event is not disruption-occasioned, so description and specifiable are required."),
  "entanglement": z.object({
  "actions_changed_understanding": z.boolean().describe("Section 3.3. Whether actions taken during the process changed what was understood."),
  "not_pre_planned": z.boolean().describe("Section 3.3. Whether the action sequence emerged from the interaction rather than being pre-planned.").optional(),
  "understanding_changed_actions": z.boolean().describe("Section 3.3. Whether what was understood changed which actions were taken next.")
}).strict().describe("Section 3.3. The action-entangled invariant realized: action generates the data sensemaking needs, and sensemaking shapes the action taken. Both directions of the loop are required, since severing either (analysis paralysis one way, unreflective execution the other) breaks the invariant."),
  "relating": z.object({
  "cues": z.array(z.string()).describe("The specific cues attended to during the process."),
  "frame": z.string().describe("The general frame generated or revised from the cues."),
  "frame_revisions": z.array(z.string()).describe("How the frame was revised in response to cues that did not fit it.").optional(),
  "personal_framing_avoided": z.boolean().describe("Section 3.2. Whether structural failure modes were routed to structural causation rather than misapplied to personal causation.").optional()
}).strict().describe("Section 3.2. The particular-to-general relating invariant realized, bidirectional between cues and frame. Operates at practitioner trace tier: what an independent observer verifies is whether the record documents traced cues, the frame they informed, and the revisions they produced. Cues and a frame are required; a frame with no traceable cues is assertion, cues with no frame are cataloging."),
  "scales_addressed": z.array(z.enum(["intra_personal", "inter_personal", "witness_reception"])).describe("Section 4. The operational scales at which this process operates.").optional(),
  "sufficiency": z.object({
  "frame_provisional": z.boolean().describe("Section 3.4. Whether the frame is treated as provisional rather than definitive."),
  "next_action_tests_frame": z.boolean().describe("Section 3.4. Whether the next action was designed to generate information that could disconfirm the frame."),
  "revision_conditions": z.string().describe("Section 3.4. The evidence that would cause the frame to be revised, recorded explicitly."),
  "stopped_before_complete": z.boolean().describe("Section 3.4. Whether the process terminated before all available information was incorporated, naming the unresolved questions not pursued before acting.")
}).strict().describe("Section 3.4. The sufficiency-oriented invariant realized: a plausible account that enables a next action whose outcome generates information for revising it, satisficing rather than optimizing. The provisional frame, its named revision conditions, and a frame-testing next action are required; optimizing (seeking the correct answer first) and guessing (no revision conditions) both violate it."),
  "temporal_phases": z.object({
  "disruption_phase": z.string().describe("The phase in which intelligibility broke down and existing frames were inadequate."),
  "independently_verifiable": z.boolean().describe("Section 3.5. Whether the satisfaction is verifiable by an independent observer without depending solely on participant self-report (required by the checker at SMS-Loop-Closed and above).").optional(),
  "liminal_phase": z.string().describe("The period of not-knowing, the prior frame suspended and no replacement yet formed."),
  "liminal_phase_documented": z.boolean().describe("Section 3.5, 2.3. Whether the liminal phase is documented; its absence with a resolution frame identical to a pre-existing frame is the applying-without-understanding failure mode."),
  "resolution_distinct_from_prior": z.boolean().describe("Section 3.5. Whether the resolution frame is not identical to any frame available before the disruption."),
  "resolution_phase": z.string().describe("The phase in which a new or revised frame emerged.")
}).strict().describe("Section 3.5. The temporally-structured invariant realized, the Adverse-Signal lifecycle-state analogue. The disruption, liminal, and resolution phases, with the liminal phase the diagnostic marker: its documented presence, together with a resolution frame distinct from any pre-existing frame, is what distinguishes sensemaking from applying a pre-existing frame (the applying-without-understanding failure of Section 2.3). All three phases and the two markers are required.")
}).strict();

export type SensemakingRecord = z.infer<typeof SensemakingRecord>;
