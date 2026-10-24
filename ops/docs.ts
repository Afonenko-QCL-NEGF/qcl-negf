// DOC04 ordinary producer: observe selected sources and actual native guards,
// then one capped local Nix candidate. A marker never confers BUILD authority.
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

export function docsBuildCommand(nixExecutable: string, sourceRoot: string, attempt: string) {
  for (const path of [nixExecutable, sourceRoot, attempt]) canonical(path);
  return {
    executable: nixExecutable,
    cwd: sourceRoot,
    clearEnv: true as const,
    env: {
      PATH: nixExecutable.slice(0, nixExecutable.lastIndexOf("/")),
      HOME: `${attempt}/home`,
      TMPDIR: `${attempt}/tmp`,
      XDG_CACHE_HOME: `${attempt}/cache`,
      LC_ALL: "C",
    },
    args: [
      "--store",
      "local",
      "build",
      "--offline",
      "--no-link",
      "--json",
      "--keep-failed",
      "--max-jobs",
      "1",
      "--cores",
      "4",
      "--timeout",
      "1800",
      "--option",
      "sandbox",
      "true",
      "--option",
      "builders",
      "",
      "--option",
      "substitute",
      "false",
      "--option",
      "use-cgroups",
      "false",
      "--file",
      `${sourceRoot}/nix/docs.nix`,
      "--argstr",
      "inputsFile",
      `${attempt}/producer-inputs.json`,
    ],
  };
}

export interface PathRecord {
  path: string;
  sha256: string;
}
export interface DocsTool {
  store_path: string;
  executable: string;
  deriver: string;
  version: string;
}
export interface ProducerInputs {
  source_root: string;
  source_graph: PathRecord;
  plan: PathRecord;
  project: PathRecord;
  manifest: PathRecord;
  prepared_depot: { store_path: string; metadata: PathRecord };
  assets_lock: PathRecord;
  asset_inputs: PathRecord;
  review_inputs: PathRecord;
  tools: Record<"python" | "node" | "julia" | "git", DocsTool>;
}
export interface DocsAdmission {
  format: "qcl-negf.docs-admission.v1";
  created_epoch: number;
  attempt_directory: string;
  repository_root: string;
  plan_sha256: string;
  unit: { name: string; uid: 0; boot_id: string; control_group: string };
  resource_readback: PathRecord;
  tools: Record<"nix" | "git" | "deno" | "python" | "node" | "julia", DocsTool>;
  inputs: ProducerInputs;
}
function exactKeys(
  value: unknown,
  keys: readonly string[],
): asserts value is Record<string, unknown> {
  if (
    !record(value) || Object.keys(value).length !== keys.length ||
    keys.some((key) => !Object.hasOwn(value, key))
  ) throw new Error("invalid_private_input_fields");
}
function storePath(path: unknown): asserts path is string {
  if (typeof path !== "string") throw new Error("invalid_store_path");
  canonical(path);
  if (!/^\/nix\/store\/[a-z0-9]{32}-[^/]+(?:\/.*)?$/.test(path)) {
    throw new Error("immutable_store_path_required");
  }
}
function pathRecord(value: unknown): asserts value is PathRecord {
  exactKeys(value, ["path", "sha256"]);
  storePath(value.path);
  if (typeof value.sha256 !== "string" || !hex.test(value.sha256)) {
    throw new Error("invalid_input_sha256");
  }
}
function docsTool(value: unknown): asserts value is DocsTool {
  exactKeys(value, ["store_path", "executable", "deriver", "version"]);
  storePath(value.store_path);
  storePath(value.executable);
  storePath(value.deriver);
  if (
    value.store_path.slice(11).includes("/") || !value.deriver.endsWith(".drv") ||
    !contains(value.store_path, value.executable) || value.store_path === value.executable ||
    typeof value.version !== "string" || !value.version.trim() || value.version.length > 256
  ) {
    throw new Error("invalid_tool_binding");
  }
}
// JSON.parse alone silently accepts duplicate authority fields. Scan the same
// finite JSON grammar first; decoded keys share one set per object, depth capped.
export function parseDocsJson(text: string): unknown {
  const result: unknown = JSON.parse(text);
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
export function parseDocsAdmission(value: unknown): DocsAdmission {
  exactKeys(value, [
    "format",
    "created_epoch",
    "attempt_directory",
    "repository_root",
    "plan_sha256",
    "unit",
    "resource_readback",
    "tools",
    "inputs",
  ]);
  if (
    value.format !== "qcl-negf.docs-admission.v1" || typeof value.created_epoch !== "number" ||
    !Number.isFinite(value.created_epoch) ||
    typeof value.plan_sha256 !== "string" || !hex.test(value.plan_sha256)
  ) throw new Error("invalid_admission");
  for (const key of ["attempt_directory", "repository_root"] as const) {
    if (typeof value[key] !== "string") throw new Error("invalid_admission_path");
    canonical(value[key]);
  }
  exactKeys(value.unit, ["name", "uid", "boot_id", "control_group"]);
  if (
    value.unit.uid !== 0 || typeof value.unit.name !== "string" ||
    !/^[A-Za-z0-9][A-Za-z0-9_-]{1,127}\.service$/.test(value.unit.name) ||
    typeof value.unit.boot_id !== "string" || !/^[a-f0-9-]{36}$/.test(value.unit.boot_id) ||
    typeof value.unit.control_group !== "string"
  ) throw new Error("invalid_unit_binding");
  canonical(value.unit.control_group);
  if (!value.unit.control_group.endsWith("/" + value.unit.name)) {
    throw new Error("unit_cgroup_mismatch");
  }
  exactKeys(value.resource_readback, ["path", "sha256"]);
  if (
    typeof value.resource_readback.path !== "string" ||
    typeof value.resource_readback.sha256 !== "string" ||
    !hex.test(value.resource_readback.sha256)
  ) throw new Error("invalid_resource_readback");
  canonical(value.resource_readback.path);
  exactKeys(value.tools, ["nix", "git", "deno", "python", "node", "julia"]);
  const tools = value.tools;
  for (const tool of Object.values(tools)) docsTool(tool);
  const inputs = value.inputs;
  exactKeys(inputs, [
    "source_root",
    "source_graph",
    "plan",
    "project",
    "manifest",
    "prepared_depot",
    "assets_lock",
    "asset_inputs",
    "review_inputs",
    "tools",
  ]);
  storePath(inputs.source_root);
  for (
    const key of [
      "source_graph",
      "plan",
      "project",
      "manifest",
      "assets_lock",
      "asset_inputs",
      "review_inputs",
    ] as const
  ) {
    pathRecord(inputs[key]);
  }
  exactKeys(inputs.prepared_depot, ["store_path", "metadata"]);
  storePath(inputs.prepared_depot.store_path);
  pathRecord(inputs.prepared_depot.metadata);
  exactKeys(inputs.tools, ["python", "node", "julia", "git"]);
  for (const [key, tool] of Object.entries(inputs.tools)) {
    docsTool(tool);
    if (
      ["store_path", "executable", "deriver", "version"].some((field) =>
        tool[field as keyof DocsTool] !== (tools[key] as DocsTool)[field as keyof DocsTool]
      )
    ) {
      throw new Error("producer_tool_mismatch");
    }
  }
  if (
    (inputs.project as PathRecord).path !== `${inputs.source_root}/julia/Project.toml` ||
    (inputs.manifest as PathRecord).path !== `${inputs.source_root}/julia/Manifest.toml` ||
    (inputs.assets_lock as PathRecord).path !== `${inputs.source_root}/ops/docs/assets.lock.json`
  ) {
    throw new Error("producer_source_path_mismatch");
  }
  return structuredClone(value) as unknown as DocsAdmission;
}
export function checkDocsAdmissionFreshness(
  createdEpoch: number,
  nowEpoch = Date.now() / 1000,
): void {
  if (
    typeof createdEpoch !== "number" || !Number.isFinite(createdEpoch) ||
    typeof nowEpoch !== "number" || !Number.isFinite(nowEpoch)
  ) throw new Error("invalid_admission_epoch");
  const age = nowEpoch - createdEpoch;
  if (age < 0 || age > 300) throw new Error("stale_or_future_admission");
}
export interface CgroupReadback {
  uid: number;
  pid: number;
  boot_id: string;
  control_group: string;
  unit: Record<string, string>;
  controls: Record<string, string>;
}
export function checkDocsCgroup(admission: DocsAdmission, actual: CgroupReadback) {
  const unit = actual.unit, controls = actual.controls;
  if (
    actual.uid !== 0 || actual.boot_id.trim() !== admission.unit.boot_id ||
    actual.control_group !== admission.unit.control_group || unit.Id !== admission.unit.name ||
    unit.ActiveState !== "active" || unit.SubState !== "running" ||
    unit.MainPID !== String(actual.pid) || !["", "root", "0"].includes(unit.User) ||
    unit.ControlGroup !== actual.control_group || unit.KillMode !== "control-group" ||
    !["30min", "1800000000"].includes(unit.RuntimeMaxUSec)
  ) throw new Error("native_unit_mismatch");
  const bounded = (text: string, cap: number) =>
    /^\d+$/.test(text) && Number(text) > 0 && Number(text) <= cap;
  const cpu = /^(\d+)\s+(\d+)$/.exec(controls["cpu.max"]?.trim());
  if (
    !cpu || Number(cpu[1]) <= 0 || Number(cpu[2]) <= 0 || Number(cpu[1]) / Number(cpu[2]) > 4 ||
    !bounded(controls["memory.max"]?.trim(), 4294967296) ||
    controls["memory.swap.max"]?.trim() !== "0" || !bounded(controls["pids.max"]?.trim(), 128) ||
    !/^\d+\s*$/.test(controls["memory.current"] ?? "") ||
    !controls["memory.events"]?.trim() || !controls["cpu.stat"]?.trim()
  ) throw new Error("native_cgroup_cap_mismatch");
  return structuredClone(actual);
}
async function kernelText(path: string, cap = 65536): Promise<string> {
  const file = await Deno.open(path, { read: true });
  try {
    const data = new Uint8Array(cap + 1);
    let count = 0;
    while (count <= cap) {
      const n = await file.read(data.subarray(count));
      if (n === null) break;
      count += n;
      if (count > cap) throw new Error("kernel_read_cap");
    }
    return new TextDecoder("utf-8", { fatal: true }).decode(data.subarray(0, count));
  } finally {
    file.close();
  }
}
async function resolveDocsExecutable(name: string): Promise<string> {
  for (const directory of (Deno.env.get("PATH") ?? "").split(":")) {
    if (!directory.startsWith("/")) continue;
    try {
      const path = await Deno.realPath(`${directory}/${name}`);
      canonical(path);
      const info = await Deno.stat(path);
      if (info.isFile && info.mode !== null && (info.mode & 0o111)) return path;
    } catch (error) {
      if (error instanceof Deno.errors.NotFound) continue;
      throw error;
    }
  }
  throw new Error(`executable_unavailable: ${name}`);
}
async function protectedFile(path: string, cap = 2097152) {
  const data = await readRegularBounded(path, cap), info = await Deno.lstat(path);
  if (info.uid !== 0 || info.mode === null || (info.mode & 0o022) !== 0) {
    throw new Error("root_protected_authority_required");
  }
  return data;
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
// intentionally not a CPU/RAM/descendant sandbox; BUILD additionally verifies its owning unit.
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
// Root e5fc selected trees total 314113 bytes per graph; the complete CLI
// lifecycle observes seven graphs (2198791 tree bytes plus config/revisions).
// The finite 4 MiB allowance leaves headroom inside the shared 8 MiB log budget.
export const productionDocsGitLimits: Readonly<GitLimits> = Object.freeze({
  wallMs: 3000,
  drainMs: 1000,
  streamBytes: 524288,
  totalBytes: 1048576,
  maxCommands: 1024,
  maxTotalBytes: 4194304,
  totalWallMs: 1800000,
});
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
// The child has piped streams only: no Command.output()/unbounded stdout path.
export function makeDocsGitTransport(
  spawn: (call: GitCall) => Child = (call) => {
    const child = new Deno.Command(call.executable, {
      args: call.args,
      cwd: call.cwd,
      env: call.env,
      clearEnv: call.clearEnv,
      stdin: "null",
      stdout: "piped",
      stderr: "piped",
    }).spawn();
    return {
      stdout: child.stdout,
      stderr: child.stderr,
      status: child.status,
      kill: () => child.kill("SIGKILL"),
    };
  },
): GitTransport {
  return async (call) => {
    canonical(call.tag.attempt);
    if (!Number.isSafeInteger(call.tag.ordinal) || call.tag.ordinal < 1) {
      throw new Error("invalid_git_ordinal");
    }
    await ancestors(call.tag.attempt, true);
    const parent = `${call.tag.attempt}/git`;
    try {
      await Deno.mkdir(parent, { mode: 0o700 });
    } catch (error) {
      if (!(error instanceof Deno.errors.AlreadyExists)) throw error;
    }
    await ancestors(parent, true);
    const directory = `${parent}/${call.tag.ordinal}`;
    await Deno.mkdir(directory, { mode: 0o700 }); // exclusive before any child
    const stdout = await Deno.open(`${directory}/stdout.log`, {
      write: true,
      createNew: true,
      mode: 0o600,
    });
    let stderr: Deno.FsFile | null = null;
    const chunks: Uint8Array[] = [];
    let result: FiniteResult;
    try {
      stderr = await Deno.open(`${directory}/stderr.log`, {
        write: true,
        createNew: true,
        mode: 0o600,
      });
      result = await runFinite(() => spawn(call), async (stream, bytes, signal) => {
        const file = stream === "stdout" ? stdout : stderr!;
        let offset = 0;
        while (offset < bytes.length) {
          if (signal.aborted) throw new Error("git_log_write_aborted");
          const written = await file.write(bytes.subarray(offset));
          if (written <= 0) throw new Error("git_log_short_write");
          offset += written;
        }
        if (stream === "stdout") chunks.push(bytes.slice());
      }, call.limits);
    } catch (error) {
      const bytes = new TextEncoder().encode(
        JSON.stringify(
          {
            call,
            result: null,
            error: safeFailureDetail(error),
            accounting: "unknown",
          },
          null,
          2,
        ) + "\n",
      );
      const path = `${directory}/result.json`;
      await Deno.writeFile(path, bytes, { createNew: true, mode: 0o600 });
      throw Object.assign(new Error(safeFailureDetail(error)), {
        receipt: { path, sha256: await sha256(bytes) },
      });
    } finally {
      stdout.close();
      stderr?.close();
    }
    const data = new Uint8Array(result.stdout_acknowledged_bytes);
    let offset = 0;
    for (const chunk of chunks) {
      const retained = chunk.subarray(0, data.length - offset);
      data.set(retained, offset);
      offset += retained.length;
      if (offset === data.length) break;
    }
    const bytes = new TextEncoder().encode(JSON.stringify({ call, result }, null, 2) + "\n");
    const path = `${directory}/result.json`;
    await Deno.writeFile(path, bytes, { createNew: true, mode: 0o600 });
    return { stdout: data, result, receipt: { path, sha256: await sha256(bytes) } };
  };
}

// The reader validates finite retained transport evidence before exposing Git stdout.
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

export async function dispatchDocsBuild(options: {
  admission: DocsAdmission;
  attempt: string;
  wallMs: number;
  invoke: GitTransport;
}) {
  canonical(options.attempt);
  if (!Number.isSafeInteger(options.wallMs) || options.wallMs <= 0) {
    throw new Error("candidate_deadline");
  }
  await Deno.writeTextFile(
    `${options.attempt}/producer-inputs.json`,
    JSON.stringify(options.admission.inputs, null, 2) + "\n",
    { createNew: true, mode: 0o600 },
  );
  const command = docsBuildCommand(
    options.admission.tools.nix.executable,
    options.admission.inputs.source_root,
    options.attempt,
  );
  return options.invoke({
    ...command,
    tag: { attempt: options.attempt, ordinal: 20000 },
    limits: { wallMs: options.wallMs, drainMs: 1000, streamBytes: 7340032, totalBytes: 7340032 },
  });
}
export function parseDocsNixOutput(stdout: Uint8Array): string {
  const result = parseDocsJson(new TextDecoder("utf-8", { fatal: true }).decode(stdout));
  if (
    !Array.isArray(result) || result.length !== 1 || !record(result[0]) ||
    !record(result[0].outputs) ||
    Object.keys(result[0].outputs).length !== 1 || typeof result[0].outputs.out !== "string"
  ) throw new Error("one_nix_output_required");
  const output = result[0].outputs.out;
  storePath(output);
  return output;
}

export interface DocsCheck {
  name: string;
  status: "observed" | "blocked";
  reason: string;
}
export function buildBlockers(checks: readonly DocsCheck[] = []): string[] {
  return checks.length
    ? checks.filter((check) => check.status === "blocked").map((check) => check.reason)
    : ["preflight_not_observed"];
}
interface PreflightReceipt {
  sources: SourceGraph | null;
  plan: string;
  inputs: FileBinding[];
  admission: FileBinding | null;
  imports: unknown;
  assets: unknown;
  toolchain: unknown;
  steps: unknown[];
  measurements: unknown;
  checks: DocsCheck[];
  result: "blocked" | "prerequisites_observed";
  parent_attempt: null;
}
interface BuildContext {
  args: ReturnType<typeof parseDocsArgs>;
  root: string;
  started: number;
  admission: DocsAdmission;
  inputs: FileBinding[];
  readGit: GitReader;
  invoke: GitTransport;
  command: (executable: string, args: string[], cap?: number, wall?: number) => Promise<GitReply>;
  native: unknown;
  remaining: () => number;
}
const preflightContexts = new WeakMap<PreflightReceipt, BuildContext>();
export async function preflight(
  args: ReturnType<typeof parseDocsArgs>,
  root = workspace,
  deps?: { readGit: GitReader },
): Promise<PreflightReceipt> {
  const started = performance.now();
  canonical(root);
  canonical(args.attempt);
  if (contains(root, args.attempt) || contains(args.attempt, root)) {
    throw new Error("attempt_source_overlap");
  }
  await ancestors(args.attempt.slice(0, args.attempt.lastIndexOf("/")) || "/", true);
  await absent(args.attempt);
  await Deno.mkdir(args.attempt, { mode: 0o700 });
  const checks: DocsCheck[] = [], inputs: FileBinding[] = [];
  async function observe<T>(name: string, work: () => Promise<T>): Promise<T | null> {
    try {
      const value = await work();
      checks.push({ name, status: "observed", reason: name });
      return value;
    } catch (error) {
      checks.push({ name, status: "blocked", reason: `${name}: ${safeFailureDetail(error)}` });
      return null;
    }
  }
  const addInput = async (path: string, cap = 2097152) => {
    const data = await readRegularBounded(path, cap);
    const binding = { path, bytes: data.length, sha256: await sha256(data) };
    if (!inputs.some((item) => item.path === path)) inputs.push(binding);
    return { data, binding };
  };
  const planInput = await observe("pilot_plan", () => addInput(args.plan));
  const plan = planInput &&
    await observe(
      "pilot_policy",
      () =>
        Promise.resolve(parseDocsPlan(
          parseDocsJson(new TextDecoder("utf-8", { fatal: true }).decode(planInput.data)),
        )),
    );
  let admissionBinding: FileBinding | null = null;
  const admission = args.admission
    ? await observe("native_admission", async () => {
      const data = await protectedFile(args.admission!);
      const value = parseDocsAdmission(
        parseDocsJson(new TextDecoder("utf-8", { fatal: true }).decode(data)),
      );
      checkDocsAdmissionFreshness(value.created_epoch);
      if (
        value.repository_root !== root ||
        value.attempt_directory !== args.attempt ||
        value.plan_sha256 !== planInput?.binding.sha256
      ) throw new Error("stale_or_mismatched_admission");
      admissionBinding = { path: args.admission!, bytes: data.length, sha256: await sha256(data) };
      return value;
    })
    : null;
  if (!args.admission) {
    checks.push({
      name: "native_admission",
      status: "blocked",
      reason: "native_admission_not_supplied",
    });
  }
  let usedLogBytes = 0, consumptionUnknown = false, ordinal = 10000;
  const physical = makeDocsGitTransport();
  const invoke: GitTransport = async (call) => {
    if (consumptionUnknown || usedLogBytes >= 8388608) {
      throw new Error("combined_log_budget_exhausted_or_unknown");
    }
    const available = 8388608 - usedLogBytes;
    try {
      const reply = await physical({
        ...call,
        limits: {
          ...call.limits,
          totalBytes: Math.min(call.limits.totalBytes, available),
          streamBytes: Math.min(call.limits.streamBytes, available),
        },
      });
      usedLogBytes += reply.result.stdout_received_bytes + reply.result.stderr_received_bytes;
      if (reply.result.drain !== "complete") consumptionUnknown = true;
      return reply;
    } catch (error) {
      consumptionUnknown = true;
      throw error;
    }
  };
  const remaining = () => Math.max(0, Math.floor(1800000 - (performance.now() - started)));
  const command = async (executable: string, argv: string[], cap = 65536, wall = 10000) => {
    const available = remaining();
    if (available <= 0) throw new Error("candidate_deadline");
    const reply = await invoke({
      executable,
      args: argv,
      cwd: root,
      clearEnv: true,
      env: { LC_ALL: "C", HOME: `${args.attempt}/home`, TMPDIR: `${args.attempt}/tmp` },
      tag: { attempt: args.attempt, ordinal: ++ordinal },
      limits: {
        wallMs: Math.min(wall, available),
        drainMs: 1000,
        streamBytes: cap,
        totalBytes: cap,
      },
    });
    return reply;
  };
  const output = (reply: GitReply) => {
    const r = reply.result;
    if (
      r.reason !== null || !r.exit?.success || r.exit.code !== 0 || r.drain !== "complete" ||
      r.retention !== "acknowledged" || r.errors.length
    ) throw new Error(`command_failed: ${JSON.stringify(reply.receipt)}`);
    return new TextDecoder("utf-8", { fatal: true }).decode(reply.stdout).trim();
  };
  const gitExecutable = deps ? null : await observe("git_executable", async () => {
    const path = await resolveDocsExecutable("git");
    if (admission && path !== admission.tools.git.executable) {
      throw new Error("admitted_git_path_mismatch");
    }
    return path;
  });
  const readGit = deps?.readGit ??
    (gitExecutable
      ? makeDocsGitReader({
        root,
        attempt: args.attempt,
        gitExecutable,
        invoke,
        limits: productionDocsGitLimits,
      })
      : null);
  const sources = readGit
    ? await observe("clean_source_graph", () => sourceGraph(root, true, readGit))
    : null;
  if (!readGit) {
    checks.push({
      name: "clean_source_graph",
      status: "blocked",
      reason: "bounded_git_transport_unavailable",
    });
  }
  if (plan) {
    for (
      const path of [
        ...plan.source_inputs,
        "ops/docs.ts",
        "nix/docs.nix",
        "ops/docs/produce.py",
        "ops/docs/assemble.py",
        "ops/docs/math-render.mjs",
        "ops/docs/runtime-assets.py",
      ]
    ) {
      await observe(`source_input:${path}`, () => addInput(`${root}/${path}`));
    }
  }
  const selected = await observe("selected_docs_no_executable_blocks", () =>
    scanDocsSources([
      `${root}/components/QCLNEGF.jl/docs/src`,
      `${root}/components/QCLNEGFRunner.jl/docs/src`,
      `${root}/docs/public`,
    ]));
  if (selected) {
    for (const file of selected.files) {
      if (!inputs.some((item) => item.path === file.path)) inputs.push(file);
    }
  }
  const assets = await observe("asset_lock_inputs", async () => {
    const file = await addInput(`${root}/ops/docs/assets.lock.json`);
    const lock = parseDocsJson(new TextDecoder("utf-8", { fatal: true }).decode(file.data));
    if (
      !record(lock) || lock.format !== "qcl-docs-assets-v1" || lock.closure_status !== "complete" ||
      !Array.isArray(lock.missing_inputs) || lock.missing_inputs.length
    ) {
      throw new Error(
        `asset_closure_incomplete: ${JSON.stringify(record(lock) ? lock.missing_inputs : null)}`,
      );
    }
    return { path: file.binding, status: "declared_complete_requires_producer_verification" };
  });
  let native: unknown = null;
  if (admission && sources) {
    native = await observe("fresh_native_inputs_and_own_unit", async () => {
      for (const path of ["home", "tmp", "cache"]) {
        await Deno.mkdir(`${args.attempt}/${path}`, { mode: 0o700 });
      }
      const authority = await protectedFile(admission.resource_readback.path);
      if (await sha256(authority) !== admission.resource_readback.sha256) {
        throw new Error("resource_authority_hash_mismatch");
      }
      await Deno.writeFile(`${args.attempt}/resource-readback.json`, authority, {
        createNew: true,
        mode: 0o600,
      });
      const bound = async (item: PathRecord, cap = 2097152) => {
        const data = await readRegularBounded(item.path, cap);
        if (await sha256(data) !== item.sha256) {
          throw new Error(`immutable_input_hash_mismatch: ${item.path}`);
        }
        return data;
      };
      await ancestors(admission.inputs.source_root, true);
      await ancestors(admission.inputs.prepared_depot.store_path, true);
      const records = [
        admission.inputs.source_graph,
        admission.inputs.plan,
        admission.inputs.project,
        admission.inputs.manifest,
        admission.inputs.prepared_depot.metadata,
        admission.inputs.assets_lock,
        admission.inputs.asset_inputs,
        admission.inputs.review_inputs,
      ];
      for (const item of records) await bound(item);
      const expectedGraph = parseDocsJson(
        new TextDecoder().decode(await bound(admission.inputs.source_graph)),
      );
      if (
        JSON.stringify(privateGraph(expectedGraph as SourceGraph)) !==
          JSON.stringify(privateGraph(sources))
      ) {
        throw new Error("export_graph_mismatch");
      }
      if (admission.inputs.plan.sha256 !== planInput?.binding.sha256) {
        throw new Error("export_plan_mismatch");
      }
      const assetInputs = parseDocsJson(
        new TextDecoder().decode(await bound(admission.inputs.asset_inputs)),
      );
      if (
        !record(assetInputs) || !Object.keys(assetInputs).length ||
        Object.keys(assetInputs).length > 10000
      ) throw new Error("invalid_asset_input_map");
      for (const [key, path] of Object.entries(assetInputs)) {
        if (!relativeDocsPath(key)) throw new Error("invalid_asset_input_key");
        storePath(path);
        await ancestors(path, false);
      }
      // Source export must bind the same selected recipes and public input bytes.
      for (const file of inputs.filter((file) => file.path.startsWith(root + "/"))) {
        const exported = await boundedFile(
          admission.inputs.source_root + file.path.slice(root.length),
          2097152,
        );
        if (exported.bytes !== file.bytes || exported.sha256 !== file.sha256) {
          throw new Error(`export_source_mismatch: ${file.path}`);
        }
      }
      const systemctl = await resolveDocsExecutable("systemctl");
      const unitText = output(
        await command(systemctl, [
          "show",
          admission.unit.name,
          "--no-pager",
          ...[
            "Id",
            "ActiveState",
            "SubState",
            "MainPID",
            "User",
            "ControlGroup",
            "RuntimeMaxUSec",
            "KillMode",
            "MemoryMax",
            "MemorySwapMax",
            "TasksMax",
            "CPUQuotaPerSecUSec",
          ].map((key) => "--property=" + key),
        ]),
      );
      const unit: Record<string, string> = {};
      for (const line of unitText.split("\n")) {
        const index = line.indexOf("=");
        if (index > 0) unit[line.slice(0, index)] = line.slice(index + 1);
      }
      const membership = await kernelText("/proc/self/cgroup");
      const match = /^0::([^\n]+)\n?$/.exec(membership);
      if (!match) throw new Error("unified_own_cgroup_required");
      const controlGroup = match[1];
      canonical(controlGroup);
      const controls: Record<string, string> = {};
      for (
        const key of [
          "cpu.max",
          "memory.max",
          "memory.swap.max",
          "pids.max",
          "memory.current",
          "memory.events",
          "cpu.stat",
        ]
      ) {
        controls[key] = await kernelText(`/sys/fs/cgroup${controlGroup}/${key}`);
      }
      const uid = Deno.uid();
      if (uid === null) throw new Error("native_uid_unavailable");
      const actual = checkDocsCgroup(admission, {
        uid,
        pid: Deno.pid,
        boot_id: await kernelText("/proc/sys/kernel/random/boot_id"),
        control_group: controlGroup,
        unit,
        controls,
      });
      const toolReadbacks: Record<string, unknown> = {};
      const nixStore = await Deno.realPath(`${admission.tools.nix.store_path}/bin/nix-store`);
      if (!contains(admission.tools.nix.store_path, nixStore)) {
        throw new Error("nix_store_tool_path_mismatch");
      }
      for (const [name, tool] of Object.entries(admission.tools)) {
        await ancestors(tool.store_path, true);
        await ancestors(tool.deriver, false);
        const actual = await Deno.realPath(tool.executable);
        if (actual !== tool.executable || !contains(tool.store_path, actual)) {
          throw new Error(`tool_path_mismatch: ${name}`);
        }
        const info = await Deno.stat(actual);
        if (!info.isFile || info.mode === null || !(info.mode & 0o111)) {
          throw new Error(`tool_not_executable: ${name}`);
        }
        const version = output(await command(actual, ["--version"]));
        if (!version.includes(tool.version)) throw new Error(`tool_version_mismatch: ${name}`);
        const deriver = output(
          await command(nixStore, ["--store", "local", "--query", "--deriver", tool.store_path]),
        );
        if (deriver !== tool.deriver) throw new Error(`tool_deriver_mismatch: ${name}`);
        toolReadbacks[name] = { executable: actual, version, deriver };
      }
      if (
        await Deno.realPath(Deno.execPath()) !== admission.tools.deno.executable
      ) throw new Error("running_deno_mismatch");
      const readbacks = {
        actual,
        tools: toolReadbacks,
        systemctl,
        resource_readback: admission.resource_readback,
        source_graph: admission.inputs.source_graph,
        prepared_depot: admission.inputs.prepared_depot,
      };
      await Deno.writeTextFile(
        `${args.attempt}/native-readbacks.json`,
        JSON.stringify(readbacks, null, 2) + "\n",
        { createNew: true, mode: 0o600 },
      );
      return readbacks;
    });
  }
  const blockers = buildBlockers(checks);
  const receipt: PreflightReceipt = {
    sources,
    plan: args.plan,
    inputs,
    admission: admissionBinding,
    imports: { selected_docs: selected, actual_imports: "producer_once_pending" },
    assets,
    toolchain: native,
    steps: [],
    measurements: null,
    checks,
    result: blockers.length ? "blocked" : "prerequisites_observed",
    parent_attempt: null,
  };
  await Deno.writeTextFile(
    `${args.attempt}/receipt.json`,
    JSON.stringify(receipt, null, 2) + "\n",
    { createNew: true, mode: 0o600 },
  );
  if (!blockers.length && admission && readGit) {
    preflightContexts.set(receipt, {
      args,
      root,
      started,
      admission,
      inputs,
      readGit,
      invoke,
      command,
      native,
      remaining,
    });
  }
  return receipt;
}
export async function runDocs(
  args: ReturnType<typeof parseDocsArgs>,
  root = workspace,
  deps?: { readGit: GitReader },
) {
  const receipt = await preflight(args, root, deps);
  if (args.mode !== "build" || receipt.result !== "prerequisites_observed") return receipt;
  const context = preflightContexts.get(receipt);
  if (!context) throw new Error("build_context_not_prepared");
  const { admission, inputs, readGit } = context;
  const observe = () =>
    observeDocsSources(root, inputs.map((file) => file.path), {
      readGit,
      readInput: observeDocsInput,
      limits: { maxFiles: 10000, maxFileBytes: 2097152, maxTotalBytes: 67108864 },
    });
  const initial = await observe();
  const prepared = prepareDocsExpected({ inputs }, initial);
  let buildResult: unknown = null;
  const sourceResult = prepared.kind === "expected_ready"
    ? await withDocsSourceIdentity({
      expected: prepared.expected,
      observe,
      execute: async (): Promise<
        Operation<
          { output: string; bundle_sha256: string; producer_receipt_sha256: string; files: unknown }
        >
      > => {
        const reply = await dispatchDocsBuild({
          admission,
          attempt: args.attempt,
          wallMs: context.remaining(),
          invoke: context.invoke,
        });
        buildResult = { result: reply.result, receipt: reply.receipt };
        const directory = reply.receipt.path.slice(0, reply.receipt.path.lastIndexOf("/"));
        await Deno.copyFile(`${directory}/stdout.log`, `${args.attempt}/nix.stdout`);
        await Deno.copyFile(`${directory}/stderr.log`, `${args.attempt}/nix.stderr`);
        await Deno.writeTextFile(
          `${args.attempt}/nix-result.json`,
          JSON.stringify(reply.result, null, 2) + "\n",
          { createNew: true, mode: 0o600 },
        );
        if (
          reply.result.reason !== null || !reply.result.exit?.success ||
          reply.result.exit.code !== 0 ||
          reply.result.drain !== "complete" || reply.result.retention !== "acknowledged" ||
          reply.result.errors.length
        ) {
          return { kind: "failed", error: `nix_failed: ${reply.receipt.path}` };
        }
        const output = parseDocsNixOutput(reply.stdout);
        await ancestors(output, true);
        const files = await inventoryTree(`${output}/public`, 10000, 67108864);
        if (files.some((file) => file.bytes > 16777216)) throw new Error("public_file_byte_limit");
        const bundle = await boundedFile(`${output}/public/bundle.json`, 2097152);
        const producer = await boundedFile(`${output}/producer-receipt.json`, 2097152);
        parseDocsJson(new TextDecoder().decode(await readRegularBounded(bundle.path, 2097152)));
        parseDocsJson(new TextDecoder().decode(await readRegularBounded(producer.path, 2097152)));
        return {
          kind: "completed",
          value: {
            output,
            bundle_sha256: bundle.sha256,
            producer_receipt_sha256: producer.sha256,
            files,
          },
        };
      },
    })
    : null;
  await Deno.writeTextFile(
    `${args.attempt}/git-before.json`,
    JSON.stringify(sourceResult?.before ?? initial, null, 2) + "\n",
    { createNew: true, mode: 0o600 },
  );
  await Deno.writeTextFile(
    `${args.attempt}/git-after.json`,
    JSON.stringify(sourceResult?.after ?? null, null, 2) + "\n",
    { createNew: true, mode: 0o600 },
  );
  const terminal = {
    result: sourceResult?.state ?? "blocked_expected_identity",
    source: sourceResult ?? prepared,
    nix: buildResult,
    admission: receipt.admission,
    native_readbacks: `${args.attempt}/native-readbacks.json`,
    elapsed_ms: performance.now() - context.started,
    scientific_acceptance: "not_measured",
    browser_acceptance: "not_measured",
  };
  await Deno.writeTextFile(
    `${args.attempt}/terminal-receipt.json`,
    JSON.stringify(terminal, null, 2) + "\n",
    { createNew: true, mode: 0o600 },
  );
  return terminal;
}
if (import.meta.main) {
  try {
    const args = parseDocsArgs(Deno.args);
    const receipt = await runDocs(args);
    console.log(
      JSON.stringify({
        result: receipt.result,
        receipt: `${args.attempt}/${
          "source" in receipt ? "terminal-receipt.json" : "receipt.json"
        }`,
      }),
    );
    Deno.exitCode = receipt.result === "completed_bound" ? 0 : 2;
  } catch (error) {
    console.error(String(error));
    Deno.exitCode = 1;
  }
}
