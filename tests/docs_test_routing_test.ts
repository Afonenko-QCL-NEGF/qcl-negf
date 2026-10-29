// deno-lint-ignore-file require-await -- Inert async DI fakes match the production adapter signatures.
import {
  parseUnitArgs,
  parseUnitReport,
  prepareStaticSeeds,
  runUnits,
  unitCommands,
  unitPaths,
} from "../ops/docs_tests.ts";
import { checkCommands, planImpact, preparationCommands } from "../ops/impact.ts";
import { type Command, type RetainedResult } from "../ops/process.ts";
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
const tools = { python: "/explicit/python", node: "/explicit/node", deno: "/explicit/deno" };
function result(text: string, stderr = ""): RetainedResult {
  const stdout = new TextEncoder().encode(text), err = new TextEncoder().encode(stderr);
  return {
    stdout,
    stderr: err,
    receipt: { path: "/tmp/r", sha256: "a".repeat(64) },
    result: {
      reason: null,
      exit: { code: 0, success: true },
      drain: "complete",
      errors: [],
      stdout_received_bytes: stdout.length,
      stdout_attempted_bytes: stdout.length,
      stdout_acknowledged_bytes: stdout.length,
      stderr_received_bytes: err.length,
      stderr_attempted_bytes: err.length,
      stderr_acknowledged_bytes: err.length,
      retention: "acknowledged",
      process_tree_terminated: null,
      resource_measurements: null,
    },
  };
}
Deno.test("docs unit inputs are exact asset map with explicit fallback only", async () => {
  ok(parseUnitArgs(["--inputs", "/tmp/space map.json"]) === "/tmp/space map.json");
  ok(parseUnitArgs([], "/tmp/map") === "/tmp/map");
  for (
    const args of [[], ["--plan", "/tmp/p"], ["--inputs", "/tmp/p", "--inputs", "/tmp/q"], [
      "--inputs",
      "relative",
    ]]
  ) await refuses(() => parseUnitArgs(args));
});
Deno.test("fixed full test files execute once with explicit tools and narrow static capability", () => {
  const commands = unitCommands("/root", "/tmp/owned", tools);
  ok(commands.length === 3);
  ok(
    commands[0].args.includes("test_docs_assembly.py") && commands[1].args.includes(unitPaths[1]) &&
      commands[2].args.includes(unitPaths[2]),
  );
  ok(
    commands[1].args.includes("--test-isolation=none"),
    "Node subprocess wrapper must not hide actual test count",
  );
  ok(commands[2].args.at(-2) === "--" && commands[2].args.at(-1) === "/tmp/owned/static");
  for (const c of commands) {
    ok(c.clearEnv === true);
    ok(
      !c.args.some((a) =>
        /filter|ignore|bootstrap|prepare|Pkg|instantiate|build|test-name-pattern/.test(a)
      ),
    );
    ok(!["nix", "julia", "uv", "npm", "git"].includes(c.executable));
  }
  ok(!commands[2].args.some((a) => /^--allow-(env|run|net|ffi)/.test(a)));
});
Deno.test("complete TAP and unittest evidence reject skips/partial/fail/zero", async () => {
  ok(
    parseUnitReport(
      "tap",
      "TAP version 14\nok 1 - x\nok 2 - y\n1..2\n# fail 0\n# skipped 0\n",
      "",
    ) === 2,
  );
  ok(
    parseUnitReport(
      "python",
      "",
      "...\n----------------------------------------------------------------------\nRan 3 tests in 0.004s\n\nOK\n",
    ) === 3,
  );
  for (
    const raw of [
      "1..0\n",
      "ok 1 - x\n",
      "ok 1 - x\n1..2\n",
      "not ok 1 - x\n1..1\n",
      "ok 1 - x # SKIP absent\n1..1\n",
      "ok 1 - x\n1..1\n# skipped 1\n",
      "ok 2 - x\n1..1\n",
      "ok 1 - x\n1..1\n1..1\n",
    ]
  ) await refuses(() => parseUnitReport("tap", raw, ""));
  for (
    const text of [
      "Ran 0 tests in 0.0s\n\nOK\n",
      "Ran 2 tests in 0.1s\n\nOK (skipped=1)\n",
      "Ran 2 tests in 0.1s\n\nFAILED (errors=1)\n",
    ]
  ) await refuses(() => parseUnitReport("python", "", text));
});
Deno.test("static symlink seeds are owned exact live topology before unprivileged test", async () => {
  const root = await Deno.makeTempDir();
  await prepareStaticSeeds(root);
  const file =
    `${root}/prepared-symlink-file/snapshot/runner/src/application/configuration_types.jl`;
  ok(await Deno.readLink(file) === "../../../../backing/configuration_types.jl");
  ok((await Deno.stat(file)).size === 0);
  const directory = `${root}/prepared-symlink-directory/snapshot/core`;
  ok(await Deno.readLink(directory) === "../backing/core");
  ok((await Deno.stat(directory)).isDirectory);
  await refuses(() => prepareStaticSeeds(root));
  await Deno.remove(root, { recursive: true });
});
Deno.test("unit dispatch has no graph/Nix/package adapter and fails missing prerequisite", async () => {
  const root = await Deno.makeTempDir({ dir: "/tmp", prefix: "qcl-docs-routing-" });
  for (const p of ["static", "logs"]) await Deno.mkdir(`${root}/${p}`);
  const path = `${root}/inputs`;
  await Deno.writeTextFile(path, '{"fixture":"/nix/store/immutable"}');
  const calls: Command[] = [];
  const execute = async (c: Command, label: string) => {
    calls.push(c);
    if (label === "version-node") return result("v24.22.1\n");
    if (label === "version-python") {
      return result("3.14.7\n6.0.3\n4.26.0\n/explicit/jsonschema/__init__.py\n");
    }
    if (label === "unit-0") return result("", ".\nRan 1 test in 0.001s\n\nOK\n");
    if (label.startsWith("unit-")) return result("TAP version 14\nok 1 - literal\n1..1\n");
    return result("{}");
  };
  const pass = await runUnits({
    root: "/root",
    temporary: root,
    tools,
    assetInputs: path,
    execute,
  });
  ok(pass.status === "pass" && pass.results.length === 3 && calls.length === 6);
  ok(!calls.some((c) => ["nix", "git", "julia", "uv", "npm"].includes(c.executable)));
  let count = 0;
  await refuses(() =>
    runUnits({
      root: "/root",
      temporary: root,
      tools,
      assetInputs: path,
      execute: async () => {
        count++;
        return result("v22.0.0");
      },
    })
  );
  ok(count === 1);
  await Deno.remove(root, { recursive: true });
});
Deno.test("one docs package handoff preserves P16 D and explicit prepare split", () => {
  const p = planImpact([{
    owner: "root",
    path: "docs/public/make.jl",
    oldMode: "100644",
    newMode: "100644",
  }]);
  const context = { root: "/root", julia: "/existing/julia" };
  const build = checkCommands({ ...p, groups: ["docs-build"] }, context),
    prepare = preparationCommands({ ...p, groups: ["docs-build"] }, context);
  ok(
    build.length === 1 && build[0].cwd === "/root" && build[0].args.join(" ") === "task docs:build",
  );
  ok(prepare.length === 1 && prepare[0].args.join(" ") === "task docs:prepare");
  const prose = planImpact([{
    owner: "root",
    path: "docs/ordinary.md",
    oldMode: "100644",
    newMode: "100644",
  }]);
  ok(prose.groups.join() === "docs" && preparationCommands(prose, context).length === 0);
});
Deno.test("Root discovery excludes only two dedicated test files and mandatory task remains", async () => {
  const config = JSON.parse(await Deno.readTextFile(new URL("../deno.json", import.meta.url)));
  const check = config.tasks.check;
  ok(check.includes("--ignore=tests/docs_math_test.mjs,tests/docs_static_slice_test.ts"));
  ok(check.includes("deno task docs:check"));
  ok(
    config.tasks["docs:check"].includes("ops/docs_tests.ts") &&
      config.tasks["docs:build"].endsWith("ops/docs.ts build") &&
      config.tasks["docs:prepare"].endsWith("ops/docs.ts prepare"),
  );
});
