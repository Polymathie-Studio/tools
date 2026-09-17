#!/usr/bin/env python3
"""
verify-drift.py -- check that what is published to the Polymathie host matches the local
generated dist for every CSIS standard, and that the family manifest matches too.

This is the drift gate for the publishing obligation: a source edit that was regenerated but
not re-published, or a published file that was hand-touched, shows up here as DRIFT. It compares
the local `<id>/dist/` against the published `schema/csis/<id>/` in the tools-repo clone, and the
local `csis-manifest.json` against `schema/csis/csis-manifest.json`. It does NOT regenerate
(that needs the LinkML venv); run `generate.py <id>` first, then this, to catch source-vs-dist
drift as well. Zero external dependencies (standard library only).

Run:  python3 verify-drift.py            (check every standard with a dist, plus the manifest)
      python3 verify-drift.py <id> ...   (check only the named standards)

Exit codes: 0 everything in sync, 1 drift or unpublished files found.
Set POLYMATHIE_TOOLS to the tools-repo clone path (default ~/code/polymathie-studio-tools).
"""
import filecmp
import os
import sys
from pathlib import Path

MR_DIR = Path(__file__).resolve().parent
TOOLS_REPO = Path(os.environ.get("POLYMATHIE_TOOLS", Path.home() / "code" / "polymathie-studio-tools"))
FAMILY = "craft"
MANIFEST = MR_DIR / "craft-manifest.json"


def check_pair(local: Path, published: Path, label: str, findings: list):
    if not published.exists():
        findings.append(f"UNPUBLISHED  {label}: {published} does not exist on the host clone")
    elif not filecmp.cmp(local, published, shallow=False):
        findings.append(f"DRIFT        {label}: local dist differs from published")


def main(argv):
    published_root = TOOLS_REPO / "schema" / FAMILY
    if not (TOOLS_REPO / ".git").exists():
        sys.exit(f"tools repo clone not found at {TOOLS_REPO}; set POLYMATHIE_TOOLS to its path")

    ids = argv[1:]
    if not ids:
        ids = sorted(d.name for d in MR_DIR.iterdir()
                     if d.is_dir() and (d / "dist").is_dir())

    findings, checked = [], 0
    for std in ids:
        dist = MR_DIR / std / "dist"
        if not dist.is_dir():
            findings.append(f"NO DIST      {std}: no local dist (run generate.py {std})")
            continue
        for f in sorted(dist.iterdir()):
            if f.is_file():
                check_pair(f, published_root / std / f.name, f"{std}/{f.name}", findings)
                checked += 1

    # the family manifest, the discovery entry point
    if MANIFEST.exists():
        check_pair(MANIFEST, published_root / MANIFEST.name, MANIFEST.name, findings)
        checked += 1

    if findings:
        print(f"drift check: {len(findings)} finding(s) across {checked} published file(s)")
        for line in findings:
            print("  " + line)
        return 1
    print(f"drift check: clean, {checked} published file(s) match local for {len(ids)} standard(s) plus the manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
