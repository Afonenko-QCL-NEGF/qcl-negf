import { type SourceGraph, sourceGraph } from "./git.ts";
import { buildSolver, type DepotSpec } from "./solver.ts";
import { main, run, workspace } from "./process.ts";

export function immutableStorePath(value: string): string {
  if (!/^\/nix\/store\/[a-z0-9]{32}-[A-Za-z0-9+._?-]+$/.test(value)) {
    throw new Error("Release requires a single immutable Nix store closure path");
  }
  return value;
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
  if (
    cacheUri !== undefined && (
      !cacheUri || cacheUri.startsWith("-") || /\s/.test(cacheUri) ||
      Array.from(cacheUri).some((character) =>
        character.charCodeAt(0) < 32 || character.charCodeAt(0) === 127
      )
    )
  ) {
    throw new Error("Release cache URI must be a nonempty Nix store URI without controls");
  }
  if (cacheUri?.includes("://") && new URL(cacheUri).password) {
    throw new Error("Release cache URI must not embed credentials");
  }
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

// Builds already pinned source inputs. Deployment is the platform adapter's
// separate command and runs under its dedicated maintenance credentials.
if (import.meta.main) {
  await main(async () => {
    const [depotFile, output, cache] = Deno.args;
    if (!depotFile || !output || Deno.args.length > 3) {
      throw new Error("Usage: application_cd.ts DEPOT_JSON MANIFEST_JSON [NIX_CACHE_URI]");
    }
    const sources = await sourceGraph();
    const application = immutableStorePath(
      await run({
        executable: "nix",
        args: ["build", "--no-link", "--print-out-paths", "--no-update-lock-file", ".#application"],
        cwd: workspace,
      }, true),
    );
    const spec: DepotSpec = JSON.parse(await Deno.readTextFile(depotFile));
    let solver = "";
    await buildSolver(spec, sources.revision, depotFile, async (command) => {
      const response = await run(command, true);
      if (command.args[0] === "build") solver = immutableStorePath(response);
      return response;
    });
    const rawInfo = JSON.parse(
      await run({
        executable: "nix",
        args: ["path-info", "--json", application, solver],
      }, true),
    );
    const evidence: Record<string, { narHash?: string }> = Array.isArray(rawInfo)
      ? Object.fromEntries(rawInfo.map((item) => [item.path, item]))
      : rawInfo;
    const manifest = await deploymentManifest(sources, application, solver, evidence, cache);
    if (JSON.stringify(await sourceGraph()) !== JSON.stringify(sources)) {
      throw new Error("Source graph changed during release assembly");
    }
    // Publish both closures before advertising a deployable manifest.
    if (cache) {
      await run({ executable: "nix", args: ["copy", "--to", cache, application, solver] });
    }
    const temporary = output + ".pending";
    await Deno.writeTextFile(temporary, JSON.stringify(manifest, null, 2) + "\n", {
      createNew: true,
    });
    await Deno.rename(temporary, output);
    console.log(`Application release manifest: ${output}`);
  });
}
