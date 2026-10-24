/** Fixed DOC06 source projection. All selected package files remain inert bytes.
 * Local DEV output, not a shared Fragment/Bundle or a configuration validator.
 * External snapshot preparation alone establishes commit-to-bytes binding.
 */
const PROFILE = "configuration-source-energy-chunk-v1";
const TOOL = "qcl-negf.doc06-static-slice.v1";
const CLASSES = [
  "signature",
  "units",
  "default",
  "constraint",
  "effects",
  "errors",
  "formula_origin",
  "value_origin",
  "assigning_origin",
  "effective_origin",
];
const PATHS = [
  "runner/src/application/configuration_types.jl",
  "runner/src/infrastructure/config/configuration.jl",
  "runner/src/infrastructure/config/configuration_sources.jl",
  "runner/src/application/auto_strategy.jl",
  "runner/docs/src/user/configuration.md",
  "runner/test/fixtures/configurations/base.yaml",
  "runner/schema/run.schema.json",
  "contracts/src/qcl_negf_contracts/schemas/run.schema.json",
  "core/src/numerics/optimized/production_contracts.jl",
] as const;
const OWNERS: Record<string, string> = {
  runner: "components/QCLNEGFRunner.jl",
  contracts: "components/qcl-negf-contracts",
  core: "components/QCLNEGF.jl",
};
const encoder = new TextEncoder();
const decoder = new TextDecoder("utf-8", { fatal: true });
const FILE_CAP = 128 * 1024;
const SOURCE_CAP = 512 * 1024;
const RECEIPT_CAP = 16 * 1024;
const OUTPUT_CAP = 32 * 1024;
class Refusal extends Error {
  constructor(readonly reason: string) {
    super(reason);
  }
}
class Unsupported extends Error {
  constructor(readonly reason: string) {
    super(reason);
  }
}
function refuse(reason: string): never {
  throw new Refusal(reason);
}
function unsupported(reason: string): never {
  throw new Unsupported(reason);
}
function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    unsupported("malformed_schema");
  }
  return value as Record<string, unknown>;
}
function own(obj: Record<string, unknown>, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(obj, key);
}
function bytes(text: string): number {
  return encoder.encode(text).length;
}
async function sha256(data: Uint8Array): Promise<string> {
  // An owned ArrayBuffer is required by the Deno2.8 WebCrypto DOM signature.
  const owned = new Uint8Array(data.length);
  owned.set(data);
  return Array.from(
    new Uint8Array(await crypto.subtle.digest("SHA-256", owned.buffer)),
    (b) => b.toString(16).padStart(2, "0"),
  ).join("");
}
function json(value: unknown): string {
  return JSON.stringify(value, null, 2) + "\n";
}

/** Bounded lexical/syntax guard, then built-in JSON.parse as data only.
 * No target loaders, references or embedded code are invoked by this routine.
 */
function parseData(text: string): unknown {
  let i = 0, tokens = 0;
  function token() {
    if (++tokens > 32768) refuse("json_token_cap");
  }
  function ws() {
    while (i < text.length && /[\x20\t\r\n]/.test(text[i])) i++;
  }
  function punct(c: string) {
    ws();
    if (text[i] !== c) unsupported("malformed_schema");
    token();
    i++;
  }
  function string(): string {
    ws();
    if (text[i] !== '"') unsupported("malformed_schema");
    token();
    const start = i++;
    let contentBytes = 0;
    while (i < text.length) {
      const c = text[i++];
      if (c === '"') {
        let value: unknown;
        try {
          value = JSON.parse(text.slice(start, i));
        } catch {
          unsupported("malformed_schema");
        }
        if (typeof value !== "string") unsupported("malformed_schema");
        if (bytes(value) > 16384) refuse("json_string_cap");
        return value;
      }
      if (c.charCodeAt(0) < 32) unsupported("malformed_schema");
      if (c === "\\") {
        if (i >= text.length) unsupported("malformed_schema");
        const escape = text[i++];
        if (escape === "u") {
          if (!/^[0-9a-fA-F]{4}$/.test(text.slice(i, i + 4))) unsupported("malformed_schema");
          i += 4;
        } else if (!'"\\/bfnrt'.includes(escape)) unsupported("malformed_schema");
      }
      // Bound raw token work before decoding; escaped strings may take up to
      // six raw ASCII bytes per decoded character, still within file cap.
      contentBytes++;
      if (contentBytes > 6 * 16384) refuse("json_string_cap");
    }
    unsupported("malformed_schema");
  }
  function value(depth: number): void {
    ws();
    if (text[i] === "{" || text[i] === "[") {
      if (depth >= 32) refuse("json_depth_cap");
      if (text[i] === "{") {
        punct("{");
        ws();
        const keys = new Set<string>();
        if (text[i] !== "}") {
          while (true) {
            const key = string();
            if (
              keys.has(key) || ["__proto__", "prototype", "constructor"].includes(key)
            ) unsupported("malformed_schema");
            keys.add(key);
            punct(":");
            value(depth + 1);
            ws();
            if (text[i] !== ",") break;
            punct(",");
          }
        }
        punct("}");
      } else {
        punct("[");
        ws();
        if (text[i] !== "]") {
          while (true) {
            value(depth + 1);
            ws();
            if (text[i] !== ",") break;
            punct(",");
          }
        }
        punct("]");
      }
    } else if (text[i] === '"') string();
    else {
      const tail = text.slice(i);
      const literal = /^(?:true|false|null)/.exec(tail);
      const number = /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/.exec(tail);
      const match = literal ?? number;
      if (!match) unsupported("malformed_schema");
      token();
      i += match[0].length;
      if (number && !literal) {
        const n = Number(match[0]);
        if (!Number.isFinite(n) || (Number.isInteger(n) && !Number.isSafeInteger(n))) {
          unsupported("malformed_schema");
        }
      }
    }
  }
  value(0);
  ws();
  if (i !== text.length) unsupported("malformed_schema");
  try {
    return JSON.parse(text);
  } catch {
    unsupported("malformed_schema");
  }
}

function absolute(path: string): string {
  if (!path.startsWith("/") || path.includes("\0") || path.includes("\\")) refuse("invalid_path");
  const parts = path.split("/");
  if (parts.includes(".") || parts.includes("..")) refuse("invalid_path");
  return "/" + parts.filter(Boolean).join("/");
}
function within(path: string, root: string): boolean {
  return path === root || path.startsWith(root + "/");
}
async function statMaybe(path: string): Promise<Deno.FileInfo | null> {
  try {
    return await Deno.lstat(path);
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) return null;
    throw error;
  }
}
async function realDirectory(path: string) {
  const info = await Deno.lstat(path);
  if (info.isSymlink || !info.isDirectory || await Deno.realPath(path) !== path) {
    refuse("symlink_or_invalid_directory");
  }
}
async function selectedPath(root: string, relative: string): Promise<boolean> {
  let path = root;
  const parts = relative.split("/");
  for (let i = 0; i < parts.length; i++) {
    path += "/" + parts[i];
    const info = await statMaybe(path);
    if (!info) return false;
    if (
      info.isSymlink || (i < parts.length - 1 && !info.isDirectory) ||
      (i === parts.length - 1 && !info.isFile)
    ) refuse("symlink_or_invalid_source");
  }
  return true;
}
async function boundedRead(path: string, cap: number): Promise<Uint8Array> {
  const info = await Deno.lstat(path);
  if (info.isSymlink || !info.isFile) refuse("symlink_or_invalid_source");
  if (info.size > cap) refuse("input_byte_cap");
  // Read into a prebounded buffer; readFile could allocate beyond a prior stat
  // if the source grew. A retained frozen snapshot is still an external premise.
  const buffer = new Uint8Array(info.size + 1);
  const file = await Deno.open(path, { read: true });
  try {
    const opened = await file.stat();
    if (!opened.isFile || opened.size !== info.size) refuse("source_changed");
    let count = 0;
    while (count < buffer.length) {
      const n = await file.read(buffer.subarray(count));
      if (n === null) break;
      count += n;
    }
    if (count !== info.size || (await file.stat()).size !== info.size) refuse("source_changed");
    return buffer.subarray(0, count);
  } finally {
    file.close();
  }
}
function strictText(data: Uint8Array): string {
  try {
    return decoder.decode(data).replace(/\r\n?/g, "\n");
  } catch {
    refuse("invalid_utf8");
  }
}
type InputEntry = { path: string; owner: string; revision: string; sha256: string; bytes: number };
type Input = InputEntry & {
  actual_sha256: string | null;
  actual_bytes: number | null;
  status: string;
  text: string | null;
};
function inputEntries(value: unknown): { graph: string; files: InputEntry[] } {
  const root = object(value);
  if (
    root.format !== "qcl-negf.doc06-source-input.v1" ||
    typeof root.source_graph_sha256 !== "string" ||
    !/^[a-f0-9]{64}$/.test(root.source_graph_sha256) || !Array.isArray(root.files)
  ) refuse("invalid_source_receipt");
  if (root.files.length > 12) refuse("source_count_cap");
  if (root.files.length !== PATHS.length) refuse("incomplete_source_receipt");
  const seen = new Set<string>();
  const files: InputEntry[] = [];
  for (const raw of root.files) {
    const item = object(raw);
    if (
      typeof item.path !== "string" || !PATHS.some((p) => p === item.path) || seen.has(item.path)
    ) refuse("invalid_source_path");
    seen.add(item.path);
    const owner = OWNERS[item.path.split("/")[0]];
    if (
      item.owner !== owner || typeof item.revision !== "string" ||
      !/^[a-f0-9]{40}$/.test(item.revision) ||
      typeof item.sha256 !== "string" || !/^[a-f0-9]{64}$/.test(item.sha256) ||
      typeof item.bytes !== "number" || !Number.isSafeInteger(item.bytes) || item.bytes < 0
    ) refuse("invalid_source_identity");
    if (item.bytes > FILE_CAP) refuse("input_byte_cap");
    files.push({
      path: item.path,
      owner,
      revision: item.revision,
      sha256: item.sha256,
      bytes: item.bytes,
    });
  }
  if (files.reduce((sum, f) => sum + f.bytes, 0) > SOURCE_CAP) refuse("aggregate_source_cap");
  return { graph: root.source_graph_sha256, files };
}

type Observation = { value: unknown; reason?: string; selector: string };
function missing(selector: string): Observation {
  return { value: null, reason: "source_missing", selector };
}
function failed(selector: string, reason = "unsupported_syntax"): Observation {
  return { value: null, reason, selector };
}
type JuliaText = {
  mask: string;
  hasCmd: boolean;
  docs: { start: number; end: number; text: string; literal: boolean }[];
};
/** Mask strings/comments, retaining offsets and newlines. No Julia AST/evaluation. */
function juliaText(text: string): JuliaText {
  const mask = text.split("");
  const docs: JuliaText["docs"] = [];
  let hasCmd = false;
  function blank(start: number, end: number) {
    for (let j = start; j < end; j++) if (text[j] !== "\n") mask[j] = " ";
  }
  let i = 0;
  while (i < text.length) {
    const start = i;
    if (text.startsWith("#=", i)) {
      i += 2;
      let depth = 1;
      while (i < text.length && depth) {
        if (text.startsWith("#=", i)) {
          depth++;
          i += 2;
        } else if (text.startsWith("=#", i)) {
          depth--;
          i += 2;
        } else i++;
      }
      blank(start, i);
    } else if (text[i] === "#") {
      while (i < text.length && text[i] !== "\n") i++;
      blank(start, i);
    } else if (text[i] === "`") {
      // Cmd interpolation/nesting is outside the supported source grammar.
      // Mask the bounded literal, and conservatively disable typed extraction
      // for the whole selected file even when its first delimiter is closed.
      hasCmd = true;
      i++;
      while (i < text.length) {
        if (text[i] === "\\") {
          i += 2;
          continue;
        }
        if (text[i++] === "`") break;
      }
      blank(start, Math.min(i, text.length));
    } else if (text[i] === '"' || text[i] === "'") {
      const triple = text.startsWith('"""', i);
      const delimiter = triple ? '"""' : text[i];
      i += delimiter.length;
      const content = i;
      let literal = true, closed = false;
      while (i < text.length) {
        if (text[i] === "\\") {
          i += 2;
          continue;
        }
        if (text[i] === "$") literal = false;
        if (text.startsWith(delimiter, i)) {
          closed = true;
          break;
        }
        i++;
      }
      // An assigned/string-macro literal is not an associated docstring.
      const prefix = text.slice(text.lastIndexOf("\n", start - 1) + 1, start);
      if (triple && closed && /^\s*$/.test(prefix)) {
        docs.push({ start, end: i + 3, text: text.slice(content, i), literal });
      }
      i = closed ? i + delimiter.length : text.length;
      blank(start, i);
    } else i++;
  }
  return { mask: mask.join(""), docs, hasCmd };
}
function lines(text: string, offset: number): number {
  return text.slice(0, offset).split("\n").length;
}
function apiObservations(
  input: Input,
): { documented: Observation; typed: Observation; doc: Observation } {
  const selector = "configuration_source";
  if (input.text === null) {
    return { documented: missing(selector), typed: missing(selector), doc: missing(selector) };
  }
  const text = input.text;
  const lex = juliaText(text);
  const methods = [...lex.mask.matchAll(/\bfunction\s+configuration_source\s*\(/g)];
  let typed = failed(selector), documented = failed(selector), doc = failed(selector);
  if (methods.length !== 1) return { documented, typed, doc };
  const method = methods[0], start = method.index!;
  const previous = lex.docs.filter((d) => d.end <= start).at(-1);
  if (
    previous && previous.literal && /^\s*(?:@\w+\s*)?$/.test(lex.mask.slice(previous.end, start))
  ) {
    if (bytes(previous.text) > 4096) refuse("docstring_byte_cap");
    const signatures = [
      ...previous.text.matchAll(/^\s*(configuration_source\(configuration,\s*dotted_path\))\s*$/gm),
    ];
    if (signatures.length === 1) {
      const value = signatures[0][1].replace(/,\s*/, ", ");
      if (bytes(value) > 512) refuse("signature_byte_cap");
      documented = {
        value,
        selector: `configuration_source:docstring:L${lines(text, previous.start)}`,
      };
      doc = { value: previous.text.trim(), selector: documented.selector };
    }
  }
  const linePrefix = lex.mask.slice(lex.mask.lastIndexOf("\n", start - 1) + 1, start);
  const header = /^function\s+configuration_source\s*\(([^)]*)\)([^\n]*)/.exec(
    lex.mask.slice(start),
  );
  if (
    header && !lex.hasCmd && /^\s*$/.test(linePrefix) && !/@\w+/.test(lex.mask.slice(0, start)) &&
    /^configuration::ResolvedRunConfiguration,dotted_path::AbstractString,?$/.test(
      header[1].replace(/\s/g, ""),
    ) && /^\s*$/.test(header[2])
  ) {
    if (bytes(header[0]) > 512) refuse("signature_byte_cap");
    typed = {
      value:
        "configuration_source(configuration::ResolvedRunConfiguration, dotted_path::AbstractString)",
      selector: `configuration_source:typed-header:L${lines(text, start)}`,
    };
  }
  return { documented, typed, doc };
}
function typedDefault(input: Input): Observation {
  const selector = "ProductionOptions.energy_chunk";
  if (input.text === null) return missing(selector);
  const lex = juliaText(input.text);
  if (lex.hasCmd) return failed(selector, "unsupported_command_literal");
  const structs = [
    ...lex.mask.matchAll(/^\s*(?:Base\.@kwdef\s+)?struct\s+ProductionOptions\s*$/gm),
  ];
  if (structs.length !== 1) return failed(selector);
  const start = structs[0].index! + structs[0][0].length;
  const end = /^\s*end\s*$/m.exec(lex.mask.slice(start));
  if (!end) return failed(selector);
  const region = lex.mask.slice(start, start + end.index);
  if (/@\w+/.test(region)) return failed(selector, "unsupported_macro_context");
  // Only a flat list of typed field declarations is supported. In particular,
  // the first end must not terminate an inner constructor/body whose local
  // typed assignment happens to resemble a field. Other field RHS remain
  // opaque, but block forms and non-field statements make this region unknown.
  const fieldLines = region.split("\n").filter((line) => line.trim().length > 0);
  if (
    fieldLines.some((line) => !/^[ \t]+[A-Za-z_]\w*[ \t]*::[^\n]+$/.test(line)) ||
    /\b(?:function|begin|quote|let|for|while|if|try|struct|macro|do|end)\b/.test(region)
  ) {
    return failed(selector, "unsupported_nested_struct_context");
  }
  const fields = [...region.matchAll(/^\s*energy_chunk\s*::\s*Int\s*=([^\n]*)$/gm)];
  if (fields.length !== 1 || !/^\s*\d+\s*$/.test(fields[0][1])) return failed(selector);
  const value = Number(fields[0][1].trim());
  if (!Number.isSafeInteger(value)) return failed(selector, "unsafe_integer_literal");
  return { value, selector: `${selector}:L${lines(input.text, start + fields[0].index!)}` };
}
function exampleValue(input: Input): Observation {
  const selector = "production.energy_chunk";
  if (input.text === null) return missing(selector);
  const text = input.text;
  const blocks = [...text.matchAll(/^production:\s*(?:#[^\n]*)?$/gm)];
  if (blocks.length !== 1) return failed(selector);
  const start = blocks[0].index! + blocks[0][0].length;
  const rest = text.slice(start).replace(/^\n/, "");
  const block = rest.split(/^(?=[^\s#])/m)[0];
  if (/^\s*(?:<<:|[!&*])/m.test(block)) return failed(selector);
  const leaves = [...block.matchAll(/^[ ]{2}energy_chunk:([^\n]*)$/gm)];
  if (leaves.length !== 1) return failed(selector);
  const literal = /^\s*(\d+)\s*(?:#[^\n]*)?$/.exec(leaves[0][1]);
  if (!literal || !Number.isSafeInteger(Number(literal[1]))) return failed(selector);
  return { value: Number(literal[1]), selector: `${selector}:L${lines(text, start) + 1}` };
}

type SchemaProjection = {
  constraint: Observation;
  declaration: Observation;
  description: Observation;
  rootRequired: Observation;
  productionRequired: Observation;
  validationCoverage: Observation;
};
function schemaProjection(input: Input): SchemaProjection {
  const pointer = "/$defs/production/properties/energy_chunk";
  const unavailable = input.text === null ? missing(pointer) : failed(pointer);
  const result: SchemaProjection = {
    constraint: unavailable,
    declaration: unavailable,
    description: unavailable,
    rootRequired: input.text === null ? missing("/required") : failed("/required"),
    productionRequired: unavailable,
    validationCoverage: input.text === null ? missing("") : failed(""),
  };
  if (input.text === null) return result;
  let failurePointer = "";
  const segment = (key: string) => key.replace(/~/g, "~0").replace(/\//g, "~1");
  try {
    const root = object(parseData(input.text));
    const required = function (node: Record<string, unknown>, location: string): string[] {
      failurePointer = location + "/required";
      if (!own(node, "required")) return [];
      const list = node.required;
      if (
        !Array.isArray(list) || list.some((x) => typeof x !== "string") ||
        new Set(list).size !== list.length
      ) unsupported("malformed_schema");
      return list as string[];
    };
    const allowed = function (
      node: Record<string, unknown>,
      keys: string[],
      location: string,
      reason = "unsupported_schema_keyword",
    ) {
      const extra = Object.keys(node).find((key) => !keys.includes(key));
      if (extra !== undefined) {
        failurePointer = location + "/" + segment(extra);
        unsupported(reason);
      }
    };
    // Only keywords which cannot add an unprojected selected-path condition
    // are permitted here. Unselected properties/$defs are opaque data.
    const objectKeys = [
      "$schema",
      "$id",
      "$comment",
      "title",
      "description",
      "examples",
      "type",
      "required",
      "properties",
      "$defs",
      "definitions",
      "additionalProperties",
      "$ref",
    ];
    const leafKeys = [
      "$comment",
      "title",
      "description",
      "examples",
      "type",
      "minimum",
      "default",
      "$ref",
    ];
    // Literal root membership is independent of later selected-path coverage.
    failurePointer = "/type";
    if (own(root, "type") && root.type !== "object") unsupported("malformed_schema");
    result.rootRequired = {
      value: required(root, "").includes("production"),
      selector: "/required",
    };
    // allOf is accepted only through this narrow scope classifier. Conditions
    // are never evaluated; values below other immediate root properties are
    // opaque source data, including their nested refs/combinators.
    allowed(root, [...objectKeys, "allOf"], "", "unsupported_selected_schema_context");
    if (own(root, "$ref")) {
      failurePointer = "/$ref";
      unsupported("unsupported_root_ref");
    }
    const footprint: { if: string[]; then: string[] }[] = [];
    if (own(root, "allOf")) {
      failurePointer = "/allOf";
      if (!Array.isArray(root.allOf) || root.allOf.length === 0) unsupported("malformed_schema");
      for (let i = 0; i < root.allOf.length; i++) {
        const location = `/allOf/${i}`;
        failurePointer = location;
        const item = object(root.allOf[i]);
        allowed(item, ["if", "then"], location, "unsupported_selected_schema_context");
        const scopes = { if: [] as string[], then: [] as string[] };
        for (const clause of ["if", "then"] as const) {
          failurePointer = location + "/" + clause;
          if (!own(item, clause)) unsupported("unsupported_selected_schema_context");
          const node = object(item[clause]);
          allowed(node, ["properties"], failurePointer, "unsupported_selected_schema_context");
          failurePointer = location + "/" + clause + "/properties";
          if (!own(node, "properties")) unsupported("unsupported_selected_schema_context");
          const properties = object(node.properties);
          const names = Object.keys(properties);
          if (names.length === 0) unsupported("malformed_schema");
          if (own(properties, "production")) {
            failurePointer += "/production";
            unsupported("unsupported_selected_schema_context");
          }
          scopes[clause] = names;
        }
        footprint.push(scopes);
      }
    }
    result.validationCoverage = { value: footprint, selector: own(root, "allOf") ? "/allOf" : "" };
    let hops = 0;
    const seen = new Set<string>();
    const resolve = function (
      raw: unknown,
      location: string,
    ): { node: Record<string, unknown>; location: string } {
      failurePointer = location;
      let node = object(raw);
      while (own(node, "$ref")) {
        failurePointer = location + "/$ref";
        // Draft-specific sibling constraints are intentionally unsupported.
        allowed(
          node,
          ["$ref", "$comment", "title", "description"],
          location,
          "unsupported_ref_siblings",
        );
        const ref = node.$ref;
        if (typeof ref !== "string" || !ref.startsWith("#/")) unsupported("unsupported_local_ref");
        if (seen.has(ref)) unsupported("cyclic_local_ref");
        if (++hops > 8) refuse("local_ref_hop_cap");
        seen.add(ref);
        let value: unknown = root;
        const parts = ref.slice(2).split("/");
        for (const part of parts) {
          if (/~(?![01])/.test(part)) unsupported("unsupported_local_ref");
          const key = part.replace(/~1/g, "/").replace(/~0/g, "~");
          const container = object(value);
          if (!own(container, key)) unsupported("missing_local_ref");
          value = container[key];
        }
        location = ref.slice(1);
        failurePointer = location;
        node = object(value);
      }
      return { node, location };
    };
    failurePointer = "/properties";
    const production = resolve(object(root.properties).production, "/properties/production");
    allowed(production.node, objectKeys, production.location);
    failurePointer = production.location + "/type";
    if (production.node.type !== "object") unsupported("malformed_schema");
    const productionRequired = required(production.node, production.location);
    result.productionRequired = {
      value: productionRequired.includes("energy_chunk"),
      selector: production.location + "/required",
    };
    failurePointer = production.location + "/properties";
    const selected = resolve(
      object(production.node.properties).energy_chunk,
      production.location + "/properties/energy_chunk",
    );
    allowed(selected.node, leafKeys, selected.location);
    failurePointer = selected.location + "/type";
    if (selected.node.type !== "integer") unsupported("malformed_schema");
    failurePointer = selected.location + "/minimum";
    if (typeof selected.node.minimum !== "number" || !Number.isFinite(selected.node.minimum)) {
      unsupported("malformed_schema");
    }
    failurePointer = selected.location + "/description";
    if (own(selected.node, "description") && typeof selected.node.description !== "string") {
      unsupported("malformed_schema");
    }
    failurePointer = selected.location + "/default";
    if (
      own(selected.node, "default") &&
      (typeof selected.node.default !== "number" || !Number.isSafeInteger(selected.node.default))
    ) unsupported("unsupported_schema_default");
    result.constraint = {
      value: {
        type: "integer",
        minimum: selected.node.minimum,
        required: productionRequired.includes("energy_chunk"),
      },
      selector: selected.location,
    };
    result.declaration = {
      value: own(selected.node, "default") ? selected.node.default : null,
      selector: selected.location + "/default",
    };
    result.description = typeof selected.node.description === "string"
      ? { value: selected.node.description, selector: selected.location + "/description" }
      : failed(selected.location + "/description", "description_absent");
  } catch (error) {
    if (!(error instanceof Unsupported)) throw error;
    // Never project a successfully read prefix as a full selected constraint.
    result.constraint = failed(failurePointer, error.reason);
    result.declaration = failed(failurePointer, error.reason);
    result.description = failed(failurePointer, error.reason);
    result.validationCoverage = failed(failurePointer, error.reason);
  }
  return result;
}

type Status = "known" | "partial" | "unknown" | "not_assigned" | "not_applicable";
type Mode = "literal-extraction" | "authored-context" | "dynamic-unknown";
type SourceRef = {
  owner: string;
  revision: string;
  path: string;
  sha256: string;
  selector: string;
};
type Fact = { name: string; status: Status; text: string; sources: SourceRef[] };
type Extraction = {
  subject: string;
  fact_index: number;
  mode: Mode;
  context: string;
  value: unknown;
  selector: string | null;
  reason?: string;
};
type Subject = { kind: "api" | "input"; key: string; facts: Fact[] };
function sourceRef(input: Input, selector: string): SourceRef[] {
  if (input.actual_sha256 === null) return [];
  return [{
    owner: input.owner,
    revision: input.revision,
    path: input.path.slice(input.path.indexOf("/") + 1),
    sha256: input.actual_sha256,
    selector,
  }];
}
function buildProjection(inputs: Input[], graph: string, manifestHash: string) {
  const api: Subject = { kind: "api", key: "configuration_source", facts: [] };
  const leaf: Subject = { kind: "input", key: "production.energy_chunk", facts: [] };
  const extractions: Extraction[] = [];
  const diagnostics: { reason: string }[] = [];
  const byPath = (path: string) => inputs.find((i) => i.path === path)!;
  const apiInput = byPath(PATHS[0]), coreInput = byPath(PATHS[8]), exampleInput = byPath(PATHS[5]);
  const schemaInput = byPath(PATHS[7]),
    packagedInput = byPath(PATHS[6]),
    routeInput = byPath(PATHS[4]);
  const observedApi = apiObservations(apiInput);
  const observedTyped = typedDefault(coreInput);
  const observedExample = exampleValue(exampleInput);
  const observedSchema = schemaProjection(schemaInput);
  // Precheck packaged schema independently; it can never replace canonical facts.
  if (packagedInput.text !== null) {
    try {
      parseData(packagedInput.text);
    } catch (error) {
      if (!(error instanceof Unsupported)) throw error;
      diagnostics.push({ reason: "malformed_packaged_schema" });
    }
  }
  if (
    packagedInput.actual_sha256 !== null && schemaInput.actual_sha256 !== null &&
    packagedInput.actual_sha256 !== schemaInput.actual_sha256
  ) diagnostics.push({ reason: "packaged_schema_mismatch" });
  function add(
    subject: Subject,
    name: string,
    status: Status,
    text: string,
    context: string,
    observation?: Observation,
    input?: Input,
    mode?: Mode,
  ) {
    if (text.length > 2048) refuse("fact_text_cap");
    const sources = input && observation ? sourceRef(input, observation.selector) : [];
    const fact_index = subject.facts.length;
    subject.facts.push({ name, status, text, sources });
    extractions.push({
      subject: subject.key,
      fact_index,
      mode: mode ?? (observation?.reason ? "dynamic-unknown" : "authored-context"),
      context,
      value: observation?.value ?? null,
      selector: observation?.selector ?? null,
      ...(observation?.reason ? { reason: observation.reason } : {}),
    });
  }
  function literal(
    subject: Subject,
    name: string,
    context: string,
    observation: Observation,
    input: Input,
    label: string,
    known: Status = "known",
  ) {
    add(
      subject,
      name,
      observation.reason
        ? (observation.reason === "source_missing" ? "unknown" : "partial")
        : known,
      observation.reason
        ? `${label}: извлечение недоступно (${observation.reason}); значение не вычислялось.`
        : `${label}: ${
          typeof observation.value === "string"
            ? observation.value
            : JSON.stringify(observation.value)
        }. Это декларация исходного текста.`,
      context,
      observation,
      input,
      observation.reason ? "dynamic-unknown" : "literal-extraction",
    );
  }
  // API literal documentation is distinct from the nonexhaustive typed header.
  literal(
    api,
    "signature",
    "documented-signature",
    observedApi.documented,
    apiInput,
    "Документированная сигнатура",
  );
  literal(
    api,
    "signature",
    "typed-signature",
    observedApi.typed,
    apiInput,
    "Текстовый typed header; не полный список методов",
    "partial",
  );
  add(
    api,
    "units",
    "not_applicable",
    "Авторский контекст: идентификатор источника или nothing не является физической величиной.",
    "units",
  );
  add(
    api,
    "default",
    observedApi.typed.reason ? "partial" : "not_assigned",
    observedApi.typed.reason
      ? "Аргументные defaults не установлены: header не распознан."
      : "В распознанном текстовом header аргументные defaults не объявлены; методы не исполнялись.",
    "argument-defaults",
    observedApi.typed,
    apiInput,
  );
  add(
    api,
    "constraint",
    "partial",
    "Текстовый header описывает ResolvedRunConfiguration и AbstractString; lookup не подтверждает schema validation и полный dispatch contract.",
    "typed-constraints",
    observedApi.typed,
    apiInput,
  );
  if (!observedApi.doc.reason) {
    add(
      api,
      "effects",
      "known",
      "Документированное описание (не runtime effect inventory):\n" + String(observedApi.doc.value),
      "documented-effects",
      observedApi.doc,
      apiInput,
      "literal-extraction",
    );
  } else {
    add(
      api,
      "effects",
      "unknown",
      "Документированное описание lookup недоступно; effects не восстанавливались из тела функции.",
      "documented-effects",
      observedApi.doc,
      apiInput,
      "dynamic-unknown",
    );
  }
  add(
    api,
    "errors",
    "partial",
    "Docstring и header не являются исчерпывающим throws/error contract; вызов не выполнялся.",
    "errors",
    observedApi.doc,
    apiInput,
  );
  add(
    api,
    "formula_origin",
    "not_applicable",
    "Авторский контекст: lookup provenance не задаёт физическую формулу.",
    "formula-origin",
  );
  add(
    api,
    "value_origin",
    "not_applicable",
    "Физическое происхождение численного значения к этому lookup не применяется; фактический возвращённый identifier не задан.",
    "value-origin",
  );
  add(
    api,
    "assigning_origin",
    "partial",
    "Статическое документированное правило относится к recorded assigning history; фактическая history отсутствует. Полная causal chain не восстановлена.",
    "assigning-origin",
    observedApi.doc,
    apiInput,
  );
  add(
    api,
    "effective_origin",
    "unknown",
    "Retained run/execution context отсутствует; effective origin неизвестен.",
    "effective-origin",
  );

  const constraint = observedSchema.constraint;
  const declaredDefault = observedSchema.declaration;
  literal(
    leaf,
    "signature",
    "schema-type",
    constraint.reason ? constraint : { value: "integer", selector: constraint.selector + "/type" },
    schemaInput,
    "Объявленный тип owning schema",
  );
  literal(
    leaf,
    "signature",
    "typed-field",
    observedTyped.reason
      ? observedTyped
      : { value: "energy_chunk::Int", selector: observedTyped.selector },
    coreInput,
    "Текстовая Int field declaration; не runtime inventory",
    "partial",
  );
  // Copy owning description; scheduling interpretation is explicitly authored.
  if (!observedSchema.description.reason) {
    add(
      leaf,
      "units",
      "known",
      "Owning schema description (source declaration): " + String(observedSchema.description.value),
      "units",
      observedSchema.description,
      schemaInput,
      "literal-extraction",
    );
  } else {
    add(
      leaf,
      "units",
      "unknown",
      observedSchema.description.reason === "description_absent"
        ? "В распознанном direct leaf description не объявлено; физические единицы из имени не выводятся."
        : `Owning description не извлечено (${observedSchema.description.reason}); физические единицы из имени не выводятся.`,
      "units",
      observedSchema.description,
      schemaInput,
    );
  }
  literal(
    leaf,
    "default",
    "schema-default",
    declaredDefault,
    schemaInput,
    !declaredDefault.reason && declaredDefault.value === null
      ? "В распознанном direct leaf нет own default keyword; это не runtime assignment"
      : "Default в schema context; декларация не применяется к конфигурации",
    declaredDefault.value === null ? "not_assigned" : "known",
  );
  literal(
    leaf,
    "default",
    "typed-default",
    observedTyped,
    coreInput,
    "Отдельная текстовая default declaration ProductionOptions",
  );
  literal(
    leaf,
    "default",
    "example-explicit",
    observedExample,
    exampleInput,
    "Отдельное явное значение illustrative base fixture; не default",
  );
  literal(
    leaf,
    "constraint",
    "schema-constraint",
    constraint,
    schemaInput,
    "Прямые type/minimum/required декларации owning schema; не полный validator",
  );
  if (!constraint.reason) {
    leaf.facts[leaf.facts.length - 1].sources.push(
      ...sourceRef(schemaInput, observedSchema.productionRequired.selector),
    );
  }
  literal(
    leaf,
    "constraint",
    "root-production-required",
    observedSchema.rootRequired,
    schemaInput,
    "Root required-production membership",
  );
  add(
    leaf,
    "constraint",
    "partial",
    observedSchema.validationCoverage.reason
      ? `Selected schema context не распознан (${observedSchema.validationCoverage.reason}); полная validation не выполнялась.`
      : "Авторский контекст: извлечены прямые selected declarations и scope root properties; root conditional predicates и полный validator не вычислялись. Footprint: " +
        JSON.stringify(observedSchema.validationCoverage.value),
    "schema-validation-coverage",
    observedSchema.validationCoverage,
    schemaInput,
    observedSchema.validationCoverage.reason ? "dynamic-unknown" : "authored-context",
  );
  add(
    leaf,
    "effects",
    observedSchema.description.reason ? "unknown" : "partial",
    observedSchema.description.reason
      ? `Owning description не извлечено (${observedSchema.description.reason}); полный effect inventory неизвестен.`
      : "Авторский контекст: параметр планирования energy-node work; этот adapter не меняет сетку/физическую модель и не исполняет scheduling. Owning description приведено отдельно; полный effect inventory не установлен.",
    "effects",
    observedSchema.description,
    schemaInput,
    observedSchema.description.reason ? "dynamic-unknown" : "authored-context",
  );
  add(
    leaf,
    "errors",
    "partial",
    "Прямые schema declarations не являются полным loader error inventory. Core guard/body не интерпретируются; runtime exception path не проверен.",
    "errors",
    { value: null, selector: "file" },
    coreInput,
  );
  add(
    leaf,
    "formula_origin",
    observedSchema.description.reason ? "unknown" : "not_applicable",
    observedSchema.description.reason
      ? `Owning description не извлечено (${observedSchema.description.reason}); formula origin неизвестен.`
      : "Авторский контекст: scheduling count не предоставляет физическую формулу; формула NEGF или rationale допуска не генерируются.",
    "formula-origin",
    observedSchema.description,
    schemaInput,
    observedSchema.description.reason ? "dynamic-unknown" : "authored-context",
  );
  add(
    leaf,
    "value_origin",
    "partial",
    "Schema, typed declaration и явный example — отдельные source contexts. Actual instance numeric origin неизвестен; совпадение чисел не является provenance.",
    "value-origin",
  );
  // Only authored excerpts are copied; fenced configuration/inspection code is not run.
  const route = routeInput.text;
  const marker = route?.indexOf("## Recorded assignments and value origins") ?? -1;
  const next = route && marker >= 0 ? route.indexOf("\n\n", marker) : -1;
  const paragraphStart = next >= 0 ? next + 2 : -1;
  const paragraphEnd = route && paragraphStart >= 0 ? route.indexOf("\n\n", paragraphStart) : -1;
  const excerpt = route && paragraphStart >= 0 && paragraphEnd >= 0
    ? route.slice(paragraphStart, paragraphEnd)
    : null;
  const routeObservation: Observation = route === null
    ? missing("configuration-route")
    : excerpt
    ? { value: excerpt, selector: `configuration-route:L${lines(route, paragraphStart)}` }
    : failed("configuration-route", "authored_excerpt_unavailable");
  add(
    leaf,
    "assigning_origin",
    "partial",
    excerpt
      ? "Авторский контекст из owning route; actual assigning history отсутствует:\n" + excerpt
      : "Actual assigning identifier неизвестен: source files, generated policy и effective ExecutionPlan не восстановлены из defaults или example.",
    "assigning-origin",
    routeObservation,
    routeInput,
    excerpt ? "authored-context" : "dynamic-unknown",
  );
  if (route !== null) {
    // These are literal authored paragraphs, never results of a merge/planner.
    const paragraphs = route.split(/\n\s*\n/);
    for (
      const [context, matches] of [
        ["synthetic-override-example", (p: string) =>
          /energy_chunk/.test(p) &&
          /fixture expectations|Synthetic example:|synthetic source example/.test(p)],
        ["authored-planner-policy", (p: string) => /application:auto_exact/.test(p)],
      ] as const
    ) {
      const candidates = paragraphs.filter(matches);
      if (candidates.length === 1) {
        const paragraph = candidates[0];
        add(
          leaf,
          "assigning_origin",
          "partial",
          "Цитата owning route; синтетическое/статическое объяснение, не результат выполнения:\n" +
            paragraph,
          context,
          {
            value: paragraph,
            selector: `configuration-route:L${lines(route, route.indexOf(paragraph))}`,
          },
          routeInput,
          "authored-context",
        );
      }
    }
  }
  add(
    leaf,
    "effective_origin",
    "unknown",
    "Effective configuration/ExecutionPlan/snapshot отсутствуют; origin не выводится из literal defaults, примера или application:auto_exact marker.",
    "effective-origin",
  );

  const facts = {
    format: TOOL,
    profile: PROFILE,
    source_manifest_sha256: manifestHash,
    subjects: [api, leaf],
    coverage: { fact_classes: CLASSES, scope: "fixed-slice", status: "partial" },
    binding: { status: "source-prototype", application_release: null, run: null },
  };
  const receipt = {
    tool: TOOL,
    profile: PROFILE,
    source_graph_sha256: graph,
    source_manifest_sha256: manifestHash,
    external_binding:
      "Receipt hashes verify supplied bytes only; external source preparation must prove commit-to-bytes binding.",
    lexical_normalization:
      "UTF-8 strict; CRLF/CR normalized to LF for extraction; hashes use raw bytes",
    inputs: inputs.map(({ text: _text, sha256, bytes: expectedBytes, ...input }) => ({
      ...input,
      expected_sha256: sha256,
      expected_bytes: expectedBytes,
    })),
    extractions,
    diagnostics,
    aggregate_source_bytes: inputs.reduce((sum, input) => sum + (input.actual_bytes ?? 0), 0),
    result: "partial" as const,
  };
  return { facts, receipt };
}

export type SliceOptions = { snapshotDir: string; sourceReceiptPath: string; outDir: string };
export type SliceResult = { status: "produced" | "partial" | "refused"; reason?: string };
export async function generateStaticSlice(options: SliceOptions): Promise<SliceResult> {
  try {
    const snapshot = absolute(options.snapshotDir);
    const sourceReceipt = absolute(options.sourceReceiptPath);
    const out = absolute(options.outDir);
    if (
      snapshot === "/" || out === "/" || within(out, snapshot) || within(snapshot, out) ||
      within(sourceReceipt, out)
    ) refuse("source_output_overlap");
    await realDirectory(snapshot);
    const receiptInfo = await Deno.lstat(sourceReceipt);
    if (
      receiptInfo.isSymlink || !receiptInfo.isFile ||
      await Deno.realPath(sourceReceipt) !== sourceReceipt
    ) refuse("symlink_or_invalid_receipt");
    const parent = out.slice(0, out.lastIndexOf("/")) || "/";
    await realDirectory(parent);
    if (await statMaybe(out)) refuse("output_not_fresh");
    const receiptBytes = await boundedRead(sourceReceipt, RECEIPT_CAP);
    const receiptText = strictText(receiptBytes);
    let parsed: { graph: string; files: InputEntry[] };
    try {
      parsed = inputEntries(parseData(receiptText));
    } catch (error) {
      if (error instanceof Unsupported) refuse("invalid_source_receipt");
      throw error;
    }
    const inputs: Input[] = [];
    let aggregate = 0;
    // Canonical fixed order, independent of supplied receipt entry ordering.
    for (const path of PATHS) {
      const expected = parsed.files.find((entry) => entry.path === path)!;
      if (!await selectedPath(snapshot, path)) {
        inputs.push({
          ...expected,
          actual_sha256: null,
          actual_bytes: null,
          status: "source_missing",
          text: null,
        });
        continue;
      }
      const fullPath = snapshot + "/" + path;
      const info = await Deno.lstat(fullPath);
      if (info.size > FILE_CAP || aggregate + info.size > SOURCE_CAP) {
        refuse("aggregate_source_cap");
      }
      const raw = await boundedRead(fullPath, FILE_CAP);
      const actualHash = await sha256(raw);
      if (raw.length !== expected.bytes || actualHash !== expected.sha256) {
        refuse("source_identity_mismatch");
      }
      aggregate += raw.length;
      inputs.push({
        ...expected,
        actual_sha256: actualHash,
        actual_bytes: raw.length,
        status: "verified",
        text: strictText(raw),
      });
    }
    const manifestHash = await sha256(receiptBytes);
    const built = buildProjection(inputs, parsed.graph, manifestHash);
    const factsText = json(built.facts);
    if (bytes(factsText) > OUTPUT_CAP) refuse("facts_output_cap");
    const receiptTextOut = json({
      ...built.receipt,
      output: {
        path: "facts.json",
        sha256: await sha256(encoder.encode(factsText)),
        bytes: bytes(factsText),
      },
    });
    if (bytes(receiptTextOut) > OUTPUT_CAP) refuse("receipt_output_cap");
    if (bytes(json(built.receipt.diagnostics)) > 8192) refuse("diagnostics_output_cap");
    // No output directory exists until all reads/projection/caps have passed.
    // createNew prevents clobbering a competing writer; filesystem atomicity
    // against adversarial concurrent namespace replacement is not certified.
    await Deno.mkdir(out);
    await Deno.writeTextFile(out + "/source-receipt.json", receiptTextOut, { createNew: true });
    // Stage a bounded file, retaining failed pending evidence if I/O fails.
    // Publish complete facts last, inside the fresh single-writer directory.
    await Deno.writeTextFile(out + "/facts.pending.json", factsText, { createNew: true });
    await Deno.rename(out + "/facts.pending.json", out + "/facts.json");
    return { status: "partial" };
  } catch (error) {
    if (error instanceof Refusal) return { status: "refused", reason: error.reason };
    if (error instanceof Unsupported) return { status: "refused", reason: error.reason };
    // Avoid leaking host/private paths from platform exceptions into artifacts.
    return { status: "refused", reason: "io_or_input_failure" };
  }
}

if (import.meta.main) {
  const flags = new Map<string, string>();
  const names = ["--snapshot", "--source-receipt", "--out"];
  let valid = Deno.args.length === 6;
  for (let i = 0; i < Deno.args.length && valid; i += 2) {
    const key = Deno.args[i], value = Deno.args[i + 1];
    if (!names.includes(key) || flags.has(key) || !value || value.startsWith("--")) valid = false;
    else flags.set(key, value);
  }
  const result = valid && flags.size === 3
    ? await generateStaticSlice({
      snapshotDir: flags.get("--snapshot")!,
      sourceReceiptPath: flags.get("--source-receipt")!,
      outDir: flags.get("--out")!,
    })
    : { status: "refused", reason: "invalid_options" };
  console.log(json(result).trimEnd());
  Deno.exitCode = result.status === "refused" ? 2 : 0;
}
