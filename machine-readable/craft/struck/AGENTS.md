# AGENTS.md: using the STRUCK machine-readable layer

For an AI agent working with STRUCK-conformant outputs. Doubles as a CLAUDE.md, Cursor rule, or Windsurf rule.

## To validate an output

An evidence-grade output is an `EvidenceGradeOutput`. Validate it against `dist/struck.schema.json` (JSON Schema 2020-12) with any standard validator, or import `dist/struck.zod.ts` in TypeScript and parse with it. A passing instance carries the five obligations in the right shape; a failing one names which is missing.

## What passing the schema does and does not mean

The schema enforces the structural obligations: the grade profile is present per dimension, derivation rungs are labeled by role, contested regions are represented rather than a single value, no combined-confidence field is present, and the conformance block answers all five questions. It does not decide the interpretive obligations: whether a refutation condition is genuinely in world terms, whether a rung is presented above its standing, whether adequacy is being asserted. Those require a reader's judgment. `src/struck-register.yaml` marks each obligation as shape, judgment, or mixed; do not report a schema pass as full STRUCK conformance.

## The conformance verdict

A STRUCK conformance result is a per-obligation verdict, in the shape of `dist/conformance.verdict.intoto.json`: an in-toto attestation whose predicate answers each obligation, with deliberately no aggregate or total field. Do not synthesize a single conformance score; report the profile.

## Do not hand-edit dist/

Every file in `dist/` is generated from `src/struck.linkml.yaml` by `generate.py`. To change the shape, edit the source and regenerate; do not edit the generated artifacts.
