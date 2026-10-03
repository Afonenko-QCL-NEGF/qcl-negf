import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { sourceGraph } from "../../ops/git.ts";
import { captureLabSnapshot } from "../../ops/lab_snapshot.ts";

function assert(value: unknown, message: string): asserts value {
  if (!value) throw new Error(message);
}

async function git(root: string, args: string[]): Promise<string> {
  const result = await new Deno.Command("git", {
    args: ["-c", "protocol.file.allow=always", "-C", root, ...args],
    env: { GIT_CONFIG_NOSYSTEM: "1", GIT_CONFIG_GLOBAL: "/dev/null" },
    stdin: "null",
    stdout: "piped",
    stderr: "piped",
  }).output();
  if (!result.success) throw new Error(new TextDecoder().decode(result.stderr));
  return new TextDecoder().decode(result.stdout).trimEnd();
}

async function commit(root: string, message: string): Promise<string> {
  await git(root, ["add", "--all"]);
  await git(root, [
    "-c",
    "user.name=Snapshot Test",
    "-c",
    "user.email=test@example.invalid",
    "-c",
    "commit.gpgSign=false",
    "commit",
    "--quiet",
    "-m",
    message,
  ]);
  return git(root, ["rev-parse", "HEAD"]);
}

async function fixture(action: (root: string, component: string, area: string) => Promise<void>) {
  const area = await Deno.makeTempDir({ dir: "/tmp", prefix: "qcl-lab-snapshot-test-" });
  try {
    const componentSource = join(area, "component source");
    const root = join(area, "source root");
    await Deno.mkdir(componentSource);
    await git(componentSource, ["init", "--quiet"]);
    await Deno.writeTextFile(join(componentSource, "model.jl"), "selected version one\n");
    await commit(componentSource, "initial component");
    await Deno.mkdir(root);
    await git(root, ["init", "--quiet"]);
    await Deno.writeTextFile(join(root, ".gitignore"), ".build/\n");
    await Deno.writeTextFile(join(root, "README.md"), "tracked root\n");
    await git(root, ["submodule", "add", "--quiet", componentSource, "components/QCLNEGF.jl"]);
    await git(root, [
      "config",
      "-f",
      ".gitmodules",
      "submodule.components/QCLNEGF.jl.url",
      "https://github.com/example/QCLNEGF.jl.git",
    ]);
    await commit(root, "initial integration");
    await action(root, join(root, "components/QCLNEGF.jl"), area);
  } finally {
    await Deno.remove(area, { recursive: true });
  }
}

async function rejects(action: () => Promise<unknown>, pattern: RegExp) {
  let failure = "";
  try {
    await action();
  } catch (error) {
    failure = (error as Error).message;
  }
  assert(pattern.test(failure), `Expected ${pattern}, received ${JSON.stringify(failure)}`);
}

async function absent(path: string): Promise<boolean> {
  try {
    await Deno.lstat(path);
    return false;
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) return true;
    throw error;
  }
}

Deno.test("local snapshot selects the clean component HEAD and preserves original checkout", async () => {
  await fixture(async (root, component) => {
    await sourceGraph(root);
    const rootRevision = await git(root, ["rev-parse", "HEAD"]);
    const oldComponent = await git(component, ["rev-parse", "HEAD"]);
    await Deno.writeTextFile(join(component, "model.jl"), "selected version two\n");
    const selected = await commit(component, "selected development component");
    const userFile = join(root, "private-untracked.txt");
    await Deno.writeTextFile(userFile, "user file must stay private\n");
    const originalStatus = await git(root, ["status", "--porcelain=v1", "--untracked-files=all"]);
    const originalModules = await Deno.readTextFile(join(root, ".gitmodules"));
    const result = await captureLabSnapshot(join(root, ".build/local-lab/sources"), root);
    assert(result.revision !== rootRevision, "Development composition needs its own commit");
    assert(result.sourceGraph.revision === result.revision, "Graph must name snapshot commit");
    assert(result.sourceGraph.components.length === 1, "Exactly the authoritative component");
    assert(result.sourceGraph.components[0].revision === selected, "Use actual clean HEAD");
    assert(
      result.sourceGraph.components[0].revision !== oldComponent,
      "Do not restore stale gitlink",
    );
    assert(
      await git(result.repository, ["rev-parse", "HEAD"]) === result.revision,
      "Committed root",
    );
    assert(
      await git(result.repository, ["status", "--porcelain"]) === "",
      "Clean snapshot checkout",
    );
    assert(
      await Deno.readTextFile(join(result.repository, "components/QCLNEGF.jl/model.jl")) ===
        "selected version two\n",
      "Materialized exact selected component",
    );
    assert(
      await absent(join(result.repository, "private-untracked.txt")),
      "Do not copy user files",
    );
    assert(
      await Deno.readTextFile(userFile) === "user file must stay private\n",
      "Preserve user file",
    );
    assert(await git(root, ["rev-parse", "HEAD"]) === rootRevision, "Original HEAD unchanged");
    assert(
      await git(root, ["status", "--porcelain=v1", "--untracked-files=all"]) === originalStatus,
      "Original status unchanged",
    );
    assert(
      await Deno.readTextFile(join(root, ".gitmodules")) === originalModules,
      "Original gitmodule URLs unchanged",
    );
    const evidence = JSON.parse(await Deno.readTextFile(result.evidence));
    assert(evidence.original_revision === rootRevision, "Capture original root provenance");
    assert(evidence.components[0].revision === selected, "Capture selected component provenance");
    assert(evidence.snapshot_revision === result.revision, "Evidence names committed snapshot");
    await rejects(() => sourceGraph(result.repository), /public HTTPS GitHub repository URL/);
  });
});

Deno.test("snapshot remains cloneable with submodules after original repositories disappear", async () => {
  await fixture(async (root, _component, area) => {
    const result = await captureLabSnapshot(join(root, ".build/local-lab/sources"), root);
    const copiedRepo = new URL(result.sourceGraph.components[0].url);
    const bare = decodeURIComponent(copiedRepo.pathname);
    const blob = await git(_component, ["rev-parse", "HEAD:model.jl"]);
    const originalGit = await git(_component, ["rev-parse", "--absolute-git-dir"]);
    const originalObject = await Deno.stat(
      join(originalGit, "objects", blob.slice(0, 2), blob.slice(2)),
    );
    const copiedObject = await Deno.stat(join(bare, "objects", blob.slice(0, 2), blob.slice(2)));
    assert(originalObject.ino !== copiedObject.ino, "Object copies must not use hardlinks");
    await Deno.remove(join(root, "components"), { recursive: true });
    await Deno.remove(join(root, ".git/modules"), { recursive: true });
    await Deno.remove(join(area, "component source"), { recursive: true });
    assert(await absent(join(bare, "objects/info/alternates")), "No shared object alternates");
    assert(
      await absent(join(result.repository, ".git/objects/info/alternates")),
      "Root is independent",
    );
    const clone = join(area, "consumer clone");
    await git(area, [
      "clone",
      "--quiet",
      "--no-hardlinks",
      "--recurse-submodules",
      pathToFileURL(result.repository).href,
      clone,
    ]);
    assert(
      await git(clone, ["rev-parse", "HEAD"]) === result.revision,
      "Fetch exact snapshot commit",
    );
    assert(
      await Deno.readTextFile(join(clone, "components/QCLNEGF.jl/model.jl")) ===
        "selected version one\n",
      "Copied object store survives source loss",
    );
  });
});

Deno.test("snapshot rejects dirty tracked root code before creating destination", async () => {
  await fixture(async (root) => {
    await Deno.writeTextFile(join(root, "README.md"), "dirty code\n");
    const destination = join(root, ".build/local-lab/sources");
    await rejects(() => captureLabSnapshot(destination, root), /tracked root changes/);
    assert(await absent(destination), "Fail before any private source capture");
  });
});

for (const kind of ["tracked", "untracked"] as const) {
  Deno.test(`snapshot rejects ${kind} dirty component files`, async () => {
    await fixture(async (root, component) => {
      await Deno.writeTextFile(
        join(component, kind === "tracked" ? "model.jl" : "untracked.txt"),
        "not a committed input\n",
      );
      const destination = join(root, ".build/local-lab/sources");
      await rejects(() => captureLabSnapshot(destination, root), /dirty component/);
      assert(await absent(destination), "Dirty component must not be captured");
    });
  });
}

Deno.test("snapshot refuses destination collision without deleting existing data", async () => {
  await fixture(async (root) => {
    const destination = join(root, ".build/local-lab/sources");
    await Deno.mkdir(destination, { recursive: true });
    await Deno.writeTextFile(join(destination, "existing.txt"), "keep\n");
    await rejects(() => captureLabSnapshot(destination, root), /already exists/);
    assert(
      await Deno.readTextFile(join(destination, "existing.txt")) === "keep\n",
      "Preserve collision",
    );
  });
});

Deno.test("snapshot refuses path traversal, external destinations and component destinations", async () => {
  await fixture(async (root, component, area) => {
    await rejects(() => captureLabSnapshot(`${root}/.build/../escape`, root), /traversal/);
    await rejects(() => captureLabSnapshot(join(area, "outside"), root), /source .build/);
    await rejects(
      () => captureLabSnapshot(join(component, ".build/snapshot"), root),
      /source .build|component/,
    );
  });
});

Deno.test("snapshot rejects a symlinked destination parent", async () => {
  await fixture(async (root, _component, area) => {
    const outside = join(area, "outside");
    await Deno.mkdir(outside);
    await Deno.symlink(outside, join(root, ".build"));
    await rejects(
      () => captureLabSnapshot(join(root, ".build/local-lab/sources"), root),
      /symlink/,
    );
    assert(await absent(join(outside, "local-lab")), "Do not write through symlink");
  });
});

Deno.test("snapshot explicitly rejects unsupported recursive gitlinks", async () => {
  await fixture(async (root, component) => {
    const revision = await git(component, ["rev-parse", "HEAD"]);
    await git(component, [
      "clone",
      "--quiet",
      "--no-hardlinks",
      "--",
      component,
      join(component, "vendor/nested"),
    ]);
    await git(component, [
      "update-index",
      "--add",
      "--cacheinfo",
      `160000,${revision},vendor/nested`,
    ]);
    await git(component, [
      "-c",
      "user.name=Snapshot Test",
      "-c",
      "user.email=test@example.invalid",
      "-c",
      "commit.gpgSign=false",
      "commit",
      "--quiet",
      "-m",
      "nested gitlink",
    ]);
    await rejects(
      () => captureLabSnapshot(join(root, ".build/local-lab/sources"), root),
      /recursive.*unsupported|nested.*unsupported/i,
    );
  });
});

Deno.test("snapshot rejects a source HEAD race and removes only its own capture", async () => {
  await fixture(async (root, component) => {
    await Deno.writeTextFile(join(component, "model.jl"), "selected version two\n");
    await commit(component, "advance selected source");
    const parent = join(root, ".build/local-lab");
    const destination = join(parent, "sources");
    await Deno.mkdir(parent, { recursive: true });
    await Deno.writeTextFile(join(parent, "unrelated.txt"), "keep\n");
    const watcher = Deno.watchFs(parent);
    let mutated = false;
    const mutation = (async () => {
      for await (const event of watcher) {
        if (
          !event.paths.some((path) => path === destination || path.startsWith(destination + "/"))
        ) continue;
        await Deno.writeTextFile(join(component, "model.jl"), "racing version three\n");
        await commit(component, "source changed during capture");
        mutated = true;
        watcher.close();
        break;
      }
    })();
    try {
      await rejects(() => captureLabSnapshot(destination, root), /Source component changed during/);
      await mutation;
      assert(mutated, "Race fixture must actually advance source HEAD");
      assert(await absent(destination), "Failed capture must not publish usable evidence");
      assert(
        await Deno.readTextFile(join(parent, "unrelated.txt")) === "keep\n",
        "Preserve neighbours",
      );
      assert(
        await Deno.readTextFile(join(component, "model.jl")) === "racing version three\n",
        "Do not undo source owner changes",
      );
    } finally {
      watcher.close();
    }
  });
});

Deno.test("snapshot copies borrowed Git objects instead of inheriting source alternates", async () => {
  await fixture(async (root, component, area) => {
    const sourceGit = await git(component, ["rev-parse", "--absolute-git-dir"]);
    const externalObjects = join(area, "component source/.git/objects");
    await Deno.writeTextFile(join(sourceGit, "objects/info/alternates"), externalObjects + "\n");
    const blob = await git(component, ["rev-parse", "HEAD:model.jl"]);
    await Deno.remove(join(sourceGit, "objects", blob.slice(0, 2), blob.slice(2)));
    assert(
      await git(component, ["show", "HEAD:model.jl"]) === "selected version one",
      "Fixture must actually borrow its blob",
    );
    const result = await captureLabSnapshot(join(root, ".build/local-lab/sources"), root);
    const bare = decodeURIComponent(new URL(result.sourceGraph.components[0].url).pathname);
    assert(
      await absent(join(bare, "objects/info/alternates")),
      "No borrowed object path may remain",
    );
    await Deno.remove(join(area, "component source"), { recursive: true });
    assert(
      await git(bare, ["show", "HEAD:model.jl"]) === "selected version one",
      "Copied object must survive loss of alternate repository",
    );
  });
});

for (const replacement of ["symlink", "directory"] as const) {
  Deno.test(`snapshot refuses destination parent ${replacement} replacement during source selection`, async () => {
    await fixture(async (root, component, area) => {
      const parent = join(root, ".build/local-lab");
      const destination = join(parent, "sources");
      const previous = join(root, ".build/previous-parent");
      const outside = join(area, "outside");
      await Deno.mkdir(parent, { recursive: true });
      await Deno.mkdir(outside);
      await Deno.writeTextFile(join(outside, "keep.txt"), "foreign data\n");
      const original = Deno.lstat;
      let changed = false;
      Deno.lstat = async (path) => {
        const result = await original(path);
        // Real source selection has started, after destination preflight.
        if (path === component && !changed) {
          changed = true;
          await Deno.rename(parent, previous);
          if (replacement === "symlink") await Deno.symlink(outside, parent);
          else await Deno.mkdir(parent);
        }
        return result;
      };
      try {
        await rejects(() => captureLabSnapshot(destination, root), /symlink|location changed/);
      } finally {
        Deno.lstat = original;
      }
      assert(changed, "Regression must replace parent during source selection");
      assert(await absent(destination), "Replacement parent must receive no capture");
      assert(await absent(join(outside, "sources")), "No private Git writes outside .build");
      assert(await absent(join(previous, "sources")), "Reject before reserving output");
      assert(
        await Deno.readTextFile(join(outside, "keep.txt")) === "foreign data\n",
        "Preserve foreign data",
      );
    });
  });
}

Deno.test("snapshot rechecks destination after reservation before Git writes", async () => {
  await fixture(async (root, _component, area) => {
    const parent = join(root, ".build/local-lab");
    const destination = join(parent, "sources");
    const previous = join(root, ".build/previous-parent");
    const outside = join(area, "outside");
    await Deno.mkdir(parent, { recursive: true });
    await Deno.mkdir(join(outside, "sources"), { recursive: true });
    await Deno.writeTextFile(join(outside, "sources/keep.txt"), "foreign capture\n");
    const original = Deno.mkdir;
    let changed = false;
    Deno.mkdir = async (path, options) => {
      await original(path, options);
      if (path === destination && !changed) {
        changed = true;
        await Deno.rename(parent, previous);
        await Deno.symlink(outside, parent);
      }
    };
    try {
      await rejects(() => captureLabSnapshot(destination, root), /symlink|location changed/);
    } finally {
      Deno.mkdir = original;
    }
    assert(changed, "Regression must replace parent after reservation");
    assert(
      await absent(join(outside, "sources/components")),
      "No Git preparation in foreign output",
    );
    assert(await absent(join(outside, "sources/repository")), "No Git clone in foreign output");
    assert(
      await Deno.readTextFile(join(outside, "sources/keep.txt")) === "foreign capture\n",
      "Cleanup must preserve foreign output",
    );
  });
});
