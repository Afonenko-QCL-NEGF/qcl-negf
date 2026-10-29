import { git, type GitReader } from "./git.ts";
import { type Command, main, workspace } from "./process.ts";

export type ImpactGroup =
  | "docs"
  | "root"
  | "contracts"
  | "results"
  | "aiida"
  | "portal"
  | "frontend"
  | "research"
  | "core"
  | "runner"
  | "platform"
  | "infra"
  | "julia-integration"
  | "docs-build";
export interface ChangedPath {
  owner: string;
  path: string;
  oldMode: string;
  newMode: string;
}
export interface ImpactPlan {
  format: "qcl-negf.impact.v1";
  base: string | null;
  head: string | null;
  groups: ImpactGroup[];
  reasons: { owner: string; path: string; groups: ImpactGroup[]; reason: string }[];
  unknowns: string[];
  nativeGates: string[];
  scientificStage: "not_requested";
}
export interface ImpactContext {
  root: string;
  julia: string;
}
export interface ImpactOptions {
  base: string | null;
  head: string | null;
  overrides: ("full" | "python" | "julia" | "infra")[];
}
const components = {
  "components/QCLNEGF.jl": "core",
  "components/QCLNEGFRunner.jl": "runner",
  "components/qcl-negf-contracts": "contracts",
  "components/qcl-negf-results": "results",
  "components/qcl-negf-aiida": "aiida",
  "components/qcl-negf-portal": "portal",
  "components/qcl-negf-research": "research",
  "components/qcl-negf-platform": "platform",
} as const;
const python: ImpactGroup[] = ["contracts", "results", "aiida", "portal", "research"];
const numerical: ImpactGroup[] = [
  "core",
  "runner",
  "results",
  "aiida",
  "portal",
  "julia-integration",
];
const all: ImpactGroup[] = [
  ...python,
  "docs",
  "root",
  "frontend",
  "core",
  "runner",
  "platform",
  "infra",
  "julia-integration",
  "docs-build",
];
const sorted = <T extends string>(items: readonly T[]): T[] => [...new Set(items)].sort();
function pathSafe(path: string) {
  if (
    !path || path.startsWith("/") || (path.includes("\0") || /[\\\uFFFD]/.test(path)) ||
    path.split("/").some((p) => !p || p === "." || p === "..")
  ) throw Error("Unsafe impact path");
}
function refSafe(ref: string) {
  if (!ref || ref.startsWith("-") || (ref.includes("\0") || /[\s\\\uFFFD]/.test(ref))) {
    throw Error("Unsafe Git ref");
  }
}
const pyPath = (group: string) => `components/qcl-negf-${group}`;
const juliaPath = (group: string) =>
  `components/${group === "core" ? "QCLNEGF.jl" : "QCLNEGFRunner.jl"}`;
const denoCheck = (cwd: string): Command => ({ executable: "deno", args: ["task", "check"], cwd });
const pytest = (root: string, group: string, integration = false): Command => ({
  executable: "uv",
  args: [
    "run",
    "--locked",
    "--no-sync",
    "pytest",
    "-c",
    `${pyPath(group)}/pyproject.toml`,
    `${pyPath(group)}/${integration ? "integration" : "tests"}`,
  ],
  cwd: root,
});
const frontendBuild = (root: string): Command[] => [
  {
    executable: "npm",
    args: ["ci", "--ignore-scripts"],
    cwd: `${root}/${pyPath("portal")}/frontend`,
  },
  { executable: "npm", args: ["run", "build"], cwd: `${root}/${pyPath("portal")}/frontend` },
];
const uvSync = (root: string): Command => ({
  executable: "uv",
  args: ["sync", "--locked", "--all-packages", "--all-extras", "--all-groups"],
  cwd: root,
});
const backendPaths = (root: string) =>
  ["proxmox", "arch-libvirt"].map((b) => `${root}/components/qcl-negf-platform/tofu/${b}`);
interface GroupRule {
  check: (context: ImpactContext) => Command[];
  prepare: (context: ImpactContext) => Command[];
  gates: string[];
}
// One command registry is shared by the planner, test/prepare CLIs and workflow.
const registry = {} as Record<ImpactGroup, GroupRule>;
for (const group of all) registry[group] = { check: () => [], prepare: () => [], gates: [] };
registry.docs.gates = [
  "D: local links and anchors require source review; formatting is not link acceptance",
];
registry.root.check = ({ root }) => [denoCheck(root)];
for (const group of python) {
  registry[group] = {
    check: ({ root }) => [
      ...(group === "portal" ? [denoCheck(`${root}/${pyPath(group)}`)] : []),
      pytest(root, group),
      ...(group === "research"
        ? [{
          executable: "uv",
          args: ["run", "--locked", "--no-sync", "python", `${pyPath(group)}/tools/validate.py`],
          cwd: root,
        }]
        : []),
    ],
    // The coherent native workspace includes Portal's wheel build hook.
    prepare: ({ root }) => [...frontendBuild(root), uvSync(root)],
    gates: [
      "Python checks require the prepared locked workspace; wheel metadata/assets need native wheel verification",
    ],
  };
}
registry.frontend = {
  check: (
    { root },
  ) => [{ executable: "npm", args: ["test"], cwd: `${root}/${pyPath("portal")}/frontend` }],
  prepare: ({ root }) => frontendBuild(root),
  gates: ["Frontend tests require explicitly prepared locked npm dependencies"],
};
for (const group of ["core", "runner"] as const) {
  registry[group] = {
    check: ({ root, julia }) => [denoCheck(`${root}/${juliaPath(group)}`), {
      executable: julia,
      args: [
        "--startup-file=no",
        "--threads=2",
        "--check-bounds=yes",
        `--project=${root}/julia`,
        `${root}/${juliaPath(group)}/test/runtests.jl`,
      ],
      cwd: `${root}/${juliaPath(group)}`,
      env: { OPENBLAS_NUM_THREADS: "1", JULIA_NUM_PRECOMPILE_TASKS: "2" },
    }],
    prepare: ({ root, julia }) => [
      {
        executable: "deno",
        args: ["task", "bootstrap"],
        cwd: `${root}/components/QCLNEGFRunner.jl`,
      },
      {
        executable: julia,
        args: ["--startup-file=no", "--project=julia", "-e", "using Pkg; Pkg.instantiate()"],
        cwd: root,
        env: { JULIA_NUM_PRECOMPILE_TASKS: "2", OPENBLAS_NUM_THREADS: "1" },
      },
    ],
    gates: [
      "Julia checks require explicitly prepared runtime/project; numerical fixtures are not scientific acceptance",
    ],
  };
}
registry["julia-integration"] = {
  check: (
    { root, julia },
  ) => [{
    ...pytest(root, "results", true),
    env: { JULIA: julia, QCL_NEGF_SOLVER_PROJECT: `${root}/julia` },
  }],
  prepare: (c) => [...registry.results.prepare(c), ...registry.runner.prepare(c)],
  gates: ["Results/Julia integration requires actual prepared package environment"],
};
registry["docs-build"] = {
  check: ({ root }) => [{ executable: "deno", args: ["task", "docs:build"], cwd: root }],
  prepare: ({ root }) => [{ executable: "deno", args: ["task", "docs:prepare"], cwd: root }],
  gates: [
    "One full documentation artifact requires explicit captured inputs and native offline/cache/browser qualification; prose-only D never selects it",
  ],
};
registry.platform = {
  check: ({ root }) => [denoCheck(`${root}/components/qcl-negf-platform`)],
  prepare: () => [],
  gates: [
    "Platform Python tests require its actual Python/pytest dependencies; Deno checks do not install them",
  ],
};
registry.infra = {
  check: ({ root }) => [
    ...backendPaths(root).flatMap((
      cwd,
    ) => [{ executable: "tofu", args: ["fmt", "-check", "-recursive"], cwd }, {
      executable: "tofu",
      args: ["validate"],
      cwd,
    }]),
    {
      executable: "nix",
      args: ["flake", "check", "--no-build", "--no-update-lock-file"],
      cwd: root,
    },
  ],
  prepare: ({ root }) =>
    backendPaths(root).map((cwd) => ({
      executable: "tofu",
      args: ["init", "-backend=false", "-input=false", "-lockfile=readonly"],
      cwd,
    })),
  gates: [
    "Infra checks require explicitly initialized locked providers and Nix inputs; source evaluation is not service/VM readiness",
  ],
};
function closure(group: ImpactGroup): ImpactGroup[] {
  if (group === "contracts") return sorted([...python, ...numerical]);
  if (group === "results") return ["results", "aiida", "portal"];
  if (group === "aiida") return ["aiida", "portal"];
  if (group === "core" || group === "runner") return numerical;
  if (group === "frontend") return ["frontend", "portal"];
  if (group === "platform") return ["platform", "infra"];
  return [group];
}
function classified(c: ChangedPath): { groups: ImpactGroup[]; reason: string; unknown?: string } {
  const group = Object.hasOwn(components, c.owner)
    ? components[c.owner as keyof typeof components]
    : undefined;
  if (c.owner !== "root" && !group) {
    return { groups: all, reason: "unknown owner", unknown: `Unknown owner: ${c.owner}` };
  }
  const modes = [c.oldMode, c.newMode];
  if (modes.some((m) => !["000000", "100644", "100755"].includes(m))) {
    return {
      groups: all,
      reason: "unsupported mode",
      unknown: `Unsupported modes: ${c.owner}/${c.path} ${modes.join("→")}`,
    };
  }
  const prose = c.newMode !== "100755" && c.oldMode !== "100755" &&
    /(^|\/)(AGENTS|CONTRIBUTING|README)\.md$|^docs\/.*\.md$|^\.agents\/.*\.md$/s.test(c.path);
  if (
    c.path === "README.md" && group && ["contracts", "results", "aiida", "portal"].includes(group)
  ) return { groups: [group], reason: "README is native wheel metadata" };
  if (prose) {
    return { groups: ["docs"], reason: "prose/instructions; review local links and anchors" };
  }
  if (c.owner === "root") {
    const known = /^(ops|tests|nix|julia|docs|\.github)\//.test(c.path) ||
      [
        "flake.nix",
        "flake.lock",
        "deno.json",
        "deno.lock",
        "pyproject.toml",
        "uv.lock",
        ".gitmodules",
        "LICENSE",
      ].includes(c.path);
    return known ? { groups: all, reason: "Root assembly/build requires full integration" } : {
      groups: all,
      reason: "unclassified Root path",
      unknown: `Unclassified Root path: ${c.path}`,
    };
  }
  if (group === undefined) throw Error("Missing owning impact group");
  if (group === "portal" && c.path.startsWith("frontend/")) {
    return { groups: closure("frontend"), reason: "Portal frontend and API wheel" };
  }
  if ((group === "core" || group === "runner") && c.path.startsWith("docs/")) {
    return {
      groups: sorted([...closure(group), "docs-build"]),
      reason: "executable Julia documentation input",
    };
  }
  return { groups: closure(group), reason: "owning source/native metadata and dependency closure" };
}
export function planImpact(
  changes: readonly ChangedPath[],
  unknowns: readonly string[] = [],
): ImpactPlan {
  const reasons: ImpactPlan["reasons"] = [],
    groups: ImpactGroup[] = [],
    uncertainty = [...unknowns];
  for (const c of changes) {
    pathSafe(c.path);
    pathSafe(c.owner);
    const rule = classified(c), selected = sorted(rule.groups);
    reasons.push({
      owner: c.owner,
      path: c.path,
      groups: selected,
      reason: rule.reason + (c.newMode === "000000" ? "; deleted" : ""),
    });
    groups.push(...selected);
    if (rule.unknown) uncertainty.push(rule.unknown);
  }
  if (uncertainty.length) groups.push(...all);
  const selected = sorted(groups);
  return {
    format: "qcl-negf.impact.v1",
    base: null,
    head: null,
    groups: selected,
    reasons: reasons.sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b))),
    unknowns: sorted(uncertainty),
    nativeGates: sorted(selected.flatMap((g) => registry[g].gates)),
    scientificStage: "not_requested",
  };
}
export function parseImpactOptions(args: readonly string[]): ImpactOptions {
  const options: ImpactOptions = { base: null, head: null, overrides: [] };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--base" || a === "--head") {
      const k = a === "--base" ? "base" : "head", value = args[++i];
      if (options[k] !== null || value === undefined) throw Error("Duplicate/missing impact ref");
      refSafe(value);
      options[k] = value;
    } else if (["--full", "--python", "--julia", "--infra"].includes(a)) {
      const flag = a.slice(2) as ImpactOptions["overrides"][number];
      if (options.overrides.includes(flag)) throw Error("Duplicate impact override");
      options.overrides.push(flag);
    } else throw Error("Usage: [--base REF --head REF] [--full|--python|--julia|--infra]");
  }
  if ((options.base === null) !== (options.head === null)) {
    throw Error("Both --base and --head required");
  }
  if (!args.length) options.overrides = ["full"];
  return options;
}
export function selectedPlan(
  changes: readonly ChangedPath[],
  options: ImpactOptions,
  unknowns: readonly string[] = [],
): ImpactPlan {
  const p = planImpact(changes, unknowns);
  for (const flag of options.overrides) {
    const extra: ImpactGroup[] = flag === "full"
      ? all
      : flag === "python"
      ? [...python, "frontend"]
      : flag === "julia"
      ? [...numerical, "docs-build"]
      : ["platform", "infra"];
    p.groups.push(...extra);
  }
  p.groups = sorted(p.groups);
  p.nativeGates = sorted(p.groups.flatMap((g) => registry[g].gates));
  return p;
}
function uniqueCommands(commands: Command[]): Command[] {
  return [...new Map(commands.map((c) => [JSON.stringify(c), c])).values()];
}
export function checkCommands(plan: ImpactPlan, context: ImpactContext): Command[] {
  const existing = sorted(
    plan.reasons
      .filter((r) =>
        r.groups.length === 1 && r.groups[0] === "docs" && !r.reason.endsWith("; deleted")
      )
      .map((r) => `${context.root}/${r.owner === "root" ? "" : r.owner + "/"}${r.path}`),
  );
  return uniqueCommands([
    ...(existing.length
      ? [{ executable: "deno", args: ["fmt", "--check", ...existing], cwd: context.root }]
      : []),
    ...plan.groups.flatMap((g) => registry[g].check(context)),
  ]);
}
export function preparationCommands(plan: ImpactPlan, context: ImpactContext): Command[] {
  return uniqueCommands(plan.groups.flatMap((g) => registry[g].prepare(context)));
}
function rawChanges(raw: string, owner: string) {
  if (!raw) return [];
  if (!raw.endsWith("\0")) throw Error("Truncated raw Git diff");
  const fields = raw.split("\0"), rows: (ChangedPath & { old: string; next: string })[] = [];
  fields.pop();
  if (fields.length % 2) throw Error("Malformed raw Git diff fields");
  for (let i = 0; i < fields.length; i += 2) {
    const m = /^:([0-7]{6}) ([0-7]{6}) ([a-f0-9]{40}) ([a-f0-9]{40}) ([AMDT])$/.exec(fields[i]);
    if (!m) throw Error("Malformed raw Git diff header");
    pathSafe(fields[i + 1]);
    rows.push({ owner, path: fields[i + 1], oldMode: m[1], newMode: m[2], old: m[3], next: m[4] });
  }
  return rows;
}
const diff = (
  before: string,
  after: string,
) => [
  "diff",
  "--raw",
  "-z",
  "--no-abbrev",
  "--ignore-submodules=none",
  "--no-renames",
  "--no-ext-diff",
  "--no-textconv",
  before,
  after,
  "--",
];
export async function collectCommittedChanges(
  root: string,
  baseRef: string,
  headRef: string,
  readGit: GitReader,
) {
  refSafe(baseRef);
  refSafe(headRef);
  const resolve = async (where: string, ref: string) => {
    const id = await readGit(where, [
      "rev-parse",
      "--verify",
      "--end-of-options",
      `${ref}^{commit}`,
    ]);
    if (!/^[a-f0-9]{40}$/.test(id)) throw Error("Git ref is not a canonical commit");
    return id;
  };
  const base = await resolve(root, baseRef), head = await resolve(root, headRef);
  const changes: ChangedPath[] = [], unknowns: string[] = [];
  const rows = rawChanges(await readGit(root, diff(base, head)), "root");
  let configured: Set<string> | null = null;
  if (rows.some((r) => r.oldMode === "160000" || r.newMode === "160000")) {
    try {
      const config = await readGit(root, [
        "config",
        "--blob",
        `${head}:.gitmodules`,
        "--null",
        "--get-regexp",
        "^submodule\\..*\\.path$",
      ]);
      if (!config.endsWith("\0")) throw Error("Malformed committed submodule config");
      configured = new Set();
      for (const entry of config.slice(0, -1).split("\0")) {
        const match = /^submodule\.[^\n]+\.path\n(components\/[A-Za-z0-9][A-Za-z0-9.-]*)$/.exec(
          entry,
        );
        if (!match || configured.has(match[1])) throw Error("Invalid committed submodule config");
        configured.add(match[1]);
      }
    } catch {
      unknowns.push("Committed .gitmodules unavailable or invalid");
    }
  }
  for (const r of rows) {
    if (r.oldMode !== "160000" && r.newMode !== "160000") {
      changes.push({ owner: r.owner, path: r.path, oldMode: r.oldMode, newMode: r.newMode });
      continue;
    }
    if (
      r.oldMode !== "160000" || r.newMode !== "160000" || !configured?.has(r.path) ||
      !Object.hasOwn(components, r.path)
    ) {
      unknowns.push(`Added/deleted/unconfigured gitlink: ${r.path}`);
      continue;
    }
    const local = `${root}/${r.path}`;
    let raw: string;
    try {
      if (await resolve(local, r.old) !== r.old || await resolve(local, r.next) !== r.next) {
        throw Error("Component commit mismatch");
      }
      raw = await readGit(local, diff(r.old, r.next));
    } catch {
      unknowns.push(`Unavailable component objects: ${r.path}`);
      continue;
    }
    for (const c of rawChanges(raw, r.path)) {
      changes.push({ owner: c.owner, path: c.path, oldMode: c.oldMode, newMode: c.newMode });
    }
  }
  return { base, head, changes, unknowns: sorted(unknowns) };
}
export async function resolveImpact(
  options: ImpactOptions,
  root = workspace,
  readGit: GitReader = git,
): Promise<ImpactPlan> {
  if (options.base === null || options.head === null) return selectedPlan([], options);
  const c = await collectCommittedChanges(root, options.base, options.head, readGit);
  return { ...selectedPlan(c.changes, options, c.unknowns), base: c.base, head: c.head };
}
if (import.meta.main) {
  await main(async () =>
    console.log(JSON.stringify(await resolveImpact(parseImpactOptions(Deno.args)), null, 2))
  );
}
