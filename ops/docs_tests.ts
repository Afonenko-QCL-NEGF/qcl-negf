// Ordinary source-unit entry point. All prerequisites are explicit; this never
// resolves a source graph, prepares packages, or realizes a Nix derivation.
import { captureDocsFile, commandCompleted, parseDocsJson } from "./docs.ts";
import { type Command, main, type RetainedResult, runRetained, workspace } from "./process.ts";

export const unitPaths = [
  "tests/test_docs_assembly.py",
  "tests/docs_math_test.mjs",
  "tests/docs_static_slice_test.ts",
] as const;
export interface UnitTools {
  node: string;
  python: string;
  deno: string;
}
function absolute(path: string): void {
  if (
    !path.startsWith("/") || path.endsWith("/") || path.includes("\\") ||
    path.split("/").slice(1).some((p) => !p || p === "." || p === "..") ||
    // deno-lint-ignore no-control-regex
    /[\x00-\x1f\x7f]/.test(path)
  ) throw Error("explicit_canonical_tool_required");
}
export function parseUnitArgs(args: string[], configured?: string): string {
  const value = args.length === 0
    ? configured
    : args.length === 2 && args[0] === "--inputs"
    ? args[1]
    : undefined;
  if (!value) throw Error("docs_check_requires_asset_inputs");
  absolute(value);
  return value;
}
export function unitCommands(root: string, temporary: string, tools: UnitTools): Command[] {
  for (const path of [root, temporary, ...Object.values(tools)]) absolute(path);
  if (!temporary.startsWith("/tmp/")) throw Error("owned_tmp_capability_required");
  const env = {
    TMPDIR: `${temporary}/python`,
    PYTHONNOUSERSITE: "1",
    PYTHONDONTWRITEBYTECODE: "1",
  };
  return [
    {
      executable: tools.python,
      args: ["-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_docs_assembly.py"],
      cwd: root,
      clearEnv: true,
      env,
    },
    {
      executable: tools.node,
      args: ["--test", "--test-isolation=none", "--test-reporter=tap", unitPaths[1]],
      cwd: root,
      clearEnv: true,
      env: {
        TMPDIR: `${temporary}/node`,
        DOC04_KATEX_ROOT: `${temporary}/assets/katex`,
        DOC04_DOCUMENTER_ROOT: `${temporary}/assets/documenter`,
        DOC04_COMPLETE_CSS_JSON: `${temporary}/assets/css.json`,
      },
    },
    {
      executable: tools.deno,
      args: [
        "test",
        "--no-config",
        "--no-lock",
        "--cached-only",
        "--no-npm",
        "--no-remote",
        "--reporter=tap",
        `--allow-read=${root}/ops/docs,${root}/tests,${temporary}/static`,
        `--allow-write=${temporary}/static`,
        unitPaths[2],
        "--",
        `${temporary}/static`,
      ],
      cwd: root,
      clearEnv: true,
      env: {},
    },
  ] satisfies Command[];
}
export function parseUnitReport(kind: "python" | "tap", stdout: string, stderr: string): number {
  if (kind === "python") {
    const match = stderr.match(/(?:^|\n)Ran (\d+) tests? in [\d.]+s\n\nOK\s*$/);
    if (
      !match || stdout.trim() ||
      /skipped|expected failures|unexpected successes|FAILED|ERROR/.test(stderr)
    ) throw Error("incomplete_python_report");
    const n = Number(match[1]);
    if (!Number.isSafeInteger(n) || n < 1) throw Error("empty_python_report");
    return n;
  }
  if (/^(?:not ok\b|ok .*#\s*(?:SKIP|TODO)\b)/im.test(stdout)) throw Error("failed_or_skipped_tap");
  const plans = [...stdout.matchAll(/^1\.\.(\d+)\s*$/gm)];
  const tests = [...stdout.matchAll(/^ok (\d+)(?:\s|$)/gm)];
  const n = Number(plans[0]?.[1]);
  if (
    plans.length !== 1 || !Number.isSafeInteger(n) || n < 1 || tests.length !== n ||
    tests.some((m, i) => Number(m[1]) !== i + 1)
  ) throw Error("incomplete_tap_report");
  for (const line of stdout.split("\n")) {
    if (
      /^# (?:fail|cancelled|skipped|todo) /.test(line) &&
      !/^# (?:fail|cancelled|skipped|todo) 0\s*$/.test(line)
    ) throw Error("tap_nonpass_summary");
  }
  return n;
}
export async function prepareStaticSeeds(root: string): Promise<void> {
  for (const kind of ["file", "directory"]) {
    const base = `${root}/prepared-symlink-${kind}`;
    await Deno.mkdir(`${base}/backing`, { recursive: true });
    if (kind === "file") {
      await Deno.mkdir(`${base}/snapshot/runner/src/application`, { recursive: true });
      await Deno.writeFile(`${base}/backing/configuration_types.jl`, new Uint8Array(), {
        createNew: true,
      });
      await Deno.symlink(
        "../../../../backing/configuration_types.jl",
        `${base}/snapshot/runner/src/application/configuration_types.jl`,
      );
    } else {
      await Deno.mkdir(`${base}/backing/core`);
      await Deno.mkdir(`${base}/snapshot`);
      await Deno.symlink("../backing/core", `${base}/snapshot/core`);
    }
  }
}
export async function runUnits(options: {
  root: string;
  temporary: string;
  tools: UnitTools;
  assetInputs: string;
  execute?: (command: Command, label: string) => Promise<RetainedResult>;
}) {
  const execute = options.execute ?? ((command, label) =>
    runRetained(command, {
      directory: `${options.temporary}/logs/${label}`,
      limits: {
        wallMs: 120000,
        drainMs: 5000,
        streamBytes: 4 * 1024 * 1024,
        totalBytes: 8 * 1024 * 1024,
      },
    }));
  const call = async (command: Command, label: string) => {
    const result = await execute(structuredClone(command), label);
    if (!commandCompleted(result)) throw Error(`docs_unit_transport_incomplete:${label}`);
    return {
      stdout: new TextDecoder("utf-8", { fatal: true }).decode(result.stdout),
      stderr: new TextDecoder("utf-8", { fatal: true }).decode(result.stderr),
    };
  };
  const base = { cwd: options.root, clearEnv: true, env: {} };
  for (
    const [name, executable, args, expected] of [
      ["node", options.tools.node, ["--version"], /^v24\./],
      ["python", options.tools.python, [
        "-B",
        "-c",
        "import sys,yaml,jsonschema; print(sys.version.split()[0]); print(yaml.__version__); from importlib.metadata import version; print(version('jsonschema')); print(jsonschema.__file__)",
      ], /^3\.14\.\d+\n6\.\d+\.\d+\n4\.\d+\.\d+\n.+jsonschema/],
    ] as const
  ) {
    const report = await call({ ...base, executable, args: [...args] }, `version-${name}`);
    if (!expected.test(report.stdout) || report.stderr.trim()) {
      throw Error(`docs_unit_prerequisite:${name}`);
    }
  }
  const captured = await captureDocsFile(options.assetInputs, 2 * 1024 * 1024);
  const asset = parseDocsJson(captured.raw);
  if (!asset || typeof asset !== "object" || Array.isArray(asset) || !Object.keys(asset).length) {
    throw Error("asset_inputs_shape");
  }
  const capturedPath = `${options.temporary}/asset-inputs.json`;
  await Deno.writeTextFile(capturedPath, captured.raw, { createNew: true, mode: 0o600 });
  await call({
    ...base,
    executable: options.tools.python,
    args: [
      "-B",
      `${options.root}/ops/docs/produce.py`,
      "--unit-assets",
      capturedPath,
      "--unit-output",
      `${options.temporary}/assets`,
    ],
  }, "asset-fixture");
  await prepareStaticSeeds(`${options.temporary}/static`);
  const results = [];
  for (
    const [i, command] of unitCommands(options.root, options.temporary, options.tools).entries()
  ) {
    const report = await call(command, `unit-${i}`);
    results.push({
      path: unitPaths[i],
      tests: parseUnitReport(i === 0 ? "python" : "tap", report.stdout, report.stderr),
    });
  }
  return {
    status: "pass",
    qualification: "source_units_only_not_native_documentation",
    assets_sha256: captured.ref.sha256,
    results,
  };
}
export async function runUnitCli(args: string[]) {
  const assetInputs = parseUnitArgs(args, Deno.env.get("QCL_NEGF_DOCS_ASSET_INPUTS"));
  const tools = {
    node: Deno.env.get("QCL_NEGF_DOCS_NODE") ?? "",
    python: Deno.env.get("QCL_NEGF_DOCS_PYTHON") ?? "",
    deno: Deno.execPath(),
  };
  for (const path of Object.values(tools)) {
    absolute(path);
    if (!(await Deno.stat(path)).isFile) throw Error("docs_unit_tool_missing");
  }
  const temporary = await Deno.makeTempDir({ dir: "/tmp", prefix: "qcl-docs-units-" });
  for (const name of ["python", "node", "static", "logs"]) {
    await Deno.mkdir(`${temporary}/${name}`, { mode: 0o700 });
  }
  // Retain the owned fixture and command logs on failure; the returned directory
  // is diagnostic evidence, never admission or a reusable package cache.
  try {
    return {
      ...await runUnits({ root: workspace, temporary, tools, assetInputs }),
      evidence: temporary,
    };
  } catch (error) {
    throw new Error(`${error}; evidence=${temporary}`, { cause: error });
  }
}
if (import.meta.main) {
  main(async () => console.log(JSON.stringify(await runUnitCli(Deno.args), null, 2)));
}
