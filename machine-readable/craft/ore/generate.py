#!/usr/bin/env python3
"""
generate.py -- ORE machine-readable layer, generated from one source.

Runs the same pipeline STRUCK's layer uses: one LinkML model (src/ore.linkml.yaml)
generates the schema and semantic tier; thin adapters carry what LinkML does not (the
JSON Schema draft pin and the canonical $id; the Zod projection; the conformance
attestation and SARIF). Every artifact in dist/ is derived here, never hand-edited.

Requires (see requirements.txt and README): a Python venv with linkml and jsonref on the
PATH (the gen-* commands).

Usage: python generate.py
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "ore.linkml.yaml"
DIST = ROOT / "dist"
EX = ROOT / "examples"
DRAFT = "https://json-schema.org/draft/2020-12/schema"
SID = "https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/craft/ore/ore.schema.json"


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def linkml_gen():
    """LinkML owns the schema and semantic tier: one model, many formats."""
    DIST.mkdir(exist_ok=True)
    outs = {
        "gen-json-schema": "ore.schema.raw.json",
        "gen-graphql": "ore.graphql",
        "gen-jsonld-context": "ore.jsonld",
        "gen-shacl": "ore.shacl.ttl",
        "gen-owl": "ore.owl.ttl",
    }
    for gen, name in outs.items():
        (DIST / name).write_text(run([gen, str(SRC)]).stdout)
    print(f"  LinkML: generated {len(outs)} formats")


def conventions_adapter():
    """Adapter: pin the JSON Schema draft and the canonical $id (LinkML targets an older
    draft and does not set the $id). ORE carries its traceability in the register."""
    schema = json.loads((DIST / "ore.schema.raw.json").read_text())
    schema["$schema"] = DRAFT
    schema["$id"] = SID
    # Close the top-level schema to match its own tree-root $def. LinkML leaves the root
    # object open (additionalProperties: true) even though the tree-root class is closed,
    # which would let a combined-grade field slip past at the top level and defeat the
    # Section 2.4 no-combined-number rule the closed schema is meant to enforce by absence.
    schema["additionalProperties"] = False
    (DIST / "ore.schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    (DIST / "ore.schema.raw.json").unlink()
    print("  conventions adapter: draft pinned to 2020-12, $id set, top-level closed")


def _zod(node):
    """Recursive JSON Schema -> Zod. Small and controlled, so the Zod output does not
    depend on a shifting npm converter version. Covers the constructs LinkML emits:
    objects, arrays, enums, strings with patterns, integers with minimums, booleans,
    and nullability."""
    if "enum" in node:
        return "z.enum([" + ", ".join(json.dumps(v) for v in node["enum"]) + "])"
    # LinkML wraps an optional object slot as anyOf: [<schema>, {type: null}] (nullable).
    # Unwrap the non-null member(s); optionality is already applied by the required-set
    # logic below. Without this the nullable-object slots fall through to z.any().
    if "anyOf" in node or "oneOf" in node:
        members = node.get("anyOf") or node.get("oneOf")
        non_null = [m for m in members if m.get("type") != "null"]
        if len(non_null) == 1:
            return _zod(non_null[0])
        if non_null:
            return "z.union([" + ", ".join(_zod(m) for m in non_null) + "])"
        return "z.any()"
    if "allOf" in node and len(node["allOf"]) == 1:
        return _zod(node["allOf"][0])
    t = node.get("type")
    if isinstance(t, list):
        non_null = [x for x in t if x != "null"]
        t = non_null[0] if non_null else "string"
    if t == "object" or "properties" in node:
        req = set(node.get("required", []))
        fields = []
        for name, sub in node.get("properties", {}).items():
            zt = _zod(sub)
            if sub.get("description"):
                zt += f".describe({json.dumps(sub['description'])})"
            if name not in req:
                zt += ".optional()"
            fields.append(f"  {json.dumps(name)}: {zt}")
        obj = "z.object({\n" + ",\n".join(fields) + "\n})"
        return obj + (".strict()" if node.get("additionalProperties") is False else "")
    if t == "array":
        return f"z.array({_zod(node.get('items', {}))})"
    if t == "string":
        s = "z.string()"
        return s + (f".regex(new RegExp({json.dumps(node['pattern'])}))" if "pattern" in node else "")
    if t == "integer":
        s = "z.number().int()"
        return s + (f".gte({node['minimum']})" if "minimum" in node else "")
    if t == "number":
        return "z.number()"
    if t == "boolean":
        return "z.boolean()"
    return "z.any()"


def zod_adapter():
    """Adapter: dereference ($defs inlined) then emit Zod with the controlled converter.
    Conditional obligations are not expressed in Zod (Zod has no native if/then); they are
    enforced against the JSON Schema by the tests."""
    import jsonref
    schema = json.loads((DIST / "ore.schema.json").read_text())
    schema.pop("$id", None); schema.pop("$schema", None)  # else jsonref resolves refs against $id
    deref = dict(jsonref.replace_refs(schema, proxies=False, lazy_load=False))
    deref.pop("$defs", None)
    body = _zod(deref)
    ts = ('import { z } from "zod";\n\n'
          "// Generated from ore.schema.json. Do not edit by hand; run generate.py.\n"
          "export const GradedSource = " + body + ";\n\n"
          "export type GradedSource = z.infer<typeof GradedSource>;\n")
    (DIST / "ore.zod.ts").write_text(ts)
    print("  Zod adapter: dist/ore.zod.ts (controlled converter)")


def attestation_adapter():
    """Adapter: project a conformance declaration to an in-toto attestation (VSA-shaped,
    per-obligation, no total) and a SARIF run. This is the verdict tier LinkML does not
    reach; the payload is a thin projection of the generated conformance object."""
    import yaml
    inst = yaml.safe_load((EX / "conformant.yaml").read_text())
    conf = inst["conformance"]
    Q = {
        "posture_declared_and_enforced": "ORE.8.1 intake posture declared and downstream condition enforced",
        "sources_graded_on_dimensions": "ORE.8.2 every admitted source graded on the Section 3 dimensions",
        "outputs_expose_grade_profile": "ORE.8.3 every output exposes the grade profile of its support",
        "no_grade_as_worth_verdict": "ORE.8.4 no grade presented or used as a worth-verdict",
    }
    vsa = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [{"name": inst["source_identifier"], "digest": {"sha256": "<sha256 of the source record>"}}],
        "predicateType": "https://standards.crosswalkri.org/ore/conformance/v0.1.2",
        "predicate": {"verifier": "ore-conformance", "obligations": conf},  # no total field
    }
    (DIST / "conformance.verdict.intoto.json").write_text(json.dumps(vsa, indent=2) + "\n")
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": "ore-conformance", "version": "0.1.2",
                                "rules": [{"id": k, "shortDescription": {"text": v}} for k, v in Q.items()]}},
            "results": [{"ruleId": k,
                         "level": {"satisfied": "none", "declared_absent_with_justification": "note",
                                   "not_applicable": "none"}.get(conf[k], "warning"),
                         "message": {"text": f"{Q[k]}: {conf[k]}"}} for k in Q],
        }],
    }
    (DIST / "conformance.sarif").write_text(json.dumps(sarif, indent=2) + "\n")
    print("  attestation adapter: in-toto verdict (no total) + SARIF")


def main():
    linkml_gen()
    conventions_adapter()
    zod_adapter()
    attestation_adapter()
    print("done. artifacts in dist/")


if __name__ == "__main__":
    sys.exit(main())
