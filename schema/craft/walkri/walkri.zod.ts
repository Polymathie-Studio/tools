import { z } from "zod";

// Generated from walkri.schema.json. Do not edit by hand; run generate.py.
export const SpecifiedInstrument = z.object({
  "chain_attribution": z.object({
  "chain_condition_served": z.string().describe("The chain condition this instrument's quality serves (its layer attribution), where WALKRI operates inside a chain.").optional(),
  "resolution": z.string().describe("WALKRI Section 8.3. The resolution the instrument's criterion elements specify, carried upward rather than a bare pass mark, so the precision actually achieved at the capture point travels.").optional(),
  "standalone": z.boolean().describe("The Declared-Absent value. True where WALKRI is used standalone, outside any evaluation chain.")
}).strict().describe("WALKRI Section 8.3. Where WALKRI operates inside an evaluation chain, the chain condition this instrument serves (its layer attribution), or the Declared-Absent value where WALKRI is used standalone.").optional(),
  "conformance": z.object({
  "conformance_threshold_status": z.enum(["pass", "fail", "override"]).describe("WALKRI Part VIII. The status of one criterion specification requirement on one instrument. Silence is not one of the values."),
  "criterion_intent_status": z.enum(["pass", "fail", "override"]).describe("WALKRI Part VIII. The status of one criterion specification requirement on one instrument. Silence is not one of the values."),
  "evidence_form_status": z.enum(["pass", "fail", "override"]).describe("WALKRI Part VIII. The status of one criterion specification requirement on one instrument. Silence is not one of the values."),
  "operational_definition_status": z.enum(["pass", "fail", "override"]).describe("WALKRI Part VIII. The status of one criterion specification requirement on one instrument. Silence is not one of the values."),
  "overrides": z.array(z.object({
  "authorized_by": z.string().describe("The name or identifier of the person who authorized the override."),
  "flag_text": z.string().describe("The text of the flag being overridden."),
  "justification": z.string().describe("The justification for the override."),
  "requirement": z.enum(["criterion_intent", "operational_definition", "response_form", "evidence_form", "conformance_threshold"]).describe("WALKRI Part III. The five criterion specification requirements an override can apply to.")
}).strict()).describe("WALKRI Section 8.3. One entry for each requirement whose status is override, carrying the flag, the justification, and the authorizer.").optional(),
  "response_form_status": z.enum(["pass", "fail", "override"]).describe("WALKRI Part VIII. The status of one criterion specification requirement on one instrument. Silence is not one of the values.")
}).strict().describe("WALKRI Part VIII. The per-requirement conformance status of the instrument: for each of the five criterion specification requirements, pass, fail, or override. There is deliberately no overall or total field. The minimum conformance threshold (Section 8.4, all five pass, overrides permitted where documented) is a computed rule over these five statuses, never a stored bare pass mark."),
  "conformance_threshold": z.object({
  "applicable_components": z.array(z.string()).describe("Which components of the external standard apply to this criterion.").optional(),
  "evidence_per_component": z.string().describe("What evidence satisfies each applicable component.").optional(),
  "minimum_threshold": z.string().describe("The minimum threshold for passage (which components must be met, and which are non-waivable).").optional(),
  "not_applicable_reason": z.string().describe("Where no external standard is referenced, the declared reason the conformance-threshold content is not applicable.").optional(),
  "references_external_standard": z.boolean().describe("Whether this instrument references an external standard."),
  "registry_treatment": z.string().describe("Where the external standard maintains a registry, whether registry membership is accepted as sufficient evidence of current qualification or independent assessment is required regardless of registry status.").optional()
}).strict().describe("WALKRI Section 3.5. For an instrument that references an external standard, the components that apply, the evidence that satisfies each, the minimum passage threshold, and the treatment of any registry the standard maintains. Where no external standard is referenced, references_external_standard is false and a not_applicable_reason is declared, never left silent."),
  "criterion_intent": z.object({
  "label": z.string().describe("The instrument's label (a name)."),
  "measurement_claim": z.string().describe("What a true response tells us about the subject. A measurement claim distinct from the label.")
}).strict().describe("WALKRI Section 3.1. A measurement claim, not a name. Records the label and the intent separately so the intent's distinctness from the label is legible."),
  "dependency_declaration": z.object({
  "edges": z.array(z.object({
  "depends_on": z.string().describe("The instrument this one depends on."),
  "relation": z.string().describe("The formal relation from which the edge was derived (the conditional logic that produced it).")
}).strict()).describe("The derived and attested dependency edges, where the instrument depends on others.").optional(),
  "independent": z.boolean().describe("The Declared-Absent value. True where the instrument has no dependency edges.")
}).strict().describe("WALKRI Section 3.9. The instrument's dependency graph, derived mechanically from the instrument set's own formal logic and attested, or the Declared-Absent value where the instrument has no dependency edges. An independent instrument declares its independence rather than falling silent."),
  "evidence_form": z.array(z.object({
  "access_path": z.string().describe("The path by which a reviewer independently locates and verifies the evidence, resolving without login, access request, or contact with the applicant."),
  "completion_sufficiency": z.enum(["sufficient_to_verify_completion", "supporting_context_only"]).describe("WALKRI Section 3.4. For a completion claim, whether an evidence type verifies completion or only supports context.").optional(),
  "evidence_type": z.enum(["standing", "activity", "outcome", "planning", "financial_accountability"]).describe("WALKRI Section 3.4. The five evidence types; each proves a different thing and they are not interchangeable."),
  "required_content": z.string().describe("The specific elements this evidence type must contain (the required elements named for the type).")
}).strict()).describe("WALKRI Section 3.4. The artifact that satisfies the criterion, one entry per required evidence type. A single criterion may require more than one type."),
  "instrument_identifier": z.string().describe("What instrument this specifies (the field name or instrument label)."),
  "modality": z.enum(["form_field", "prompt_constraint", "structured_output_schema_element", "rubric_item", "extraction_specification"]).describe("WALKRI Part I. The modality in which an instrument is rendered; the five requirements attach in each."),
  "operational_definition": z.object({
  "categories": z.array(z.object({
  "category": z.string().describe("The option or response category being defined."),
  "definition": z.string().describe("The complete definition of this category."),
  "edge_case": z.string().describe("For a binary field, an edge-case determination.").optional(),
  "non_qualifying_examples": z.array(z.string()).describe("Examples that do not qualify for this category.").optional(),
  "qualifying_examples": z.array(z.string()).describe("Examples that qualify for this category.").optional()
}).strict()).describe("Per-option definitions for a categorical, binary, or numeric instrument.").optional(),
  "text_minimum_content": z.string().describe("For a text or narrative instrument, the minimum content that constitutes a complete response.").optional(),
  "text_scope": z.string().describe("For a text or narrative instrument, the scope of acceptable response content.").optional()
}).strict().describe("WALKRI Section 3.2. A complete definition of each option, with qualifying and non-qualifying examples, or, for a text field, the scope and minimum content that constitutes a complete response."),
  "participatory_specification": z.object({
  "contribution": z.string().describe("What aspect of the definition they contributed to or validated."),
  "participants": z.string().describe("Who participated, described by role or relationship to the measured condition."),
  "timing": z.string().describe("When the participation occurred relative to the instrument's publication.")
}).strict().describe("WALKRI Section 3.6. Optional. The record of population input into the definition, where the instrument measures a condition an identifiable group experiences.").optional(),
  "response_form": z.object({
  "justification": z.string().describe("Why this response type is appropriate for the criterion intent, addressing whether it captures the required variance."),
  "response_type": z.enum(["single_select", "multi_select", "binary", "numeric", "text", "url", "composite"]).describe("WALKRI Section 3.3. The response type of an instrument.")
}).strict().describe("WALKRI Section 3.3. The response type and a written justification that the type can capture the variance in the construct the criterion intent requires. Response type is a measurement decision, not a formatting one.")
}).strict();

export type SpecifiedInstrument = z.infer<typeof SpecifiedInstrument>;
