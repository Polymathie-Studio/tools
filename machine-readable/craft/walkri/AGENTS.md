# AGENTS.md: using the WALKRI machine-readable layer

For an AI agent working with WALKRI-conformant instrument specifications. Doubles as a CLAUDE.md, Cursor rule, or Windsurf rule.

## To validate an instrument specification

An instrument specification is a `SpecifiedInstrument`. Validate it against `dist/walkri.schema.json` (JSON Schema 2020-12) with any standard validator, or import `dist/walkri.zod.ts` in TypeScript and parse with it. A passing instance carries all five criterion specification requirements, names an evidence type from the taxonomy with required content and an independent access path, states a conformance threshold (its components and passage bar where it references an external standard, or a declared not-applicable reason where it does not), declares its dependency edges or its independence, and records a per-requirement conformance status; a failing one names what is missing.

## Five requirements, and no overall score

A field is a measurement instrument only if it satisfies all five requirements; four of five is a flag to resolve or override, not a pass. Do not collapse the five statuses into a single number: the schema is closed so no overall pass-mark field is admitted, and the conformance verdict carries no total by design. Report the five statuses and, for any override, its flag, justification, and authorizer.

## What passing the schema does and does not mean

The schema enforces the structural obligations: all five requirements are present, the evidence form names a taxonomy type with an access path, a conformance threshold referencing an external standard names its components and passage bar, a non-independent instrument carries its dependency edges, and no overall pass mark is present. It does not decide the interpretive obligations: whether the criterion intent is a genuine measurement claim distinct from the label, whether the operational definition actually constrains interpretation, and the five data-quality assessments (validity, integrity, precision, reliability, timeliness). Those require a reader's judgment. `src/walkri-register.yaml` marks each obligation as shape, judgment, or mixed; do not report a schema pass as full WALKRI conformance.

## The conformance verdict

A WALKRI conformance result is a per-requirement verdict, in the shape of `dist/conformance.verdict.intoto.json`: an in-toto attestation whose predicate carries the five requirement statuses and any overrides, with deliberately no aggregate or total field. Do not synthesize a single conformance score; report the per-requirement record with the resolution each criterion element specifies.

## Do not hand-edit dist/

Every file in `dist/` is generated from `src/walkri.linkml.yaml` by `generate.py`. To change the shape, edit the source and regenerate; do not edit the generated artifacts.
