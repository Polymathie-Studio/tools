import { z } from "zod";

// Generated from cross.schema.json. Do not edit by hand; run generate.py.
export const IndicatorSpecification = z.object({
  "baseline": z.object({
  "data_source": z.string().describe("The named data source evidencing this state (required for a baseline).").optional(),
  "documented_state": z.string().describe("The documented state, expressed for a change indicator in the same units as the paired state.")
}).strict().describe("CROSS Part V. The FROM state. Required for change-obligation indicators (the documented prior condition) and for retroactive indicators (the state at the award period's start); for build-obligation indicators it documents the gap where the funder has activated beneficiary engagement.").optional(),
  "construction_methodology": z.string().describe("CROSS Part V. The calculation or counting rule in enough detail that an independent reviewer with the stated data source could replicate the result, including partial-data handling and sub-unit aggregation."),
  "data_cost_estimation": z.string().describe("CROSS Part V. Attestation that data collection is feasible within the project budget, with the approximate cost and funding source. An indicator that cannot be collected within budget has not been operationalized."),
  "data_source": z.object({
  "collection_method": z.string().describe("How the data is collected."),
  "independent_corroboration": z.string().describe("CROSS Part V. Where the source is applicant-controlled (not independently accessible), the named independent corroboration that makes the data auditable.").optional(),
  "independently_accessible": z.boolean().describe("Whether the source is accessible to an independent reviewer without relying on the applicant."),
  "source": z.string().describe("The named data source.")
}).strict().describe("CROSS Part V. The named source and collection method. The source must be accessible to an independent reviewer; an applicant-controlled source without named independent corroboration does not satisfy the data-quality standard."),
  "disaggregation": z.array(z.string()).describe("CROSS Part V. The categories by which indicator values will be reported. Committed categories may be supplemented but not removed without committee approval, protecting longitudinal comparability.").optional(),
  "indicator_name": z.string().describe("CROSS Part V. A short descriptive label. Not the operational definition; the same name may carry different operational definitions across funders."),
  "measurement_form": z.object({
  "aggregation_type": z.enum(["cumulative", "non_cumulative"]).describe("CROSS Part V. Whether values sum across reporting periods."),
  "contract_centric": z.boolean().describe("CROSS Part V. True where the obligation object is a contract's behavior under specified conditions rather than a discrete artifact or count."),
  "execution_verification": z.object({
  "failure_surface": z.string().describe("At least one example of behavior that would constitute a failure to meet the invariant, and how the chosen instrument would detect it."),
  "invariant_specification": z.string().describe("A narrative description of the invariants or properties the contract must satisfy (conservation of balances, absence of re-entrancy on named functions, bounded slippage), the human-readable counterpart of the formal specification."),
  "verification_artifact": z.string().describe("The concrete completion evidence, a proof object, a named-firm audit report, or a named contract and query a reviewer can use to reproduce the behavioral check from public chain data."),
  "verification_method": z.string().describe("Whether the invariant is assessed by formal verification, independent audit, manual review of on-chain behavior, continuous monitoring, or a combination; if formal, the named tool or approach.")
}).strict().describe("CROSS Part V. Where the obligation object is a contract's behavior, the execution and verification instruments that confirm completion.").optional(),
  "form": z.enum(["quantitative", "ordinal", "binary", "qualitative"]).describe("CROSS Part V. How a result is expressed."),
  "plain_language_form": z.string().describe("What a result looks like and in what form it will be reported, in plain language (a count of unique addresses, a shipped library version, a binary against defined completion criteria)."),
  "source_type": z.enum(["on_chain_verifiable", "off_chain_verifiable", "qualitative_narrative"]).describe("CROSS Part V. Where a result is verified from.")
}).strict().describe("CROSS Part V. The measurement form in plain language, classified on three axes for data-quality assessment, with the execution-and-verification instruments named where the obligation object is a contract's behavior rather than a discrete artifact or count."),
  "obligation_mode": z.enum(["build", "change", "retroactive"]).describe("CROSS Part III. The obligation mode an indicator serves."),
  "operational_definition": z.object({
  "edge_case_determination": z.string().describe("At least one example of how an ambiguous instance is handled."),
  "exclusion_criteria": z.string().describe("What the indicator explicitly does not count."),
  "inclusion_criteria": z.string().describe("What qualifies as one instance of the claimed result."),
  "unit_of_analysis": z.string().describe("The named unit (person, wallet address, transaction, repository, site, or other).")
}).strict().describe("CROSS Part V, meeting WALKRI Part III Criterion 2. What counts and what does not count as one unit of the claimed result. This is the field-level composition point with WALKRI: CROSS frames the chain and WALKRI ensures the instrument is sound."),
  "rationale": z.string().describe("CROSS Part V. Why this indicator was selected over available alternatives; the diagnostic thinking that preceded tool selection. Required across all obligation modes."),
  "sustainability_plan": z.object({
  "continuation": z.string().describe("What happens to the funded work at the end of the grant period, who maintains it, and under what conditions it remains publicly accessible."),
  "cost_coverage": z.string().describe("How ongoing costs will be covered after the grant ends, naming the expected source with enough specificity to assess plausibility.").optional(),
  "end_state": z.string().describe("Where the work reaches a defined end state after which maintenance is not required, the specification of that state and when it will be declared reached.").optional(),
  "handoff": z.string().describe("Where the work is handed to another party, the receiving party's identity and the transition conditions.").optional()
}).strict().describe("CROSS Part V. Optional, activated by funder configuration. Required above a funder-defined size threshold or for infrastructure with ongoing operational requirements beyond the grant period.").optional(),
  "target": z.object({
  "data_source": z.string().describe("The named data source evidencing this state (required for a baseline).").optional(),
  "documented_state": z.string().describe("The documented state, expressed for a change indicator in the same units as the paired state.")
}).strict().describe("CROSS Part V. A documented state (a baseline FROM state or a target TO state) with the data source that evidences it.")
}).strict();

export type IndicatorSpecification = z.infer<typeof IndicatorSpecification>;
