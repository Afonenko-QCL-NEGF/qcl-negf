# Initial Git and GitHub setup

The prepared distribution contains a real `qcl-negf` Git repository, eight initialized submodules,
`main` branches, neutral initial commits, `v0.2.0` tags and GitHub `origin` URLs. Keep its `.git`
directory and each component's `.git` file. Submodule objects are stored under the superproject's
Git directory. Copying only visible files would lose the version graph.

## Publish the prepared repositories

Git, GitHub CLI and Deno 2 must be available before publication. If using Nix to obtain them,
enter `nix develop "path:$PWD"` from the freshly unpacked workspace. This uses the included source
directories for the initial development shell. A clean Git flake with submodules resolves their
public GitHub URLs, which become available only after the initial push. After publication use
the ordinary `nix develop` and pinned Git source builds.

From the root `qcl-negf` directory, authenticate GitHub CLI and review the generated command plan:

```sh
gh auth login
git submodule status --recursive
deno task graph
deno task publish --public
```

The plan creates each component repository, pushes its `main` branch and `v0.2.0` tag, then publishes
the superproject. To execute that plan:

```sh
deno task publish --public --apply
```

The task never rewrites history or force-pushes. It validates clean working trees, exact gitlinks,
origins and tags. GitHub publication is separate from installing or activating infrastructure.
The source archive itself has not performed publication.

The underlying commands for one component are ordinary GitHub CLI and Git:

```sh
gh repo create AfonenkoA/QCLNEGF.jl --public
git -C components/QCLNEGF.jl push --atomic origin main:main refs/tags/v0.2.0:refs/tags/v0.2.0
```

After publishing all eight components, the corresponding superproject commands are:

```sh
gh repo create AfonenkoA/qcl-negf --public
git push --atomic origin main:main refs/tags/v0.2.0:refs/tags/v0.2.0
```

Do not initialize remote README, LICENSE or `.gitignore` files; those files already exist locally.
For a different owner, update each repository's origin and the superproject `.gitmodules`, commit
the changes, and create matching release tags before publishing. Standalone Julia `[sources]` URLs
also identify their distribution owner and must be updated for a permanently independent fork.

## Initialize from source directories without Git metadata

This procedure is only for a source-only export, not the prepared Git distribution. First initialize
and publish each component independently, for example:

```sh
git -C QCLNEGF.jl init -b main
git -C QCLNEGF.jl add .
git -C QCLNEGF.jl commit -m "Initial source"
git -C QCLNEGF.jl tag v0.2.0
gh repo create AfonenkoA/QCLNEGF.jl --public --source=QCLNEGF.jl --remote=origin --push
git -C QCLNEGF.jl push origin v0.2.0
```

Then initialize a new integration repository and add the eight published repositories with
`git submodule add URL components/NAME`. Select the desired commit in each submodule, run
`deno task lock` to generate native environments, and commit `.gitmodules`, gitlinks and the
generated lock files together. Reinitialization creates new commit IDs; it is not a way to preserve
the tested source identity of the supplied distribution.

## Normal development

```sh
git clone --recurse-submodules https://github.com/AfonenkoA/qcl-negf.git
cd qcl-negf
git -C components/QCLNEGF.jl switch -c experiment/operator
```

Normal submodule checkout uses detached HEAD because it selects a commit. Create a branch before
developing. Commit and push changed components first; then stage their paths in the superproject
to record new gitlinks. Run the integrated checks and commit any package-manager-generated lock
changes with the source selection. Do not use `git submodule update --remote` as a release build
step: it chooses moving branch tips rather than the committed source set.

Only the superproject needs the authoritative integration runner registration. Its workflow checks
out the recursive Git tree and builds/tests the complete selected graph. Runner credentials and
deployment credentials are separate, and infrastructure provisioning is not triggered by ordinary
source pushes.
