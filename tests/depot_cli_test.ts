// Exercise the real module entry point: import-only producer tests cannot detect
// a top-level-await cycle between the CLI and its dynamically imported producer.
Deno.test("depot v2 CLI reaches argument validation before native preparation", async () => {
  const target = await Deno.makeTempDir({ prefix: "qcl-depot-cli-" });
  try {
    const output = await new Deno.Command(Deno.execPath(), {
      args: [
        "run",
        "--no-prompt",
        new URL("../ops/solver.ts", import.meta.url).href,
        "depot",
        target + "/must-not-exist",
        "--format",
        "v2",
        "--test-workers",
        "invalid",
      ],
      clearEnv: true,
      stdin: "null",
      stdout: "piped",
      stderr: "piped",
    }).output();
    const stderr = new TextDecoder().decode(output.stderr);
    if (
      output.code !== 1 ||
      !stderr.includes(
        "Expected --profile production-build|local-debug or --test-workers INTEGER",
      ) ||
      stderr.includes("Top-level await promise never resolved")
    ) throw Error(`CLI did not reach v2 argument validation: ${stderr}`);
    const entries = [];
    for await (const entry of Deno.readDir(target)) entries.push(entry.name);
    if (entries.length) throw Error("Invalid options started native preparation");
  } finally {
    await Deno.remove(target, { recursive: true });
  }
});
