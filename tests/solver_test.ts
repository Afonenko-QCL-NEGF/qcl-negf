import { type BuildOptions, buildSolver, parseBuildOptions } from "../ops/solver.ts";
import { type SourceGraph } from "../ops/git.ts";
import { type Command } from "../ops/process.ts";

const graph: SourceGraph = {
  format: "qcl-negf.git-graph.v1",
  revision: "a".repeat(40),
  components: [
    {
      path: "components/QCLNEGF.jl",
      revision: "b".repeat(40),
      url: "https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl",
    },
    {
      path: "components/QCLNEGFRunner.jl",
      revision: "c".repeat(40),
      url: "https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl",
    },
  ],
};
const manifestSha = "d".repeat(64);
const hash = "sha256-" + btoa(String.fromCharCode(...Array(32).fill(1)));
const otherHash = "sha256-" + btoa(String.fromCharCode(...Array(32).fill(2)));
const encoder = new TextEncoder();

interface Binding {
  captured_input_sha256: string;
  captured_input_bytes: number;
  consumed_metadata_sha256: string;
  consumed_metadata_bytes: number;
  normalization: string;
  source_revision: string;
  julia_manifest_sha256: string;
  archive_url: string;
  archive_hash: string;
}
// Deliberately bridge the pre-RED signature: run the accepted D2 contract against
// the old implementation without turning the intended behavioral RED into TS errors.
const build = buildSolver as unknown as (
  metadataJson: string,
  expectedGraph: SourceGraph,
  expectedManifest: string,
  execute: (command: Command) => Promise<string>,
  options?: BuildOptions,
) => Promise<Binding>;

function depot(url = "https://artifacts.example.invalid/depot.tar.gz", archiveHash = hash) {
  return {
    format: "qcl-negf.julia-depot.v1",
    sources: structuredClone(graph),
    julia: "1.13.0",
    juliaManifest: manifestSha,
    url,
    hash: archiveHash,
  };
}
function assert(value: boolean, message: string): void {
  if (!value) throw new Error(message);
}
async function sha(value: string): Promise<string> {
  const bytes = new Uint8Array(await crypto.subtle.digest("SHA-256", encoder.encode(value)));
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
}
function argument(command: Command, name: string): string {
  const index = command.args.indexOf(name);
  assert(index > 0 && command.args[index - 1] === "--argstr", `Missing data argument ${name}`);
  return command.args[index + 1];
}
async function bound(
  command: Command,
  receipt: Binding,
  raw: string,
  url: string,
  archiveHash: string,
) {
  const json = argument(command, "depotManifestJson");
  const digest = await sha(json); // Hash the actual outgoing argument, independently of production.
  assert(argument(command, "depotManifestSha256") === digest, "Outgoing JSON/SHA mismatch");
  assert(!command.args.includes("depotManifest"), "Late pathname input must be absent");
  const consumed = JSON.parse(json);
  assert(
    consumed.url === url && consumed.hash === archiveHash,
    "Build consumed a different archive",
  );
  assert(consumed.sources.revision === graph.revision, "Wrong root consumed");
  assert(consumed.sources.components.length === 2, "Lost graph entries");
  for (const component of graph.components) {
    const actual = consumed.sources.components.find((item: { path: string }) =>
      item.path === component.path
    );
    assert(
      actual?.revision === component.revision && actual?.url === component.url,
      "Wrong component consumed",
    );
  }
  assert(receipt.captured_input_sha256 === await sha(raw), "Raw digest is not captured input");
  assert(
    receipt.captured_input_bytes === encoder.encode(raw).length,
    "Raw count must use UTF8 bytes",
  );
  assert(receipt.consumed_metadata_sha256 === digest, "Observation must bind actual argv");
  assert(
    receipt.consumed_metadata_bytes === encoder.encode(json).length,
    "Consumed count must use UTF8 bytes",
  );
  assert(receipt.normalization === "JSON.parse→JSON.stringify", "Normalization must be explicit");
  assert(
    receipt.source_revision === graph.revision && receipt.julia_manifest_sha256 === manifestSha,
    "Source/lock observation mismatch",
  );
  assert(
    receipt.archive_url === url && receipt.archive_hash === archiveHash,
    "Archive observation mismatch",
  );
  return consumed;
}
async function refuses(raw: unknown, label: string) {
  const commands: Command[] = [];
  let rejected = false;
  try {
    await build(raw as string, graph, manifestSha, (command) => {
      commands.push(command);
      return Promise.resolve("");
    });
  } catch {
    rejected = true;
  }
  assert(rejected && commands.length === 0, `${label}: reject before any external callback`);
}

Deno.test("build resource options reject ambiguous or executable input before commands", () => {
  assert(parseBuildOptions([]).profile === "production-build", "Default production profile");
  assert(
    parseBuildOptions(["--profile", "local-debug"]).testWorkerLimit === null,
    "Owning debug policy",
  );
  for (
    const flags of [
      ["--profile", "unknown"],
      ["--test-workers", "0"],
      ["--test-workers", "-1"],
      ["--test-workers", "1.5"],
      ["--test-workers", 'builtins.abort "bad"'],
      ["--test-workers", "9007199254740992"],
      ["--profile"],
      ["--test-workers", "16", "--test-workers", "32"],
      ["--profile", "local-debug", "--test-workers", "16"],
    ]
  ) {
    let rejected = false;
    try {
      parseBuildOptions(flags);
    } catch {
      rejected = true;
    }
    assert(rejected, "Invalid worker options accepted");
  }
});

Deno.test("OPS04 HTTPS metadata binds exact consumed JSON bytes and production worker arguments", async () => {
  const spec = depot();
  const raw = JSON.stringify({ extra: "μ preserved", ...spec }, null, 2) + "\n";
  const commands: Command[] = [];
  const receipt = await build(raw, graph, manifestSha, (command) => {
    commands.push(command);
    return Promise.resolve("");
  }, parseBuildOptions(["--test-workers", "16"]));
  assert(
    commands.length === 1 && commands[0].executable === "nix" && commands[0].args[0] === "build",
    "HTTPS uses exactly one build",
  );
  const consumed = await bound(commands[0], receipt, raw, spec.url, hash);
  assert(consumed.extra === "μ preserved", "Unknown metadata must survive normalization");
  assert(
    receipt.captured_input_sha256 !== receipt.consumed_metadata_sha256,
    "Pretty raw bytes differ from produced bytes",
  );
  assert(argument(commands[0], "juliaTestProfile") === "production-build", "Profile lost");
  const limit = commands[0].args.indexOf("juliaTestWorkerLimit");
  assert(
    limit > 0 && commands[0].args[limit - 1] === "--arg" && commands[0].args[limit + 1] === "16",
    "Integer worker limit lost",
  );
  const source = argument(commands[0], "source");
  assert(
    source.startsWith("git+file:") && source.includes(`rev=${graph.revision}`) &&
      source.includes("submodules=1"),
    "Pinned source arguments lost",
  );
});

Deno.test("OPS04 path replacement after capture keeps A while replacement before capture consistently selects B", async () => {
  const directory = await Deno.makeTempDir({ prefix: "ops04-binding-" });
  const path = `${directory}/solver-depot.json`;
  const specA = depot("file:///artifact%20directory/depot-A.tar.gz");
  const specB = depot("file:///artifact/depot-B.tar.gz", otherHash);
  try {
    await Deno.writeTextFile(path, JSON.stringify(specA, null, 2));
    // This is the CLI capture boundary: production helper receives only a string.
    const captured = await Deno.readTextFile(path);
    const commands: Command[] = [];
    const receipt = await build(captured, graph, manifestSha, async (command) => {
      commands.push(command);
      if (command.args[0] === "store") await Deno.writeTextFile(path, JSON.stringify(specB));
      return "";
    });
    assert(commands.length === 2 && commands[1].args[0] === "build", "Prefetch must precede build");
    assert(
      JSON.stringify(commands[0].args) ===
        JSON.stringify([
          "store",
          "prefetch-file",
          "--hash-type",
          "sha256",
          "--expected-hash",
          hash,
          "--name",
          "qcl-negf-julia-depot.tar.gz",
          specA.url,
        ]),
      "Prefetch lost captured A URL/hash/name",
    );
    await bound(commands[1], receipt, captured, specA.url, hash);
    // Replacement before capture selects B, consistently in both consumers.
    const capturedB = await Deno.readTextFile(path);
    const commandsB: Command[] = [];
    const receiptB = await build(capturedB, graph, manifestSha, (command) => {
      commandsB.push(command);
      return Promise.resolve("");
    });
    assert(
      commandsB.length === 2 && commandsB[0].args.includes(specB.url) &&
        commandsB[0].args.includes(otherHash),
      "Captured B prefetch mismatch",
    );
    await bound(commandsB[1], receiptB, capturedB, specB.url, otherHash);
  } finally {
    await Deno.remove(directory, { recursive: true });
  }
});

Deno.test("OPS04 first callback cannot mutate captured operative metadata or resource arguments", async () => {
  const spec = depot("file:///artifact/depot.tar.gz");
  const raw = JSON.stringify(spec);
  const options: BuildOptions = { profile: "production-build", testWorkerLimit: 16 };
  const commands: Command[] = [];
  const receipt = await build(raw, graph, manifestSha, (command) => {
    commands.push(command);
    spec.url = "file:///unrelated/depot.tar.gz";
    spec.hash = otherHash;
    options.profile = "local-debug";
    options.testWorkerLimit = 2;
    return Promise.resolve("");
  }, options);
  assert(commands.length === 2, "Expected verified local build");
  await bound(commands[1], receipt, raw, "file:///artifact/depot.tar.gz", hash);
  assert(
    argument(commands[1], "juliaTestProfile") === "production-build",
    "Callback mutated frozen profile",
  );
  const worker = commands[1].args.indexOf("juliaTestWorkerLimit");
  assert(commands[1].args[worker + 1] === "16", "Callback mutated frozen worker budget");
});

Deno.test("OPS04 graph and object order are immaterial while raw duplicate members normalize once", async () => {
  const spec = depot();
  spec.sources.components.reverse();
  const raw = '{"hash":"discarded","url":"https://discarded.invalid",' +
    JSON.stringify(spec).slice(1);
  const commands: Command[] = [];
  const receipt = await build(raw, graph, manifestSha, (command) => {
    commands.push(command);
    return Promise.resolve("");
  });
  assert(commands.length === 1, "Ordering or duplicate-member parse outcome rejected");
  await bound(commands[0], receipt, raw, spec.url, hash);
  // Repeated members replace values while retaining their first insertion positions.
  // This ordered expectation is independent of the outgoing JSON and production parser.
  const expected = JSON.stringify({
    hash,
    url: "https://artifacts.example.invalid/depot.tar.gz",
    format: "qcl-negf.julia-depot.v1",
    sources: {
      format: "qcl-negf.git-graph.v1",
      revision: "a".repeat(40),
      components: [
        {
          path: "components/QCLNEGFRunner.jl",
          revision: "c".repeat(40),
          url: "https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl",
        },
        {
          path: "components/QCLNEGF.jl",
          revision: "b".repeat(40),
          url: "https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl",
        },
      ],
    },
    julia: "1.13.0",
    juliaManifest: "d".repeat(64),
  });
  assert(
    argument(commands[0], "depotManifestJson") === expected,
    "Produced JSON must have one JS parse outcome with first-insertion key order",
  );
});

Deno.test("OPS04 rejected prefetch and command failures never return success observation", async () => {
  for (
    const url of ["file:///artifact/depot.tar.gz", "https://artifacts.example.invalid/depot.tar.gz"]
  ) {
    const commands: Command[] = [];
    const failure = new Error("fixture external failure");
    let caught: unknown;
    try {
      await build(JSON.stringify(depot(url)), graph, manifestSha, (command) => {
        commands.push(command);
        return Promise.reject(failure);
      });
    } catch (error) {
      caught = error;
    }
    assert(
      caught === failure && commands.length === 1,
      "Failure must propagate without later commands",
    );
    assert(
      commands[0].args[0] === (url.startsWith("file:") ? "store" : "build"),
      "Wrong first command",
    );
  }
});

Deno.test("OPS04 same-root wrong component graph and malformed archive metadata execute nothing", async () => {
  const cases: Array<[string, unknown]> = [
    ["object legacy input", depot()],
    ["null", "null"],
    ["array", "[]"],
    ["number", "3"],
    ["invalid JSON", "{"],
    ["nonstring", 42],
    ["BOM", "\uFEFF" + JSON.stringify(depot())],
    ["raw NUL", JSON.stringify(depot()) + "\0"],
    ["raw oversize", " ".repeat(65537)],
  ];
  const mutations: Array<[string, (spec: ReturnType<typeof depot>) => void]> = [
    ["depot format", (spec) => {
      spec.format = "other";
    }],
    ["Julia", (spec) => {
      spec.julia = "1.12.0";
    }],
    ["Manifest", (spec) => {
      spec.juliaManifest = "e".repeat(64);
    }],
    ["graph format", (spec) => {
      (spec.sources as { format: string }).format = "other";
    }],
    ["root", (spec) => {
      spec.sources.revision = "f".repeat(40);
    }],
    ["component revision", (spec) => {
      spec.sources.components[0].revision = "f".repeat(40);
    }],
    ["component URL", (spec) => {
      spec.sources.components[0].url = "https://github.com/other/repository";
    }],
    ["component path", (spec) => {
      spec.sources.components[0].path = "components/Wrong.jl";
    }],
    ["missing", (spec) => {
      spec.sources.components.pop();
    }],
    ["extra", (spec) => {
      spec.sources.components.push({
        path: "components/Extra",
        revision: "f".repeat(40),
        url: "https://github.com/example/Extra",
      });
    }],
    ["duplicate", (spec) => {
      spec.sources.components.push({ ...spec.sources.components[0] });
    }],
    ["malformed URL", (spec) => {
      spec.url = "not a URL";
    }],
  ];
  for (const [label, mutate] of mutations) {
    const spec = depot();
    mutate(spec);
    cases.push([label, JSON.stringify(spec)]);
  }
  cases.push(["nonstring URL", JSON.stringify({ ...depot(), url: 1 })]);
  cases.push(["nonstring hash", JSON.stringify({ ...depot(), hash: null })]);
  cases.push(["UTF8 oversize", JSON.stringify({ ...depot(), extra: "μ".repeat(33000) })]);
  // 1e20 is valid short JSON, but JS stringify emits a 21-digit decimal.
  const expanded = JSON.stringify(depot()).slice(0, -1) + ',"extra":[' +
    Array(4000).fill("1e20").join(",") + "]}";
  assert(encoder.encode(expanded).length < 65536, "Produced-size fixture raw input must fit");
  cases.push(["produced oversize", expanded]);
  for (const [label, raw] of cases) await refuses(raw, label);
});

Deno.test("OPS04 accepts exactly 65536 captured UTF8 bytes without truncation", async () => {
  const json = JSON.stringify(depot());
  const raw = json + " ".repeat(65536 - encoder.encode(json).length);
  const commands: Command[] = [];
  const receipt = await build(raw, graph, manifestSha, (command) => {
    commands.push(command);
    return Promise.resolve("");
  });
  assert(commands.length === 1, "Exact raw bound rejected");
  await bound(commands[0], receipt, raw, depot().url, hash);
});

Deno.test("OPS04 programmatic invalid options reject before callback", async () => {
  for (
    const options of [
      { profile: "unknown", testWorkerLimit: null },
      { profile: "production-build", testWorkerLimit: 0 },
      { profile: "production-build", testWorkerLimit: 1.5 },
      { profile: "local-debug", testWorkerLimit: 16 },
    ]
  ) {
    let calls = 0;
    let rejected = false;
    try {
      await build(JSON.stringify(depot()), graph, manifestSha, () => {
        calls++;
        return Promise.resolve("");
      }, options as BuildOptions);
    } catch {
      rejected = true;
    }
    assert(rejected && calls === 0, "Invalid direct options reached callback");
  }
});

Deno.test("OPS04 unchecked legacy object plus pathname invocation is rejected before callback", async () => {
  const directory = await Deno.makeTempDir({ prefix: "ops04-legacy-" });
  const path = `${directory}/B.json`;
  try {
    const wrong = depot();
    wrong.sources.components[0].revision = "f".repeat(40);
    await Deno.writeTextFile(path, JSON.stringify(wrong));
    let commands = 0;
    let rejected = false;
    const legacy = buildSolver as unknown as (...args: unknown[]) => Promise<unknown>;
    try {
      await legacy(depot(), graph.revision, path, () => {
        commands++;
        return Promise.resolve("");
      });
    } catch {
      rejected = true;
    }
    assert(rejected && commands === 0, "Legacy A-object/B-path bypass must reject before callback");
    await refuses(await Deno.readTextFile(path), "Actually captured wrong-graph B");
  } finally {
    await Deno.remove(directory, { recursive: true });
  }
});

// Accepted CLI seam addendum: dynamic export lookup lets the absent baseline
// exports produce a behavioral RED without a missing-export typecheck error.
import * as solverModule from "../ops/solver.ts";
interface TestDepotFile {
  stat(): Promise<{ isFile: boolean }>;
  read(buffer: Uint8Array): Promise<number | null>;
  close(): void;
}
type TestOpenDepot = (path: string) => Promise<TestDepotFile>;
interface TestCliDependencies {
  openDepotInput: TestOpenDepot;
  readSourceGraph(): Promise<SourceGraph>;
  readJuliaManifestSha256(): Promise<string>;
  execute(command: Command, capture?: boolean): Promise<string>;
}
const captureMetadata = (solverModule as unknown as {
  captureDepotMetadata(path: string, open?: TestOpenDepot): Promise<string>;
}).captureDepotMetadata;
const solverCli = (solverModule as unknown as {
  runSolverBuildCli(
    args: readonly string[],
    dependencies?: Partial<TestCliDependencies>,
  ): Promise<Binding>;
}).runSolverBuildCli;

function trackedInput(bytes: Uint8Array, settings: {
  chunk?: number;
  isFile?: boolean;
  statError?: Error;
  readError?: Error;
  noProgress?: boolean;
} = {}) {
  const events: string[] = [];
  const requests: number[] = [];
  let opens = 0;
  let closes = 0;
  let offset = 0;
  const open: TestOpenDepot = (_path) => {
    opens++;
    events.push("open");
    return Promise.resolve({
      stat() {
        events.push("stat");
        if (settings.statError) return Promise.reject(settings.statError);
        return Promise.resolve({ isFile: settings.isFile ?? true });
      },
      read(buffer) {
        events.push("read");
        requests.push(buffer.length);
        if (settings.readError) return Promise.reject(settings.readError);
        if (settings.noProgress) return Promise.resolve(0);
        if (offset === bytes.length) return Promise.resolve(null);
        const count = Math.min(
          buffer.length,
          settings.chunk ?? bytes.length,
          bytes.length - offset,
        );
        buffer.set(bytes.subarray(offset, offset + count));
        offset += count;
        return Promise.resolve(count);
      },
      close() {
        events.push("close");
        closes++;
      },
    });
  };
  return {
    open,
    events,
    requests,
    get opens() {
      return opens;
    },
    get closes() {
      return closes;
    },
    get bytesReturned() {
      return offset;
    },
  };
}

Deno.test("OPS04 capture uses one descriptor and bounded progressing short reads through exact UTF8 roundtrip", async () => {
  const text = "μ".repeat(32768); // exactly 65536 UTF8 bytes, including split multibyte reads
  const input = trackedInput(encoder.encode(text), { chunk: 997 });
  const captured = await captureMetadata("fixture.json", input.open);
  assert(captured === text, "Short reads truncated or changed captured bytes");
  assert(input.opens === 1 && input.closes === 1, "Capture must own exactly one descriptor");
  assert(
    input.events[0] === "open" && input.events[1] === "stat" && input.events.at(-1) === "close",
    "Stat must precede data reads; close must finish capture",
  );
  assert(
    input.bytesReturned === 65536 && input.requests[0] === 65537 && input.requests.at(-1) === 1,
    "Exact-bound capture must probe EOF using sentinel space",
  );
  let returned = 0;
  for (let index = 0; index < input.requests.length; index++) {
    assert(
      input.requests[index] === 65537 - returned,
      "Each read must use only remaining bounded storage",
    );
    returned += Math.min(997, 65536 - returned);
  }
});

Deno.test("OPS04 capture sentinel oversize closes without an additional read", async () => {
  const input = trackedInput(new Uint8Array(70000).fill(65), { chunk: 4096 });
  let rejected = false;
  try {
    await captureMetadata("fixture.json", input.open);
  } catch {
    rejected = true;
  }
  assert(
    rejected && input.bytesReturned === 65537,
    "Oversize must consume at most limit plus sentinel",
  );
  assert(
    input.opens === 1 && input.closes === 1 && input.requests.length === 17,
    "No extra read after sentinel and no descriptor leak",
  );
  assert(input.requests.at(-1) === 1, "Final request must be only sentinel byte");
});

Deno.test("OPS04 capture closes after stat/read/no-progress/decoder failures and never reads nonregular input", async () => {
  const statFailure = new Error("fixture stat error");
  const readFailure = new Error("fixture read error");
  const fixtures = [
    {
      input: trackedInput(encoder.encode("valid"), { isFile: false }),
      expected: undefined,
      reads: 0,
    },
    {
      input: trackedInput(encoder.encode("valid"), { statError: statFailure }),
      expected: statFailure,
      reads: 0,
    },
    {
      input: trackedInput(encoder.encode("valid"), { readError: readFailure }),
      expected: readFailure,
      reads: 1,
    },
    {
      input: trackedInput(encoder.encode("valid"), { noProgress: true }),
      expected: undefined,
      reads: 1,
    },
    { input: trackedInput(new Uint8Array([0xc3, 0x28])), expected: undefined, reads: 2 },
    { input: trackedInput(new Uint8Array([0xef, 0xbb, 0xbf, 65])), expected: undefined, reads: 2 },
    { input: trackedInput(new Uint8Array([65, 0, 66])), expected: undefined, reads: 2 },
  ];
  for (const { input, expected, reads } of fixtures) {
    let caught: unknown;
    try {
      await captureMetadata("fixture.json", input.open);
    } catch (error) {
      caught = error;
    }
    assert(caught !== undefined, "Failed capture returned successful string");
    if (expected) assert(caught === expected, "Original I/O failure must propagate");
    assert(
      input.opens === 1 && input.closes === 1 && input.requests.length === reads,
      "Failure leaked descriptor or read a nonregular input",
    );
  }
  const failure = new Error("fixture open error");
  let caught: unknown;
  try {
    await captureMetadata("fixture.json", () => Promise.reject(failure));
  } catch (error) {
    caught = error;
  }
  assert(caught === failure, "Open failure must propagate without a descriptor");
});

Deno.test("OPS04 default capture validates actual regular-file UTF8 bytes and closes directory rejection", async () => {
  const directory = await Deno.makeTempDir({ prefix: "ops04-capture-real-" });
  const path = `${directory}/input.json`;
  try {
    const valid = JSON.stringify({ ...depot(), extra: "μ/😀" }, null, 2);
    await Deno.writeFile(path, encoder.encode(valid));
    assert(await captureMetadata(path) === valid, "Default opener changed actual UTF8 bytes");
    for (
      const bytes of [
        new Uint8Array([0xc3, 0x28]),
        new Uint8Array([0xf0, 0x9f, 0x98]),
        new Uint8Array([0xef, 0xbb, 0xbf, 123, 125]),
        new Uint8Array([123, 0, 125]),
      ]
    ) {
      await Deno.writeFile(path, bytes);
      let rejected = false;
      try {
        await captureMetadata(path);
      } catch {
        rejected = true;
      }
      assert(rejected, "Default reader accepted malformed encoding/BOM/raw NUL");
    }
    let rejected = false;
    try {
      await captureMetadata(directory);
    } catch {
      rejected = true;
    }
    assert(rejected, "Default reader accepted nonregular directory");
    await Deno.writeFile(path, new Uint8Array());
    assert(
      await captureMetadata(path) === "",
      "Empty capture must remain empty for semantic validator",
    );
  } finally {
    await Deno.remove(directory, { recursive: true });
  }
});

Deno.test("OPS04 solver CLI preserves argv compatibility and captures once for HTTPS/file builds", async () => {
  for (
    const url of ["https://artifacts.example.invalid/depot.tar.gz", "file:///artifact/depot.tar.gz"]
  ) {
    const raw = JSON.stringify(depot(url), null, 2);
    const input = trackedInput(encoder.encode(raw), { chunk: 7 });
    const commands: Command[] = [];
    const captures: Array<boolean | undefined> = [];
    const receipt = await solverCli([
      "synthetic-depot.json",
      "--profile",
      "production-build",
      "--test-workers",
      "16",
    ], {
      openDepotInput: input.open,
      readSourceGraph: () => Promise.resolve(structuredClone(graph)),
      readJuliaManifestSha256: () => Promise.resolve(manifestSha),
      execute: (command, capture) => {
        commands.push(command);
        captures.push(capture);
        return Promise.resolve("");
      },
    });
    assert(input.opens === 1 && input.closes === 1, "Solver CLI must use one actual capture");
    assert(
      commands.length === (url.startsWith("file:") ? 2 : 1),
      "Solver CLI dispatch route changed",
    );
    assert(
      captures.every((value) => value !== true),
      "Solver CLI unexpectedly captures command stdout",
    );
    const command = commands.at(-1)!;
    await bound(command, receipt, raw, url, hash);
    assert(argument(command, "juliaTestProfile") === "production-build", "Solver CLI profile lost");
    const worker = command.args.indexOf("juliaTestWorkerLimit");
    assert(command.args[worker + 1] === "16", "Solver CLI worker flag lost");
  }
});

Deno.test("OPS04 solver CLI invalid argv encoding size graph and lock preflight dispatch no commands", async () => {
  const wrong = depot();
  wrong.sources.components[0].revision = "f".repeat(40);
  const valid = encoder.encode(JSON.stringify(depot()));
  const fixtures = [
    { args: [], bytes: valid },
    { args: ["input.json", "--profile", "unknown"], bytes: valid },
    { args: ["input.json", "--test-workers", "16", "--test-workers", "32"], bytes: valid },
    { args: ["input.json", "--unexpected", "value"], bytes: valid },
    { args: ["input.json"], bytes: new Uint8Array(65537).fill(65) },
    { args: ["input.json"], bytes: new Uint8Array([0xc3, 0x28]) },
    { args: ["input.json"], bytes: encoder.encode(JSON.stringify(wrong)) },
    { args: ["input.json"], bytes: encoder.encode("{}") },
    { args: ["input.json"], bytes: valid, lock: "e".repeat(64) },
  ];
  for (const fixture of fixtures) {
    const input = trackedInput(fixture.bytes, { chunk: 97 });
    let calls = 0;
    let rejected = false;
    try {
      await solverCli(fixture.args, {
        openDepotInput: input.open,
        readSourceGraph: () => Promise.resolve(structuredClone(graph)),
        readJuliaManifestSha256: () => Promise.resolve(fixture.lock ?? manifestSha),
        execute: () => {
          calls++;
          return Promise.resolve("");
        },
      });
    } catch {
      rejected = true;
    }
    assert(rejected && calls === 0, "Solver CLI preflight allowed dispatch");
    assert(
      input.opens <= 1 && input.opens === input.closes,
      "Solver CLI failed capture leaked/reopened input",
    );
  }
});
