// DOC06 source-only controls. Target sources are inert fixture bytes.
// No std/downloaded modules, process/env/network/FFI capabilities are needed.
import { generateStaticSlice } from "../ops/docs/static-slice.ts";

type Fact = { name: string; status: string; text: string; sources: unknown[] };
type Extraction = {
  subject: string;
  fact_index: number;
  mode: "literal-extraction" | "authored-context" | "dynamic-unknown";
  context: string;
  value: unknown;
  reason?: string;
  selector?: string;
};
type Projection = {
  format: string;
  profile: string;
  subjects: { kind: string; key: string; facts: Fact[] }[];
  coverage: { fact_classes: string[]; scope: string; status: string };
  binding: { status: string; application_release: null; run: null };
};
type Receipt = {
  result: string;
  inputs: {
    path: string;
    actual_sha256: string | null;
    actual_bytes: number | null;
    status: string;
  }[];
  extractions: Extraction[];
  diagnostics?: { reason: string }[];
};
type Run = {
  status: string;
  reason?: string;
  facts?: Projection;
  receipt?: Receipt;
  bytes?: string;
};
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
const API = "configuration_source";
const INPUT = "production.energy_chunk";
const REVISION = {
  runner: "1acc165650fd4f4c2d49605cc679f90e3f6fcdae",
  contracts: "12fc26462bbab3df76904c6deb01f8c6596de7be",
  core: "e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee",
};
const OWNER = {
  runner: "components/QCLNEGFRunner.jl",
  contracts: "components/qcl-negf-contracts",
  core: "components/QCLNEGF.jl",
};
// Mandatory pre-created harness-owned /tmp capability, covered by its 8 MiB sampler.
// No environment lookup, implicit temp directory, or worktree write fallback.
const TMP = Deno.args[0];
if (!TMP || !TMP.startsWith("/tmp/") || Deno.args.length !== 1) {
  throw new Error("pass exactly one harness-owned /tmp capability after --");
}
const encoder = new TextEncoder();
function assert(ok: unknown, message = "assertion failed"): asserts ok {
  if (!ok) throw new Error(message);
}
function equal(actual: unknown, expected: unknown, message: string) {
  assert(
    JSON.stringify(actual) === JSON.stringify(expected),
    `${message}: got ${JSON.stringify(actual)}, wanted ${JSON.stringify(expected)}`,
  );
}
async function hash(bytes: Uint8Array): Promise<string> {
  const owned = new Uint8Array(bytes.length);
  owned.set(bytes);
  const result = new Uint8Array(await crypto.subtle.digest("SHA-256", owned.buffer));
  return Array.from(result, (b) => b.toString(16).padStart(2, "0")).join("");
}
function schema(
  leaf =
    '"type":"integer","minimum":1,"description":"Maximum number of energy points in one scheduling chunk; not an energy spacing. No schema default."',
): string {
  return `{"type":"object","required":["production"],"properties":{"production":{"$ref":"#/$defs/production"}},"$defs":{"production":{"type":"object","required":["energy_chunk"],"properties":{"energy_chunk":{${leaf}}}}}}`;
}
function sources(typed = 64, example = 64): Record<string, string> {
  const json = schema();
  return {
    [PATHS[0]]:
      `"""\n    configuration_source(configuration, dotted_path)\n\nReturn the last recorded assigning source identifier, or nothing when history is absent or empty.\nThis lookup does not load or validate sources and does not establish an effective origin.\n"""\nfunction configuration_source(\n    configuration::ResolvedRunConfiguration,\n    dotted_path::AbstractString,\n)\n    history = get(configuration.source_history, String(dotted_path), nothing)\n    return isnothing(history) || isempty(history) ? nothing : last(history)\nend\n`,
    [PATHS[1]]:
      `function _deep_merge!(target, source, source_file)\n    # Source observation only; fixture must never invoke this body.\n    assigning_identifier = abspath(source_file)\nend\n`,
    [PATHS[2]]: "# Ordered sources are collected, merged, validated, then resolved.\n",
    [PATHS[3]]:
      "# Selected execution plan can replace energy_chunk and record application:auto_exact.\n",
    [PATHS[4]]:
      "# Run configurations\nLater source files override explicit fields. configuration_source returns the last recorded assigning identifier, not a complete effective origin.\n\nSynthetic example: production.energy_chunk is 17 in first.yaml and 23 in second.yaml; the expected final explicit value is 23. This is a synthetic source example, not a measured run.\n",
    [PATHS[5]]: `production:\n  energy_chunk: ${example}\nother:\n  energy_chunk: 123\n`,
    [PATHS[6]]: json,
    [PATHS[7]]: json,
    [PATHS[8]]:
      `"""Production operators without changing the physical model."""\nBase.@kwdef struct ProductionOptions\n    energy_chunk::Int = ${typed}\n    residual_chunk::Int = 256\nend\nfunction _check_production_options(options::ProductionOptions)\n    options.energy_chunk > 0 || throw(ArgumentError("energy_chunk must be positive"))\nend\n`,
  };
}
async function write(path: string, bytes: string | Uint8Array) {
  await Deno.mkdir(path.slice(0, path.lastIndexOf("/")), { recursive: true });
  await Deno.writeFile(path, typeof bytes === "string" ? encoder.encode(bytes) : bytes);
}
async function exists(path: string): Promise<boolean> {
  try {
    await Deno.lstat(path);
    return true;
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) return false;
    throw error;
  }
}
type Entry = { path: string; owner: string; revision: string; sha256: string; bytes: number };
class Fixture {
  constructor(readonly dir: string, readonly text: Record<string, string>) {}
  entries: Entry[] = [];
  get snapshot() {
    return `${this.dir}/snapshot`;
  }
  get sourceReceipt() {
    return `${this.dir}/input-receipt.json`;
  }
  async prepare() {
    for (const path of PATHS) {
      const bytes = encoder.encode(this.text[path]);
      const alias = path.split("/")[0] as keyof typeof OWNER;
      await write(`${this.snapshot}/${path}`, bytes);
      this.entries.push({
        path,
        owner: OWNER[alias],
        revision: REVISION[alias],
        sha256: await hash(bytes),
        bytes: bytes.length,
      });
    }
    await this.receipt();
  }
  async receipt() {
    await write(
      this.sourceReceipt,
      JSON.stringify(
        {
          format: "qcl-negf.doc06-source-input.v1",
          source_graph_sha256: "a".repeat(64),
          files: this.entries,
        },
        null,
        2,
      ) + "\n",
    );
  }
  async run(label = "out"): Promise<Run> {
    const outDir = `${this.dir}/${label}`;
    const result = await generateStaticSlice({
      snapshotDir: this.snapshot,
      sourceReceiptPath: this.sourceReceipt,
      outDir,
    });
    assert(["produced", "partial", "refused"].includes(result.status), "explicit bounded result");
    if (result.status === "refused") {
      assert(!await exists(`${outDir}/facts.json`), "refusal cannot publish facts");
      return result;
    }
    const bytes = await Deno.readTextFile(`${outDir}/facts.json`);
    const receiptBytes = await Deno.readTextFile(`${outDir}/source-receipt.json`);
    assert(encoder.encode(bytes).length <= 32768, "facts output cap");
    assert(encoder.encode(receiptBytes).length <= 32768, "receipt output cap");
    const facts = JSON.parse(bytes) as Projection;
    const receipt = JSON.parse(receiptBytes) as Receipt;
    equal(receipt.result, result.status, "receipt/result coherence");
    return { ...result, facts, receipt, bytes };
  }
}
async function fixture(body: (f: Fixture) => Promise<void>, text = sources()) {
  const dir = await Deno.makeTempDir({ dir: TMP, prefix: "slice-" });
  let completed = false;
  try {
    const f = new Fixture(dir, text);
    await f.prepare();
    await body(f);
    completed = true;
  } finally {
    // Preserve failed-case evidence for the coordinator; never remove raw logs.
    if (completed) await Deno.remove(dir, { recursive: true });
  }
}
async function preparedSymlinkFixture(
  kind: "file" | "directory",
  body: (f: Fixture) => Promise<void>,
) {
  // Fixed external seeds only. No child link creation, rename, repair or fallback.
  equal(await Deno.realPath(TMP), TMP, "owned TMP is canonical");
  const tmpInfo = await Deno.lstat(TMP);
  assert(tmpInfo.isDirectory && !tmpInfo.isSymlink, "owned TMP is a real directory");
  const dir = `${TMP}/prepared-symlink-${kind}`;
  const directoryInfo = await Deno.lstat(dir);
  assert(
    directoryInfo.isDirectory && !directoryInfo.isSymlink,
    "prepared root is a real directory",
  );
  const file = kind === "file";
  const linkRelative = file
    ? "snapshot/runner/src/application/configuration_types.jl"
    : "snapshot/core";
  const backingRelative = file ? "backing/configuration_types.jl" : "backing/core";
  const linkText = file ? "../../../../backing/configuration_types.jl" : "../backing/core";
  const expectedDirectories = file
    ? [
      "backing",
      "snapshot",
      "snapshot/runner",
      "snapshot/runner/src",
      "snapshot/runner/src/application",
    ]
    : ["backing", "backing/core", "snapshot"];
  const expected = new Map<string, string>(expectedDirectories.map((path) => [path, "directory"]));
  expected.set(linkRelative, "symlink");
  if (file) expected.set(backingRelative, "file");
  const observed = new Map<string, string>();
  async function inventory(relative: string): Promise<void> {
    for await (const entry of Deno.readDir(relative ? `${dir}/${relative}` : dir)) {
      const path = relative ? `${relative}/${entry.name}` : entry.name;
      const info = await Deno.lstat(`${dir}/${path}`);
      const type = info.isSymlink
        ? "symlink"
        : info.isDirectory
        ? "directory"
        : info.isFile
        ? "file"
        : "special";
      equal(type, expected.get(path), "unexpected or changed seed node blocks before traversal");
      observed.set(path, type);
      if (type === "directory") await inventory(path);
    }
  }
  await inventory("");
  equal([...observed].sort(), [...expected].sort(), "exact no-follow prepared inventory");
  for (const path of expectedDirectories) {
    const absolute = `${dir}/${path}`;
    equal(
      await Deno.realPath(absolute),
      absolute,
      "prepared ancestor stays real/canonical inside TMP",
    );
  }
  const link = `${dir}/${linkRelative}`, backing = `${dir}/${backingRelative}`;
  async function topology() {
    assert((await Deno.lstat(link)).isSymlink, "negative source remains a real link");
    equal(await Deno.readLink(link), linkText, "exact relative seed link text");
    equal(await Deno.realPath(link), backing, "exact live backing target inside same TMP fixture");
    const target = await Deno.lstat(backing);
    assert(
      !target.isSymlink && (file ? target.isFile : target.isDirectory),
      "ordinary live backing target type",
    );
  }
  await topology();
  if (file) equal((await Deno.lstat(backing)).size, 0, "baseline regular seed bytes are zero");
  const f = new Fixture(dir, sources());
  await f.prepare();
  await topology();
  // Read real bytes of all nine aliases and compare with existing receipt entries,
  // not just two independently computed hashes of the authored literal string.
  for (const path of PATHS) {
    const actual = await Deno.readFile(`${f.snapshot}/${path}`);
    const entry = f.entries.find((candidate) => candidate.path === path)!;
    equal(
      new TextDecoder("utf-8", { fatal: true }).decode(actual),
      f.text[path],
      "selected literal bytes readable",
    );
    equal(actual.length, entry.bytes, "actual selected byte length matches receipt");
    equal(await hash(actual), entry.sha256, "actual selected SHA matches receipt");
    if (!(file && path === PATHS[0])) {
      const info = await Deno.lstat(`${f.snapshot}/${path}`);
      assert(info.isFile && !info.isSymlink, "every non-link selected leaf remains regular");
    }
  }
  const selectedPath = file ? PATHS[0] : PATHS[8];
  const directBacking = file ? backing : `${backing}/${selectedPath.slice("core/".length)}`;
  const directBytes = await Deno.readFile(directBacking);
  const selectedEntry = f.entries.find((entry) => entry.path === selectedPath)!;
  equal(
    new TextDecoder("utf-8", { fatal: true }).decode(directBytes),
    f.text[selectedPath],
    "direct backing has exact selected literal",
  );
  equal(directBytes.length, selectedEntry.bytes, "backing byte length matches receipt");
  equal(await hash(directBytes), selectedEntry.sha256, "backing SHA matches receipt");
  equal(
    await Deno.readTextFile(`${f.snapshot}/${selectedPath}`),
    f.text[selectedPath],
    "alias has exact same literal",
  );
  await body(f);
  // Both finite prepared trees are retained on success and failure for receipts.
}
function facts(run: Run, key: string): Fact[] {
  assert(run.status !== "refused", `projection required: ${run.reason}`);
  const subject = run.facts!.subjects.find((s) => s.key === key);
  assert(subject, `subject ${key} present`);
  return subject.facts;
}
function extraction(run: Run, key: string, context: string): Extraction {
  const records = run.receipt!.extractions.filter((e) =>
    e.subject === key && e.context === context
  );
  equal(records.length, 1, `one extraction for ${key}/${context}`);
  return records[0];
}
function literal(run: Run, context: string, value: unknown) {
  const entry = extraction(run, INPUT, context);
  equal(entry.mode, "literal-extraction", `${context} is literal`);
  equal(entry.value, value, `${context} value independently expected`);
  equal(facts(run, INPUT)[entry.fact_index].status, "known", `${context} source fact known`);
}
function unsupported(
  run: Run,
  key: string,
  context: string,
  reason?: string,
  allowRefusal = false,
) {
  if (run.status === "refused") {
    assert(allowRefusal, `${context}: this unsupported construct must preserve partial projection`);
    assert(run.reason, "refusal has reason");
    return;
  }
  const entry = extraction(run, key, context);
  equal(entry.value, null, `${context}: no stale or computed value`);
  assert(
    ["partial", "unknown"].includes(facts(run, key)[entry.fact_index].status),
    `${context}: unsupported must not become known/pass`,
  );
  assert(
    entry.reason && (!reason || entry.reason === reason),
    `${context}: explicit reason ${reason ?? "required"}`,
  );
}

// Catches constant-64 implementations, class loss, fabricated origins, and nondeterminism.
Deno.test("DOC06 positive: source numbers stay separate and all ten classes survive", async () => {
  for (const [typed, example] of [[64, 64], [79, 31], [101, 47]]) {
    await fixture(async (f) => {
      const run = await f.run();
      equal(run.facts!.format, "qcl-negf.doc06-static-slice.v1", "private prototype format");
      equal(run.facts!.profile, "configuration-source-energy-chunk-v1", "fixed scope");
      equal(run.facts!.binding, {
        status: "source-prototype",
        application_release: null,
        run: null,
      }, "no fabricated run/release");
      for (const key of [API, INPUT]) {
        const fs = facts(run, key);
        equal(
          [...new Set(fs.map((x) => x.name))].sort(),
          [...CLASSES].sort(),
          "all ten fact classes",
        );
        for (const fact of fs) {
          equal(
            Object.keys(fact).sort(),
            ["name", "sources", "status", "text"],
            "Fact shape unchanged",
          );
          assert(fact.text.length <= 2048, "fact text bounded");
        }
        assert(
          fs.some((x) => x.name === "effective_origin" && x.status === "unknown"),
          "effective context absent",
        );
      }
      const api = extraction(run, API, "documented-signature");
      equal(
        api.value,
        "configuration_source(configuration, dotted_path)",
        "documented two-argument signature",
      );
      equal(facts(run, API)[api.fact_index].status, "known", "documented signature known");
      equal(
        facts(run, API)[extraction(run, API, "typed-signature").fact_index].status,
        "partial",
        "typed declaration is not method inventory",
      );
      const constraint = extraction(run, INPUT, "schema-constraint");
      equal(
        constraint.value,
        { type: "integer", minimum: 1, required: true },
        "direct schema constraints",
      );
      equal(
        constraint.selector,
        "/$defs/production/properties/energy_chunk",
        "resolved exact pointer",
      );
      const absent = extraction(run, INPUT, "schema-default");
      equal(absent.value, null, "schema has no assignment");
      equal(
        facts(run, INPUT)[absent.fact_index].status,
        "not_assigned",
        "schema absent default distinct",
      );
      literal(run, "typed-default", typed);
      literal(run, "example-explicit", example);
      assert(!run.bytes!.includes(f.dir), "private paths absent from public facts");
      equal(
        (await f.run("again")).bytes,
        run.bytes,
        "same bytes deterministic across output directories",
      );
    }, sources(typed, example));
  }
});

// Catches fallback to fixture/default values when an expected source is missing.
for (
  const [path, key, context] of [
    [PATHS[0], API, "documented-signature"],
    [PATHS[7], INPUT, "schema-constraint"],
  ] as const
) {
  Deno.test(`DOC06 missing source: ${path}`, async () => {
    await fixture(async (f) => {
      await Deno.remove(`${f.snapshot}/${path}`);
      const run = await f.run();
      assert(run.status !== "refused", "missing selected source produces bounded partial coverage");
      unsupported(run, key, context, "source_missing");
      const missing = run.receipt!.inputs.find((x) => x.path === path)!;
      equal(missing.actual_sha256, null, "missing hash is null");
      equal(missing.actual_bytes, null, "missing size is null, not zero");
      literal(run, "typed-default", 64);
      literal(run, "example-explicit", 64);
      if (path === PATHS[0]) {
        equal(extraction(run, INPUT, "schema-constraint").value, {
          type: "integer",
          minimum: 1,
          required: true,
        }, "unaffected canonical schema remains independently known");
      }
    });
  });
}

// Catches accepting changed bytes under stale source identities.
Deno.test("DOC06 refuses receipt hash mismatch", () =>
  fixture(async (f) => {
    await write(`${f.snapshot}/${PATHS[8]}`, f.text[PATHS[8]].replace("= 64", "= 83"));
    equal((await f.run()).status, "refused", "mismatch must refuse");
  }));

// Catches permissive namespace/owner parsing and private path projection.
for (const bad of ["../private/secret.jl", "/private/secret.jl", "runner/not-allowlisted.jl"]) {
  Deno.test(`DOC06 refuses nonallowlisted input ${bad}`, () =>
    fixture(async (f) => {
      f.entries[0].path = bad;
      await f.receipt();
      equal((await f.run()).status, "refused", "input namespace refusal");
    }));
}
Deno.test("DOC06 refuses wrong owning component", () =>
  fixture(async (f) => {
    f.entries[0].owner = OWNER.core;
    await f.receipt();
    equal((await f.run()).status, "refused", "wrong owner refusal");
  }));
Deno.test("DOC06 refuses symlink selected file even with matching bytes", () =>
  preparedSymlinkFixture("file", async (f) => {
    const run = await f.run();
    equal(run.status, "refused", "no symlink input");
    equal(run.reason, "symlink_or_invalid_source", "intended source link guard reached");
  }));
Deno.test("DOC06 refuses symlink input ancestor", () =>
  preparedSymlinkFixture("directory", async (f) => {
    const run = await f.run();
    equal(run.status, "refused", "no symlink ancestor");
    equal(run.reason, "symlink_or_invalid_source", "intended source ancestor guard reached");
  }));
Deno.test("DOC06 refuses existing output and source overlap", () =>
  fixture(async (f) => {
    const occupied = `${f.dir}/occupied`;
    await write(`${occupied}/keep`, "preserve");
    for (const outDir of [occupied, `${f.snapshot}/new-output`]) {
      equal(
        (await generateStaticSlice({
          snapshotDir: f.snapshot,
          sourceReceiptPath: f.sourceReceipt,
          outDir,
        })).status,
        "refused",
        "output boundary",
      );
    }
    equal(await Deno.readTextFile(`${occupied}/keep`), "preserve", "existing output preserved");
  }));

// Catches last-key-wins parsing, remote fetching and numeric loss of precision.
const BAD_SCHEMA: [string, string][] = [
  ["invalid-json", "{broken"],
  ["duplicate-key", schema().replace('"minimum":1', '"minimum":1,"minimum":2')],
  [
    "duplicate-selected-property",
    schema().replace('"energy_chunk":{', '"energy_chunk":{"type":"number"},"energy_chunk":{'),
  ],
  ["wrong-minimum-type", schema('"type":"integer","minimum":"1"')],
  ["unsafe-integer", schema('"type":"integer","minimum":9007199254740993')],
  ["nonfinite-number", schema('"type":"integer","minimum":1e999')],
  ["missing-ref", schema().replace("#/$defs/production", "#/$defs/missing")],
  [
    "cyclic-ref",
    '{"required":["production"],"properties":{"production":{"$ref":"#/$defs/p"}},"$defs":{"p":{"$ref":"#/$defs/p"}}}',
  ],
  ["remote-ref", schema().replace("#/$defs/production", "https://invalid.example/schema.json")],
  ["prototype-key", schema().replace('"type":"object"', '"__proto__":{},"type":"object"')],
  ["combinator", schema('"type":"integer","minimum":1,"anyOf":[{"maximum":4},{"minimum":9}]')],
];
for (const [label, json] of BAD_SCHEMA) {
  Deno.test(`DOC06 schema unsupported: ${label}`, async () => {
    const text = sources();
    text[PATHS[6]] = text[PATHS[7]] = json;
    const malformed = [
      "invalid-json",
      "duplicate-key",
      "duplicate-selected-property",
      "wrong-minimum-type",
      "unsafe-integer",
      "nonfinite-number",
      "prototype-key",
    ].includes(label);
    await fixture(
      async (f) => unsupported(await f.run(), INPUT, "schema-constraint", undefined, malformed),
      text,
    );
  });
}
Deno.test("DOC06 local pointer escaping is decoded with own-key traversal", async () => {
  const text = sources();
  text[PATHS[6]] = text[PATHS[7]] = schema().replace('"production":{"type"', '"p/~q":{"type"')
    .replace("#/$defs/production", "#/$defs/p~1~0q");
  await fixture(async (f) => {
    const run = await f.run();
    equal(extraction(run, INPUT, "schema-constraint").value, {
      type: "integer",
      minimum: 1,
      required: true,
    }, "escaped local ref resolved");
  }, text);
});
Deno.test("DOC06 packaged schema mismatch is explicit without replacing canonical authority", async () => {
  const text = sources();
  text[PATHS[6]] = schema('"type":"integer","minimum":8');
  await fixture(async (f) => {
    const run = await f.run();
    equal(extraction(run, INPUT, "schema-constraint").value, {
      type: "integer",
      minimum: 1,
      required: true,
    }, "Contracts source remains authority");
    assert(
      run.receipt!.diagnostics?.some((d) => d.reason === "packaged_schema_mismatch"),
      "mismatch diagnostic",
    );
  }, text);
});
Deno.test("DOC06 schema default declaration is reported without applying it", async () => {
  const text = sources(79, 31);
  text[PATHS[6]] = text[PATHS[7]] = schema('"type":"integer","minimum":1,"default":11');
  await fixture(async (f) => {
    const run = await f.run();
    literal(run, "schema-default", 11);
    literal(run, "typed-default", 79);
    literal(run, "example-explicit", 31);
    assert(
      facts(run, INPUT).some((x) => x.name === "effective_origin" && x.status === "unknown"),
      "declared default is not runtime provenance",
    );
  }, text);
});

// Catches constant folding/evaluation and matching target strings/comments as declarations.
for (
  const rhs of ['ENV["QCL_CHUNK"]', "compute_chunk()", "32 + 32", "@value 64", "9007199254740993"]
) {
  Deno.test(`DOC06 dynamic typed RHS remains unsupported: ${rhs}`, async () => {
    const text = sources();
    text[PATHS[8]] = text[PATHS[8]].replace("energy_chunk::Int = 64", `energy_chunk::Int = ${rhs}`);
    await fixture(async (f) => {
      const run = await f.run();
      unsupported(run, INPUT, "typed-default");
      if (run.status !== "refused") literal(run, "example-explicit", 64);
    }, text);
  });
}
for (
  const [label, replacement] of [
    ["comment", "# energy_chunk::Int = 64"],
    ["string", 'note::String = "energy_chunk::Int = 64"'],
    ["duplicate", "energy_chunk::Int = 64\n    energy_chunk::Int = 79"],
  ] as const
) {
  Deno.test(`DOC06 rejects false typed field match: ${label}`, async () => {
    const text = sources();
    text[PATHS[8]] = text[PATHS[8]].replace("energy_chunk::Int = 64", replacement);
    await fixture(async (f) => unsupported(await f.run(), INPUT, "typed-default"), text);
  });
}
for (const prefix of ["@generate ", "@eval "]) {
  Deno.test(`DOC06 macro method is not typed inventory: ${prefix}`, async () => {
    const text = sources();
    text[PATHS[0]] = text[PATHS[0]].replace(
      "function configuration_source(",
      `${prefix}function configuration_source(`,
    );
    await fixture(async (f) => unsupported(await f.run(), API, "typed-signature"), text);
  });
}
Deno.test("DOC06 signature inside string is not a declaration", async () => {
  const text = sources();
  text[PATHS[0]] =
    's = "function configuration_source(configuration::ResolvedRunConfiguration, dotted_path::AbstractString)"\n';
  await fixture(async (f) => unsupported(await f.run(), API, "typed-signature"), text);
});
for (const scalar of ["*chunk", "!!int 64", "&chunk 64", "64 + 1"]) {
  Deno.test(`DOC06 YAML target is opaque unsupported: ${scalar}`, async () => {
    const text = sources();
    text[PATHS[5]] = `production:\n  energy_chunk: ${scalar}\n`;
    await fixture(async (f) => unsupported(await f.run(), INPUT, "example-explicit"), text);
  });
}
Deno.test("DOC06 YAML duplicate selected leaf is ambiguous", async () => {
  const text = sources();
  text[PATHS[5]] = "production:\n  energy_chunk: 64\n  energy_chunk: 79\n";
  await fixture(async (f) => unsupported(await f.run(), INPUT, "example-explicit"), text);
});

// Catches allocation-after-read. Each fixture is freed serially.
for (
  const [label, mutate] of [
    ["file-bytes", (t: Record<string, string>) => {
      t[PATHS[1]] = "x".repeat(131073);
    }],
    ["docstring", (t: Record<string, string>) => {
      t[PATHS[0]] = t[PATHS[0]].replace("Return the last", "x".repeat(4097) + "Return the last");
    }],
  ] as [string, (t: Record<string, string>) => void][]
) {
  Deno.test(`DOC06 refuses cap overrun: ${label}`, async () => {
    const text = sources();
    mutate(text);
    await fixture(
      async (f) => equal((await f.run()).status, "refused", "explicit overrun refusal"),
      text,
    );
  });
}

// Catches missing lexical guards without allowing malformed selected shape or
// Fact text limits to explain refusal. Only an unused $defs annotation changes;
// the complete healthy production ref/type/minimum/required/default path remains.
function schemaWithUnusedExample(fragment: string): string {
  return schema().replace('"$defs":{', `"$defs":{"unused":{"examples":[${fragment}]},`);
}
for (
  const [label, under, over] of [
    ["json-depth", "[".repeat(20) + "0" + "]".repeat(20), "[".repeat(34) + "0" + "]".repeat(34)],
    ["json-string", `"${"x".repeat(16000)}"`, `"${"x".repeat(16385)}"`],
    ["json-tokens", `[${"0,".repeat(100)}0]`, `[${"0,".repeat(32769)}0]`],
  ] as const
) {
  Deno.test(`DOC06 lexical cap with healthy selected schema: ${label}`, async () => {
    const healthy = sources(79, 31);
    healthy[PATHS[6]] = healthy[PATHS[7]] = schemaWithUnusedExample(under);
    await fixture(async (f) => {
      const run = await f.run();
      assert(run.status !== "refused", "under-cap unused annotation preserves healthy projection");
      const selected = extraction(run, INPUT, "schema-constraint");
      equal(
        selected.value,
        { type: "integer", minimum: 1, required: true },
        "independent healthy selected constraint",
      );
      equal(
        facts(run, INPUT)[selected.fact_index].status,
        "known",
        "selected declaration remains known",
      );
      equal(
        selected.selector,
        "/$defs/production/properties/energy_chunk",
        "selected pointer unchanged",
      );
      const absent = extraction(run, INPUT, "schema-default");
      equal(absent.value, null, "unused branch does not assign schema default");
      equal(
        facts(run, INPUT)[absent.fact_index].status,
        "not_assigned",
        "schema default stays absent",
      );
      literal(run, "typed-default", 79);
      literal(run, "example-explicit", 31);
    }, healthy);
    const overflow = sources(79, 31);
    overflow[PATHS[6]] = overflow[PATHS[7]] = schemaWithUnusedExample(over);
    await fixture(
      async (f) =>
        equal((await f.run()).status, "refused", "lexical cap must refuse healthy-shaped schema"),
      overflow,
    );
  });
}
Deno.test("DOC06 refuses receipt-byte and source-count caps", () =>
  fixture(async (f) => {
    await write(f.sourceReceipt, " ".repeat(16385));
    equal((await f.run()).status, "refused", "receipt cap before parser");
    f.entries.push(...Array.from({ length: 4 }, () => ({ ...f.entries[0] })));
    await f.receipt();
    equal((await f.run("count")).status, "refused", "input count cap");
  }));
Deno.test("DOC06 refuses source aggregate cap without truncated success", async () => {
  const text = sources();
  for (const path of [PATHS[1], PATHS[2], PATHS[3], PATHS[4], PATHS[8]]) {
    text[path] = "#" + "x".repeat(110000) + "\n" + text[path];
  }
  await fixture(async (f) => equal((await f.run()).status, "refused", "aggregate cap"), text);
});

// Catches eval/module execution. Marker is first created/read/deleted in the very
// same writable subtree; absence cannot be explained by a denied write capability.
Deno.test("DOC06 Julia and valid JavaScript sentinels remain inert bytes", () =>
  fixture(async (f) => {
    const marker = `${f.dir}/sentinel-marker`;
    await write(marker, "capability-proven");
    equal(await Deno.readTextFile(marker), "capability-proven", "marker is writable/readable");
    await Deno.remove(marker);
    // Julia sentinel is data, never loaded by Julia or another process.
    const julia = `open(${JSON.stringify(marker)}, "w") do io; write(io, "executed"); end\n`;
    const js = `Deno.writeTextFileSync(${JSON.stringify(marker)}, "executed");\n`;
    for (const [label, prefix] of [["julia", julia], ["js", js]]) {
      // Rebind hashes to sentinel bytes so refusal cannot be a stale-hash trick.
      const text = sources();
      text[PATHS[1]] = prefix;
      const bytes = encoder.encode(prefix);
      await write(`${f.snapshot}/${PATHS[1]}`, bytes);
      const entry = f.entries.find((e) => e.path === PATHS[1])!;
      entry.sha256 = await hash(bytes);
      entry.bytes = bytes.length;
      await f.receipt();
      const run = await f.run(label);
      assert(
        run.status !== "refused",
        "opaque supporting source accepts bounded inert sentinel bytes",
      );
      literal(run, "typed-default", 64);
      assert(!await exists(marker), `${label} target bytes never executed`);
    }
  }));

// Catches permissive UTF-8 decoding and source receipt identity ambiguity.
Deno.test("DOC06 invalid UTF-8 is refused even with matching receipt hash", () =>
  fixture(async (f) => {
    const bytes = new Uint8Array([0x23, 0x20, 0xc3, 0x28]);
    await write(`${f.snapshot}/${PATHS[1]}`, bytes);
    const entry = f.entries.find((e) => e.path === PATHS[1])!;
    entry.sha256 = await hash(bytes);
    entry.bytes = bytes.length;
    await f.receipt();
    equal((await f.run()).status, "refused", "strict UTF-8 decoding");
  }));
Deno.test("DOC06 duplicate receipt path is refused", () =>
  fixture(async (f) => {
    f.entries[1] = { ...f.entries[0] };
    await f.receipt();
    equal((await f.run()).status, "refused", "receipt cannot collapse duplicate paths");
  }));
Deno.test("DOC06 wrong source byte length is refused", () =>
  fixture(async (f) => {
    f.entries[0].bytes += 1;
    await f.receipt();
    equal((await f.run()).status, "refused", "identity includes raw byte length");
  }));
Deno.test("DOC06 duplicate required member is not a direct complete constraint", async () => {
  const text = sources();
  text[PATHS[6]] = text[PATHS[7]] = schema().replace(
    '["energy_chunk"]',
    '["energy_chunk","energy_chunk"]',
  );
  await fixture(
    async (f) => unsupported(await f.run(), INPUT, "schema-constraint", undefined, true),
    text,
  );
});
Deno.test("DOC06 local reference hop cap refuses a long acyclic chain", async () => {
  const text = sources();
  const refs = Array.from({ length: 10 }, (_, i) => `"p${i}":{"$ref":"#/$defs/p${i + 1}"}`).join(
    ",",
  );
  text[PATHS[6]] =
    text[PATHS[7]] =
      `{"properties":{"production":{"$ref":"#/$defs/p0"}},"$defs":{${refs},"p10":{"type":"object","required":["energy_chunk"],"properties":{"energy_chunk":{"type":"integer","minimum":1}}}}}`;
  await fixture(async (f) => equal((await f.run()).status, "refused", "reference hop cap"), text);
});

// Independent CPP regressions: neither Cmd text nor constructor locals are fields.
// Healthy pairs prevent an implementation from making every Core source unknown.
for (
  const [label, core] of [
    [
      "Cmd literal",
      "Base.@kwdef struct ProductionOptions\n    note::Any = `\n    energy_chunk::Int = 64\n    `\nend\n",
    ],
    [
      "inner constructor local",
      "struct ProductionOptions\n    function ProductionOptions()\n        energy_chunk::Int = 64\n        new()\n    end\nend\n",
    ],
  ] as const
) {
  Deno.test(`DOC06 false field context stays unknown: ${label}`, async () => {
    await fixture(async (f) => {
      const run = await f.run();
      literal(run, "typed-default", 64);
      literal(run, "example-explicit", 31);
    }, sources(64, 31));
    const text = sources(64, 31);
    text[PATHS[8]] = core;
    await fixture(async (f) => {
      const run = await f.run();
      unsupported(run, INPUT, "typed-default");
      literal(run, "example-explicit", 31);
      equal(extraction(run, INPUT, "schema-constraint").value, {
        type: "integer",
        minimum: 1,
        required: true,
      }, "independent schema survives unsupported Core context");
    }, text);
  });
}

// M1/M2/M3 regressions authored before the source correction. A1/A2 are the
// existing RED evidence; this source-only stage does not execute a new RED.
function rootConditional(
  json = schema(),
  branch = '"algorithms":{"anyOf":[false,{"$ref":"https://invalid.example/inert"}]}',
) {
  return json.replace(
    '{"type":"object"',
    `{"allOf":[{"if":{"properties":{"run":{"not":false}}},"then":{"properties":{${branch}}}}],"type":"object"`,
  );
}
function assertSchemaUnknown(
  run: Run,
  selector: string,
  reason = "unsupported_selected_schema_context",
) {
  for (const context of ["schema-type", "schema-constraint", "schema-default", "units"]) {
    unsupported(run, INPUT, context, reason);
    equal(extraction(run, INPUT, context).selector, selector, `${context} cites offending pointer`);
  }
  literal(run, "root-production-required", true);
  equal(
    extraction(run, INPUT, "root-production-required").selector,
    "/required",
    "independent root membership locator",
  );
  literal(run, "typed-default", 79);
  literal(run, "example-explicit", 31);
  equal(
    extraction(run, API, "documented-signature").mode,
    "literal-extraction",
    "independent API survives",
  );
  for (const context of ["units", "effects", "formula-origin"]) {
    const entry = extraction(run, INPUT, context);
    const fact = facts(run, INPUT)[entry.fact_index];
    equal(entry.mode, "dynamic-unknown", `${context} has no authored evidence`);
    equal(fact.status, "unknown", `${context} unknown`);
    assert(fact.text.includes(reason), `${context} preserves failure reason`);
    assert(!fact.text.includes("description отсутствует"), "failure is not absence");
    assert(!fact.text.includes("приведено отдельно"), "no missing quotation promise");
    assert(!fact.text.includes("параметр планирования"), "no unsupported scheduling claim");
  }
}
Deno.test("DOC06 unrelated root condition preserves direct declarations with partial validation", async () => {
  const text = sources(79, 31);
  text[PATHS[6]] = text[PATHS[7]] = rootConditional();
  await fixture(async (f) => {
    const run = await f.run();
    literal(run, "schema-type", "integer");
    literal(run, "schema-constraint", { type: "integer", minimum: 1, required: true });
    literal(run, "root-production-required", true);
    const absent = extraction(run, INPUT, "schema-default");
    equal(absent.mode, "literal-extraction", "own default absence is literal");
    equal(absent.value, null, "no own default keyword");
    equal(
      facts(run, INPUT)[absent.fact_index].status,
      "not_assigned",
      "recognized direct default absence",
    );
    assert(
      facts(run, INPUT)[absent.fact_index].text.includes("own default"),
      "absence claim limited to own keyword",
    );
    const constraint = extraction(run, INPUT, "schema-constraint");
    const selectors = (facts(run, INPUT)[constraint.fact_index].sources as { selector: string }[])
      .map((s) => s.selector);
    equal(
      selectors,
      ["/$defs/production/properties/energy_chunk", "/$defs/production/required"],
      "combined direct declaration cites leaf and required",
    );
    const coverage = extraction(run, INPUT, "schema-validation-coverage");
    equal(coverage.mode, "authored-context", "coverage explicitly authored");
    equal(coverage.selector, "/allOf", "root conditional scope locator");
    equal(
      coverage.value,
      [{ if: ["run"], then: ["algorithms"] }],
      "literal property footprint without predicate evaluation",
    );
    equal(
      facts(run, INPUT)[coverage.fact_index].status,
      "partial",
      "full validation remains partial",
    );
    const description = extraction(run, INPUT, "units");
    equal(description.mode, "literal-extraction", "description literal");
    equal(
      description.selector,
      "/$defs/production/properties/energy_chunk/description",
      "exact owning description",
    );
    for (const context of ["effects", "formula-origin"]) {
      const entry = extraction(run, INPUT, context);
      equal(entry.mode, "authored-context", `${context} authored interpretation`);
      equal(entry.selector, description.selector, `${context} grounded in extracted description`);
      equal(
        facts(run, INPUT)[entry.fact_index].status,
        context === "effects" ? "partial" : "not_applicable",
        `${context} bounded status`,
      );
    }
    literal(run, "typed-default", 79);
    literal(run, "example-explicit", 31);
    for (const key of [API, INPUT]) {
      equal(
        [...new Set(facts(run, key).map((fact) => fact.name))].sort(),
        [...CLASSES].sort(),
        "all ten classes retained",
      );
    }
    equal(
      run.facts!.binding,
      { status: "source-prototype", application_release: null, run: null },
      "no runtime identity",
    );
    equal(run.facts!.coverage.status, "partial", "partial global coverage");
    equal((await f.run("again")).bytes, run.bytes, "facts deterministic across fresh dirs");
    equal(
      await Deno.readTextFile(`${f.dir}/again/source-receipt.json`),
      await Deno.readTextFile(`${f.dir}/out/source-receipt.json`),
      "receipt deterministic across fresh dirs",
    );
  }, text);
});
for (const clause of ["if", "then"] as const) {
  Deno.test(`DOC06 root conditional selected production fails closed in ${clause}`, async () => {
    const text = sources(79, 31);
    const positive = rootConditional();
    text[PATHS[6]] = text[PATHS[7]] = clause === "if"
      ? positive.replace('"run":{"not":false}', '"production":{"not":false}')
      : positive.replace('"algorithms":{"anyOf"', '"production":{"anyOf"');
    await fixture(
      async (f) => assertSchemaUnknown(await f.run(), `/allOf/0/${clause}/properties/production`),
      text,
    );
  });
}
for (
  const [label, replacement, selector] of [
    ["else", '"else":{},"if":', "/allOf/0/else"],
    ["item escaped extra", '"x/y~z":{},"if":', "/allOf/0/x~1y~0z"],
  ] as const
) {
  Deno.test(`DOC06 root conditional rejects unknown item key: ${label}`, async () => {
    const text = sources(79, 31);
    text[PATHS[6]] = text[PATHS[7]] = rootConditional().replace('"if":', replacement);
    await fixture(async (f) => assertSchemaUnknown(await f.run(), selector), text);
  });
}
for (const keyword of ["required", "additionalProperties", "not", "$ref", "x/y~z"] as const) {
  Deno.test(`DOC06 root conditional rejects root-wide clause key: ${keyword}`, async () => {
    const text = sources(79, 31);
    text[PATHS[6]] = text[PATHS[7]] = rootConditional().replace(
      '"then":{"properties":',
      `"then":{${JSON.stringify(keyword)}:false,"properties":`,
    );
    const segment = keyword.replace(/~/g, "~0").replace(/\//g, "~1");
    await fixture(
      async (f) => assertSchemaUnknown(await f.run(), `/allOf/0/then/${segment}`),
      text,
    );
  });
}
Deno.test("DOC06 root anyOf keeps direct required independent", async () => {
  const text = sources(79, 31);
  text[PATHS[6]] = text[PATHS[7]] = schema().replace('{"type":', '{"anyOf":[{}],"type":');
  await fixture(async (f) => assertSchemaUnknown(await f.run(), "/anyOf"), text);
});
for (
  const [label, json, pointer] of [
    [
      "production allOf",
      schema().replace('"production":{"type":', '"production":{"allOf":[{}],"type":'),
      "/$defs/production/allOf",
    ],
    [
      "leaf anyOf",
      schema('"type":"integer","minimum":1,"description":"Present despite failure","anyOf":[{}]'),
      "/$defs/production/properties/energy_chunk/anyOf",
    ],
  ] as const
) {
  Deno.test(`DOC06 unsupported selected context preserves failure locators: ${label}`, async () => {
    const text = sources(79, 31);
    text[PATHS[6]] = text[PATHS[7]] = json;
    await fixture(
      async (f) => assertSchemaUnknown(await f.run(), pointer, "unsupported_schema_keyword"),
      text,
    );
  });
}
Deno.test("DOC06 escaped resolved production required uses its source pointer", async () => {
  const text = sources(79, 31);
  text[PATHS[6]] = text[PATHS[7]] = rootConditional(
    schema().replace('"production":{"type"', '"p/~q":{"type"').replace(
      "#/$defs/production",
      "#/$defs/p~1~0q",
    ),
  );
  await fixture(async (f) => {
    const run = await f.run();
    const constraint = extraction(run, INPUT, "schema-constraint");
    literal(run, "schema-constraint", { type: "integer", minimum: 1, required: true });
    equal(
      (facts(run, INPUT)[constraint.fact_index].sources as { selector: string }[]).map((s) =>
        s.selector
      ),
      ["/$defs/p~1~0q/properties/energy_chunk", "/$defs/p~1~0q/required"],
      "escaped source locations retained",
    );
  }, text);
});
Deno.test("DOC06 direct root membership false remains literal under unsupported context", async () => {
  const text = sources(79, 31);
  text[PATHS[6]] = text[PATHS[7]] = rootConditional().replace('["production"]', "[]").replace(
    '"algorithms":{"anyOf"',
    '"production":{"anyOf"',
  );
  await fixture(async (f) => {
    const run = await f.run();
    literal(run, "root-production-required", false);
    equal(
      extraction(run, INPUT, "root-production-required").selector,
      "/required",
      "false direct membership exact locator",
    );
    unsupported(run, INPUT, "schema-constraint", "unsupported_selected_schema_context");
  }, text);
});
for (const absent of ["description_absent", "source_missing"] as const) {
  Deno.test(`DOC06 description failure keeps absence and unavailable distinct: ${absent}`, async () => {
    const text = sources(79, 31);
    if (absent === "description_absent") {
      text[PATHS[6]] = text[PATHS[7]] = schema('"type":"integer","minimum":1');
    }
    await fixture(async (f) => {
      if (absent === "source_missing") await Deno.remove(`${f.snapshot}/${PATHS[7]}`);
      const run = await f.run();
      const units = extraction(run, INPUT, "units");
      equal(units.reason, absent, "reason is not rewritten as absence");
      const unitText = facts(run, INPUT)[units.fact_index].text;
      assert(
        unitText.includes(
          absent === "description_absent"
            ? "direct leaf description не объявлено"
            : "не извлечено (source_missing)",
        ),
        "reason-aware units text",
      );
      for (const context of ["effects", "formula-origin"]) {
        const entry = extraction(run, INPUT, context);
        equal(entry.mode, "dynamic-unknown", "no fabricated authored interpretation");
        equal(facts(run, INPUT)[entry.fact_index].status, "unknown", "failure status unknown");
        assert(facts(run, INPUT)[entry.fact_index].text.includes(absent), "reason retained");
        assert(
          !facts(run, INPUT)[entry.fact_index].text.includes("приведено отдельно"),
          "no quotation promise",
        );
      }
      literal(run, "typed-default", 79);
      literal(run, "example-explicit", 31);
    }, text);
  });
}
Deno.test("DOC06 no root composition still states partial validation coverage", () =>
  fixture(async (f) => {
    const run = await f.run();
    const coverage = extraction(run, INPUT, "schema-validation-coverage");
    equal(coverage.selector, "", "root JSON pointer without allOf");
    equal(coverage.value, [], "no conditional footprint");
    equal(coverage.mode, "authored-context", "explicit interpretation mode");
    equal(
      facts(run, INPUT)[coverage.fact_index].status,
      "partial",
      "direct facts never claim instance validation",
    );
  }));
