import { sourceGraph } from "./git.ts";
import { frontendBuild } from "./environment.ts";
import { main, run, workspace } from "./process.ts";

export async function sha256(bytes: Uint8Array): Promise<string> {
  return Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes as BufferSource)))
    .map((x) => x.toString(16).padStart(2, "0")).join("");
}

if (import.meta.main) {
  await main(async () => {
    const [destination, ...flags] = Deno.args;
    if (!destination || flags.some((flag) => flag !== "--build")) {
      throw new Error("Usage: deno task release RELEASE_DIRECTORY [--build]");
    }
    const graph = await sourceGraph();
    await Deno.mkdir(destination, { recursive: true });
    const root = await Deno.realPath(destination);
    const temporary = await Deno.makeTempDir({ dir: root, prefix: ".assembling-" });
    let retained = false;
    try {
      await frontendBuild();
      await run({
        executable: "uv",
        args: ["sync", "--locked", "--all-packages", "--all-extras", "--all-groups"],
        cwd: workspace,
      });
      await run({
        executable: "uv",
        args: [
          "build",
          "--all-packages",
          "--wheel",
          "--no-build-isolation",
          "--no-sources",
          "--out-dir",
          `${temporary}/wheels`,
        ],
        cwd: workspace,
      });
      const files: string[] = [];
      for await (const entry of Deno.readDir(`${temporary}/wheels`)) {
        // uv creates its own output-directory ignore marker alongside artifacts.
        if (entry.isFile && entry.name === ".gitignore") {
          await Deno.remove(`${temporary}/wheels/.gitignore`);
          continue;
        }
        if (!entry.isFile || !entry.name.endsWith(".whl")) {
          throw new Error("Unexpected wheel output");
        }
        files.push(entry.name);
      }
      if (files.length !== 4) {
        throw new Error("The application release must contain four Python wheels");
      }
      const wheels = [];
      for (const file of files.sort()) {
        wheels.push({
          file,
          sha256: await sha256(await Deno.readFile(`${temporary}/wheels/${file}`)),
        });
      }
      if (JSON.stringify(await sourceGraph()) !== JSON.stringify(graph)) {
        throw new Error("The Git source graph changed while building");
      }
      const manifest =
        JSON.stringify({ format: "qcl-negf.release.v2", sources: graph, wheels }, null, 2) + "\n";
      const identity = await sha256(new TextEncoder().encode(manifest));
      await Deno.writeTextFile(`${temporary}/release.json`, manifest);
      await Deno.writeTextFile(
        `${temporary}/README.md`,
        `# QCL-NEGF application release\n\nSource superproject: https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/${graph.revision}\n\n` +
          "The superproject Git tree pins all component commits. Its native package-manager locks pin external dependencies. " +
          "The wheels carry the Python application and frontend. They do not include Julia, NixOS images or external Python packages.\n\n" +
          `Build the Nix application from the published source with:\n\n\`\`\`sh\nnix build 'git+https://github.com/Afonenko-QCL-NEGF/qcl-negf?rev=${graph.revision}&submodules=1#application'\n\`\`\`\n`,
      );
      const final = `${root}/${identity}`;
      await Deno.rename(temporary, final);
      retained = true;
      console.log(`Retained application release: ${final}`);
      if (flags.includes("--build")) {
        await run({
          executable: "nix",
          args: [
            "build",
            "--no-link",
            "--print-out-paths",
            "--no-update-lock-file",
            ".#application",
          ],
          cwd: workspace,
        });
      }
    } finally {
      if (!retained) await Deno.remove(temporary, { recursive: true });
    }
  });
}
