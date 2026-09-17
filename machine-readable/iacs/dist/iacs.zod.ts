import { z } from "zod";

// Generated from iacs.schema.json. Do not edit by hand; run generate.py.
export const IACSConformanceRecord = z.object({
  "applicable_mechanisms": z.array(z.object({
  "cynefin_domain": z.enum(["clear", "complicated", "complex", "chaotic"]).describe("Section 4.1. The Cynefin domains and their detection action modes.").optional(),
  "detection_surface": z.array(z.string()).describe("Section 2 criterion 3. The observable signals in the coordination record that indicate the mechanism is active."),
  "id": z.string().describe("The mechanism handle (for example, positional, interpretive, synthetic_coordination)."),
  "mechanism": z.string().describe("Section 2 criterion 1. The distinct causal process by which advantage accumulates through informational position."),
  "name": z.string(),
  "orthogonal_at_mechanism": z.boolean().describe("Section 2 criterion 4. True when the mechanism is individuated at the level of causal process, so its presence does not entail another's."),
  "remediation_direction": z.string().describe("Section 5 Scope. The structural remediation direction the mechanism implies; a pointer, since IACS defers the remediation architecture.").optional(),
  "status": z.enum(["primary", "extension_specified", "extension_stub_scoped_out"]).describe("Section 5. The specification status of a mechanism."),
  "sub_pattern": z.array(z.string()).describe("A named sub-pattern of this mechanism (for example, Distributed Monoculture, Coordination Record Asymmetry, Consensus Manufacturing).").optional()
}).strict()).describe("Section 6. The mechanisms the system identifies as applicable, rendered as structured objects (the code system, not a label list). Each carries its causal process, detection surface, orthogonality, status, Cynefin domain, and remediation direction."),
  "architecture": z.object({
  "adopted_tier": z.enum(["assessed", "operational", "instrumented", "loop_closed", "auditable"]).describe("Section 6. The adoption tiers."),
  "applicability_inventory": z.boolean().describe("Section 6 Assessed. A class applicability inventory naming applicable, partial, and not-applicable mechanisms with a present, assumed, or absent detection state."),
  "audience_baseline_declared": z.boolean().describe("Section 6 Instrumented. The audience linguistic, epistemic, and ontological baseline, required when Descriptive Capacity asymmetry is applicable in a document-production context.").optional(),
  "classification_process_documented": z.boolean().describe("Section 6 Operational. A documented classification process per applicable mechanism.").optional(),
  "cynefin_documented": z.boolean().describe("Section 6 Instrumented. A documented Cynefin domain classification per mechanism with the matching action mode.").optional(),
  "detection_architecture_present": z.boolean().describe("Section 6 Instrumented. A real-time detection architecture instrumenting the surfaces, disclosed to participants.").optional()
}).strict().describe("The system-level detection architecture and tier. Higher-tier fields are optional in the schema; the checker requires them at the tiers the register specifies."),
  "classifications": z.array(z.object({
  "cynefin_domain": z.enum(["clear", "complicated", "complex", "chaotic"]).describe("Section 4.1. The Cynefin domains and their detection action modes."),
  "detection_signals_observed": z.array(z.string()).describe("The specific detection-surface signals observed in the record."),
  "mechanism": z.string().describe("The handle of the mechanism assigned (references an applicable_mechanisms entry).")
}).strict()).describe("Section 6. The classifications the system has produced, each referencing a mechanism and the signals observed.").optional(),
  "conformance": z.object({
  "applicability_mapped": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-obligation answer; silence is not one of the values."),
  "classification_process_documented": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-obligation answer; silence is not one of the values."),
  "detection_instrumented": z.enum(["satisfied", "declared_absent_with_justification", "not_applicable"]).describe("Per-obligation answer; silence is not one of the values.")
}).strict().describe("The per-obligation conformance answers on the face. There is deliberately no overall or total field: conformance is per-obligation, mirroring the suite's refusal to collapse a profile into a single number.")
}).strict();

export type IACSConformanceRecord = z.infer<typeof IACSConformanceRecord>;
