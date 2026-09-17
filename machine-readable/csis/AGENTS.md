# AGENTS.md: the Coordination Structural Integrity Suite machine-readable layer

This file tells an AI agent how to consume the Coordination Structural Integrity Suite through its machine-readable layer. It doubles as a `CLAUDE.md`, a Cursor rule, and a Windsurf rule. It is the middle layer between the prose standards and the structured artifacts a tool ingests directly.

## The three layers

The suite ships in three layers. Read the one that fits your task.

1. Prose: the standard documents themselves, the source of truth. In the public suite repository under `tensegrity-suite/`, and locally under `standards/`.
2. Skill and prompt: the interpretive layer. `standards/claude-skills/` carries the reasoning frames; `standards/prompts/` carries the audit prompts. Use these to actually assess whether a coordination system conforms to a standard, because that assessment is interpretive and cannot be reduced to a machine check.
3. Machine-readable: this directory. A tool reads it to know what exists and how to reach it, with no prose to interpret.

## The machine-readable files

- `csis-manifest.json`: the canonical descriptor. Every standard and candidate, each with an id, canonical name, version, status, family group, and a `canonicalSource` pointer. Generated from `csis-registry.json` plus the versions parsed from the standards; do not edit it by hand.
- `standards-family-manifest.schema.json`: the schema the manifest validates against, shared across the standards families.
- `validate.py`: a zero-dependency contract check. Run `python3 validate.py` to confirm the manifest conforms to the schema.
- `conformance.py`: emits `csis-conformance.json`, a structured report of what the machine layer can verify about itself, and a declared list of what it cannot.
- `csis-registry.json`: the single hand-maintained seed the manifest is generated from. Edit this, then regenerate, rather than editing the manifest.

## How to use the manifest

Read `csis-manifest.json` to enumerate the suite: the ten standards (seven compressive, three generative), two supporting specifications, and the candidates. Each member's `canonicalSource` is a pointer to the standard document, not the document. To do real work with a standard, follow the pointer and read the canonical source; the manifest describes and locates, it does not reproduce. This is the substrate discipline: the layer serves pointers and metadata, never standard prose in place of source.

## Two things that are not optional

Candidates are not standards. Any member with `status: "candidate"` is not promoted and is not a conformance gate. Do not treat it as settled, do not audit against it, and do not cite it as a requirement. Its description says so; honor it.

Machine conformance is not standard conformance. This layer can verify that the manifest is schema-valid, that candidates are marked, and that sources resolve. It cannot tell you whether a coordination system meets a standard. That judgment is interpretive and lives in the audit prompts and skills. If you are asked to assess a system, go to layer 2, not this one.

## Regenerating

The layer is derived, never hand-maintained. After any change to the standards or the registry, regenerate the family manifest: `python3 standards/tools/generate-csis-manifest.py`. The generator also flags source inconsistencies (version drift, stale secondary stamps) and exits non-zero when it finds them, which is the intended gate.

## Per-standard sets (the fetch surface)

Each standard also ships its own machine-readable set under `<id>/` (register, LinkML model, generated `dist/`, worked examples), the thing a consumer fetches instead of reading the prose. The set is generated from one canonical source per standard (`<id>/src/<id>-register.yaml` and `<id>/src/<id>.linkml.yaml`) using the toolchain venv in `requirements.txt`. The per-standard flow is three commands, run with the venv on PATH:

```
python generate.py <id>          # LinkML + adapters -> <id>/dist/
python validate-fixtures.py <id> # conformant passes, every negative fixture fails
python publish-schema.py <id>    # copy <id>/dist/ into the Polymathie-Studio/tools clone and push
```

Then regenerate the manifest so the member's `machineReadable` block (pointers to the published set) updates. Adding a standard means writing its register and model, a `CONFIG` entry in `generate.py`, and fixtures, then running the three commands. The published schemas live under the Polymathie parent brand at `Polymathie-Studio/tools/schema/csis/<id>/`; the sources stay here. Gotcha: a colon inside a single-line LinkML `description:` breaks the YAML parse, so use a block scalar or reword.
