# Architecture and repository boundaries

This document describes the implemented baseline. The proposed next-release architecture and
normative requirements are in the [current system corpus](system/README.md). Keep implementation
facts here separate from target decisions there; historical session reports do not override either.

## Source composition

The superproject contains eight direct submodules. Git gitlinks are the source authority: they
record exact component commits. Package metadata records dependency relationships; package-manager
locks record the resolved external versions. `deno task graph` derives a release source manifest
from Git rather than maintaining another list of hashes.

Recursive submodules are deliberately absent. AiiDA, results and the runner share contracts, and
the runner uses the Julia core. Nesting these dependencies under every consumer would create
duplicate checkouts and potentially different versions of the same dependency. The flat workspace
contains one selected copy of each component. `--recurse-submodules` remains the normal Git clone
command, but does not imply a nested dependency graph in this version.

The combined project is an integration workspace and release definition. It is not an additional
runtime service or a replacement engine. Each library retains its native package metadata and can
be distributed independently. Python workspace sources and Julia development paths select the
checked-out components for local work; published wheels use normal package dependencies.

## Package review

| Boundary | Decision | Reason |
| --- | --- | --- |
| Julia core / scientific runner | Separate packages and repositories | The numerical library has a useful independent lifecycle and must not require YAML, file storage, a scheduler or deployment tools |
| Julia reference / optimized methods | Separate modules within the core | They implement the same scientific contract and need coordinated oracle tests |
| AiiDA plugin / HTTP service | Separate repositories | The plugin is useful without HTTP and must not own web authentication or presentation |
| CalcJob / Parser / WorkChain / service | Separate modules in the AiiDA package | They share AiiDA entry points, provenance and one execution contract |
| FastAPI / React client | One portal repository, separate directories | The browser assets ship in the API wheel and share API/authentication compatibility |
| Results / workflow engine | Separate repositories | Saved artifacts must remain readable and exportable without a live AiiDA profile |
| Contracts / consumers | One shared contracts repository | Format definitions and validation have independent tests; duplicate schema copies are checked rather than independently edited |
| Scientific studies / solver | Separate repositories | Scientific model choices and literature inputs are data, not execution infrastructure |
| Proxmox / libvirt | Separate OpenTofu modules in platform | Providers differ while guest services and deployment conventions are shared |
| Site configuration / public platform | Private site repository | Real addresses, credentials, resource measurements and storage lifecycle are installation-specific |

## Scientific execution

The Julia core owns equations, typed physical parameters, numerical methods and in-memory solves.
The runner owns resolved plans, persistence, resource inspection and execution adapters. It invokes
the core through a one-way package dependency. AiiDA invokes the runner as an executable and checks
scientific identity and status independently of process exit status.

One execution uses one node and one threaded process. Independent executions may run on different
workers. Continuation points stay within an execution so their numerical initialization is not
lost. Slurm assigns CPU/RAM/time; it does not select scientific tolerances. A failed attempt never
silently becomes a scientifically different calculation.

Worker-local scratch reduces repeated large writes over the 1 Gbit/s link. The shared NFS directory
is the submission and result exchange location. The staging adapter owns copying and validating
results; NFS is not a backup, and a killed or unavailable worker cannot promise a final transfer.
See the runner's staging documentation for its exact failure guarantees.

## Runtime state

Controller PostgreSQL and AiiDA's file repository form one logical dataset and require coordinated
backups. NFS job directories, persistent controller state, binary caches and node-local scratch
have different retention and recovery purposes. Immutable OS images and Nix store closures do not
contain these mutable datasets. Replacing an OS image does not authorize destroying a data disk.

The portal uses one AiiDA owner thread and event loop for its profile, ORM operations and artifact
handles. This avoids implicit event-loop creation and concurrent ORM access from arbitrary HTTP
worker threads. The initial API is a single trusted team's interface, not a multitenant security
boundary.

## Verification boundaries

Git and package-lock checks establish which source and dependency versions are used. Tests establish
specific behavioral properties. Nix evaluation, OpenTofu formatting and provider initialization do
not establish that a VM booted or a cluster completed a calculation. Production acceptance includes
real VM boot, Slurm execution, cancellation, scientific failure, large artifact staging and backup
restoration on the target infrastructure.
