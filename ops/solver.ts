import { type SourceGraph, sourceGraph } from "./git.ts";
import { type Command, exists, main, run, workspace } from "./process.ts";

export interface DepotInputFile {
  stat(): Promise<{ isFile: boolean }>;
  read(buffer: Uint8Array): Promise<number | null>;
  close(): void;
}
export type OpenDepotInput = (path: string) => Promise<DepotInputFile>;

export interface BuildCliDependencies {
  openDepotInput: OpenDepotInput;
  readSourceGraph(): Promise<SourceGraph>;
  readJuliaManifestSha256(): Promise<string>;
  execute(command: Command, capture?: boolean): Promise<string>;
}

export interface DepotBinding {
  readonly captured_input_sha256: string;
  readonly captured_input_bytes: number;
  readonly consumed_metadata_sha256: string;
  readonly consumed_metadata_bytes: number;
  readonly normalization: "JSON.parse→JSON.stringify";
  readonly source_revision: string;
  readonly julia_manifest_sha256: string;
  readonly archive_url: string;
  readonly archive_hash: string;
}

const metadataLimit = 65536;
const encoder = new TextEncoder();
const openDepotInput: OpenDepotInput = (path) => Deno.open(path, { read: true });

async function sha256(bytes: Uint8Array): Promise<string> {
  const digest = new Uint8Array(
    await crypto.subtle.digest("SHA-256", new Uint8Array(bytes).buffer),
  );
  return Array.from(digest, (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export async function readJuliaManifestSha256(): Promise<string> {
  return await sha256(await Deno.readFile(`${workspace}/julia/Manifest.toml`));
}

export async function captureDepotMetadata(
  path: string,
  open: OpenDepotInput = openDepotInput,
): Promise<string> {
  const file = await open(path);
  try {
    if (!(await file.stat()).isFile) throw new Error("Depot metadata must be a regular file");
    const buffer = new Uint8Array(metadataLimit + 1);
    let count = 0;
    while (true) {
      const read = await file.read(buffer.subarray(count));
      if (read === null) break;
      if (!Number.isInteger(read) || read <= 0 || read > buffer.length - count) {
        throw new Error("Depot metadata read made no valid progress");
      }
      count += read;
      if (count > metadataLimit) throw new Error("Depot metadata exceeds 65536 bytes");
    }
    const bytes = buffer.subarray(0, count);
    if (bytes.includes(0) || (bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf)) {
      throw new Error("Depot metadata contains raw NUL or BOM");
    }
    const value = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    const encoded = encoder.encode(value);
    if (encoded.length !== bytes.length || encoded.some((byte, index) => byte !== bytes[index])) {
      throw new Error("Depot metadata UTF8 roundtrip failed");
    }
    return value;
  } finally {
    file.close();
  }
}

function object(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function graphComponents(value: unknown): Map<string, { revision: string; url: string }> {
  if (!Array.isArray(value)) throw new Error("Invalid depot component graph");
  const components = new Map<string, { revision: string; url: string }>();
  for (const component of value) {
    if (
      !object(component) || typeof component.path !== "string" ||
      typeof component.revision !== "string" || typeof component.url !== "string" ||
      components.has(component.path)
    ) {
      throw new Error("Invalid or duplicate depot component");
    }
    components.set(component.path, { revision: component.revision, url: component.url });
  }
  return components;
}

// Shared CLI preflight and direct-helper validation; no dispatch or pathname access.
export async function prepareDepotMetadata(
  metadataJson: string,
  expectedGraph: SourceGraph,
  expectedManifest: string,
) {
  if (typeof metadataJson !== "string") {
    throw new Error("Depot metadata must be a captured JSON string");
  }
  const captured = encoder.encode(metadataJson);
  if (
    captured.length > metadataLimit || metadataJson.startsWith("\uFEFF") ||
    metadataJson.includes("\0") ||
    new TextDecoder("utf-8", { fatal: true }).decode(captured) !== metadataJson
  ) {
    throw new Error("Invalid or oversized depot metadata string");
  }
  const metadata: unknown = JSON.parse(metadataJson);
  if (
    !object(metadata) || metadata.format !== "qcl-negf.julia-depot.v1" ||
    metadata.julia !== "1.13.0" || typeof expectedManifest !== "string" ||
    !/^[a-f0-9]{64}$/.test(expectedManifest) || metadata.juliaManifest !== expectedManifest
  ) {
    throw new Error("Depot format, Julia version or Manifest identity mismatch");
  }
  const sources = metadata.sources;
  if (
    !object(sources) || sources.format !== "qcl-negf.git-graph.v1" || !object(expectedGraph) ||
    expectedGraph.format !== "qcl-negf.git-graph.v1" ||
    typeof expectedGraph.revision !== "string" || !/^[a-f0-9]{40}$/.test(expectedGraph.revision) ||
    sources.revision !== expectedGraph.revision
  ) {
    throw new Error("Depot belongs to a different source graph");
  }
  const expected = graphComponents(expectedGraph.components);
  const actual = graphComponents(sources.components);
  if (actual.size !== expected.size) throw new Error("Depot component set mismatch");
  for (const [path, component] of expected) {
    const candidate = actual.get(path);
    if (
      !candidate || candidate.revision !== component.revision || candidate.url !== component.url
    ) {
      throw new Error("Depot component identity mismatch");
    }
  }
  if (typeof metadata.url !== "string" || typeof metadata.hash !== "string") {
    throw new Error("Depot archive URL and hash must be strings");
  }
  const url = metadata.url;
  const archiveHash = metadata.hash;
  const protocol = new URL(url).protocol;
  const revision = expectedGraph.revision;
  const manifest = expectedManifest;
  const boundJson = JSON.stringify(metadata);
  if (typeof boundJson !== "string") throw new Error("Depot metadata serialization failed");
  const consumed = encoder.encode(boundJson);
  if (consumed.length > metadataLimit) {
    throw new Error("Produced depot metadata exceeds 65536 bytes");
  }
  const capturedSha = await sha256(captured);
  const consumedSha = await sha256(consumed);
  const binding: DepotBinding = Object.freeze({
    captured_input_sha256: capturedSha,
    captured_input_bytes: captured.length,
    consumed_metadata_sha256: consumedSha,
    consumed_metadata_bytes: consumed.length,
    normalization: "JSON.parse→JSON.stringify",
    source_revision: revision,
    julia_manifest_sha256: manifest,
    archive_url: url,
    archive_hash: archiveHash,
  });
  return { boundJson, protocol, binding };
}

export interface BuildOptions {
  profile: "production-build" | "local-debug";
  testWorkerLimit: number | null;
}

export function parseBuildOptions(flags: string[]): BuildOptions {
  const options: BuildOptions = { profile: "production-build", testWorkerLimit: null };
  const seen = new Set<string>();
  for (let index = 0; index < flags.length; index += 2) {
    const flag = flags[index];
    const value = flags[index + 1];
    if (seen.has(flag) || value === undefined) throw new Error("Missing or duplicate build option");
    seen.add(flag);
    if (flag === "--profile" && ["production-build", "local-debug"].includes(value)) {
      options.profile = value as BuildOptions["profile"];
    } else if (flag === "--test-workers" && /^[1-9][0-9]*$/.test(value)) {
      const workers = Number(value);
      if (!Number.isSafeInteger(workers)) {
        throw new Error("Worker limit must be a safe positive integer");
      }
      options.testWorkerLimit = workers;
    } else {
      throw new Error("Expected --profile production-build|local-debug or --test-workers INTEGER");
    }
  }
  if (
    options.profile === "local-debug" && options.testWorkerLimit !== null &&
    options.testWorkerLimit !== 2
  ) {
    throw new Error("local-debug uses two test workers");
  }
  return options;
}

export async function buildSolver(
  metadataJson: string,
  expectedGraph: SourceGraph,
  expectedJuliaManifestSha256: string,
  execute: (command: Command) => Promise<string> = run,
  options: BuildOptions = parseBuildOptions([]),
): Promise<DepotBinding> {
  // Validate programmatic callers before prefetch/build as well as CLI input.
  options = parseBuildOptions([
    "--profile",
    options.profile,
    ...(options.testWorkerLimit === null
      ? []
      : ["--test-workers", String(options.testWorkerLimit)]),
  ]);
  const profile = options.profile;
  const workers = options.testWorkerLimit;
  const { boundJson, protocol, binding } = await prepareDepotMetadata(
    metadataJson,
    expectedGraph,
    expectedJuliaManifestSha256,
  );
  if (protocol === "file:") {
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
        binding.archive_hash,
        "--name",
        "qcl-negf-julia-depot.tar.gz",
        binding.archive_url,
      ],
      cwd: workspace,
    });
  }
  const fileUrl = new URL(`file://${workspace}/`);
  fileUrl.searchParams.set("rev", binding.source_revision);
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
      "depotManifestJson",
      boundJson,
      "--argstr",
      "depotManifestSha256",
      binding.consumed_metadata_sha256,
      "--argstr",
      "juliaTestProfile",
      profile,
      ...(workers === null ? [] : [
        "--arg",
        "juliaTestWorkerLimit",
        String(workers),
      ]),
    ],
    cwd: workspace,
  });
  return binding;
}

export async function runSolverBuildCli(
  args: readonly string[],
  dependencies: Partial<BuildCliDependencies> = {},
): Promise<DepotBinding> {
  const {
    openDepotInput: open = openDepotInput,
    readSourceGraph: readGraph = sourceGraph,
    readJuliaManifestSha256: readManifest = readJuliaManifestSha256,
    execute = run,
  } = dependencies;
  const [target, ...flags] = args;
  if (!target) {
    throw new Error(
      "Usage: solver.ts build DEPOT_JSON [--profile PROFILE] [--test-workers INTEGER]",
    );
  }
  const options = parseBuildOptions(flags);
  const captured = await captureDepotMetadata(target, open);
  const graph = structuredClone(await readGraph());
  const manifest = await readManifest();
  return await buildSolver(captured, graph, manifest, (command) => execute(command), options);
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
    throw new Error(
      "Usage: solver.ts depot OUTPUT_DIRECTORY [--url URL] | build DEPOT_JSON [--profile PROFILE] [--test-workers INTEGER]",
    );
  }
  if (operation === "build") {
    await runSolverBuildCli([target, ...flags]);
    return;
  }
  const graph = await sourceGraph();
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
