import { deploymentManifest, immutableStorePath } from "../ops/application_cd.ts";
import { type SourceGraph } from "../ops/git.ts";

const graph: SourceGraph = {
  format: "qcl-negf.git-graph.v1",
  revision: "a".repeat(40),
  components: [{
    path: "components/QCLNEGFRunner.jl",
    revision: "b".repeat(40),
    url: "https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl",
  }],
};
const application = "/nix/store/" + "a".repeat(32) + "-qcl-application";
const solver = "/nix/store/" + "b".repeat(32) + "-qcl-solver";
const hash = "sha256-" + btoa(String.fromCharCode(...Array(32).fill(1)));

function assert(value: boolean, message: string): void {
  if (!value) throw new Error(message);
}

Deno.test("CD binds executable identity to both source and immutable closure hashes", async () => {
  const value = await deploymentManifest(graph, application, solver, {
    [application]: { narHash: hash },
    [solver]: { narHash: hash },
  });
  assert(value.solver_executable === `${solver}/bin/qcl-negf`, "Pinned executable missing");
  assert(value.application_path === application, "Pinned application missing");
  assert(/^[a-f0-9]{64}$/.test(value.release_id), "Content identity missing");
  const another = await deploymentManifest(
    { ...graph, revision: "c".repeat(40) },
    application,
    solver,
    {
      [application]: { narHash: hash },
      [solver]: { narHash: hash },
    },
  );
  assert(value.release_id !== another.release_id, "A different source reused a release identity");
});

Deno.test("CD refuses mutable paths and missing closure evidence", async () => {
  for (const path of ["/run/current-system", "/nix/store/../mutable", application + "/bin"]) {
    let rejected = false;
    try {
      immutableStorePath(path);
    } catch {
      rejected = true;
    }
    assert(rejected, "Mutable or malformed closure was accepted");
  }
  let rejected = false;
  try {
    await deploymentManifest(graph, application, solver, { [application]: { narHash: hash } });
  } catch {
    rejected = true;
  }
  assert(rejected, "A release without solver closure evidence was accepted");
});

Deno.test("CD carries the selected cache without changing binary release identity", async () => {
  const evidence = { [application]: { narHash: hash }, [solver]: { narHash: hash } };
  const value = await deploymentManifest(
    graph,
    application,
    solver,
    evidence,
    "https://cache.example.invalid",
  );
  assert(
    value.cache_uri === "https://cache.example.invalid",
    "Controller lost the published cache",
  );
  const mirror = await deploymentManifest(
    graph,
    application,
    solver,
    evidence,
    "ssh://mirror.example.invalid",
  );
  assert(
    value.release_id === mirror.release_id,
    "Transport mirror changed the binary release identity",
  );
  for (
    const cache of [
      "",
      "--option",
      "https://cache.example.invalid/\n",
      "https://user:example-password@cache.example.invalid",
    ]
  ) {
    let rejected = false;
    try {
      await deploymentManifest(graph, application, solver, evidence, cache);
    } catch {
      rejected = true;
    }
    assert(rejected, "Malformed cache URI was accepted");
  }
});

Deno.test("OPS04 cache password parity rejects explicit empty and encoded passwords", async () => {
  const evidence = { [application]: { narHash: hash }, [solver]: { narHash: hash } };
  // Literal table shared in meaning with the independent Platform fixtures. These
  // are synthetic values; assertion messages deliberately omit URI contents.
  const rejected: unknown[] = [
    "https://user:example-password@cache.example.invalid",
    "https://user:@cache.example.invalid",
    "https://:@cache.example.invalid",
    "ssh://account:@cache.example.invalid",
    "ssh-ng://account:@cache.example.invalid",
    "ssh://account:%70%61%73%73@cache.example.invalid",
    "https://user:%3A@cache.example.invalid",
    "https://[malformed",
    "--option",
    "https://cache.example.invalid/ white",
    "https://cache.example.invalid/\t",
    "https://cache.example.invalid/\n",
    "https://cache.example.invalid/\0",
    "https://cache.example.invalid/\u001f",
    "https://cache.example.invalid/\u007f",
    "",
    7,
    null,
    {},
  ];
  for (const cache of rejected) {
    let refused = false;
    try {
      await deploymentManifest(graph, application, solver, evidence, cache as string);
    } catch {
      refused = true;
    }
    assert(refused, "Cache password or argument guard must refuse before publication");
  }
});

Deno.test("OPS04 cache username-only and existing local routes preserve literal URI and release identity", async () => {
  const evidence = { [application]: { narHash: hash }, [solver]: { narHash: hash } };
  const baseline = await deploymentManifest(graph, application, solver, evidence);
  assert(!("cache_uri" in baseline), "No-cache manifest gained a transport");
  for (
    const cache of [
      "https://cache.example.invalid",
      "ssh://account@cache.example.invalid",
      "ssh-ng://account@cache.example.invalid",
      "ssh://account%3Aname@cache.example.invalid",
      "file:///tmp/qcl-cache",
      "/tmp/qcl-cache",
      "local?root=/tmp/qcl-cache",
    ]
  ) {
    const value = await deploymentManifest(graph, application, solver, evidence, cache);
    assert(value.cache_uri === cache, "Cache URI must remain literal argument data");
    assert(value.release_id === baseline.release_id, "Transport changed binary identity");
    assert(value.closures.length === 2, "Transport changed closure inventory");
  }
});

import * as applicationCdModule from "../ops/application_cd.ts";
import { type Command } from "../ops/process.ts";
interface CdInputFile {
  stat(): Promise<{ isFile: boolean }>;
  read(buffer: Uint8Array): Promise<number | null>;
  close(): void;
}
interface CdBinding {
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
interface CdDependencies {
  openDepotInput(path: string): Promise<CdInputFile>;
  readSourceGraph(): Promise<SourceGraph>;
  readJuliaManifestSha256(): Promise<string>;
  execute(command: Command, capture?: boolean): Promise<string>;
}
const applicationCli = (applicationCdModule as unknown as {
  runApplicationCdCli(args: readonly string[], dependencies?: Partial<CdDependencies>): Promise<{
    manifest: Awaited<ReturnType<typeof deploymentManifest>>;
    depotBinding: CdBinding;
  }>;
}).runApplicationCdCli;
const cdEncoder = new TextEncoder();
const cdManifestSha = "d".repeat(64);
const cdOtherHash = "sha256-" + btoa(String.fromCharCode(...Array(32).fill(2)));
function cdDepot(url = "file:///artifact/depot-A.tar.gz", archiveHash = hash) {
  return {
    format: "qcl-negf.julia-depot.v1",
    sources: structuredClone(graph),
    julia: "1.13.0",
    juliaManifest: cdManifestSha,
    url,
    hash: archiveHash,
  };
}
async function cdSha(value: string): Promise<string> {
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", cdEncoder.encode(value)));
  return Array.from(digest, (byte) => byte.toString(16).padStart(2, "0")).join("");
}
async function absent(path: string): Promise<boolean> {
  try {
    await Deno.stat(path);
    return false;
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) return true;
    throw error;
  }
}
function cdArgument(command: Command, name: string): string {
  const index = command.args.indexOf(name);
  assert(
    index > 0 && command.args[index - 1] === "--argstr",
    "Expected literal string data argument",
  );
  return command.args[index + 1];
}

Deno.test("OPS04 application CLI captures A before first application callback and publishes via actual pending rename", async () => {
  const directory = await Deno.makeTempDir({ prefix: "ops04-assembly-" });
  const input = `${directory}/depot.json`;
  const output = `${directory}/release.json`;
  const cache = "ssh-ng://account@cache.example.invalid";
  const specA = cdDepot();
  const specB = cdDepot("file:///artifact/depot-B.tar.gz", cdOtherHash);
  const rawA = JSON.stringify(specA, null, 2) + "\n";
  const events: string[] = [];
  const commands: Command[] = [];
  const captures: Array<boolean | undefined> = [];
  let opens = 0;
  let graphReads = 0;
  try {
    await Deno.writeTextFile(input, rawA);
    const dependencies: CdDependencies = {
      openDepotInput(path) {
        opens++;
        events.push("open");
        assert(
          path === input && opens === 1,
          "Application must capture original metadata exactly once",
        );
        return Deno.open(path, { read: true });
      },
      readSourceGraph() {
        graphReads++;
        events.push("graph");
        return Promise.resolve(structuredClone(graph));
      },
      readJuliaManifestSha256() {
        events.push("lock");
        return Promise.resolve(cdManifestSha);
      },
      async execute(command, capture) {
        commands.push(command);
        captures.push(capture);
        if (command.args[0] === "build" && command.args.includes(".#application")) {
          events.push("application");
          assert(
            opens === 1 && graphReads === 1 && events.includes("lock"),
            "Application dispatched before capture and identity preflight",
          );
          await Deno.writeTextFile(`${input}.replacement`, JSON.stringify(specB));
          await Deno.rename(`${input}.replacement`, input);
          return application;
        }
        if (command.args[0] === "store") {
          events.push("prefetch");
          return "";
        }
        if (command.args[0] === "build" && command.args.includes("nix/solver.nix")) {
          events.push("solver");
          return solver;
        }
        if (command.args[0] === "path-info") {
          events.push("path-info");
          return JSON.stringify({ [application]: { narHash: hash }, [solver]: { narHash: hash } });
        }
        if (command.args[0] === "copy") {
          events.push("copy");
          assert(
            graphReads === 2 && await absent(output) && await absent(`${output}.pending`),
            "Copy must follow recheck and precede manifest writes",
          );
          return "";
        }
        throw new Error("Unexpected external command in fixture");
      },
    };
    const result = await applicationCli([input, output, cache], dependencies);
    assert(opens === 1 && graphReads === 2, "Application capture or graph recheck missing");
    assert(
      JSON.stringify(events) ===
        JSON.stringify([
          "open",
          "graph",
          "lock",
          "application",
          "prefetch",
          "solver",
          "path-info",
          "graph",
          "copy",
        ]),
      "Assembly causality changed",
    );
    assert(
      commands.length === 5 && captures[0] === true && captures[1] === true &&
        captures[2] === true && captures[3] === true && captures[4] !== true,
      "CLI stdout capture behavior changed",
    );
    assert(
      JSON.stringify(commands[1].args) ===
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
      "Late capture selected B for prefetch",
    );
    const outgoing = cdArgument(commands[2], "depotManifestJson");
    const outgoingSha = await cdSha(outgoing);
    assert(
      cdArgument(commands[2], "depotManifestSha256") === outgoingSha,
      "Actual outgoing metadata digest mismatch",
    );
    assert(
      !commands[2].args.includes("depotManifest") && !commands[2].args.includes(input),
      "Solver received a late metadata pathname",
    );
    assert(
      JSON.parse(outgoing).url === specA.url && JSON.parse(outgoing).hash === hash,
      "Late path replacement selected B for build",
    );
    const binding = result.depotBinding;
    assert(
      binding.captured_input_sha256 === await cdSha(rawA) &&
        binding.captured_input_bytes === cdEncoder.encode(rawA).length,
      "Returned raw binding did not capture A",
    );
    assert(
      binding.consumed_metadata_sha256 === outgoingSha &&
        binding.consumed_metadata_bytes === cdEncoder.encode(outgoing).length,
      "Returned consumed binding differs from actual argv",
    );
    assert(
      binding.source_revision === graph.revision &&
        binding.julia_manifest_sha256 === cdManifestSha && binding.archive_url === specA.url &&
        binding.archive_hash === hash && binding.normalization === "JSON.parse→JSON.stringify",
      "Returned identity observation mismatch",
    );
    assert(
      JSON.stringify(commands[4].args) ===
        JSON.stringify(["copy", "--to", cache, application, solver]),
      "Cache must remain one literal argument",
    );
    const written = JSON.parse(await Deno.readTextFile(output));
    const expectedReleaseId = await cdSha(
      JSON.stringify({
        sources: graph,
        closures: [{ path: application, narHash: hash }, { path: solver, narHash: hash }],
      }),
    );
    assert(
      written.release_id === expectedReleaseId && written.release_id === result.manifest.release_id,
      "Publication changed existing binary identity",
    );
    assert(
      written.schema === "qcl-negf-release-v1" && written.cache_uri === cache &&
        written.application_path === application &&
        written.solver_executable === `${solver}/bin/qcl-negf`,
      "Written manifest contract changed",
    );
    assert(await absent(`${output}.pending`), "Successful rename left pending file");
  } finally {
    await Deno.remove(directory, { recursive: true });
  }
});

Deno.test("OPS04 application CLI accepts captured B with its archive and no cache while preserving owned identity snapshots", async () => {
  const directory = await Deno.makeTempDir({ prefix: "ops04-assembly-B-" });
  const input = `${directory}/depot.json`;
  const output = `${directory}/release.json`;
  const specB = cdDepot("file:///artifact/depot-B.tar.gz", cdOtherHash);
  const borrowedGraph = structuredClone(graph);
  const commands: Command[] = [];
  let opens = 0;
  let graphReads = 0;
  try {
    await Deno.writeTextFile(input, JSON.stringify(specB));
    const dependencies: CdDependencies = {
      openDepotInput(path) {
        opens++;
        return Deno.open(path, { read: true });
      },
      readSourceGraph() {
        graphReads++;
        return Promise.resolve(graphReads === 1 ? borrowedGraph : structuredClone(graph));
      },
      readJuliaManifestSha256: () => Promise.resolve(cdManifestSha),
      execute(command) {
        commands.push(command);
        if (command.args.includes(".#application")) {
          // Both dependency references and nested graph values must already be owned.
          dependencies.openDepotInput = () => Promise.reject(new Error("late opener mutation"));
          dependencies.readSourceGraph = () => Promise.reject(new Error("late reader mutation"));
          dependencies.readJuliaManifestSha256 = () =>
            Promise.reject(new Error("late lock mutation"));
          dependencies.execute = () => Promise.reject(new Error("late dispatch mutation"));
          borrowedGraph.components[0].revision = "f".repeat(40);
          return Promise.resolve(application);
        }
        if (command.args[0] === "store") return Promise.resolve("");
        if (command.args[0] === "build") return Promise.resolve(solver);
        if (command.args[0] === "path-info") {
          return Promise.resolve(
            JSON.stringify([{ path: application, narHash: hash }, { path: solver, narHash: hash }]),
          );
        }
        return Promise.reject(new Error("Unexpected external command"));
      },
    };
    const result = await applicationCli([input, output], dependencies);
    assert(
      opens === 1 && graphReads === 2 && commands.length === 4,
      "Dependency capture, graph recheck or no-cache command count changed",
    );
    assert(
      commands[1].args.includes(specB.url) && commands[1].args.includes(cdOtherHash),
      "Captured B did not reach prefetch",
    );
    const outgoing = JSON.parse(cdArgument(commands[2], "depotManifestJson"));
    assert(
      outgoing.url === specB.url && outgoing.hash === cdOtherHash &&
        outgoing.sources.components[0].revision === graph.components[0].revision,
      "Borrowed identity or archive changed consumed bytes",
    );
    assert(
      result.manifest.sources.components[0].revision === graph.components[0].revision,
      "Borrowed nested graph mutated release identity",
    );
    assert(
      !("cache_uri" in result.manifest) && await absent(`${output}.pending`),
      "No-cache publication contract changed",
    );
    assert(
      JSON.parse(await Deno.readTextFile(output)).release_id === result.manifest.release_id,
      "Successful CLI did not publish output",
    );
  } finally {
    await Deno.remove(directory, { recursive: true });
  }
});

Deno.test("OPS04 application CLI metadata argv and cache preflight rejects before every execute and publication", async () => {
  const directory = await Deno.makeTempDir({ prefix: "ops04-assembly-refusal-" });
  const input = `${directory}/depot.json`;
  const output = `${directory}/release.json`;
  const wrong = cdDepot();
  wrong.sources.components[0].revision = "f".repeat(40);
  const valid = cdEncoder.encode(JSON.stringify(cdDepot()));
  const fixtures: Array<{ args: string[]; bytes: Uint8Array; lock?: string }> = [
    { args: [], bytes: valid },
    { args: [input], bytes: valid },
    { args: [input, output, "cache", "extra"], bytes: valid },
    { args: [input, output], bytes: new Uint8Array(65537).fill(65) },
    { args: [input, output], bytes: new Uint8Array([0xc3, 0x28]) },
    { args: [input, output], bytes: cdEncoder.encode(JSON.stringify(wrong)) },
    { args: [input, output], bytes: cdEncoder.encode("{}") },
    { args: [input, output], bytes: valid, lock: "e".repeat(64) },
  ];
  for (
    const cache of [
      "",
      "--option",
      "https://user:@cache.example.invalid",
      "ssh://account:@cache.example.invalid",
      "ssh-ng://account:%70@cache.example.invalid",
      "https://[broken",
      "https://cache.example.invalid/\n",
      "https://cache.example.invalid/\u007f",
    ]
  ) {
    fixtures.push({ args: [input, output, cache], bytes: valid });
  }
  try {
    for (const fixture of fixtures) {
      await Deno.writeFile(input, fixture.bytes);
      let calls = 0;
      let opens = 0;
      let rejected = false;
      try {
        await applicationCli(fixture.args, {
          openDepotInput(path) {
            opens++;
            return Deno.open(path, { read: true });
          },
          readSourceGraph: () => Promise.resolve(structuredClone(graph)),
          readJuliaManifestSha256: () => Promise.resolve(fixture.lock ?? cdManifestSha),
          execute: () => {
            calls++;
            return Promise.resolve("");
          },
        });
      } catch {
        rejected = true;
      }
      assert(rejected && calls === 0, "Application preflight dispatched external command");
      assert(
        opens <= 1 && await absent(output) && await absent(`${output}.pending`),
        "Failed preflight captured twice or published output",
      );
    }
  } finally {
    await Deno.remove(directory, { recursive: true });
  }
});

Deno.test("OPS04 application graph drift blocks copy and all manifest writes after path-info", async () => {
  const directory = await Deno.makeTempDir({ prefix: "ops04-assembly-drift-" });
  const input = `${directory}/depot.json`;
  const output = `${directory}/release.json`;
  const commands: Command[] = [];
  let graphReads = 0;
  try {
    await Deno.writeTextFile(
      input,
      JSON.stringify(cdDepot("https://artifacts.example.invalid/depot.tar.gz")),
    );
    let rejected = false;
    try {
      await applicationCli([input, output, "ssh://account@cache.example.invalid"], {
        openDepotInput: (path) => Deno.open(path, { read: true }),
        readSourceGraph() {
          graphReads++;
          const value = structuredClone(graph);
          if (graphReads > 1) value.components[0].revision = "f".repeat(40);
          return Promise.resolve(value);
        },
        readJuliaManifestSha256: () => Promise.resolve(cdManifestSha),
        execute(command) {
          commands.push(command);
          if (command.args.includes(".#application")) return Promise.resolve(application);
          if (command.args[0] === "build") return Promise.resolve(solver);
          if (command.args[0] === "path-info") {
            return Promise.resolve(
              JSON.stringify({ [application]: { narHash: hash }, [solver]: { narHash: hash } }),
            );
          }
          return Promise.reject(new Error("No copy permitted after drift"));
        },
      });
    } catch {
      rejected = true;
    }
    assert(
      rejected && graphReads === 2 && commands.length === 3 &&
        commands.at(-1)?.args[0] === "path-info",
      "Graph recheck removed or drift allowed publication dispatch",
    );
    assert(
      await absent(output) && await absent(`${output}.pending`),
      "Graph drift published manifest",
    );
  } finally {
    await Deno.remove(directory, { recursive: true });
  }
});

Deno.test("OPS04 application pending collision preserves original attempt and refuses final rename", async () => {
  const directory = await Deno.makeTempDir({ prefix: "ops04-assembly-pending-" });
  const input = `${directory}/depot.json`;
  const output = `${directory}/release.json`;
  const preserved = "existing pending attempt\n";
  const commands: Command[] = [];
  try {
    await Deno.writeTextFile(
      input,
      JSON.stringify(cdDepot("https://artifacts.example.invalid/depot.tar.gz")),
    );
    await Deno.writeTextFile(`${output}.pending`, preserved);
    let rejected = false;
    try {
      await applicationCli([input, output], {
        openDepotInput: (path) => Deno.open(path, { read: true }),
        readSourceGraph: () => Promise.resolve(structuredClone(graph)),
        readJuliaManifestSha256: () => Promise.resolve(cdManifestSha),
        execute(command) {
          commands.push(command);
          if (command.args.includes(".#application")) return Promise.resolve(application);
          if (command.args[0] === "build") return Promise.resolve(solver);
          if (command.args[0] === "path-info") {
            return Promise.resolve(
              JSON.stringify({ [application]: { narHash: hash }, [solver]: { narHash: hash } }),
            );
          }
          return Promise.reject(new Error("Unexpected external command"));
        },
      });
    } catch {
      rejected = true;
    }
    assert(rejected && commands.length === 3, "Existing pending attempt did not block publication");
    assert(
      await absent(output) && await Deno.readTextFile(`${output}.pending`) === preserved,
      "Pending collision overwrote prior attempt or renamed it as success",
    );
  } finally {
    await Deno.remove(directory, { recursive: true });
  }
});
