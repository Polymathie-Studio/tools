#!/usr/bin/env -S deno run --allow-read
// Zero-dependency JSON Schema validator for the Polymathie family manifest.
//
// It covers the JSON Schema (draft 2020-12) features the manifest schema uses:
// type (including unions and null), required, properties, additionalProperties
// (boolean or subschema), items, enum, and $ref into $defs. No dependency, so
// MISSING stays as dependency-free as the family it describes. The schema itself
// is a portable standard, so adopters may validate their own manifests with any
// JSON Schema tool; this script is our own check.
//
// Run: deno run --allow-read validate.ts [path-to-manifest.json]

type Json = unknown;
type Schema = Record<string, any>;

function jsonType(v: Json): string {
  if (v === null) return "null";
  if (Array.isArray(v)) return "array";
  if (Number.isInteger(v)) return "integer";
  return typeof v;
}

function typeMatches(v: Json, t: string): boolean {
  if (t === "integer") return Number.isInteger(v as number);
  if (t === "number") return typeof v === "number";
  if (t === "object") return v !== null && typeof v === "object" && !Array.isArray(v);
  if (t === "array") return Array.isArray(v);
  return jsonType(v) === t;
}

function resolveRef(ref: string, root: Schema): Schema {
  if (!ref.startsWith("#/")) throw new Error(`unsupported $ref: ${ref}`);
  let node: any = root;
  for (const part of ref.slice(2).split("/")) node = node?.[part];
  if (!node) throw new Error(`$ref not found: ${ref}`);
  return node;
}

function validate(data: Json, schema: Schema, path: string, root: Schema, errors: string[]): void {
  if (schema.$ref) {
    validate(data, resolveRef(schema.$ref, root), path, root, errors);
    return;
  }

  if (schema.type) {
    const types = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!types.some((t: string) => typeMatches(data, t))) {
      errors.push(`${path}: expected type ${types.join(" or ")}, got ${jsonType(data)}`);
      return; // later checks assume the type held
    }
  }

  if (schema.enum && !schema.enum.some((e: Json) => e === data)) {
    errors.push(`${path}: ${JSON.stringify(data)} is not one of ${JSON.stringify(schema.enum)}`);
  }

  if (typeMatches(data, "object")) {
    const obj = data as Record<string, Json>;
    for (const key of schema.required ?? []) {
      if (!(key in obj)) errors.push(`${path}: missing required property "${key}"`);
    }
    const props = schema.properties ?? {};
    const addl = schema.additionalProperties;
    for (const [key, val] of Object.entries(obj)) {
      const childPath = `${path}/${key}`;
      if (key in props) validate(val, props[key], childPath, root, errors);
      else if (addl === false) errors.push(`${childPath}: additional property not allowed`);
      else if (addl && typeof addl === "object") validate(val, addl, childPath, root, errors);
    }
  }

  if (typeMatches(data, "array") && schema.items) {
    (data as Json[]).forEach((el, i) => validate(el, schema.items, `${path}[${i}]`, root, errors));
  }
}

const dir = new URL(".", import.meta.url).pathname;
const target = Deno.args[0] ?? dir + "manifest.json";
const schema = JSON.parse(await Deno.readTextFile(dir + "manifest.schema.json"));
const manifest = JSON.parse(await Deno.readTextFile(target));

const errors: string[] = [];
validate(manifest, schema, "manifest", schema, errors);

if (errors.length === 0) {
  console.log(`VALID: ${target} conforms to manifest.schema.json`);
} else {
  console.error(`INVALID: ${errors.length} error(s) in ${target}:`);
  for (const e of errors) console.error("  " + e);
  Deno.exit(1);
}
