#!/usr/bin/env python3
"""
generate-frame-language-manifest.py  (v0.1.0)

Generates the Frame Language family machine-readable manifest from canonical source, under
"derive, never duplicate." Zero external dependencies (standard library only).

Frame Language's machine-readable layer is a code-system: a controlled vocabulary published as
data plus its schema, vendored into the one source at machine-readable/frame-language/src/. This
is the same shape GRAIN uses under CRAFT, not the register-and-model shape the CSIS standards use.
The generator reads each code-system member's version from the vendored catalog's own version
field, emits the family manifest, and publishes the catalog, its schema, and the manifest into the
one source's schema/frame-language/ directory (a within-repo copy, since sources and schemas now
colocate in one repo).

Inputs (read, never written):
  - machine-readable/frame-language/frame-language-registry.json : the family seed
  - the vendored catalog and schema the seed's members name (src/...)

Outputs (overwritten):
  - machine-readable/frame-language/frame-language-manifest.json : validates against
    standards-family-manifest.schema.json
  - schema/frame-language/frame-language-manifest.json, term-registry.json, term-registry.schema.json

Run: python3 machine-readable/frame-language/generate-frame-language-manifest.py  (from the tools repo root)
Exit codes: 0 clean, 1 findings.
"""

import json
import shutil
import sys
from pathlib import Path

MR_DIR = Path(__file__).resolve().parent
REGISTRY = MR_DIR / "frame-language-registry.json"
OUT = MR_DIR / "frame-language-manifest.json"
# The one source colocates sources and schemas; publish is a within-repo copy. tools repo root is
# two levels up from machine-readable/frame-language/.
TOOLS_ROOT = MR_DIR.parent.parent
SCHEMA_DIR = TOOLS_ROOT / "schema" / "frame-language"
BASE_SCHEMA = TOOLS_ROOT / "schema" / "standards-family-manifest.schema.json"
# Published fetch-surface host, matching each schema's own $id.
SID_BASE = "https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/frame-language"

warnings = []


def warn(msg):
    warnings.append(msg)


def build_code_system_member(entry):
    """A code-system member: a controlled vocabulary published as data plus its schema, vendored
    into the one source. Version is read from the vendored catalog's own version field. The
    machineReadable block points at the published catalog and its schema."""
    catalog = MR_DIR / entry["catalogFile"]
    version = "unknown"
    if catalog.exists():
        try:
            version = json.loads(catalog.read_text(encoding="utf-8")).get("version", "unknown")
        except json.JSONDecodeError:
            warn(f"BAD CATALOG for {entry['id']}: {entry['catalogFile']} is not valid JSON")
    else:
        warn(f"NO CATALOG for {entry['id']}: {entry['catalogFile']} not found")

    catalog_name = Path(entry["catalogFile"]).name
    schema_name = Path(entry["schemaFile"]).name
    member = {
        "id": entry["id"],
        "name": entry["name"],
        "kind": entry.get("kind", "code-system"),
        "version": version,
        "status": entry.get("status", "published"),
        "group": entry.get("role", "vocabulary"),
        "canonicalSource": f"machine-readable/frame-language/{entry['catalogFile']}",
        "license": entry.get("license"),
        "description": entry.get("description", ""),
        "machineReadable": {
            "kind": "code-system",
            "catalog": f"{SID_BASE}/{catalog_name}",
            "schema": f"{SID_BASE}/{schema_name}",
            "set": f"{SID_BASE}/",
        },
    }
    return member


def build_member(entry):
    if entry.get("mrKind") == "code-system":
        return build_code_system_member(entry)
    warn(f"UNKNOWN member kind for {entry['id']}: only code-system members are handled in this family's establishment")
    return None


def publish(manifest):
    """Publish the catalog, its schema, and the manifest into schema/frame-language/, and refresh
    the shared base schema. A within-repo copy; commit and push are done outside this script."""
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    for entry in json.loads(REGISTRY.read_text(encoding="utf-8"))["members"]:
        if entry.get("mrKind") == "code-system":
            for f in (entry["catalogFile"], entry["schemaFile"]):
                src = MR_DIR / f
                if src.exists():
                    shutil.copy2(src, SCHEMA_DIR / Path(f).name)
                else:
                    warn(f"PUBLISH SKIP: {f} missing, not copied to schema/frame-language/")
    (SCHEMA_DIR / OUT.name).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    fam = reg["family"]
    members = [m for m in (build_member(e) for e in reg["members"]) if m]

    manifest = {
        "$schema": "../../schema/standards-family-manifest.schema.json",
        "$comment": "GENERATED by machine-readable/frame-language/generate-frame-language-manifest.py from frame-language-registry.json plus the version read from each code-system catalog. Do not edit by hand; edit the registry or the vendored sources and regenerate.",
        "name": fam["name"],
        "publisher": fam["publisher"],
        "author": fam["author"],
        "version": reg.get("manifestVersion", "0.1.0"),
        "license": fam["license"],
        "description": fam.get("description", ""),
        "homepage": fam.get("homepage"),
        "site": fam.get("site"),
        "canonicalSourceRepo": fam.get("canonicalSourceRepo"),
        "generatedBy": "machine-readable/frame-language/generate-frame-language-manifest.py",
        "conformance": {"report": None, "schema": None, "baseline": []},
        "agentInstruction": None,
        "domain": {
            "kind": "code-system",
            "readSurface": "language",
            "note": "Frame Language reads the stance a term speaks from in actual vocabulary and construction; its machine-readable layer is the Frame 1 vocabulary registry, the one source the skill, MCP server, and analyzer derive from. The prose standards (Dimensional Frame Language, the Frame Language Grammar, the Foundational Vocabulary Specification) are added as members once their public canonical locations are confirmed. Rewiring the live surfaces to fetch from this registry is a gated follow-up, not part of this establishment.",
        },
        "members": members,
    }
    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    publish(manifest)

    published = [m for m in members if m["status"] == "published"]
    print(f"members: {len(members)} ({len(published)} published)")
    print(f"wrote: {OUT.name}")
    print(f"published to: schema/frame-language/ (manifest + catalog + schema)")
    if warnings:
        print(f"\n{len(warnings)} finding(s):")
        for w in warnings:
            print(f"  - {w}")
        return 1
    print("\nno findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
