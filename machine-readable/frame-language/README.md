# Frame Language (machine-readable layer)

Frame Language reads which stance a term speaks from (Frame 1, Frame 2, Frame 3) in actual
vocabulary and construction, so the gap between a stated intent and the structure a term
actually specifies is legible and machine-checkable. Its machine-readable layer is a
code-system: a controlled vocabulary published as data plus its schema.

## What is here

- `src/term-registry.json` : the canonical Frame 1 vocabulary registry, the one source the skill,
  the MCP server, and the analyzer derive their watchlists from. Reconciled from the three prior
  encodings (the Frame Language Grammar, the MCP server watchlist, the analyzer term registry).
- `src/term-registry.schema.json` : the JSON Schema the registry validates against, `$id` on the
  Polymathie host.
- `frame-language-registry.json` : the family seed (metadata plus members) the manifest is
  generated from.
- `generate-frame-language-manifest.py` : emits `frame-language-manifest.json` and publishes the
  catalog, its schema, and the manifest into `schema/frame-language/`.
- `validate.py` : structural validation of the registry against the schema (stdlib only).

## Published surfaces

- Manifest: `schema/frame-language/frame-language-manifest.json`
- Catalog: `schema/frame-language/term-registry.json`
- Schema: `schema/frame-language/term-registry.schema.json`

Raw host: `https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/frame-language/`

## Regenerate

```
python3 machine-readable/frame-language/validate.py
python3 machine-readable/frame-language/generate-frame-language-manifest.py
```

## Scope of this establishment

This is the low-risk establishment: the registry, its schema, and the family manifest on the one
source, alongside the other three families. It makes no change to the live surfaces. Two things
are deliberately deferred and remain the author's calls:

- The prose standards (Dimensional Frame Language, the Frame Language Grammar, the Foundational
  Vocabulary Specification, the last currently filed with the Coordination Structural Integrity
  Suite) are added as members once their public canonical locations are confirmed.
- Rewiring the live surfaces (skill, MCP server, analyzer) to fetch their watchlists from this
  registry, which completes the derive-from-one-source design, is a gated follow-up.
