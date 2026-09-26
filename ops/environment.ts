import { main, run, workspace } from "./process.ts";

const components = `${workspace}/components`;
const frontend = `${components}/qcl-negf-portal/frontend`;
export const julia = Deno.env.get("JULIA") ?? "julia";

export async function frontendBuild(): Promise<void> {
  await run({ executable: "npm", args: ["ci", "--ignore-scripts"], cwd: frontend });
  await run({ executable: "npm", args: ["run", "build"], cwd: frontend });
}

export async function sync(): Promise<void> {
  // Portal's native build hook refuses a wheel without its frontend assets.
  await frontendBuild();
  await run({
    executable: "uv",
    args: ["sync", "--locked", "--all-packages", "--all-extras", "--all-groups"],
    cwd: workspace,
  });
  await run({
    executable: julia,
    args: ["--startup-file=no", "--project=julia", "-e", "using Pkg; Pkg.instantiate()"],
    cwd: workspace,
    env: { JULIA_NUM_PRECOMPILE_TASKS: "2", OPENBLAS_NUM_THREADS: "1" },
  });
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
    if (Deno.args.length !== 1 || !["sync", "lock"].includes(Deno.args[0])) {
      throw new Error("Usage: environment.ts sync|lock");
    }
    if (Deno.args[0] === "sync") await sync();
    else await lock();
  });
}
