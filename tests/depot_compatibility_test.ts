import * as solver from "../ops/solver.ts";
import type { SourceGraph } from "../ops/git.ts";
import type { Command } from "../ops/process.ts";
const a = (ok: unknown, why: string) => {
  if (!ok) throw Error(why);
};
const sha = async (raw: string) =>
  [...new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(raw)))].map(
    (x) => x.toString(16).padStart(2, "0"),
  ).join("");
const graph: SourceGraph = {
  format: "qcl-negf.git-graph.v1",
  revision: "a".repeat(40),
  components: [{
    path: "components/QCLNEGF.jl",
    revision: "b".repeat(40),
    url: "https://github.com/example/core",
  }],
};
const manifest = "c".repeat(64);
const inputs = {
  schema: "qcl-negf.julia-depot-inputs.v1",
  system: "x86_64-linux",
  julia: {
    version: "1.13.0",
    drv: "/nix/store/" + "1".repeat(32) + "-julia.drv",
    output: "/nix/store/" + "2".repeat(32) + "-julia",
    profile: "production-build",
    test_workers: 2,
  },
  files: [{ path: "julia/Manifest.toml", sha256: manifest }],
  selector_policy: "locked-external-native-default-v1",
};
function canonical(v: unknown): string {
  if (Array.isArray(v)) return "[" + v.map(canonical).join(",") + "]";
  if (v && typeof v === "object") {
    return "{" + Object.entries(v).sort(([a], [b]) =>
      a < b ? -1 : a > b ? 1 : 0
    ).map(([k, x]) => JSON.stringify(k) + ":" + canonical(x)).join(",") + "}";
  }
  return JSON.stringify(v);
}
async function depot() {
  const digest = await sha(canonical(inputs));
  return {
    format: "qcl-negf.julia-depot.v2",
    sources: { ...graph, revision: "f".repeat(40) },
    julia: "1.13.0",
    juliaManifest: manifest,
    url: "file:///tmp/original.tar.gz",
    hash: "sha256-" + "A".repeat(43) + "=",
    compatibility: {
      schema: "qcl-negf.julia-depot-compatibility.v1",
      inputs: structuredClone(inputs),
      inputs_sha256: digest,
      native: {
        schema: "qcl-negf.julia-depot-native.v1",
        inputs_sha256: digest,
        julia_drv: inputs.julia.drv,
        julia_output: inputs.julia.output,
        observed_platform: "x86_64-linux-gnu-libgfortran5-cxx11-julia_version+1.13.0",
        preferences_sha256: "1".repeat(64),
        selector_closure_sha256: "2".repeat(64),
        artifact_selection_sha256: "3".repeat(64),
        receipt_sha256: "4".repeat(64),
      },
    },
  };
}
// Extra argument bridges pre-implementation signature so RED is a behavioral failure.
const prepare = solver.prepareDepotMetadata as unknown as (
  ...args: unknown[]
) => Promise<{ boundJson: string; binding: Record<string, unknown> }>;
Deno.test("v2 keeps original producer graph while binding selected current graph", async () => {
  const d = await depot();
  const result = await prepare(JSON.stringify(d), graph, manifest, inputs);
  a(JSON.parse(result.boundJson).sources.revision === "f".repeat(40), "original graph rewritten");
  a(result.binding.source_revision === graph.revision, "CURRENT graph lost");
  a(
    result.binding.depot_inputs_sha256 === d.compatibility.inputs_sha256,
    "missing qualified dependency binding",
  );
});
Deno.test("v2 mismatched current dependency inputs reject before commands", async () => {
  for (const field of ["manifest", "factory", "workers", "unknown", "proof"]) {
    const d = await depot();
    if (field === "manifest") d.compatibility.inputs.files[0].sha256 = "d".repeat(64);
    if (field === "factory") {
      d.compatibility.native.julia_drv = "/nix/store/" + "9".repeat(32) + "-wrong.drv";
    }
    if (field === "workers") d.compatibility.inputs.julia.test_workers = 4;
    if (field === "unknown") (d.compatibility as unknown as Record<string, unknown>).extra = true;
    if (field === "proof") d.compatibility.native.inputs_sha256 = "f".repeat(64);
    let refused = false;
    try {
      await prepare(JSON.stringify(d), graph, manifest, inputs);
    } catch {
      refused = true;
    }
    a(refused, "accepted changed " + field);
  }
});
Deno.test("v2 needs trusted current inputs, not its own supplied expectations", async () => {
  let refused = false;
  try {
    await prepare(JSON.stringify(await depot()), graph, manifest);
  } catch {
    refused = true;
  }
  a(refused, "v2 self-authorized");
});
Deno.test("v2 build URL stays current and consumed metadata preserves producer", async () => {
  const d = await depot(), commands: Command[] = [];
  const fn = solver.buildSolver as unknown as (
    ...args: unknown[]
  ) => Promise<Record<string, unknown>>;
  const r = await fn(
    JSON.stringify(d),
    graph,
    manifest,
    (c: Command) => {
      commands.push(c);
      return Promise.resolve(
        '[{"drvPath":"/nix/store/' + "3".repeat(32) + '-solver.drv","outputs":{"out":"/nix/store/' +
          "4".repeat(32) + '-solver"}}]',
      );
    },
    { profile: "production-build", testWorkerLimit: 2 },
    inputs,
  );
  a(commands.length === 2, "prefetch/build order");
  const c = commands[1];
  a(
    c.args[c.args.indexOf("source") + 1].includes("rev=" + graph.revision),
    "old producer source selected",
  );
  a(
    JSON.parse(String(r.consumed_metadata_json)).sources.revision === "f".repeat(40),
    "provenance retagged",
  );
});
Deno.test("portable binding checks actual selected graph bytes separately from canonical digest", async () => {
  const d = await depot();
  const fn = solver.buildSolver as unknown as (...args: unknown[]) => Promise<unknown>;
  const r = await fn(
    JSON.stringify(d),
    graph,
    manifest,
    () =>
      Promise.resolve(
        '[{"drvPath":"/nix/store/' + "3".repeat(32) + '-solver.drv","outputs":{"out":"/nix/store/' +
          "4".repeat(32) + '-solver"}}]',
      ),
    { profile: "production-build", testWorkerLimit: 2 },
    inputs,
  );
  const exportFn = (solver as unknown as Record<string, unknown>).workerDepotBinding as (
    r: unknown,
    v: unknown,
  ) => Promise<Record<string, unknown>>;
  a(typeof exportFn === "function", "missing portable producer export");
  const json = JSON.stringify(graph, null, 2) + "\n",
    ref = {
      path: "records/source.json",
      bytes: new TextEncoder().encode(json).length,
      sha256: await sha(json),
    };
  const b = await exportFn(r, { ref, json });
  a(
    b.selected_source_graph_record_sha256 === ref.sha256,
    "record bytes hash confused with canonical hash",
  );
  a(b.inputs_sha256 === d.compatibility.inputs_sha256, "native compatibility lost");
  let refused = false;
  try {
    await exportFn(r, { ref, json: json + " " });
  } catch {
    refused = true;
  }
  a(refused, "unbound graph bytes accepted");
});
import { deploymentManifest } from "../ops/application_cd.ts";
Deno.test("CD revalidates V2 native proof and keeps four-field release solver projection", async () => {
  const selected = {
    ...graph,
    components: [...graph.components, {
      path: "components/QCLNEGFRunner.jl",
      revision: "c".repeat(40),
      url: "https://github.com/example/runner",
    }],
  };
  const d = await depot();
  const result = await (solver.buildSolver as unknown as (
    ...args: unknown[]
  ) => Promise<solver.SolverBuildResult>)(
    JSON.stringify(d),
    selected,
    manifest,
    () =>
      Promise.resolve(
        '[{"drvPath":"/nix/store/' + "3".repeat(32) +
          '-solver.drv","outputs":{"out":"/nix/store/' + "4".repeat(32) + '-solver"}}]',
      ),
    { profile: "production-build", testWorkerLimit: 2 },
    inputs,
  );
  const app = "/nix/store/" + "5".repeat(32) + "-app";
  const receipt = {
    result,
    juliaManifestSha256: manifest,
    installedJuliaManifestSha256: manifest,
    depotInputs: inputs,
  };
  const value = await deploymentManifest(
    selected,
    app,
    result.output_path,
    { [app]: { narHash: d.hash }, [result.output_path]: { narHash: d.hash } },
    undefined,
    receipt as unknown as Parameters<typeof deploymentManifest>[5],
  );
  a(
    Object.keys(value.solver_build!).sort().join(",") ===
      "drv_path,julia_manifest_sha256,output_path,source_graph_sha256",
    "release schema expanded",
  );
});
Deno.test("programmatic V2 cannot mix selected factory resource options before dispatch", async () => {
  const d = await depot();
  let calls = 0, refused = false;
  try {
    await (solver.buildSolver as unknown as (...a: unknown[]) => Promise<unknown>)(
      JSON.stringify(d),
      graph,
      manifest,
      () => {
        calls++;
        return Promise.resolve("unexpected");
      },
      { profile: "local-debug", testWorkerLimit: null },
      inputs,
    );
  } catch {
    refused = true;
  }
  a(refused && calls === 0, "mismatched native factory options dispatched");
});
import { runApplicationCdCli } from "../ops/application_cd.ts";
import { canonicalInputs, nixDataApplication } from "../ops/depot_compatibility.ts";
Deno.test("literal canonical proof has one byte representation across languages", () => {
  a(
    canonicalInputs({ b: 2, a: ["x", null] }) === '{"a":["x",null],"b":2}',
    "canonical order/whitespace changed",
  );
  a(
    nixDataApplication({ source: "git+file:///tmp/x?rev=abc" }).startsWith(
      "f: f (builtins.fromJSON ",
    ),
    "eval function not applied",
  );
});
Deno.test("actual application CLI selects explicit v2 factory options and rejects drift before dispatch", async () => {
  const dir = await Deno.makeTempDir();
  try {
    const selected = {
      ...graph,
      components: [...graph.components, {
        path: "components/QCLNEGFRunner.jl",
        revision: "c".repeat(40),
        url: "https://github.com/example/runner",
      }],
    };
    const d = await depot(),
      file = dir + "/depot.json",
      out = dir + "/release.json",
      commands: Command[] = [];
    await Deno.writeTextFile(file, JSON.stringify(d));
    const app = "/nix/store/" + "5".repeat(32) + "-app",
      sol = "/nix/store/" + "4".repeat(32) + "-solver";
    const deps = {
      readSourceGraph: () => Promise.resolve(selected),
      readJuliaManifestSha256: () => Promise.resolve(manifest),
      readInstalledJuliaManifestSha256: () => Promise.resolve(manifest),
      readDepotInputs: (_g: SourceGraph, opt: solver.BuildOptions) => {
        a(opt.testWorkerLimit === 2, "explicit native budget lost");
        return Promise.resolve(inputs as solver.DepotInputs);
      },
      execute: (c: Command) => {
        commands.push(c);
        if (c.args.includes("--print-out-paths")) return Promise.resolve(app);
        if (c.args[0] === "path-info") {
          return Promise.resolve(
            JSON.stringify({ [app]: { narHash: d.hash }, [sol]: { narHash: d.hash } }),
          );
        }
        return Promise.resolve(
          '[{"drvPath":"/nix/store/' + "3".repeat(32) + '-solver.drv","outputs":{"out":"' + sol +
            '"}}]',
        );
      },
    };
    await runApplicationCdCli([file, out, "--test-workers", "2"], deps);
    a(
      commands.some((c) => c.args.includes("juliaTestWorkerLimit") && c.args.includes("2")),
      "solver native factory budget lost",
    );
    commands.length = 0;
    d.compatibility.native.julia_drv = "/nix/store/" + "9".repeat(32) + "-wrong.drv";
    await Deno.writeTextFile(file, JSON.stringify(d));
    let refused = false;
    try {
      await runApplicationCdCli([file, dir + "/bad.json", "--test-workers", "2"], deps);
    } catch {
      refused = true;
    }
    a(refused && commands.length === 0, "bad native binding dispatched application build");
  } finally {
    await Deno.remove(dir, { recursive: true });
  }
});
