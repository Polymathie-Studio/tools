# Polymathie tools

The parent-brand hub for the standards families' tooling and machine-readable schemas. Polymathie is the umbrella over the Coordination Structural Integrity Suite (CSIS), the CrossWalkri evidence family, Frame Language, and the DS4AI design suite; their standards live in their own repositories, and their machine-readable schemas are hosted together here so a consumer has one place to fetch from.

## The `schema/` fetch surface

Every standard ships a machine-readable set a tool can ingest directly, with no prose to interpret. Those sets are published here and referenced by their raw GitHub URLs, which are the `$id` of each schema.

```
schema/
  standards-family-manifest.schema.json   the shared base schema every family manifest validates against
  csis/
    scls/                                  the Structural Consent Legibility Standard's set
      scls.schema.json                     JSON Schema (draft 2020-12)
      scls.zod.ts                          Zod projection
      scls.jsonld, scls.graphql,           semantic tier
      scls.shacl.ttl, scls.owl.ttl
      conformance.verdict.intoto.json      per-obligation verdict (Verification-Summary-Attestation, no total)
      conformance.sarif                    findings run
  <family>/<standard>/                     the same layout for every other standard
```

## How the sets are produced

The schemas here are generated, never hand-maintained (derive, never duplicate). Each standard's canonical source (a register and a LinkML model) lives in its own family's repository; that family's generator produces the set and publishes it here. The shared shape and the generation pipeline are specified in the CSIS corpus (the Machine-Readable Publishing Specification).

## Using a schema

Fetch the JSON Schema by its raw URL and validate an instance with any standard 2020-12 validator, or import the Zod projection in TypeScript. Passing the schema checks the structural obligations; the interpretive obligations belong to each standard's conformance checker, not the schema.
