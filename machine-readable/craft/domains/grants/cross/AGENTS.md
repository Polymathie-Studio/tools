# AGENTS.md: using the CROSS machine-readable conformance layer

For an AI agent validating CROSS outcome indicators. Doubles as a CLAUDE.md, Cursor rule, or Windsurf rule.

## This is the conformance layer, not the serialization layer

Use this directory to validate whether an indicator specification is well-formed against CROSS. To move round data into or out of CROSS (round configuration, operator runbooks, applicant-facing publication), use the repository's `schemas/` directory instead; that is the serialization and interop family. The two answer different questions.

## To validate an indicator specification

An indicator specification is an `IndicatorSpecification`. Validate it against `dist/cross.schema.json` (JSON Schema 2020-12) with any standard validator, or import `dist/cross.zod.ts` in TypeScript and parse with it. A passing instance carries the indicator name, the rationale, the measurement form with its three-axis classification, an operational definition with inclusion, exclusion, unit of analysis, and edge case, the construction methodology, a named data source, a target, and, where the conditions apply, a baseline, execution-and-verification instruments, and independent corroboration; a failing one names what is missing.

## The three conditional obligations

Do not treat the required-field list as the whole of it. Three conditions carry the weight: a contract-centric indicator (its obligation is a contract's behavior) must name its execution and verification instruments; a change or retroactive indicator must carry a baseline; and an applicant-controlled data source (not independently accessible) must name independent corroboration. The schema enforces all three. An indicator that satisfies the field list but fails one of these is not conformant.

## No aggregate score

The conformance verdict is an indicator profile (obligation mode and the three classification axes) plus the state of its conditional obligations, in the shape of `dist/conformance.verdict.intoto.json`, with deliberately no aggregate or total field. The schema is closed at the top level so a smuggled overall score is rejected. Report the profile, not a single number.

## What passing the schema does and does not mean

The schema enforces the shape of one indicator. It does not decide whether the rationale engages seriously with alternatives, whether the operational definition actually meets WALKRI's bar, or the round-level obligations (gate architecture, conflict of interest, the Part XIII inheritance receipt), which are audit judgments over a whole round. `src/cross-register.yaml` marks each obligation as shape, judgment, or mixed; do not report a schema pass as full CROSS conformance.

## Do not hand-edit dist/

Every file in `dist/` is generated from `src/cross.linkml.yaml` by `generate.py`. To change the shape, edit the source and regenerate; do not edit the generated artifacts.
