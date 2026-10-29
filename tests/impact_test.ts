import {
  checkCommands,
  collectCommittedChanges,
  parseImpactOptions,
  planImpact,
  preparationCommands,
  selectedPlan,
} from "../ops/impact.ts";
import type { ChangedPath, ImpactGroup } from "../ops/impact.ts";
import type { GitReader, SourceGraph } from "../ops/git.ts";
import type { Command } from "../ops/process.ts";

function ok(value: unknown, message: string): asserts value {
  if (!value) throw Error(message);
}
function equal(a: unknown, b: unknown) {
  ok(JSON.stringify(a) === JSON.stringify(b), `${JSON.stringify(a)} != ${JSON.stringify(b)}`);
}
async function refuses(f: () => unknown | Promise<unknown>) {
  let rejected = false;
  try {
    await f();
  } catch {
    rejected = true;
  }
  ok(rejected, "unsafe input accepted");
}
const owner = (n: string) => `components/qcl-negf-${n}`;
const change = (
  path: string,
  repo = "root",
  oldMode = "100644",
  newMode = "100644",
): ChangedPath => ({ owner: repo, path, oldMode, newMode });
const context = { root: "/fixture", julia: "/prepared/julia" };
const native = (commands: Command[]) =>
  commands.some((c) =>
    c.executable === "/prepared/julia" || ["uv", "npm", "nix", "tofu"].includes(c.executable) ||
    c.args.some((a) => ["bootstrap", "docs", "init"].includes(a))
  );

Deno.test("prose docs and instructions select D only with explicit links review and no prepare", () => {
  for (
    const c of [
      change("docs/guide with space.md"),
      change("AGENTS.md"),
      change("docs/x.md", owner("results")),
    ]
  ) {
    const p = planImpact([c]);
    equal(p.groups, ["docs"]);
    ok(
      p.nativeGates.some((g) => g.includes("links") && g.includes("anchors")),
      "missing D source-review gate",
    );
    equal(preparationCommands(p, context), []);
    const commands = checkCommands(p, context);
    ok(
      !native(commands) && commands.some((x) => x.args.includes("--check")),
      "D invoked native work",
    );
    ok(
      commands.some((x) =>
        x.args.includes(`/fixture/${c.owner === "root" ? "" : c.owner + "/"}${c.path}`)
      ),
      "lost exact whitespace pathname",
    );
  }
});
Deno.test("wheel README metadata is owner-native not blanket prose or unrelated Julia", () => {
  for (const n of ["contracts", "results", "aiida", "portal"]) {
    const p = planImpact([change("README.md", owner(n))]);
    ok(
      p.groups.includes(n as ImpactGroup) && !p.groups.includes("core") &&
        !p.groups.includes("runner"),
      "README hidden wheel impact or Julia overreach",
    );
    ok(p.nativeGates.some((g) => g.includes("wheel")), "wheel prerequisite not declared");
  }
});
Deno.test("Python source closure keeps consumers without unrelated Julia and preparation honest", () => {
  const p = planImpact([change("src/qcl_negf_results/reader.py", owner("results"))]);
  equal(p.groups, ["aiida", "portal", "results"]);
  const checks = checkCommands(p, context), prep = preparationCommands(p, context);
  ok(!checks.some((c) => c.executable === "/prepared/julia"), "Python route invoked Julia");
  ok(
    checks.filter((c) => c.executable === "uv").every((c) =>
      c.args.includes("--locked") && c.args.includes("--no-sync")
    ),
    "pytest hid sync",
  );
  ok(prep.some((c) => c.executable === "uv" && c.args[0] === "sync"), "Python environment missing");
  ok(
    prep.some((c) => c.executable === "npm" && c.args[0] === "ci"),
    "Portal wheel prerequisite hidden",
  );
  ok(!prep.some((c) => c.executable === "/prepared/julia"), "Python prepare invoked Julia");
});
Deno.test("Core and semantic Contracts retain whole Julia oracle files and Results integration", () => {
  for (
    const c of [
      change("src/reference.jl", "components/QCLNEGF.jl"),
      change("src/schema.py", owner("contracts")),
    ]
  ) {
    const p = planImpact([c]), commands = checkCommands(p, context);
    for (
      const g of ["core", "runner", "julia-integration", "results", "aiida", "portal"] as const
    ) ok(p.groups.includes(g), `missing ${g}`);
    for (const n of ["QCLNEGF.jl", "QCLNEGFRunner.jl"]) {
      ok(
        commands.some((x) =>
          x.args.includes(`/fixture/components/${n}/test/runtests.jl`) &&
          x.args.includes("--check-bounds=yes")
        ),
        "oracle test dropped",
      );
    }
    ok(
      commands.some((x) => x.args.includes("components/qcl-negf-results/integration")),
      "integration dropped",
    );
    ok(!commands.some((x) => x.args.includes("docs")), "source change built docs implicitly");
  }
});
Deno.test("executable docs/config/native metadata differ from prose; unknown requires full", () => {
  for (
    const c of [
      change("docs/make.jl", "components/QCLNEGF.jl"),
      change("LICENSE", owner("results")),
      change("config/studies/a.yaml", owner("research")),
      change("tofu/a.tf", owner("platform")),
    ]
  ) {
    ok(planImpact([c]).groups.some((g) => g !== "docs"), "executable/native path treated as prose");
  }
  for (
    const p of [
      planImpact([change("surprise.bin")]),
      planImpact([], ["missing objects"]),
      planImpact([change("docs/a.md", "root", "120000", "120000")]),
    ]
  ) {
    ok(
      p.unknowns.length > 0 && p.groups.includes("docs-build") &&
        p.groups.includes("julia-integration"),
      "unknown became empty pass",
    );
    equal(p.scientificStage, "not_requested");
  }
});
Deno.test("infra checks never install providers; full retains both docs; manual parser stays strict", async () => {
  const p = selectedPlan([], parseImpactOptions(["--infra"]));
  const checks = checkCommands(p, context), prep = preparationCommands(p, context);
  ok(
    !checks.some((c) => c.args.includes("init") || c.args.includes("instantiate")),
    "check installs providers",
  );
  equal(prep.filter((c) => c.executable === "tofu").length, 2);
  ok(
    prep.filter((c) => c.executable === "tofu").every((c) => c.args.includes("-lockfile=readonly")),
    "provider lock mutation",
  );
  equal(
    checkCommands(selectedPlan([], parseImpactOptions([])), context).filter((c) =>
      c.args.includes("docs")
    ).length,
    2,
  );
  for (
    const flags of [["--base", "x"], ["--head", "x"], ["--base", "--evil", "--head", "HEAD"], [
      "--python",
      "--python",
    ], ["--unknown"]]
  ) await refuses(() => parseImpactOptions(flags));
  const flags = parseImpactOptions(["--base", "HEAD~1", "--head", "HEAD", "--python"]);
  ok(flags.base === "HEAD~1" && flags.head === "HEAD", "range lost");
  const manual = selectedPlan([], parseImpactOptions(["--python"]));
  ok(!manual.groups.includes("core") && manual.groups.includes("research"), "manual scope changed");
});
Deno.test("planner is deterministic, rejects traversal and preserves delete/add modes", async () => {
  const changes = [change("src/a.py", owner("aiida")), change("src/z.py", owner("results"))];
  equal(planImpact(changes), planImpact([...changes].reverse()));
  equal(planImpact([change("docs/deleted.md", "root", "100644", "000000")]).groups, ["docs"]);
  ok(
    checkCommands(planImpact([change("docs/deleted.md", "root", "100644", "000000")]), context)
      .length === 0,
    "fmt deleted file",
  );
  for (const path of ["../x", "/etc/passwd", "a/../b", "a//b", "a\\b", "a\u0000b", "a/./b"]) {
    await refuses(() => planImpact([change(path)]));
  }
});

const A = "a".repeat(40), B = "b".repeat(40), C = "c".repeat(40), D = "d".repeat(40);
const raw = (path: string, old = "100644", next = "100644", before = A, after = B) =>
  `:${old} ${next} ${before} ${after} M\0${path}\0`;
function gitFixture(
  rootRaw: string,
  componentRaw = raw("src/a.py"),
  missing = false,
  configured = owner("results"),
) {
  const calls: { root: string; args: readonly string[] }[] = [];
  const read: GitReader = (root, args) => {
    calls.push({ root, args: [...args] });
    if (args[0] === "rev-parse") {
      if (missing && root !== "/fixture") throw Error("missing object");
      return Promise.resolve(
        args.at(-1)!.startsWith("before")
          ? A
          : args.at(-1)!.startsWith("after")
          ? B
          : args.at(-1)!.replace("^{commit}", ""),
      );
    }
    if (args[0] === "config") return Promise.resolve(`submodule.results.path\n${configured}\0`);
    if (args[0] === "diff") return Promise.resolve(root === "/fixture" ? rootRaw : componentRaw);
    throw Error("unexpected reader operation");
  };
  return { read, calls };
}
Deno.test("raw NUL collector resolves commits, reads committed config, expands gitlink objects only", async () => {
  const { read, calls } = gitFixture(
    raw(owner("results"), "160000", "160000", C, D),
    raw("docs/space and\ttab.md"),
  );
  const c = await collectCommittedChanges("/fixture", "before", "after", read);
  equal([c.base, c.head], [A, B]);
  equal(c.changes, [change("docs/space and\ttab.md", owner("results"))]);
  equal(c.unknowns, []);
  ok(
    calls.some((c) => c.args.includes("--blob") && c.args.includes(`${B}:.gitmodules`)),
    "working config became composition authority",
  );
  ok(
    calls.filter((c) => c.args[0] === "diff").every((c) =>
      c.args.includes("--raw") && c.args.includes("-z") && c.args.includes("--no-ext-diff") &&
      c.args.includes("--no-textconv") && c.args.includes("--no-renames")
    ),
    "raw safety flags missing",
  );
  ok(
    !calls.some((c) =>
      c.args.some((a) => ["fetch", "checkout", "update-index", "add"].includes(a))
    ),
    "collector mutated Git",
  );
});
Deno.test("missing/new/deleted/unconfigured gitlinks remain explicit full uncertainty", async () => {
  for (
    const f of [
      gitFixture(raw(owner("results"), "160000", "160000", C, D), "", true),
      gitFixture(raw(owner("results"), "000000", "160000", "0".repeat(40), D)),
      gitFixture(raw(owner("results"), "160000", "000000", C, "0".repeat(40))),
      gitFixture(raw("components/foreign", "160000", "160000", C, D)),
    ]
  ) {
    const c = await collectCommittedChanges("/fixture", "before", "after", f.read);
    ok(
      c.unknowns.length > 0 &&
        planImpact(c.changes, c.unknowns).groups.includes("julia-integration"),
      "uncertain gitlink became no-op",
    );
  }
});
Deno.test("raw collector rejects unsafe refs and malformed records before interpreting data", async () => {
  for (const ref of ["--all", "", "HEAD\nother", "x y"]) {
    const f = gitFixture("");
    await refuses(() => collectCommittedChanges("/fixture", ref, "after", f.read));
    equal(f.calls.length, 0);
  }
  for (
    const text of [
      "not raw",
      raw("../escape"),
      raw("x").slice(0, -1),
      `:100644 100644 ${A} ${B} R100\0old\0new\0`,
    ]
  ) {
    const f = gitFixture(text);
    await refuses(() => collectCommittedChanges("/fixture", "before", "after", f.read));
  }
  const f = gitFixture(
    raw("docs/old.md", "100644", "000000") + raw("docs/new.md", "000000", "100644"),
  );
  equal((await collectCommittedChanges("/fixture", "before", "after", f.read)).changes.length, 2);
});
Deno.test("CI import guard and executor preserve clean selected HEAD and before/after graph checks", async () => {
  const source = await Deno.readTextFile(new URL("../ops/ci.ts", import.meta.url));
  ok(source.includes("if (import.meta.main)"), "ci import would execute checks");
  const { runChecks } = await import("../ops/ci.ts");
  const graph: SourceGraph = { format: "qcl-negf.git-graph.v1", revision: B, components: [] };
  const plan = { ...planImpact([change("docs/x.md")]), base: A, head: B };
  const commands: Command[] = [];
  let reads = 0;
  await runChecks(plan, context, async (c: Command) => {
    commands.push(c);
    return await Promise.resolve("");
  }, async () => {
    reads++;
    return await Promise.resolve(graph);
  });
  equal(reads, 2);
  ok(commands.length > 0 && !native(commands), "D CI escaped selection");
  await refuses(() =>
    runChecks(
      plan,
      context,
      () => Promise.resolve(""),
      () => Promise.resolve({ ...graph, revision: A }),
    )
  );
  let dispatch = 0;
  await refuses(() =>
    runChecks(plan, context, async () => {
      dispatch++;
      return await Promise.resolve("");
    }, async () => {
      return await Promise.reject(Error("dirty graph"));
    })
  );
  equal(dispatch, 0);
  reads = 0;
  await refuses(() =>
    runChecks(
      plan,
      context,
      () => Promise.resolve(""),
      () => Promise.resolve({ ...graph, revision: ++reads === 1 ? B : A }),
    )
  );
});

Deno.test("prepare shares exact planner and graph guard but never runs checks implicitly", async () => {
  const text = await Deno.readTextFile(new URL("../ops/environment.ts", import.meta.url));
  ok(
    text.includes("export async function runPreparation"),
    "prepare has no shared selective entrypoint",
  );
  const { runPreparation } = await import("../ops/environment.ts");
  const graph: SourceGraph = { format: "qcl-negf.git-graph.v1", revision: B, components: [] };
  const commands: Command[] = [];
  let reads = 0;
  const p = { ...planImpact([change("docs/x.md")]), base: A, head: B };
  await runPreparation(p, context, async (c) => {
    commands.push(c);
    return await Promise.resolve("");
  }, async () => {
    reads++;
    return await Promise.resolve(graph);
  });
  equal(commands, []);
  equal(reads, 2);
  const py = planImpact([change("src/a.py", owner("results"))]);
  await runPreparation(py, context, async (c) => {
    commands.push(c);
    return await Promise.resolve("");
  }, () => Promise.resolve(graph));
  equal(commands, preparationCommands(py, context));
  ok(
    !commands.some((c) =>
      c.args.includes("pytest") || c.args.includes("validate") || c.executable === "/prepared/julia"
    ),
    "prepare invokes checks/Julia for Python",
  );
});
Deno.test("malformed unsafe component object diff cannot hide behind missing-object uncertainty", async () => {
  const f = gitFixture(raw(owner("results"), "160000", "160000", C, D), raw("../escape"));
  await refuses(() => collectCommittedChanges("/fixture", "before", "after", f.read));
});

Deno.test("instruction skill prose remains D and prototype-like owners remain explicit unknown", () => {
  equal(planImpact([change(".agents/skills/qcl/SKILL.md")]).groups, ["docs"]);
});
Deno.test("prototype-like owners remain explicit unknown", () => {
  const unknown = planImpact([change("docs/a.md", "toString")]);
  ok(
    unknown.unknowns.length > 0 && unknown.groups.includes("julia-integration"),
    "unknown owner inherited an object property",
  );
});
Deno.test("Git diff cannot inherit a local configuration hiding all gitlink changes", async () => {
  const f = gitFixture(raw(owner("results"), "160000", "160000", C, D));
  await collectCommittedChanges("/fixture", "before", "after", f.read);
  ok(
    f.calls.filter((c) => c.args[0] === "diff").every((c) =>
      c.args.includes("--ignore-submodules=none")
    ),
    "gitlink changes may be hidden by local Git config",
  );
});
Deno.test("source graph guard retains its own before evidence across async dispatch", async () => {
  const { runChecks } = await import("../ops/ci.ts");
  const graph: SourceGraph = { format: "qcl-negf.git-graph.v1", revision: B, components: [] };
  const plan = { ...planImpact([change("docs/x.md")]), base: A, head: B };
  await refuses(() =>
    runChecks(plan, context, async () => {
      graph.revision = A;
      return await Promise.resolve("");
    }, () => Promise.resolve(graph))
  );
});

Deno.test("known Root assembly is full recommendation while genuinely unclassified paths stay uncertain", () => {
  const p = planImpact([change("ops/ci.ts"), change("flake.lock")]);
  ok(
    p.groups.includes("docs-build") && p.groups.includes("root"),
    "Root assembly lost full closure",
  );
  equal(p.unknowns, []);
  ok(planImpact([change("surprise.bin")]).unknowns.length > 0, "unknown Root path hidden");
});
Deno.test("manual workflow uses planner/check/prepare flags without weakening runner trust", async () => {
  const text = await Deno.readTextFile(new URL("../.github/workflows/ci.yml", import.meta.url));
  for (const task of ["impact", "prepare", "test"]) {
    ok(
      text.includes(`deno task ${task} --base "$IMPACT_BASE" --head HEAD`) &&
        text.includes(`deno task ${task} --full`),
      "workflow duplicated or bypassed shared selection",
    );
  }
  for (
    const invariant of [
      "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803",
      "persist-credentials: false",
      "cancel-in-progress: false",
      "options: [full, changed, runner-smoke]",
      "github-runner-qcl-negf",
      "sudo -n true",
    ]
  ) ok(text.includes(invariant), "workflow trust/smoke boundary changed");
  ok(
    !text.includes("pull_request:") &&
      !text.includes("deno task --cwd components/QCLNEGFRunner.jl bootstrap"),
    "automatic trigger or duplicate bootstrap outside registry",
  );
});

Deno.test("valid Markdown names remain D through raw/gitlink collection, dispatch and prepare", async (t) => {
  const { runChecks } = await import("../ops/ci.ts");
  const { runPreparation } = await import("../ops/environment.ts");
  const separators = [["space", " "], ["tab", "\t"], ["LF", "\n"], ["CR", "\r"], [
    "line-separator",
    "\u2028",
  ], ["paragraph-separator", "\u2029"]] as const;
  for (const repo of ["root", owner("results")]) {
    for (const prefix of ["docs/", ".agents/skills/qcl/"]) {
      for (const [label, separator] of separators) {
        await t.step(`${repo}:${prefix}:${label}`, async () => {
          const path = prefix + "only" + separator + "prose.md";
          const fixture = repo === "root"
            ? gitFixture(raw(path))
            : gitFixture(raw(repo, "160000", "160000", C, D), raw(path));
          const collected = await collectCommittedChanges(
            "/fixture",
            "before",
            "after",
            fixture.read,
          );
          equal(collected.changes, [change(path, repo)]);
          equal(collected.unknowns, []);
          const p = { ...planImpact(collected.changes, collected.unknowns), base: A, head: B };
          equal(p.groups, ["docs"]);
          equal(preparationCommands(p, context), []);
          const graph: SourceGraph = {
            format: "qcl-negf.git-graph.v1",
            revision: B,
            components: [],
          };
          const dispatched: Command[] = [];
          let reads = 0;
          const execute = (command: Command) => {
            dispatched.push(command);
            return Promise.resolve("");
          };
          const readGraph = () => {
            reads++;
            return Promise.resolve(graph);
          };
          await runChecks(p, context, execute, readGraph);
          equal(dispatched, [{
            executable: "deno",
            args: ["fmt", "--check", `/fixture/${repo === "root" ? "" : repo + "/"}${path}`],
            cwd: "/fixture",
          }]);
          ok(!native(dispatched), "prose path dispatched package/Julia/infra work");
          await runPreparation(p, context, execute, readGraph);
          equal(dispatched.length, 1);
          equal(reads, 4);
        });
      }
    }
  }
});
