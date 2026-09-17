# AGENTS.md: using the ORE machine-readable layer

For an AI agent working with ORE-conformant source gradings. Doubles as a CLAUDE.md, Cursor rule, or Windsurf rule.

## To validate a graded source

A graded source is a `GradedSource`. Validate it against `dist/ore.schema.json` (JSON Schema 2020-12) with any standard validator, or import `dist/ore.zod.ts` in TypeScript and parse with it. A passing instance carries all three required dimensions with an assessment and a basis, records each confirmation mode present, addresses both extension dimensions (graded or absence-declared), declares an intake posture, and answers the four conformance questions; a failing one names what is missing.

## The grade is an uncertainty reading, not a quality rank

Every dimension records how much of a source's reliability can be seen, not how good the source is. Do not turn the profile into a single number: the schema is closed so no combined-grade field is admitted, and the conformance verdict carries no total by design. Treat ungraded as a distinct recorded state, never as a blank that reads as safe.

## What passing the schema does and does not mean

The schema enforces the structural obligations: the required dimensions are present with assessment and basis, confirmation modes are recorded rather than forced into one cell, an extension dimension either grades or declares its absence, no combined-grade field is present, and a posture is declared. It does not decide the interpretive obligations: whether a grade is being used as a worth-verdict, whether party count was substituted for effective independence, whether an opaque source was admitted by an unrecorded reason. Those require a reader's judgment. `src/ore-register.yaml` marks each obligation as shape, judgment, or mixed; do not report a schema pass as full ORE conformance.

## The conformance verdict

An ORE conformance result is a per-obligation verdict, in the shape of `dist/conformance.verdict.intoto.json`: an in-toto attestation whose predicate answers each of the four Section 8 obligations, with deliberately no aggregate or total field. Do not synthesize a single conformance score; report the profile.

## Do not hand-edit dist/

Every file in `dist/` is generated from `src/ore.linkml.yaml` by `generate.py`. To change the shape, edit the source and regenerate; do not edit the generated artifacts.
