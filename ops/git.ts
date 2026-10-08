import { main, run, workspace } from "./process.ts";

export interface Component {
  path: string;
  revision: string;
  url: string;
}
export interface SourceGraph {
  format: "qcl-negf.git-graph.v1";
  revision: string;
  components: Component[];
}

export function gitlinks(output: string): Array<Pick<Component, "path" | "revision">> {
  const links = [];
  for (const record of output.split("\0").filter(Boolean)) {
    const match = /^160000 commit ([a-f0-9]{40})\t(components\/[A-Za-z0-9][A-Za-z0-9.-]*)$/.exec(
      record,
    );
    if (record.startsWith("160000 ") && !match) throw new Error("Invalid component gitlink path");
    if (match) links.push({ revision: match[1], path: match[2] });
  }
  if (!links.length) throw new Error("The superproject has no committed component gitlinks");
  return links.sort((a, b) => a.path.localeCompare(b.path));
}

export function githubRepository(url: string): string {
  const match = /^https:\/\/github\.com\/([A-Za-z0-9-]+\/[A-Za-z0-9_.-]+?)(?:\.git)?$/.exec(url);
  if (!match) throw new Error(`Expected a public HTTPS GitHub repository URL: ${url}`);
  return match[1];
}

export function git(root: string, args: string[]): Promise<string> {
  return run({
    executable: "git",
    args: ["--no-optional-locks", "-C", root, ...args],
    clearEnv: true,
    env: { GIT_OPTIONAL_LOCKS: "0" },
  }, true);
}

export async function sourceGraph(root = workspace, requireClean = true): Promise<SourceGraph> {
  const revision = await git(root, ["rev-parse", "HEAD"]);
  if (!/^[a-f0-9]{40}$/.test(revision)) throw new Error("Commit the superproject first");
  if (requireClean && await git(root, ["status", "--porcelain"])) {
    throw new Error("Commit the superproject and component changes before building a release");
  }
  const configured = await git(root, [
    "config",
    "-f",
    ".gitmodules",
    "--get-regexp",
    "^submodule\\..*\\.path$",
  ]);
  const sections = new Map<string, string>();
  for (const line of configured.split("\n")) {
    const match = /^(submodule\..+)\.path (components\/[A-Za-z0-9][A-Za-z0-9.-]*)$/.exec(line);
    if (!match || sections.has(match[2])) throw new Error("Invalid or duplicate submodule path");
    sections.set(match[2], match[1]);
  }
  const components: Component[] = [];
  for (const item of gitlinks(await git(root, ["ls-tree", "-rz", "HEAD"]))) {
    const section = sections.get(item.path);
    if (!section) throw new Error(`Missing .gitmodules entry: ${item.path}`);
    const url = await git(root, ["config", "-f", ".gitmodules", "--get", `${section}.url`]);
    githubRepository(url);
    const local = `${root}/${item.path}`;
    const childTree = await git(local, ["ls-tree", "-rz", "HEAD"]);
    if (childTree.split("\0").some((record) => record.startsWith("160000 "))) {
      throw new Error(`Nested submodules are not supported in the flat source graph: ${item.path}`);
    }
    const checkedOut = await git(local, ["rev-parse", "HEAD"]);
    if (checkedOut !== item.revision) {
      throw new Error(`Submodule differs from committed gitlink: ${item.path}`);
    }
    if (requireClean && await git(local, ["status", "--porcelain"])) {
      throw new Error(`Submodule has local changes: ${item.path}`);
    }
    components.push({ ...item, url });
  }
  if (components.length !== sections.size) {
    throw new Error("Uncommitted or orphan .gitmodules entry");
  }
  return { format: "qcl-negf.git-graph.v1", revision, components };
}

if (import.meta.main) {
  await main(async () => console.log(JSON.stringify(await sourceGraph(), null, 2)));
}
