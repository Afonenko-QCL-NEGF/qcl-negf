import { type SourceGraph, sourceGraph } from "./git.ts";
import {
  type BuildCliDependencies,
  buildSolver,
  canonicalSourceGraphJson,
  captureDepotMetadata,
  type DepotInputs,
  depotNeedsInputs,
  parseBuildOptions,
  prepareDepotMetadata,
  readDepotInputs,
  readInstalledJuliaManifestSha256,
  readJuliaManifestSha256,
  solverBuildOutput,
  type SolverBuildResult,
} from "./solver.ts";
import { main, run, workspace } from "./process.ts";

export function immutableStorePath(value: string): string {
  if (/[\r\n]/.test(value) || !/^\/nix\/store\/[a-z0-9]{32}-[A-Za-z0-9+._?-]+$/.test(value)) {
    throw new Error("Release requires a single immutable Nix store closure path");
  }
  return value;
}

function validateCacheUri(cacheUri: unknown): void {
  if (cacheUri === undefined) return;
  if (
    typeof cacheUri !== "string" || !cacheUri || cacheUri.startsWith("-") || /\s/.test(cacheUri) ||
    Array.from(cacheUri).some((character) =>
      character.charCodeAt(0) < 32 || character.charCodeAt(0) === 127
    )
  ) {
    throw new Error("Release cache URI must be a nonempty Nix store URI without controls");
  }
  if (cacheUri.includes("://")) {
    const parsed = new URL(cacheUri);
    // URL.password drops an explicit empty delimiter. Inspect raw userinfo before
    // normalization; encoded colons inside a username remain username data.
    const authority = cacheUri.slice(cacheUri.indexOf("://") + 3).split(/[/?#]/, 1)[0];
    const at = authority.lastIndexOf("@");
    if (parsed.password || (at >= 0 && authority.slice(0, at).includes(":"))) {
      throw new Error("Release cache URI must not embed credentials");
    }
  }
}

export interface SolverAssemblyReceipt {
  // Trusted builder adapter input, never request/client metadata. The raw build
  // stdout must come from the command that consumed consumed_metadata_json.
  result: SolverBuildResult;
  depotInputs?: DepotInputs;
  juliaManifestSha256: string;
  installedJuliaManifestSha256: string;
}

async function checkedSolverBuild(
  sources: SourceGraph,
  solver: string,
  evidence: Record<string, { narHash?: string; deriver?: string }>,
  receipt: SolverAssemblyReceipt,
) {
  const result = receipt.result;
  const actual = solverBuildOutput(result.build_stdout_json);
  const prepared = await prepareDepotMetadata(
    result.consumed_metadata_json,
    sources,
    receipt.juliaManifestSha256,
    receipt.depotInputs,
  );
  const graphDigest = new Uint8Array(
    await crypto.subtle.digest(
      "SHA-256",
      new TextEncoder().encode(canonicalSourceGraphJson(sources)),
    ),
  );
  const sourceGraphSha = Array.from(graphDigest, (byte) => byte.toString(16).padStart(2, "0")).join(
    "",
  );
  const refs = new Set(sources.components.map((row) => row.path));
  if (
    !refs.has("components/QCLNEGF.jl") || !refs.has("components/QCLNEGFRunner.jl") ||
    result.source_graph_sha256 !== sourceGraphSha || result.source_revision !== sources.revision ||
    result.consumed_metadata_sha256 !== prepared.binding.consumed_metadata_sha256 ||
    result.consumed_metadata_bytes !== prepared.binding.consumed_metadata_bytes ||
    result.normalization !== prepared.binding.normalization ||
    result.depot_format !== prepared.binding.depot_format ||
    result.depot_inputs_sha256 !== prepared.binding.depot_inputs_sha256 ||
    result.archive_url !== prepared.binding.archive_url ||
    result.archive_hash !== prepared.binding.archive_hash ||
    result.julia_manifest_sha256 !== receipt.juliaManifestSha256 ||
    receipt.installedJuliaManifestSha256 !== receipt.juliaManifestSha256 ||
    actual.drv_path !== result.drv_path || actual.output_path !== result.output_path ||
    actual.output_path !== solver
  ) throw new Error("Solver build receipt differs from consumed source, Manifest or actual output");
  const deriver = evidence[solver]?.deriver;
  if (deriver && deriver !== "unknown-deriver" && deriver !== actual.drv_path) {
    throw new Error("Known solver deriver differs from captured actual build JSON");
  }
  return {
    source_graph_sha256: sourceGraphSha,
    julia_manifest_sha256: result.julia_manifest_sha256,
    drv_path: actual.drv_path,
    output_path: actual.output_path,
  };
}

export async function deploymentManifest(
  sources: SourceGraph,
  application: string,
  solver: string,
  evidence: Record<string, { narHash?: string; deriver?: string }>,
  cacheUri?: string,
  solverReceipt?: SolverAssemblyReceipt,
) {
  immutableStorePath(application);
  immutableStorePath(solver);
  validateCacheUri(cacheUri);
  const closures = [application, solver].map((path) => {
    const narHash = evidence[path]?.narHash;
    if (typeof narHash !== "string" || !/^sha256-[A-Za-z0-9+/]{43}=$/.test(narHash)) {
      throw new Error(`Missing immutable closure hash for ${path}`);
    }
    return { path, narHash };
  });
  const solverBuild = solverReceipt === undefined
    ? undefined
    : await checkedSolverBuild(sources, solver, evidence, solverReceipt);
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(JSON.stringify({ sources, closures })),
  );
  const release_id = Array.from(
    new Uint8Array(digest),
    (value) => value.toString(16).padStart(2, "0"),
  ).join("");
  return {
    schema: "qcl-negf-release-v1",
    release_id,
    application_path: application,
    solver_executable: `${solver}/bin/qcl-negf`,
    sources,
    closures,
    ...(solverBuild === undefined ? {} : { solver_build: solverBuild }),
    ...(cacheUri === undefined ? {} : { cache_uri: cacheUri }),
  };
}

// Builds pinned source inputs and retains the immutable release manifest.
// Local publication and whole-cluster delivery belong to the platform controller
// under local operator authority.
export async function runApplicationCdCli(
  args: readonly string[],
  dependencies: Partial<BuildCliDependencies> = {},
) {
  const {
    openDepotInput: open = (path: string) => Deno.open(path, { read: true }),
    readSourceGraph: readGraph = sourceGraph,
    readJuliaManifestSha256: readManifest = readJuliaManifestSha256,
    readInstalledJuliaManifestSha256: readInstalled = readInstalledJuliaManifestSha256,
    execute = run,
    readDepotInputs: readInputs = readDepotInputs,
  } = dependencies;
  const flagAt = args.findIndex((v) => v.startsWith("--"));
  const positional = flagAt < 0 ? args : args.slice(0, flagAt);
  const options = parseBuildOptions(flagAt < 0 ? [] : [...args.slice(flagAt)]);
  const [depotFile, output, cache] = positional;
  if (!depotFile || !output || positional.length > 3) {
    throw new Error("Usage: application_cd.ts DEPOT_JSON MANIFEST_JSON [NIX_CACHE_URI]");
  }
  validateCacheUri(cache);
  const captured = await captureDepotMetadata(depotFile, open);
  const sources = structuredClone(await readGraph());
  const juliaManifest = await readManifest();
  // Legacy v1 does not perform a new Nix evaluation. V2 requires CURRENT expected inputs.
  const isV2 = depotNeedsInputs(captured);
  const depotInputs = isV2 ? await readInputs(sources, options) : undefined;
  await prepareDepotMetadata(captured, sources, juliaManifest, depotInputs);
  const application = immutableStorePath(
    await execute({
      executable: "nix",
      args: ["build", "--no-link", "--print-out-paths", "--no-update-lock-file", ".#application"],
      cwd: workspace,
    }, true),
  );
  const depotBinding = await buildSolver(
    captured,
    sources,
    juliaManifest,
    execute,
    options,
    depotInputs,
  );
  const solver = immutableStorePath(depotBinding.output_path);
  const installedJuliaManifest = await readInstalled(solver);
  const rawInfo = JSON.parse(
    await execute({
      executable: "nix",
      args: ["path-info", "--json", application, solver],
    }, true),
  );
  const evidence: Record<string, { narHash?: string; deriver?: string }> = Array.isArray(rawInfo)
    ? Object.fromEntries(rawInfo.map((item) => [item.path, item]))
    : rawInfo;
  const manifest = await deploymentManifest(sources, application, solver, evidence, cache, {
    result: depotBinding,
    depotInputs,
    juliaManifestSha256: juliaManifest,
    installedJuliaManifestSha256: installedJuliaManifest,
  });
  if (JSON.stringify(await readGraph()) !== JSON.stringify(sources)) {
    throw new Error("Source graph changed during release assembly");
  }
  // Publish both closures before advertising a deployable manifest.
  if (cache) {
    await execute({ executable: "nix", args: ["copy", "--to", cache, application, solver] });
  }
  const temporary = output + ".pending";
  await Deno.writeTextFile(temporary, JSON.stringify(manifest, null, 2) + "\n", {
    createNew: true,
  });
  await Deno.rename(temporary, output);
  console.log(`Application release manifest: ${output}`);
  return { manifest, depotBinding };
}

if (import.meta.main) {
  await main(async () => {
    await runApplicationCdCli(Deno.args);
  });
}
