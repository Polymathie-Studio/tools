#!/usr/bin/env python3
"""
generate-craft-manifest.py  (v0.1.0)

Generates the CRAFT family machine-readable manifest from canonical source, under
"derive, never duplicate." Zero external dependencies (standard library only).

The CRAFT family spans sibling repositories under the CrossWalkri organization and is
heterogeneous in how its members carry version and metadata. This generator reads each
member's authoritative version from the location the registry names (frontmatter or a
header line), and only cross-checks against the filename version for members whose
filename stem is NOT stable. It surfaces version inconsistencies (for example a
versioned filename that has fallen behind its frontmatter) as findings.

Inputs (read, never written):
  - machine-readable/craft-registry.json : the hand-maintained seed
  - the canonical standard documents in the sibling repos (../../<repo>/<file>)

Output (overwritten):
  - machine-readable/craft-manifest.json : validates against
    standards-family-manifest.schema.json

Run: python3 machine-readable/generate-craft-manifest.py   (from the tools repo root)
Exit codes: 0 clean, 1 findings.
"""

import json
import os
import re
import sys
from pathlib import Path

# This generator lives in the one machine-readable source at
# Polymathie-Studio/tools/machine-readable/craft/. The CRAFT prose standards stay in their own
# CrossWalkri repos; CRAFT_STANDARDS_ROOT points at the directory those repos are cloned under,
# each read as <root>/<repo>/<file>. Required, no default, so no local path is baked into this
# published repo; main() validates it.
MR_DIR = Path(__file__).resolve().parent
CODE_ROOT = Path(os.environ.get("CRAFT_STANDARDS_ROOT", ""))
REGISTRY = MR_DIR / "craft-registry.json"
OUT = MR_DIR / "craft-manifest.json"

# Published fetch-surface host: CRAFT schemas publish under the Polymathie one source at
# Polymathie-Studio/tools/schema/craft/<id>/, matching each schema's own $id. A member gets a
# machineReadable block only when its set has been generated (its dist schema exists).
SID_BASE = "https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/craft"

VERSION_IN_FILENAME = re.compile(r"(\d+)_(\d+)_(\d+)\.md$")
VERSION_IN_HEADER = re.compile(r"v(\d+\.\d+\.\d+)")
FRONTMATTER_VERSION = re.compile(r"^version:\s*(.+)$", re.MULTILINE)

warnings = []


def warn(msg):
    warnings.append(msg)


def frontmatter_version(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    block = text[3:end] if end != -1 else text[3:2000]
    m = FRONTMATTER_VERSION.search(block)
    return m.group(1).strip() if m else None


def header_version(text):
    m = VERSION_IN_HEADER.search(text[:1500])
    return m.group(1) if m else None


def filename_version(name):
    m = VERSION_IN_FILENAME.search(name)
    return ".".join(m.groups()) if m else None


def build_machine_readable(std_id):
    """Pointers to a standard's generated set on the one source, present only when the set has
    been generated (machine-readable/craft/<id>/dist/<id>.schema.json exists). The URLs are the
    Polymathie fetch host, matching the schema's own $id."""
    dist = MR_DIR / std_id / "dist" / f"{std_id}.schema.json"
    if not dist.exists():
        return None
    base = f"{SID_BASE}/{std_id}"
    return {
        "schema": f"{base}/{std_id}.schema.json",
        "zod": f"{base}/{std_id}.zod.ts",
        "jsonldContext": f"{base}/{std_id}.jsonld",
        "conformanceVerdict": f"{base}/conformance.verdict.intoto.json",
        "conformanceSarif": f"{base}/conformance.sarif",
        "set": f"{base}/",
    }


def build_member(entry):
    if entry.get("status") == "planned":
        return {
            "id": entry["id"],
            "name": entry["name"],
            "kind": entry.get("kind", "standard"),
            "version": "unpublished",
            "status": "planned",
            "group": entry.get("role", "planned"),
            "canonicalSource": "https://github.com/CrossWalkri (in preparation)",
            "description": entry.get("description", ""),
        }

    path = CODE_ROOT / entry["repo"] / entry["file"]
    if not path.exists():
        warn(f"NO FILE for {entry['id']}: {path} (is the {entry['repo']} repo cloned as a sibling under {CODE_ROOT}?)")
        return None
    text = path.read_text(encoding="utf-8")

    if entry["versionSource"] == "frontmatter":
        version = frontmatter_version(text)
        src = "frontmatter"
    else:
        version = header_version(text)
        src = "header"
    if not version:
        warn(f"NO VERSION for {entry['id']}: could not read version from {src} of {entry['file']}")
        version = "unknown"

    # Cross-check the filename version only when the stem is not stable.
    if not entry.get("stableStem", False):
        fv = filename_version(entry["file"])
        if fv and fv != version:
            warn(f"VERSION DRIFT for {entry['id']}: filename {fv} lags authoritative {src} version {version} (bump the filename or the {src})")

    member = {
        "id": entry["id"],
        "name": entry["name"],
        "kind": entry.get("kind", "standard"),
        "version": version,
        "status": entry.get("status", "published"),
        "group": entry.get("role", "standard"),
        "canonicalSource": f"{entry['repo']}/{entry['file']}",
        "license": entry.get("license"),
        "description": entry.get("description", ""),
    }
    mr = build_machine_readable(entry["id"])
    if mr:
        member["machineReadable"] = mr
    if "cluster" in entry:
        member["note"] = entry["cluster"]
        warn(f"CLUSTER for {entry['id']}: canonical-document choice undetermined (see note); provisional pointer used")
    return member


def main():
    if not os.environ.get("CRAFT_STANDARDS_ROOT") or not CODE_ROOT.is_dir():
        sys.exit("set CRAFT_STANDARDS_ROOT to the directory the CrossWalkri standard repos are "
                 "cloned under (each read as <root>/<repo>/<file>); it lives outside this repo and "
                 "has no default here")
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    fam = reg["family"]
    members = [m for m in (build_member(e) for e in reg["members"]) if m]

    manifest = {
        "$schema": "./standards-family-manifest.schema.json",
        "$comment": "GENERATED by machine-readable/generate-craft-manifest.py from craft-registry.json plus versions read from each member's canonical source. Do not edit by hand; edit the registry or the sources and regenerate.",
        "name": fam["name"],
        "publisher": fam["publisher"],
        "author": fam["author"],
        "version": reg.get("manifestVersion", "0.1.0"),
        "license": fam["license"],
        "description": fam.get("description", ""),
        "homepage": fam.get("homepage"),
        "site": fam.get("site"),
        "canonicalSourceRepo": fam.get("canonicalSourceOrg"),
        "generatedBy": "machine-readable/craft/generate-craft-manifest.py",
        "conformance": {"report": None, "schema": None, "baseline": []},
        "agentInstruction": None,
        "domain": {
            "organization": "CrossWalkri",
            "roles": ["meta", "input", "exit", "reporting", "instrumentation", "primitives"],
            "note": "The family spans sibling repositories; members are heterogeneous in version source (frontmatter or header) and filename-stem stability. See craft-registry.json.",
        },
        "members": members,
    }
    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    published = [m for m in members if m["status"] == "published"]
    print(f"members: {len(members)} ({len(published)} published, {len(members) - len(published)} planned)")
    print(f"wrote: {OUT.name}")
    if warnings:
        print(f"\n{len(warnings)} finding(s):")
        for w in warnings:
            print(f"  - {w}")
        return 1
    print("\nno findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
