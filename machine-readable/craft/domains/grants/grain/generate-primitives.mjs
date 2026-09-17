#!/usr/bin/env node
/**
 * Generate the typed primitives array from the canonical GRAIN notation.
 *
 * The primitives were hand-maintained for months and fell four releases behind
 * without anything noticing: the server encoded fifty at v0.1.7 while the
 * source had settled at a hundred and forty-six, and two renames from the Frame
 * Language pass never arrived. Hand-maintaining a copy of data that has a
 * canonical source is what produced that, so the copy is gone.
 *
 * This follows the pattern the Frame Language server already uses, where the
 * watchlist derives from a single term registry rather than a hand-edited list.
 *
 * The source markdown is vendored at packages/core/src/data so builds are
 * hermetic. The canonical source is GRAIN, the Grant Representation And
 * Interchange Notation, which holds 138 grant primitives across Layers 2
 * through 7 (Layer 1 holds no grant primitives: its methodological items were
 * extracted to the upstream standards). Re-vendor grain-notation.md from the
 * published GRAIN document, then regenerate: drift is caught at that boundary,
 * not scattered through a typed array.
 *
 * The script emits two artifacts from the one source: the typed primitives.ts
 * array (unchanged in shape) and a canonical primitives.json manifest for the
 * machine-readable layer.
 *
 * Usage: node scripts/generate-primitives.mjs
 */

import { readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const SOURCE = join(here, 'grain-notation.md')
const TARGET = join(here, 'primitives.generated.ts')
const MANIFEST = join(here, 'dist', 'primitives.json')

const LAYER_SLUGS = {
  'Identity Primitives': 'identity',
  'Obligation Primitives': 'obligation',
  'Evidence Primitives': 'evidence',
  'Specification Primitives': 'specification',
  'Causal Architecture Primitives': 'causal-architecture',
  'Portfolio Primitives': 'portfolio',
}

/** The six GRAIN layer slugs, in document order, with their expected counts. */
const EXPECTED_LAYER_COUNTS = {
  identity: 19,
  obligation: 55,
  evidence: 17,
  specification: 16,
  'causal-architecture': 11,
  portfolio: 20,
}

function frontMatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---/)
  if (!m) throw new Error('no front matter in the foundation source')
  const version = m[1].match(/^version:\s*(\S+)/m)
  const date = m[1].match(/^date:\s*(\S+)/m)
  if (!version) throw new Error('no version in the foundation front matter')
  return { version: version[1], date: date ? date[1] : 'unknown' }
}

/** Split the document into layer sections, then into primitives within each. */
function parse(text) {
  const lines = text.split('\n')
  const primitives = []
  let layer = null

  let current = null
  const flush = () => {
    if (!current) return
    primitives.push(current)
    current = null
  }

  for (const line of lines) {
    const layerMatch = line.match(/^## Layer \d+: (.+)$/)
    if (layerMatch) {
      flush()
      const slug = LAYER_SLUGS[layerMatch[1].trim()]
      if (!slug) throw new Error(`unknown layer heading: ${layerMatch[1]}`)
      layer = slug
      continue
    }
    // Any other level-two heading ends the primitive run for that layer.
    if (/^## /.test(line)) {
      flush()
      layer = null
      continue
    }
    const nameMatch = line.match(/^### (.+)$/)
    if (nameMatch) {
      flush()
      if (!layer) continue // a level-three heading outside any layer section
      current = { name: nameMatch[1].trim(), layer, body: [] }
      continue
    }
    if (current) current.body.push(line)
  }
  flush()

  return primitives.map((p) => {
    const body = p.body.join('\n')
    const relIdx = body.indexOf('**Relationships:**')
    const appIdx = body.indexOf('**Applications:**')

    const descEnd = relIdx >= 0 ? relIdx : appIdx >= 0 ? appIdx : body.length
    const description = clean(body.slice(0, descEnd))

    const relationships =
      relIdx >= 0
        ? clean(
            body
              .slice(relIdx + '**Relationships:**'.length, appIdx > relIdx ? appIdx : undefined)
              .replace(/\n---\s*$/, ''),
          )
        : ''
    const applications =
      appIdx >= 0 ? clean(body.slice(appIdx + '**Applications:**'.length)) : ''

    const id = slug(p.name)
    const status = /held[\s-]weak/i.test(body) ? 'held-weak' : 'full'
    const citations = extractCitations(applications)

    return { name: p.name, layer: p.layer, description, relationships, applications, id, status, citations }
  })
}

/** Kebab-case slug of a primitive name: lowercase, runs of non-alphanumerics to one hyphen. */
function slug(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

/**
 * Best-effort citation extraction from the Applications prose.
 *
 * GRAIN embeds sources in prose, not as a structured field, so this pulls only
 * the two clean signals: explicit URLs, and text introduced by a "source:"
 * label. Parenthetical named sources are left alone because most parentheticals
 * in this prose are not citations, and pulling them would be guessing. Where
 * neither signal is present the array is empty by design.
 */
function extractCitations(applications) {
  const out = []
  const seen = new Set()
  const add = (c) => {
    const v = c.trim().replace(/[),.;]+$/, '').trim()
    if (v && !seen.has(v)) {
      seen.add(v)
      out.push(v)
    }
  }
  for (const m of applications.matchAll(/https?:\/\/[^\s)]+/g)) add(m[0])
  for (const m of applications.matchAll(/source:\s*([^)]+)/gi)) add(m[1])
  return out
}

/** Strip the trailing rule, collapse whitespace, keep paragraph breaks readable. */
function clean(s) {
  return s
    .replace(/\n-{3,}\s*$/g, '')
    .split('\n')
    .map((l) => l.trim())
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}

function tsString(s) {
  return JSON.stringify(s)
}

function main() {
  const text = readFileSync(SOURCE, 'utf8')
  const { version, date } = frontMatter(text)
  const primitives = parse(text)

  const declared = text.match(/(\d+) grant primitives across Layers 2 through 7/)
  if (!declared) {
    throw new Error(
      'could not find the GRAIN count declaration ("N grant primitives across Layers 2 through 7"). ' +
        'The Count Note phrasing changed or the wrong source is vendored; do not generate blind.',
    )
  }
  if (Number(declared[1]) !== primitives.length) {
    throw new Error(
      `GRAIN declares ${declared[1]} grant primitives but ${primitives.length} were parsed. ` +
        'Either the document structure changed or the parser is wrong; do not generate from a mismatch.',
    )
  }

  const byLayer = {}
  for (const p of primitives) byLayer[p.layer] = (byLayer[p.layer] ?? 0) + 1

  for (const [layer, expected] of Object.entries(EXPECTED_LAYER_COUNTS)) {
    const got = byLayer[layer] ?? 0
    if (got !== expected) {
      throw new Error(
        `layer ${layer} parsed ${got} primitives but ${expected} were expected. ` +
          'The parser or the source structure changed; do not generate from a mismatch.',
      )
    }
  }
  for (const layer of Object.keys(byLayer)) {
    if (!(layer in EXPECTED_LAYER_COUNTS)) {
      throw new Error(`unexpected layer ${layer} parsed; not one of the six GRAIN layers.`)
    }
  }

  const ids = new Map()
  for (const p of primitives) {
    if (ids.has(p.id)) {
      throw new Error(`duplicate primitive id "${p.id}" from "${p.name}" and "${ids.get(p.id)}".`)
    }
    ids.set(p.id, p.name)
  }

  const header = `/**
 * All ${primitives.length} GRAIN grant primitives, generated from the canonical notation.
 *
 * DO NOT EDIT THIS FILE BY HAND. It is generated by scripts/generate-primitives.mjs
 * from packages/core/src/data/grain-notation.md. Edit the source and regenerate;
 * a hand edit will be overwritten by the next build and will not survive review.
 *
 * GRAIN version ${version} (${date}).
 * Layers: ${Object.entries(byLayer)
   .map(([l, n]) => `${l} ${n}`)
   .join(', ')}.
 *
 * License: CC0, inherited from the notation.
 */

import type { CrossPrimitive, PrimitiveLayer } from './types.js'

/** The version of the foundation this array was generated from. */
export const PRIMITIVES_FOUNDATION_VERSION = '${version}'

/** The date of the foundation this array was generated from. */
export const PRIMITIVES_FOUNDATION_DATE = '${date}'

export const PRIMITIVES: readonly CrossPrimitive[] = [
`

  const entries = primitives
    .map(
      (p) => `  {
    name: ${tsString(p.name)},
    layer: ${tsString(p.layer)},
    description: ${tsString(p.description)},
    relationships: ${tsString(p.relationships)},
    applications: ${tsString(p.applications)},
  },`,
    )
    .join('\n')

  const footer = `
]

/** Return a primitive by exact name, case-insensitive. */
export function getPrimitiveByName(name: string): CrossPrimitive | undefined {
  const lower = name.toLowerCase()
  return PRIMITIVES.find((p) => p.name.toLowerCase() === lower)
}

/** Return every primitive in a layer. */
export function getPrimitivesByLayer(layer: PrimitiveLayer): CrossPrimitive[] {
  return PRIMITIVES.filter((p) => p.layer === layer)
}

/** Search names, descriptions, relationships and applications for a keyword. */
export function searchPrimitives(keyword: string): CrossPrimitive[] {
  const lower = keyword.toLowerCase()
  return PRIMITIVES.filter(
    (p) =>
      p.name.toLowerCase().includes(lower) ||
      p.description.toLowerCase().includes(lower) ||
      p.relationships.toLowerCase().includes(lower) ||
      p.applications.toLowerCase().includes(lower),
  )
}
`

  writeFileSync(TARGET, header + entries + footer, 'utf8')

  // The machine-readable manifest: the same data as primitives.ts, plus the
  // id, status, and citation fields the JSON layer carries. It leads with the
  // human-readable name (the exact GRAIN heading) so the manifest is fully
  // self-describing without the id having to be de-slugged. The manifest field
  // is "definition" where the TypeScript type keeps "description"; both hold the
  // same text. Emitted from the one source so the two artifacts cannot drift.
  const manifest = {
    notation: 'GRAIN',
    title: 'Grant Representation And Interchange Notation',
    version,
    date,
    license: 'CC0',
    total: primitives.length,
    layerCounts: byLayer,
    primitives: primitives.map((p) => ({
      name: p.name,
      id: p.id,
      layer: p.layer,
      status: p.status,
      definition: p.description,
      relationships: p.relationships,
      applications: p.applications,
      citations: p.citations,
    })),
  }
  writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2) + '\n', 'utf8')

  console.log(`generated ${primitives.length} primitives from GRAIN ${version}`)
  for (const [layer, n] of Object.entries(byLayer)) console.log(`  ${layer}: ${n}`)
  const heldWeak = primitives.filter((p) => p.status === 'held-weak').length
  const withCitations = primitives.filter((p) => p.citations.length > 0).length
  console.log(`  held-weak: ${heldWeak}, full: ${primitives.length - heldWeak}`)
  console.log(`  primitives with extracted citations: ${withCitations}`)
  console.log(`wrote manifest to ${MANIFEST}`)
}

main()
