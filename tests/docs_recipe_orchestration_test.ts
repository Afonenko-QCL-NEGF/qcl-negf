// Source-first controls. Execution requires the separately admitted fixture phase.
// Removing path/layout rejection, byte binding, deadline/caps or fail-closed BUILD
// must make these assertions fail. No real Julia, target import, network or solver.
import {
  buildBlockers,
  checkDocsAdmissionFreshness,
  checkDocsCgroup,
  checkLayout,
  type Child,
  compareDocsObservation,
  dispatchDocsBuild,
  docsBuildCommand,
  type DocsIdentity,
  docsIdentityDigest,
  docsIdentityProjection,
  type DocsObservation,
  type DocsTool,
  type GitLimits,
  GitObservationError,
  type GitReply,
  type InputObservation,
  makeDocsGitReader,
  makeDocsGitTransport,
  observeDocsSources,
  observeDocsTool,
  type Operation,
  operatorSources,
  parseDocsAdmission,
  parseDocsArgs,
  parseDocsJson,
  parseDocsNixOutput,
  parseDocsPlan,
  prepareDocsExpected,
  productionDocsGitLimits,
  readBounded,
  runFinite,
  scanDocsSources,
  withDocsSourceIdentity,
} from "../ops/docs.ts";

function assert(value: unknown, message = "assertion failed"): asserts value {
  if (!value) throw new Error(message);
}
function immediatePromise<T>(work: () => T | PromiseLike<T>): Promise<T> {
  return new Promise<T>((resolve) => resolve(work()));
}
function rejects(action: () => unknown) {
  try {
    action();
  } catch {
    return;
  }
  throw new Error("expected refusal");
}

// Source-first I2: removing actual after observation, prioritizing unknown over
// a known change, or accepting a failed Git stdout must break these controls.
const identityRoot = "/frozen/root";
const planPath = "/external/plan";
const recipePath = "/frozen/root/docs/public/make.jl";
const identityRevision = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const componentRevision = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";
const oldHash = "559aead08264d5795d3909718cdd05abd49572e84fe55590eef31a88a08fdffd"; // A
const newHash = "df7e70e5021544f4834bbee64a9e3789febc4be81470df629cad6ddb03320a5c"; // B
function present(path: string, hash = oldHash): InputObservation {
  return { kind: "present", actual: { path, bytes: 1, sha256: hash }, evidence: [] };
}
function unreadable(path: string): InputObservation {
  return {
    kind: "unreadable",
    path,
    error: { code: "permission_denied", path, detail: "fixture EACCES", evidence: [] },
  };
}
function identityFixture(maxCommands = 100) {
  const state = {
    plan: present(planPath),
    recipe: present(recipePath),
    dirty: false,
    truncated: false,
    calls: 0,
    inputCalls: 0,
    execute: 0,
    rootRevision: identityRevision,
  };
  const raw = new Uint8Array([7, 0, 255]);
  const readGit = makeDocsGitReader({
    root: identityRoot,
    attempt: "/attempts/i2",
    gitExecutable: "/admitted/git",
    limits: {
      wallMs: 100,
      drainMs: 10,
      streamBytes: 4096,
      totalBytes: 8192,
      maxCommands,
      maxTotalBytes: 100000,
      totalWallMs: 60000,
    },
    invoke: (call) =>
      immediatePromise<GitReply>(() => {
        state.calls++;
        const args = call.args.slice(8);
        let stdout: string;
        if (JSON.stringify(args) === '["rev-parse","HEAD"]') {
          stdout = call.cwd === identityRoot ? state.rootRevision : componentRevision;
        } else if (JSON.stringify(args) === '["status","--porcelain"]') {
          stdout = state.dirty ? " M recipe.jl" : "";
        } else if (JSON.stringify(args) === '["ls-tree","-rz","HEAD"]') {
          stdout = call.cwd === identityRoot
            ? `160000 commit ${componentRevision}\tcomponents/a\0`
            : "";
        } else if (
          JSON.stringify(args) ===
            JSON.stringify([
              "config",
              "-f",
              ".gitmodules",
              "--get-regexp",
              "^submodule\\..*\\.path$",
            ])
        ) {
          stdout = "submodule.a.path components/a";
        } else if (
          JSON.stringify(args) === '["config","-f",".gitmodules","--get","submodule.a.url"]'
        ) {
          stdout = "https://github.com/owner/a.git";
        } else throw new Error(`unexpected fixture argv ${JSON.stringify(args)}`);
        const bytes = new TextEncoder().encode(stdout);
        return {
          stdout: bytes,
          receipt: { path: `/attempts/i2/git/${state.calls}/result.json`, sha256: null },
          result: {
            reason: state.truncated ? "log_cap" : null,
            exit: { code: 0, success: true },
            drain: "complete",
            retention: "acknowledged",
            errors: [],
            stdout_received_bytes: bytes.length,
            stdout_attempted_bytes: bytes.length,
            stdout_acknowledged_bytes: bytes.length,
            stderr_received_bytes: 0,
            stderr_attempted_bytes: 0,
            stderr_acknowledged_bytes: 0,
            process_tree_terminated: null,
            resource_measurements: null,
          },
        };
      }),
  });
  const observe = () =>
    observeDocsSources(identityRoot, [planPath, recipePath], {
      readGit,
      readInput: (path, cap) =>
        immediatePromise<InputObservation>(() => {
          assert(cap >= 1);
          state.inputCalls++;
          return path === planPath ? state.plan : state.recipe;
        }),
      limits: { maxFiles: 2, maxFileBytes: 8, maxTotalBytes: 16 },
    });
  const prepare = async () => {
    const result = prepareDocsExpected({
      inputs: [
        { path: planPath, bytes: 1, sha256: oldHash },
        { path: recipePath, bytes: 1, sha256: oldHash },
      ],
    }, await observe());
    assert(result.kind === "expected_ready");
    return result.expected;
  };
  return { state, observe, prepare, raw, readGit };
}
Deno.test("I2 expected/before/after uses six graph observations and preserves raw failure", async () => {
  const f = identityFixture(), expected = await f.prepare();
  const result = await withDocsSourceIdentity({
    expected,
    observe: f.observe,
    execute: () =>
      immediatePromise<Operation<unknown>>(() => {
        f.state.execute++;
        return { kind: "failed", error: JSON.stringify({ exit: 7, raw: Array.from(f.raw) }) };
      }),
  });
  assert(result.state === "failed_bound" && result.candidate === null);
  assert(f.state.calls === 48 && f.state.inputCalls === 6 && f.state.execute === 1);
  assert(
    result.operation.kind === "failed" && result.operation.error === '{"exit":7,"raw":[7,0,255]}',
  );
});
for (const changed of ["plan", "recipe"] as const) {
  Deno.test(`I2 same-size ${changed} mutation is changed, not unknown`, async () => {
    const f = identityFixture(), expected = await f.prepare();
    const result = await withDocsSourceIdentity({
      expected,
      observe: f.observe,
      execute: () =>
        immediatePromise<Operation<{ exit: number; raw: number[] }>>(() => {
          f.state.execute++;
          f.state[changed] = present(changed === "plan" ? planPath : recipePath, newHash);
          return { kind: "completed", value: { exit: 7, raw: Array.from(f.raw) } };
        }),
    });
    assert(result.state === "failed_source_changed" && result.candidate === null);
    assert(result.before.actual.inputs.every((item) => item.sha256 === oldHash));
    const change = result.after.changes.find((item) => item.kind === "file_changed");
    assert(
      change?.kind === "file_changed" && change.actual.sha256 === newHash &&
        change.actual.bytes === 1 && change.expected.sha256 === oldHash,
    );
    assert(f.state.execute === 1 && result.operation.kind === "completed");
    assert(
      result.operation.value.exit === 7 &&
        JSON.stringify(result.operation.value.raw) === "[7,0,255]",
    );
  });
}
Deno.test("I2 pre-execute mismatch blocks and absence retains no invented bytes/hash", async () => {
  const f = identityFixture(), expected = await f.prepare();
  f.state.plan = { kind: "absent", path: planPath, evidence: [] };
  const result = await withDocsSourceIdentity({
    expected,
    observe: f.observe,
    execute: () =>
      immediatePromise<Operation<number>>(() => {
        f.state.execute++;
        return { kind: "completed", value: 1 };
      }),
  });
  assert(result.state === "blocked_before" && result.before.kind === "observed_changed");
  assert(result.before.changes[0].kind === "file_absent" && f.state.execute === 0);
  assert(!("bytes" in f.state.plan) && !("sha256" in f.state.plan));
});
Deno.test("I2 known change wins over unreadable input while retaining unknown evidence", async () => {
  const f = identityFixture(), expected = await f.prepare();
  const result = await withDocsSourceIdentity({
    expected,
    observe: f.observe,
    execute: () =>
      immediatePromise<Operation<unknown>>(() => {
        f.state.plan = present(planPath, newHash);
        f.state.recipe = unreadable(recipePath);
        return { kind: "failed", error: "original exit 7" };
      }),
  });
  assert(result.state === "failed_source_changed" && result.after.unknowns.length === 1);
  assert(result.after.unknowns[0].code === "permission_denied");
});
Deno.test("I2 permission error and truncated Git are unknown, successful dirty is changed", async () => {
  for (const mode of ["permission", "truncated", "dirty"] as const) {
    const f = identityFixture(), expected = await f.prepare();
    const result = await withDocsSourceIdentity({
      expected,
      observe: f.observe,
      execute: () =>
        immediatePromise<never>(() => {
          if (mode === "permission") f.state.plan = unreadable(planPath);
          if (mode === "truncated") f.state.truncated = true;
          if (mode === "dirty") f.state.dirty = true;
          throw new Error("original callback throw");
        }),
    });
    assert(
      result.operation?.kind === "unknown_partial" &&
        result.operation.error.includes("original callback throw"),
    );
    if (mode === "dirty") {
      assert(result.state === "failed_source_changed");
      assert(
        result.after.changes.some((c) =>
          c.kind === "git_dirty" && c.actual_status === " M recipe.jl"
        ),
      );
    } else assert(result.state === "failed_identity_unknown");
    assert(result.after !== null && result.candidate === null);
  }
});
Deno.test("I2 forged preparation and contradictory observation cannot be matched", async () => {
  const f = identityFixture(), expected = await f.prepare();
  const observed = await f.observe();
  const contradictory = { ...observed, inputs: [present(planPath), present(planPath)] };
  assert(compareDocsObservation(expected, contradictory).kind === "unreadable_unknown");
  let executed = false, rejected = false;
  try {
    await withDocsSourceIdentity({
      expected: JSON.parse(JSON.stringify(expected)),
      observe: f.observe,
      execute: () =>
        immediatePromise<Operation<number>>(() => {
          executed = true;
          return { kind: "completed", value: 1 };
        }),
    });
  } catch {
    rejected = true;
  }
  assert(rejected && !executed);
});
Deno.test("I2 private projection detaches and sorts without mutating raw graph", async () => {
  const f = identityFixture(), expected = await f.prepare();
  const reversed: DocsIdentity = { graph: expected.graph, inputs: [...expected.inputs].reverse() };
  const raw = JSON.stringify(reversed);
  const copy = docsIdentityProjection(reversed);
  assert(copy !== reversed && copy.graph !== reversed.graph && copy.inputs !== reversed.inputs);
  assert(JSON.stringify(reversed) === raw && copy.inputs[0].path === planPath);
  assert(await docsIdentityDigest(expected) === await docsIdentityDigest(reversed));
});
Deno.test("I2 late expected rejects frozen mismatch and graph changes stay reachable", async () => {
  const f = identityFixture(), expected = await f.prepare();
  f.state.plan = present(planPath, newHash);
  const preparation = prepareDocsExpected({ inputs: expected.inputs }, await f.observe());
  assert(
    preparation.kind === "expected_invalid" &&
      preparation.changes.some((c) => c.kind === "file_changed"),
  );
  f.state.plan = present(planPath);
  const result = await withDocsSourceIdentity({
    expected,
    observe: f.observe,
    execute: () =>
      immediatePromise<Operation<number>>(() => {
        f.state.rootRevision = "cccccccccccccccccccccccccccccccccccccccc";
        return { kind: "completed", value: 1 };
      }),
  });
  assert(
    result.state === "failed_source_changed" &&
      result.after.changes.some((c) => c.kind === "graph_changed"),
  );
});
Deno.test("I2 completed operation still needs a matched after; observer throw preserves unknown", async () => {
  const f = identityFixture(), expected = await f.prepare();
  let observations = 0;
  const result = await withDocsSourceIdentity({
    expected,
    observe: () =>
      immediatePromise<DocsObservation>(() => {
        observations++;
        if (observations === 2) throw new Error("after unavailable");
        return f.observe();
      }),
    execute: () => immediatePromise<Operation<number>>(() => ({ kind: "completed", value: 7 })),
  });
  assert(
    result.state === "failed_identity_unknown" &&
      result.after.unknowns[0].detail.includes("after unavailable"),
  );
  assert(
    result.after.observation.start.kind === "rejected" &&
      result.after.observation.inputs.length === 2,
  );
  const stable = identityFixture(), stableExpected = await stable.prepare();
  const completed = await withDocsSourceIdentity({
    expected: stableExpected,
    observe: stable.observe,
    execute: () => immediatePromise<Operation<number>>(() => ({ kind: "completed", value: 7 })),
  });
  assert(
    completed.state === "completed_bound" && completed.operation.value === 7 &&
      completed.candidate === null,
  );
});
Deno.test("I2 aggregate command budget admits no transport after exhaustion", async () => {
  const f = identityFixture(1);
  const first = await f.observe();
  assert(first.start.kind === "rejected" && first.end.kind === "rejected" && f.state.calls === 1);
  await f.observe();
  assert(f.state.calls === 1);
});
Deno.test("I2 input observation is detached and missing/additional paths remain unknown", async () => {
  const f = identityFixture(), expected = await f.prepare();
  const observation = await f.observe();
  const original = JSON.stringify(observation);
  if (f.state.plan.kind === "present") f.state.plan.actual.sha256 = newHash;
  assert(JSON.stringify(observation) === original);
  assert(
    compareDocsObservation(expected, { ...observation, inputs: observation.inputs.slice(0, 1) })
      .kind === "unreadable_unknown",
  );
  assert(
    compareDocsObservation(expected, {
      ...observation,
      inputs: [...observation.inputs, present("/additional/input")],
    }).kind === "unreadable_unknown",
  );
});

const strictGitLimits: GitLimits = {
  wallMs: 100,
  drainMs: 10,
  streamBytes: 8,
  totalBytes: 8,
  maxCommands: 8,
  maxTotalBytes: 16,
  totalWallMs: 60000,
};
const requiredGitLimits = [
  "wallMs",
  "drainMs",
  "streamBytes",
  "totalBytes",
  "maxCommands",
  "maxTotalBytes",
  "totalWallMs",
] as const;
const requiredInputLimits = ["maxFiles", "maxFileBytes", "maxTotalBytes"] as const;
function factoryForReply(reply: unknown, limits: GitLimits = strictGitLimits) {
  let calls = 0;
  const readGit = makeDocsGitReader({
    root: identityRoot,
    attempt: "/attempts/i3",
    gitExecutable: "/admitted/git",
    limits,
    invoke: () =>
      immediatePromise<GitReply>(() => {
        calls++;
        return reply as GitReply;
      }),
  });
  return { readGit, calls: () => calls };
}
async function caught(action: () => Promise<unknown>): Promise<unknown> {
  try {
    await action();
  } catch (error) {
    return error;
  }
  throw new Error("expected rejection");
}
function oneByteReply(): GitReply {
  return {
    stdout: new Uint8Array([65]),
    receipt: { path: "/attempts/i3/git/1/result.json", sha256: null },
    result: {
      reason: null,
      exit: { code: 0, success: true },
      drain: "complete",
      errors: [],
      retention: "acknowledged",
      stdout_received_bytes: 1,
      stdout_attempted_bytes: 1,
      stdout_acknowledged_bytes: 1,
      stderr_received_bytes: 0,
      stderr_attempted_bytes: 0,
      stderr_acknowledged_bytes: 0,
      process_tree_terminated: null,
      resource_measurements: null,
    },
  };
}
Deno.test("I3 every required Git limit and exact envelope are validated before transport", () => {
  const invalid: unknown[] = [null, [], { ...strictGitLimits, extra: 1 }];
  for (const key of requiredGitLimits) {
    const missing = { ...strictGitLimits };
    delete (missing as Partial<GitLimits>)[key];
    invalid.push(missing);
    for (
      const value of [
        undefined,
        true,
        "1",
        NaN,
        Infinity,
        -Infinity,
        0,
        -1,
        1.5,
        Number.MAX_SAFE_INTEGER + 1,
      ]
    ) {
      invalid.push({ ...strictGitLimits, [key]: value });
    }
  }
  let invokes = 0;
  for (const limits of invalid) {
    rejects(() =>
      makeDocsGitReader({
        root: identityRoot,
        attempt: "/attempts/i3",
        gitExecutable: "/admitted/git",
        limits: limits as GitLimits,
        invoke: () =>
          immediatePromise<GitReply>(() => {
            invokes++;
            return oneByteReply();
          }),
      })
    );
  }
  assert(invokes === 0);
});
Deno.test("I3 every required input limit is validated before Git or input reads", async () => {
  const valid = { maxFiles: 2, maxFileBytes: 8, maxTotalBytes: 16 };
  const invalid: unknown[] = [null, [], { ...valid, extra: 1 }];
  for (const key of requiredInputLimits) {
    const missing = { ...valid };
    delete (missing as Partial<typeof valid>)[key];
    invalid.push(missing);
    for (const value of [undefined, true, "1", NaN, Infinity, 0, -1, 1.5]) {
      invalid.push({ ...valid, [key]: value });
    }
  }
  let git = 0, inputs = 0;
  for (const limits of invalid) {
    await caught(() =>
      observeDocsSources(identityRoot, [planPath], {
        limits: limits as typeof valid,
        readGit: () =>
          immediatePromise<string>(() => {
            git++;
            return "";
          }),
        readInput: () =>
          immediatePromise<InputObservation>(() => {
            inputs++;
            return present(planPath);
          }),
      })
    );
  }
  assert(git === 0 && inputs === 0);
});
Deno.test("I3 malformed or contradictory reply closes admission before the next invoke", async () => {
  const valid = oneByteReply();
  const cases: unknown[] = [
    null,
    {},
    { ...valid, result: null },
    { ...valid, result: {} },
    { ...valid, result: { ...valid.result, errors: null } },
    { ...valid, stdout: "A" },
    { ...valid, result: { ...valid.result, stdout_received_bytes: -1 } },
    { ...valid, result: { ...valid.result, stdout_attempted_bytes: 2 } },
    { ...valid, receipt: { path: "relative", sha256: null } },
    {
      ...valid,
      stdout: new Uint8Array([65, 66]),
      result: {
        ...valid.result,
        stdout_received_bytes: 0,
        stdout_attempted_bytes: 0,
        stdout_acknowledged_bytes: 0,
      },
    },
  ];
  for (
    const key of [
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
    ]
  ) {
    const result: Record<string, unknown> = { ...valid.result };
    delete result[key];
    cases.push({ ...valid, result });
  }
  for (const reply of cases) {
    const f = factoryForReply(reply);
    const error = await caught(() => f.readGit(identityRoot, ["rev-parse", "HEAD"]));
    assert(error instanceof GitObservationError && error.code === "invalid_reply");
    assert(
      error.accounting?.kind === "unknown" && error.accounting.admission === "closed" &&
        error.accounting.retention === "unknown" && error.accounting.received_bytes === null,
    );
    if (
      reply && typeof reply === "object" && "stdout" in reply && reply.stdout instanceof Uint8Array
    ) {
      assert(error.accounting.observed_stdout_bytes === reply.stdout.length);
    } else assert(error.accounting.observed_stdout_bytes === null);
    if (
      reply && typeof reply === "object" && "receipt" in reply && reply.receipt === valid.receipt
    ) {
      assert(error.receipt?.path === "/attempts/i3/git/1/result.json");
    }
    const next = await caught(() => f.readGit(identityRoot, ["rev-parse", "HEAD"]));
    assert(
      next instanceof GitObservationError && next.code === "budget_exhausted" && f.calls() === 1,
    );
  }
});
Deno.test("I3 partial retained reply debits known received bytes without pretending success", async () => {
  const partial = oneByteReply();
  partial.result.reason = "log_cap";
  partial.result.retention = "incomplete_unknown_partial";
  const f = factoryForReply(partial, {
    ...strictGitLimits,
    streamBytes: 1,
    totalBytes: 1,
    maxTotalBytes: 1,
  });
  const first = await caught(() => f.readGit(identityRoot, ["rev-parse", "HEAD"]));
  assert(first instanceof GitObservationError && first.code === "log_cap");
  assert(first.accounting?.kind === "known" && first.accounting.received_bytes === 1);
  assert(first.accounting.retention === "incomplete_unknown_partial");
  assert(first.receipt?.path === "/attempts/i3/git/1/result.json");
  await caught(() => f.readGit(identityRoot, ["rev-parse", "HEAD"]));
  assert(f.calls() === 1);
});
Deno.test("I4 every hidden required limit is rejected before normalization or I/O", async () => {
  let invokes = 0, inputs = 0;
  for (const key of requiredGitLimits) {
    const limits = { ...strictGitLimits };
    Object.defineProperty(limits, key, { value: limits[key], enumerable: false });
    rejects(() =>
      makeDocsGitReader({
        root: identityRoot,
        attempt: "/attempts/i4",
        gitExecutable: "/admitted/git",
        limits,
        invoke: () =>
          immediatePromise<GitReply>(() => {
            invokes++;
            return oneByteReply();
          }),
      })
    );
  }
  for (const key of requiredInputLimits) {
    for (const maxTotalBytes of [16, 32]) {
      const limits = { maxFiles: 2, maxFileBytes: 8, maxTotalBytes };
      Object.defineProperty(limits, key, { value: limits[key], enumerable: false });
      await caught(() =>
        observeDocsSources(identityRoot, [planPath], {
          limits,
          readGit: () =>
            immediatePromise<string>(() => {
              invokes++;
              return "";
            }),
          readInput: () =>
            immediatePromise<InputObservation>(() => {
              inputs++;
              return present(planPath);
            }),
        })
      );
    }
  }
  assert(invokes === 0 && inputs === 0);
});
Deno.test("I4 accessor and introspection failures close admission without running getters", async () => {
  for (
    const field of [
      "result",
      "receipt",
      "stdout",
      "counter",
      "exit",
      "errors",
      "errorEntry",
      "receiptPath",
    ] as const
  ) {
    let getters = 0;
    const reply = oneByteReply();
    const getter = {
      enumerable: true,
      get: () => {
        getters++;
        throw new Error("getter must not execute");
      },
    };
    if (field === "counter") Object.defineProperty(reply.result, "stdout_received_bytes", getter);
    else if (field === "exit") Object.defineProperty(reply.result.exit!, "code", getter);
    else if (field === "errors") Object.defineProperty(reply.result, "errors", getter);
    else if (field === "errorEntry") {
      reply.result.errors = ["failure"];
      Object.defineProperty(reply.result.errors, "0", getter);
    } else if (field === "receiptPath") Object.defineProperty(reply.receipt, "path", getter);
    else Object.defineProperty(reply, field, getter);
    const f = factoryForReply(reply);
    const first = await caught(() => f.readGit(identityRoot, ["rev-parse", "HEAD"]));
    assert(
      first instanceof GitObservationError && first.code === "invalid_reply" &&
        first.accounting?.kind === "unknown",
    );
    const next = await caught(() => f.readGit(identityRoot, ["rev-parse", "HEAD"]));
    assert(
      next instanceof GitObservationError && next.code === "budget_exhausted" && f.calls() === 1 &&
        getters === 0,
    );
  }
  const proxy = new Proxy(oneByteReply(), {
    getOwnPropertyDescriptor: () => {
      throw new Error("introspection failed");
    },
  });
  const f = factoryForReply(proxy);
  const first = await caught(() => f.readGit(identityRoot, ["rev-parse", "HEAD"]));
  assert(first instanceof GitObservationError && first.code === "invalid_reply");
  await caught(() => f.readGit(identityRoot, ["rev-parse", "HEAD"]));
  assert(f.calls() === 1);
});
Deno.test("I4 nearby healthy data reply and serialized input policy remain usable", async () => {
  const f = factoryForReply(oneByteReply());
  assert(await f.readGit(identityRoot, ["rev-parse", "HEAD"]) === "A");
  assert(await f.readGit(identityRoot, ["rev-parse", "HEAD"]) === "A" && f.calls() === 2);
  const observer = identityFixture();
  const expected = await observer.prepare();
  assert(compareDocsObservation(expected, await observer.observe()).kind === "matched");
  let extraReads = 0;
  const changed = await caught(() =>
    observeDocsSources(identityRoot, [planPath, recipePath], {
      readGit: observer.readGit,
      limits: { maxFiles: 2, maxFileBytes: 8, maxTotalBytes: 32 },
      readInput: (path) =>
        immediatePromise<InputObservation>(() => {
          extraReads++;
          return present(path);
        }),
    })
  );
  assert(changed instanceof Error && changed.message === "input_limits_changed");
  assert(observer.state.calls === 32 && extraReads === 0);
});
const tuple = {
  root: "/sources/root",
  attempt: "/attempts/a",
  owner: "operator" as const,
  source: "/attempts/a/stage/operator/src",
  build: "/attempts/a/raw/operator",
};
Deno.test("strict CLI refuses duplicates, unknown options and missing admission", () => {
  assert(
    parseDocsArgs(["preflight", "--plan", "/p", "--attempt-directory", "/a"]).mode === "preflight",
  );
  rejects(() => parseDocsArgs(["build", "--plan", "/p", "--attempt-directory", "/a"]));
  rejects(() =>
    parseDocsArgs(["preflight", "--plan", "/p", "--plan", "/q", "--attempt-directory", "/a"])
  );
  rejects(() =>
    parseDocsArgs(["preflight", "--plan", "/p", "--attempt-directory", "/a", "--ready", "true"])
  );
});
Deno.test("layout rejects aliases and overlaps before fake importer", () => {
  let imports = 0;
  const invalid = [
    { ...tuple, attempt: "" },
    { ...tuple, root: "relative" },
    { ...tuple, source: "/attempts/a/stage/core/src" },
    { ...tuple, attempt: "/sources/root/a" },
    { ...tuple, root: "/attempts/a/root" },
    { ...tuple, root: "/sources//root" },
    { ...tuple, build: tuple.source },
  ];
  for (const value of invalid) {
    rejects(() => {
      checkLayout(value);
      imports++;
    });
  }
  assert(imports === 0);
  checkLayout({ ...tuple, root: "/attempts/ab" }); // component prefix, not string prefix
});
Deno.test("operator staging preserves frozen chapter bytes and recipe-owned index", async () => {
  const recovery = await Deno.readFile(
    new URL("../docs/public/operator-recovery.md", import.meta.url),
  );
  const recipe = await Deno.readTextFile(new URL("../docs/public/make.jl", import.meta.url));
  const staged = await operatorSources(recovery, recipe);
  assert(staged.recovery === recovery, "exact recovery bytes must be retained");
  assert(
    new TextDecoder().decode(staged.index) ===
      "# Документация оператора\n\n[Восстановление прерванного запуска](@ref operator-recovery)\n\n[Неизменяемый runtime захвата](capture-runtime-delivery.md)\n\n[Свидетельство сборки solver](solver-build-receipt.md)\n",
  );
  const changed = recovery.slice();
  changed[0] ^= 1;
  let refused = false;
  try {
    await operatorSources(changed, recipe);
  } catch {
    refused = true;
  }
  assert(refused, "changed canonical input must refuse before staging");
});
Deno.test("caller status/marker cannot manufacture BUILD readiness", () => {
  assert(buildBlockers().includes("preflight_not_observed"));
  assert(
    buildBlockers([{
      name: "asset_bytes",
      status: "blocked",
      reason: "missing actual asset",
    }])[0] === "missing actual asset",
  );
});
function fake(data: Uint8Array, status: Promise<{ code: number; success: boolean }>): Child {
  return {
    stdout: new ReadableStream({
      start(c) {
        c.enqueue(data);
        c.close();
      },
    }),
    stderr: new ReadableStream({
      start(c) {
        c.enqueue(new Uint8Array([21, 22, 23, 24, 25, 26, 27, 28]));
        c.close();
      },
    }),
    status,
    kill() {},
  };
}
Deno.test("finite drains preserve partial logs on combined cap and failed exit", async () => {
  const saved: Record<string, number[]> = { stdout: [], stderr: [] };
  const result = await runFinite(
    () =>
      fake(
        new Uint8Array([11, 12, 13, 14, 15, 16, 17, 18]),
        Promise.resolve({ code: 7, success: false }),
      ),
    (stream, bytes) =>
      immediatePromise<void>(() => {
        saved[stream].push(...bytes);
      }),
    { wallMs: 100, drainMs: 20, streamBytes: 6, totalBytes: 9 },
  );
  assert(result.reason === "log_cap");
  assert(JSON.stringify(saved) === '{"stdout":[11,12,13,14,15,16],"stderr":[21,22,23]}');
  assert(result.stdout_acknowledged_bytes === 6 && result.stderr_acknowledged_bytes === 3);
  assert(result.stdout_received_bytes === 8 && result.stderr_received_bytes === 8);
  assert(result.retention === "acknowledged");
  assert(result.exit?.code === 7);
  assert(result.process_tree_terminated === null);
});
Deno.test("rejecting sink distinguishes received bytes from acknowledged retention", async () => {
  const saved: number[] = [];
  const result = await runFinite(
    () => fake(new Uint8Array([31, 32, 33]), Promise.resolve({ code: 0, success: true })),
    (stream, bytes) =>
      immediatePromise<void>(() => {
        if (stream === "stderr") throw new Error("sink rejected; partial write unknown");
        saved.push(...bytes);
      }),
    { wallMs: 100, drainMs: 20, streamBytes: 16, totalBytes: 32 },
  );
  assert(JSON.stringify(saved) === "[31,32,33]");
  assert(result.stdout_acknowledged_bytes === 3 && result.stderr_acknowledged_bytes === 0);
  assert(result.stderr_received_bytes === 8 && result.stderr_attempted_bytes === 8);
  assert(result.retention === "failed_unknown_partial");
});
Deno.test("deadline retains exact nonzero prefix and snapshots a hanging sink", async () => {
  let release!: () => void;
  const saved: number[] = [];
  const result = await runFinite(
    () => fake(new Uint8Array([41, 42]), new Promise(() => {})),
    async (stream, bytes) => {
      if (stream === "stdout") saved.push(...bytes);
      else {await new Promise<void>((resolve) => {
          release = resolve;
        });}
    },
    { wallMs: 5, drainMs: 5, streamBytes: 16, totalBytes: 32 },
  );
  assert(JSON.stringify(saved) === "[41,42]");
  assert(result.reason === "deadline" && result.drain === "incomplete");
  assert(result.stdout_acknowledged_bytes === 2 && result.stderr_acknowledged_bytes === 0);
  assert(result.stderr_received_bytes === 8 && result.retention === "incomplete_unknown_partial");
  const snapshot = JSON.stringify(result);
  release();
  await Promise.resolve();
  await Promise.resolve();
  assert(JSON.stringify(result) === snapshot, "late sink completion must not mutate receipt");
});
Deno.test("incremental reader enforces cap plus one sentinel despite small metadata", async () => {
  let received = 0, closed = false;
  const requests: number[] = [];
  let refused = false;
  try {
    await readBounded(
      {
        read(buffer) {
          return immediatePromise<number | null>(() => {
            requests.push(buffer.length);
            buffer.fill(71);
            received += buffer.length;
            return buffer.length;
          });
        },
        close() {
          closed = true;
        },
      },
      4,
      1,
    ); // observed metadata is small, actual stream grew
  } catch {
    refused = true;
  }
  assert(refused && closed && received === 5);
  assert(requests.every((n) => n <= 5), "no read beyond cap plus sentinel");
  let offset = 0;
  const bytes = new Uint8Array([81, 82, 83]);
  const retained = await readBounded(
    {
      read(buffer) {
        return immediatePromise<number | null>(() => {
          if (offset === bytes.length) return null;
          const n = Math.min(buffer.length, bytes.length - offset);
          buffer.set(bytes.subarray(offset, offset + n));
          offset += n;
          return n;
        });
      },
      close() {},
    },
    4,
    3,
  );
  assert(JSON.stringify([...retained]) === "[81,82,83]");
  let changedClosed = false, sent = false, changedRefused = false;
  try {
    await readBounded(
      {
        read(buffer) {
          return immediatePromise<number | null>(() => {
            if (sent) return null;
            sent = true;
            buffer.set([91, 92]);
            return 2;
          });
        },
        close() {
          changedClosed = true;
        },
      },
      4,
      1,
    );
  } catch {
    changedRefused = true;
  }
  assert(changedRefused && changedClosed, "growth within cap still invalidates metadata binding");
});
Deno.test("deadline plus unclosed pipes return finite drain failure", async () => {
  let killed = false;
  const result = await runFinite(
    () => ({
      stdout: new ReadableStream(),
      stderr: new ReadableStream(),
      status: new Promise(() => {}),
      kill() {
        killed = true;
      },
    }),
    async () => {},
    { wallMs: 5, drainMs: 5, streamBytes: 6, totalBytes: 9 },
  );
  assert(killed && result.reason === "deadline");
  assert(result.drain === "incomplete");
  assert(result.exit === null);
});

// Filesystem controls are inert until an explicitly permitted fixture execution.
import { checkLayoutFiles, inventoryTree } from "../ops/docs.ts";
Deno.test("filesystem gate rejects existing outputs, ancestor links and payload links", async () => {
  const base = await Deno.makeTempDir({ prefix: "qcl-doc04-fixture-" });
  const root = `${base}/root`, attempt = `${base}/attempt`;
  const value = {
    root,
    attempt,
    owner: "operator" as const,
    source: `${attempt}/stage/operator/src`,
    build: `${attempt}/raw/operator`,
  };
  async function refuse(action: () => Promise<unknown>) {
    let refused = false;
    try {
      await action();
    } catch {
      refused = true;
    }
    assert(refused, "fixture must refuse");
  }
  try {
    await Deno.mkdir(`${root}/julia`, { recursive: true });
    await Deno.writeTextFile(`${root}/julia/Project.toml`, "[deps]\n");
    await Deno.writeTextFile(`${root}/julia/Manifest.toml`, "# fixture\n");
    await Deno.mkdir(value.source, { recursive: true });
    await Deno.mkdir(`${attempt}/raw`);
    await checkLayoutFiles(value);
    await Deno.mkdir(value.build);
    await refuse(() => checkLayoutFiles(value));
    await Deno.remove(value.build);
    await Deno.writeTextFile(value.build, "existing output");
    await refuse(() => checkLayoutFiles(value));
    await Deno.remove(value.build);
    await Deno.symlink(`${base}/missing`, value.build);
    await refuse(() => checkLayoutFiles(value));
    await Deno.remove(value.build);
    await Deno.symlink(root, `${base}/linked-root`);
    await refuse(() => checkLayoutFiles({ ...value, root: `${base}/linked-root` }));
    await Deno.symlink(`${base}/missing`, `${value.source}/payload-link`);
    await refuse(() => inventoryTree(value.source, 20, 4096));
    await Deno.remove(`${value.source}/payload-link`);
    await Deno.writeTextFile(`${value.source}/index.md`, "# fixture\n");
    assert((await inventoryTree(value.source, 20, 4096)).length === 1);
    await refuse(() => inventoryTree(value.source, 20, 1));
  } finally {
    await Deno.remove(base, { recursive: true });
  }
});

import { preflight } from "../ops/docs.ts";
Deno.test("BUILD preflight with a self-authored admission stays blocked and preserves attempt", async () => {
  const base = await Deno.makeTempDir({ prefix: "qcl-doc04-preflight-" });
  const root = `${base}/root`, attempt = `${base}/attempt`;
  try {
    await Deno.mkdir(root);
    const admission = `${base}/admission.json`, plan = `${base}/plan.json`;
    await Deno.writeTextFile(admission, '{"status":"ready","approved":true}');
    await Deno.writeTextFile(plan, "{}");
    const args = parseDocsArgs([
      "build",
      "--plan",
      plan,
      "--attempt-directory",
      attempt,
      "--admission",
      admission,
    ]);
    const fixtureGit = () => Promise.reject(new Error("fixture source unavailable"));
    const result = await preflight(args, root, { readGit: fixtureGit });
    assert(result.result === "blocked");
    assert(result.steps.length === 0 && result.admission === null);
    assert(result.checks.some((c) => c.name === "native_admission" && c.status === "blocked"));
    const original = await Deno.readFile(`${attempt}/receipt.json`);
    let reused = false;
    try {
      await preflight(args, root, { readGit: fixtureGit });
      reused = true;
    } catch { /* required refusal */ }
    assert(!reused, "attempt must never be reused");
    const retained = await Deno.readFile(`${attempt}/receipt.json`);
    assert(original.every((v, i) => retained[i] === v) && original.length === retained.length);
  } finally {
    await Deno.remove(base, { recursive: true });
  }
});

// TS6 compatibility controls: additive source fixtures; execution is separately admitted.
import { sha256 } from "../ops/docs.ts";
Deno.test("TS6 SHA literal vectors preserve exact visible byte views", async () => {
  const helperState = { called: false, threwSynchronously: false };
  const helperError = new Error("immediate helper sentinel");
  let helperRejected = Promise.resolve(0);
  try {
    helperRejected = immediatePromise<number>(() => {
      helperState.called = true;
      throw helperError;
    });
  } catch {
    helperState.threwSynchronously = true;
  }
  assert(helperState.called && !helperState.threwSynchronously);
  assert(await caught(() => helperRejected) === helperError);

  const immediateState = { called: false };
  const immediate = immediatePromise<number>(() => {
    immediateState.called = true;
    return 7;
  });
  assert(immediateState.called, "work runs before caller return");
  assert(await immediate === 7);
  let releaseInner: (value: number) => void = () => {
    throw new Error("inner resolver not initialized");
  };
  const inner = new Promise<number>((resolve) => {
    releaseInner = resolve;
  });
  const outer = immediatePromise<number>(() => inner);
  assert(outer !== inner, "adoption preserves a fresh outer Promise");
  const adoption = { fulfilled: false };
  outer.then(() => {
    adoption.fulfilled = true;
  });
  await Promise.resolve();
  assert(!adoption.fulfilled, "outer stays pending until the inner settles");
  releaseInner(7);
  assert(await outer === 7);

  const valid = await identityFixture().prepare();
  const digestError = new Error("identity graph getter sentinel");
  const digestState = { getterCalled: false, threwSynchronously: false };
  const poisoned: DocsIdentity = {
    inputs: valid.inputs,
    get graph(): never {
      digestState.getterCalled = true;
      throw digestError;
    },
  };
  let digestRejected = Promise.resolve("");
  try {
    digestRejected = docsIdentityDigest(poisoned);
  } catch {
    digestState.threwSynchronously = true;
  }
  assert(digestState.getterCalled && !digestState.threwSynchronously);
  assert(await caught(() => digestRejected) === digestError);

  const empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
  const abc = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";
  const all256 = "40aff2e9d2d8922e47afd4648e6967497158785fbd1da870e7110266bf944880";
  assert(await sha256(new Uint8Array()) === empty);
  assert(await sha256(new TextEncoder().encode("abc")) === abc);
  const guarded = new Uint8Array([17, 97, 98, 99, 231]);
  assert(await sha256(new Uint8Array(guarded.buffer, 1, 3)) === abc);
  assert(await sha256(guarded.subarray(1, 4)) === abc);
  assert(await sha256(guarded.subarray(guarded.length)) === empty);
  const payload = Uint8Array.from({ length: 256 }, (_, i) => i);
  assert(await sha256(payload) === all256);
  for (let offset = 0; offset <= 256; offset++) {
    const backing = new Uint8Array(offset + payload.length + 3);
    backing.fill(19);
    backing.set(payload, offset);
    backing.fill(237, offset + payload.length);
    assert(await sha256(new Uint8Array(backing.buffer, offset, payload.length)) === all256);
    assert(await sha256(backing.subarray(offset, offset + payload.length)) === all256);
    // Change only bytes outside the view; the literal expected digest stays fixed.
    backing.fill(83, 0, offset);
    backing.fill(149, offset + payload.length);
    assert(await sha256(new Uint8Array(backing.buffer, offset, payload.length)) === all256);
    assert(await sha256(backing.subarray(offset, offset + payload.length)) === all256);
  }
});
for (const size of [0, 1, 3, 4, 5]) {
  Deno.test(`TS6 single stdout cap4 boundary size${size}`, async () => {
    const payload = Uint8Array.from({ length: size }, (_, i) => 71 + i);
    const saved: number[] = [];
    const signals: AbortSignal[] = [];
    const result = await runFinite(() => ({
      stdout: new ReadableStream<Uint8Array>({
        start(c) {
          c.enqueue(payload);
          c.close();
        },
      }),
      stderr: new ReadableStream<Uint8Array>({
        start(c) {
          c.close();
        },
      }),
      status: Promise.resolve({ code: 0, success: true }),
      kill() {},
    }), (stream, bytes, signal) =>
      immediatePromise<void>(() => {
        assert(stream === "stdout");
        signals.push(signal);
        saved.push(...bytes);
      }), { wallMs: 100, drainMs: 20, streamBytes: 4, totalBytes: 4 });
    const kept = Math.min(size, 4);
    assert(result.stdout_received_bytes === size);
    assert(result.stdout_attempted_bytes === kept && result.stdout_acknowledged_bytes === kept);
    assert(
      result.stderr_received_bytes === 0 && result.stderr_attempted_bytes === 0 &&
        result.stderr_acknowledged_bytes === 0,
    );
    assert(JSON.stringify(saved) === JSON.stringify(Array.from(payload.subarray(0, kept))));
    assert(result.reason === (size === 5 ? "log_cap" : null));
    assert(result.drain === "complete" && result.retention === "acknowledged");
    assert(result.exit?.code === 0 && result.exit.success && result.errors.length === 0);
    assert(signals.every((signal) => !signal.aborted));
    assert(result.process_tree_terminated === null && result.resource_measurements === null);
  });
}
Deno.test("TS6 incomplete drain requests abort and hanging reader cancellation; late writes detach", async () => {
  const saved: number[] = [];
  const state = { cancelRequests: 0, sinkStarted: false, abortObserved: false };
  let releaseSink: () => void = () => {
    throw new Error("sink not started");
  };
  let releaseStatus: () => void = () => {
    throw new Error("status not created");
  };
  let finishSink: () => void = () => {
    throw new Error("sink completion not created");
  };
  const sinkFinished = new Promise<void>((resolve) => {
    finishSink = resolve;
  });
  const status = new Promise<{ code: number; success: boolean }>((resolve) => {
    releaseStatus = () => resolve({ code: 0, success: true });
  });
  const result = await runFinite(() => ({
    stdout: new ReadableStream<Uint8Array>({
      start(c) {
        c.enqueue(new Uint8Array([61, 62, 63, 64]));
      },
      cancel() {
        state.cancelRequests++;
        return new Promise<void>(() => {});
      },
    }),
    stderr: new ReadableStream<Uint8Array>({
      cancel() {
        state.cancelRequests++;
        return new Promise<void>(() => {});
      },
    }),
    status,
    kill() {},
  }), async (stream, bytes, signal) => {
    assert(stream === "stdout");
    state.sinkStarted = true;
    signal.addEventListener("abort", () => {
      state.abortObserved = signal.aborted;
    }, { once: true });
    saved.push(...bytes.subarray(0, 2));
    await new Promise<void>((resolve) => {
      releaseSink = resolve;
    });
    // A cooperative abort request does not prevent an external sink from writing.
    saved.push(...bytes.subarray(2));
    finishSink();
  }, { wallMs: 5, drainMs: 5, streamBytes: 16, totalBytes: 32 });
  assert(state.sinkStarted && state.abortObserved && state.cancelRequests === 2);
  assert(JSON.stringify(saved) === "[61,62]");
  assert(result.reason === "deadline" && result.drain === "incomplete" && result.exit === null);
  assert(
    result.stdout_received_bytes === 4 && result.stdout_attempted_bytes === 4 &&
      result.stdout_acknowledged_bytes === 0,
  );
  assert(
    result.stderr_received_bytes === 0 && result.stderr_attempted_bytes === 0 &&
      result.stderr_acknowledged_bytes === 0,
  );
  assert(result.retention === "incomplete_unknown_partial" && result.errors.length === 0);
  assert(result.process_tree_terminated === null && result.resource_measurements === null);
  const snapshot = JSON.stringify(result);
  releaseSink();
  releaseStatus();
  await sinkFinished;
  await Promise.resolve();
  await Promise.resolve();
  assert(JSON.stringify(saved) === "[61,62,63,64]", "late external writes remain possible");
  assert(JSON.stringify(result) === snapshot, "late sink/status must not promote detached receipt");
  assert(result.stdout_acknowledged_bytes === 0 && result.exit === null);
});

// Ordinary producer regressions: execute only within the separately booked packet.
function quietGitChild(data: Uint8Array): Child {
  return {
    ...fake(data, Promise.resolve({ code: 0, success: true })),
    stderr: new ReadableStream<Uint8Array>({
      start(controller) {
        controller.close();
      },
    }),
  };
}

Deno.test("DOC04 production Git transport retains exact bounded bytes and refuses reused ordinal", async () => {
  const attempt = await Deno.makeTempDir({ prefix: "qcl-doc04-git-" });
  let spawned = 0;
  try {
    const transport = makeDocsGitTransport(() => {
      spawned++;
      return quietGitChild(new Uint8Array([65, 0, 255, 66]));
    });
    const call = {
      executable: "/admitted/git",
      cwd: "/frozen/root",
      args: ["rev-parse", "HEAD"],
      env: { GIT_OPTIONAL_LOCKS: "0" },
      clearEnv: true as const,
      tag: { attempt, ordinal: 1 },
      limits: { wallMs: 100, drainMs: 20, streamBytes: 4, totalBytes: 4 },
    };
    const reply = await transport(call);
    assert(JSON.stringify(Array.from(reply.stdout)) === "[65,0,255,66]");
    assert(reply.result.retention === "acknowledged" && reply.result.reason === null);
    assert(reply.receipt.sha256 === await sha256(await Deno.readFile(reply.receipt.path)));
    assert(
      JSON.stringify(Array.from(await Deno.readFile(`${attempt}/git/1/stdout.log`))) ===
        "[65,0,255,66]",
    );
    await caught(() => transport(call));
    assert(spawned === 1, "fresh receipt directory must be exclusive before spawn");
  } finally {
    await Deno.remove(attempt, { recursive: true });
  }
});
Deno.test("DOC04 production Git transport preserves original overflow receipt without buffered fallback", async () => {
  const attempt = await Deno.makeTempDir({ prefix: "qcl-doc04-git-cap-" });
  try {
    const transport = makeDocsGitTransport(() => quietGitChild(new Uint8Array([1, 2, 3, 4, 5])));
    const reply = await transport({
      executable: "/admitted/git",
      cwd: "/frozen/root",
      args: ["rev-parse", "HEAD"],
      env: {},
      clearEnv: true,
      tag: { attempt, ordinal: 1 },
      limits: { wallMs: 100, drainMs: 20, streamBytes: 4, totalBytes: 4 },
    });
    assert(reply.result.reason === "log_cap" && reply.result.stdout_received_bytes === 5);
    assert(reply.stdout.length === 4 && reply.result.stdout_acknowledged_bytes === 4);
    const retained = JSON.parse(await Deno.readTextFile(reply.receipt.path));
    assert(retained.result.reason === "log_cap" && retained.result.stdout_received_bytes === 5);
  } finally {
    await Deno.remove(attempt, { recursive: true });
  }
});

Deno.test("DOC04 pilot plan rejects executable policy changes and partial journeys", async () => {
  const plan = JSON.parse(
    await Deno.readTextFile(new URL("../ops/docs/pilot-plan.json", import.meta.url)),
  );
  assert(parseDocsPlan(plan).slices.length === 3);
  for (
    const mutation of [
      { ...plan, profile: "default" },
      { ...plan, support_policy: "primary_pages_only" },
      { ...plan, source_inputs: ["../outside"] },
      { ...plan, slices: plan.slices.slice(0, 2) },
      { ...plan, limits: { ...plan.limits, total_bytes: 268435457 } },
      { ...plan, expected_primary_anchors: [] },
    ]
  ) rejects(() => parseDocsPlan(mutation));
});
Deno.test("DOC04 selected source scan rejects executable blocks and retains file hashes", async () => {
  const root = await Deno.makeTempDir({ prefix: "qcl-doc04-source-" });
  try {
    await Deno.writeTextFile(`${root}/index.md`, "# Theory\n```julia\nx = 1\n```\n");
    const initial = await scanDocsSources([root]);
    assert(initial.files.length === 1 && initial.executable_blocks === 0);
    assert(initial.files[0].sha256 === await sha256(await Deno.readFile(`${root}/index.md`)));
    for (const block of ["@example", "@eval", "@setup", "@repl"]) {
      await Deno.writeTextFile(
        `${root}/index.md`,
        `# Theory\n\`\`\`${block} named\nx = 1\n\`\`\`\n`,
      );
      await caught(() => scanDocsSources([root]));
    }
  } finally {
    await Deno.remove(root, { recursive: true });
  }
});

Deno.test("DOC04 build dispatch is one offline sandboxed local Nix builder with fixed producer input", () => {
  const command = docsBuildCommand(
    "/nix/store/pinned/bin/nix",
    "/nix/store/source",
    "/attempts/fresh",
  );
  assert(command.executable === "/nix/store/pinned/bin/nix");
  assert(
    JSON.stringify(command.args) === JSON.stringify([
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
      "/nix/store/source/nix/docs.nix",
      "--argstr",
      "inputsFile",
      "/attempts/fresh/producer-inputs.json",
    ]),
  );
  assert(command.clearEnv && command.cwd === "/nix/store/source");
  rejects(() => docsBuildCommand("julia", "/nix/store/source", "/attempts/fresh"));
  rejects(() =>
    docsBuildCommand("/nix/store/pinned/bin/nix", "/source/../escape", "/attempts/fresh")
  );
});

Deno.test("DOC04 production Git spawn failure retains original error and unknown consumption", async () => {
  const attempt = await Deno.makeTempDir({ prefix: "qcl-doc04-git-spawn-" });
  try {
    const transport = makeDocsGitTransport(() => {
      throw new Error("original spawn denied");
    });
    const error = await caught(() =>
      transport({
        executable: "/admitted/git",
        cwd: "/frozen/root",
        args: ["rev-parse", "HEAD"],
        env: {},
        clearEnv: true,
        tag: { attempt, ordinal: 1 },
        limits: { wallMs: 100, drainMs: 20, streamBytes: 4, totalBytes: 4 },
      })
    );
    assert(String(error).includes("original spawn denied"));
    const retained = JSON.parse(await Deno.readTextFile(`${attempt}/git/1/result.json`));
    assert(retained.result === null && retained.accounting === "unknown");
    assert(retained.error.includes("original spawn denied"));
  } finally {
    await Deno.remove(attempt, { recursive: true });
  }
});

Deno.test("DOC04 private JSON refuses duplicate authority keys and unsupported native markers", () => {
  rejects(() => parseDocsJson('{"unit":{"uid":0,"u\\u0069d":1000}}'));
  rejects(() => parseDocsAdmission({ format: "qcl-negf.docs-admission.v1", status: "ready" }));
  assert(
    JSON.stringify(parseDocsJson('{"one":{"uid":0},"two":{"uid":1}}')) ===
      '{"one":{"uid":0},"two":{"uid":1}}',
  );
});
Deno.test("DOC04 own unit and actual cgroup caps are required before build", () => {
  const admission = {
    unit: {
      name: "qcl-docs-fixture.service",
      boot_id: "boot",
      control_group: "/system.slice/qcl-docs-fixture.service",
    },
  } as Parameters<typeof checkDocsCgroup>[0];
  const actual = {
    uid: 0,
    pid: 42,
    boot_id: "boot\n",
    control_group: admission.unit.control_group,
    unit: {
      Id: admission.unit.name,
      ActiveState: "active",
      SubState: "running",
      MainPID: "42",
      User: "root",
      ControlGroup: admission.unit.control_group,
      KillMode: "control-group",
      RuntimeMaxUSec: "30min",
    },
    controls: {
      "cpu.max": "400000 100000",
      "memory.max": "4294967296",
      "memory.swap.max": "0",
      "pids.max": "128",
      "memory.current": "123",
      "memory.events": "oom 0",
      "cpu.stat": "usage_usec 12",
    },
  };
  assert(checkDocsCgroup(admission, actual).uid === 0);
  for (
    const change of [
      { uid: 1000 },
      { control_group: "/system.slice/other.service" },
      { unit: { ...actual.unit, MainPID: "77" } },
      { unit: { ...actual.unit, KillMode: "process" } },
      { controls: { ...actual.controls, "cpu.max": "max 100000" } },
      { controls: { ...actual.controls, "memory.max": "4294967297" } },
      { controls: { ...actual.controls, "memory.swap.max": "1" } },
      { controls: { ...actual.controls, "pids.max": "max" } },
    ]
  ) rejects(() => checkDocsCgroup(admission, { ...actual, ...change }));
});

Deno.test("DOC04 dispatch fake captures one fixed command and excludes private admission bytes", async () => {
  const attempt = await Deno.makeTempDir({ prefix: "qcl-doc04-dispatch-" });
  try {
    const admission = {
      inputs: { selected_public: "kept" },
      tools: { nix: { executable: "/nix/store/pinned/bin/nix" } },
      unit: { private_unit: "not-published" },
      resource_readback: { private_host: "not-published" },
    } as unknown as Parameters<typeof dispatchDocsBuild>[0]["admission"];
    Object.assign(admission.inputs, { source_root: "/nix/store/source" });
    let calls = 0;
    await dispatchDocsBuild({
      admission,
      attempt,
      wallMs: 100,
      invoke: (call) =>
        immediatePromise(() => {
          calls++;
          assert(
            JSON.stringify(call.args) ===
              JSON.stringify(
                docsBuildCommand(
                  admission.tools.nix.executable,
                  admission.inputs.source_root,
                  attempt,
                ).args,
              ),
          );
          return oneByteReply();
        }),
    });
    const projected = await Deno.readTextFile(`${attempt}/producer-inputs.json`);
    assert(
      projected.includes("selected_public") && !projected.includes("not-published") &&
        !projected.includes("resource_readback"),
    );
    await caught(() =>
      dispatchDocsBuild({
        admission,
        attempt,
        wallMs: 100,
        invoke: () => {
          calls++;
          return Promise.resolve(oneByteReply());
        },
      })
    );
    assert(calls === 1, "reused sanitized input must refuse before another command");
  } finally {
    await Deno.remove(attempt, { recursive: true });
  }
});
Deno.test("DOC04 Nix output permits one immutable output only", () => {
  const path = "/nix/store/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-docs";
  assert(
    parseDocsNixOutput(new TextEncoder().encode(JSON.stringify([{ outputs: { out: path } }]))) ===
      path,
  );
  for (
    const value of [[], [{ outputs: { out: path } }, { outputs: { out: path } }], [{
      outputs: { out: path, other: path },
    }], [{ outputs: { out: "/mutable/output" } }]]
  ) {
    rejects(() => parseDocsNixOutput(new TextEncoder().encode(JSON.stringify(value))));
  }
});

// HIGH regression: production tree volumes, not the tiny binary transport fixture.
import { sourceGraph } from "../ops/git.ts";
Deno.test("DOC04 production Git limits admit actual root tree and full seven graph lifecycle", async () => {
  const root = "/frozen/production-graph";
  const components = [
    ["QCLNEGF.jl", 20711],
    ["QCLNEGFRunner.jl", 27420],
    ["qcl-negf-aiida", 2765],
    ["qcl-negf-contracts", 4273],
    ["qcl-negf-platform", 16035],
    ["qcl-negf-portal", 3016],
    ["qcl-negf-research", 3056],
    ["qcl-negf-results", 5542],
  ] as const;
  const revision = "a".repeat(40), blob = "b".repeat(40);
  const paddedTree = (initial: string, size: number) => {
    const prefix = `100644 blob ${blob}\t`;
    let result = initial, index = 0;
    while (size - result.length >= prefix.length + 256) {
      result += `${prefix}file-${String(index++).padStart(6, "0")}.md\0`;
    }
    result += prefix + "q".repeat(size - result.length - prefix.length - 1) + "\0";
    assert(result.length === size);
    return result;
  };
  const rootTree = paddedTree(
    components.map(([name]) => `160000 commit ${revision}\tcomponents/${name}\0`).join(""),
    231295,
  );
  const trees = new Map(
    components.map(([name, size]) => [root + "/components/" + name, paddedTree("", size)]),
  );
  let rootTrees = 0, commands = 0, received = 0;
  const readGit = makeDocsGitReader({
    root,
    attempt: "/attempts/production-graph",
    gitExecutable: "/admitted/git",
    limits: productionDocsGitLimits,
    invoke: (call) =>
      immediatePromise(() => {
        commands++;
        const args = call.args.slice(8);
        let text: string;
        if (args[0] === "rev-parse") text = revision;
        else if (args[0] === "status") text = "";
        else if (args[0] === "ls-tree") {
          if (call.cwd === root) {
            rootTrees++;
            text = rootTree;
          } else {
            text = trees.get(call.cwd)!;
            assert(typeof text === "string");
          }
        } else if (args[0] === "config" && args[3] === "--get-regexp") {
          text = components.map(([name], index) => `submodule.c${index}.path components/${name}`)
            .join("\n");
        } else if (args[0] === "config" && args[3] === "--get") {
          const match = /^submodule.c(\d+).url$/.exec(args[4]);
          assert(match);
          text = `https://github.com/owner/${components[Number(match[1])][0]}.git`;
        } else throw new Error(`unexpected production graph fixture argv ${JSON.stringify(args)}`);
        const stdout = new TextEncoder().encode(text), reply = oneByteReply();
        received += stdout.length;
        return {
          ...reply,
          stdout,
          result: {
            ...reply.result,
            stdout_received_bytes: stdout.length,
            stdout_attempted_bytes: stdout.length,
            stdout_acknowledged_bytes: stdout.length,
          },
        };
      }),
  });
  for (let observation = 0; observation < 7; observation++) {
    const graph = await sourceGraph(root, true, readGit);
    assert(graph.components.length === 8 && graph.revision === revision);
  }
  assert(rootTrees === 7 && commands === 252);
  assert(received >= 2198791 && received < productionDocsGitLimits.maxTotalBytes);
});
Deno.test("DOC04 production Git tree overflow retains failure under finite production caps", async () => {
  const attempt = await Deno.makeTempDir({ prefix: "qcl-doc04-production-overflow-" });
  try {
    let spawns = 0;
    const transport = makeDocsGitTransport(() => {
      spawns++;
      return quietGitChild(new Uint8Array(productionDocsGitLimits.streamBytes + 1).fill(65));
    });
    const reader = makeDocsGitReader({
      root: identityRoot,
      attempt,
      gitExecutable: "/admitted/git",
      limits: productionDocsGitLimits,
      invoke: transport,
    });
    const error = await caught(() => reader(identityRoot, ["ls-tree", "-rz", "HEAD"]));
    assert(error instanceof GitObservationError && error.code === "log_cap" && spawns === 1);
    const retained = JSON.parse(await Deno.readTextFile(`${attempt}/git/1/result.json`));
    assert(retained.result.stdout_received_bytes === productionDocsGitLimits.streamBytes + 1);
    assert(retained.result.stdout_acknowledged_bytes === productionDocsGitLimits.streamBytes);
  } finally {
    await Deno.remove(attempt, { recursive: true });
  }
});
function completeAdmissionFixture(created_epoch: unknown) {
  const store = "/nix/store/" + "a".repeat(32) + "-fixture";
  const tool = {
    store_path: store,
    executable: store + "/bin/tool",
    deriver: store + ".drv",
    nar_hash: "sha256:" + "a".repeat(52),
    version: "1.0",
  };
  const file = (path: string) => ({ path, sha256: "b".repeat(64) });
  return {
    format: "qcl-negf.docs-admission.v1",
    created_epoch,
    attempt_directory: "/attempts/fresh",
    repository_root: "/frozen/root",
    plan_sha256: "b".repeat(64),
    unit: {
      name: "qcl-docs-fresh.service",
      uid: 0,
      boot_id: "a".repeat(36),
      control_group: "/system.slice/qcl-docs-fresh.service",
    },
    resource_readback: file("/protected/resource.json"),
    tools: { nix: tool, git: tool, deno: tool, python: tool, node: tool, julia: tool },
    inputs: {
      source_root: store,
      source_graph: file(store + "/graph.json"),
      plan: file(store + "/plan.json"),
      project: file(store + "/julia/Project.toml"),
      manifest: file(store + "/julia/Manifest.toml"),
      prepared_depot: { store_path: store, metadata: file(store + "/depot.json") },
      assets_lock: file(store + "/ops/docs/assets.lock.json"),
      asset_inputs: file(store + "/assets.json"),
      review_inputs: file(store + "/reviews.json"),
      tools: { python: tool, node: tool, julia: tool, git: tool },
    },
  };
}
Deno.test("DOC04 fractional admission epoch matches numeric contract and retains freshness refusal", () => {
  const epoch = 1792862662.9105856;
  const admission = parseDocsAdmission(completeAdmissionFixture(epoch));
  assert(admission.created_epoch === epoch);
  checkDocsAdmissionFreshness(admission.created_epoch, epoch + 0.125);
  checkDocsAdmissionFreshness(admission.created_epoch, epoch + 300);
  for (const invalid of [true, false, "1792862662.9105856", NaN, Infinity, -Infinity]) {
    rejects(() => parseDocsAdmission(completeAdmissionFixture(invalid)));
  }
  rejects(() => checkDocsAdmissionFreshness(admission.created_epoch, epoch - 0.125));
  rejects(() => checkDocsAdmissionFreshness(admission.created_epoch, epoch + 300.125));
});

function toolIdentityFixture() {
  const tool = { ...completeAdmissionFixture(1).tools.python };
  const calls: { executable: string; argv: string[] }[] = [];
  const paths: string[] = [];
  const state = {
    actual: tool.executable,
    version: "tool 1.0 full version\n",
    hash: tool.nar_hash + "\n",
    deriver: tool.deriver + "\n",
    isFile: true,
    mode: 0o555 as number | null,
    failure: null as Partial<GitReply["result"]> | null,
    buildCalls: 0,
  };
  const nixStore = tool.store_path + "/bin/nix-store";
  const io = {
    ancestors: (path: string, directory: boolean) => {
      assert(directory && path === tool.store_path);
      paths.push(path);
      return Promise.resolve();
    },
    realPath: (path: string) => {
      assert(path === tool.executable);
      paths.push(path);
      return Promise.resolve(state.actual);
    },
    stat: (path: string) => {
      assert(path === state.actual);
      paths.push(path);
      return Promise.resolve({ isFile: state.isFile, mode: state.mode });
    },
    command: (executable: string, argv: string[]) => {
      calls.push({ executable, argv });
      const versionCall = argv.length === 1 && argv[0] === "--version";
      assert(executable === (versionCall ? tool.executable : nixStore));
      if (!versionCall) {
        assert(JSON.stringify(argv.slice(0, 3)) === '["--store","local","--query"]');
        assert(argv.length === 5 && argv[4] === tool.store_path);
        assert(argv[3] === "--hash" || argv[3] === "--deriver");
      }
      const text = versionCall ? state.version : argv[3] === "--hash" ? state.hash : state.deriver;
      const reply = oneByteReply();
      reply.stdout = new TextEncoder().encode(text);
      if (!versionCall && argv[3] === "--hash" && state.failure) {
        reply.result = { ...reply.result, ...state.failure };
      }
      return Promise.resolve(reply);
    },
  };
  return {
    tool,
    state,
    calls,
    paths,
    async prebuild(expected: DocsTool = tool) {
      const result = await observeDocsTool("python", expected, nixStore, io);
      // A failed tool gate must never reach even this inert builder stand-in.
      state.buildCalls++;
      return result;
    },
  };
}
Deno.test("DOC04 Tool identity accepts absent deriver metadata with explicit provenance limit", async () => {
  for (const expectedNull of [true, false]) {
    for (const observedKnown of [true, false]) {
      if (!expectedNull && !observedKnown) continue;
      const f = toolIdentityFixture();
      f.state.deriver = observedKnown ? f.tool.deriver + "\n" : "unknown-deriver\n";
      const result = await f.prebuild({ ...f.tool, deriver: expectedNull ? null : f.tool.deriver });
      assert(result.deriver === (observedKnown ? f.tool.deriver : null));
      assert(result.deriver_binding === (expectedNull ? "not_asserted" : "matched"));
      assert(result.derivation_provenance === "derivation provenance not established");
      assert(result.store_path === f.tool.store_path && result.nar_hash === f.tool.nar_hash);
      assert(result.version === "tool 1.0 full version");
      assert(!f.paths.includes(f.tool.deriver), "physical .drv must never be queried");
      assert(f.calls.length === 3 && f.calls.filter((c) => c.argv[3] === "--hash").length === 1);
      assert(f.state.buildCalls === 1);
    }
  }
});
Deno.test("DOC04 Tool identity strictly refuses malformed admission and producer projection", () => {
  for (
    const value of [
      null,
      "",
      "sha256:" + "a".repeat(51),
      "sha256:" + "e".repeat(52),
      "sha512:" + "a".repeat(52),
      "sha256:" + "a".repeat(52) + "\n",
      false,
    ]
  ) {
    const input = completeAdmissionFixture(1);
    Object.assign(input.tools.python, { nar_hash: value });
    rejects(() => parseDocsAdmission(input));
  }
  for (
    const value of [
      "unknown-deriver",
      "null",
      false,
      "",
      "/tmp/a.drv",
      "/nix/store/" + "a".repeat(32) + "-a.drv/child",
    ]
  ) {
    const input = completeAdmissionFixture(1);
    Object.assign(input.tools.python, { deriver: value });
    rejects(() => parseDocsAdmission(input));
  }
  const old = completeAdmissionFixture(1);
  Reflect.deleteProperty(old.tools.python, "nar_hash");
  rejects(() => parseDocsAdmission(old));
  for (const field of ["nar_hash", "deriver"] as const) {
    const input = completeAdmissionFixture(1);
    Object.assign(input.inputs.tools, {
      python: {
        ...input.inputs.tools.python,
        ...(field === "nar_hash" ? { nar_hash: "sha256:" + "b".repeat(52) } : { deriver: null }),
      },
    });
    try {
      parseDocsAdmission(input);
      throw new Error("expected producer_tool_mismatch");
    } catch (error) {
      assert(error instanceof Error && error.message === "producer_tool_mismatch");
    }
  }
  const nullable = completeAdmissionFixture(1);
  Object.assign(nullable.tools.python, { deriver: null });
  assert(parseDocsAdmission(nullable).tools.python.deriver === null);
});
Deno.test("DOC04 Tool identity failures block before build with fixed finite queries", async () => {
  const cases: [string, (f: ReturnType<typeof toolIdentityFixture>) => void][] = [
    ["tool_nar_hash_mismatch", (f) => f.state.hash = "sha256:" + "b".repeat(52) + "\n"],
    ["tool_deriver_mismatch", (f) => f.state.deriver = "unknown-deriver\n"],
    ["tool_deriver_mismatch", (f) => f.state.deriver = f.tool.store_path + "-other.drv\n"],
    ["tool_path_mismatch", (f) => f.state.actual = f.tool.store_path + "/bin/other"],
    ["tool_path_mismatch", (f) => f.state.actual = "/tmp/escaped"],
    ["tool_path_mismatch", (f) => f.state.actual = f.tool.store_path + "-other/bin/tool"],
    ["tool_not_executable", (f) => f.state.mode = 0o444],
    ["tool_not_executable", (f) => f.state.isFile = false],
    ["tool_version_mismatch", (f) => f.state.version = "tool 2.0"],
    ["invalid_tool_nar_hash", (f) => f.state.hash += f.state.hash],
    ["invalid_tool_nar_hash", (f) => f.state.hash = " " + f.state.hash],
    ["invalid_tool_nar_hash", (f) => f.state.hash += "\n"],
    ["invalid_tool_nar_hash", (f) => f.state.hash = ""],
    ["noncanonical_absolute_path", (f) => f.state.deriver = "unknown-deriver\nextra\n"],
    ["command_failed", (f) => f.state.failure = { exit: { code: 1, success: false } }],
    ["command_failed", (f) => f.state.failure = { reason: "log_cap" }],
    ["command_failed", (f) => f.state.failure = { drain: "incomplete" }],
    ["command_failed", (f) => f.state.failure = { retention: "failed_unknown_partial" }],
    ["command_failed", (f) => f.state.failure = { errors: ["retained failure"] }],
  ];
  for (const [expected, change] of cases) {
    const f = toolIdentityFixture();
    change(f);
    const error = await caught(() => f.prebuild());
    assert(error instanceof Error && error.message.startsWith(expected), `${expected}: ${error}`);
    assert(f.state.buildCalls === 0 && f.calls.length <= 3);
  }
});
