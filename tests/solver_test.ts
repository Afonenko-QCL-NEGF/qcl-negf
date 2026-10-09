import { buildSolver, parseBuildOptions } from "../ops/solver.ts";
import { type Command } from "../ops/process.ts";

const revision = "a".repeat(40);
const hash = "sha256-" + btoa(String.fromCharCode(...Array(32).fill(1)));
const target = decodeURIComponent(new URL("../flake.nix", import.meta.url).pathname);

Deno.test("build resource options reject ambiguous or executable input before running commands", () => {
  assert(parseBuildOptions([]).profile === "production-build", "Default is production");
  assert(
    parseBuildOptions(["--profile", "local-debug"]).testWorkerLimit === null,
    "Debug selects its owning worker policy",
  );
  assert(
    parseBuildOptions(["--test-workers", "16"]).testWorkerLimit === 16,
    "Explicit production worker budget",
  );
  for (
    const flags of [
      ["--profile", "unknown"],
      ["--test-workers", "0"],
      ["--test-workers", "-1"],
      ["--test-workers", "1.5"],
      ["--test-workers", 'builtins.abort "bad"'],
      ["--test-workers", "9007199254740992"],
      ["--profile"],
      ["--test-workers", "16", "--test-workers", "32"],
      ["--profile", "local-debug", "--test-workers", "16"],
    ]
  ) {
    let refused = false;
    try {
      parseBuildOptions(flags);
    } catch {
      refused = true;
    }
    assert(refused, "Invalid or conflicting worker budget must be refused");
  }
});

Deno.test("explicit production worker budget reaches Nix as validated arguments", async () => {
  const commands: Command[] = [];
  await buildSolver(
    { sources: { revision }, url: "https://artifacts.example.org/depot.tar.gz", hash },
    revision,
    target,
    (command) => {
      commands.push(command);
      return Promise.resolve("");
    },
    parseBuildOptions(["--profile", "production-build", "--test-workers", "16"]),
  );
  const args = commands[0].args;
  const profile = args.indexOf("juliaTestProfile");
  const limit = args.indexOf("juliaTestWorkerLimit");
  assert(
    profile > 0 && args[profile - 1] === "--argstr" && args[profile + 1] === "production-build",
    "Profile must be explicit string data",
  );
  assert(
    limit > 0 && args[limit - 1] === "--arg" && args[limit + 1] === "16",
    "Limit must be a validated integer",
  );
});

function assert(value: boolean, message: string): void {
  if (!value) throw new Error(message);
}

Deno.test("local depot is hash-prefetched before a solver build with the matching fetchurl name", async () => {
  const commands: Command[] = [];
  const url = "file:///artifact%20directory/depot.tar.gz";
  await buildSolver({ sources: { revision }, url, hash }, revision, target, (command) => {
    commands.push(command);
    return Promise.resolve("");
  });
  assert(commands.length === 2, "Expected verified prefetch followed by solver build");
  assert(
    JSON.stringify(commands[0].args) === JSON.stringify([
      "store",
      "prefetch-file",
      "--hash-type",
      "sha256",
      "--expected-hash",
      hash,
      "--name",
      "qcl-negf-julia-depot.tar.gz",
      url,
    ]),
    "Local prefetch must retain URL and expected archive hash as separate arguments",
  );
  assert(commands[0].executable === "nix", "Prefetch must use Nix");
  assert(commands[1].args[0] === "build", "Build must follow successful prefetch");
  const depot = await Deno.readTextFile(new URL("../nix/depot.nix", import.meta.url));
  assert(
    depot.includes('name = "qcl-negf-julia-depot.tar.gz";'),
    "Nix fetchurl and prefetch must have the same output name",
  );
});

Deno.test("a rejected local depot hash prevents the solver build", async () => {
  const commands: Command[] = [];
  let failure = "";
  try {
    await buildSolver(
      { sources: { revision }, url: "file:///artifact/depot.tar.gz", hash },
      revision,
      target,
      (command) => {
        commands.push(command);
        if (command.args[0] === "store") return Promise.reject(new Error("hash mismatch"));
        return Promise.resolve("");
      },
    );
  } catch (error) {
    failure = (error as Error).message;
  }
  assert(failure === "hash mismatch", "Expected the failed prefetch to abort the operation");
  assert(commands.length === 1 && commands[0].args[0] === "store", "No build after rejection");
});

Deno.test("HTTPS depot builds keep normal fetchurl admission and source mismatch executes nothing", async () => {
  const commands: Command[] = [];
  const execute = (command: Command) => {
    commands.push(command);
    return Promise.resolve("");
  };
  const spec = { sources: { revision }, url: "https://artifacts.example.org/depot.tar.gz", hash };
  await buildSolver(spec, revision, target, execute);
  assert(commands.length === 1 && commands[0].args[0] === "build", "No local prefetch for HTTPS");
  let rejected = false;
  try {
    await buildSolver(spec, "b".repeat(40), target, execute);
  } catch {
    rejected = true;
  }
  assert(rejected && commands.length === 1, "Reject a different source before any command");
});
