// Pure routing contract. Normalized metadata is supplied by a trusted adapter,
// never deserialized as admission authority from caller-controlled JSON.
type Ref = { path: string; sha256: string };
type Tool = Ref & { version: string; receipt_ref: Ref };
type Unit = {
  test_path: string;
  test_sha256: string;
  expected_tests: number;
  report_format: string;
};
type Limits = {
  per_step_wall_seconds: number;
  per_step_log_bytes: number;
  total_log_bytes: number;
  cpu: number;
  ram_bytes: number;
  node_tmp_bytes: number;
  python_tmp_bytes: number;
  doc06_tmp_bytes: number;
};
type Inputs = {
  format: string;
  source_revision: string;
  source_files: Ref[];
  tools: Record<string, Tool>;
  loader_env: Record<string, never>;
  units: Record<string, Unit>;
  katex: {
    root: string;
    version: string;
    module_sha256: string;
    css_sha256: string;
    source_receipt_ref: Ref;
  };
  storage: { owned_tmp_root: string; attempt_dir: string; deno_cache_dir: string };
  admission_ref: Ref;
  limits: Limits;
};
type Graph = { revision: string; digest: string; clean: boolean };
type FileFact = { kind: string; canonical: string; sha256: string };
type DirectoryFact = { kind: string; canonical: string; symlink_ancestors: string[] };
type Metadata = {
  workspace: string;
  source_graph: Graph;
  source_files: Record<string, string>;
  base_task: string;
  files: Record<string, FileFact>;
  directories: Record<string, DirectoryFact>;
  absent_paths: string[];
  retained_tools: Record<
    string,
    {
      ref: Ref;
      path: string;
      version: string;
      sha256: string;
      schema: string;
      externally_measured: boolean;
    }
  >;
  reviewed_units: Record<string, Unit>;
  retained_katex: {
    ref: Ref;
    root: string;
    version: string;
    module_sha256: string;
    css_sha256: string;
  };
  admission: {
    ref: Ref;
    source_revision: string;
    source_graph_digest: string;
    fresh: boolean;
    exclusive_storage: string[];
    tools: Ref[];
    limits: Limits;
    process_tree_supervision: boolean;
  };
};
type Parsed = { inputs: Inputs; input_sha256: string };
type Ready = Parsed & {
  result: string;
  reasons: string[];
  workspace: string;
  source_graph: Graph;
  versions: Record<string, { evidence: string; measurement: null; version: string }>;
  license_status: string;
};
type Step = {
  name: string;
  kind: string;
  executable: string;
  args: string[];
  cwd: string;
  clearEnv: boolean;
  env: Record<string, string>;
  input_sha256: string;
  source_graph_digest: string;
  limits: { wall_seconds: number; log_bytes: number };
  task?: string;
};
type Plan = { mode: "check" | "docs"; scope: string; input_sha256: string; steps: Step[] };
type Capture = {
  stdout: string;
  stderr: string;
  exit_code: number | null;
  signal: string | null;
  started_at: string;
  ended_at: string;
  capture_complete: boolean;
  drains_complete: boolean;
  stop_reason: string | null;
  supervision: { process_tree_owned: boolean; limits_enforced: boolean; evidence_ref: Ref };
};
type Executor = { sourceGraph(): Graph | Promise<Graph>; execute(step: Step): Promise<Capture> };
type Summary = {
  result?: string;
  status?: string;
  reason?: string;
  expected_tests?: number;
  observed_tests?: number;
  passed?: number;
  failed?: number;
  skipped?: number;
  todo?: number | { status: string };
  cancelled?: number | { status: string };
  errors?: number | { status: string };
};
type StepReceipt = {
  name: string;
  result: string;
  summary: Summary;
  capture: Capture | null;
  reason?: string;
  plan: Step;
  input_sha256: string;
  source_revision: string;
  source_graph_digest: string;
  runtime_identity: Tool;
  attempt_identity: string;
  stream_identity?: {
    stdout_sha256: string;
    stderr_sha256: string;
    stdout_bytes: number;
    stderr_bytes: number;
  };
};
const UNIT_NAMES = ["doc04-python", "doc04-node", "doc06-deno"];
const SOURCES = [
  "deno.json",
  "ops/ci.ts",
  "ops/docs_tests.ts",
  "tests/docs_test_routing_test.ts",
  ".github/workflows/ci.yml",
  ".github/workflows/release.yml",
  "tests/test_docs_assembly.py",
  "ops/docs/assemble.py",
  "tests/docs_math_test.mjs",
  "ops/docs/math-render.mjs",
  "tests/docs_static_slice_test.ts",
  "ops/docs/static-slice.ts",
];
const PATHS = [
  "tests/test_docs_assembly.py",
  "tests/docs_math_test.mjs",
  "tests/docs_static_slice_test.ts",
];
const FORMATS = ["python-unittest-summary-v1", "node-test-tap-v1", "deno-test-tap-v1"];
const MODULE_HASH = "cd4b290a4ecf5068161d6a87745655aa74eb18a6e939fa2872d26520ce261b88";
const CSS_HASH = "df9ef84e97d38557de02183e238f8ddfd10988b37741492e12c3157bc856011e";
const MAXIMA: Limits = {
  per_step_wall_seconds: 120,
  per_step_log_bytes: 1048576,
  total_log_bytes: 4194304,
  cpu: 1,
  ram_bytes: 1073741824,
  node_tmp_bytes: 33554432,
  python_tmp_bytes: 33554432,
  doc06_tmp_bytes: 8388608,
};
function requireThat(value: unknown, reason: string): asserts value {
  if (!value) throw new Error(reason);
}
function same(a: unknown, b: unknown): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}
function object(value: unknown, keys: string[]): asserts value is Record<string, unknown> {
  requireThat(
    value !== null && typeof value === "object" && !Array.isArray(value),
    "Expected object",
  );
  requireThat(same(Object.keys(value).sort(), [...keys].sort()), "Missing or additional fields");
}
function hash(value: unknown): asserts value is string {
  requireThat(typeof value === "string" && /^[a-f0-9]{64}$/.test(value), "Invalid SHA256");
}
function absolute(value: unknown): asserts value is string {
  requireThat(
    typeof value === "string" && value.startsWith("/") && value !== "/" &&
      // deno-lint-ignore no-control-regex -- Reject NUL..space/DEL, comma and backslash.
      !/[\x00-\x20\x7f,\\]/.test(value) && !value.endsWith("/") &&
      !value.split("/").slice(1).some((s) => !s || s === "." || s === ".."),
    "Invalid canonical path spelling",
  );
}
function reference(value: unknown): asserts value is Ref {
  object(value, ["path", "sha256"]);
  absolute(value.path);
  hash(value.sha256);
}
function inside(path: string, root: string): boolean {
  return path === root || path.startsWith(root + "/");
}
function overlap(a: string, b: string): boolean {
  return inside(a, b) || inside(b, a);
}

// Strict JSON reader rejects duplicate decoded member names at every level.
function strictJson(text: string): unknown {
  let i = 0;
  const ws = () => {
    while (/[ \t\r\n]/.test(text[i] ?? "") && i < text.length) i++;
  };
  const string = (): string => {
    const start = i++;
    while (i < text.length) {
      if (text[i] === "\\") {
        i += 2;
        continue;
      }
      if (text[i++] === '"') return JSON.parse(text.slice(start, i));
    }
    throw new Error("Unterminated JSON string");
  };
  const value = (): unknown => {
    ws();
    if (text[i] === '"') return string();
    if (text[i] === "{") {
      i++;
      ws();
      const result: Record<string, unknown> = Object.create(null);
      if (text[i] === "}") {
        i++;
        return result;
      }
      while (true) {
        ws();
        requireThat(text[i] === '"', "Expected JSON member");
        const key = string();
        requireThat(!Object.hasOwn(result, key), "Duplicate JSON member");
        ws();
        requireThat(text[i++] === ":", "Expected colon");
        result[key] = value();
        ws();
        const end = text[i++];
        if (end === "}") return result;
        requireThat(end === ",", "Expected comma");
      }
    }
    if (text[i] === "[") {
      i++;
      ws();
      const result: unknown[] = [];
      if (text[i] === "]") {
        i++;
        return result;
      }
      while (true) {
        result.push(value());
        ws();
        const end = text[i++];
        if (end === "]") return result;
        requireThat(end === ",", "Expected comma");
      }
    }
    const token = /^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/.exec(
      text.slice(i),
    );
    requireThat(token, "Invalid JSON token");
    i += token[0].length;
    return JSON.parse(token[0]);
  };
  const result = value();
  ws();
  requireThat(i === text.length, "Trailing JSON data");
  return result;
}

// Synchronous SHA256 keeps parseInputs import-safe and deterministic.
function sha256(text: string): string {
  const data = new TextEncoder().encode(text);
  const bytes = new Uint8Array(Math.ceil((data.length + 9) / 64) * 64);
  bytes.set(data);
  bytes[data.length] = 128;
  const view = new DataView(bytes.buffer);
  view.setUint32(bytes.length - 4, data.length * 8);
  const h = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19,
  ];
  const k = [
    0x428a2f98,
    0x71374491,
    0xb5c0fbcf,
    0xe9b5dba5,
    0x3956c25b,
    0x59f111f1,
    0x923f82a4,
    0xab1c5ed5,
    0xd807aa98,
    0x12835b01,
    0x243185be,
    0x550c7dc3,
    0x72be5d74,
    0x80deb1fe,
    0x9bdc06a7,
    0xc19bf174,
    0xe49b69c1,
    0xefbe4786,
    0x0fc19dc6,
    0x240ca1cc,
    0x2de92c6f,
    0x4a7484aa,
    0x5cb0a9dc,
    0x76f988da,
    0x983e5152,
    0xa831c66d,
    0xb00327c8,
    0xbf597fc7,
    0xc6e00bf3,
    0xd5a79147,
    0x06ca6351,
    0x14292967,
    0x27b70a85,
    0x2e1b2138,
    0x4d2c6dfc,
    0x53380d13,
    0x650a7354,
    0x766a0abb,
    0x81c2c92e,
    0x92722c85,
    0xa2bfe8a1,
    0xa81a664b,
    0xc24b8b70,
    0xc76c51a3,
    0xd192e819,
    0xd6990624,
    0xf40e3585,
    0x106aa070,
    0x19a4c116,
    0x1e376c08,
    0x2748774c,
    0x34b0bcb5,
    0x391c0cb3,
    0x4ed8aa4a,
    0x5b9cca4f,
    0x682e6ff3,
    0x748f82ee,
    0x78a5636f,
    0x84c87814,
    0x8cc70208,
    0x90befffa,
    0xa4506ceb,
    0xbef9a3f7,
    0xc67178f2,
  ];
  const r = (x: number, n: number) => (x >>> n) | (x << (32 - n));
  for (let offset = 0; offset < bytes.length; offset += 64) {
    const w = new Uint32Array(64);
    for (let j = 0; j < 16; j++) w[j] = view.getUint32(offset + j * 4);
    for (let j = 16; j < 64; j++) {
      const x = w[j - 15], y = w[j - 2];
      w[j] = (w[j - 16] + (r(x, 7) ^ r(x, 18) ^ (x >>> 3)) + w[j - 7] +
        (r(y, 17) ^ r(y, 19) ^ (y >>> 10))) >>> 0;
    }
    let [a, b, c, d, e, f, g, z] = h;
    for (let j = 0; j < 64; j++) {
      const t1 = (z + (r(e, 6) ^ r(e, 11) ^ r(e, 25)) + ((e & f) ^ (~e & g)) + k[j] + w[j]) >>> 0;
      const t2 = ((r(a, 2) ^ r(a, 13) ^ r(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) >>> 0;
      z = g;
      g = f;
      f = e;
      e = (d + t1) >>> 0;
      d = c;
      c = b;
      b = a;
      a = (t1 + t2) >>> 0;
    }
    [a, b, c, d, e, f, g, z].forEach((v, j) => h[j] = (h[j] + v) >>> 0);
  }
  return h.map((v) => v.toString(16).padStart(8, "0")).join("");
}

export function genericCheckPlan() {
  const excluded = ["tests/docs_math_test.mjs", "tests/docs_static_slice_test.ts"];
  return {
    excluded,
    command: "deno fmt --check ops tests deno.json && deno lint ops tests && " +
      "deno check ops/*.ts && deno test --allow-read --allow-write --allow-run=git " +
      "--ignore=tests/docs_math_test.mjs --ignore=tests/docs_static_slice_test.ts tests && " +
      "deno task transfer:check && deno task restore:check",
  };
}
export function parseInputs(text: string): Parsed {
  requireThat(new TextEncoder().encode(text).length <= 32768, "Descriptor exceeds 32KiB");
  const d = strictJson(text);
  object(d, [
    "format",
    "source_revision",
    "source_files",
    "tools",
    "loader_env",
    "units",
    "katex",
    "storage",
    "admission_ref",
    "limits",
  ]);
  requireThat(d.format === "qcl-negf.docs-test-inputs.v1", "Unknown descriptor format");
  requireThat(
    typeof d.source_revision === "string" && /^[a-f0-9]{40}$/.test(d.source_revision),
    "Invalid revision",
  );
  requireThat(
    Array.isArray(d.source_files) && d.source_files.length === SOURCES.length,
    "Exact source closure required",
  );
  for (const item of d.source_files) {
    object(item, ["path", "sha256"]);
    hash(item.sha256);
  }
  requireThat(
    same(d.source_files.map((s) => s.path).sort(), [...SOURCES].sort()),
    "Invalid source paths",
  );
  object(d.loader_env, []);
  object(d.tools, ["deno", "node", "python"]);
  for (const tool of Object.values(d.tools)) {
    object(tool, ["path", "version", "sha256", "receipt_ref"]);
    absolute(tool.path);
    hash(tool.sha256);
    requireThat(
      typeof tool.version === "string" && /^\d+\.\d+\.\d+$/.test(tool.version),
      "Invalid version",
    );
    reference(tool.receipt_ref);
  }
  object(d.units, UNIT_NAMES);
  const units = d.units;
  UNIT_NAMES.forEach((name, index) => {
    const unit = units[name];
    object(unit, ["test_path", "test_sha256", "expected_tests", "report_format"]);
    requireThat(
      unit.test_path === PATHS[index] && unit.report_format === FORMATS[index],
      "Invalid unit contract",
    );
    hash(unit.test_sha256);
    requireThat(
      Number.isSafeInteger(unit.expected_tests) && Number(unit.expected_tests) > 0,
      "Positive count required",
    );
  });
  object(d.katex, ["root", "version", "module_sha256", "css_sha256", "source_receipt_ref"]);
  absolute(d.katex.root);
  hash(d.katex.module_sha256);
  hash(d.katex.css_sha256);
  reference(d.katex.source_receipt_ref);
  requireThat(d.katex.version === "0.16.8", "Wrong KaTeX version");
  object(d.storage, ["owned_tmp_root", "attempt_dir", "deno_cache_dir"]);
  Object.values(d.storage).forEach(absolute);
  reference(d.admission_ref);
  object(d.limits, Object.keys(MAXIMA));
  for (const [key, max] of Object.entries(MAXIMA)) {
    const value = d.limits[key];
    requireThat(
      Number.isSafeInteger(value) && Number(value) > 0 && Number(value) <= max,
      "Invalid limit",
    );
  }
  return { inputs: d as unknown as Inputs, input_sha256: sha256(text) };
}

export function preflightInputs(parsed: Parsed, m: Metadata): Ready {
  const d = parsed.inputs, reasons: string[] = [];
  const check = (ok: unknown, reason: string) => {
    if (!ok) reasons.push(reason);
  };
  const file = (path: string, digest: string) => {
    const f = m.files[path];
    check(
      f && f.kind === "regular" && f.canonical === path && f.sha256 === digest,
      `File binding: ${path}`,
    );
  };
  const ref = (r: Ref) => file(r.path, r.sha256);
  const directory = (path: string) => {
    const f = m.directories[path];
    check(
      f && f.kind === "directory" && f.canonical === path && f.symlink_ancestors.length === 0,
      `Directory binding: ${path}`,
    );
  };
  check(
    m.source_graph.clean && m.source_graph.revision === d.source_revision,
    "Source graph mismatch",
  );
  check(/^[a-f0-9]{64}$/.test(m.source_graph.digest), "Missing graph digest");
  check(m.base_task === genericCheckPlan().command, "Base task changed");
  for (const s of d.source_files) {
    check(m.source_files[s.path] === s.sha256, `Source bytes: ${s.path}`);
  }
  directory(m.workspace);
  for (const [name, tool] of Object.entries(d.tools)) {
    file(tool.path, tool.sha256);
    ref(tool.receipt_ref);
    const retained = m.retained_tools[name];
    check(
      retained && retained.schema === "normalized-tool-identity" && retained.externally_measured &&
        same(retained.ref, tool.receipt_ref) && retained.path === tool.path &&
        retained.version === tool.version &&
        retained.sha256 === tool.sha256,
      `Retained tool: ${name}`,
    );
    check(
      name === "deno"
        ? tool.version === "2.8.3"
        : new RegExp(name === "node" ? "^24\\." : "^3\\.14\\.").test(tool.version),
      `Tool version: ${name}`,
    );
  }
  for (const name of UNIT_NAMES) {
    const unit = d.units[name];
    check(
      d.source_files.find((s) => s.path === unit.test_path)?.sha256 === unit.test_sha256 &&
        same(unit, m.reviewed_units[name]),
      `Reviewed source-bound count: ${name}`,
    );
  }
  const k = d.katex;
  directory(k.root);
  ref(k.source_receipt_ref);
  check(
    k.module_sha256 === MODULE_HASH && k.css_sha256 === CSS_HASH,
    "KaTeX exact hashes required",
  );
  file(`${k.root}/dist/katex.mjs`, k.module_sha256);
  file(`${k.root}/dist/katex.min.css`, k.css_sha256);
  check(
    same(m.retained_katex, {
      ref: k.source_receipt_ref,
      root: k.root,
      version: k.version,
      module_sha256: k.module_sha256,
      css_sha256: k.css_sha256,
    }),
    "Retained KaTeX mismatch",
  );
  const storage = Object.values(d.storage);
  check(
    d.storage.owned_tmp_root.startsWith("/tmp/") && d.storage.owned_tmp_root !== "/tmp",
    "Unique /tmp descendant required",
  );
  for (const path of storage) check(!overlap(path, m.workspace), "Storage overlaps workspace");
  for (let i = 0; i < storage.length; i++) {
    for (let j = i + 1; j < storage.length; j++) {
      check(!overlap(storage[i], storage[j]), "Storage domains overlap");
    }
  }
  directory(d.storage.owned_tmp_root);
  directory(d.storage.deno_cache_dir);
  directory(d.storage.attempt_dir.slice(0, d.storage.attempt_dir.lastIndexOf("/")));
  for (
    const path of [
      d.storage.attempt_dir,
      ...["node", "python", "doc06"].map((n) => `${d.storage.owned_tmp_root}/${n}`),
    ]
  ) check(m.absent_paths.includes(path), "Fresh exclusive child required");
  ref(d.admission_ref);
  const a = m.admission;
  check(
    a && same(a.ref, d.admission_ref) && a.fresh && a.process_tree_supervision &&
      a.source_revision === d.source_revision && a.source_graph_digest === m.source_graph.digest,
    "Trusted active admission missing",
  );
  if (a) {
    for (const path of storage) check(a.exclusive_storage.includes(path), "Storage not admitted");
    for (const tool of Object.values(d.tools)) {
      check(
        a.tools.some((t) => t.path === tool.path && t.sha256 === tool.sha256),
        "Tool not admitted",
      );
    }
    for (const key of Object.keys(MAXIMA) as (keyof Limits)[]) {
      check(a.limits[key] >= d.limits[key], "Limits not admitted");
    }
  }
  return {
    ...parsed,
    result: reasons.length ? "blocked" : "ready_for_unit_attempt",
    reasons,
    workspace: m.workspace,
    source_graph: structuredClone(m.source_graph),
    versions: Object.fromEntries(
      Object.entries(d.tools).map(([name, t]) => [name, {
        evidence: "retained_receipt_bound",
        measurement: null,
        version: t.version,
      }]),
    ),
    license_status: "not_evaluated",
  };
}

export function planChecks(mode: "check" | "docs", r: Ready | null): Plan {
  requireThat(
    r?.result === "ready_for_unit_attempt",
    "Prepared exact inputs and trusted admission required",
  );
  requireThat(mode === "check" || mode === "docs", "Unknown check mode");
  const d = r.inputs, tmp = d.storage.owned_tmp_root, root = r.workspace;
  const test = `${root}/${PATHS[2]}`, adapter = `${root}/ops/docs/static-slice.ts`;
  const step = (
    name: string,
    executable: string,
    args: string[],
    env: Record<string, string>,
    clearEnv = true,
  ): Step => ({
    name,
    kind: name === "base" ? "base-task" : "dedicated-unit",
    executable,
    args,
    cwd: root,
    env,
    clearEnv,
    input_sha256: r.input_sha256,
    source_graph_digest: r.source_graph.digest,
    limits: {
      wall_seconds: d.limits.per_step_wall_seconds,
      log_bytes: d.limits.per_step_log_bytes,
    },
    ...(name === "base" ? { task: "check:base" } : {}),
  });
  const steps = [
    step("doc04-python", d.tools.python.path, [
      "-m",
      "unittest",
      "discover",
      "-s",
      "tests",
      "-p",
      "test_docs_assembly.py",
    ], { TMPDIR: `${tmp}/python`, PYTHONNOUSERSITE: "1", PYTHONDONTWRITEBYTECODE: "1" }),
    step("doc04-node", d.tools.node.path, ["--test", "--test-reporter=tap", PATHS[1]], {
      DOC04_KATEX_ROOT: d.katex.root,
      TMPDIR: `${tmp}/node`,
    }),
    step("doc06-deno", d.tools.deno.path, [
      "test",
      "--no-config",
      "--no-lock",
      "--cached-only",
      "--no-npm",
      "--no-remote",
      "--reporter=tap",
      `--allow-read=${test},${adapter},${tmp}/doc06`,
      `--allow-write=${tmp}/doc06`,
      test,
      "--",
      `${tmp}/doc06`,
    ], { DENO_DIR: d.storage.deno_cache_dir }),
  ];
  if (mode === "check") {
    steps.unshift(step("base", d.tools.deno.path, ["task", "check:base"], {}, false));
  }
  return {
    mode,
    scope: mode === "check" ? "full-root-check" : "docs-units-only",
    input_sha256: r.input_sha256,
    steps,
  };
}
export function validatePlan(p: Plan, r: Ready): void {
  requireThat(same(p, planChecks(p.mode, r)), "Plan differs from exact reviewed routes");
}
export function parseUnitReport(
  format: string,
  stdout: string,
  stderr: string,
  expected: number,
): Summary {
  requireThat(Number.isSafeInteger(expected) && expected > 0, "Positive reviewed count required");
  const na = { status: "not_applicable" };
  const result: Summary = {
    result: "passed_unit",
    expected_tests: expected,
    observed_tests: expected,
    passed: expected,
    failed: 0,
    skipped: 0,
    todo: na,
    cancelled: na,
    errors: na,
  };
  if (format === FORMATS[0]) {
    const match = /^\.*\n-{70}\nRan (\d+) tests? in \d+(?:\.\d+)?s\n\nOK\n$/.exec(stderr);
    requireThat(match && Number(match[1]) === expected, "Unknown or unsuccessful unittest summary");
    result.errors = 0;
    return result;
  }
  requireThat(format === FORMATS[1] || format === FORMATS[2], "Unknown report format");
  requireThat(
    !stderr.trim() && !/Bail out!|not ok/im.test(stdout) &&
      !/^ok [^\n]*#[ \t]*(?:SKIP|TODO)\b/im.test(stdout),
    "Unsuccessful TAP",
  );
  const lines = stdout.trimEnd().split("\n");
  requireThat(
    lines.shift() === (format === FORMATS[1] ? "TAP version 13" : "TAP version 14"),
    "Unknown TAP version",
  );
  if (format === FORMATS[2]) {
    requireThat(lines.shift() === `# ./${PATHS[2]}`, "Unknown Deno TAP file header");
  }
  const plans = lines.filter((s) => /^1\.\./.test(s));
  requireThat(plans.length === 1 && plans[0] === `1..${expected}`, "Invalid TAP plan");
  const tests = lines.filter((s) => /^ok /.test(s));
  requireThat(
    tests.length === expected && tests.every((s, i) => new RegExp(`^ok ${i + 1} - .+$`).test(s)),
    "Invalid TAP cases",
  );
  if (format === FORMATS[1]) {
    const counters: Record<string, number> = {
      tests: expected,
      suites: 0,
      pass: expected,
      fail: 0,
      cancelled: 0,
      skipped: 0,
      todo: 0,
    };
    for (const [key, value] of Object.entries(counters)) {
      requireThat(
        lines.filter((s) => s.startsWith(`# ${key} `)).length === 1 &&
          lines.includes(`# ${key} ${value}`),
        "Missing or inconsistent Node counter",
      );
    }
    requireThat(
      lines.every((s) =>
        /^ok \d+ - .+$|^# Subtest: .+$|^1\.\.\d+$|^# (?:tests|suites|pass|fail|cancelled|skipped|todo) \d+$|^# duration_ms \d+(?:\.\d+)?$/
          .test(s)
      ),
      "Unknown Node TAP layout",
    );
    result.cancelled = 0;
  } else {requireThat(
      lines.every((s) => /^ok \d+ - .+$|^1\.\.\d+$/.test(s)),
      "Unknown Deno TAP layout",
    );}
  result.todo = 0;
  return result;
}

export async function runChecks(p: Plan, r: Ready, executor: Executor) {
  validatePlan(p, r);
  const receipts: StepReceipt[] = p.steps.map((s) => ({
    name: s.name,
    result: "blocked",
    summary: {},
    capture: null,
    plan: structuredClone(s),
    input_sha256: r.input_sha256,
    source_revision: r.inputs.source_revision,
    source_graph_digest: r.source_graph.digest,
    runtime_identity: structuredClone(
      r.inputs
        .tools[s.name === "doc04-node" ? "node" : s.name === "doc04-python" ? "python" : "deno"],
    ),
    attempt_identity: r.inputs.storage.attempt_dir,
  }));
  let sourceObservation = { status: "measured", reason: "" };
  const observeSource = async (): Promise<boolean> => {
    try {
      return same(await executor.sourceGraph(), r.source_graph);
    } catch (error) {
      sourceObservation = {
        status: "not_measured",
        reason: error instanceof Error ? error.message : "Source reader failed",
      };
      return false;
    }
  };
  let stable = await observeSource(), total = 0, stopped = !stable;
  for (let i = 0; i < p.steps.length; i++) {
    const step = p.steps[i], receipt = receipts[i];
    if (stopped) continue;
    try {
      const c = await executor.execute(structuredClone(step));
      receipt.capture = c;
      receipt.stream_identity = {
        stdout_sha256: sha256(c.stdout),
        stderr_sha256: sha256(c.stderr),
        stdout_bytes: new TextEncoder().encode(c.stdout).length,
        stderr_bytes: new TextEncoder().encode(c.stderr).length,
      };
      total += new TextEncoder().encode(c.stdout).length +
        new TextEncoder().encode(c.stderr).length;
      stable = (await observeSource()) && stable;
      const elapsed = Date.parse(c.ended_at) - Date.parse(c.started_at);
      requireThat(
        c.exit_code === 0 && c.signal === null && c.stop_reason === null &&
          c.capture_complete && c.drains_complete && c.supervision.process_tree_owned &&
          c.supervision.limits_enforced &&
          /^[a-f0-9]{64}$/.test(c.supervision.evidence_ref.sha256) &&
          Number.isFinite(elapsed) && elapsed >= 0 && elapsed <= step.limits.wall_seconds * 1000 &&
          new TextEncoder().encode(c.stdout).length <= step.limits.log_bytes &&
          new TextEncoder().encode(c.stderr).length <= step.limits.log_bytes &&
          total <= r.inputs.limits.total_log_bytes && stable,
        "Execution/capture/source guards failed",
      );
      receipt.summary = step.name === "base"
        ? { status: "not_applicable", reason: "composite-task" }
        : parseUnitReport(
          r.inputs.units[step.name].report_format,
          c.stdout,
          c.stderr,
          r.inputs.units[step.name].expected_tests,
        );
      receipt.result = step.name === "base" ? "passed_base" : "passed_unit";
    } catch (error) {
      receipt.result = "failed";
      receipt.reason = error instanceof Error ? error.message : "Execution failure";
      stopped = true;
    }
  }
  stable = (await observeSource()) && stable;
  return {
    scope: p.scope,
    result: stable &&
        receipts.every((s) => s.result === (s.name === "base" ? "passed_base" : "passed_unit"))
      ? "passed"
      : "failed",
    required_steps: p.steps.map((s) => s.name),
    steps: receipts,
    source_stable: stable,
    source_observation: sourceObservation,
    input_sha256: r.input_sha256,
    source_revision: r.inputs.source_revision,
    source_graph_digest: r.source_graph.digest,
    base: p.mode === "docs" ? "not_requested" : receipts[0].result,
    retained: {
      attempt_dir: r.inputs.storage.attempt_dir,
      owned_tmp_root: r.inputs.storage.owned_tmp_root,
      cleanup_attempted: false,
    },
  };
}
export function parseCiArgs(args: string[]) {
  const scopes: string[] = [];
  let docsInputs: string | null = null;
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--docs-inputs") {
      requireThat(
        docsInputs === null && i + 1 < args.length && !args[i + 1].startsWith("--"),
        "Expected one docs inputs file",
      );
      docsInputs = args[++i];
      requireThat(docsInputs.length > 0, "Empty docs inputs");
    } else {
      requireThat(
        ["--python", "--julia", "--infra"].includes(a) && !scopes.includes(a.slice(2)),
        "Unknown or duplicate scope",
      );
      scopes.push(a.slice(2));
    }
  }
  requireThat(
    scopes.length ? docsInputs === null : docsInputs !== null,
    "Full checks require --docs-inputs FILE; targeted scopes cannot consume it",
  );
  return { all: scopes.length === 0, scopes, docsInputs };
}
export function workflowRoute(
  mode: "full" | "application-release" | "runner-smoke",
  file: string | null,
) {
  if (mode === "runner-smoke") {
    return {
      scope: "base-only",
      base: ["deno", "task", "check:base"],
      aggregateExecutions: 0,
      dedicatedUnits: "not_requested",
      preflight: null,
      cancelInProgress: false,
    };
  }
  requireThat(
    (mode === "full" || mode === "application-release") && file,
    "Prepared docs inputs required",
  );
  return {
    scope: "full-root-check",
    preflight: ["deno", "task", "docs:preflight", "--inputs", file],
    aggregate: ["deno", "task", "test", "--docs-inputs", file],
    aggregateExecutions: 1,
    standaloneCheckExecutions: 0,
    order: ["source-graph", "docs-preflight", "prepare", "full-aggregate"],
    cancelInProgress: false,
  };
}
