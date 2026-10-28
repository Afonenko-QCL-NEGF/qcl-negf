import { pathToFileURL } from "node:url";
// Explicit native capture/finalize. Capture is not usable depot metadata.
import {
  canonicalInputs,
  type DepotInputs,
  digest,
  exact,
  hex,
  nixDataApplication,
  record,
  validateInputs,
} from "./depot_compatibility.ts";
import {
  canonicalSourceGraphJson,
  captureDepotMetadata,
  decodeDepotJson,
  parseBuildOptions,
  prepareDepotMetadata,
  readDepotInputs,
  solverBuildOutput,
} from "./solver.ts";
import { type SourceGraph, sourceGraph } from "./git.ts";
import { type Command, run, workspace } from "./process.ts";
export interface NativeFacts {
  observed_platform: string;
  preferences_sha256: string;
  selector_closure_sha256: string;
  artifact_selection_sha256: string;
}
interface Candidate {
  schema: string;
  sources: SourceGraph;
  inputs: DepotInputs;
  juliaManifest: string;
  url: string;
  hash: string;
  native_facts: NativeFacts;
}
const rel = (p: unknown): p is string =>
  typeof p === "string" && /^[A-Za-z0-9_.+/-]{1,240}$/.test(p) &&
  p.split("/").every((x) => !["", ".", ".."].includes(x));
function facts(v: unknown): asserts v is NativeFacts {
  exact(v, [
    "observed_platform",
    "preferences_sha256",
    "selector_closure_sha256",
    "artifact_selection_sha256",
  ]);
  if (
    typeof v.observed_platform !== "string" || !/^[!-~]{1,1024}$/.test(v.observed_platform) ||
    ![v.preferences_sha256, v.selector_closure_sha256, v.artifact_selection_sha256].every(hex)
  ) throw Error("Invalid native observations");
}
export async function checkQualification(
  q: unknown,
  raw: string,
  inputSha: string,
  native: NativeFacts,
  review: string,
) {
  exact(q, ["schema", "candidate_sha256", "inputs_sha256", "native_facts_sha256", "source_review"]);
  exact(q.source_review, ["path", "bytes", "sha256"]);
  if (
    q.schema !== "qcl-negf.julia-depot-qualification.v1" ||
    q.candidate_sha256 !== await digest(raw) || q.inputs_sha256 !== inputSha ||
    q.native_facts_sha256 !== await digest(canonicalInputs(native)) || !rel(q.source_review.path) ||
    q.source_review.bytes !== new TextEncoder().encode(review).length ||
    q.source_review.bytes === 0 || q.source_review.sha256 !== await digest(review)
  ) throw Error("Qualification does not bind exact candidate/facts/SOURCE evidence");
}
export async function finalizeCandidate(
  raw: string,
  qualification: string,
  review: string,
  expectedGraph: SourceGraph,
  expectedInputs: DepotInputs,
) {
  const value = decodeDepotJson(raw);
  exact(value, ["schema", "sources", "inputs", "juliaManifest", "url", "hash", "native_facts"]);
  if (value.schema !== "qcl-negf.julia-depot-candidate.v1") {
    throw Error("Not a raw native candidate");
  }
  validateInputs(value.inputs);
  facts(value.native_facts);
  canonicalSourceGraphJson(value.sources as SourceGraph);
  if (canonicalInputs(value.inputs) !== canonicalInputs(expectedInputs)) {
    throw Error("Finalize CURRENT dependency inputs differ");
  }
  const c = value as unknown as Candidate;
  const sha = await digest(canonicalInputs(c.inputs));
  await checkQualification(decodeDepotJson(qualification), raw, sha, c.native_facts, review);
  const metadata = {
    format: "qcl-negf.julia-depot.v2",
    sources: c.sources,
    julia: "1.13.0",
    juliaManifest: c.juliaManifest,
    url: c.url,
    hash: c.hash,
    compatibility: {
      schema: "qcl-negf.julia-depot-compatibility.v1",
      inputs: c.inputs,
      inputs_sha256: sha,
      native: {
        schema: "qcl-negf.julia-depot-native.v1",
        inputs_sha256: sha,
        julia_drv: c.inputs.julia.drv,
        julia_output: c.inputs.julia.output,
        ...c.native_facts,
        receipt_sha256: await digest(qualification),
      },
    },
  };
  await prepareDepotMetadata(
    JSON.stringify(metadata),
    expectedGraph,
    c.juliaManifest,
    expectedInputs,
  );
  return metadata;
}
// Walk an owned non-writable namespace; retain one regular FD, compare path/FD identities.
export async function readNamespace(root: string, name: string): Promise<string> {
  if (!rel(name)) throw Error("Require relative qualification reference");
  const rootInfo = await Deno.lstat(root);
  if (
    !rootInfo.isDirectory || rootInfo.isSymlink || rootInfo.mode === null ||
    (rootInfo.mode & 0o022) !== 0
  ) throw Error("Unsafe qualification namespace");
  const identities: { path: string; info: Deno.FileInfo }[] = [];
  let path = root;
  for (const part of name.split("/")) {
    path += "/" + part;
    const i = await Deno.lstat(path);
    if (i.isSymlink || i.uid !== rootInfo.uid || i.mode === null || (i.mode & 0o022) !== 0) {
      throw Error("Unsafe qualification reference");
    }
    identities.push({ path, info: i });
  }
  const last = identities.at(-1)!;
  if (!last.info.isFile || last.info.nlink !== 1) {
    throw Error("Qualification reference is not a private regular file");
  }
  const raw = await captureDepotMetadata(path, async (p) => {
    const f = await Deno.open(p, { read: true });
    const i = await f.stat();
    if (
      i.dev !== last.info.dev || i.ino !== last.info.ino || i.nlink !== 1 ||
      i.mode !== last.info.mode || i.uid !== last.info.uid
    ) {
      f.close();
      throw Error("Qualification file replaced before open");
    }
    return f;
  });
  for (const item of [{ path: root, info: rootInfo }, ...identities]) {
    const i = await Deno.lstat(item.path);
    if (
      i.dev !== item.info.dev || i.ino !== item.info.ino || i.mode !== item.info.mode ||
      i.uid !== item.info.uid || i.isSymlink ||
      (item.info.isFile &&
        (i.nlink !== 1 || i.size !== item.info.size ||
          i.mtime?.getTime() !== item.info.mtime?.getTime() ||
          i.ctime?.getTime() !== item.info.ctime?.getTime()))
    ) throw Error("Qualification namespace replaced");
  }
  return raw;
}
async function immutable(path: string, raw: string) {
  const f = await Deno.open(path, { write: true, createNew: true, mode: 0o600 });
  try {
    const bytes = new TextEncoder().encode(raw);
    let n = 0;
    while (n < bytes.length) n += await f.write(bytes.subarray(n));
    await f.sync();
  } finally {
    f.close();
  }
  const parent = await Deno.open(path.slice(0, path.lastIndexOf("/")), { read: true });
  try {
    await parent.sync();
  } finally {
    parent.close();
  }
}
export async function summarizeNative(
  raw: string,
  expected?: { project: string; depot: string },
): Promise<NativeFacts> {
  const n = decodeDepotJson(raw);
  exact(n, ["observed_platform", "preferences", "selectors", "artifacts"]);
  if (!record(n.preferences) || !Array.isArray(n.selectors) || !Array.isArray(n.artifacts)) {
    throw Error("Malformed raw native facts");
  }
  exact(n.preferences, ["packages", "environment"]);
  if (!record(n.preferences.packages)) throw Error("Missing measured package preferences");
  const env = n.preferences.environment;
  exact(env, ["load_path", "depot_path", "active_project", "manifest", "cpu_target"]);
  if (
    canonicalInputs(env.load_path) !== '["@","@stdlib"]' || !Array.isArray(env.depot_path) ||
    env.depot_path.length !== 1 || typeof env.depot_path[0] !== "string" ||
    !env.depot_path[0].startsWith("/") || typeof env.active_project !== "string" ||
    !/^\/nix\/store\/[0-9abcdfghijklmnpqrsvwxyz]{32}-[A-Za-z0-9+._-]+\/julia\/Project.toml$/.test(
      env.active_project,
    ) || env.manifest !== env.active_project.replace(/Project.toml$/, "Manifest.toml") ||
    env.cpu_target !== "generic" ||
    (expected && (env.active_project !== expected.project || env.depot_path[0] !== expected.depot))
  ) throw Error("Native effective environment differs from isolated profile");
  for (const row of n.selectors) {
    exact(row, ["uuid", "tree", "artifacts_file", "selector_sha256", "augmentation_sha256"]);
    if (
      typeof row.uuid !== "string" ||
      !(row.tree === null || typeof row.tree === "string" && /^[a-f0-9]{40}$/.test(row.tree)) ||
      !["JuliaArtifacts.toml", "Artifacts.toml"].includes(String(row.artifacts_file)) ||
      ![row.selector_sha256, row.augmentation_sha256].every((v) => v === null || hex(v))
    ) throw Error("Invalid selector closure observation");
  }
  for (const row of n.artifacts) {
    exact(row, ["uuid", "tree", "artifact", "artifact_tree", "platform", "selection"]);
    if (
      typeof row.uuid !== "string" ||
      !(row.tree === null || typeof row.tree === "string" && /^[a-f0-9]{40}$/.test(row.tree)) ||
      typeof row.artifact !== "string" || row.artifact.length === 0 ||
      typeof row.artifact_tree !== "string" || !/^[a-f0-9]{40}$/.test(row.artifact_tree) ||
      row.platform !== n.observed_platform || !record(row.selection) ||
      Object.hasOwn(row.selection, "download")
    ) throw Error("Invalid selected artifact observation");
  }
  const out = {
    observed_platform: n.observed_platform,
    preferences_sha256: await digest(canonicalInputs(n.preferences)),
    selector_closure_sha256: await digest(canonicalInputs(n.selectors)),
    artifact_selection_sha256: await digest(canonicalInputs(n.artifacts)),
  };
  facts(out);
  return out;
}
export async function runDepotV2(
  target: string,
  flags: string[],
  execute: (c: Command, capture?: boolean) => Promise<string> = run,
  dependencies: {
    readGraph?: () => Promise<SourceGraph>;
    readInputs?: (
      graph: SourceGraph,
      options: ReturnType<typeof parseBuildOptions>,
    ) => Promise<DepotInputs>;
  } = {},
) {
  let url: string | undefined, qualification: string | undefined;
  const buildFlags: string[] = [];
  for (let i = 0; i < flags.length; i += 2) {
    const [k, v] = flags.slice(i, i + 2);
    if (v === undefined) throw Error("Missing depot option");
    if (k === "--url" && url === undefined) url = v;
    else if (k === "--qualification" && qualification === undefined) qualification = v;
    else buildFlags.push(k, v);
  }
  const options = parseBuildOptions(buildFlags);
  const readGraph = dependencies.readGraph ?? sourceGraph;
  const readInputs = dependencies.readInputs ?? readDepotInputs;
  // Readers may return shared state and retain/mutate their arguments. Capture
  // owned evidence immediately, and give callbacks separate argument objects.
  const graph = structuredClone(await readGraph());
  const inputs = structuredClone(
    await readInputs(structuredClone(graph), structuredClone(options)),
  );
  validateInputs(inputs);
  const source = pathToFileURL(workspace + "/");
  source.searchParams.set("rev", graph.revision);
  source.searchParams.set("submodules", "1");
  const args = [
    "--argstr",
    "source",
    `git+${source.href}`,
    "--argstr",
    "juliaTestProfile",
    options.profile,
    ...(options.testWorkerLimit === null
      ? []
      : ["--arg", "juliaTestWorkerLimit", String(options.testWorkerLimit)]),
  ];
  if (qualification !== undefined) {
    const targetInfo = await Deno.lstat(target);
    if (!targetInfo.isDirectory || targetInfo.isSymlink) {
      throw Error("Qualification output must be a real directory");
    }
    const root = await Deno.realPath(target);
    const raw = await readNamespace(root, "depot-candidate.json");
    const q = await readNamespace(root, qualification);
    const parsed = decodeDepotJson(q);
    if (!record(parsed) || !record(parsed.source_review) || !rel(parsed.source_review.path)) {
      throw Error("Missing SOURCE review reference");
    }
    const review = await readNamespace(root, parsed.source_review.path);
    const candidate = decodeDepotJson(raw) as unknown as Candidate;
    if (url !== undefined) throw Error("Finalize preserves original archive URL");
    const native = await summarizeNative(await readNamespace(root, "native-facts.json"));
    if (canonicalInputs(native) !== canonicalInputs(candidate.native_facts)) {
      throw Error("Native capture changed");
    }
    const before = await Deno.lstat(root + "/depot.tar.gz");
    const owner = await Deno.lstat(root);
    if (
      !before.isFile || before.isSymlink || before.nlink !== 1 || before.uid !== owner.uid ||
      before.mode === null || (before.mode & 0o022) !== 0
    ) throw Error("Unsafe original archive");
    const archive = await execute({
      executable: "nix",
      args: ["hash", "file", "--type", "sha256", "--sri", root + "/depot.tar.gz"],
    }, true);
    const after = await Deno.lstat(root + "/depot.tar.gz");
    if (
      after.dev !== before.dev || after.ino !== before.ino || after.size !== before.size ||
      after.mode !== before.mode || after.uid !== before.uid || after.nlink !== 1 ||
      after.isSymlink ||
      after.mtime?.getTime() !== before.mtime?.getTime() ||
      after.ctime?.getTime() !== before.ctime?.getTime()
    ) throw Error("Original archive changed during hash");
    if (archive !== candidate.hash) throw Error("Original archive bytes changed");
    const metadata = await finalizeCandidate(raw, q, review, graph, inputs);
    if (canonicalSourceGraphJson(await readGraph()) !== canonicalSourceGraphJson(graph)) {
      throw Error("Selected source changed during finalize");
    }
    await immutable(root + "/solver-depot.json", JSON.stringify(metadata, null, 2) + "\n");
    return;
  }
  if (url !== undefined) {
    const u = new URL(url);
    if (
      !["http:", "https:"].includes(u.protocol) || u.username || u.password ||
      Array.from(url).some((c) => c.charCodeAt(0) <= 32 || c.charCodeAt(0) === 127)
    ) throw Error("Unsafe publication URL");
  }
  await Deno.mkdir(target, { mode: 0o700 });
  const output = await Deno.realPath(target);
  await Deno.mkdir(output + "/depot", { mode: 0o700 });
  await Deno.mkdir(output + "/home", { mode: 0o700 });
  await Deno.mkdir(output + "/tmp", { mode: 0o700 });
  const actual = solverBuildOutput(
    await execute({
      executable: "nix",
      args: ["build", "--no-link", "--json", "--file", "nix/depot-julia.nix", ...args],
      cwd: workspace,
    }, true),
  );
  if (actual.drv_path !== inputs.julia.drv || actual.output_path !== inputs.julia.output) {
    throw Error("Realized Julia differs from selected pinned factory");
  }
  const projectRaw = await execute({
    executable: "nix",
    args: [
      "eval",
      "--offline",
      "--json",
      "--file",
      "nix/depot-project.nix",
      "--apply",
      nixDataApplication({ source: `git+${source.href}` }),
    ],
    cwd: workspace,
  }, true);
  const project = decodeDepotJson(projectRaw);
  exact(project, ["source", "caBundle"]);
  const selected = project.source;
  if (
    typeof project.caBundle !== "string" ||
    !/^\/nix\/store\/[0-9abcdfghijklmnpqrsvwxyz]{32}-[A-Za-z0-9+._-]+\/etc\/ssl\/certs\/ca-bundle.crt$/
      .test(project.caBundle)
  ) throw Error("Require selected immutable CA bundle");
  if (
    typeof selected !== "string" ||
    !/^\/nix\/store\/[0-9abcdfghijklmnpqrsvwxyz]{32}-[A-Za-z0-9+._-]+$/.test(selected)
  ) {
    throw Error("Selected project must be immutable store source");
  }
  await execute({
    executable: inputs.julia.output + "/bin/julia",
    args: [
      "--startup-file=no",
      "--project=" + selected + "/julia",
      selected + "/components/QCLNEGFRunner.jl/tools/prepare_depot.jl",
      "--facts",
      output + "/native-facts.json",
    ],
    cwd: selected,
    clearEnv: true,
    env: {
      HOME: output + "/home",
      TMPDIR: output + "/tmp",
      PATH: inputs.julia.output + "/bin",
      JULIA_SSL_CA_ROOTS_PATH: project.caBundle,
      JULIA_LOAD_PATH: "@:@stdlib",
      JULIA_DEPOT_PATH: output + "/depot",
      JULIA_CPU_TARGET: "generic",
      JULIA_PKG_PRECOMPILE_AUTO: "0",
      OPENBLAS_NUM_THREADS: "1",
    },
  });
  const native = await summarizeNative(await readNamespace(output, "native-facts.json"), {
    project: selected + "/julia/Project.toml",
    depot: output + "/depot",
  });
  for (const name of ["compiled", "logs", "scratchspaces"]) {
    try {
      await Deno.remove(output + "/depot/" + name, { recursive: true });
    } catch (e) {
      if (!(e instanceof Deno.errors.NotFound)) throw e;
    }
  }
  if (canonicalSourceGraphJson(await readGraph()) !== canonicalSourceGraphJson(graph)) {
    throw Error("Selected source changed during prepare");
  }
  await execute({
    executable: "tar",
    args: [
      "--sort=name",
      "--mtime=@0",
      "--owner=0",
      "--group=0",
      "--numeric-owner",
      "-czf",
      output + "/depot.tar.gz",
      "-C",
      output + "/depot",
      ".",
    ],
  });
  await Deno.chmod(output + "/depot.tar.gz", 0o600);
  const archiveHash = await execute({
    executable: "nix",
    args: ["hash", "file", "--type", "sha256", "--sri", output + "/depot.tar.gz"],
  }, true);
  const manifest = inputs.files.find((f) => f.path === "julia/Manifest.toml")?.sha256;
  if (!manifest) throw Error("Missing frozen native Manifest binding");
  await immutable(
    output + "/depot-candidate.json",
    JSON.stringify(
      {
        schema: "qcl-negf.julia-depot-candidate.v1",
        sources: graph,
        inputs,
        juliaManifest: manifest,
        url: url ?? pathToFileURL(output + "/depot.tar.gz").href,
        hash: archiveHash,
        native_facts: native,
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    "Native candidate captured; SOURCE qualification/finalize required, no usable v2 metadata emitted.",
  );
}
