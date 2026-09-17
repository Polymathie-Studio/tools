#!/usr/bin/env python3
"""
validate.py -- structural validation of the Frame Language term registry against its schema.

Zero external dependencies (jsonschema is not vendored in this repo). Checks the load-bearing
structure the term-registry.schema.json declares: required top-level and per-term fields, the
frame enum, the sources enum, the common_phrasings shape, and that term ids are unique. It is a
guard against a malformed registry reaching the published catalog, not a full JSON Schema engine.

Run: python3 machine-readable/frame-language/validate.py   (from the tools repo root)
Exit codes: 0 clean, 1 findings.
"""

import json
import sys
from pathlib import Path

MR_DIR = Path(__file__).resolve().parent
REGISTRY = MR_DIR / "src" / "term-registry.json"

REQUIRED_TOP = ["version", "date", "terms"]
REQUIRED_TERM = ["term", "frame", "imports", "frame_2_replacement", "strengthened_form", "procedure", "sources"]
FRAME_ENUM = {1, 2, 3}
SOURCE_ENUM = {"grammar", "mcp", "analyzer"}

findings = []


def fail(msg):
    findings.append(msg)


def is_str_list(v):
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def main():
    if not REGISTRY.exists():
        sys.exit(f"no registry at {REGISTRY}")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    for k in REQUIRED_TOP:
        if k not in data:
            fail(f"missing top-level field: {k}")
    terms = data.get("terms", [])
    if not isinstance(terms, list) or not terms:
        fail("terms must be a non-empty array")
        terms = []

    seen = set()
    for i, t in enumerate(terms):
        where = t.get("term", f"index {i}")
        for k in REQUIRED_TERM:
            if k not in t:
                fail(f"[{where}] missing required field: {k}")
        if t.get("term") in seen:
            fail(f"[{where}] duplicate term")
        seen.add(t.get("term"))
        if t.get("frame") not in FRAME_ENUM:
            fail(f"[{where}] frame must be one of {sorted(FRAME_ENUM)}, got {t.get('frame')!r}")
        if not is_str_list(t.get("frame_2_replacement", [])):
            fail(f"[{where}] frame_2_replacement must be an array of strings")
        if not is_str_list(t.get("primitive_anchors", [])):
            fail(f"[{where}] primitive_anchors must be an array of strings")
        srcs = t.get("sources", [])
        if not is_str_list(srcs) or not srcs or not set(srcs) <= SOURCE_ENUM:
            fail(f"[{where}] sources must be a non-empty array drawn from {sorted(SOURCE_ENUM)}")
        for cp in t.get("common_phrasings", []):
            if not (isinstance(cp, dict) and isinstance(cp.get("frame_1"), str) and isinstance(cp.get("frame_2"), str)):
                fail(f"[{where}] each common_phrasing needs string frame_1 and frame_2")

    if findings:
        print(f"{len(findings)} finding(s):")
        for f in findings:
            print(f"  - {f}")
        return 1
    print(f"registry valid: {len(terms)} terms, all required fields present, enums and shapes clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
