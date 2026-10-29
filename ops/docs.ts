// One ordinary cached documentation package; source/L is separate from native qualification.
import { pathToFileURL } from "node:url";
import { type Command, main, type RetainedResult, runRetained, workspace } from "./process.ts";
import { type GitReader, type SourceGraph, sourceGraph } from "./git.ts";
import { canonicalSourceGraphJson, depotNeedsInputs, prepareDepotMetadata } from "./solver.ts";
import { type DepotInputs, nixDataApplication, validateInputs } from "./depot_compatibility.ts";
function record(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
export type Owner = "core" | "runner" | "operator";
export interface Layout {
  root: string;
  attempt: string;
  owner: Owner;
  source: string;
  build: string;
}
function canonical(path: string): void {
  if (
    !path.startsWith("/") || path.endsWith("/") || path.includes("\\") ||
    path.split("/").slice(1).some((p) => !p || p === "." || p === "..") ||
    // Reject path NUL, C0 controls and DEL; preserve this exact security boundary.
    // deno-lint-ignore no-control-regex
    /[\x00-\x1f\x7f]/.test(path)
  ) throw new Error("noncanonical_absolute_path");
}
function contains(parent: string, child: string): boolean {
  return child === parent || child.startsWith(parent + "/");
}
export function checkLayout(value: Layout): void {
  for (const p of [value.root, value.attempt, value.source, value.build]) canonical(p);
  if (!["core", "runner", "operator"].includes(value.owner)) throw new Error("unknown_owner");
  if (
    contains(value.root, value.attempt) || contains(value.attempt, value.root) ||
    contains(value.source, value.build) || contains(value.build, value.source) ||
    value.source !== `${value.attempt}/stage/${value.owner}/src` ||
    value.build !== `${value.attempt}/raw/${value.owner}`
  ) throw new Error("invalid_owner_layout");
}
async function absent(path: string): Promise<void> {
  try {
    await Deno.lstat(path);
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) return;
    throw error;
  }
  throw new Error("existing_output_or_attempt");
}
async function ancestors(path: string, directory: boolean): Promise<void> {
  canonical(path);
  let cursor = path;
  while (cursor !== "/") {
    const info = await Deno.lstat(cursor);
    if (info.isSymlink || (cursor !== path && !info.isDirectory)) {
      throw new Error("symlink_or_invalid_ancestor");
    }
    cursor = cursor.slice(0, cursor.lastIndexOf("/")) || "/";
  }
  const info = await Deno.lstat(path);
  if (directory ? !info.isDirectory : !info.isFile) throw new Error("wrong_file_kind");
  if (await Deno.realPath(path) !== path) throw new Error("noncanonical_realpath");
}
export async function checkLayoutFiles(value: Layout): Promise<void> {
  checkLayout(value);
  for (const path of [value.root, value.attempt, value.source, `${value.attempt}/raw`]) {
    await ancestors(path, true);
  }
  await absent(value.build); // lstat rejects even dangling symlinks
  await ancestors(`${value.root}/julia/Project.toml`, false);
  await ancestors(`${value.root}/julia/Manifest.toml`, false);
}
export async function sha256(bytes: Uint8Array<ArrayBuffer>): Promise<string> {
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
  return Array.from(digest, (v) => v.toString(16).padStart(2, "0")).join("");
}
const OPERATOR_SHA = "8f05ff4cced8579b09cccd4b4315101e861e1896b87321b42e597374da79de49";
export async function operatorSources(recovery: Uint8Array<ArrayBuffer>, recipe: string) {
  if (await sha256(recovery) !== OPERATOR_SHA) throw new Error("operator_source_hash_mismatch");
  // Read only the exact, single-line recipe-owned quoted literal. This neither
  // evaluates Julia nor permits interpolation or arbitrary template expressions.
  const matches = [
    ...recipe.matchAll(/^const QCL_DOCS_OPERATOR_INDEX = ("(?:[^"\\\n]|\\[n"\\])*")$/gm),
  ];
  if (matches.length !== 1) throw new Error("operator_index_literal_unbound");
  const text: unknown = JSON.parse(matches[0][1]);
  if (typeof text !== "string" || text.includes("$") || !text.endsWith("\n")) {
    throw new Error("operator_index_literal_invalid");
  }
  const index = new TextEncoder().encode(text);
  return { recovery, index, recovery_sha256: OPERATOR_SHA, index_sha256: await sha256(index) };
}

export interface DocsPlan {
  format: "qcl-negf.docs-pilot-plan.v1";
  profile: "pilot-v1";
  slices: {
    id: string;
    owner: string;
    primary_sources: string[];
    section: string;
    primary_urls: string[];
  }[];
  source_inputs: string[];
  assets_lock: string;
  support_policy: "existing_owning_page_graphs";
  transform_policy: "documenter-1.17-light-self-v1";
  public_prefix: "/docs";
  limits: Record<string, number>;
  expected_primary_anchors: string[];
}
const docsLimits: Record<string, number> = {
  files: 10000,
  total_bytes: 268435456,
  file_bytes: 16777216,
  manifest_bytes: 2097152,
  fragment_bytes: 32768,
  help_view_bytes: 65536,
  tex_bytes: 16384,
  math_batch_bytes: 4194304,
  math_records: 10000,
  math_markup_bytes: 262144,
  math_total_markup_bytes: 33554432,
  math_css_bytes: 1048576,
  math_style_groups: 20000,
  math_batch_wall_seconds: 60,
};
function relativeDocsPath(value: unknown): value is string {
  return typeof value === "string" && /^[A-Za-z0-9_./#-]+$/.test(value) &&
    !value.startsWith("/") && value.split("/").every((v) => v && v !== "." && v !== "..");
}
export function parseDocsPlan(value: unknown): DocsPlan {
  if (
    !record(value) || value.format !== "qcl-negf.docs-pilot-plan.v1" ||
    value.profile !== "pilot-v1" || value.support_policy !== "existing_owning_page_graphs" ||
    value.transform_policy !== "documenter-1.17-light-self-v1" || value.public_prefix !== "/docs" ||
    value.assets_lock !== "ops/docs/assets.lock.json" || !record(value.limits)
  ) {
    throw new Error("invalid_docs_plan_policy");
  }
  if (
    Object.keys(value.limits).length !== Object.keys(docsLimits).length ||
    Object.entries(docsLimits).some(([key, cap]) => {
      const actual = (value.limits as Record<string, unknown>)[key];
      return !Number.isSafeInteger(actual) || (actual as number) <= 0 || (actual as number) > cap;
    })
  ) throw new Error("invalid_docs_plan_limits");
  const requiredInputs = [
    "julia/Project.toml",
    "julia/Manifest.toml",
    "components/QCLNEGF.jl/docs/make.jl",
    "components/QCLNEGFRunner.jl/docs/make.jl",
    "docs/public/make.jl",
    "docs/public/operator-recovery.md",
    "docs/capture-runtime-delivery.md",
    "docs/solver-build-receipt.md",
    "components/qcl-negf-contracts/src/qcl_negf_contracts/schemas/model-help.schema.json",
  ];
  if (
    !Array.isArray(value.source_inputs) || value.source_inputs.length !== requiredInputs.length ||
    !requiredInputs.every((path) => (value.source_inputs as unknown[]).includes(path))
  ) {
    throw new Error("invalid_docs_plan_source_inputs");
  }
  const anchors = [
    "researcher-scba-route",
    "researcher-final-route",
    "reader-api-routes",
    "developer-configuration-route",
    "operator-recovery-route",
    "operator-recovery",
  ];
  if (
    !Array.isArray(value.expected_primary_anchors) ||
    value.expected_primary_anchors.length !== anchors.length ||
    !anchors.every((anchor) => (value.expected_primary_anchors as unknown[]).includes(anchor))
  ) {
    throw new Error("invalid_docs_plan_coverage");
  }
  const owners = [["researcher", "core", "core"], ["developer", "runner", "runner"], [
    "operator",
    "root",
    "operator",
  ]];
  if (
    !Array.isArray(value.slices) || value.slices.length !== owners.length ||
    owners.some(([id, owner, section], index) => {
      const slice: unknown = (value.slices as unknown[])[index];
      return !record(slice) || slice.id !== id || slice.owner !== owner ||
        slice.section !== section ||
        !Array.isArray(slice.primary_sources) || !slice.primary_sources.length ||
        !slice.primary_sources.every(relativeDocsPath) ||
        !Array.isArray(slice.primary_urls) || !slice.primary_urls.length ||
        !slice.primary_urls.every((url) => relativeDocsPath(url) && url.startsWith(section + "/"));
    })
  ) throw new Error("invalid_docs_plan_journeys");
  return structuredClone(value) as unknown as DocsPlan;
}
// Selected public Markdown only; this is not an arbitrary Julia effect proof.
export async function scanDocsSources(roots: readonly string[]) {
  const files: FileBinding[] = [];
  let total = 0;
  for (const root of roots) {
    const entries = await inventoryTree(root, 5000 - files.length, 16777216 - total);
    for (const entry of entries) {
      const path = `${root}/${entry.path}`;
      if (/\.md$/i.test(entry.path)) {
        const data = await readRegularBounded(path, Math.min(2097152, 16777216 - total));
        if (await sha256(data) !== entry.sha256) throw new Error("docs_source_changed_during_scan");
        const text = new TextDecoder("utf-8", { fatal: true }).decode(data);
        if (/^[ \t]*(?:`{3,}|~{3,})[ \t]*@(example|eval|setup|repl)\b/m.test(text)) {
          throw new Error(`executable_docs_block: ${path}`);
        }
      }
      total += entry.bytes;
      files.push({ path, bytes: entry.bytes, sha256: entry.sha256 });
    }
  }
  return { files, executable_blocks: 0 as const, bytes: total };
}

export function parseDocsJson(text: string): unknown {
  const result: unknown = JSON.parse(text, (_key, value) => {
    if (typeof value === "number" && !Number.isFinite(value)) throw Error("nonfinite_json_number");
    return value;
  });
  let i = 0;
  const ws = () => {
    while (/\s/.test(text[i] ?? "") && i < text.length) i++;
  };
  const string = () => {
    const start = i++;
    while (i < text.length) {
      if (text[i] === "\\") {
        i += 2;
        continue;
      }
      if (text[i++] === '"') return JSON.parse(text.slice(start, i)) as string;
    }
    throw new Error("unterminated_json_string");
  };
  const value = (depth: number): void => {
    if (depth > 64) throw new Error("json_depth_limit");
    ws();
    if (text[i] === '"') {
      string();
      return;
    }
    if (text[i] === "{") {
      i++;
      ws();
      const keys = new Set<string>();
      if (text[i] === "}") {
        i++;
        return;
      }
      for (;;) {
        ws();
        if (text[i] !== '"') throw new Error("invalid_json_key");
        const key = string();
        if (keys.has(key)) throw new Error("duplicate_json_key");
        keys.add(key);
        ws();
        i++;
        value(depth + 1);
        ws();
        if (text[i++] === "}") break;
      }
    } else if (text[i] === "[") {
      i++;
      ws();
      if (text[i] === "]") {
        i++;
        return;
      }
      for (;;) {
        value(depth + 1);
        ws();
        if (text[i++] === "]") break;
      }
    } else {
      while (i < text.length && !/[\s,}\]]/.test(text[i])) i++;
    }
  };
  value(0);
  ws();
  if (i !== text.length) throw new Error("invalid_json_tail");
  return result;
}

// Bounded read-only inventory, rejecting internal symlinks and special files.
// This binds bytes only; effect/admission approval is deliberately separate.
export async function inventoryTree(root: string, maxFiles: number, maxBytes: number) {
  if (![maxFiles, maxBytes].every((n) => Number.isSafeInteger(n) && n > 0)) {
    throw new Error("invalid_inventory_limit");
  }
  let entries = 0;
  await ancestors(root, true);
  const files: { path: string; bytes: number; sha256: string }[] = [];
  let total = 0;
  async function walk(path: string, depth: number): Promise<void> {
    if (depth > 64) throw new Error("staging_depth_limit");
    for await (const entry of Deno.readDir(path)) {
      if (++entries > maxFiles) throw new Error("staging_entry_limit");
      const full = `${path}/${entry.name}`;
      const info = await Deno.lstat(full);
      if (info.isSymlink || (!info.isFile && !info.isDirectory)) {
        throw new Error("staging_special_entry");
      }
      if (info.isDirectory) await walk(full, depth + 1);
      else {
        if (files.length >= maxFiles || info.size > maxBytes - total) {
          throw new Error("staging_byte_limit");
        }
        const data = await readRegularBounded(full, maxBytes - total);
        if (data.length !== info.size) throw new Error("source_changed_during_read");
        total += data.length;
        files.push({
          path: full.slice(root.length + 1),
          bytes: data.length,
          sha256: await sha256(data),
        });
      }
    }
  }
  await walk(root, 0);
  return files.sort((a, b) => a.path.localeCompare(b.path));
}

export interface BoundedReader {
  read(buffer: Uint8Array): Promise<number | null>;
  close(): void;
}
// Actual bytes consumed are at most cap+1; one extra byte is an explicit overflow
// sentinel. Reuse one bounded buffer even for short reads. Every exit closes the
// owned reader. This is a byte bound, not an I/O deadline or race-proof snapshot.
export async function readBounded(reader: BoundedReader, cap: number, expectedSize: number) {
  try {
    if (
      !Number.isSafeInteger(cap) || cap < 0 || cap >= Number.MAX_SAFE_INTEGER ||
      !Number.isSafeInteger(expectedSize) || expectedSize < 0 || expectedSize > cap
    ) {
      throw new Error("invalid_read_limit_or_metadata");
    }
    const buffer = new Uint8Array(cap + 1);
    let actual = 0;
    while (actual <= cap) {
      const target = buffer.subarray(actual, Math.min(cap + 1, actual + 65536));
      const n = await reader.read(target);
      if (n === null) break;
      if (!Number.isSafeInteger(n) || n <= 0 || n > target.length) {
        throw new Error("invalid_reader_progress");
      }
      actual += n;
      if (actual > cap) throw new Error("input_byte_limit");
    }
    if (actual !== expectedSize) throw new Error("source_changed_during_read");
    return buffer.slice(0, actual);
  } finally {
    reader.close();
  }
}
async function readRegularBounded(path: string, cap: number) {
  await ancestors(path, false);
  const before = await Deno.lstat(path);
  if (!before.isFile || before.isSymlink) throw new Error("invalid_read_file_kind");
  const file = await Deno.open(path, { read: true });
  let owned = true;
  try {
    const opened = await file.stat(), current = await Deno.lstat(path);
    if (
      !opened.isFile || !current.isFile || current.isSymlink ||
      opened.dev !== before.dev || opened.ino !== before.ino ||
      current.dev !== before.dev || current.ino !== before.ino || opened.size !== before.size
    ) {
      throw new Error("source_metadata_changed");
    }
    // Metadata checks reject observed changes; they do not establish exclusivity
    // or eliminate filesystem races. The actual byte cap does not depend on stat.
    owned = false;
    const data = await readBounded(file, cap, opened.size);
    const after = await Deno.lstat(path);
    if (
      !after.isFile || after.isSymlink || after.dev !== before.dev || after.ino !== before.ino ||
      after.size !== before.size || after.mtime?.getTime() !== before.mtime?.getTime()
    ) {
      throw new Error("source_metadata_changed");
    }
    return data;
  } finally {
    if (owned) file.close();
  }
}
export interface FileBinding {
  path: string;
  bytes: number;
  sha256: string;
}

export interface FileRef {
  path: string;
  sha256: string;
}
export interface DocsRequest {
  format: "qcl-negf.docs-request.v1";
  depot_metadata: FileRef;
  asset_inputs: FileRef;
  review_inputs: FileRef;
  factory: { profile: "production-build" | "local-debug"; test_workers: number | null };
}
export interface CapturedDocsFile {
  ref: FileRef;
  raw: string;
}
export interface DocsRequestSnapshot {
  request: DocsRequest;
  raw_sha256: string;
  files: {
    depot_metadata: CapturedDocsFile;
    asset_inputs: CapturedDocsFile;
    review_inputs: CapturedDocsFile;
  };
}
export function exact(value: unknown, keys: string[]): asserts value is Record<string, unknown> {
  if (!record(value)) throw Error("expected_closed_object");
  const names = Reflect.ownKeys(value);
  if (
    names.length !== keys.length ||
    !names.every((k) => typeof k === "string" && keys.includes(k)) ||
    names.some((k) => !("value" in Object.getOwnPropertyDescriptor(value, k)!))
  ) {
    throw Error("unexpected_missing_or_accessor_field");
  }
}
export function parseDocsRequest(value: unknown): DocsRequest {
  exact(value, ["format", "depot_metadata", "asset_inputs", "review_inputs", "factory"]);
  if (value.format !== "qcl-negf.docs-request.v1") throw Error("unsupported_docs_request");
  for (const key of ["depot_metadata", "asset_inputs", "review_inputs"]) {
    const ref = value[key];
    exact(ref, ["path", "sha256"]);
    if (
      typeof ref.path !== "string" || typeof ref.sha256 !== "string" ||
      !/^[a-f0-9]{64}$/.test(ref.sha256)
    ) throw Error("invalid_file_ref");
    canonical(ref.path);
  }
  const f = value.factory;
  exact(f, ["profile", "test_workers"]);
  if (
    typeof f.profile !== "string" ||
    !["production-build", "local-debug"].includes(f.profile) ||
    !(f.test_workers === null ||
      Number.isSafeInteger(f.test_workers) && Number(f.test_workers) > 0) ||
    f.profile === "local-debug" && f.test_workers !== null && f.test_workers !== 2
  ) throw Error("invalid_factory_profile");
  return structuredClone(value) as unknown as DocsRequest;
}
export function parseDocsArgs(
  args: string[],
  configuredInputs?: string,
): { mode: "plan" | "prepare" | "build"; inputs: string } {
  const mode = args[0];
  if (mode !== "plan" && mode !== "prepare" && mode !== "build") {
    throw Error("expected_plan_prepare_or_build");
  }
  if (args.length !== 1 && (args.length !== 3 || args[1] !== "--inputs")) {
    throw Error("unknown_duplicate_or_missing_option");
  }
  const inputs = args.length === 3 ? args[2] : configuredInputs;
  if (!inputs) throw Error("missing_docs_inputs_prerequisite");
  canonical(inputs);
  return { mode, inputs };
}
export async function captureDocsFile(
  path: string,
  maximum = 2 * 1024 * 1024,
): Promise<CapturedDocsFile> {
  const bytes = await readRegularBounded(path, maximum);
  const raw = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  if (raw.startsWith("\uFEFF") || raw.includes("\0")) throw Error("invalid_docs_utf8_json");
  parseDocsJson(raw);
  return { ref: { path, sha256: await sha256(bytes) }, raw };
}
export async function captureDocsRequest(
  path: string,
  read = captureDocsFile,
): Promise<DocsRequestSnapshot> {
  const captured = structuredClone(await read(path, 65536));
  const request = parseDocsRequest(parseDocsJson(captured.raw));
  const files = {} as DocsRequestSnapshot["files"];
  for (const key of ["depot_metadata", "asset_inputs", "review_inputs"] as const) {
    const ref = request[key];
    // Readers receive only scalar path/cap, never retained comparison objects.
    const file = structuredClone(
      await read(ref.path, key === "depot_metadata" ? 65536 : 2 * 1024 * 1024),
    );
    if (file.ref.path !== ref.path || file.ref.sha256 !== ref.sha256) {
      throw Error("captured_input_hash_mismatch");
    }
    files[key] = file;
  }
  return { request, raw_sha256: captured.ref.sha256, files };
}
export function currentDocsSource(root: string, graph: SourceGraph): string {
  canonical(root);
  canonicalSourceGraphJson(graph);
  const url = pathToFileURL(root + "/");
  url.searchParams.set("rev", graph.revision);
  url.searchParams.set("submodules", "1");
  return "git+" + url.href;
}
export interface PackagePlan {
  mode: "plan" | "prepare" | "build";
  selected: SourceGraph;
  command: Command;
  inputs: string;
  inputs_sha256: string;
  pendingGates: string[];
}
export async function planDocsBuild(snapshot: DocsRequestSnapshot, graph: SourceGraph, context: {
  root: string;
  inputFile: string;
  manifestSha256: string;
  mode: PackagePlan["mode"];
  nix?: string;
  depotInputs?: DepotInputs;
}): Promise<PackagePlan> {
  // Validate before copying: structuredClone would otherwise discard symbol
  // fields and evaluate accessors, changing the closed input semantics.
  exact(snapshot, ["request", "raw_sha256", "files"]);
  parseDocsRequest(snapshot.request);
  if (typeof snapshot.raw_sha256 !== "string" || !/^[a-f0-9]{64}$/.test(snapshot.raw_sha256)) {
    throw Error("invalid_request_capture_hash");
  }
  exact(snapshot.files, ["depot_metadata", "asset_inputs", "review_inputs"]);
  for (const key of ["depot_metadata", "asset_inputs", "review_inputs"] as const) {
    const file = snapshot.files[key];
    exact(file, ["ref", "raw"]);
    exact(file.ref, ["path", "sha256"]);
    if (
      typeof file.raw !== "string" ||
      new TextEncoder().encode(file.raw).length >
        (key === "depot_metadata" ? 65536 : 2 * 1024 * 1024)
    ) throw Error("invalid_captured_docs_bytes");
    parseDocsJson(file.raw);
  }
  // Capture every borrowed comparison before the first async operation.
  const selected = JSON.parse(canonicalSourceGraphJson(graph)) as SourceGraph;
  const captured = structuredClone(snapshot), config = structuredClone(context);
  captured.request = parseDocsRequest(captured.request);
  for (const key of ["depot_metadata", "asset_inputs", "review_inputs"] as const) {
    const file = captured.files[key];
    if (
      file.ref.path !== captured.request[key].path ||
      file.ref.sha256 !== captured.request[key].sha256 ||
      await sha256(new TextEncoder().encode(file.raw)) !== file.ref.sha256
    ) throw Error("invalid_captured_docs_input");
  }
  canonical(config.inputFile);
  const metadata = await prepareDepotMetadata(
    captured.files.depot_metadata.raw,
    selected,
    config.manifestSha256,
    config.depotInputs,
  );
  const source = currentDocsSource(config.root, selected);
  const inputs = JSON.stringify({
    format: "qcl-negf.docs-package-inputs.v1",
    source,
    sources: selected,
    factory: captured.request.factory,
    depot_metadata_json: metadata.boundJson,
    depot_capture_json: captured.files.depot_metadata.raw,
    depot_capture_sha256: metadata.binding.captured_input_sha256,
    asset_inputs_json: captured.files.asset_inputs.raw,
    review_inputs_json: captured.files.review_inputs.raw,
  });
  const inputs_sha256 = await sha256(new TextEncoder().encode(inputs));
  const command: Command = {
    executable: config.nix ?? "nix",
    cwd: config.root,
    args: [
      "build",
      "--offline",
      "--impure",
      "--no-link",
      "--json",
      "--keep-failed",
      "--file",
      `${config.root}/nix/docs.nix`,
      "--argstr",
      "inputFile",
      config.inputFile,
      "--argstr",
      "inputSha256",
      inputs_sha256,
      "--argstr",
      "target",
      config.mode === "prepare" ? "inputs" : "docs",
    ],
  };
  return {
    mode: config.mode,
    selected,
    command,
    inputs,
    inputs_sha256,
    pendingGates: [
      "Native offline imports/full pages/assets/C1C2/cache/browser qualification is separate",
    ],
  };
}
export function parseDocsNixOutput(stdout: Uint8Array): string {
  const rows: unknown = parseDocsJson(new TextDecoder("utf-8", { fatal: true }).decode(stdout));
  if (
    !Array.isArray(rows) || rows.length !== 1 || !record(rows[0]) || !record(rows[0].outputs) ||
    Object.keys(rows[0].outputs).length !== 1 || typeof rows[0].outputs.out !== "string" ||
    !/^\/nix\/store\/[0-9abcdfghijklmnpqrsvwxyz]{32}-[A-Za-z0-9+._-]+$/.test(rows[0].outputs.out)
  ) throw Error("invalid_docs_nix_output");
  return rows[0].outputs.out;
}
export function commandCompleted(result: RetainedResult): boolean {
  const r = result.result;
  return r.reason === null && r.exit?.success === true && r.exit.code === 0 &&
    r.drain === "complete" &&
    r.retention === "acknowledged" && r.errors.length === 0 &&
    r.stdout_received_bytes === r.stdout_acknowledged_bytes &&
    r.stderr_received_bytes === r.stderr_acknowledged_bytes &&
    result.stdout.length === r.stdout_acknowledged_bytes &&
    result.stderr.length === r.stderr_acknowledged_bytes;
}
export async function runDocsBuild(plan: PackagePlan, deps: {
  readGraph: () => Promise<SourceGraph>;
  execute: (command: Command) => Promise<RetainedResult>;
  readBundle?: (path: string) => Promise<CapturedDocsFile>;
}) {
  const selected = structuredClone(plan);
  let dispatched = false;
  let retained: RetainedResult | null = null;
  try {
    if (
      canonicalSourceGraphJson(await deps.readGraph()) !==
        canonicalSourceGraphJson(selected.selected)
    ) throw Error("source_changed_before_dispatch");
    if (selected.mode === "plan") {
      return { state: "completed" as const, output: null, bundle_sha256: null, receipt: null };
    }
    dispatched = true;
    retained = structuredClone(await deps.execute(structuredClone(selected.command)));
    if (!commandCompleted(retained)) {
      return {
        state: retained.result.reason === "exit_failure" ? "failed" as const : "unknown" as const,
        output: null,
        bundle_sha256: null,
        receipt: retained.receipt,
      };
    }
    const output = parseDocsNixOutput(retained.stdout);
    let bundle_sha256: string | null = null;
    if (selected.mode === "build") {
      const bundle = await (deps.readBundle ?? captureDocsFile)(`${output}/public/bundle.json`);
      if (
        bundle.ref.path !== `${output}/public/bundle.json` ||
        await sha256(new TextEncoder().encode(bundle.raw)) !== bundle.ref.sha256
      ) throw Error("output_bundle_capture_mismatch");
      const document = parseDocsJson(bundle.raw);
      if (
        !record(document) || document.format !== "qcl-negf.docs-bundle.v1" ||
        canonicalSourceGraphJson(document.sources as SourceGraph) !==
          canonicalSourceGraphJson(selected.selected)
      ) throw Error("output_bundle_source_mismatch");
      bundle_sha256 = bundle.ref.sha256;
    }
    if (
      canonicalSourceGraphJson(await deps.readGraph()) !==
        canonicalSourceGraphJson(selected.selected)
    ) throw Error("source_changed_after_dispatch");
    return { state: "completed" as const, output, bundle_sha256, receipt: retained.receipt };
  } catch (error) {
    return {
      state: dispatched ? "unknown" as const : "failed" as const,
      output: null,
      bundle_sha256: null,
      receipt: retained?.receipt ?? null,
      error: String(error),
    };
  }
}
export function docsGitReader(directory: string, execute = runRetained): GitReader {
  let ordinal = 0;
  return async (root, args) => {
    const result = await execute({
      executable: "git",
      args: ["--no-optional-locks", "-C", root, ...args],
      clearEnv: true,
      env: { GIT_OPTIONAL_LOCKS: "0" },
    }, {
      directory: `${directory}/git-${++ordinal}`,
      limits: {
        wallMs: 30000,
        drainMs: 2000,
        streamBytes: 2 * 1024 * 1024,
        totalBytes: 4 * 1024 * 1024,
      },
    });
    if (!commandCompleted(result)) {
      throw Object.assign(Error("bounded_git_failed"), { receipt: result.receipt });
    }
    return new TextDecoder("utf-8", { fatal: true }).decode(result.stdout).trimEnd();
  };
}
export async function runDocsCli(args: string[]) {
  const options = parseDocsArgs(args, Deno.env.get("QCL_NEGF_DOCS_INPUTS"));
  const snapshot = await captureDocsRequest(options.inputs);
  const attempt = await Deno.makeTempDir({ prefix: "qcl-docs-cli-" });
  const read = docsGitReader(attempt);
  const graph = await sourceGraph(workspace, true, read);
  const manifestSha256 = await sha256(
    await readRegularBounded(`${workspace}/julia/Manifest.toml`, 16 * 1024 * 1024),
  );
  let depotInputs: DepotInputs | undefined;
  if (depotNeedsInputs(snapshot.files.depot_metadata.raw)) {
    const reply = await runRetained({
      executable: "nix",
      cwd: workspace,
      args: [
        "eval",
        "--offline",
        "--impure",
        "--json",
        "--file",
        `${workspace}/nix/depot-inputs.nix`,
        "--apply",
        nixDataApplication({
          source: currentDocsSource(workspace, graph),
          juliaTestProfile: snapshot.request.factory.profile,
          juliaTestWorkerLimit: snapshot.request.factory.test_workers,
        }),
      ],
    }, {
      directory: `${attempt}/dependency-inputs`,
      limits: {
        wallMs: 120000,
        drainMs: 2000,
        streamBytes: 2 * 1024 * 1024,
        totalBytes: 4 * 1024 * 1024,
      },
    });
    if (!commandCompleted(reply)) throw Error("current_depot_inputs_unavailable");
    const value = parseDocsJson(new TextDecoder("utf-8", { fatal: true }).decode(reply.stdout));
    validateInputs(value);
    depotInputs = value;
  }
  const plan = await planDocsBuild(snapshot, graph, {
    root: workspace,
    inputFile: `${attempt}/inputs.json`,
    manifestSha256,
    mode: options.mode,
    depotInputs,
  });
  if (options.mode === "plan") return plan;
  await Deno.writeTextFile(`${attempt}/inputs.json`, plan.inputs, { createNew: true, mode: 0o600 });
  return await runDocsBuild(plan, {
    readGraph: () => sourceGraph(workspace, true, read),
    execute: (command) =>
      runRetained(command, {
        directory: `${attempt}/realize`,
        limits: {
          wallMs: 24 * 60 * 60 * 1000,
          drainMs: 5000,
          streamBytes: 8 * 1024 * 1024,
          totalBytes: 16 * 1024 * 1024,
        },
      }),
  });
}
if (import.meta.main) {
  await main(async () => {
    const result = await runDocsCli(Deno.args);
    console.log(JSON.stringify(result, null, 2));
    if ("state" in result && result.state !== "completed") {
      throw Error("documentation_command_did_not_complete");
    }
  });
}
