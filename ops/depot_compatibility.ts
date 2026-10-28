// Pure bounded proof validation. Native observations remain trusted producer assertions.
export interface DepotInputs {
  schema: "qcl-negf.julia-depot-inputs.v1";
  system: "x86_64-linux";
  julia: {
    version: "1.13.0";
    drv: string;
    output: string;
    profile: "production-build" | "local-debug";
    test_workers: number | null;
  };
  files: { path: string; sha256: string | null }[];
  selector_policy: "locked-external-native-default-v1";
}
export function record(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}
export function exact(v: unknown, keys: string[]): asserts v is Record<string, unknown> {
  if (!record(v) || Object.keys(v).sort().join("\0") !== [...keys].sort().join("\0")) {
    throw Error("Unknown or missing depot proof fields");
  }
}
export const hex = (v: unknown): v is string => typeof v === "string" && /^[a-f0-9]{64}$/.test(v);
export function store(v: unknown, drv = false): v is string {
  return typeof v === "string" &&
    /^\/nix\/store\/[0-9abcdfghijklmnpqrsvwxyz]{32}-[A-Za-z0-9+._-]+$/.test(v) &&
    (!drv || v.endsWith(".drv"));
}
export function canonicalInputs(v: unknown): string {
  if (Array.isArray(v)) return "[" + v.map(canonicalInputs).join(",") + "]";
  if (record(v)) {
    return "{" + Object.keys(v).sort().map((k) =>
      JSON.stringify(k) + ":" + canonicalInputs(v[k])
    ).join(",") + "}";
  }
  return JSON.stringify(v);
}
export async function digest(raw: string): Promise<string> {
  return [...new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(raw)))]
    .map((b) => b.toString(16).padStart(2, "0")).join("");
}
export function validateInputs(v: unknown): asserts v is DepotInputs {
  exact(v, ["schema", "system", "julia", "files", "selector_policy"]);
  if (
    v.schema !== "qcl-negf.julia-depot-inputs.v1" || v.system !== "x86_64-linux" ||
    v.selector_policy !== "locked-external-native-default-v1"
  ) throw Error("Unsupported depot input profile");
  exact(v.julia, ["version", "drv", "output", "profile", "test_workers"]);
  const j = v.julia;
  if (
    j.version !== "1.13.0" || !store(j.drv, true) || !store(j.output) ||
    String(j.output).endsWith(".drv") ||
    !["production-build", "local-debug"].includes(String(j.profile)) ||
    !(j.test_workers === null ||
      (Number.isSafeInteger(j.test_workers) && Number(j.test_workers) > 0)) ||
    (j.profile === "local-debug" && j.test_workers !== 2)
  ) throw Error("Invalid exact Julia factory input");
  if (!Array.isArray(v.files) || v.files.length < 1 || v.files.length > 128) {
    throw Error("Invalid dependency file inventory");
  }
  let prior = "";
  for (const row of v.files) {
    exact(row, ["path", "sha256"]);
    if (
      typeof row.path !== "string" || !/^[A-Za-z0-9_.+/-]{1,240}$/.test(row.path) ||
      row.path.split("/").some((p) => ["", ".", ".."].includes(p)) || row.path <= prior ||
      !(row.sha256 === null || hex(row.sha256))
    ) throw Error("Invalid sorted dependency file binding");
    prior = row.path;
  }
}
export async function validateCompatibility(
  v: unknown,
  expected: DepotInputs | undefined,
  manifest: string,
): Promise<string> {
  exact(v, ["schema", "inputs", "inputs_sha256", "native"]);
  if (v.schema !== "qcl-negf.julia-depot-compatibility.v1" || expected === undefined) {
    throw Error("V2 needs trusted CURRENT dependency inputs");
  }
  validateInputs(v.inputs);
  validateInputs(expected);
  const actual = await digest(canonicalInputs(v.inputs));
  if (
    !hex(v.inputs_sha256) || v.inputs_sha256 !== actual ||
    canonicalInputs(v.inputs) !== canonicalInputs(expected) ||
    !v.inputs.files.some((f) => f.path === "julia/Manifest.toml" && f.sha256 === manifest)
  ) throw Error("CURRENT dependency inputs differ from captured depot");
  exact(v.native, [
    "schema",
    "inputs_sha256",
    "julia_drv",
    "julia_output",
    "observed_platform",
    "preferences_sha256",
    "selector_closure_sha256",
    "artifact_selection_sha256",
    "receipt_sha256",
  ]);
  const n = v.native;
  if (
    n.schema !== "qcl-negf.julia-depot-native.v1" || n.inputs_sha256 !== actual ||
    n.julia_drv !== expected.julia.drv || n.julia_output !== expected.julia.output ||
    typeof n.observed_platform !== "string" || !/^[!-~]{1,1024}$/.test(n.observed_platform) ||
    ![
      n.preferences_sha256,
      n.selector_closure_sha256,
      n.artifact_selection_sha256,
      n.receipt_sha256,
    ].every(hex)
  ) throw Error("Native depot qualification binding differs");
  return actual;
}

// --argstr is not function application for modern `nix eval`.
export function nixDataApplication(args: Record<string, unknown>): string {
  return "f: f (builtins.fromJSON " +
    JSON.stringify(JSON.stringify(args)).replaceAll("${", "\\${") + ")";
}
