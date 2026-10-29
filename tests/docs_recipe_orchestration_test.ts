// deno-lint-ignore-file require-await -- Inert async DI fakes match the production adapter signatures.
// Source-only literal request/transport controls; no native tools or target imports.
import {
  captureDocsFile,
  captureDocsRequest,
  checkLayout,
  checkLayoutFiles,
  currentDocsSource,
  type DocsRequest,
  inventoryTree,
  type PackagePlan,
  parseDocsArgs,
  parseDocsJson,
  parseDocsNixOutput,
  parseDocsRequest,
  planDocsBuild,
  readBounded,
  runDocsBuild,
  sha256,
} from "../ops/docs.ts";
import { type RetainedResult } from "../ops/process.ts";
import { type SourceGraph } from "../ops/git.ts";
function ok(v: unknown, m = "assertion failed"): asserts v {
  if (!v) throw Error(m);
}
async function refuses(f: () => unknown | Promise<unknown>) {
  let failed = false;
  try {
    await f();
  } catch {
    failed = true;
  }
  ok(failed, "expected refusal");
}
const graph: SourceGraph = {
  format: "qcl-negf.git-graph.v1",
  revision: "a".repeat(40),
  components: [{
    path: "components/QCLNEGF.jl",
    revision: "b".repeat(40),
    url: "https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl",
  }],
};
const encoder = new TextEncoder();
const manifest = "d".repeat(64);
const ref = (path: string) => ({ path, sha256: "f".repeat(64) });
const request = (): DocsRequest => ({
  format: "qcl-negf.docs-request.v1",
  depot_metadata: ref("/captured/depot"),
  asset_inputs: ref("/captured/assets"),
  review_inputs: ref("/captured/reviews"),
  factory: { profile: "production-build", test_workers: 2 },
});
async function fixture() {
  const raw = " \n" + JSON.stringify({
    format: "qcl-negf.julia-depot.v1",
    sources: graph,
    julia: "1.13.0",
    juliaManifest: manifest,
    url: "https://artifacts.example.invalid/depot",
    hash: "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
    unicode: "Проверка",
  }) + "\n";
  const req = request();
  const files = {} as Awaited<ReturnType<typeof captureDocsRequest>>["files"];
  for (const key of ["depot_metadata", "asset_inputs", "review_inputs"] as const) {
    const text = key === "depot_metadata" ? raw : "{}\n";
    const sha = await sha256(encoder.encode(text));
    req[key].sha256 = sha;
    files[key] = { ref: { ...req[key] }, raw: text };
  }
  return { request: req, raw_sha256: "e".repeat(64), files };
}
async function plan(mode: PackagePlan["mode"] = "build") {
  return await planDocsBuild(await fixture(), graph, {
    root: "/selected root/Русский",
    inputFile: "/tmp/inputs.json",
    manifestSha256: manifest,
    mode,
  });
}
const output = "/nix/store/" + "a".repeat(32) + "-docs";
function response(text = JSON.stringify([{ outputs: { out: output } }])): RetainedResult {
  const bytes = encoder.encode(text);
  return {
    stdout: bytes,
    stderr: new Uint8Array(),
    receipt: { path: "/tmp/receipt", sha256: "e".repeat(64) },
    result: {
      reason: null,
      exit: { code: 0, success: true },
      drain: "complete",
      errors: [],
      stdout_received_bytes: bytes.length,
      stderr_received_bytes: 0,
      stdout_attempted_bytes: bytes.length,
      stderr_attempted_bytes: 0,
      stdout_acknowledged_bytes: bytes.length,
      stderr_acknowledged_bytes: 0,
      retention: "acknowledged",
      process_tree_terminated: null,
      resource_measurements: null,
    },
  };
}
Deno.test("closed docs request preserves owned values and rejects getters/symbols/unknowns", async () => {
  const req = request(), parsed = parseDocsRequest(req);
  req.factory.test_workers = 7;
  ok(parsed.factory.test_workers === 2);
  for (
    const mutate of [
      (r: Record<string, unknown>) => r.extra = undefined,
      (r: Record<string, unknown>) =>
        Object.defineProperty(r, "format", {
          get() {
            throw Error("getter");
          },
        }),
      (r: Record<string, unknown>) => r[Symbol("extra") as unknown as string] = 1,
    ]
  ) {
    const r = structuredClone(parsed);
    mutate(r as unknown as Record<string, unknown>);
    await refuses(() => parseDocsRequest(r));
  }
  for (const path of ["/x/../y", "/x//y", "/x/", "/x\n/y"]) {
    const r = request();
    r.asset_inputs.path = path;
    await refuses(() => parseDocsRequest(r));
  }
  for (const n of [0, -1, 1.5, Infinity, NaN]) {
    const r = request();
    r.factory.test_workers = n;
    await refuses(() => parseDocsRequest(r));
  }
  const r = request();
  r.factory.profile = "local-debug";
  r.factory.test_workers = 3;
  await refuses(() => parseDocsRequest(r));
});
Deno.test("strict duplicate decoded keys/nonfinite/depth refuse before dispatch", async () => {
  for (
    const raw of [
      '{"a":1,"a":2}',
      '{"a":1,"\\u0061":2}',
      '{"a":1e999}',
      '{"a":NaN}',
      "[".repeat(66) + "0" + "]".repeat(66),
    ]
  ) await refuses(() => parseDocsJson(raw));
  ok(
    JSON.stringify(parseDocsJson(' {"x":[null,false,0,"Русский"]} ')) ===
      '{"x":[null,false,0,"Русский"]}',
  );
});
Deno.test("ordinary CLI distinguishes plan/prepare/build without pilot admission", async () => {
  for (const mode of ["plan", "prepare", "build"]) {
    ok(parseDocsArgs([mode, "--inputs", "/tmp/with space.json"]).mode === mode);
    ok(parseDocsArgs([mode], "/tmp/fallback").inputs === "/tmp/fallback");
  }
  for (
    const args of [[], ["preflight"], ["build"], ["build", "--inputs", "/a", "--inputs", "/b"], [
      "build",
      "--admission",
      "/x",
    ]]
  ) await refuses(() => parseDocsArgs(args));
});
Deno.test("same-FD capture retains exact Unicode/whitespace and refuses symlinks/caps", async () => {
  const dir = await Deno.makeTempDir();
  const path = `${dir}/input`;
  const raw = ' \n{"значение":"данные"}\n';
  await Deno.writeTextFile(path, raw);
  const captured = await captureDocsFile(path);
  ok(captured.raw === raw);
  ok(captured.ref.sha256 === await sha256(encoder.encode(raw)));
  await refuses(() => captureDocsFile(path, 2));
  await Deno.symlink(path, `${dir}/link`);
  await refuses(() => captureDocsFile(`${dir}/link`));
  await Deno.writeFile(path, new Uint8Array([0xff]));
  await refuses(() => captureDocsFile(path));
  await Deno.remove(dir, { recursive: true });
});
Deno.test("request capture rejects mismatched binding and detaches reader aliases", async () => {
  const snap = await fixture();
  const raw = JSON.stringify(snap.request);
  const root = { ref: ref("/request"), raw };
  let calls = 0;
  const got = await captureDocsRequest("/request", async (path) => {
    calls++;
    if (path === "/request") return root;
    return Object.values(snap.files).find((f) => f.ref.path === path)!;
  });
  snap.files.asset_inputs.raw = "changed";
  root.raw = "changed";
  ok(got.files.asset_inputs.raw === "{}\n" && calls === 4);
  await refuses(() =>
    captureDocsRequest(
      "/request",
      async (path) => path === "/request" ? { ref: ref(path), raw } : { ref: ref(path), raw: "{}" },
    )
  );
});
Deno.test("ordinary package argv binds CURRENT source but preserves original raw depot bytes", async () => {
  const snap = await fixture();
  const p = await planDocsBuild(snap, graph, {
    root: "/selected root/Русский",
    inputFile: "/tmp/inputs.json",
    manifestSha256: manifest,
    mode: "build",
  });
  const input = JSON.parse(p.inputs);
  ok(input.depot_capture_json === snap.files.depot_metadata.raw);
  ok(input.depot_capture_sha256 === snap.files.depot_metadata.ref.sha256);
  ok(
    input.source.includes("selected%20root") && input.source.includes(`rev=${graph.revision}`) &&
      input.source.includes("submodules=1"),
  );
  ok(
    p.command.args.includes("--keep-failed") && !p.command.args.includes("--option") &&
      !p.command.args.includes("--builders"),
  );
  ok(p.inputs_sha256 === await sha256(encoder.encode(p.inputs)));
  ok((await plan("prepare")).command.args.at(-1) === "inputs");
  const stale = structuredClone(graph);
  stale.revision = "c".repeat(40);
  await refuses(() =>
    planDocsBuild(snap, stale, {
      root: "/root",
      inputFile: "/tmp/i",
      manifestSha256: manifest,
      mode: "build",
    })
  );
});
Deno.test("package planning snapshots source/request before hash awaits", async () => {
  const snap = await fixture(), g = structuredClone(graph);
  const promise = planDocsBuild(snap, g, {
    root: "/root",
    inputFile: "/tmp/i",
    manifestSha256: manifest,
    mode: "build",
  });
  g.revision = "c".repeat(40);
  snap.request.factory.test_workers = 99;
  snap.files.depot_metadata.raw = "{}";
  const p = await promise;
  ok(p.selected.revision === graph.revision && JSON.parse(p.inputs).factory.test_workers === 2);
});
Deno.test("build success requires retained output exact bundle graph and after-read", async () => {
  const p = await plan();
  let reads = 0;
  const result = await runDocsBuild(p, {
    readGraph: async () => {
      reads++;
      return graph;
    },
    execute: async (call) => {
      call.args.length = 0;
      return response();
    },
    readBundle: async (path) => {
      const raw = JSON.stringify({ format: "qcl-negf.docs-bundle.v1", sources: graph });
      return { ref: { path, sha256: await sha256(encoder.encode(raw)) }, raw };
    },
  });
  ok(
    result.state === "completed" && reads === 2 && p.command.args.length > 0 &&
      result.bundle_sha256 ===
        await sha256(
          encoder.encode(JSON.stringify({ format: "qcl-negf.docs-bundle.v1", sources: graph })),
        ),
  );
});
Deno.test("source drift/missing proof/lost reply cannot produce completed", async () => {
  for (
    const fault of [
      "before",
      "after",
      "reply",
      "bundle",
      "retention",
      "stderr",
      "bad-output",
      "exit",
    ]
  ) {
    let reads = 0, calls = 0;
    const r = await runDocsBuild(await plan(), {
      readGraph: async () => {
        reads++;
        const g = structuredClone(graph);
        if (fault === "before" || fault === "after" && reads === 2) g.revision = "c".repeat(40);
        return g;
      },
      execute: async () => {
        calls++;
        if (fault === "reply") throw Error("lost");
        const r = response(fault === "bad-output" ? "[]" : undefined);
        if (fault === "retention") r.result.retention = "failed_unknown_partial";
        if (fault === "stderr") r.result.stderr_received_bytes = 1;
        if (fault === "exit") {
          r.result.reason = "exit_failure";
          r.result.exit = { code: 2, success: false };
        }
        return r;
      },
      readBundle: async () => {
        throw Error("missing");
      },
    });
    ok(r.state === (fault === "before" || fault === "exit" ? "failed" : "unknown"), fault);
    ok(calls === (fault === "before" ? 0 : 1));
  }
});
Deno.test("plan never dispatches and malformed Nix outputs fail closed", async () => {
  let calls = 0;
  const r = await runDocsBuild(await plan("plan"), {
    readGraph: async () => graph,
    execute: async () => {
      calls++;
      return response();
    },
  });
  ok(r.state === "completed" && calls === 0);
  for (
    const raw of [
      "[]",
      "[{},{}]",
      '[{"outputs":{"out":"/tmp/foreign"}}]',
      '[{"outputs":{"out":"' + output + '","dev":"' + output + '"}}]',
    ]
  ) await refuses(() => parseDocsNixOutput(encoder.encode(raw)));
  ok(currentDocsSource("/root", graph).includes(graph.revision));
});
Deno.test("layout/inventory keeps fresh canonical nonoverlap and byte bounds", async () => {
  const base = await Deno.makeTempDir(), root = `${base}/root`, attempt = `${base}/attempt`;
  const value = {
    root,
    attempt,
    owner: "core" as const,
    source: `${attempt}/stage/core/src`,
    build: `${attempt}/raw/core`,
  };
  checkLayout(value);
  await Deno.mkdir(`${root}/julia`, { recursive: true });
  await Deno.writeTextFile(`${root}/julia/Project.toml`, "");
  await Deno.writeTextFile(`${root}/julia/Manifest.toml`, "");
  await Deno.mkdir(value.source, { recursive: true });
  await Deno.mkdir(`${attempt}/raw`);
  await checkLayoutFiles(value);
  await Deno.mkdir(value.build);
  await refuses(() => checkLayoutFiles(value));
  await Deno.remove(value.build);
  await Deno.writeTextFile(`${value.source}/a`, "abc");
  ok((await inventoryTree(value.source, 5, 3))[0].bytes === 3);
  await refuses(() => inventoryTree(value.source, 5, 2));
  await Deno.symlink(`${value.source}/a`, `${value.source}/link`);
  await refuses(() => inventoryTree(value.source, 5, 10));
  let closed = false;
  await refuses(() =>
    readBounded(
      {
        read: async (b) => {
          b.fill(1);
          return b.length;
        },
        close() {
          closed = true;
        },
      },
      3,
      1,
    )
  );
  ok(closed);
  await Deno.remove(base, { recursive: true });
});

Deno.test("planner rejects invalid closed DTO before copy can normalize it", async () => {
  for (const kind of ["symbol", "accessor", "extra", "invalid-asset-json"]) {
    const snap = await fixture();
    if (kind === "symbol") Object.defineProperty(snap.request, Symbol("extra"), { value: 1 });
    if (kind === "accessor") {
      Object.defineProperty(snap.request.factory, "profile", { get: () => "production-build" });
    }
    if (kind === "extra") Object.assign(snap.files.asset_inputs, { extra: undefined });
    if (kind === "invalid-asset-json") {
      snap.files.asset_inputs.raw = '{"a":1,"a":2}';
      snap.files.asset_inputs.ref.sha256 = await sha256(
        encoder.encode(snap.files.asset_inputs.raw),
      );
      snap.request.asset_inputs.sha256 = snap.files.asset_inputs.ref.sha256;
    }
    await refuses(() =>
      planDocsBuild(snap, graph, {
        root: "/root",
        inputFile: "/tmp/i",
        manifestSha256: manifest,
        mode: "build",
      })
    );
  }
});

Deno.test("a bundle reader cannot substitute hash/path for retained raw bytes", async () => {
  for (const defect of ["hash", "path", "graph"]) {
    const result = await runDocsBuild(await plan(), {
      readGraph: async () => graph,
      execute: async () => response(),
      readBundle: async (path) => {
        const different = structuredClone(graph);
        if (defect === "graph") different.revision = "c".repeat(40);
        const raw = JSON.stringify({ format: "qcl-negf.docs-bundle.v1", sources: different });
        return {
          ref: {
            path: defect === "path" ? "/tmp/foreign" : path,
            sha256: defect === "hash" ? "f".repeat(64) : await sha256(encoder.encode(raw)),
          },
          raw,
        };
      },
    });
    ok(result.state === "unknown", defect);
  }
});

Deno.test("factory profile is a primitive literal for JSON requests and package planning", async () => {
  for (
    const factory of [
      { profile: ["production-build"], test_workers: 2 },
      { profile: ["local-debug"], test_workers: 999 },
    ]
  ) {
    // Ordinary JSON values, without accessors or custom prototypes.
    const input = parseDocsJson(JSON.stringify({ ...request(), factory }));
    await refuses(() => parseDocsRequest(input));
  }
  const snapshot = await fixture();
  snapshot.request = parseDocsJson(JSON.stringify({
    ...snapshot.request,
    factory: { profile: ["production-build"], test_workers: 2 },
  })) as DocsRequest;
  await refuses(() =>
    planDocsBuild(snapshot, graph, {
      root: "/root",
      inputFile: "/tmp/inputs.json",
      manifestSha256: manifest,
      mode: "build",
    })
  );
});
Deno.test("factory profile rejection never executes a custom coercion hook", async () => {
  let coerced = 0;
  const profile = {
    toString() {
      coerced++;
      return "production-build";
    },
  };
  await refuses(() => parseDocsRequest({ ...request(), factory: { profile, test_workers: 2 } }));
  ok(coerced === 0, "invalid profile must be refused without invoking toString");
});
Deno.test("factory profile healthy literals retain their exact worker policies", async () => {
  for (const profile of ["production-build", "local-debug"] as const) {
    const validWorkers = profile === "local-debug"
      ? [null, 2]
      : [null, 1, 2, 999, Number.MAX_SAFE_INTEGER];
    for (const test_workers of validWorkers) {
      const factory = { profile, test_workers };
      const parsed = parseDocsRequest(parseDocsJson(JSON.stringify({ ...request(), factory })));
      ok(parsed.factory.profile === profile && parsed.factory.test_workers === test_workers);
    }
    for (const test_workers of [0, -1, 1.5, true, Number.MAX_SAFE_INTEGER + 1]) {
      await refuses(() => parseDocsRequest({ ...request(), factory: { profile, test_workers } }));
    }
  }
  for (const test_workers of [1, 3, 999]) {
    await refuses(() =>
      parseDocsRequest({ ...request(), factory: { profile: "local-debug", test_workers } })
    );
  }
  for (const profile of [null, false, 7, {}, [], ["production-build", "local-debug"], "unknown"]) {
    await refuses(() => parseDocsRequest({ ...request(), factory: { profile, test_workers: 2 } }));
  }
});
