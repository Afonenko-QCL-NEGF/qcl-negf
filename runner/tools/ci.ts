// Typed process orchestration. Subprocess arguments never pass through a shell.
import { fileURLToPath } from "node:url";
const root = fileURLToPath(new URL("../", import.meta.url));
const julia = Deno.env.get("JULIA") ?? "julia";
const environment = Deno.env.get("QCL_NEGF_PROJECT");
async function run(args: string[], env: Record<string, string> = {}) {
  const status = await new Deno.Command(julia, {
    args: ["--startup-file=no", ...args],
    cwd: root,
    env: { JULIA_NUM_PRECOMPILE_TASKS: "2", OPENBLAS_NUM_THREADS: "1", ...env },
    stdin: "inherit",
    stdout: "inherit",
    stderr: "inherit",
  }).spawn().status;
  if (!status.success) throw new Error(`Julia failed with exit ${status.code}`);
}
const command = Deno.args[0] ?? "test";
switch (command) {
  case "test":
    if (environment) {
      await run([
        "--threads=2",
        "--check-bounds=yes",
        `--project=${environment}`,
        "test/runtests.jl",
        ...Deno.args.slice(1),
      ]);
    } else {
      await run([
        "--project=.",
        "-e",
        'using Pkg; Pkg.instantiate(); Pkg.test(; julia_args=["--threads=2", "--check-bounds=yes"], test_args=ARGS)',
        ...Deno.args.slice(1),
      ]);
    }
    break;
  case "docs":
    if (!environment) await run(["--project=docs", "-e", "using Pkg; Pkg.instantiate()"]);
    await run([`--project=${environment ?? "docs"}`, "docs/make.jl"]);
    break;
  default:
    throw new Error(`Unknown task: ${command}`);
}
