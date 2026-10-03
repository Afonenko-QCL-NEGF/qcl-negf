import { deploymentManifest, immutableStorePath } from "../ops/application_cd.ts";
import { type SourceGraph } from "../ops/git.ts";

const graph: SourceGraph = {
  format: "qcl-negf.git-graph.v1",
  revision: "a".repeat(40),
  components: [{
    path: "components/QCLNEGFRunner.jl",
    revision: "b".repeat(40),
    url: "https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl",
  }],
};
const application = "/nix/store/" + "a".repeat(32) + "-qcl-application";
const solver = "/nix/store/" + "b".repeat(32) + "-qcl-solver";
const hash = "sha256-" + btoa(String.fromCharCode(...Array(32).fill(1)));

function assert(value: boolean, message: string): void {
  if (!value) throw new Error(message);
}

Deno.test("CD binds executable identity to both source and immutable closure hashes", async () => {
  const value = await deploymentManifest(graph, application, solver, {
    [application]: { narHash: hash },
    [solver]: { narHash: hash },
  });
  assert(value.solver_executable === `${solver}/bin/qcl-negf`, "Pinned executable missing");
  assert(value.application_path === application, "Pinned application missing");
  assert(/^[a-f0-9]{64}$/.test(value.release_id), "Content identity missing");
  const another = await deploymentManifest(
    { ...graph, revision: "c".repeat(40) },
    application,
    solver,
    {
      [application]: { narHash: hash },
      [solver]: { narHash: hash },
    },
  );
  assert(value.release_id !== another.release_id, "A different source reused a release identity");
});

Deno.test("CD refuses mutable paths and missing closure evidence", async () => {
  for (const path of ["/run/current-system", "/nix/store/../mutable", application + "/bin"]) {
    let rejected = false;
    try {
      immutableStorePath(path);
    } catch {
      rejected = true;
    }
    assert(rejected, "Mutable or malformed closure was accepted");
  }
  let rejected = false;
  try {
    await deploymentManifest(graph, application, solver, { [application]: { narHash: hash } });
  } catch {
    rejected = true;
  }
  assert(rejected, "A release without solver closure evidence was accepted");
});

Deno.test("CD carries the selected cache without changing binary release identity", async () => {
  const evidence = { [application]: { narHash: hash }, [solver]: { narHash: hash } };
  const value = await deploymentManifest(
    graph,
    application,
    solver,
    evidence,
    "https://cache.example.invalid",
  );
  assert(
    value.cache_uri === "https://cache.example.invalid",
    "Controller lost the published cache",
  );
  const mirror = await deploymentManifest(
    graph,
    application,
    solver,
    evidence,
    "ssh://mirror.example.invalid",
  );
  assert(
    value.release_id === mirror.release_id,
    "Transport mirror changed the binary release identity",
  );
  for (
    const cache of [
      "",
      "--option",
      "https://cache.example.invalid/\n",
      "https://user:example-password@cache.example.invalid",
    ]
  ) {
    let rejected = false;
    try {
      await deploymentManifest(graph, application, solver, evidence, cache);
    } catch {
      rejected = true;
    }
    assert(rejected, "Malformed cache URI was accepted");
  }
});
