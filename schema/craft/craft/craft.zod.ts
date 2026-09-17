import { z } from "zod";

// Generated from craft.schema.json. Do not edit by hand; run generate.py.
export const EvaluationRecord = z.object({
  "condition_findings": z.array(z.object({
  "basis": z.string().describe("The basis on which the result was reached."),
  "condition": z.enum(["condition_1_decision_context", "condition_2_technical_ontology", "condition_3_measurement_instruments", "condition_4_pre_specified_criteria", "condition_5_decision_logic", "condition_6_feedback_propagation"]).describe("CRAFT Section 5. The six conditions an evaluation chain must satisfy."),
  "layer": z.enum(["craft_base", "domain_application", "per_axis_quality"]).describe("CRAFT Section 12. The architectural layer a finding concerns, preserved so the hierarchy is not flattened."),
  "result": z.string().describe("The result of evaluating this condition on this input."),
  "uncertainty_band": z.string().describe("CRAFT Section 12.2 and Condition 3. The instrument uncertainty band, where Condition 3 specified one for the instrument producing this finding, so the outcome against the Condition 4 threshold is independently checkable.").optional()
}).strict()).describe("CRAFT Section 12.2. For each condition evaluated, the result, the basis, and the layer attribution; with the uncertainty band where Condition 3 specified one."),
  "evaluation_timestamp": z.string().describe("CRAFT Section 12.2. Date and time of evaluation."),
  "gate_check_result": z.string().describe("CRAFT Section 12.2 and 7.1. The adversarial gate result at evaluation time."),
  "input_provenance": z.string().describe("CRAFT Section 12.2. A reference to the input in sufficient form to allow the finding to be checked independently."),
  "outcome": z.enum(["accepted", "rejected", "indeterminate"]).describe("CRAFT Section 12.2. The outcome against the Condition 4 threshold carrying the Condition 3 uncertainty. Indeterminate is its own outcome class, not collapsible into accepted or rejected."),
  "propagation_targets": z.array(z.object({
  "signal_class": z.string().describe("The signal class propagated (for an indeterminate outcome, the non-resolution signal class distinct from a rejection)."),
  "target_condition": z.enum(["condition_1_decision_context", "condition_2_technical_ontology", "condition_3_measurement_instruments", "condition_4_pre_specified_criteria", "condition_5_decision_logic", "condition_6_feedback_propagation"]).describe("CRAFT Section 5. The six conditions an evaluation chain must satisfy.")
}).strict()).describe("CRAFT Section 12.2. For rejection and indeterminate outcomes, the prior condition(s) the signal must propagate to under Condition 6. An indeterminate outcome propagates as its own signal class.").optional(),
  "record_type": z.enum(["evaluation_record"]).describe("CRAFT Section 12.2. The evaluation record's declared type."),
  "specification_id": z.string().describe("CRAFT Section 12.2. The specification document in force at evaluation time."),
  "specification_version": z.string().describe("CRAFT Section 12.2. The exact version of that specification.")
}).strict();

export type EvaluationRecord = z.infer<typeof EvaluationRecord>;
