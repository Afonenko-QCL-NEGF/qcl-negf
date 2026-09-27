import { githubRepository, gitlinks } from "../ops/git.ts";

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
