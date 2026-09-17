#!/usr/bin/env python3
"""
generate.py -- WALKRI machine-readable layer, generated from one source.

Runs the same pipeline the ORE and STRUCK layers use: one LinkML model
(src/walkri.linkml.yaml) generates the schema and semantic tier; thin adapters carry
what LinkML does not (the JSON Schema draft pin and the canonical $id; the Zod projection;
the conformance attestation and SARIF). Every artifact in dist/ is derived here, never
hand-edited.

Requires (see requirements.txt and README): a Python venv with linkml and jsonref on the
PATH (the gen-* commands).

Usage: python generate.py
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "walkri.linkml.yaml"
DIST = ROOT / "dist"
EX = ROOT / "examples"
DRAFT = "https://json-schema.org/draft/2020-12/schema"
SID = "https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/craft/walkri/walkri.schema.json"

# The five criterion specification requirements (WALKRI Part III), in the order the
# conformance record and Section 8.4 minimum threshold read them.
REQUIREMENTS = {
    "criterion_intent_status": "WALKRI.3.1 criterion intent: a measurement claim distinct from the label",
    "operational_definition_status": "WALKRI.3.2 operational definition: each category defined with qualifying and non-qualifying examples",
    "response_form_status": "WALKRI.3.3 response form: response type justified against the required variance",
    "evidence_form_status": "WALKRI.3.4 evidence form: evidence type, required content, and independent access path",
    "conformance_threshold_status": "WALKRI.3.5 conformance threshold: applicable components, evidence, and minimum passage threshold",
}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def linkml_gen():
    """LinkML owns the schema and semantic tier: one model, many formats."""
    DIST.mkdir(exist_ok=True)
    outs = {
        "gen-json-schema": "walkri.schema.raw.json",
        "gen-graphql": "walkri.graphql",
        "gen-jsonld-context": "walkri.jsonld",
        "gen-shacl": "walkri.shacl.ttl",
        "gen-owl": "walkri.owl.ttl",
    }
    for gen, name in outs.items():
        (DIST / name).write_text(run([gen, str(SRC)]).stdout)
    print(f"  LinkML: generated {len(outs)} formats")


def _coerce_bool_consts(node):
    """LinkML renders a boolean-slot rule precondition (equals_string on a boolean) as a
    string const ("true"/"false"), which never matches the real boolean value in the data, so
    the generated if/then silently never fires. There is no boolean-equals in LinkML's rule
    DSL, so the fix lives here: coerce any const of exactly "true"/"false" to a real boolean.
    The model carries no string slot whose value is legitimately "true"/"false", so this is
    unambiguous. Without it the Section 3.5 and 3.9 conditional obligations do not enforce."""
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
    draft and does not set the $id). WALKRI carries its traceability in the register."""
    schema = json.loads((DIST / "walkri.schema.raw.json").read_text())
    schema["$schema"] = DRAFT
    schema["$id"] = SID
    _coerce_bool_consts(schema)  # make the boolean-discriminated conditionals actually fire
    # Close the top-level schema to match its own tree-root $def. LinkML leaves the root
    # object open (additionalProperties: true) even though the tree-root class is closed,
    # which would let a smuggled overall-score or bare-pass-mark field slip past at the top
    # level and defeat the Part VIII per-requirement discipline (no overall pass mark) the
    # closed schema is meant to enforce by absence.
    schema["additionalProperties"] = False
    (DIST / "walkri.schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    (DIST / "walkri.schema.raw.json").unlink()
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
    Conditional obligations (the Section 3.5, 3.9, and 8.3 rules) are not expressed in Zod
    (Zod has no native if/then); they are enforced against the JSON Schema by the tests."""
    import jsonref
    schema = json.loads((DIST / "walkri.schema.json").read_text())
    schema.pop("$id", None); schema.pop("$schema", None)  # else jsonref resolves refs against $id
    deref = dict(jsonref.replace_refs(schema, proxies=False, lazy_load=False))
    deref.pop("$defs", None)
    body = _zod(deref)
    ts = ('import { z } from "zod";\n\n'
          "// Generated from walkri.schema.json. Do not edit by hand; run generate.py.\n"
          "export const SpecifiedInstrument = " + body + ";\n\n"
          "export type SpecifiedInstrument = z.infer<typeof SpecifiedInstrument>;\n")
    (DIST / "walkri.zod.ts").write_text(ts)
    print("  Zod adapter: dist/walkri.zod.ts (controlled converter)")


def attestation_adapter():
    """Adapter: project a conformance record to an in-toto attestation (VSA-shaped,
    per-requirement, no total) and a SARIF run. This is the verdict tier LinkML does not
    reach; the payload is a thin projection of the generated conformance object. WALKRI's
    conformance is the five per-requirement statuses (Part VIII); there is no overall pass
    mark, mirroring the Section 8.4 minimum threshold, which is a computed rule over the
    five, never a stored total."""
    import yaml
    inst = yaml.safe_load((EX / "conformant.yaml").read_text())
    conf = inst["conformance"]
    statuses = {k: conf[k] for k in REQUIREMENTS}
    vsa = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [{"name": inst["instrument_identifier"], "digest": {"sha256": "<sha256 of the instrument specification>"}}],
        "predicateType": "https://standards.crosswalkri.org/walkri/conformance/v0.2.1",
        "predicate": {"verifier": "walkri-conformance",
                      "requirements": statuses,           # the five per-requirement statuses, no total
                      "overrides": conf.get("overrides", [])},
    }
    (DIST / "conformance.verdict.intoto.json").write_text(json.dumps(vsa, indent=2) + "\n")
    # SARIF level per requirement status: pass is clean, override is a documented exception
    # (note), fail is an error. A form with any fail, or an override missing its
    # documentation, cannot be certified (Section 8.4).
    level = {"pass": "none", "override": "note", "fail": "error"}
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": "walkri-conformance", "version": "0.2.1",
                                "rules": [{"id": k, "shortDescription": {"text": v}} for k, v in REQUIREMENTS.items()]}},
            "results": [{"ruleId": k,
                         "level": level.get(statuses[k], "warning"),
                         "message": {"text": f"{REQUIREMENTS[k]}: {statuses[k]}"}} for k in REQUIREMENTS],
        }],
    }
    (DIST / "conformance.sarif").write_text(json.dumps(sarif, indent=2) + "\n")
    print("  attestation adapter: in-toto verdict (per-requirement, no total) + SARIF")


def main():
    linkml_gen()
    conventions_adapter()
    zod_adapter()
    attestation_adapter()
    print("done. artifacts in dist/")


if __name__ == "__main__":
    sys.exit(main())
