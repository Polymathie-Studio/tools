import { z } from "zod";

// Generated from scls.schema.json. Do not edit by hand; run generate.py.
export const ConsentRecord = z.object({
  "action": z.object({
  "category_level": z.boolean().describe("True if this is a category-level authorization rather than a specific action.").optional(),
  "specification": z.string().describe("The action stated precisely enough for affected parties to evaluate whether they are materially affected."),
  "trigger_condition": z.string().describe("SCLS 3.1. Required inside a category-level authorization, naming the condition under which a specific action within the class triggers a standing evaluation.").optional()
}).strict().describe("SCLS 3.1. The specified action; a category-level authorization names the trigger condition that requires a standing evaluation before a specific action proceeds."),
  "affected_constituency": z.object({
  "identification_basis": z.array(z.string()).describe("SCLS 3.1. Evidence-based where system evidence exists; self-identification permitted.").optional(),
  "identified_before_action": z.boolean().describe("SCLS 3.1. The identification event precedes execution.")
}).strict().describe("SCLS 3.1, 3.1.1. The materially-affected set, identified before the action, on an evidence-and-self-identification basis."),
  "architecture": z.object({
  "adopted_tier": z.enum(["assessed", "operational", "instrumented", "loop_closed", "auditable"]).describe("SCLS 5. The adoption tiers."),
  "detection_architecture": z.object({
  "shadow_detections": z.array(z.object({
  "escalation_threshold": z.string().describe("The signal or combination that triggers Signal Escalation."),
  "monitoring_threshold": z.string().describe("The signal that initiates monitoring."),
  "shadow_type": z.enum(["entitlement_stealing", "enduring", "martyrdom"]).describe("SCLS 5.3.1. The shadow dynamics with detection signatures.")
}).strict()),
  "transparent_to_participants": z.boolean().describe("SCLS 5.3.1. The monitored patterns are transparent to participants (itself an Observation-domain consent requirement).")
}).strict().describe("SCLS 5.3.1. Graduated shadow-dynamics detection. Required by the checker at Instrumented and above.").optional(),
  "domains_applicable": z.array(z.enum(["coordination", "data", "participation", "output", "observation"])).describe("SCLS 4. The consent domains identified as relevant to the system's operations."),
  "durable_constituency_definition": z.object({
  "accessible_without_authority_gating": z.boolean(),
  "independent_observer_determinable": z.boolean().describe("Specific enough that an independent observer can determine whether a party holds participation rights without the author's intent.")
}).strict().describe("SCLS 3.1.2. The durable, accessible definition of who holds participation rights."),
  "external_override_disclosure": z.object({
  "gap_treatment": z.string().describe("How the gap between explicit consent and externally imposed obligations is addressed. Presence is shape; adequacy is checked."),
  "jurisdictions": z.array(z.string()).describe("The external legal jurisdictions that apply.")
}).strict().describe("SCLS 2.3.2. The disclosure whose absence is a consent legibility failure."),
  "standing_evaluation": z.object({
  "distributed_evaluation": z.boolean().describe("The evaluation function is not concentrated in a single actor."),
  "evidence_backed_evaluation": z.boolean(),
  "implausible_absence_detection": z.boolean(),
  "self_identification": z.boolean()
}).strict().describe("SCLS 3.1.1. The four-element standing evaluation mechanism. Required by the checker at Instrumented and above.").optional()
}).strict().describe("SCLS system-level context. Which domains apply, the adopted tier, the durable constituency definition, the external-override disclosure, and the higher-tier blocks (standing evaluation, detection architecture) that a record declares its context against. The higher-tier blocks are optional in the schema; the checker requires them at the tiers the register specifies."),
  "authorization": z.object({
  "authorizing_set": z.array(z.string()).describe("SCLS 3.2. Neither excludes affected parties nor includes unaffected parties who dilute the affected constituency's voice."),
  "response_status": z.enum(["authorized", "not_yet_responded", "unable_to_respond"]).describe("SCLS 3.2. The distinction silence cannot collapse."),
  "system_obligations": z.object({
  "exit_or_objection_cost_not_punitive": z.boolean().describe("SCLS 6.1. The structural cost of dissent is recorded; whether it is punitive is a checked judgment."),
  "legibility": z.boolean().describe("SCLS 6.1. The action described in terms the constituency can evaluate."),
  "support": z.boolean().describe("SCLS 6.1. Analytical infrastructure to evaluate implications."),
  "time": z.boolean().describe("SCLS 6.1. A consent window proportional to complexity (Section 6.4).")
}).strict().describe("SCLS 6.1. The four obligations are on the system, not the participant. Presence is shape; the qualitative reads (is the description evaluable, is the exit cost punitive) are checked.")
}).strict().describe("SCLS 3.2, 6.1. A meaningful opportunity to authorize or refuse, the four system obligations, and the response-status distinction."),
  "conformance": z.object({
  "authorize_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("SCLS. Per-invariant answer; silence is not one of the values."),
  "cost_bearer_identified": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("SCLS. Per-invariant answer; silence is not one of the values."),
  "identify_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("SCLS. Per-invariant answer; silence is not one of the values."),
  "verify_satisfied": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("SCLS. Per-invariant answer; silence is not one of the values.")
}).strict().describe("SCLS. The invariant conformance answers on the face. There is deliberately no overall or total field: conformance is per-invariant, mirroring the suite's refusal to collapse a profile into a single number and the SLSA Verification-Summary-Attestation shape."),
  "cost_bearing_party": z.object({
  "consent_to_cost_distribution": z.boolean().describe("SCLS 2.1. Obtained before the action proceeds (native nested-required)."),
  "identity": z.string()
}).strict().describe("SCLS 2.1. Present when the cost-bearing party is distinct from both the acting and the benefiting party; when present it carries consent to the cost distribution (native nested-required). Whether a distinct cost-bearer exists is domain fact and is checked, not schema-enforced.").optional(),
  "domains_touched": z.array(z.enum(["coordination", "data", "participation", "output", "observation"])).describe("SCLS 4. Which of the five consent domains this action implicates."),
  "negotiated_limits": z.array(z.object({
  "limit": z.string().describe("An explicit boundary set by the consenting party.")
}).strict()).describe("SCLS 2.3.1. Explicit limits set by the consenting party. Absence in a serving or allowing quadrant is a shadow indicator."),
  "verification": z.object({
  "agreed_limits": z.string(),
  "durable": z.boolean().describe("SCLS 3.3. The record is durable."),
  "tamper_evident": z.boolean().describe("SCLS 3.3. The record is tamper-evident (the ASEP durable-logging requirement)."),
  "who_acted": z.string(),
  "who_bears_cost": z.string(),
  "who_benefited": z.string(),
  "who_was_affected": z.string()
}).strict().describe("SCLS 3.3. The consent record's completeness and durability."),
  "wheel": z.object({
  "both_legible_to_both_parties": z.boolean().describe("SCLS 2.3.1. Both axes were legible to both parties at the time of the interaction."),
  "who_acts": z.string().describe("The action axis. Who is acting."),
  "who_benefits": z.string().describe("The benefit axis. Who the action is for.")
}).strict().describe("SCLS 2.1, 3.2. The two independent axes, both legible to both parties (2.3.1 bidirectional awareness)."),
  "withdrawal": z.object({
  "mechanism": z.string().describe("The mechanism by which consent can be withdrawn."),
  "structural_cost": z.string().describe("The structural cost of withdrawing. Whether it exceeds participation benefit is a checked judgment.").optional()
}).strict().describe("SCLS 2.3.1. Revocability. Structurally feasible, not merely formally permitted.")
}).strict();

export type ConsentRecord = z.infer<typeof ConsentRecord>;
