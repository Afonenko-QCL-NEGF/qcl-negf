import { publicationCommands, repositoryState } from "../ops/publish.ts";

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
function response(status: string, body: unknown): string {
  return `HTTP/2.0 ${status}\nContent-Type: application/json\r\n\r\n${JSON.stringify(body)}`;
}
const item = {
  repository: "Afonenko-QCL-NEGF/qcl-negf",
  directory: "/checkout with spaces/qcl-negf",
  revision: "a".repeat(40),
};

Deno.test("publication preserves origin and atomically pushes the selected commit and release tag", () => {
  const commands = publicationCommands(item, "public");
  assert(commands.length === 2);
  assert(commands[0].executable === "gh");
  assert(
    JSON.stringify(commands[0].args) ===
      JSON.stringify(["repo", "create", item.repository, "--public"]),
  );
  assert(commands[0].env?.GH_HOST === "github.com");
  assert(commands[1].executable === "git");
  assert(
    JSON.stringify(commands[1].args) === JSON.stringify([
      "-C",
      item.directory,
      "push",
      "--atomic",
      "origin",
      `${item.revision}:refs/heads/main`,
      "refs/tags/v0.2.0:refs/tags/v0.2.0",
    ]),
  );
});

Deno.test("resuming publication of an existing repository performs no creation or force push", () => {
  const commands = publicationCommands(item, "private", "exists");
  assert(commands.length === 1 && commands[0].executable === "git");
  assert(!commands[0].args.some((arg) => arg.includes("force")));
});

Deno.test("repository preflight accepts a matching successful API response", () => {
  const existing = response("200 OK", { full_name: item.repository, private: false });
  assert(repositoryState(existing, 0, item.repository, "public") === "exists");
  assert(
    repositoryState(
      response("200 OK", { full_name: item.repository, private: true }),
      0,
      item.repository,
      "private",
    ) === "exists",
  );
});

Deno.test("only an explicit GitHub API 404 permits repository creation", () => {
  assert(
    repositoryState(
      response("404 Not Found", { message: "Not Found" }),
      1,
      item.repository,
      "public",
    ) === "absent",
  );
  rejects(() => repositoryState("", 1, item.repository, "public"));
  rejects(() => repositoryState("network error: 404", 1, item.repository, "public"));
  rejects(() =>
    repositoryState(
      response("401 Unauthorized", { message: "Bad credentials" }),
      1,
      item.repository,
      "public",
    )
  );
  rejects(() =>
    repositoryState(
      response("403 Forbidden", { message: "rate limit exceeded" }),
      1,
      item.repository,
      "public",
    )
  );
  rejects(() =>
    repositoryState(response("500 Internal Server Error", {}), 1, item.repository, "public")
  );
  rejects(() =>
    repositoryState(
      "HTTP/1.1 404 Not Found\n\n<html>proxy error</html>",
      1,
      item.repository,
      "public",
    )
  );
  rejects(() =>
    repositoryState(
      response("404 Not Found", { message: "Not Found" }),
      0,
      item.repository,
      "public",
    )
  );
});

Deno.test("publication refuses wrong identity, failed API calls and visibility mismatches", () => {
  rejects(() =>
    repositoryState(
      response("200 OK", { full_name: "someone/else", private: false }),
      0,
      item.repository,
      "public",
    )
  );
  rejects(() =>
    repositoryState(
      response("200 OK", { full_name: item.repository, private: false }),
      1,
      item.repository,
      "public",
    )
  );
  rejects(() =>
    repositoryState(
      response("200 OK", { full_name: item.repository, private: false }),
      0,
      item.repository,
      "private",
    )
  );
  rejects(() =>
    repositoryState(
      response("200 OK", { full_name: item.repository }),
      0,
      item.repository,
      "public",
    )
  );
});
