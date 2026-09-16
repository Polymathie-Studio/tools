import { z } from "zod";

// Generated from asep.schema.json. Do not edit by hand; run generate.py.
export const AdverseSignalRecord = z.object({
  "architecture": z.object({
  "adopted_tier": z.enum(["assessed", "operational", "instrumented", "loop_closed", "auditable"]).describe("ASEP 5. The adoption tiers."),
  "anti_retaliation_policy": z.boolean().describe("ASEP 4.1. Explicit anti-retaliation commitment (required by the checker at Instrumented and above).").optional(),
  "classification_framework": z.object({
  "coverage_review": z.boolean().describe("Subject to periodic coverage review for missing harm classes.").optional(),
  "ex_ante": z.boolean().describe("Defined before specific disputes."),
  "version": z.string().describe("ASEP 2.2. Versioned, defined ex-ante.")
}).strict().describe("ASEP 3.2.2. The adverse-signal categories and severity levels."),
  "escalation_architecture_present": z.boolean().describe("ASEP 3.3.6. The Signal Escalation state machine is implemented (required by the checker at Instrumented and above).").optional(),
  "logging": z.object({
  "durable": z.boolean(),
  "independent_of_evaluated_actors": z.boolean().describe("ASEP 4.3. At least one path is independent of the actors being evaluated (required by the checker at Instrumented and above).").optional(),
  "tamper_evident": z.boolean()
}).strict().describe("ASEP 3.2.1, 4.3. Durability and independence of the logs."),
  "reliability_disclosure": z.boolean().describe("ASEP 2.3. Disclosure that audit reliability is bounded until the Four Batteries Relational Battery is jointly instrumented.").optional()
}).strict().describe("The system-level ASEP context. Higher-tier blocks are optional in the schema; the checker requires them at the tiers the register specifies."),
  "classification": z.object({
  "category": z.string(),
  "complexity_domain": z.enum(["clear", "complicated", "complex", "chaotic"]).describe("ASEP 3.3.6, 3.3.7. The Cynefin domains.").optional(),
  "framework_version": z.string().describe("ASEP 2.2. The version of the classification framework in effect at signal generation (ex-ante criteria)."),
  "severity": z.enum(["low", "medium", "high"]).describe("ASEP 3.3.2. Graduated severity.")
}).strict().describe("ASEP 3.2.2. Category and severity assigned against the ex-ante versioned framework."),
  "conformance": z.object({
  "ex_ante_criteria": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("ASEP. Per-invariant answer; silence is not one of the values."),
  "finite_path_to_decision": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("ASEP. Per-invariant answer; silence is not one of the values."),
  "no_silent_erasure": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("ASEP. Per-invariant answer; silence is not one of the values.")
}).strict().describe("ASEP 2.2. The three invariant answers on the face. There is deliberately no overall or total field: conformance is per-invariant, mirroring the suite's refusal to collapse a profile into a single number."),
  "disposition": z.object({
  "kind": z.enum(["act", "monitor", "close"]).describe("ASEP 2.2. The finite-path terminal outcomes."),
  "non_adverse_judgment_recorded": z.boolean().describe("ASEP 2.2. If the signal was judged non-adverse, that judgment is itself recorded (no silent erasure).").optional(),
  "rationale": z.string()
}).strict().describe("ASEP 2.2. The terminal disposition on the finite path to decision."),
  "escalation": z.object({
  "acknowledgment_window": z.string().describe("ASEP 3.3.6. The maximum elapsed time from generation to first acknowledgment, pre-specified."),
  "stage": z.enum(["generated", "acknowledged", "auto_escalated", "obligation_triggered", "terminal_visibility"]).describe("ASEP 3.3.6. The time-governed escalation stages."),
  "window_pre_specified": z.boolean().describe("ASEP 3.3.6. The window length was published before it began running (window validity).")
}).strict().describe("ASEP 3.3.6. The time-governed Signal Escalation stage, driven by elapsed time not human initiative."),
  "navigate": z.object({
  "action": z.enum(["mitigate_or_contain", "escalate", "initiate_engagement", "monitor", "close"]).describe("ASEP 3.3.1. The bounded action set."),
  "conflict_engagement": z.object({
  "documented_exchange": z.boolean().describe("A documented exchange within the engagement process took place before Navigate terminated the signal."),
  "pathway_opened": z.boolean()
}).strict().describe("ASEP 3.3.1a. Present for a conflict-class signal; opens an engagement pathway and records a documented exchange before termination.").optional(),
  "rationale": z.string().describe("ASEP 3.3.1. The documented basis for the decision."),
  "structural_root_cause_finding": z.object({
  "finding": z.enum(["no_structural_condition", "structural_condition_identified", "insufficient_information"]).describe("ASEP 3.3.3. The three structural root cause findings.")
}).strict().describe("ASEP 3.3.3. Present when a pattern threshold triggered reclassification; one of the three named findings.").optional(),
  "time_to_assessment": z.string().describe("ASEP 3.3.1. The recorded first substantive look against the per-severity bound."),
  "time_to_first_decision": z.string().describe("ASEP 3.3.1. The recorded first decision against the per-severity bound.")
}).strict().describe("ASEP 3.3. The signal-processing lifecycle from assessment through decision."),
  "observation": z.object({
  "description": z.string().describe("What happened, stated as observation not evaluation."),
  "power_context": z.string().describe("ASEP 3.2.2. Relative power or dependency, history, and incentives, where salient.").optional(),
  "when": z.string(),
  "where": z.string(),
  "who_affected": z.string()
}).strict().describe("ASEP 3.2.1. The durable log entry, observation separated from evaluation."),
  "source": z.object({
  "reporter": z.string(),
  "role": z.string()
}).strict().describe("ASEP 3.2.1, 4.2. Any actor may log a signal that meets minimal criteria.")
}).strict();

export type AdverseSignalRecord = z.infer<typeof AdverseSignalRecord>;
