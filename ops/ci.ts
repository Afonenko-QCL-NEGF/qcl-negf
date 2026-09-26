import { main, run, workspace } from "./process.ts";
import { julia } from "./environment.ts";
import { sourceGraph } from "./git.ts";

await main(async () => {
  const args = new Set(Deno.args);
  if ([...args].some((a) => !["--python", "--julia", "--infra"].includes(a))) {
    throw new Error("Usage: deno task test [--python|--julia|--infra]");
  }
  const all = args.size === 0;
  const graph = await sourceGraph();
  if (all || args.has("--python")) {
    await run({
      executable: "deno",
      args: ["task", "check"],
      cwd: `${workspace}/components/qcl-negf-portal`,
    });
    for (const name of ["contracts", "results", "aiida", "portal", "research"]) {
      const path = `components/qcl-negf-${name}`;
      await run({
        executable: "uv",
        args: [
          "run",
          "--locked",
          "--no-sync",
          "pytest",
          "-c",
          `${path}/pyproject.toml`,
          `${path}/tests`,
        ],
        cwd: workspace,
      });
    }
    await run({
      executable: "uv",
      args: [
        "run",
        "--locked",
        "--no-sync",
        "python",
        "components/qcl-negf-research/tools/validate.py",
      ],
      cwd: workspace,
    });
    await run({
      executable: "npm",
      args: ["test"],
      cwd: `${workspace}/components/qcl-negf-portal/frontend`,
    });
  }
  if (all || args.has("--julia")) {
    for (const name of ["QCLNEGF.jl", "QCLNEGFRunner.jl"]) {
      await run({
        executable: "deno",
        args: ["task", "check"],
        cwd: `${workspace}/components/${name}`,
      });
      await run({
        executable: julia,
        args: [
          "--startup-file=no",
          "--threads=2",
          "--check-bounds=yes",
          `--project=${workspace}/julia`,
          `${workspace}/components/${name}/test/runtests.jl`,
        ],
        cwd: `${workspace}/components/${name}`,
        env: { OPENBLAS_NUM_THREADS: "1", JULIA_NUM_PRECOMPILE_TASKS: "2" },
      });
      await run({
        executable: "deno",
        args: ["task", "docs"],
        cwd: `${workspace}/components/${name}`,
        env: { JULIA: julia, QCL_NEGF_PROJECT: `${workspace}/julia` },
      });
    }
    await run({
      executable: "uv",
      args: [
        "run",
        "--locked",
        "--no-sync",
        "pytest",
        "-c",
        "components/qcl-negf-results/pyproject.toml",
        "components/qcl-negf-results/integration",
      ],
      cwd: workspace,
      env: { JULIA: julia, QCL_NEGF_SOLVER_PROJECT: `${workspace}/julia` },
    });
  }
  if (all || args.has("--infra")) {
    await run({
      executable: "deno",
      args: ["task", "check"],
      cwd: `${workspace}/components/qcl-negf-platform`,
    });
    for (const backend of ["proxmox", "arch-libvirt"]) {
      const cwd = `${workspace}/components/qcl-negf-platform/tofu/${backend}`;
      await run({ executable: "tofu", args: ["fmt", "-check", "-recursive"], cwd });
      await run({
        executable: "tofu",
        args: ["init", "-backend=false", "-input=false", "-lockfile=readonly"],
        cwd,
      });
      await run({ executable: "tofu", args: ["validate"], cwd });
    }
    await run({
      executable: "nix",
      args: ["flake", "check", "--no-build", "--no-update-lock-file"],
      cwd: workspace,
    });
  }
  if (JSON.stringify(await sourceGraph()) !== JSON.stringify(graph)) {
    throw new Error("The Git source graph changed during checks");
  }
});
