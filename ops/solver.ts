import { sourceGraph } from "./git.ts";
import { type Command, exists, main, run, workspace } from "./process.ts";

export interface DepotSpec {
  sources?: { revision?: string };
  url: string;
  hash: string;
}

export async function buildSolver(
  spec: DepotSpec,
  revision: string,
  target: string,
  execute: (command: Command) => Promise<string> = run,
): Promise<void> {
  if (spec.sources?.revision !== revision) {
    throw new Error("Depot belongs to a different source graph");
  }
  if (new URL(spec.url).protocol === "file:") {
    // The sandbox cannot see the archive's host path. Verified flat-file
    // prefetch supplies the exact fetchurl output without weakening isolation.
    await execute({
      executable: "nix",
      args: [
        "store",
        "prefetch-file",
        "--hash-type",
        "sha256",
        "--expected-hash",
        spec.hash,
        "--name",
        "qcl-negf-julia-depot.tar.gz",
        spec.url,
      ],
      cwd: workspace,
    });
  }
  const fileUrl = new URL(`file://${workspace}/`);
  fileUrl.searchParams.set("rev", revision);
  fileUrl.searchParams.set("submodules", "1");
  await execute({
    executable: "nix",
    args: [
      "build",
      "--impure",
      "--no-link",
      "--print-out-paths",
      "--file",
      "nix/solver.nix",
      "--argstr",
      "source",
      `git+${fileUrl.href}`,
      "--argstr",
      "depotManifest",
      await Deno.realPath(target),
    ],
    cwd: workspace,
  });
}

async function checksum(path: string): Promise<string> {
  const output = await run({ executable: "sha256sum", args: [path] }, true);
  const match = /^([a-f0-9]{64})\s/.exec(output);
  if (!match) throw new Error("Invalid SHA-256 output");
  return match[1];
}

function sri(hex: string): string {
  const bytes = hex.match(/../g)!.map((pair) => parseInt(pair, 16));
  return "sha256-" + btoa(String.fromCharCode(...bytes));
}

async function solver(): Promise<void> {
  const [operation, target, ...flags] = Deno.args;
  if (!target || !["depot", "build"].includes(operation)) {
    throw new Error("Usage: solver.ts depot OUTPUT_DIRECTORY [--url URL] | build DEPOT_JSON");
  }
  const graph = await sourceGraph();
  if (operation === "build") {
    if (flags.length) throw new Error("Unexpected build arguments");
    const spec = JSON.parse(await Deno.readTextFile(target));
    await buildSolver(spec, graph.revision, target);
    return;
  }
  if (flags.length && (flags.length !== 2 || flags[0] !== "--url")) {
    throw new Error("Expected --url URL");
  }
  const requestedUrl = flags[1] ? new URL(flags[1]) : undefined;
  if (
    requestedUrl &&
    (!["https:", "http:"].includes(requestedUrl.protocol) || requestedUrl.username ||
      requestedUrl.password)
  ) {
    throw new Error("Artifact URL must use HTTP(S) without embedded credentials");
  }
  if (await exists(target)) throw new Error("Choose a new depot output directory");
  await Deno.mkdir(target, { recursive: true });
  const output = await Deno.realPath(target);
  const depot = `${output}/depot`;
  const { julia } = await import("./environment.ts");
  await run({
    executable: "deno",
    args: ["task", "prepare-depot", `${workspace}/julia`, depot],
    cwd: `${workspace}/components/QCLNEGFRunner.jl`,
    env: { JULIA: julia },
  });
  if (JSON.stringify(await sourceGraph()) !== JSON.stringify(graph)) {
    throw new Error("Sources changed during depot preparation");
  }
  const archive = `${output}/depot.tar.gz`;
  await run({
    executable: "tar",
    args: [
      "--sort=name",
      "--mtime=@0",
      "--owner=0",
      "--group=0",
      "--numeric-owner",
      "-czf",
      archive,
      "-C",
      depot,
      ".",
    ],
  });
  const manifest = {
    format: "qcl-negf.julia-depot.v1",
    sources: graph,
    julia: "1.13.0",
    juliaManifest: await checksum(`${workspace}/julia/Manifest.toml`),
    url: requestedUrl?.href ?? new URL(`file://${archive}`).href,
    hash: sri(await checksum(archive)),
  };
  await Deno.writeTextFile(`${output}/solver-depot.json`, JSON.stringify(manifest, null, 2) + "\n");
  console.log(`${output}/solver-depot.json`);
  // Archive publication is intentionally separate from generation; no upload occurs here.
}

if (import.meta.main) await main(solver);
