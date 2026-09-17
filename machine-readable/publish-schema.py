#!/usr/bin/env python3
"""
publish-schema.py -- publish a CSIS standard's generated set to the Polymathie fetch host.

Copies machine-readable/<id>/dist/ into the Polymathie-Studio/tools clone under
schema/csis/<id>/, refreshes the shared base schema at schema/, commits, and pushes. This
is the cross-org publish step of the family's regenerate obligation: the sources stay
federated in this layer, the schemas centralize at the one host, and running this after
generate.py keeps the published schema from drifting from its source.

Run: python publish-schema.py <standard-id>     e.g.  python publish-schema.py scls
Requires a local clone of Polymathie-Studio/tools with push access. Default location
~/code/polymathie-studio-tools; override with the POLYMATHIE_TOOLS environment variable.
Zero external dependencies (standard library only).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

MR_DIR = Path(__file__).resolve().parent
BASE_SCHEMA = MR_DIR / "standards-family-manifest.schema.json"
MANIFEST = MR_DIR / "csis-manifest.json"
TOOLS_REPO = Path(os.environ.get("POLYMATHIE_TOOLS", Path.home() / "code" / "polymathie-studio-tools"))
FAMILY = "csis"


def git(args):
    return subprocess.run(["git", *args], cwd=TOOLS_REPO, check=True, capture_output=True, text=True)


def main(argv):
    if len(argv) != 2:
        sys.exit("usage: python publish-schema.py <standard-id | manifest>")
    std = argv[1]
    if not (TOOLS_REPO / ".git").exists():
        sys.exit(f"tools repo clone not found at {TOOLS_REPO}; clone Polymathie-Studio/tools "
                 f"there, or set POLYMATHIE_TOOLS to its path")

    git(["pull", "--ff-only", "-q"])  # take others' pushes before adding ours

    schema_dir = TOOLS_REPO / "schema"
    schema_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BASE_SCHEMA, schema_dir / BASE_SCHEMA.name)  # shared base, refreshed

    if std == "manifest":
        # the family manifest is the discovery entry point; publish it alongside the schemas
        if not MANIFEST.exists():
            sys.exit(f"no manifest at {MANIFEST} (run generate-csis-manifest.py first)")
        (schema_dir / FAMILY).mkdir(parents=True, exist_ok=True)
        shutil.copy2(MANIFEST, schema_dir / FAMILY / MANIFEST.name)
        label = f"{FAMILY} manifest"
        where = f"schema/{FAMILY}/{MANIFEST.name}"
    else:
        dist = MR_DIR / std / "dist"
        if not (dist / f"{std}.schema.json").exists():
            sys.exit(f"no generated set at {dist} (run generate.py {std} first)")
        dest = schema_dir / FAMILY / std
        dest.mkdir(parents=True, exist_ok=True)
        for f in sorted(dist.iterdir()):
            if f.is_file():
                shutil.copy2(f, dest / f.name)
        label = f"{FAMILY}/{std} schema set"
        where = f"schema/{FAMILY}/{std}/ ({sum(1 for _ in dest.iterdir())} files)"

    git(["add", "-A"])
    if not git(["status", "--porcelain"]).stdout.strip():
        print(f"{label}: already up to date, nothing to publish")
        return 0
    git(["-c", "user.name=Regis Chapman", "-c", "user.email=durgadas@mac.com",
         "commit", "-q", "-m", f"Publish {label}"])
    git(["push", "-q"])
    print(f"published {label} to {TOOLS_REPO.name} ({where})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
