import { git, githubRepository, gitlinks, type GitReader, sourceGraph } from "../ops/git.ts";

function assert(value: boolean): void {
  if (!value) throw new Error("Assertion failed");
}
function rejects(action: () => unknown): void {
  let failed = false;
  try {
    action();
  } catch {
    failed = true;
  }
  assert(failed);
}

Deno.test("source graph uses Git gitlinks, not arbitrary file records", () => {
  const sha = "a".repeat(40);
  const items = gitlinks(
    `100644 blob ${sha}\tREADME.md\0` +
      `160000 commit ${sha}\tcomponents/QCLNEGF.jl\0`,
  );
  assert(items.length === 1 && items[0].revision === sha && items[0].path.endsWith(".jl"));
});
Deno.test("source graph refuses absent gitlinks and escaping paths", () => {
  rejects(() => gitlinks(""));
  rejects(() => gitlinks(`160000 commit ${"a".repeat(40)}\tcomponents/../../outside\0`));
  rejects(() => gitlinks(`160000 commit ${"a".repeat(40)}\tcomponents/a/nested\0`));
});
Deno.test("publication resolves exact HTTPS repositories", () => {
  assert(
    githubRepository("https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl.git") ===
      "Afonenko-QCL-NEGF/QCLNEGF.jl",
  );
  rejects(() => githubRepository("https://github.com/owner/repo/extra"));
  rejects(() => githubRepository("https://example.org/owner/repo"));
  rejects(() => githubRepository("https://github.com/owner/repo?token=secret"));
});

// Handwritten Git protocol; unexpected roots/argv fail rather than dispatching Git.
type Reply = readonly [root: string, args: readonly string[], output: string];
function fakeGitReader(replies: readonly Reply[]): { readGit: GitReader; done: () => void } {
  let next = 0;
  const readGit: GitReader = (root, args) =>
    new Promise<string>((resolve) => {
      const reply = replies[next++];
      if (!reply || root !== reply[0] || JSON.stringify(args) !== JSON.stringify(reply[1])) {
        throw new Error(`Unexpected Git read: ${root} ${JSON.stringify(args)}`);
      }
      resolve(reply[2]);
    });
  return { readGit, done: () => assert(next === replies.length) };
}
const fixtureRoot = "/fixture/root";
const rootRevision = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const childRevision = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";
const configuredArgs = [
  "config",
  "-f",
  ".gitmodules",
  "--get-regexp",
  "^submodule\\..*\\.path$",
] as const;
const configuredPath = "submodule.a.path components/a";
const committedTree = `160000 commit ${childRevision}\tcomponents/a\0`;
const urlArgs = ["config", "-f", ".gitmodules", "--get", "submodule.a.url"] as const;
const childRoot = "/fixture/root/components/a";

function repliesFor(options: {
  clean?: boolean;
  rootRevision?: string;
  rootStatus?: string;
  configured?: string;
  tree?: string;
  url?: string;
  childTree?: string;
  childRevision?: string;
  childStatus?: string;
} = {}): Reply[] {
  const replies: Reply[] = [[
    fixtureRoot,
    ["rev-parse", "HEAD"],
    options.rootRevision ?? rootRevision,
  ]];
  if (options.clean !== false) {
    replies.push([fixtureRoot, ["status", "--porcelain"], options.rootStatus ?? ""]);
  }
  replies.push(
    [fixtureRoot, configuredArgs, options.configured ?? configuredPath],
    [fixtureRoot, ["ls-tree", "-rz", "HEAD"], options.tree ?? committedTree],
    [fixtureRoot, urlArgs, options.url ?? "https://github.com/owner/a.git"],
    [childRoot, ["ls-tree", "-rz", "HEAD"], options.childTree ?? ""],
    [childRoot, ["rev-parse", "HEAD"], options.childRevision ?? childRevision],
  );
  if (options.clean !== false) {
    replies.push([childRoot, ["status", "--porcelain"], options.childStatus ?? ""]);
  }
  return replies;
}

async function graphRejects(replies: readonly Reply[], expected: string): Promise<void> {
  const fixture = fakeGitReader(replies);
  let error: unknown;
  try {
    await sourceGraph(fixtureRoot, true, fixture.readGit);
  } catch (caught) {
    error = caught;
  }
  assert(error instanceof Error && error.message === expected);
  fixture.done();
}

Deno.test("injected reader preserves graph JSON and raw digest including original URL", async () => {
  const fixture = fakeGitReader(repliesFor());
  const graph = await sourceGraph(fixtureRoot, true, fixture.readGit);
  fixture.done();
  const json = JSON.stringify(graph);
  assert(
    json ===
      '{"format":"qcl-negf.git-graph.v1","revision":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","components":[{"revision":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","path":"components/a","url":"https://github.com/owner/a.git"}]}',
  );
  const digest = new Uint8Array(
    await crypto.subtle.digest("SHA-256", new TextEncoder().encode(json)),
  );
  assert(
    Array.from(digest, (byte) => byte.toString(16).padStart(2, "0")).join("") ===
      "95a1af7b7d1bd04187ffa64d8b94dbd4eb0345bdd5edac06d7cceee87ada3958",
  );
});

Deno.test("injected reader skips both status reads only when requireClean is false", async () => {
  const fixture = fakeGitReader(repliesFor({ clean: false }));
  const graph = await sourceGraph(fixtureRoot, false, fixture.readGit);
  assert(graph.components.length === 1 && graph.components[0].revision === childRevision);
  fixture.done();
});

Deno.test("gitlinks retains legacy locale order for case and punctuation", () => {
  const items = gitlinks(
    `160000 commit ${childRevision}\tcomponents/a.\0` +
      `160000 commit ${childRevision}\tcomponents/a-\0` +
      `160000 commit ${childRevision}\tcomponents/A\0` +
      `160000 commit ${childRevision}\tcomponents/a\0`,
  );
  assert(
    JSON.stringify(items.map((item) => item.path)) ===
      '["components/a","components/A","components/a-","components/a."]',
  );
});

Deno.test("mixed-case graph retains legacy component order and raw digest", async () => {
  const replies: Reply[] = [
    [fixtureRoot, ["rev-parse", "HEAD"], rootRevision],
    [fixtureRoot, ["status", "--porcelain"], ""],
    [
      fixtureRoot,
      configuredArgs,
      "submodule.dot.path components/a.\nsubmodule.dash.path components/a-\nsubmodule.upper.path components/A\nsubmodule.lower.path components/a",
    ],
    [
      fixtureRoot,
      ["ls-tree", "-rz", "HEAD"],
      `160000 commit ${childRevision}\tcomponents/a.\0` +
      `160000 commit ${childRevision}\tcomponents/a-\0` +
      `160000 commit ${childRevision}\tcomponents/A\0` +
      `160000 commit ${childRevision}\tcomponents/a\0`,
    ],
  ];
  // Literal legacy traversal, deliberately different from recorded tree order.
  for (
    const [path, section, url] of [
      ["components/a", "submodule.lower", "https://github.com/owner/a.git"],
      ["components/A", "submodule.upper", "https://github.com/owner/A"],
      ["components/a-", "submodule.dash", "https://github.com/owner/a-"],
      ["components/a.", "submodule.dot", "https://github.com/owner/a."],
    ]
  ) {
    replies.push(
      [fixtureRoot, ["config", "-f", ".gitmodules", "--get", `${section}.url`], url],
      [`${fixtureRoot}/${path}`, ["ls-tree", "-rz", "HEAD"], ""],
      [`${fixtureRoot}/${path}`, ["rev-parse", "HEAD"], childRevision],
      [`${fixtureRoot}/${path}`, ["status", "--porcelain"], ""],
    );
  }
  const fixture = fakeGitReader(replies);
  const json = JSON.stringify(await sourceGraph(fixtureRoot, true, fixture.readGit));
  fixture.done();
  assert(
    json ===
      '{"format":"qcl-negf.git-graph.v1","revision":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","components":[{"revision":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","path":"components/a","url":"https://github.com/owner/a.git"},{"revision":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","path":"components/A","url":"https://github.com/owner/A"},{"revision":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","path":"components/a-","url":"https://github.com/owner/a-"},{"revision":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","path":"components/a.","url":"https://github.com/owner/a."}]}',
  );
  const digest = new Uint8Array(
    await crypto.subtle.digest("SHA-256", new TextEncoder().encode(json)),
  );
  assert(
    Array.from(digest, (byte) => byte.toString(16).padStart(2, "0")).join("") ===
      "842a16f0d2d2323eee605ccbe1f03e2c8ef7f1ec464c6ddf9d025371afcf9304",
  );
});

Deno.test("reader injection preserves revision and cleanliness guards", async () => {
  await graphRejects(
    repliesFor({ rootRevision: "uncommitted" }).slice(0, 1),
    "Commit the superproject first",
  );
  await graphRejects(
    repliesFor({ rootStatus: " M README.md" }).slice(0, 2),
    "Commit the superproject and component changes before building a release",
  );
  await graphRejects(
    repliesFor({ childStatus: " M child.jl" }),
    "Submodule has local changes: components/a",
  );
});

Deno.test("reader injection preserves missing gitlink and configuration guards", async () => {
  await graphRejects(
    repliesFor({ tree: "" }).slice(0, 4),
    "The superproject has no committed component gitlinks",
  );
  await graphRejects(
    repliesFor({ tree: `160000 commit ${childRevision}\tcomponents/../outside\0` }).slice(0, 4),
    "Invalid component gitlink path",
  );
  await graphRejects(
    repliesFor({ configured: "submodule.b.path components/b" }).slice(0, 4),
    "Missing .gitmodules entry: components/a",
  );
  await graphRejects(
    repliesFor({ configured: `${configuredPath}\nsubmodule.duplicate.path components/a` }).slice(
      0,
      3,
    ),
    "Invalid or duplicate submodule path",
  );
  await graphRejects(
    repliesFor({ configured: "not a submodule record" }).slice(0, 3),
    "Invalid or duplicate submodule path",
  );
  await graphRejects(
    repliesFor({ configured: `${configuredPath}\nsubmodule.b.path components/b` }),
    "Uncommitted or orphan .gitmodules entry",
  );
});

Deno.test("reader injection preserves URL, nested and mismatched child guards", async () => {
  await graphRejects(
    repliesFor({ url: "https://example.org/owner/a" }).slice(0, 5),
    "Expected a public HTTPS GitHub repository URL: https://example.org/owner/a",
  );
  await graphRejects(
    repliesFor({ childTree: `160000 commit ${childRevision}\tnested\0` }).slice(0, 6),
    "Nested submodules are not supported in the flat source graph: components/a",
  );
  await graphRejects(
    repliesFor({ childRevision: rootRevision }).slice(0, 7),
    "Submodule differs from committed gitlink: components/a",
  );
});

// Compile-time compatibility witnesses only; neither reference dispatches Git.
const legacySourceGraph: (root?: string, requireClean?: boolean) => ReturnType<typeof sourceGraph> =
  sourceGraph;
const defaultGitReader: GitReader = git;
void legacySourceGraph;
void defaultGitReader;
