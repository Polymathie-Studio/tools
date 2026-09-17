#!/usr/bin/env node
/**
 * Zero-dependency validator for the GRAIN primitives manifest.
 *
 * Uses only node built-ins. Loads primitives.json (or a path given as the first
 * argument) and enforces the manifest contract: every primitive carries the
 * seven required fields with correct types; ids are unique and kebab-case; the
 * total is 138 and the six per-layer counts match; every status is in the
 * allowed set. Exits non-zero on any failure, so it can gate a publish.
 *
 * Usage:
 *   node validate.mjs                 # validate the real manifest
 *   node validate.mjs some.json       # validate a fixture (e.g. a negative one)
 */

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const target = process.argv[2] ? process.argv[2] : join(here, 'primitives.json')

const EXPECTED_TOTAL = 138
const EXPECTED_LAYER_COUNTS = {
  identity: 19,
  obligation: 55,
  evidence: 17,
  specification: 16,
  'causal-architecture': 11,
  portfolio: 20,
}
const LAYERS = new Set(Object.keys(EXPECTED_LAYER_COUNTS))
const STATUSES = new Set(['full', 'held-weak'])
const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/

const errors = []
const fail = (msg) => errors.push(msg)

function isString(v) {
  return typeof v === 'string'
}

let manifest
try {
  manifest = JSON.parse(readFileSync(target, 'utf8'))
} catch (e) {
  console.error(`could not read or parse ${target}: ${e.message}`)
  process.exit(1)
}

if (typeof manifest !== 'object' || manifest === null || Array.isArray(manifest)) {
  console.error('manifest is not a JSON object')
  process.exit(1)
}

if (!Array.isArray(manifest.primitives)) {
  console.error('manifest.primitives is missing or not an array')
  process.exit(1)
}

const seenIds = new Set()
const byLayer = {}

manifest.primitives.forEach((p, i) => {
  const where = p && isString(p.id) ? p.id : `index ${i}`
  if (typeof p !== 'object' || p === null || Array.isArray(p)) {
    fail(`primitive at ${where} is not an object`)
    return
  }
  // Required fields and types.
  if (!isString(p.name) || p.name.length === 0) fail(`primitive ${where}: name missing or empty`)
  if (!isString(p.id) || !KEBAB.test(p.id)) fail(`primitive ${where}: id missing or not kebab-case`)
  if (!isString(p.layer) || !LAYERS.has(p.layer)) fail(`primitive ${where}: layer missing or not one of the six`)
  if (!isString(p.status) || !STATUSES.has(p.status)) fail(`primitive ${where}: status missing or not in {full, held-weak}`)
  if (!isString(p.definition) || p.definition.length === 0) fail(`primitive ${where}: definition missing or empty`)
  if (!isString(p.relationships)) fail(`primitive ${where}: relationships missing or not a string`)
  if (!isString(p.applications)) fail(`primitive ${where}: applications missing or not a string`)
  if (!Array.isArray(p.citations) || !p.citations.every(isString)) {
    fail(`primitive ${where}: citations missing or not an array of strings`)
  }
  // No unexpected fields.
  const allowed = new Set(['name', 'id', 'layer', 'status', 'definition', 'relationships', 'applications', 'citations'])
  for (const k of Object.keys(p)) {
    if (!allowed.has(k)) fail(`primitive ${where}: unexpected field "${k}"`)
  }
  // Uniqueness and per-layer tally.
  if (isString(p.id)) {
    if (seenIds.has(p.id)) fail(`duplicate id "${p.id}"`)
    seenIds.add(p.id)
  }
  if (isString(p.layer) && LAYERS.has(p.layer)) byLayer[p.layer] = (byLayer[p.layer] ?? 0) + 1
})

// Total.
if (manifest.primitives.length !== EXPECTED_TOTAL) {
  fail(`total is ${manifest.primitives.length}, expected ${EXPECTED_TOTAL}`)
}
if (manifest.total !== undefined && manifest.total !== manifest.primitives.length) {
  fail(`manifest.total (${manifest.total}) does not match the primitives array length (${manifest.primitives.length})`)
}

// Per-layer counts.
for (const [layer, expected] of Object.entries(EXPECTED_LAYER_COUNTS)) {
  const got = byLayer[layer] ?? 0
  if (got !== expected) fail(`layer ${layer}: counted ${got}, expected ${expected}`)
}

if (errors.length > 0) {
  console.error(`FAIL: ${errors.length} problem(s) in ${target}`)
  for (const e of errors) console.error(`  - ${e}`)
  process.exit(1)
}

console.log(`PASS: ${target} is a valid GRAIN primitives manifest (${manifest.primitives.length} primitives).`)
process.exit(0)
