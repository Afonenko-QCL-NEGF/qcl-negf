import { type SourceGraph, sourceGraph } from "./git.ts";
import {
  type BuildCliDependencies,
  buildSolver,
  captureDepotMetadata,
  prepareDepotMetadata,
  readJuliaManifestSha256,
} from "./solver.ts";
import { main, run, workspace } from "./process.ts";

export function immutableStorePath(value: string): string {
  if (!/^\/nix\/store\/[a-z0-9]{32}-[A-Za-z0-9+._?-]+$/.test(value)) {
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

export async function deploymentManifest(
  sources: SourceGraph,
  application: string,
  solver: string,
  evidence: Record<string, { narHash?: string }>,
  cacheUri?: string,
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
    execute = run,
  } = dependencies;
  const [depotFile, output, cache] = args;
  if (!depotFile || !output || args.length > 3) {
    throw new Error("Usage: application_cd.ts DEPOT_JSON MANIFEST_JSON [NIX_CACHE_URI]");
  }
  validateCacheUri(cache);
  const captured = await captureDepotMetadata(depotFile, open);
  const sources = structuredClone(await readGraph());
  const juliaManifest = await readManifest();
  await prepareDepotMetadata(captured, sources, juliaManifest);
  const application = immutableStorePath(
    await execute({
      executable: "nix",
      args: ["build", "--no-link", "--print-out-paths", "--no-update-lock-file", ".#application"],
      cwd: workspace,
    }, true),
  );
  let solver = "";
  const depotBinding = await buildSolver(captured, sources, juliaManifest, async (command) => {
    const response = await execute(command, true);
    if (command.args[0] === "build") solver = immutableStorePath(response);
    return response;
  });
  const rawInfo = JSON.parse(
    await execute({
      executable: "nix",
      args: ["path-info", "--json", application, solver],
    }, true),
  );
  const evidence: Record<string, { narHash?: string }> = Array.isArray(rawInfo)
    ? Object.fromEntries(rawInfo.map((item) => [item.path, item]))
    : rawInfo;
  const manifest = await deploymentManifest(sources, application, solver, evidence, cache);
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
