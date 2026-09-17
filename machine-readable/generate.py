#!/usr/bin/env python3
"""
generate.py -- CSIS per-standard machine-readable layer, generated from one source.

For a standard id, runs the pipeline on <id>/src/<id>.linkml.yaml: one LinkML model
generates the schema and semantic tier, and thin adapters carry what LinkML does not (the
JSON Schema draft pin and the canonical $id; the Zod projection; the conformance
attestation and SARIF). Every artifact in <id>/dist/ is derived here, never hand-edited.

The CSIS layer holds many standards under one family manifest (the per-family shape
principle), so this one generator is parameterized by standard id rather than copied per
repository. Add a standard by writing its <id>/src/<id>.linkml.yaml and register, and an
entry in CONFIG below.

Requires the venv toolchain (requirements.txt): linkml, jsonref, pyyaml, jsonschema.
Run: python generate.py <standard-id>     e.g.  python generate.py scls
"""
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_BIN = Path.home() / ".venvs" / "csis-machine-readable" / "bin"
DRAFT = "https://json-schema.org/draft/2020-12/schema"

# Interim schema host: all families' schemas publish under the Polymathie parent brand at
# Polymathie-Studio/tools/schema (settled 2026-09-16; a larger reorg under a top-level
# Polymathie org is deferred, so this host is interim and the URLs migrate later).
SID_BASE = "https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/csis"

# Per-standard configuration the adapters need beyond the model itself.
CONFIG = {
    "scls": {
        "version": "0.3.25",
        "root_class": "ConsentRecord",
        # what names the attested subject in a conformant instance
        "subject": lambda inst: inst["action"]["specification"],
        "conformance": {
            "identify_satisfied": "SCLS Identify invariant (3.1) satisfied on the face",
            "authorize_satisfied": "SCLS Authorize invariant (3.2) satisfied on the face",
            "verify_satisfied": "SCLS Verify invariant (3.3) satisfied on the face",
            "cost_bearer_identified": "SCLS 2.1 cost-bearing party identified with consent to the cost distribution",
        },
    },
    "asep": {
        "version": "0.7.13",
        "root_class": "AdverseSignalRecord",
        "subject": lambda inst: inst["observation"]["description"],
        "conformance": {
            "no_silent_erasure": "ASEP invariant (2.2): the signal was not silently erased; a disposition is recorded",
            "ex_ante_criteria": "ASEP invariant (2.2): classified against ex-ante versioned criteria",
            "finite_path_to_decision": "ASEP invariant (2.2): the signal reached a terminal disposition with rationale",
        },
    },
    "iacs": {
        "version": "0.1.28",
        "root_class": "IACSConformanceRecord",
        "subject": lambda inst: f"IACS detection architecture, {len(inst['applicable_mechanisms'])} mechanisms, {inst['architecture']['adopted_tier']} tier",
        "conformance": {
            "applicability_mapped": "IACS Section 6: class applicability inventory mapped",
            "classification_process_documented": "IACS Section 6: documented classification process per applicable mechanism",
            "detection_instrumented": "IACS Section 6: detection architecture instrumenting the surfaces",
        },
    },
    "spos": {
        "version": "0.1.26",
        "root_class": "SPOSPowerRecord",
        "subject": lambda inst: f"SPOS power record, {inst['architecture']['adopted_tier']} tier, {len(inst['dimensions'])} dimensions",
        "conformance": {
            "distribute_satisfied": "SPOS Distribute invariant (4.1): distribution assessed across all three dimensions",
            "authorize_satisfied": "SPOS Authorize invariant (4.2): concentration above threshold authorized by the affected constituency",
            "monitor_satisfied": "SPOS Monitor invariant (4.3): continuous detection across all three dimensions",
        },
    },
    "ros": {
        "version": "0.1.8",
        "root_class": "RegenerativeObligationRecord",
        "subject": lambda inst: f"ROS record, {inst['stance']['stance']} stance, {inst['adopted_tier']} tier",
        "conformance": {
            "extraction_visible": "ROS invariant (2.2): extraction visible in the record",
            "three_conditions_met": "ROS invariant (2.2): return satisfies all three validity conditions",
            "stance_declared": "ROS invariant (2.2): stance declared in a verifiable public record",
            "no_retroactive_reclassification": "ROS invariant (2.2): no retroactive reclassification of extraction events",
        },
    },
    "pfds": {
        "version": "2.5.0",
        "root_class": "PrecisionReview",
        "subject": lambda inst: inst["subject"],
        "conformance": {
            "violations_detectable": "PFDS invariant (2): violations are detectable",
            "compliance_serves_purpose": "PFDS invariant (2): compliance demonstrates the coordination purpose is served",
            "method_structure_congruent": "PFDS Method-Structure Congruence (3): the method matched the structural character",
            "deficits_mapped": "PFDS (6.1): deficits recorded in the precision deficit map",
        },
    },
    "css": {
        "version": "0.1.5",
        "root_class": "CoordinationScalingRecord",
        "subject": lambda inst: f"{inst['subject']} at {inst['effective_radius']['nominal_effective_radius']}, {inst['adoption_level']}",
        "conformance": {
            "effective_radius_assessed": "CSS (11): effective Radius assessed by the functional breaks, the primary instrument",
            "minimum_conditions_present": "CSS (3): all minimum conditions for all crossed thresholds present, the non-averaging floor",
            "maximum_conditions_absent": "CSS (2): maximum conditions absent at all crossed thresholds, capture vectors closed",
            "sequential_build_respected": "CSS (3): the sequential build requirement respected, no compound structural debt",
        },
    },
    "cts": {
        "version": "0.2.10",
        "root_class": "ConflictTransformationRecord",
        "subject": lambda inst: f"{inst['subject']}, {inst['adoption_tier']} tier, {len(inst['invariants'])} invariants",
        "conformance": {
            "conflict_legible": "CTS (4.1): conflict events are legible in the coordination record",
            "graduated_architecture_present": "CTS (4.2): a graduated engagement spine with adjudication last, not first",
            "proactive_disposition_protected": "CTS (4.3): proactive engagement is not structurally penalized",
            "transformation_capacity_provisioned": "CTS (4.4): operator capacity is structurally provisioned, not volunteer-dependent",
            "engagement_recognized": "CTS (4.5): conflict engagement is recognized as coordination work",
        },
    },
    "fbcs": {
        "version": "0.3.7",
        "root_class": "FourBatteriesRecord",
        "subject": lambda inst: f"{inst['subject']}, {len(inst['batteries'])} batteries, {inst.get('scope_adoption_tier', 'no scope tier')}",
        "conformance": {
            "personal_battery_charged": "FBCS (2, 7): Personal battery charge above the threshold on the defined instrument",
            "relational_battery_charged": "FBCS (2, 7): Relational battery charge above the threshold on the defined instrument",
            "contribution_battery_charged": "FBCS (2, 7): Contribution battery charge above the threshold on the defined instrument",
            "mission_battery_charged": "FBCS (2, 7): Mission battery charge above the threshold on the defined instrument",
            "checking_practice_genuine": "FBCS (7.2): the checking practice meets regularity, structural embeddedness, adverse-result integrity, and specificity",
            "scope_conditions_present": "FBCS (8.2): the four scope-and-delegation conditions are present",
        },
    },
    "sms": {
        "version": "1.1.23",
        "root_class": "SensemakingRecord",
        "subject": lambda inst: f"{inst['disruption']['description']} ({inst['architecture']['adopted_tier']} tier)",
        "conformance": {
            "disruption_occasioned_satisfied": "SMS (3.1): the disruption-occasioned invariant satisfied for this process",
            "particular_to_general_satisfied": "SMS (3.2): the particular-to-general relating invariant satisfied for this process",
            "action_entangled_satisfied": "SMS (3.3): the action-entangled invariant satisfied for this process",
            "sufficiency_oriented_satisfied": "SMS (3.4): the sufficiency-oriented invariant satisfied for this process",
            "temporally_structured_satisfied": "SMS (3.5): the temporally-structured invariant satisfied for this process",
        },
    },
}


def gen_cmd(name):
    """Resolve a LinkML gen-* command, preferring the toolchain venv over PATH."""
    p = VENV_BIN / name
    if p.exists():
        return str(p)
    w = shutil.which(name)
    if w:
        return w
    sys.exit(f"missing generator '{name}'; set up the venv (see requirements.txt)")


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def linkml_gen(std, src, dist):
    """LinkML owns the schema and semantic tier: one model, many formats."""
    dist.mkdir(parents=True, exist_ok=True)
    outs = {
        "gen-json-schema": f"{std}.schema.raw.json",
        "gen-graphql": f"{std}.graphql",
        "gen-jsonld-context": f"{std}.jsonld",
        "gen-shacl": f"{std}.shacl.ttl",
        "gen-owl": f"{std}.owl.ttl",
    }
    for gen, name in outs.items():
        (dist / name).write_text(run([gen_cmd(gen), str(src)]).stdout)
    print(f"  LinkML: generated {len(outs)} formats")


def conventions_adapter(std, dist):
    """Adapter: pin the JSON Schema draft and the canonical $id (LinkML targets an older
    draft and does not set the $id), and close the top-level object. LinkML leaves the root
    open even though the tree-root class is closed, which would let stray fields slip past
    at the top level."""
    raw = dist / f"{std}.schema.raw.json"
    schema = json.loads(raw.read_text())
    schema["$schema"] = DRAFT
    schema["$id"] = f"{SID_BASE}/{std}/{std}.schema.json"
    schema["additionalProperties"] = False
    (dist / f"{std}.schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    raw.unlink()
    print("  conventions adapter: draft pinned to 2020-12, $id set, top-level closed")


def _zod(node):
    """Recursive JSON Schema -> Zod. Small and controlled, so the Zod output does not depend
    on a shifting npm converter. Covers the constructs LinkML emits: objects, arrays, enums,
    strings with patterns, integers with minimums, booleans, and nullability."""
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


def zod_adapter(std, dist, root_class):
    """Adapter: dereference ($defs inlined) then emit Zod with the controlled converter."""
    import jsonref
    schema = json.loads((dist / f"{std}.schema.json").read_text())
    schema.pop("$id", None); schema.pop("$schema", None)  # else jsonref resolves refs against $id
    deref = dict(jsonref.replace_refs(schema, proxies=False, lazy_load=False))
    deref.pop("$defs", None)
    body = _zod(deref)
    ts = ('import { z } from "zod";\n\n'
          f"// Generated from {std}.schema.json. Do not edit by hand; run generate.py.\n"
          f"export const {root_class} = " + body + ";\n\n"
          f"export type {root_class} = z.infer<typeof {root_class}>;\n")
    (dist / f"{std}.zod.ts").write_text(ts)
    print(f"  Zod adapter: dist/{std}.zod.ts (controlled converter)")


def attestation_adapter(std, dist, examples, cfg):
    """Adapter: project a conformance declaration to an in-toto attestation (VSA-shaped,
    per-obligation, no total) and a SARIF run, from the conformant example."""
    import yaml
    inst = yaml.safe_load((examples / "conformant.yaml").read_text())
    conf = inst["conformance"]
    Q = cfg["conformance"]
    subject = cfg["subject"](inst)
    vsa = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [{"name": subject, "digest": {"sha256": "<sha256 of the consent record>"}}],
        "predicateType": f"{SID_BASE}/{std}/conformance/v{cfg['version']}",
        "predicate": {"verifier": f"{std}-conformance", "obligations": conf},  # no total field
    }
    (dist / "conformance.verdict.intoto.json").write_text(json.dumps(vsa, indent=2) + "\n")
    level = {"satisfied": "none", "declared_absent_with_justification": "note", "not_applicable": "none"}
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": f"{std}-conformance", "version": cfg["version"],
                                "rules": [{"id": k, "shortDescription": {"text": v}} for k, v in Q.items()]}},
            "results": [{"ruleId": k, "level": level.get(conf[k], "warning"),
                         "message": {"text": f"{Q[k]}: {conf[k]}"}} for k in Q],
        }],
    }
    (dist / "conformance.sarif").write_text(json.dumps(sarif, indent=2) + "\n")
    print("  attestation adapter: in-toto verdict (no total) + SARIF")


def main(argv):
    if len(argv) != 2 or argv[1] not in CONFIG:
        sys.exit(f"usage: python generate.py <standard-id>   (known: {', '.join(CONFIG)})")
    std = argv[1]
    cfg = CONFIG[std]
    base = ROOT / std
    src = base / "src" / f"{std}.linkml.yaml"
    dist = base / "dist"
    examples = base / "examples"
    if not src.exists():
        sys.exit(f"missing source model: {src}")
    print(f"generating {std} from {src.relative_to(ROOT)}")
    linkml_gen(std, src, dist)
    conventions_adapter(std, dist)
    zod_adapter(std, dist, cfg["root_class"])
    if (examples / "conformant.yaml").exists():
        attestation_adapter(std, dist, examples, cfg)
    else:
        print("  (no examples/conformant.yaml; skipped the verdict adapter)")
    print(f"done. artifacts in {std}/dist/")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
