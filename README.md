# QCL-NEGF

An integrated, reproducible workspace for quantum-cascade transport research.
Julia computes the numerical model, AiiDA records scientific workflows, Slurm allocates resources,
and NixOS defines the machines. GitHub hosts source and workflow state; CI runs on your own runner.

## Components

Each directory below is an independent Git submodule. The superproject commit identifies the
complete compatible source set; there is no separate manually maintained source-revision lock.

| Submodule | Responsibility |
| --- | --- |
| `components/QCLNEGF.jl` | Julia scientific library: domain types, physics, numerical operators and in-memory solving |
| `components/QCLNEGFRunner.jl` | Julia scientific execution: plans, file adapters, checkpoints, CLI and local scratch staging |
| `components/qcl-negf-contracts` | Shared schemas and validation |
| `components/qcl-negf-results` | Independent reading, verification, export and visualization of results |
| `components/qcl-negf-aiida` | CalcJob, Parser, WorkChain and workflow service |
| `components/qcl-negf-portal` | Authenticated FastAPI service and its React client |
| `components/qcl-negf-research` | Scientific input catalog and literature provenance |
| `components/qcl-negf-platform` | NixOS roles, OpenTofu infrastructure and Arch host preparation |

See [architecture](docs/architecture.md), [GitHub initialization](docs/publication.md), and
[infrastructure](components/qcl-negf-platform/docs/infrastructure.md).
For existing checkouts, see [the organization transfer procedure](docs/organization-transfer.md).

## Prepare and test

After publication, clone the workspace with its component commits:

```sh
git clone --recurse-submodules https://github.com/Afonenko-QCL-NEGF/qcl-negf.git
cd qcl-negf
git submodule update --init --recursive
nix develop
deno task --cwd components/QCLNEGFRunner.jl bootstrap
export JULIA="$PWD/components/QCLNEGFRunner.jl/.build/julia/bin/julia"
deno task prepare
deno task check
deno task test
```

Nix 2.27 or newer is required for automatic submodule fetching. The flake declares
`inputs.self.submodules = true`. The development shell provides Python 3.14, Node, Deno, uv,
OpenTofu, Ansible, Git and GitHub CLI. Julia 1.13.0 is prepared separately and checksum-verified.
An existing Julia 1.13.0 installation can be selected with `JULIA` instead.

`prepare` builds the browser assets and installs the committed native environments.
`test --python`, `test --julia` and `test --infra` select the corresponding checks.
AiiDA integration tests require a normal process namespace and local process execution;
Slurm VM tests additionally require a usable Nix builder and virtualization support.
Run `nix build --no-link --no-update-lock-file .#checks.x86_64-linux.slurm-vm`
to boot the three-VM Slurm/NFS integration test. The ordinary infrastructure checks evaluate
this test definition; they do not boot its VMs.

Python uses one uv workspace and generated `uv.lock`. Julia uses the generated
`julia/Project.toml` and `julia/Manifest.toml`, with local paths to the two selected submodules.
Node, Nix and OpenTofu use their native generated locks. Git cannot replace the dependency
resolvers for PyPI, Julia registries, npm or Nixpkgs.

After editing native dependency declarations, run `deno task lock`. This invokes the native
package managers; it does not fabricate hashes or copy commit IDs by hand. Review and commit
generated changes in their owning component first, then update the superproject gitlinks and
root environment locks. Ordinary preparation and CI use locked inputs.

## Local scientific work

The core library can be cloned and used independently on Arch Linux without any server services.
Inside this workspace, run a small example using the prepared environment:

```sh
"$JULIA" --project=julia components/QCLNEGF.jl/examples/02_bdd_and_basis.jl
"$JULIA" --project=julia components/QCLNEGF.jl/examples/03_scalar_green.jl
```

The runner provides the same scientific CLI used by AiiDA. Scientific parameters are explicit;
resource limits never silently reduce the numerical model or relax convergence criteria.

## Builds and infrastructure

```sh
deno task graph
deno task release /var/lib/qcl-negf-releases --build
deno task solver:depot /var/lib/qcl-negf-artifacts/julia-0.2.0
deno task solver:build /var/lib/qcl-negf-artifacts/julia-0.2.0/solver-depot.json
```

The release command checks the actual Git source graph, builds four Python wheels using the
locked build environment, retains their hashes and source provenance, and optionally builds the
Nix application. Julia has its own prepared dependency depot and Nix package, so changing the
web client does not re-prepare the numerical environment.

`solver:depot` downloads the dependencies selected by the committed Julia manifest into a fresh
depot, creates an archive and computes its hash automatically. It writes `solver-depot.json` for
the local build and private site flake. Copy this JSON into the private site repository; retain
the archive outside source control. The default artifact URL is local to the build machine.
For another builder, pass `--url https://YOUR-ARTIFACT-SERVER/depot.tar.gz` and upload the generated
archive to that exact address through your artifact storage. The command itself does not upload.

The primary Proxmox host runs storage, control, compute and isolated CI VMs. The existing Arch
server hosts an additional NixOS worker through QEMU/KVM and libvirt; Arch is retained.
Main NFS storage is on the primary Proxmox host in a dedicated NixOS storage VM. Worker scratch
is local. The initial Arch worker uses 30 GiB RAM and 12 vCPUs out of a 32 GiB, 12-logical-CPU
host; these are configurable caps, not a claim that SMT threads are physical cores.

Keep real host addresses, credentials, disk choices and application state outside this public
workspace. Use the platform's private-site example and its image/provisioning commands.
The source repository never contains generated VM images, dependency depots or scientific results.

MIT license. See [CONTRIBUTING.md](CONTRIBUTING.md).
