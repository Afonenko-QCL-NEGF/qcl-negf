import * as native from "../ops/depot_producer.ts";
import { canonicalInputs, digest } from "../ops/depot_compatibility.ts";
const ok = (v: unknown, s: string) => {
  if (!v) throw Error(s);
};
Deno.test("qualification binds exact candidate raw bytes rather than parsed equivalence", async () => {
  const fn = (native as unknown as Record<string, unknown>).checkQualification as (
    ...a: unknown[]
  ) => Promise<void>;
  ok(typeof fn === "function", "missing raw-byte qualification validation");
  const raw = '{"raw":"candidate"}\n',
    inputs = "1".repeat(64),
    facts = {
      observed_platform: "linux",
      preferences_sha256: "2".repeat(64),
      selector_closure_sha256: "3".repeat(64),
      artifact_selection_sha256: "4".repeat(64),
    },
    review = "Source review evidence\n";
  const q = {
    schema: "qcl-negf.julia-depot-qualification.v1",
    candidate_sha256: await digest(raw),
    inputs_sha256: inputs,
    native_facts_sha256: await digest(canonicalInputs(facts)),
    source_review: {
      path: "review.md",
      bytes: new TextEncoder().encode(review).length,
      sha256: await digest(review),
    },
  };
  await fn(q, raw, inputs, facts, review);
  for (const changed of [raw + " ", raw.trim()]) {
    let reject = false;
    try {
      await fn(q, changed, inputs, facts, review);
    } catch {
      reject = true;
    }
    ok(reject, "normalized candidate accepted");
  }
  for (
    const path of ["../review.md", "/tmp/review.md", "nested//review.md", "nested/./review.md"]
  ) {
    let reject = false;
    try {
      await fn({ ...q, source_review: { ...q.source_review, path } }, raw, inputs, facts, review);
    } catch {
      reject = true;
    }
    ok(reject, "escaping review accepted");
  }
});
import {
  finalizeCandidate,
  readNamespace,
  runDepotV2,
  summarizeNative,
} from "../ops/depot_producer.ts";
import type { DepotInputs } from "../ops/depot_compatibility.ts";
import type { SourceGraph } from "../ops/git.ts";
Deno.test("actual producer argv isolates native environment and emits only candidate before finalize", async () => {
  const root = await Deno.makeTempDir({ prefix: "qcl-depot З # 100% " }), out = root + "/attempt";
  try {
    const graph: SourceGraph = {
      format: "qcl-negf.git-graph.v1",
      revision: "a".repeat(40),
      components: [{
        path: "components/Core",
        revision: "b".repeat(40),
        url: "https://github.com/example/core",
      }],
    };
    const inputs: DepotInputs = {
      schema: "qcl-negf.julia-depot-inputs.v1",
      system: "x86_64-linux",
      julia: {
        version: "1.13.0",
        drv: "/nix/store/" + "1".repeat(32) + "-julia.drv",
        output: "/nix/store/" + "2".repeat(32) + "-julia",
        profile: "production-build",
        test_workers: 2,
      },
      files: [{ path: "julia/Manifest.toml", sha256: "c".repeat(64) }],
      selector_policy: "locked-external-native-default-v1",
    };
    const commands: import("../ops/process.ts").Command[] = [];
    await runDepotV2(out, ["--test-workers", "2"], async (c) => {
      commands.push(c);
      if (c.executable.endsWith("/bin/julia")) {
        ok(c.clearEnv, "inherited user environment");
        ok(c.env?.JULIA_LOAD_PATH === "@:@stdlib", "global preference stack");
        ok(c.env?.JULIA_DEPOT_PATH === out + "/depot", "depot fallback");
        ok(!("JULIA" in c.env!), "arbitrary Julia override");
        await Deno.writeTextFile(
          c.args.at(-1)!,
          JSON.stringify({
            observed_platform: "x86_64-linux-gnu",
            preferences: {
              packages: {},
              environment: {
                load_path: ["@", "@stdlib"],
                depot_path: [c.env!.JULIA_DEPOT_PATH],
                active_project: c.args[1].slice("--project=".length) + "/Project.toml",
                manifest: c.args[1].slice("--project=".length) + "/Manifest.toml",
                cpu_target: "generic",
              },
            },
            selectors: [],
            artifacts: [],
          }),
          { createNew: true, mode: 0o600 },
        );
        return "";
      }
      if (c.executable === "tar") {
        await Deno.writeTextFile(out + "/depot.tar.gz", "synthetic archive", { mode: 0o600 });
        return "";
      }
      if (c.args[0] === "build") {
        return JSON.stringify([{
          drvPath: inputs.julia.drv,
          outputs: { out: inputs.julia.output },
        }]);
      }
      if (c.args[0] === "eval") {
        ok(c.args.includes("--apply"), "nix eval must apply selected-source data");
        return JSON.stringify({
          source: "/nix/store/" + "3".repeat(32) + "-source",
          caBundle: "/nix/store/" + "4".repeat(32) + "-cacert/etc/ssl/certs/ca-bundle.crt",
        });
      }
      if (c.args[0] === "hash") return "sha256-" + "A".repeat(43) + "=";
      return "";
    }, { readGraph: () => Promise.resolve(graph), readInputs: () => Promise.resolve(inputs) });
    const raw = await readNamespace(out, "depot-candidate.json"), candidate = JSON.parse(raw);
    ok(candidate.format === undefined, "candidate is usable metadata");
    const route = new URL(candidate.url);
    ok(
      route.hash === "" && decodeURIComponent(route.pathname) === out + "/depot.tar.gz",
      "archive URL changed Unicode/space/#/% filename",
    );
    let missing = false;
    try {
      await Deno.stat(out + "/solver-depot.json");
    } catch {
      missing = true;
    }
    ok(missing, "usable v2 emitted without SOURCE review");
    const review = "Independent SOURCE assessment\n";
    await Deno.writeTextFile(out + "/review.md", review, { mode: 0o600 });
    const facts = await summarizeNative(await readNamespace(out, "native-facts.json"));
    const qualification = JSON.stringify({
      schema: "qcl-negf.julia-depot-qualification.v1",
      candidate_sha256: await digest(raw),
      inputs_sha256: await digest(canonicalInputs(inputs)),
      native_facts_sha256: await digest(canonicalInputs(facts)),
      source_review: {
        path: "review.md",
        bytes: new TextEncoder().encode(review).length,
        sha256: await digest(review),
      },
    });
    const current = { ...graph, revision: "d".repeat(40) };
    const m = await finalizeCandidate(raw, qualification, review, current, inputs);
    ok(m.sources.revision === graph.revision, "finalize retagged original graph");
    let rejected = false;
    try {
      await finalizeCandidate(raw, qualification, review + "changed", current, inputs);
    } catch {
      rejected = true;
    }
    ok(rejected, "SOURCE bytes tamper accepted");
    await Deno.writeTextFile(out + "/qualification.json", qualification, { mode: 0o600 });
    await runDepotV2(
      out,
      ["--test-workers", "2", "--qualification", "qualification.json"],
      (c) => {
        commands.push(c);
        if (c.args[0] === "hash") return Promise.resolve("sha256-" + "A".repeat(43) + "=");
        throw Error("Finalize must not run Julia/build");
      },
      { readGraph: () => Promise.resolve(current), readInputs: () => Promise.resolve(inputs) },
    );
    const final = JSON.parse(await readNamespace(out, "solver-depot.json"));
    ok(final.sources.revision === graph.revision, "actual finalize retagged producer graph");
    const frozen = await Deno.lstat(out + "/solver-depot.json");
    let collision = false;
    try {
      await runDepotV2(
        out,
        ["--test-workers", "2", "--qualification", "qualification.json"],
        (c) => {
          commands.push(c);
          return Promise.resolve("sha256-" + "A".repeat(43) + "=");
        },
        { readGraph: () => Promise.resolve(current), readInputs: () => Promise.resolve(inputs) },
      );
    } catch {
      collision = true;
    }
    const after = await Deno.lstat(out + "/solver-depot.json");
    ok(
      collision && after.ino === frozen.ino && after.mtime?.getTime() === frozen.mtime?.getTime(),
      "existing metadata changed during explicit finalize retry",
    );
    ok(
      commands.filter((c) => c.executable.endsWith("/bin/julia")).length === 1,
      "unexpected extra native call",
    );
  } finally {
    await Deno.remove(root, { recursive: true });
  }
});
Deno.test("qualification namespace rejects symlink parent and hardlinks", async () => {
  const root = await Deno.makeTempDir();
  try {
    await Deno.mkdir(root + "/owned", { mode: 0o700 });
    await Deno.writeTextFile(root + "/outside.md", "outside", { mode: 0o600 });
    await Deno.symlink(root + "/outside.md", root + "/owned/review.md");
    let refused = false;
    try {
      await readNamespace(root + "/owned", "review.md");
    } catch {
      refused = true;
    }
    ok(refused, "symlink escaped owned namespace");
    await Deno.remove(root + "/owned/review.md");
    await Deno.link(root + "/outside.md", root + "/owned/review.md");
    refused = false;
    try {
      await readNamespace(root + "/owned", "review.md");
    } catch {
      refused = true;
    }
    ok(refused, "hardlinked review accepted");
  } finally {
    await Deno.remove(root, { recursive: true });
  }
});
Deno.test("raw facts without measured isolated native environment are not a candidate", async () => {
  let refused = false;
  try {
    await summarizeNative(
      JSON.stringify({
        observed_platform: "x86_64-linux-gnu",
        preferences: {},
        selectors: [],
        artifacts: [],
      }),
    );
  } catch {
    refused = true;
  }
  ok(refused, "empty native environment became qualified candidate");
});

// All subprocesses below are tiny synthetic boundaries. The expected identities
// are literals, independent of the producer's serialization/validation helpers.
async function producerSnapshotCase(
  mode:
    | "healthy"
    | "shared-source"
    | "fresh-source"
    | "shared-inputs"
    | "detached-inputs"
    | "reader-arguments"
    | "invalid-extra"
    | "invalid-nan",
) {
  const root = await Deno.makeTempDir({ prefix: "qcl-depot-snapshot-" }), out = root + "/attempt";
  const graph: SourceGraph = {
    format: "qcl-negf.git-graph.v1",
    revision: "a".repeat(40),
    components: [{
      path: "components/Core",
      revision: "b".repeat(40),
      url: "https://github.com/example/core",
    }],
  };
  const inputs: DepotInputs = {
    schema: "qcl-negf.julia-depot-inputs.v1",
    system: "x86_64-linux",
    julia: {
      version: "1.13.0",
      drv: "/nix/store/" + "1".repeat(32) + "-julia.drv",
      output: "/nix/store/" + "2".repeat(32) + "-julia",
      profile: "production-build",
      test_workers: 2,
    },
    files: [{ path: "julia/Manifest.toml", sha256: "c".repeat(64) }],
    selector_policy: "locked-external-native-default-v1",
  };
  if (mode === "invalid-extra") {
    Object.assign(inputs, { unexpected: undefined });
  }
  if (mode === "invalid-nan") inputs.julia.test_workers = NaN;
  const commands: import("../ops/process.ts").Command[] = [];
  let failure = "";
  try {
    try {
      await runDepotV2(out, ["--test-workers", "2"], async (command) => {
        commands.push(command);
        if (command.args[0] === "build") {
          if (mode === "shared-source" || mode === "fresh-source") {
            graph.revision = "d".repeat(40);
            graph.components[0].revision = "e".repeat(40);
          }
          return JSON.stringify([{
            drvPath: "/nix/store/" + "1".repeat(32) + "-julia.drv",
            outputs: { out: "/nix/store/" + "2".repeat(32) + "-julia" },
          }]);
        }
        if (command.args[0] === "eval") {
          if (mode === "shared-inputs" || mode === "detached-inputs") {
            inputs.julia.drv = "/nix/store/" + "5".repeat(32) + "-other-julia.drv";
            inputs.julia.output = "/nix/store/" + "6".repeat(32) + "-other-julia";
            inputs.files[0].sha256 = "f".repeat(64);
          }
          return JSON.stringify({
            source: "/nix/store/" + "3".repeat(32) + "-source",
            caBundle: "/nix/store/" + "4".repeat(32) + "-cacert/etc/ssl/certs/ca-bundle.crt",
          });
        }
        if (command.executable.endsWith("/bin/julia")) {
          const project = command.args[1].slice("--project=".length) + "/Project.toml";
          await Deno.writeTextFile(
            command.args.at(-1)!,
            JSON.stringify({
              observed_platform: "x86_64-linux-gnu",
              preferences: {
                packages: {},
                environment: {
                  load_path: ["@", "@stdlib"],
                  depot_path: [command.env!.JULIA_DEPOT_PATH],
                  active_project: project,
                  manifest: project.replace("Project.toml", "Manifest.toml"),
                  cpu_target: "generic",
                },
              },
              selectors: [],
              artifacts: [],
            }),
            { createNew: true, mode: 0o600 },
          );
          return "";
        }
        if (command.executable === "tar") {
          await Deno.writeTextFile(out + "/depot.tar.gz", "synthetic", { mode: 0o600 });
          return "";
        }
        if (command.args[0] === "hash") return "sha256-" + "A".repeat(43) + "=";
        throw Error("Unexpected synthetic subprocess");
      }, {
        readGraph: () =>
          Promise.resolve(
            mode === "fresh-source" || mode === "reader-arguments" ? structuredClone(graph) : graph,
          ),
        readInputs: (readerGraph, readerOptions) => {
          if (mode === "reader-arguments") {
            // A reader is allowed to mutate its own arguments. Neither the
            // retained source comparand nor the selected command options are it.
            readerGraph.revision = "d".repeat(40);
            readerGraph.components[0].revision = "e".repeat(40);
            readerOptions.profile = "local-debug";
            readerOptions.testWorkerLimit = 4;
          }
          return Promise.resolve(mode === "detached-inputs" ? structuredClone(inputs) : inputs);
        },
      });
    } catch (error) {
      failure = String(error);
    }
    let candidate: { sources: SourceGraph; inputs: DepotInputs; juliaManifest: string } | null =
      null;
    try {
      candidate = JSON.parse(await Deno.readTextFile(out + "/depot-candidate.json"));
    } catch (error) {
      if (!(error instanceof Deno.errors.NotFound)) throw error;
    }
    return { commands, candidate, failure };
  } finally {
    await Deno.remove(root, { recursive: true });
  }
}

Deno.test("producer snapshots reject shared and fresh source drift without retagging", async () => {
  for (const mode of ["healthy", "shared-source", "fresh-source"] as const) {
    const result = await producerSnapshotCase(mode), build = result.commands[0];
    ok(
      build.args[build.args.indexOf("source") + 1].includes("rev=" + "a".repeat(40)),
      "source URL changed",
    );
    if (mode === "healthy") {
      ok(
        result.candidate?.sources.revision === "a".repeat(40) && !result.failure,
        "healthy control failed",
      );
    } else {ok(
        result.candidate === null &&
          result.failure.includes("Selected source changed during prepare"),
        mode + " source drift bypassed original provenance guard",
      );}
  }
});
Deno.test("producer snapshots detach exact factory and nested manifest inputs", async () => {
  for (const mode of ["shared-inputs", "detached-inputs"] as const) {
    const result = await producerSnapshotCase(mode);
    ok(!result.failure && result.candidate !== null, mode + " control did not finish capture");
    const runtime = result.commands.find((command) => command.executable.endsWith("/bin/julia"));
    ok(
      runtime?.executable === "/nix/store/" + "2".repeat(32) + "-julia/bin/julia",
      "invoked factory differs from realized A",
    );
    ok(
      result.candidate?.inputs.julia.drv === "/nix/store/" + "1".repeat(32) + "-julia.drv",
      "candidate factory changed after capture",
    );
    ok(
      result.candidate?.inputs.files[0].sha256 === "c".repeat(64) &&
        result.candidate.juliaManifest === "c".repeat(64),
      "nested Manifest evidence remained borrowed",
    );
  }
});
Deno.test("producer snapshots keep reader argument mutations out of evidence", async () => {
  const result = await producerSnapshotCase("reader-arguments"), build = result.commands[0];
  ok(
    !result.failure && result.candidate !== null,
    "reader argument mutation corrupted retained source comparand",
  );
  ok(
    build.args[build.args.indexOf("source") + 1].includes("rev=" + "a".repeat(40)),
    "reader mutated selected source URL",
  );
  ok(
    build.args[build.args.indexOf("juliaTestProfile") + 1] === "production-build" &&
      build.args[build.args.indexOf("juliaTestWorkerLimit") + 1] === "2",
    "reader mutated retained factory options",
  );
  ok(
    result.candidate?.sources.revision === "a".repeat(40) &&
      result.candidate.sources.components[0].revision === "b".repeat(40),
    "reader received nested retained graph evidence",
  );
});

Deno.test("producer snapshots preserve invalid DTO fields for existing validation", async () => {
  for (const mode of ["invalid-extra", "invalid-nan"] as const) {
    const result = await producerSnapshotCase(mode);
    ok(
      result.failure !== "" && result.candidate === null && result.commands.length === 0,
      mode + " was normalized into accepted evidence before dispatch",
    );
  }
});
