#!/usr/bin/env python3
"""Enforce a CSIS standard's structural obligations: its conformant example must validate
against <id>/dist/<id>.schema.json and every non-conformant fixture must fail. Run against
the GENERATED JSON Schema with a standard 2020-12 validator (not LinkML's own), which is
where the conditional obligations are actually enforced. Exit 0 if all pass, 1 otherwise.

Run: python validate-fixtures.py <standard-id>     e.g.  python validate-fixtures.py scls
"""
import json, sys
from pathlib import Path
import yaml, jsonschema

ROOT = Path(__file__).resolve().parent


def main(argv):
    if len(argv) != 2:
        sys.exit("usage: python validate-fixtures.py <standard-id>")
    std = argv[1]
    base = ROOT / std
    schema_path = base / "dist" / f"{std}.schema.json"
    examples = base / "examples"
    if not schema_path.exists():
        sys.exit(f"missing generated schema: {schema_path} (run generate.py {std} first)")
    schema = json.loads(schema_path.read_text())
    ok = True

    def must_pass(p):
        nonlocal ok
        try:
            jsonschema.validate(yaml.safe_load(p.read_text()), schema)
            print(f"  PASS (valid): {p.name}")
        except jsonschema.ValidationError as e:
            ok = False
            print(f"  FAIL (should be valid): {p.name} -> {e.message[:70]}")

    def must_fail(p):
        nonlocal ok
        try:
            jsonschema.validate(yaml.safe_load(p.read_text()), schema)
            ok = False
            print(f"  FAIL (should be invalid): {p.name} validated")
        except jsonschema.ValidationError as e:
            print(f"  PASS (correctly rejected): {p.name} -> {e.message[:55]}")

    conformant = examples / "conformant.yaml"
    if conformant.exists():
        must_pass(conformant)
    for f in sorted(examples.glob("nonconformant-*.yaml")):
        must_fail(f)
    print(f"{std}: {'all fixtures OK' if ok else 'FIXTURE FAILURES'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
