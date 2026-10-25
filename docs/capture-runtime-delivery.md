# Immutable optional capture runtime

Platform `nix/application.nix` selects a Results-only virtual environment from
its existing PythonSet and uv.lock and exports it as application passthru
`captureRuntime`. Root `flake.nix::lib.mkSolver` passes its exact immutable
`bin/qcl-negf-results` path to Runner's optional `captureExecutable` argument.
No additional package resolver, service or binding file is involved. The solver
references the capture environment; application passthru does not make the full
API/AiiDA/frontend application output a solver dependency.

The Runner public wrapper owns command routing: an ordinary `run-plan` with a
trusted capture spec may call Results `capture-run`, targeting the internal Julia
wrapper. Other commands and B0 use the ordinary path. Missing capture capability
before spawn permits one ordinary Julia spawn; capture failure after spawn never
retries Julia. This wiring does not establish that the runtime or wrapper works.

`tests/capture_runtime_eval.nix` returns actual application, capture and solver
derivation paths, and checks the capture executable's immutable Nix string
context. A later approved evaluation supplies the local flake and an existing
prepared depot without realizing either. Inspect the recursive derivation graph
for capture: it must contain Results and Contracts and exclude the full returned
application derivation, qcl-negf-api, aiida-qcl-negf and qcl-negf-portal-static.
Inspect solver's graph to confirm the actual capture derivation is a dependency.
These graph checks are separate from building or invoking the runtime. They have
not been performed by this source change.

The existing Platform API unit sets `RestrictNamespaces=true`, retaining User
`qcl-negf`, `NoNewPrivileges=true`, current delegated cgroup and ordinary child
fork/exec. The existing infrastructure fixture checks the merged unit for APIs
with and without configurator. This source setting does not prove realized
namespace topology: an approved native DEPLOYBIND must verify effective
RestrictNamespaces, API MainPID namespaces relative to guest PID1, cgroup2 mount
root `/`, actual bound membership and readable ancestry including global root.
Record that evidence in the existing deployment receipt. Realized unit or
namespace changes require that deployment gate again. No new capability,
permission relaxation, identity file or per-request privileged helper is added.

Scientific plans, fingerprints, physics, storage byte budgets and numerical
acceptance are unchanged by these three wiring lines. Runner owns operational
capture reserve/routing, Results owns bounded observation, and AiiDA owns
provenance mapping. Their validation and native qualification remain distinct.
