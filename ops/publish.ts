import { git, githubRepository, sourceGraph } from "./git.ts";
import { type Command, display, main, run, workspace } from "./process.ts";

export interface Publication {
  repository: string;
  directory: string;
  revision: string;
}

export type Visibility = "public" | "private";
export type RepositoryState = "exists" | "absent";

export function publicationCommands(
  item: Publication,
  visibility: Visibility,
  state: RepositoryState = "absent",
): Command[] {
  const commands: Command[] = [];
  if (state === "absent") {
    commands.push({
      executable: "gh",
      args: ["repo", "create", item.repository, `--${visibility}`],
      env: { GH_HOST: "github.com" },
    });
  }
  // origin already exists. gh --source would try to add it again and can fail
  // after creating the remote repository. Push both refs atomically ourselves.
  commands.push({
    executable: "git",
    args: [
      "-C",
      item.directory,
      "push",
      "--atomic",
      "origin",
      `${item.revision}:refs/heads/main`,
      "refs/tags/v0.2.0:refs/tags/v0.2.0",
    ],
  });
  return commands;
}

export function repositoryState(
  output: string,
  exitCode: number,
  repository: string,
  visibility: Visibility,
): RepositoryState {
  const normalized = output.replaceAll("\r\n", "\n");
  const status = /^HTTP\/\d+(?:\.\d+)? ([1-5]\d{2})(?: [^\n]*)?\n/.exec(normalized);
  const boundary = normalized.indexOf("\n\n");
  if (!status || boundary < 0) {
    throw new Error(
      `No valid HTTP response for ${repository}; check GitHub authentication or connection`,
    );
  }
  const code = Number(status[1]);
  if (code !== 200 && code !== 404) {
    throw new Error(`GitHub preflight for ${repository} failed with HTTP ${code}`);
  }
  let body: unknown;
  try {
    body = JSON.parse(normalized.slice(boundary + 2));
  } catch {
    throw new Error(`Invalid GitHub API response for ${repository}`);
  }
  if (typeof body !== "object" || body === null || Array.isArray(body)) {
    throw new Error(`Invalid GitHub API response for ${repository}`);
  }
  const data = body as Record<string, unknown>;
  if (code === 404 && exitCode !== 0 && data.message === "Not Found") return "absent";
  if (code !== 200 || exitCode !== 0) {
    throw new Error(`Unconfirmed GitHub API result for ${repository}`);
  }
  if (
    typeof data.full_name !== "string" ||
    data.full_name.toLowerCase() !== repository.toLowerCase()
  ) {
    throw new Error(`GitHub returned a different repository for ${repository}`);
  }
  if (data.private !== (visibility === "private")) {
    throw new Error(
      `Existing repository ${repository} does not have requested ${visibility} visibility`,
    );
  }
  return "exists";
}

async function inspectRepository(
  item: Publication,
  visibility: Visibility,
): Promise<RepositoryState> {
  const response = await new Deno.Command("gh", {
    args: ["api", "--hostname", "github.com", "--include", `repos/${item.repository}`],
    stdin: "null",
    stdout: "piped",
    stderr: "piped",
  }).output();
  return repositoryState(
    new TextDecoder().decode(response.stdout),
    response.code,
    item.repository,
    visibility,
  );
}

if (import.meta.main) {
  await main(async () => {
    const flags = new Set(Deno.args);
    if (
      [...flags].some((flag) => !["--apply", "--public", "--private"].includes(flag)) ||
      flags.has("--public") && flags.has("--private")
    ) {
      throw new Error("Usage: deno task publish [--public|--private] [--apply]");
    }
    const visibility = flags.has("--private") ? "private" : "public";
    const graph = await sourceGraph();
    const origin = await git(workspace, ["remote", "get-url", "origin"]);
    const entries = graph.components.map((c) => ({
      repository: githubRepository(c.url),
      directory: `${workspace}/${c.path}`,
      revision: c.revision,
    }));
    entries.push({
      repository: githubRepository(origin),
      directory: workspace,
      revision: graph.revision,
    });
    if (new Set(entries.map((entry) => entry.repository.toLowerCase())).size !== entries.length) {
      throw new Error("Each component and the superproject must publish to a distinct repository");
    }
    for (const entry of entries) {
      const remote = await git(entry.directory, ["remote", "get-url", "origin"]);
      if (githubRepository(remote) !== entry.repository) {
        throw new Error(`Unexpected origin for ${entry.repository}`);
      }
      if (await git(entry.directory, ["rev-parse", "v0.2.0^{commit}"]) !== entry.revision) {
        throw new Error(`Tag v0.2.0 must identify the selected commit in ${entry.repository}`);
      }
      if (await git(entry.directory, ["branch", "--show-current"]) !== "main") {
        throw new Error(`Check out main before initial publication: ${entry.repository}`);
      }
    }
    if (!flags.has("--apply")) {
      // No remote queries during a dry run. Creation is conditional on absence
      // when applying; the printed commands show the initial-publication plan.
      for (const entry of entries) {
        for (const command of publicationCommands(entry, visibility)) console.log(display(command));
      }
      return;
    }
    await run({ executable: "gh", args: ["auth", "status", "--hostname", "github.com"] });
    // Finish all read-only preflights before creating or pushing anything.
    const states = await Promise.all(entries.map((entry) => inspectRepository(entry, visibility)));
    for (const [index, entry] of entries.entries()) {
      for (const command of publicationCommands(entry, visibility, states[index])) {
        console.log(display(command));
        await run(command);
      }
    }
  });
}
