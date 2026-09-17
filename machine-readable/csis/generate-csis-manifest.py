#!/usr/bin/env python3
"""
generate-csis-manifest.py  (v0.4.0)

Generates the Coordination Structural Integrity Suite machine-readable layer from
canonical source, under "derive, never duplicate." Zero external dependencies
(standard library only), matching the family's zero-dependency identity.

Inputs (all read, never written):
  - standards/machine-readable/csis-registry.json : the single hand-maintained seed
    (id, family group, canonical name, description) that the published standards do
    not carry. Version-free by design.
  - standards/standards-3_0-*.md and the two supporting specs : stable-stem, so the
    filename is a frozen series stem used to locate the file. The authoritative version
    is read from the PUBLISHED standard (raw.githubusercontent) so an unpublished local
    edit cannot advance the generated registry ahead of what is published; on a fetch
    failure it falls back to the local "Version X.Y.Z" header (or frontmatter) with a
    warning.

Changelog:
  v0.4.0 : emit per-member companions (the skill and prompts, discovered by convention
    at claude-skills/claude-skill-<slug>-*.md and prompts/<slug>/, plus any named
    companion documents from the registry) and relatedStandards (the register's
    cross_standard_ref entries, surfaced for discovery), closing the companion-and-
    relationship discovery gap. Slug derives from the file stem, with a registry `slug`
    override for the standards whose companion naming differs (asep, fbcs, flfvs, ctps).
  v0.3.0 : emit a per-member machineReadable block (pointers to the standard's own
    generated set at the Polymathie fetch host) whenever machine-readable/<id>/dist/
    exists, so a standard's fetch surface wires itself into the manifest and a consumer
    is told the set exists and where it lives. SCLS is the first with one.
  v0.2.0 : version read from published source (raw.githubusercontent) with local
    fallback, closing the leak where a vault-local edit ahead of publication would
    generate a registry version ahead of the published standard.
  v0.1.0 : initial generator (registry + local header versions -> manifest + standards.ts).
  - standards/standards-candidates/**/*.md : candidates are read from their own
    frontmatter (any .md carrying a version, excluding candidate-companion, skills,
    and READMEs).

Outputs (overwritten):
  - standards/machine-readable/csis-manifest.json : the family manifest, validating
    against standards-family-manifest.schema.json.
  - standards/machine-readable/standards.generated.ts : the MCP standards.ts,
    generated from the same registry, so there is one source and no drift between them.

Exit codes: 0 clean, 1 drift or missing-file findings.

Run: python3 standards/tools/generate-csis-manifest.py
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

# The machine-readable layer is this file's own directory (the single source: it lives in
# Polymathie-Studio/tools/machine-readable/ beside the per-standard sources and generate.py).
MR_DIR = Path(__file__).resolve().parent
# The suite's prose standards, candidates, skills, and prompts are NOT part of the
# machine-readable layer; they stay in the suite working tree, and the generator reads them
# (for the local version fallback, the name check, canonicalSource, candidates, and
# companions) via STANDARDS_ROOT, which points at that tree's standards/ directory. It is
# required and has no default, so no local path is baked into this published repo; main()
# validates it before use.
STANDARDS_DIR = Path(os.environ.get("STANDARDS_ROOT", ""))
CANDIDATES_DIR = STANDARDS_DIR / "standards-candidates"
SKILLS_DIR = STANDARDS_DIR / "claude-skills"
PROMPTS_DIR = STANDARDS_DIR / "prompts"
REGISTRY = MR_DIR / "csis-registry.json"
OUT_MANIFEST = MR_DIR / "csis-manifest.json"
OUT_TS = MR_DIR / "standards.generated.ts"

# Published-source base. The authoritative version is read from the published
# standard, not the vault-local copy, so an unpublished local edit cannot advance the
# generated registry ahead of what is published. Falls back to local on fetch failure.
RAW_BASE = "https://raw.githubusercontent.com/coordination-structural-integrity-suite/suite/main/"

# Published fetch-surface host: per-standard machine-readable sets publish under the
# Polymathie parent brand at Polymathie-Studio/tools/schema (settled 2026-09-16; interim
# host, a larger reorg is deferred). A member gets a machineReadable block only when its
# set has been generated locally, pointing at this host to match the schema's own $id.
SID_BASE = "https://raw.githubusercontent.com/Polymathie-Studio/tools/main/schema/csis"

VERSION_IN_FILENAME = re.compile(r"(\d+)_(\d+)_(\d+)\.md$")
# The authoritative header stamp, in any of its forms: "Version 2.4.3 | June 2026",
# "**Version:** v0.3.25", "**Version:** 0.3.7". Requires the word Version, so it does
# not match a bare secondary "v0.7.12" stamp.
VERSION_IN_HEADER = re.compile(r"Version[:*\s]*v?(\d+\.\d+\.\d+)")
# The secondary "*Core Standard v0.7.12*" stamp some standards also carry; when it
# disagrees with the filename it is a stale secondary stamp, a real but lower finding.
SECONDARY_STAMP = re.compile(r"Core Standard\s+v(\d+\.\d+\.\d+)")
HYPHENS = re.compile("[" + "".join(chr(c) for c in (0x2010, 0x2011, 0x2012, 0x2013, 0x2014)) + "]")


def norm(s):
    """Normalize hyphen-like characters to a plain hyphen for comparison."""
    return HYPHENS.sub("-", s)
FRONTMATTER_FIELD = re.compile(r"^(version|title|type):\s*(.*)$", re.MULTILINE)
CANDIDATE_SUFFIX = re.compile(r"\s+-\s+Candidate.*$")

warnings = []


def warn(msg):
    warnings.append(msg)


def version_from_filename(name):
    m = VERSION_IN_FILENAME.search(name)
    return ".".join(m.groups()) if m else None


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fields = {}
    for key, val in FRONTMATTER_FIELD.findall(block):
        if key not in fields:  # first occurrence wins
            fields[key] = val.strip()
    return fields


def read_frontmatter_text(text):
    """Frontmatter fields from a document's raw text (parallel to read_frontmatter)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fields = {}
    for key, val in FRONTMATTER_FIELD.findall(text[3:end]):
        if key not in fields:
            fields[key] = val.strip()
    return fields


def extract_version(text, src):
    """The authoritative version from a document's text: frontmatter or header per src."""
    if src == "frontmatter":
        v = read_frontmatter_text(text).get("version")
    else:
        m = VERSION_IN_HEADER.search(text)
        v = m.group(1) if m else None
    return re.sub(r"^v", "", v.strip()) if v else None


def fetch_published_head(canonical_source):
    """First 2000 chars of the published standard, or None if it cannot be fetched."""
    try:
        with urllib.request.urlopen(RAW_BASE + canonical_source, timeout=15) as resp:
            return resp.read(2000).decode("utf-8", "replace")
    except Exception:
        return None


def build_machine_readable(std_id):
    """Pointers to a standard's own machine-readable set, present only when the set has
    been generated (machine-readable/<id>/dist/<id>.schema.json exists). The URLs are the
    Polymathie fetch host, matching the schema's own $id; publishing the dist to that host
    is the pending cross-org step, so the block records the set exists and where it lives."""
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


CROSS_REF = re.compile(r"^\s*cross_standard_ref:\s*(.+?)\s*$", re.MULTILINE)


def companion_slug(entry):
    """The slug for a standard's skill and prompts. An explicit `slug` in the registry wins
    (for standards whose file stem does not match the companion naming, e.g. asep is
    'adverse-signal'); otherwise derive it from the file stem."""
    if entry.get("slug"):
        return entry["slug"]
    stem = entry["fileStem"]
    if stem.startswith("standards-3_0-"):
        stem = stem[len("standards-3_0-"):]
    return stem.rstrip("-")


def build_companions(entry):
    """Pointers to a standard's interpretive companions, discovered by convention: the skill at
    claude-skills/claude-skill-<slug>-*.md and the prompts at prompts/<slug>/. A named
    companions list in the registry entry (guides, profiles, remediation specs) is merged in."""
    slug = companion_slug(entry)
    comp = {}
    skills = sorted(SKILLS_DIR.glob(f"claude-skill-{slug}-*.md"))
    if skills:
        comp["skill"] = "standards/claude-skills/" + skills[0].name
    if (PROMPTS_DIR / slug).is_dir():
        comp["prompts"] = f"standards/prompts/{slug}/"
    if entry.get("companions"):
        comp["documents"] = entry["companions"]
    return comp or None


def build_related_standards(std_id):
    """The cross-standard references a standard's register carries (its relationship structure),
    surfaced for discovery. Read from the register text without a YAML dependency."""
    reg = MR_DIR / std_id / "src" / f"{std_id}-register.yaml"
    if not reg.exists():
        return None
    refs = []
    for raw in CROSS_REF.findall(reg.read_text(encoding="utf-8")):
        v = raw.strip().strip('"').strip("'")
        if v and v not in refs:
            refs.append(v)
    return refs or None


def build_standard_member(entry):
    """One published-standard (or supporting-spec) member. Standards are stable-stem:
    the filename number is a frozen series stem used only to locate the file, and the
    authoritative version is read from the header Version line or the frontmatter, per
    the registry's versionSource (default header)."""
    matches = sorted(STANDARDS_DIR.glob(entry["fileStem"] + "*.md"))
    if not matches:
        warn(f"NO FILE for {entry['id']}: glob {entry['fileStem']}*.md matched nothing")
        return None
    if len(matches) > 1:
        warn(f"AMBIGUOUS for {entry['id']}: {[m.name for m in matches]}; using {matches[0].name}")
    path = matches[0]
    filename = path.name
    head = path.read_text(encoding="utf-8")[:2000]
    src = entry.get("versionSource", "header")
    canonical_source = entry["canonicalSourcePrefix"] + filename
    # Read the authoritative version from the PUBLISHED standard; fall back to the
    # local file if the fetch fails, warning that a local version may be ahead.
    published_head = fetch_published_head(canonical_source)
    if published_head is not None:
        version = extract_version(published_head, src)
    else:
        version = extract_version(head, src)
        warn(f"PUBLISHED FETCH FAILED for {entry['id']}: {canonical_source}; used the local version {version}, which may be ahead of published")
    if not version:
        version = version_from_filename(filename)
        warn(f"NO {src.upper()} VERSION for {entry['id']}: fell back to the frozen filename stem {version}, which may be stale; add an authoritative Version to the source")
    # The filename is a frozen series stem (stable-stem), so there is no
    # filename-versus-version drift to check. The secondary stamp still can drift.
    sm = SECONDARY_STAMP.search(head)
    if sm and sm.group(1) != version:
        warn(f"STALE SECONDARY STAMP for {entry['id']}: 'Core Standard v{sm.group(1)}' lags version {version}")
    # soft name check: the leading words of the canonical name, hyphen-normalized
    lead = " ".join(entry["name"].split()[:3])
    if norm(lead).lower() not in norm(head[:800]).lower():
        warn(f"NAME CHECK for {entry['id']}: '{lead}' not found near the top of {filename}")
    member = {
        "id": entry["id"],
        "name": entry["name"],
        "kind": entry["kind"],
        "version": version,
        "status": "published",
        "group": entry["group"],
        "canonicalSource": entry["canonicalSourcePrefix"] + filename,
        "description": entry["description"],
    }
    if "license" in entry:
        member["license"] = entry["license"]
    mr = build_machine_readable(entry["id"])
    if mr:
        member["machineReadable"] = mr
    comp = build_companions(entry)
    if comp:
        member["companions"] = comp
    rel = build_related_standards(entry["id"])
    if rel:
        member["relatedStandards"] = rel
    member["_filename"] = filename  # internal, stripped before emit
    return member


def is_candidate_doc(path, fm):
    if "version" not in fm:
        return False
    if fm.get("type") == "candidate-companion":
        return False
    if path.name.startswith("claude-skill") or path.name == "README.md":
        return False
    return True


def build_candidate_members():
    members = []
    for path in sorted(CANDIDATES_DIR.rglob("*.md")):
        fm = read_frontmatter(path)
        if not is_candidate_doc(path, fm):
            continue
        folder = path.parent.name
        cid = folder.lower()
        title = fm.get("title", folder)
        name = CANDIDATE_SUFFIX.sub("", title).strip()
        rel = "standards/" + str(path.relative_to(STANDARDS_DIR)).replace("\\", "/")
        members.append({
            "id": cid,
            "name": name,
            "kind": fm.get("type") or "standard-candidate",
            "version": fm["version"],
            "status": "candidate",
            "group": "candidate",
            "canonicalSource": rel,
            "description": "Candidate, not promoted, not a conformance gate.",
        })
    members.sort(key=lambda m: m["id"])
    return members


def emit_manifest(reg, std_members, cand_members):
    fam = reg["family"]
    members = [{k: v for k, v in m.items() if not k.startswith("_")}
               for m in std_members + cand_members]
    manifest = {
        "$schema": "./standards-family-manifest.schema.json",
        "$comment": "GENERATED by standards/tools/generate-csis-manifest.py from csis-registry.json plus versions parsed from the standards and candidate frontmatter. Do not edit by hand; edit the registry or the source documents and regenerate.",
        "name": fam["name"],
        "publisher": fam["publisher"],
        "author": fam["author"],
        "version": reg.get("manifestVersion", "0.1.0"),
        "license": fam["license"],
        "description": fam.get("description", ""),
        "homepage": fam.get("homepage"),
        "site": fam.get("site"),
        "canonicalSourceRepo": fam["canonicalSourceRepo"],
        "generatedBy": "standards/tools/generate-csis-manifest.py",
        "conformance": {
            "report": None,
            "schema": None,
            "baseline": [
                "Each member points at canonical source; prose is not reproduced (substrate discipline)",
                "Version parsed from the source matches the filename and header",
                "Candidate members carry candidate status and are excluded from conformance gating",
            ],
        },
        "agentInstruction": None,
        "domain": {
            "families": ["compressive", "generative"],
            "metaStandard": fam.get("metaStandard"),
            "substrateDiscipline": "The manifest is a descriptor that points at canonical source and carries conformance; it does not serve standard prose in place of source.",
        },
        "members": members,
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def emit_standards_ts(reg, std_members):
    """Regenerate the MCP standards.ts from the same registry (the ten standards only)."""
    ten = [m for m in std_members if m["group"] in ("compressive", "generative")]
    lines = []
    lines.append("/**")
    lines.append(" * The ten standards of the Coordination Structural Integrity Suite.")
    lines.append(" *")
    lines.append(" * GENERATED from standards/machine-readable/csis-registry.json by")
    lines.append(" * standards/tools/generate-csis-manifest.py. Do not edit by hand; edit the")
    lines.append(" * registry and regenerate. Full standard text is NOT embedded (substrate")
    lines.append(" * discipline); this carries pointers and metadata only.")
    lines.append(" */")
    lines.append("")
    lines.append("export type StandardFamily = 'compressive' | 'generative'")
    lines.append("")
    lines.append("export interface CsisStandard {")
    lines.append("  name: string")
    lines.append("  id: string")
    lines.append("  family: StandardFamily")
    lines.append("  version: string")
    lines.append("  githubPath: string")
    lines.append("  description: string")
    lines.append("}")
    lines.append("")
    lines.append("export const STANDARDS: readonly CsisStandard[] = [")
    for m in ten:
        github_path = None
        # canonicalSource already is prefix + filename for the published repo layout
        github_path = m["canonicalSource"]
        lines.append("  {")
        lines.append(f"    name: {json.dumps(m['name'])},")
        lines.append(f"    id: {json.dumps(m['id'])},")
        lines.append(f"    family: {json.dumps(m['group'])},")
        lines.append(f"    version: {json.dumps(m['version'])},")
        lines.append(f"    githubPath: {json.dumps(github_path)},")
        lines.append(f"    description: {json.dumps(m['description'])},")
        lines.append("  },")
    lines.append("] as const")
    lines.append("")
    lines.append("export function getStandardById(id: string): CsisStandard | undefined {")
    lines.append("  return STANDARDS.find((s) => s.id === id)")
    lines.append("}")
    lines.append("")
    lines.append("export function getStandardsByFamily(family: StandardFamily): CsisStandard[] {")
    lines.append("  return STANDARDS.filter((s) => s.family === family)")
    lines.append("}")
    lines.append("")
    lines.append("export function getStandardGithubUrl(standard: CsisStandard): string {")
    lines.append("  return `https://github.com/coordination-structural-integrity-suite/suite/blob/main/${standard.githubPath}`")
    lines.append("}")
    OUT_TS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if not os.environ.get("STANDARDS_ROOT") or not STANDARDS_DIR.is_dir():
        sys.exit("set STANDARDS_ROOT to the suite's standards/ directory (the prose standards, "
                 "candidates, claude-skills, and prompts the manifest reads); it lives in the suite "
                 "working tree, outside this repo, and has no default here")
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    std_members = [m for m in (build_standard_member(e) for e in reg["standards"]) if m]
    cand_members = build_candidate_members()
    emit_manifest(reg, std_members, cand_members)
    emit_standards_ts(reg, std_members)

    print(f"standards (published): {len(std_members)}")
    print(f"candidates:            {len(cand_members)}")
    print(f"manifest members:      {len(std_members) + len(cand_members)}")
    print(f"wrote: machine-readable/{OUT_MANIFEST.name}")
    print(f"wrote: machine-readable/{OUT_TS.name}")
    if warnings:
        print(f"\n{len(warnings)} finding(s):")
        for w in warnings:
            print(f"  - {w}")
        return 1
    print("\nno drift findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
