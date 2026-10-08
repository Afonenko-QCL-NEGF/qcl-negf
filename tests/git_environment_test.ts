import { git, sourceGraph } from "../ops/git.ts";

function assert(value: boolean, message: string): void {
  if (!value) throw new Error(message);
}

async function commit(root: string): Promise<string> {
  await git(root, ["add", "--all"]);
  await git(root, [
    "-c",
    "user.name=Graph Fixture",
    "-c",
    "user.email=graph@example.invalid",
    "-c",
    "commit.gpgSign=false",
    "-c",
    "core.hooksPath=/dev/null",
    "commit",
    "--quiet",
    "-m",
    "fixture",
  ]);
  return await git(root, ["rev-parse", "HEAD"]);
}

Deno.test("source graph reads actual committed gitlinks under scoped Git permissions", async () => {
  const area = await Deno.makeTempDir({ prefix: "qcl-graph-env-" });
  try {
    const child = `${area}/components/fixture`;
    await Deno.mkdir(child, { recursive: true });
    await git(child, ["init", "--quiet"]);
    await Deno.writeTextFile(`${child}/model.txt`, "fixture metadata, no calculation\n");
    const selected = await commit(child);
    await git(area, ["init", "--quiet"]);
    await Deno.writeTextFile(
      `${area}/.gitmodules`,
      '[submodule "fixture"]\npath = components/fixture\n' +
        "url = https://github.com/example/fixture.git\n",
    );
    await git(area, ["add", ".gitmodules"]);
    await git(area, [
      "update-index",
      "--add",
      "--cacheinfo",
      `160000,${selected},components/fixture`,
    ]);
    await git(area, [
      "-c",
      "user.name=Graph Fixture",
      "-c",
      "user.email=graph@example.invalid",
      "-c",
      "commit.gpgSign=false",
      "-c",
      "core.hooksPath=/dev/null",
      "commit",
      "--quiet",
      "-m",
      "root fixture",
    ]);
    const graph = await sourceGraph(area);
    assert(graph.components.length === 1, "Expected the sole committed fixture gitlink");
    assert(
      graph.components[0].revision === selected &&
        graph.components[0].path === "components/fixture" &&
        graph.components[0].url === "https://github.com/example/fixture.git",
      "Source graph must match actual local gitlink and .gitmodules authority",
    );
  } finally {
    await Deno.remove(area, { recursive: true });
  }
});

Deno.test("Git child has explicit no-lock env without inherited loader or user config env", async () => {
  const area = await Deno.makeTempDir({ prefix: "qcl-git-env-" });
  try {
    await git(area, ["init", "--quiet"]);
    // A Git shell alias measures its actual child environment. No network,
    // credentials, mock Command or permission widening is involved.
    const output = await git(area, [
      "-c",
      "alias.qcl-environment=!printf '%s\\n' \"$GIT_OPTIONAL_LOCKS\" " +
      '"${LD_LIBRARY_PATH-unset}" "${LD_PRELOAD-unset}" ' +
      '"${DYLD_LIBRARY_PATH-unset}" "${DYLD_INSERT_LIBRARIES-unset}" ' +
      '"${HOME-unset}" "${GIT_CONFIG_GLOBAL-unset}"',
      "qcl-environment",
    ]);
    assert(output === "0\nunset\nunset\nunset\nunset\nunset\nunset", "Unexpected Git child env");
  } finally {
    await Deno.remove(area, { recursive: true });
  }
});
