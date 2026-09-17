# AGENTS.md: using the CRAFT machine-readable layer

For an AI agent working with CRAFT evaluation records and inheritance receipts. Doubles as a CLAUDE.md, Cursor rule, or Windsurf rule.

## To validate an evaluation record

An evaluation record is the tree root. Validate it against `dist/craft.schema.json` (JSON Schema 2020-12) with any standard validator, or import `dist/craft.zod.ts` in TypeScript and parse with it. A passing record declares its type, the specification id and version in force, the timestamp, the input provenance, an outcome of accepted, rejected, or indeterminate, per-condition findings that each carry a layer attribution, the gate result, and, on any non-accept outcome, the propagation targets its signal must reach; a failing one names what is missing.

## The outcome is a class, not a score

The outcome is one of accepted, rejected, or indeterminate. Do not collapse indeterminate into accepted or rejected: it is its own class, the reading could not be resolved against the threshold, and that non-resolution is information the feedback loop carries. Do not add an aggregate score; the schema is closed at the top level so a flattening field is rejected, and the verdict carries the outcome and per-condition findings, never a single number.

## Layer attribution is required on every finding

Every condition finding declares its layer: `craft_base`, `domain_application`, or `per_axis_quality`. A finding with no layer is rejected, because a rejection cannot be routed to the prior stage that caused it without knowing which layer produced it. Preserve the hierarchy; do not flatten findings into an undifferentiated list.

## The inheritance receipt and its background state

A domain application's inheritance receipt (validate against the `InheritanceReceipt` companion class) declares its chain-level receipt and the full Precision Toolkit scope, the CSIS standards and Frame Language, not CRAFT alone. Each declared inheritance carries a background state: `background_satisfied` with a validation date, or `background_unchecked` as an explicit gap. Do not omit the state, and do not declare satisfied without the date; `background_unchecked` is honest and actionable, while an undeclared omission is neither.

## What passing the schema does and does not mean

The schema enforces the Section 12 output shapes. It does not decide whether the six conditions are satisfied, whether each is structurally operative rather than run as a periodic audit, or whether the specification was examined from two directional origins. Those require a reader's judgment, and for a meta-standard they are most of what conformance means. `src/craft-register.yaml` marks each obligation as shape, judgment, or mixed; do not report a schema pass as full CRAFT conformance.

## Do not hand-edit dist/

Every file in `dist/` is generated from `src/craft.linkml.yaml` by `generate.py`. To change the shape, edit the source and regenerate; do not edit the generated artifacts.
