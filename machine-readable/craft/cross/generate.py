#!/usr/bin/env python3
"""
generate.py -- CROSS machine-readable conformance layer, generated from one source.

Runs the same pipeline the ORE, STRUCK, WALKRI, and CRAFT layers use: one LinkML model
(src/cross.linkml.yaml) generates the schema and semantic tier; thin adapters carry what
LinkML does not (the JSON Schema draft pin and the canonical $id; the boolean-const rule fix;
the Zod projection; the indicator conformance verdict and SARIF). Every artifact in dist/ is
derived here, never hand-edited.

This is the CONFORMANCE (validation) layer, distinct from the repository's schemas/ directory,
which is the serialization and interop layer for moving round data into and out of CROSS.

Requires (see requirements.txt and README): a Python venv with linkml and jsonref on the
PATH (the gen-* commands).

Usage: python generate.py
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "cross.linkml.yaml"
DIST = ROOT / "dist"
EX = ROOT / "examples"
DRAFT = "https://json-schema.org/draft/2020-12/schema"
SID = "https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/craft/cross/cross.schema.json"

# The indicator field groups (CROSS Part V), for the SARIF rule set.
FIELD_GROUPS = {
    "indicator_name": "CROSS.5 indicator name",
    "rationale": "CROSS.5 rationale for the indicator over alternatives",
    "measurement_form": "CROSS.5 measurement form and three-axis classification",
    "operational_definition": "CROSS.5 operational definition (WALKRI Part III inclusion/exclusion/unit/edge-case)",
    "construction_methodology": "CROSS.5 construction and aggregation methodology",
    "data_source": "CROSS.5 named, independently accessible data source",
    "target": "CROSS.5 target TO state",
}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def linkml_gen():
    """LinkML owns the schema and semantic tier: one model, many formats."""
    DIST.mkdir(exist_ok=True)
    outs = {
        "gen-json-schema": "cross.schema.raw.json",
        "gen-graphql": "cross.graphql",
        "gen-jsonld-context": "cross.jsonld",
        "gen-shacl": "cross.shacl.ttl",
        "gen-owl": "cross.owl.ttl",
    }
    for gen, name in outs.items():
        (DIST / name).write_text(run([gen, str(SRC)]).stdout)
    print(f"  LinkML: generated {len(outs)} formats")


def _coerce_bool_consts(node):
    """LinkML renders a boolean-slot rule precondition (equals_string on a boolean) as a
    string const ("true"/"false"), which never matches the real boolean value in the data, so
    the generated if/then silently never fires. CROSS keys two rules on booleans
    (contract_centric, independently_accessible), so this pass is load-bearing here: without it
    the Part V contract-verification and independent-corroboration obligations do not enforce."""
    if isinstance(node, dict):
        if node.get("const") in ("true", "false"):
            node["const"] = (node["const"] == "true")
        for v in node.values():
            _coerce_bool_consts(v)
    elif isinstance(node, list):
        for v in node:
            _coerce_bool_consts(v)


def conventions_adapter():
    """Adapter: pin the JSON Schema draft and the canonical $id (LinkML targets an older
    draft and does not set the $id). CROSS carries its traceability in the register."""
    schema = json.loads((DIST / "cross.schema.raw.json").read_text())
    schema["$schema"] = DRAFT
    schema["$id"] = SID
    _coerce_bool_consts(schema)  # make the boolean-discriminated conditionals actually fire
    # Close the top-level schema to match its own tree-root $def, so a smuggled aggregate or
    # overall-score field cannot slip past at the top level.
    schema["additionalProperties"] = False
    (DIST / "cross.schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    (DIST / "cross.schema.raw.json").unlink()
    print("  conventions adapter: draft pinned to 2020-12, $id set, top-level closed")


def _zod(node):
    """Recursive JSON Schema -> Zod. Small and controlled, so the Zod output does not depend
    on a shifting npm converter version. Covers the constructs LinkML emits: objects, arrays,
    enums, strings with patterns, integers with minimums, booleans, and nullability."""
    if "enum" in node:
        return "z.enum([" + ", ".join(json.dumps(v) for v in node["enum"]) + "])"
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
    Conditional obligations (the Part V baseline, contract-verification, and corroboration
    rules) are not expressed in Zod (Zod has no native if/then); they are enforced against the
    JSON Schema by the tests."""
    import jsonref
    schema = json.loads((DIST / "cross.schema.json").read_text())
    schema.pop("$id", None); schema.pop("$schema", None)  # else jsonref resolves refs against $id
    deref = dict(jsonref.replace_refs(schema, proxies=False, lazy_load=False))
    deref.pop("$defs", None)
    body = _zod(deref)
    ts = ('import { z } from "zod";\n\n'
          "// Generated from cross.schema.json. Do not edit by hand; run generate.py.\n"
          "export const IndicatorSpecification = " + body + ";\n\n"
          "export type IndicatorSpecification = z.infer<typeof IndicatorSpecification>;\n")
    (DIST / "cross.zod.ts").write_text(ts)
    print("  Zod adapter: dist/cross.zod.ts (controlled converter)")


def attestation_adapter():
    """Adapter: project an indicator specification to an in-toto attestation (the indicator
    profile and the state of its conditional obligations, no total) and a SARIF run. There is
    no aggregate conformance score; the profile is what travels."""
    import yaml
    ind = yaml.safe_load((EX / "conformant.yaml").read_text())
    mf = ind.get("measurement_form", {})
    profile = {
        "obligation_mode": ind.get("obligation_mode"),
        "source_type": mf.get("source_type"),
        "measurement_form": mf.get("form"),
        "aggregation_type": mf.get("aggregation_type"),
        "contract_centric": mf.get("contract_centric"),
    }
    conditional = {
        "baseline_present": "baseline" in ind,
        "execution_verification_present": "execution_verification" in mf,
        "independent_corroboration_present": "independent_corroboration" in ind.get("data_source", {}),
    }
    vsa = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [{"name": ind["indicator_name"], "digest": {"sha256": "<sha256 of the indicator specification>"}}],
        "predicateType": "https://standards.crosswalkri.org/cross/indicator/v0.5.7",
        "predicate": {"verifier": "cross-indicator-conformance",
                      "profile": profile,                 # no aggregate score
                      "conditional_obligations": conditional},
    }
    (DIST / "conformance.verdict.intoto.json").write_text(json.dumps(vsa, indent=2) + "\n")
    # SARIF: one result per required field group; a present field is clean (none), an absent
    # one an error. A validated instance is all-clean; the run documents what was checked.
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": "cross-indicator-conformance", "version": "0.5.7",
                                "rules": [{"id": k, "shortDescription": {"text": v}} for k, v in FIELD_GROUPS.items()]}},
            "results": [{"ruleId": k,
                         "level": "none" if k in ind else "error",
                         "message": {"text": f"{FIELD_GROUPS[k]}: {'present' if k in ind else 'absent'}"}} for k in FIELD_GROUPS],
        }],
    }
    (DIST / "conformance.sarif").write_text(json.dumps(sarif, indent=2) + "\n")
    print("  attestation adapter: in-toto indicator profile (no total) + SARIF")


def main():
    linkml_gen()
    conventions_adapter()
    zod_adapter()
    attestation_adapter()
    print("done. artifacts in dist/")


if __name__ == "__main__":
    sys.exit(main())
