#!/usr/bin/env python3
"""
generate.py -- CRAFT machine-readable layer, generated from one source.

Runs the same pipeline the ORE, STRUCK, and WALKRI layers use: one LinkML model
(src/craft.linkml.yaml) generates the schema and semantic tier; thin adapters carry what
LinkML does not (the JSON Schema draft pin and the canonical $id; the Zod projection; the
evaluation verdict and SARIF). Every artifact in dist/ is derived here, never hand-edited.

CRAFT is a meta-standard; its runtime output is the evaluation record (Section 12.2), the
tree root. The inheritance receipt (Section 10) and compliance report (Section 12.3) are
companion classes emitted in the same schema's $defs.

Requires (see requirements.txt and README): a Python venv with linkml and jsonref on the
PATH (the gen-* commands).

Usage: python generate.py
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "craft.linkml.yaml"
DIST = ROOT / "dist"
EX = ROOT / "examples"
DRAFT = "https://json-schema.org/draft/2020-12/schema"
SID = "https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/craft/craft/craft.schema.json"

# The six conditions (CRAFT Section 5), in order, for the SARIF rule set.
CONDITIONS = {
    "condition_1_decision_context": "CRAFT.5.1 decision context specification",
    "condition_2_technical_ontology": "CRAFT.5.2 technical ontology adequate to the decision context",
    "condition_3_measurement_instruments": "CRAFT.5.3 valid measurement instruments within the ontology",
    "condition_4_pre_specified_criteria": "CRAFT.5.4 pre-specified evaluation criteria",
    "condition_5_decision_logic": "CRAFT.5.5 explicit decision logic",
    "condition_6_feedback_propagation": "CRAFT.5.6 feedback mechanism with propagation",
}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def linkml_gen():
    """LinkML owns the schema and semantic tier: one model, many formats."""
    DIST.mkdir(exist_ok=True)
    outs = {
        "gen-json-schema": "craft.schema.raw.json",
        "gen-graphql": "craft.graphql",
        "gen-jsonld-context": "craft.jsonld",
        "gen-shacl": "craft.shacl.ttl",
        "gen-owl": "craft.owl.ttl",
    }
    for gen, name in outs.items():
        (DIST / name).write_text(run([gen, str(SRC)]).stdout)
    print(f"  LinkML: generated {len(outs)} formats")


def _coerce_bool_consts(node):
    """LinkML renders a boolean-slot rule precondition (equals_string on a boolean) as a
    string const ("true"/"false"), which never matches the real boolean value in the data, so
    the generated if/then silently never fires. CRAFT's rules key on string enums (outcome,
    background_state), where a string const matches correctly, so this pass is a no-op here;
    it is kept for uniformity with the family's generators, where boolean-discriminated rules
    do occur (see the WALKRI layer)."""
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
    draft and does not set the $id). CRAFT carries its traceability in the register."""
    schema = json.loads((DIST / "craft.schema.raw.json").read_text())
    schema["$schema"] = DRAFT
    schema["$id"] = SID
    _coerce_bool_consts(schema)
    # Close the top-level schema to match its own tree-root $def. LinkML leaves the root
    # object open (additionalProperties: true) even though the tree-root class is closed,
    # which would let a flattening or aggregate field slip past at the top level and defeat
    # the Section 12 machine-readable-output constraint (preserve the hierarchy, do not
    # flatten) the closed schema is meant to enforce by absence.
    schema["additionalProperties"] = False
    (DIST / "craft.schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    (DIST / "craft.schema.raw.json").unlink()
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
    Conditional obligations (the Section 12.2 propagation rules and the Section 10 background
    rule) are not expressed in Zod (Zod has no native if/then); they are enforced against the
    JSON Schema by the tests."""
    import jsonref
    schema = json.loads((DIST / "craft.schema.json").read_text())
    schema.pop("$id", None); schema.pop("$schema", None)  # else jsonref resolves refs against $id
    deref = dict(jsonref.replace_refs(schema, proxies=False, lazy_load=False))
    deref.pop("$defs", None)
    body = _zod(deref)
    ts = ('import { z } from "zod";\n\n'
          "// Generated from craft.schema.json. Do not edit by hand; run generate.py.\n"
          "export const EvaluationRecord = " + body + ";\n\n"
          "export type EvaluationRecord = z.infer<typeof EvaluationRecord>;\n")
    (DIST / "craft.zod.ts").write_text(ts)
    print("  Zod adapter: dist/craft.zod.ts (controlled converter)")


def attestation_adapter():
    """Adapter: project an evaluation record to an in-toto attestation (the runtime verdict,
    carrying the outcome and per-condition findings, no collapsing) and a SARIF run. CRAFT's
    outcome is a single accepted/rejected/indeterminate class, and indeterminate is preserved
    as its own class rather than folded into accept or reject; there is no aggregate score to
    carry beyond it."""
    import yaml
    rec = yaml.safe_load((EX / "conformant.yaml").read_text())
    findings = rec.get("condition_findings", [])
    vsa = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [{"name": rec["specification_id"], "digest": {"sha256": "<sha256 of the evaluated input>"}}],
        "predicateType": "https://standards.crosswalkri.org/craft/evaluation/v0.4.6",
        "predicate": {"verifier": "craft-evaluation",
                      "outcome": rec["outcome"],                    # accepted / rejected / indeterminate, not collapsed
                      "condition_findings": findings,
                      "gate_check_result": rec.get("gate_check_result"),
                      "propagation_targets": rec.get("propagation_targets", [])},
    }
    (DIST / "conformance.verdict.intoto.json").write_text(json.dumps(vsa, indent=2) + "\n")
    # SARIF: one result per condition finding, severity tied to the record outcome (a rejected
    # record is an error, an indeterminate one a note, an accepted one clean), with the finding
    # layer preserved in the message so the hierarchy is not flattened.
    outcome_level = {"accepted": "none", "indeterminate": "note", "rejected": "error"}
    lvl = outcome_level.get(rec["outcome"], "warning")
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": "craft-evaluation", "version": "0.4.6",
                                "rules": [{"id": k, "shortDescription": {"text": v}} for k, v in CONDITIONS.items()]}},
            "results": [{"ruleId": f.get("condition", "unknown"),
                         "level": lvl,
                         "message": {"text": f"{f.get('condition')} [{f.get('layer')}]: {f.get('result')}"}} for f in findings],
        }],
    }
    (DIST / "conformance.sarif").write_text(json.dumps(sarif, indent=2) + "\n")
    print("  attestation adapter: in-toto evaluation verdict (outcome not collapsed) + SARIF")


def main():
    linkml_gen()
    conventions_adapter()
    zod_adapter()
    attestation_adapter()
    print("done. artifacts in dist/")


if __name__ == "__main__":
    sys.exit(main())
