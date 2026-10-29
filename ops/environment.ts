import { type Command, main, run, workspace } from "./process.ts";
import { type SourceGraph, sourceGraph } from "./git.ts";
import { runPlanCommands } from "./ci.ts";
import {
  type ImpactContext,
  type ImpactPlan,
  parseImpactOptions,
  preparationCommands,
  resolveImpact,
} from "./impact.ts";

const components = `${workspace}/components`;
const frontend = `${components}/qcl-negf-portal/frontend`;
export const julia = Deno.env.get("JULIA") ?? "julia";

export async function frontendBuild(): Promise<void> {
  await run({ executable: "npm", args: ["ci", "--ignore-scripts"], cwd: frontend });
  await run({ executable: "npm", args: ["run", "build"], cwd: frontend });
}

export async function runPreparation(
  plan: ImpactPlan,
  context: ImpactContext,
  execute: (command: Command) => Promise<string> = run,
  readGraph: () => Promise<SourceGraph> = () => sourceGraph(context.root),
): Promise<void> {
  await runPlanCommands(plan, context, preparationCommands(plan, context), execute, readGraph);
}

export async function sync(args: readonly string[] = []): Promise<void> {
  const plan = await resolveImpact(parseImpactOptions(args));
  await runPreparation(plan, { root: workspace, julia: Deno.env.get("JULIA") ?? "julia" });
}

export async function lock(): Promise<void> {
  await run({ executable: "uv", args: ["lock"], cwd: workspace });
  await run({
    executable: "npm",
    args: ["install", "--package-lock-only", "--ignore-scripts"],
    cwd: frontend,
  });
  await run({
    executable: "deno",
    args: ["task", "lock:nix"],
    cwd: `${components}/qcl-negf-portal`,
  });
  await run({
    executable: julia,
    args: [
      "--startup-file=no",
      `${components}/QCLNEGFRunner.jl/tools/prepare_workspace.jl`,
      `${components}/QCLNEGF.jl`,
      `${components}/QCLNEGFRunner.jl`,
      `${workspace}/julia`,
    ],
    cwd: workspace,
    env: { JULIA_NUM_PRECOMPILE_TASKS: "2", OPENBLAS_NUM_THREADS: "1" },
  });
  await run({ executable: "nix", args: ["flake", "lock"], cwd: `${components}/qcl-negf-platform` });
  await run({ executable: "nix", args: ["flake", "lock"], cwd: workspace });
  for (const backend of ["proxmox", "arch-libvirt"]) {
    await run({
      executable: "tofu",
      args: ["init", "-backend=false", "-input=false"],
      cwd: `${components}/qcl-negf-platform/tofu/${backend}`,
    });
  }
}

if (import.meta.main) {
  await main(async () => {
    const [command, ...args] = Deno.args;
    if (command === "sync") await sync(args);
    else if (command === "lock" && args.length === 0) await lock();
    else throw new Error("Usage: environment.ts sync [impact options] | lock");
  });
}
