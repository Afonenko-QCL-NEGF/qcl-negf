// Development composition only. Public release sourceGraph keeps its HTTPS,
// committed-gitlink and clean-checkout guards; it intentionally rejects this
// snapshot's private file URLs. Git commits, not an additional revision lock,
// are the authority for the captured composition.
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";
import { githubRepository, gitlinks, type SourceGraph } from "./git.ts";
import { main, workspace } from "./process.ts";

export interface LabSnapshot {
  repository: string;
  evidence: string;
  revision: string;
  sourceGraph: SourceGraph;
}

interface GitState {
  revision: string;
  status: string;
}

interface SelectedComponent extends GitState {
  path: string;
  section: string;
  originalUrl: string;
}

async function command(root: string, args: string[]): Promise<string> {
  const result = await new Deno.Command("git", {
    args: [
      "-c",
      "core.hooksPath=/dev/null",
      "-c",
      "core.fsmonitor=false",
      "-c",
      "commit.gpgSign=false",
      "-C",
      root,
      ...args,
    ],
    env: { GIT_CONFIG_NOSYSTEM: "1", GIT_CONFIG_GLOBAL: "/dev/null" },
    stdin: "null",
    stdout: "piped",
    stderr: "piped",
  }).output();
  if (!result.success) {
    throw new Error(
      `Local snapshot Git command failed: ${new TextDecoder().decode(result.stderr).trim()}`,
    );
  }
  return new TextDecoder().decode(result.stdout).trimEnd();
}

async function state(root: string): Promise<GitState> {
  return {
    revision: await command(root, ["rev-parse", "HEAD"]),
    status: await command(root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]),
  };
}

async function noSymlinks(path: string): Promise<void> {
  let current = isAbsolute(path) ? sep : "";
  for (const part of path.split(sep).filter(Boolean)) {
    current = join(current, part);
    try {
      if ((await Deno.lstat(current)).isSymlink) {
        throw new Error(`Local snapshot path contains a symlink: ${current}`);
      }
    } catch (error) {
      if (error instanceof Deno.errors.NotFound) return;
      throw error;
    }
  }
}

async function destinationPath(destination: string, root: string): Promise<string> {
  if (!destination || destination.split(/[\\/]/).some((part) => part === "..")) {
    throw new Error("Local snapshot destination must not contain path traversal");
  }
  const path = resolve(root, destination);
  const belowBuild = relative(join(root, ".build"), path);
  if (
    !belowBuild || belowBuild === ".." || belowBuild.startsWith(`..${sep}`) ||
    isAbsolute(belowBuild)
  ) {
    throw new Error("Local snapshot destination must be inside the source .build directory");
  }
  await noSymlinks(path);
  try {
    await Deno.lstat(path);
    throw new Error("Local snapshot destination already exists");
  } catch (error) {
    if (!(error instanceof Deno.errors.NotFound)) throw error;
  }
  // The private repositories and evidence must never become root untracked data.
  await command(root, ["check-ignore", "--", relative(root, path)]);
  return path;
}

async function selections(root: string, initial: GitState): Promise<SelectedComponent[]> {
  const links = gitlinks(await command(root, ["ls-tree", "-rz", initial.revision]));
  const allowed = new Set(links.map((link) => link.path));
  const entries = initial.status.split("\0").filter(Boolean);
  for (const entry of entries) {
    if (entry.startsWith("?? ")) continue;
    if (!/^[ M]{2} /.test(entry) || !allowed.has(entry.slice(3))) {
      throw new Error("Local snapshot rejects tracked root changes other than selected gitlinks");
    }
  }
  await noSymlinks(join(root, ".gitmodules"));
  const configured = await command(root, [
    "config",
    "-f",
    ".gitmodules",
    "--get-regexp",
    "^submodule\\..*\\.path$",
  ]);
  const sections = new Map<string, string>();
  for (const line of configured.split("\n")) {
    const match = /^(submodule\..+)\.path (components\/[A-Za-z0-9][A-Za-z0-9.-]*)$/.exec(line);
    if (!match || sections.has(match[2]) || !allowed.has(match[2])) {
      throw new Error("Local snapshot requires safe authoritative .gitmodules paths and gitlinks");
    }
    sections.set(match[2], match[1]);
  }
  if (sections.size !== links.length) {
    throw new Error("Local snapshot .gitmodules and committed gitlinks disagree");
  }
  const selected: SelectedComponent[] = [];
  for (const link of links) {
    const component = join(root, link.path);
    await noSymlinks(component);
    if (
      !(await Deno.lstat(component)).isDirectory ||
      await command(component, ["rev-parse", "--show-toplevel"]) !== component
    ) {
      throw new Error(`Local snapshot component is not an initialized repository: ${link.path}`);
    }
    const current = await state(component);
    if (current.status) throw new Error(`Local snapshot rejects dirty component: ${link.path}`);
    const tree = await command(component, ["ls-tree", "-rz", current.revision]);
    if (tree.split("\0").some((record) => record.startsWith("160000 "))) {
      throw new Error(
        `Recursive component gitlinks are unsupported in local snapshots: ${link.path}`,
      );
    }
    const section = sections.get(link.path)!;
    const originalUrl = await command(root, [
      "config",
      "-f",
      ".gitmodules",
      "--get",
      `${section}.url`,
    ]);
    githubRepository(originalUrl);
    selected.push({ ...current, path: link.path, section, originalUrl });
  }
  return selected;
}

async function verifySources(root: string, initial: GitState, selected: SelectedComponent[]) {
  const after = await state(root);
  if (after.revision !== initial.revision || after.status !== initial.status) {
    throw new Error("Source root changed during local snapshot capture");
  }
  for (const component of selected) {
    const after = await state(join(root, component.path));
    if (after.revision !== component.revision || after.status !== component.status) {
      throw new Error(`Source component changed during local snapshot capture: ${component.path}`);
    }
  }
}

/** Capture only committed tracked inputs into a new ignored local Git composition.
 * Absolute file URLs bind the snapshot to its destination; do not relocate it.
 * Recursive component submodules are rejected explicitly, matching the flat workspace.
 */
export async function captureLabSnapshot(
  destination: string,
  root = workspace,
): Promise<LabSnapshot> {
  const source = resolve(root);
  await noSymlinks(source);
  if (
    await Deno.realPath(source) !== source ||
    await command(source, ["rev-parse", "--show-toplevel"]) !== source
  ) {
    throw new Error("Local snapshot source must be a canonical Git repository root");
  }
  const output = await destinationPath(destination, source);
  const initial = await state(source);
  const selected = await selections(source, initial);
  await Deno.mkdir(dirname(output), { recursive: true, mode: 0o700 });
  // A collision here must not be removed by cleanup: ownership starts only after
  // this non-recursive mkdir succeeds.
  await Deno.mkdir(output, { mode: 0o700 });
  try {
    const repository = join(output, "repository");
    const copied = join(output, "components");
    await Deno.mkdir(copied, { mode: 0o700 });
    await command(source, [
      "clone",
      "--quiet",
      "--no-hardlinks",
      "--dissociate",
      "--no-checkout",
      "--",
      source,
      repository,
    ]);
    await command(repository, ["checkout", "--quiet", "--detach", initial.revision]);
    await command(repository, ["remote", "remove", "origin"]);
    for (const component of selected) {
      const bare = join(copied, `${component.path.slice("components/".length)}.git`);
      await command(source, [
        "clone",
        "--quiet",
        "--bare",
        "--no-hardlinks",
        "--dissociate",
        "--",
        join(source, component.path),
        bare,
      ]);
      await command(bare, ["update-ref", "--no-deref", "HEAD", component.revision]);
      await command(bare, ["remote", "remove", "origin"]);
      const url = pathToFileURL(bare).href;
      await command(repository, ["config", "-f", ".gitmodules", `${component.section}.url`, url]);
      await command(repository, [
        "update-index",
        "--cacheinfo",
        `160000,${component.revision},${component.path}`,
      ]);
      const checkout = join(repository, component.path);
      // file:// transport prevents implicit local hardlink optimizations, and
      // --no-hardlinks also documents the independence contract for every clone.
      await command(repository, [
        "-c",
        "protocol.file.allow=always",
        "clone",
        "--quiet",
        "--no-hardlinks",
        "--dissociate",
        "--no-checkout",
        "--",
        url,
        checkout,
      ]);
      await command(checkout, ["checkout", "--quiet", "--detach", component.revision]);
    }
    await command(repository, ["add", "--", ".gitmodules"]);
    await command(repository, [
      "-c",
      "user.name=QCL-NEGF local lab",
      "-c",
      "user.email=local-lab@example.invalid",
      "commit",
      "--quiet",
      "-m",
      "Capture local development component composition",
    ]);
    const revision = await command(repository, ["rev-parse", "HEAD"]);
    if (await command(repository, ["status", "--porcelain=v1", "-z", "--untracked-files=all"])) {
      throw new Error("Captured local snapshot checkout is not clean");
    }
    const components = [];
    for (const link of gitlinks(await command(repository, ["ls-tree", "-rz", revision]))) {
      const component = selected.find((item) => item.path === link.path)!;
      const url = await command(repository, [
        "config",
        "-f",
        ".gitmodules",
        "--get",
        `${component.section}.url`,
      ]);
      if (link.revision !== component.revision) {
        throw new Error("Snapshot gitlink differs from selected source");
      }
      components.push({ ...link, url });
    }
    const sourceGraph: SourceGraph = { format: "qcl-negf.git-graph.v1", revision, components };
    await verifySources(source, initial, selected);
    const evidence = join(output, "snapshot.json");
    await Deno.writeTextFile(
      evidence,
      JSON.stringify(
        {
          schema: "qcl-negf.local-development-snapshot.v1",
          published_release: false,
          original_root: source,
          original_revision: initial.revision,
          snapshot_root: repository,
          snapshot_revision: revision,
          components: selected.map((item) => ({
            path: item.path,
            revision: item.revision,
            original_url: item.originalUrl,
          })),
          source_graph: sourceGraph,
          source_verification: "HEAD and Git status unchanged after capture",
          release_guard: "Production sourceGraph intentionally rejects private file URLs",
          relocation: "unsupported; absolute copied repository URLs are committed",
        },
        null,
        2,
      ) + "\n",
      { mode: 0o600, createNew: true },
    );
    return { repository, evidence, revision, sourceGraph };
  } catch (error) {
    await Deno.remove(output, { recursive: true });
    throw error;
  }
}

if (import.meta.main) {
  await main(async () => {
    if (Deno.args.length !== 1) throw new Error("Usage: lab_snapshot.ts DESTINATION_UNDER_BUILD");
    console.log(JSON.stringify(await captureLabSnapshot(Deno.args[0])));
  });
}
