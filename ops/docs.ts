// DOC04 source integration. No BUILD dispatch until owning admission/effect/
// assembly bindings exist. Paths and marker files never confer that authority.
import { workspace } from "./process.ts";
import { githubRepository, type GitReader, type SourceGraph, sourceGraph } from "./git.ts";

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

export function parseDocsArgs(args: string[]) {
  const mode = args[0];
  if (mode !== "preflight" && mode !== "build") throw new Error("expected_preflight_or_build");
  const options = new Map<string, string>();
  const allowed = mode === "build"
    ? ["--plan", "--attempt-directory", "--admission"]
    : ["--plan", "--attempt-directory"];
  for (let i = 1; i < args.length; i += 2) {
    const key = args[i], value = args[i + 1];
    if (!allowed.includes(key) || options.has(key) || !value || value.startsWith("--")) {
      throw new Error("unknown_duplicate_or_missing_option");
    }
    canonical(value);
    options.set(key, value);
  }
  if (allowed.some((key) => !options.has(key))) throw new Error("missing_required_option");
  return {
    mode,
    plan: options.get("--plan")!,
    attempt: options.get("--attempt-directory")!,
    admission: options.get("--admission") ?? null,
  };
}

// These are concrete unclosed source integrations, not caller-provided statuses.
// No marker/admission JSON can erase them. Replacing them needs owning APIs and
// reviewed technical bindings, not a --ready flag or receipt existence test.
export function buildBlockers(): string[] {
  return [
    "missing_admitted_assembly_entrypoint",
    "missing_bounded_source_graph_runner_binding",
    "missing_shared_schema_validation_binding",
    "unknown_nested_docstring_import_cache_edges",
    "missing_installed_documenter_toolchain_cache_binding",
    "missing_full_assets_license_runtime_css_binding",
    "missing_external_fresh_inventory_admission_binding",
    "missing_process_tree_resource_and_exclusivity_binding",
  ];
}

export interface Child {
  stdout: ReadableStream<Uint8Array>;
  stderr: ReadableStream<Uint8Array>;
  status: Promise<{ code: number; success: boolean }>;
  kill(): void;
}
interface Limits {
  wallMs: number;
  drainMs: number;
  streamBytes: number;
  totalBytes: number;
}
export interface FiniteResult {
  reason: string | null;
  exit: { code: number; success: boolean } | null;
  drain: "complete" | "incomplete";
  errors: string[];
  stdout_received_bytes: number;
  stderr_received_bytes: number;
  stdout_attempted_bytes: number;
  stderr_attempted_bytes: number;
  stdout_acknowledged_bytes: number;
  stderr_acknowledged_bytes: number;
  retention: "acknowledged" | "failed_unknown_partial" | "incomplete_unknown_partial";
  process_tree_terminated: null;
  resource_measurements: null;
}
// An injectable primitive for separately admitted fake-process controls. It is
// intentionally not a CPU/RAM/descendant sandbox and is not wired to BUILD.
export async function runFinite(
  spawn: () => Child,
  save: (stream: "stdout" | "stderr", bytes: Uint8Array, signal: AbortSignal) => Promise<void>,
  limits: Limits,
): Promise<FiniteResult> {
  for (const n of Object.values(limits)) {
    if (!Number.isSafeInteger(n) || n <= 0) throw new Error("invalid_finite_limit");
  }
  let reason: string | null = null;
  let total = 0;
  const completion: {
    exit: FiniteResult["exit"];
    drain: FiniteResult["drain"];
  } = { exit: null, drain: "complete" };
  const errors: string[] = [];
  let terminal = false;
  let sinkFailed = false;
  const cancellation = new AbortController();
  const child = spawn();
  const readers = [child.stdout.getReader(), child.stderr.getReader()];
  let signal!: () => void;
  const stopped = new Promise<void>((resolve) => {
    signal = resolve;
  });
  function stop(why: string) {
    if (terminal) return;
    if (!reason) {
      reason = why;
      signal();
    }
    try {
      child.kill();
    } catch {
      errors.push("kill_failed");
    }
  }
  const timer = setTimeout(() => stop("deadline"), limits.wallMs);
  const reserved = [0, 0], received = [0, 0], acknowledged = [0, 0];
  const drains = readers.map(async (reader, i) => {
    try {
      while (true) {
        const chunk = await reader.read();
        if (terminal) break;
        if (chunk.done) break;
        const size = chunk.value.byteLength;
        received[i] += size;
        const keep = Math.min(size, limits.streamBytes - reserved[i], limits.totalBytes - total);
        reserved[i] += keep;
        total += keep; // reservation is not retained-byte evidence
        if (keep < size) stop("log_cap");
        if (keep) {
          await save(
            i === 0 ? "stdout" : "stderr",
            chunk.value.subarray(0, keep),
            cancellation.signal,
          );
          if (terminal) break;
          acknowledged[i] += keep; // only a successful sink acknowledgement counts
        }
        if (keep < size) break;
      }
    } catch {
      if (!terminal) {
        sinkFailed = true;
        errors.push("drain_or_log_write_failed_unknown_partial");
        stop("drain_or_log_write_failed");
      }
    }
  });
  const status = child.status.then((value) => {
    if (!terminal) completion.exit = { ...value };
  }, () => {
    if (!terminal) {
      errors.push("status_failed");
      stop("status_failed");
    }
  });
  const complete = Promise.all([...drains, status]);
  await Promise.race([complete, stopped]);
  let drainTimer: ReturnType<typeof setTimeout> | undefined;
  try {
    await Promise.race([
      complete,
      new Promise<void>((resolve) => {
        drainTimer = setTimeout(() => {
          completion.drain = "incomplete";
          resolve();
        }, limits.drainMs);
      }),
    ]);
  } finally {
    clearTimeout(timer);
    clearTimeout(drainTimer);
    terminal = true;
    // Cancellation may itself hang; do not await it beyond the finite drain.
    if (completion.drain === "incomplete") {
      // Cooperative cancellation is requested, never assumed effective. A sink
      // may write later; the result records unknown partial retention and is a
      // detached snapshot, not a claim of immutable terminal log bytes.
      cancellation.abort();
      for (const reader of readers) reader.cancel().catch(() => {});
    }
  }
  const drain = completion.drain;
  const observedExit = completion.exit;
  if (!reason && observedExit && !observedExit.success) reason = "exit_failure";
  return {
    reason,
    exit: observedExit ? { ...observedExit } : null,
    drain,
    errors: [...errors],
    stdout_received_bytes: received[0],
    stderr_received_bytes: received[1],
    stdout_attempted_bytes: reserved[0],
    stderr_attempted_bytes: reserved[1],
    stdout_acknowledged_bytes: acknowledged[0],
    stderr_acknowledged_bytes: acknowledged[1],
    retention: drain === "incomplete"
      ? "incomplete_unknown_partial"
      : sinkFailed
      ? "failed_unknown_partial"
      : "acknowledged",
    process_tree_terminated: null,
    resource_measurements: null,
  };
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
async function boundedFile(path: string, cap: number) {
  const data = await readRegularBounded(path, cap);
  return { path, bytes: data.length, sha256: await sha256(data) };
}
export interface FileBinding {
  path: string;
  bytes: number;
  sha256: string;
}
export interface EvidenceRef {
  path: string;
  sha256: string | null;
}
export interface ObservationError {
  code: string;
  path: string | null;
  detail: string;
  evidence: readonly EvidenceRef[];
}
export type InputObservation =
  | { kind: "present"; actual: FileBinding; evidence: readonly EvidenceRef[] }
  | { kind: "absent"; path: string; evidence: readonly EvidenceRef[] }
  | { kind: "unreadable"; path: string; error: ObservationError };
export interface GitReadEvidence {
  ordinal: number;
  root: string;
  args: readonly string[];
  stdout: string;
  stdout_sha256: string;
  receipt: EvidenceRef;
}
export type GraphRead =
  | {
    kind: "complete";
    graph: SourceGraph;
    raw_json_sha256: string;
    git: readonly GitReadEvidence[];
  }
  | { kind: "rejected"; git: readonly GitReadEvidence[]; error: ObservationError };
export interface DocsObservation {
  start: GraphRead;
  inputs: readonly InputObservation[];
  end: GraphRead;
}
export interface ObservationDeps {
  readGit: GitReader;
  readInput: (path: string, cap: number) => Promise<InputObservation>;
  limits: { maxFiles: number; maxFileBytes: number; maxTotalBytes: number };
}
export interface DocsIdentity {
  graph: SourceGraph;
  inputs: readonly FileBinding[];
}
export type ChangeEvidence =
  | {
    kind: "file_changed";
    expected: FileBinding;
    actual: FileBinding;
    evidence: readonly EvidenceRef[];
  }
  | { kind: "file_absent"; expected: FileBinding; evidence: readonly EvidenceRef[] }
  | { kind: "graph_changed"; expected: SourceGraph; actual: SourceGraph }
  | { kind: "git_dirty"; root: string; actual_status: string; evidence: GitReadEvidence }
  | {
    kind: "git_revision_changed";
    root: string;
    expected_revision: string;
    actual_revision: string;
    evidence: GitReadEvidence;
  }
  | { kind: "graph_changed_during_observation"; start: SourceGraph; end: SourceGraph };
export interface Matched {
  kind: "matched";
  observation: DocsObservation;
  actual: DocsIdentity;
}
export interface ObservedChanged {
  kind: "observed_changed";
  observation: DocsObservation;
  changes: readonly [ChangeEvidence, ...ChangeEvidence[]];
  unknowns: readonly ObservationError[];
}
export interface UnreadableUnknown {
  kind: "unreadable_unknown";
  observation: DocsObservation;
  unknowns: readonly [ObservationError, ...ObservationError[]];
}
export type Comparison = Matched | ObservedChanged | UnreadableUnknown;
export type ExpectedPreparation =
  | { kind: "expected_ready"; expected: DocsIdentity }
  | {
    kind: "expected_invalid";
    observation: DocsObservation;
    changes: readonly ChangeEvidence[];
    unknowns: readonly ObservationError[];
  };
export type Operation<T> = { kind: "completed"; value: T } | {
  kind: "failed" | "unknown_partial";
  error: string;
};
type FailureOperation = Extract<Operation<never>, { error: string }>;
interface CommonResult {
  expected: DocsIdentity;
  candidate: null;
}
export type ScopedIdentityResult<T> =
  & CommonResult
  & (
    | {
      state: "blocked_before";
      before: ObservedChanged | UnreadableUnknown;
      operation: null;
      after: null;
    }
    | {
      state: "completed_bound";
      before: Matched;
      after: Matched;
      operation: Extract<Operation<T>, { kind: "completed" }>;
    }
    | { state: "failed_bound"; before: Matched; after: Matched; operation: FailureOperation }
    | {
      state: "failed_source_changed";
      before: Matched;
      after: ObservedChanged;
      operation: Operation<T>;
    }
    | {
      state: "failed_identity_unknown";
      before: Matched;
      after: UnreadableUnknown;
      operation: Operation<T>;
    }
  );
function observationError(code: string, path: string | null, detail: unknown): ObservationError {
  return { code, path, detail: String(detail), evidence: [] };
}
const gitLimitKeys = [
  "wallMs",
  "drainMs",
  "streamBytes",
  "totalBytes",
  "maxCommands",
  "maxTotalBytes",
  "totalWallMs",
] as const;
const inputLimitKeys = ["maxFiles", "maxFileBytes", "maxTotalBytes"] as const;
function positiveLimits(value: unknown, keys: readonly string[]): void {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Error("invalid_limits");
  }
  const own = Reflect.ownKeys(value);
  if (
    own.length !== keys.length || own.some((key) => typeof key !== "string" || !keys.includes(key))
  ) throw new Error("invalid_limits");
  const descriptors = Object.getOwnPropertyDescriptors(value);
  if (
    keys.some((key) => {
      const field = descriptors[key];
      return !field || !field.enumerable || !("value" in field) ||
        typeof field.value !== "number" ||
        !Number.isSafeInteger(field.value) || field.value <= 0 ||
        field.value >= Number.MAX_SAFE_INTEGER;
    })
  ) throw new Error("invalid_limits");
}
const hex = /^[a-f0-9]{64}$/;
function validBinding(value: FileBinding): boolean {
  try {
    canonical(value.path);
  } catch {
    return false;
  }
  return Number.isSafeInteger(value.bytes) && value.bytes >= 0 && hex.test(value.sha256);
}
function validInputs(inputs: readonly FileBinding[]): boolean {
  return Array.isArray(inputs) && inputs.every(validBinding) &&
    new Set(inputs.map((i) => i.path)).size === inputs.length;
}
function privateGraph(graph: SourceGraph): SourceGraph {
  if (
    graph.format !== "qcl-negf.git-graph.v1" || !/^[a-f0-9]{40}$/.test(graph.revision) ||
    !Array.isArray(graph.components) || !graph.components.length
  ) throw new Error("invalid_graph");
  const seen = new Set<string>();
  const components = graph.components.map((item) => {
    if (
      !/^components\/[A-Za-z0-9][A-Za-z0-9.-]*$/.test(item.path) ||
      !/^[a-f0-9]{40}$/.test(item.revision) || seen.has(item.path)
    ) throw new Error("invalid_graph_component");
    seen.add(item.path);
    githubRepository(item.url);
    return { path: item.path, revision: item.revision, url: item.url };
  }).sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
  return { format: graph.format, revision: graph.revision, components };
}
export function docsIdentityProjection(identity: DocsIdentity): DocsIdentity {
  if (!validInputs(identity.inputs)) throw new Error("invalid_input_manifest");
  return {
    graph: privateGraph(identity.graph),
    inputs: identity.inputs.map((i) => ({
      path: i.path,
      bytes: i.bytes,
      sha256: i.sha256,
    })).sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0),
  };
}
export function docsIdentityDigest(identity: DocsIdentity): Promise<string> {
  return new Promise<string>((resolve) =>
    resolve(sha256(new TextEncoder().encode(JSON.stringify(docsIdentityProjection(identity)))))
  );
}

export interface GitLimits {
  wallMs: number;
  drainMs: number;
  streamBytes: number;
  totalBytes: number;
  maxCommands: number;
  maxTotalBytes: number;
  totalWallMs: number;
}
export interface GitCall {
  executable: string;
  args: string[];
  cwd: string;
  env: Record<string, string>;
  clearEnv: true;
  tag: { attempt: string; ordinal: number };
  limits: Limits;
}
export interface GitReply {
  stdout: Uint8Array;
  result: FiniteResult;
  receipt: EvidenceRef;
}
export type GitTransport = (call: GitCall) => Promise<GitReply>;
// Code dependencies only. No production spawn, filesystem writer or CLI binding.
export type GitAccounting =
  | {
    kind: "unknown";
    admission: "closed";
    retention: "unknown";
    observed_stdout_bytes: number | null;
    received_bytes: null;
  }
  | {
    kind: "known";
    admission: "open" | "closed";
    retention: FiniteResult["retention"];
    observed_stdout_bytes: number;
    received_bytes: number;
  };
export class GitObservationError extends Error {
  constructor(
    public code: string,
    public tag: { attempt: string; ordinal: number },
    detail: unknown,
    public receipt: EvidenceRef | null = null,
    public accounting: GitAccounting | null = null,
  ) {
    super(String(detail));
  }
}
function record(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
// Unknown transport data is inspected only through own data descriptors.
// These bounded field lists are the finite Git reply contract, not a generic serializer.
function ownData(value: unknown, key: string): unknown {
  if (typeof value !== "object" || value === null) throw new Error("invalid_data_object");
  const descriptor = Object.getOwnPropertyDescriptor(value, key);
  if (!descriptor || !("value" in descriptor)) throw new Error("missing_or_accessor_field");
  return descriptor.value;
}
function fields(value: unknown, keys: readonly string[]): Record<string, unknown> {
  const copy: Record<string, unknown> = {};
  for (const key of keys) copy[key] = ownData(value, key);
  return copy;
}
function receiptFrom(value: unknown): EvidenceRef | null {
  try {
    const receipt = fields(ownData(value, "receipt"), ["path", "sha256"]);
    if (
      typeof receipt.path !== "string" || (receipt.sha256 !== null &&
        (typeof receipt.sha256 !== "string" || !hex.test(receipt.sha256)))
    ) return null;
    canonical(receipt.path);
    return { path: receipt.path, sha256: receipt.sha256 };
  } catch {
    return null;
  }
}
const typedArrayLength = Object.getOwnPropertyDescriptor(
  Object.getPrototypeOf(Uint8Array.prototype),
  "length",
)!.get!;
function stdoutLength(value: unknown): number | null {
  try {
    const stdout = ownData(value, "stdout");
    return ArrayBuffer.isView(stdout) && stdout instanceof Uint8Array
      ? typedArrayLength.call(stdout)
      : null;
  } catch {
    return null;
  }
}
function safeFailureDetail(error: unknown): string {
  if (typeof error === "string") return error;
  try {
    const message = ownData(error, "message");
    if (typeof message === "string") return message;
  } catch { /* unknown */ }
  return "transport or descriptor introspection failed";
}
function snapshotGitReply(value: unknown, stdoutCap: number): GitReply {
  const length = stdoutLength(value);
  if (length === null || length > stdoutCap) throw new Error("invalid_stdout_or_bound");
  const stdout = new Uint8Array(length);
  Uint8Array.prototype.set.call(stdout, ownData(value, "stdout") as Uint8Array);
  const r = fields(ownData(value, "result"), [
    "reason",
    "exit",
    "drain",
    "errors",
    "retention",
    "stdout_received_bytes",
    "stdout_attempted_bytes",
    "stdout_acknowledged_bytes",
    "stderr_received_bytes",
    "stderr_attempted_bytes",
    "stderr_acknowledged_bytes",
    "process_tree_terminated",
    "resource_measurements",
  ]);
  if (r.exit !== null) r.exit = fields(r.exit, ["code", "success"]);
  if (!Array.isArray(r.errors)) throw new Error("invalid_errors");
  const count = ownData(r.errors, "length");
  if (typeof count !== "number" || !Number.isSafeInteger(count) || count < 0 || count > 1024) {
    throw new Error("invalid_errors_bound");
  }
  const errors: string[] = [];
  let errorChars = 0;
  for (let i = 0; i < count; i++) {
    const error = ownData(r.errors, String(i));
    if (typeof error !== "string") throw new Error("invalid_error_entry");
    errorChars += error.length;
    if (errorChars > stdoutCap) throw new Error("invalid_error_text_bound");
    errors.push(error);
  }
  r.errors = errors;
  const receipt = receiptFrom(value);
  if (!receipt) throw new Error("invalid_receipt");
  return { stdout, result: r as unknown as FiniteResult, receipt };
}
function validGitReply(value: unknown): value is GitReply {
  if (
    !record(value) || !(value.stdout instanceof Uint8Array) || !record(value.result) ||
    !receiptFrom(value)
  ) return false;
  const r = value.result;
  if (
    (r.reason !== null && typeof r.reason !== "string") ||
    (r.drain !== "complete" && r.drain !== "incomplete") ||
    !["acknowledged", "failed_unknown_partial", "incomplete_unknown_partial"].includes(
      r.retention as string,
    ) ||
    !Array.isArray(r.errors) || !r.errors.every((error) => typeof error === "string") ||
    r.process_tree_terminated !== null || r.resource_measurements !== null
  ) return false;
  if (
    r.exit !== null && (!record(r.exit) || !Number.isSafeInteger(r.exit.code) ||
      (r.exit.code as number) < 0 || typeof r.exit.success !== "boolean")
  ) return false;
  const counters = [
    "stdout_received_bytes",
    "stdout_attempted_bytes",
    "stdout_acknowledged_bytes",
    "stderr_received_bytes",
    "stderr_attempted_bytes",
    "stderr_acknowledged_bytes",
  ] as const;
  if (
    counters.some((key) =>
      typeof r[key] !== "number" || !Number.isSafeInteger(r[key]) || (r[key] as number) < 0
    )
  ) return false;
  const n = r as unknown as FiniteResult;
  if (
    !Number.isSafeInteger(n.stdout_received_bytes + n.stderr_received_bytes) ||
    n.stdout_acknowledged_bytes > n.stdout_attempted_bytes ||
    n.stdout_attempted_bytes > n.stdout_received_bytes ||
    n.stderr_acknowledged_bytes > n.stderr_attempted_bytes ||
    n.stderr_attempted_bytes > n.stderr_received_bytes ||
    value.stdout.length !== n.stdout_acknowledged_bytes
  ) return false;
  const successClaim = n.exit?.code === 0 && n.exit.success && n.reason === null &&
    n.drain === "complete" && n.retention === "acknowledged" && n.errors.length === 0;
  return !successClaim || (n.stdout_received_bytes === n.stdout_attempted_bytes &&
    n.stdout_received_bytes === n.stdout_acknowledged_bytes &&
    n.stderr_received_bytes === n.stderr_attempted_bytes &&
    n.stderr_received_bytes === n.stderr_acknowledged_bytes);
}
const readerEvidence = new WeakMap<
  GitReader,
  { ordinal: number; receipt: EvidenceRef; stdout: string }
>();
export function makeDocsGitReader(options: {
  root: string;
  attempt: string;
  gitExecutable: string;
  limits: GitLimits;
  invoke: GitTransport;
}): GitReader {
  canonical(options.root);
  canonical(options.attempt);
  canonical(options.gitExecutable);
  positiveLimits(options.limits, gitLimitKeys);
  const limits = { ...options.limits }, root = options.root, attempt = options.attempt;
  const invoke = options.invoke, executable = options.gitExecutable;
  const deadline = performance.now() + limits.totalWallMs;
  let ordinal = 0, bytes = 0, admissionClosed = false;
  const reader: GitReader = async (cwd, argv) => {
    const isRoot = cwd === root;
    if (
      !isRoot &&
      !new RegExp(
        "^" + root.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
          "/components/[A-Za-z0-9][A-Za-z0-9.-]*$",
      ).test(cwd)
    ) {
      throw new Error("invalid_git_root");
    }
    const args = [...argv];
    const fixed = [["rev-parse", "HEAD"], ["status", "--porcelain"], ["ls-tree", "-rz", "HEAD"]];
    const config = isRoot &&
      ((JSON.stringify(args) ===
        JSON.stringify([
          "config",
          "-f",
          ".gitmodules",
          "--get-regexp",
          "^submodule\\..*\\.path$",
        ])) ||
        (args.length === 5 && args[0] === "config" && args[1] === "-f" &&
          args[2] === ".gitmodules" && args[3] === "--get" &&
          // Reject C0 controls and spaces in the Git config field; preserve the exact gate.
          // deno-lint-ignore no-control-regex
          /^submodule\.[^\x00-\x20]+\.url$/.test(args[4])));
    if (!config && !fixed.some((a) => JSON.stringify(a) === JSON.stringify(args))) {
      throw new Error("invalid_git_argv");
    }
    const remaining = deadline - performance.now();
    if (
      admissionClosed || ordinal >= limits.maxCommands || bytes >= limits.maxTotalBytes ||
      remaining <= 0
    ) {
      throw new GitObservationError(
        "budget_exhausted",
        { attempt, ordinal },
        "aggregate admission closed or exhausted",
      );
    }
    const totalBytes = Math.min(limits.totalBytes, limits.maxTotalBytes - bytes);
    const call: GitCall = {
      executable,
      cwd,
      args: [
        "--no-pager",
        "--no-optional-locks",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "core.untrackedCache=false",
        "-C",
        cwd,
        ...args,
      ],
      clearEnv: true,
      env: {
        GIT_OPTIONAL_LOCKS: "0",
        GIT_CONFIG_NOSYSTEM: "1",
        GIT_CONFIG_GLOBAL: "/dev/null",
        GIT_TERMINAL_PROMPT: "0",
        LC_ALL: "C",
      },
      tag: { attempt, ordinal: ++ordinal },
      limits: {
        wallMs: Math.min(limits.wallMs, Math.max(1, Math.floor(remaining))),
        drainMs: Math.min(limits.drainMs, Math.max(1, Math.floor(remaining))),
        streamBytes: Math.min(limits.streamBytes, totalBytes),
        totalBytes,
      },
    };
    readerEvidence.delete(reader);
    let raw: unknown;
    try {
      raw = await invoke(call);
    } // Trusted finite transport owns raw retention, including failure.
    catch (error) {
      admissionClosed = true; // Unknown physical consumption is not a measured maxTotalBytes debit.
      throw new GitObservationError(
        "transport_failed",
        call.tag,
        safeFailureDetail(error),
        receiptFrom(error),
        {
          kind: "unknown",
          admission: "closed",
          retention: "unknown",
          observed_stdout_bytes: null,
          received_bytes: null,
        },
      );
    }
    // Snapshot and validation share one failure boundary. No unknown accessors run.
    let reply: GitReply;
    try {
      reply = snapshotGitReply(raw, call.limits.streamBytes);
      if (!validGitReply(reply)) throw new Error("invalid_reply_shape_or_counters");
    } catch (error) {
      admissionClosed = true;
      const observed = stdoutLength(raw);
      throw new GitObservationError(
        "invalid_reply",
        call.tag,
        safeFailureDetail(error),
        receiptFrom(raw),
        {
          kind: "unknown",
          admission: "closed",
          retention: "unknown",
          observed_stdout_bytes: observed,
          received_bytes: null,
        },
      );
    }
    const r = reply.result;
    bytes += r.stdout_received_bytes + r.stderr_received_bytes;
    const accounting: GitAccounting = {
      kind: "known",
      admission: bytes >= limits.maxTotalBytes ? "closed" : "open",
      retention: r.retention,
      observed_stdout_bytes: reply.stdout.length,
      received_bytes: r.stdout_received_bytes + r.stderr_received_bytes,
    };
    if (
      performance.now() > deadline || bytes > limits.maxTotalBytes ||
      r.stdout_received_bytes > call.limits.streamBytes ||
      r.stderr_received_bytes > call.limits.streamBytes ||
      r.stdout_received_bytes + r.stderr_received_bytes > call.limits.totalBytes ||
      !r.exit || r.exit.code !== 0 || !r.exit.success || r.reason !== null ||
      r.drain !== "complete" ||
      r.retention !== "acknowledged" || r.errors.length !== 0 ||
      r.stdout_received_bytes !== r.stdout_attempted_bytes ||
      r.stdout_received_bytes !== r.stdout_acknowledged_bytes ||
      r.stderr_received_bytes !== r.stderr_attempted_bytes ||
      r.stderr_received_bytes !== r.stderr_acknowledged_bytes ||
      reply.stdout.length !== r.stdout_acknowledged_bytes
    ) {
      throw new GitObservationError(
        r.reason ?? "git_transport_failed",
        call.tag,
        JSON.stringify(r),
        reply.receipt,
        accounting,
      );
    }
    canonical(reply.receipt.path);
    if (reply.receipt.sha256 !== null && !hex.test(reply.receipt.sha256)) {
      throw new Error("invalid_receipt");
    }
    let stdout: string;
    try {
      stdout = new TextDecoder("utf-8", { fatal: true }).decode(reply.stdout);
    } catch (error) {
      throw new GitObservationError("invalid_utf8", call.tag, error, reply.receipt);
    }
    readerEvidence.set(reader, { ordinal, receipt: { ...reply.receipt }, stdout });
    return stdout.trimEnd();
  };
  return reader;
}

export async function observeDocsInput(path: string, cap: number): Promise<InputObservation> {
  try {
    return { kind: "present", actual: await boundedFile(path, cap), evidence: [] };
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) return { kind: "absent", path, evidence: [] };
    return { kind: "unreadable", path, error: observationError("input_unreadable", path, error) };
  }
}
const observedByCode = new WeakSet<DocsObservation>();
const trustedExpected = new WeakSet<DocsIdentity>();
const inputBudget = new WeakMap<GitReader, { used: number; limits: string }>();
export async function observeDocsSources(
  root: string,
  paths: readonly string[],
  deps: ObservationDeps,
): Promise<DocsObservation> {
  canonical(root);
  positiveLimits(deps.limits, inputLimitKeys);
  for (const path of paths) canonical(path);
  if (new Set(paths).size !== paths.length || paths.length > deps.limits.maxFiles) {
    throw new Error("invalid_input_paths");
  }
  const limitKey = JSON.stringify(deps.limits);
  const budget = inputBudget.get(deps.readGit) ?? { used: 0, limits: limitKey };
  if (budget.limits !== limitKey) throw new Error("input_limits_changed");
  inputBudget.set(deps.readGit, budget);
  const graph = async (): Promise<GraphRead> => {
    const git: GitReadEvidence[] = [];
    if (budget.used >= deps.limits.maxTotalBytes) {
      return {
        kind: "rejected",
        git,
        error: observationError("budget_exhausted", null, "attempt input budget"),
      };
    }
    const recorder: GitReader = async (cwd, args) => {
      const stdout = await deps.readGit(cwd, args);
      const retained = readerEvidence.get(deps.readGit);
      if (!retained) throw new Error("missing_trusted_bounded_git_receipt");
      git.push({
        ordinal: retained.ordinal,
        root: cwd,
        args: [...args],
        stdout: retained.stdout,
        stdout_sha256: await sha256(new TextEncoder().encode(retained.stdout)),
        receipt: { ...retained.receipt },
      });
      return stdout;
    };
    try {
      const actual = await sourceGraph(root, true, recorder);
      return {
        kind: "complete",
        graph: actual,
        raw_json_sha256: await sha256(new TextEncoder().encode(JSON.stringify(actual))),
        git,
      };
    } catch (error) {
      const failure = observationError(
        error instanceof GitObservationError ? error.code : "graph_rejected",
        null,
        error,
      );
      if (error instanceof GitObservationError && error.receipt) {
        failure.evidence = [{ ...error.receipt }];
      }
      return { kind: "rejected", git, error: failure };
    }
  };
  const start = await graph(), inputs: InputObservation[] = [];
  for (const path of paths) {
    const cap = Math.min(deps.limits.maxFileBytes, deps.limits.maxTotalBytes - budget.used);
    if (cap <= 0) {
      inputs.push({
        kind: "unreadable",
        path,
        error: observationError("budget_exhausted", path, "attempt input budget"),
      });
      continue;
    }
    try {
      const item = await deps.readInput(path, cap);
      const actualPath = item.kind === "present" ? item.actual.path : item.path;
      if (
        actualPath !== path ||
        (item.kind === "present" && (!validBinding(item.actual) || item.actual.bytes > cap)) ||
        !["present", "absent", "unreadable"].includes(item.kind)
      ) throw new Error("invalid_input_observation");
      if (item.kind === "present") budget.used += item.actual.bytes;
      if (item.kind === "unreadable") budget.used += cap; // Unknown consumption reserves its full allowance.
      // Copy the observed union so later fake mutation cannot alter this record.
      inputs.push(structuredClone(item));
    } catch (error) {
      budget.used += cap;
      inputs.push({
        kind: "unreadable",
        path,
        error: observationError("input_unreadable", path, error),
      });
    }
  }
  const observed = { start, inputs, end: await graph() };
  observedByCode.add(observed);
  return observed;
}

export function compareDocsObservation(
  expected: DocsIdentity,
  observed: DocsObservation,
): Comparison {
  const changes: ChangeEvidence[] = [], unknowns: ObservationError[] = [];
  const invalid = (detail: string) =>
    unknowns.push(observationError("invalid_observation_shape", null, detail));
  if (!observed || !Array.isArray(observed.inputs) || !observed.start || !observed.end) {
    return {
      kind: "unreadable_unknown",
      observation: observed,
      unknowns: [observationError("invalid_observation_shape", null, "missing observation fields")],
    };
  }
  let expectedGraph: SourceGraph;
  try {
    expectedGraph = docsIdentityProjection(expected).graph;
  } catch (error) {
    return {
      kind: "unreadable_unknown",
      observation: observed,
      unknowns: [observationError("invalid_expected", null, error)],
    };
  }
  const expectedFiles = new Map(expected.inputs.map((i) => [i.path, i]));
  const seen = new Set<string>(), actual: FileBinding[] = [];
  for (const item of observed.inputs) {
    if (
      !item || !["present", "absent", "unreadable"].includes(item.kind) ||
      (item.kind === "present" && !item.actual)
    ) {
      invalid("invalid input union");
      continue;
    }
    const path = item.kind === "present" ? item.actual.path : item.path;
    const frozen = expectedFiles.get(path);
    if (!frozen || seen.has(path)) {
      invalid("unexpected or duplicate input");
      continue;
    }
    seen.add(path);
    if (item.kind === "present") {
      if (!validBinding(item.actual)) {
        invalid("invalid actual input");
        continue;
      }
      actual.push(item.actual);
      if (item.actual.bytes !== frozen.bytes || item.actual.sha256 !== frozen.sha256) {
        changes.push({
          kind: "file_changed",
          expected: { ...frozen },
          actual: { ...item.actual },
          evidence: item.evidence,
        });
      }
    } else if (item.kind === "absent") {
      changes.push({ kind: "file_absent", expected: { ...frozen }, evidence: item.evidence });
    } else if (item.kind === "unreadable") unknowns.push(item.error);
    else invalid("unknown input kind");
  }
  if (seen.size !== expectedFiles.size) invalid("missing input");
  const complete: SourceGraph[] = [];
  for (const record of [observed.start, observed.end]) {
    if (!Array.isArray(record.git)) {
      invalid("missing Git evidence");
      continue;
    }
    if (record.kind === "complete") {
      try {
        const graph = privateGraph(record.graph);
        complete.push(graph);
        if (JSON.stringify(graph) !== JSON.stringify(expectedGraph)) {
          changes.push({ kind: "graph_changed", expected: expectedGraph, actual: graph });
        }
      } catch (error) {
        invalid(String(error));
      }
    } else if (record.kind === "rejected") unknowns.push(record.error);
    else invalid("invalid graph record");
    // Only acknowledged successful reads enter this list; failed/truncated
    // transport stdout is deliberately absent from the observer recorder.
    for (const evidence of record.git) {
      if (
        !evidence || typeof evidence.stdout !== "string" || !Array.isArray(evidence.args) ||
        !hex.test(evidence.stdout_sha256) || !evidence.receipt
      ) {
        invalid("invalid Git evidence");
        continue;
      }
      if (
        JSON.stringify(evidence.args) === '["status","--porcelain"]' && evidence.stdout.trimEnd()
      ) {
        changes.push({
          kind: "git_dirty",
          root: evidence.root,
          actual_status: evidence.stdout,
          evidence,
        });
      }
      if (
        JSON.stringify(evidence.args) === '["rev-parse","HEAD"]' &&
        /^[a-f0-9]{40}$/.test(evidence.stdout.trimEnd())
      ) {
        const component = expectedGraph.components.find((c) =>
          evidence.root.endsWith("/" + c.path)
        );
        const revision = component?.revision ?? expectedGraph.revision;
        if (evidence.stdout.trimEnd() !== revision) {
          changes.push({
            kind: "git_revision_changed",
            root: evidence.root,
            expected_revision: revision,
            actual_revision: evidence.stdout.trimEnd(),
            evidence,
          });
        }
      }
    }
  }
  if (complete.length === 2 && JSON.stringify(complete[0]) !== JSON.stringify(complete[1])) {
    changes.push({
      kind: "graph_changed_during_observation",
      start: complete[0],
      end: complete[1],
    });
  }
  if (changes.length) {
    return {
      kind: "observed_changed",
      observation: observed,
      changes: changes as [ChangeEvidence, ...ChangeEvidence[]],
      unknowns,
    };
  }
  if (unknowns.length) {
    return {
      kind: "unreadable_unknown",
      observation: observed,
      unknowns: unknowns as [ObservationError, ...ObservationError[]],
    };
  }
  return {
    kind: "matched",
    observation: observed,
    actual: docsIdentityProjection({ graph: complete[0], inputs: actual }),
  };
}

export function prepareDocsExpected(
  frozen: { inputs: readonly FileBinding[] },
  observed: DocsObservation,
): ExpectedPreparation {
  if (
    !observedByCode.has(observed) || !validInputs(frozen.inputs) ||
    observed.start.kind !== "complete"
  ) {
    return {
      kind: "expected_invalid",
      observation: observed,
      changes: [],
      unknowns: [
        observationError(
          "invalid_expected_preparation",
          null,
          "requires trusted fresh observation and valid frozen manifest",
        ),
      ],
    };
  }
  const result = compareDocsObservation(
    { graph: observed.start.graph, inputs: frozen.inputs },
    observed,
  );
  if (result.kind !== "matched") {
    return {
      kind: "expected_invalid",
      observation: observed,
      changes: result.kind === "observed_changed" ? result.changes : [],
      unknowns: result.unknowns,
    };
  }
  const expected = docsIdentityProjection(result.actual);
  for (const component of expected.graph.components) Object.freeze(component);
  Object.freeze(expected.graph.components);
  Object.freeze(expected.graph);
  for (const input of expected.inputs) Object.freeze(input);
  Object.freeze(expected.inputs);
  Object.freeze(expected);
  trustedExpected.add(expected);
  return { kind: "expected_ready", expected };
}
export async function withDocsSourceIdentity<T>(options: {
  expected: DocsIdentity;
  observe: () => Promise<DocsObservation>;
  execute: () => Promise<Operation<T>>;
}): Promise<ScopedIdentityResult<T>> {
  if (!trustedExpected.has(options.expected)) {
    throw new Error("expected_not_prepared_by_trusted_code");
  }
  const expected = options.expected;
  const observe = async (): Promise<Comparison> => {
    try {
      const observed = await options.observe();
      if (!observedByCode.has(observed)) throw new Error("observation_not_from_trusted_observer");
      return structuredClone(compareDocsObservation(expected, observed));
    } catch (error) {
      const failure = observationError("observer_threw", null, error);
      const rejected: GraphRead = { kind: "rejected", git: [], error: failure };
      const observation: DocsObservation = {
        start: rejected,
        end: rejected,
        inputs: expected.inputs.map((i) => ({ kind: "unreadable", path: i.path, error: failure })),
      };
      return { kind: "unreadable_unknown", observation, unknowns: [failure] };
    }
  };
  const before = await observe();
  if (before.kind !== "matched") {
    return {
      state: "blocked_before",
      expected,
      candidate: null,
      before,
      operation: null,
      after: null,
    };
  }
  let operation: Operation<T>;
  try {
    operation = await options.execute();
  } catch (error) {
    operation = { kind: "unknown_partial", error: String(error) };
  }
  const after = await observe();
  if (after.kind === "observed_changed") {
    return { state: "failed_source_changed", expected, candidate: null, before, after, operation };
  }
  if (after.kind === "unreadable_unknown") {
    return {
      state: "failed_identity_unknown",
      expected,
      candidate: null,
      before,
      after,
      operation,
    };
  }
  if (operation.kind === "completed") {
    return { state: "completed_bound", expected, candidate: null, before, after, operation };
  }
  return { state: "failed_bound", expected, candidate: null, before, after, operation };
}

export async function preflight(
  args: ReturnType<typeof parseDocsArgs>,
  root = workspace,
  deps?: { readGit: GitReader },
) {
  canonical(root);
  canonical(args.attempt);
  if (contains(root, args.attempt) || contains(args.attempt, root)) {
    throw new Error("attempt_source_overlap");
  }
  await ancestors(args.attempt.slice(0, args.attempt.lastIndexOf("/")) || "/", true);
  await absent(args.attempt);
  // mkdir is exclusive. Never remove, truncate, reuse or repair an attempt.
  await Deno.mkdir(args.attempt, { mode: 0o700 });
  const blockers = buildBlockers();
  const inputs: unknown[] = [];
  // Optional trusted code dependency never confers BUILD/admission authority.
  // Production CLI supplies none and never falls back to buffered Git.
  let sources: SourceGraph | null = null;
  if (deps) {
    try {
      sources = await sourceGraph(root, true, deps.readGit);
    } catch (error) {
      blockers.push(`source_graph_unavailable: ${String(error)}`);
    }
  }
  for (
    const path of [
      args.plan,
      `${root}/julia/Project.toml`,
      `${root}/julia/Manifest.toml`,
      `${root}/docs/public/make.jl`,
      `${root}/docs/public/operator-recovery.md`,
      `${root}/ops/docs/assemble.py`,
      `${root}/ops/docs/math-render.mjs`,
      `${root}/ops/docs/assets.lock.json`,
    ]
  ) {
    try {
      inputs.push(await boundedFile(path, 2097152));
    } catch (error) {
      blockers.push(`input_unavailable: ${path}: ${String(error)}`);
    }
  }
  // Plan parsing and final adapter calls deliberately remain blocked. The
  // published assembler has pure functions, no admitted complete pipeline API;
  // prepare_catalog explicitly cannot serialize an accepted bundle. Merely
  // hashing these files is not API, plan, assets, import or schema acceptance.
  if (args.admission) blockers.push("supplied_admission_not_validated_no_dispatch");
  const receipt = {
    sources,
    plan: args.plan,
    inputs,
    admission: null,
    imports: {
      status: "not_measured",
      unknown_edges: ["nested_docstrings", "transitive_imports", "cache"],
    },
    assets: { status: "not_measured" },
    toolchain: null,
    steps: [],
    measurements: null,
    transforms: [],
    checks: blockers.map((reason) => ({ status: "blocked", reason })),
    result: "blocked",
    parent_attempt: null,
  };
  await Deno.writeTextFile(
    `${args.attempt}/receipt.json`,
    JSON.stringify(receipt, null, 2) + "\n",
    { createNew: true, mode: 0o600 },
  );
  return receipt;
}
if (import.meta.main) {
  try {
    const receipt = await preflight(parseDocsArgs(Deno.args));
    console.log(JSON.stringify(receipt, null, 2));
    Deno.exitCode = 2;
  } catch (error) {
    console.error(String(error));
    Deno.exitCode = 1;
  }
}
