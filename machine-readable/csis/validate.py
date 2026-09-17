#!/usr/bin/env python3
"""
validate.py  (v0.1.0)

Zero-dependency validator for a standards family manifest against
standards-family-manifest.schema.json. Standard library only, matching the
family's zero-dependency identity. This is a targeted contract check of the
manifest, not a full JSON Schema engine: it reads the required fields, the
member required fields, and the status enum from the schema itself, so it stays
in sync with the schema without hardcoding the contract.

Run: python3 standards/machine-readable/validate.py [manifest.json]
     (defaults to csis-manifest.json in this directory)

Exit codes: 0 valid, 1 invalid.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "standards-family-manifest.schema.json"


def validate(data, schema):
    """Return a list of human-readable error strings (empty means valid)."""
    errors = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]

    for key in schema.get("required", []):
        if key not in data:
            errors.append(f"missing required top-level field: {key}")

    members = data.get("members")
    if not isinstance(members, list):
        errors.append("'members' is missing or not an array")
        return errors

    mdef = schema["$defs"]["member"]
    mreq = mdef.get("required", [])
    status_enum = mdef["properties"]["status"].get("enum")
    seen_ids = set()
    for i, m in enumerate(members):
        where = f"members[{i}]" + (f" (id={m.get('id')})" if isinstance(m, dict) else "")
        if not isinstance(m, dict):
            errors.append(f"{where}: not an object")
            continue
        for key in mreq:
            if key not in m:
                errors.append(f"{where}: missing required field: {key}")
        if status_enum and m.get("status") not in status_enum:
            errors.append(f"{where}: status '{m.get('status')}' not in {status_enum}")
        mid = m.get("id")
        if mid in seen_ids:
            errors.append(f"{where}: duplicate id '{mid}'")
        seen_ids.add(mid)
        if "canonicalSource" in m and not isinstance(m["canonicalSource"], str):
            errors.append(f"{where}: canonicalSource is not a string")
    return errors


def main():
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "csis-manifest.json"
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = validate(data, schema)
    if errors:
        print(f"INVALID: {manifest_path.name} ({len(errors)} error(s))")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"VALID: {manifest_path.name} ({len(data['members'])} members) conforms to {SCHEMA.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
