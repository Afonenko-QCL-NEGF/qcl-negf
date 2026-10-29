export interface Command {
  executable: string;
  args: string[];
  cwd?: string;
  env?: Record<string, string>;
  clearEnv?: boolean;
}

export function display(command: Command): string {
  return [command.executable, ...command.args].map((part) => JSON.stringify(part)).join(" ");
}

export async function run(command: Command, capture = false): Promise<string> {
  const result = await new Deno.Command(command.executable, {
    args: command.args,
    cwd: command.cwd,
    env: command.env,
    clearEnv: command.clearEnv,
    stdin: "inherit",
    stdout: capture ? "piped" : "inherit",
    stderr: "inherit",
  }).output();
  if (!result.success) throw new Error(`${command.executable} exited ${result.code}`);
  return capture ? new TextDecoder().decode(result.stdout).trimEnd() : "";
}

export async function exists(path: string): Promise<boolean> {
  try {
    await Deno.stat(path);
    return true;
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) return false;
    throw error;
  }
}

export const workspace = decodeURIComponent(new URL("../", import.meta.url).pathname).replace(
  /\/$/,
  "",
);

export async function main(action: () => Promise<void>): Promise<void> {
  try {
    await action();
  } catch (error) {
    console.error(error instanceof Error ? error.message : error);
    Deno.exit(1);
  }
}

export interface Child {
  stdout: ReadableStream<Uint8Array>;
  stderr: ReadableStream<Uint8Array>;
  status: Promise<{ code: number; success: boolean }>;
  kill(): void;
}
export interface Limits {
  wallMs: number;
  drainMs: number;
  streamBytes: number;
  totalBytes: number;
}
export interface FiniteResult {
  reason: string | null;
  exit: { code: number; success: boolean } | null;
  drain: "complete" | "incomplete";
  errors: string[];
  stdout_received_bytes: number;
  stderr_received_bytes: number;
  stdout_attempted_bytes: number;
  stderr_attempted_bytes: number;
  stdout_acknowledged_bytes: number;
  stderr_acknowledged_bytes: number;
  retention: "acknowledged" | "failed_unknown_partial" | "incomplete_unknown_partial";
  process_tree_terminated: null;
  resource_measurements: null;
}
// Injectable bounded transport; it does not certify CPU/RAM or descendant cleanup.
export async function runFinite(
  spawn: () => Child,
  save: (stream: "stdout" | "stderr", bytes: Uint8Array, signal: AbortSignal) => Promise<void>,
  limits: Limits,
): Promise<FiniteResult> {
  for (const n of Object.values(limits)) {
    if (!Number.isSafeInteger(n) || n <= 0) throw new Error("invalid_finite_limit");
  }
  let reason: string | null = null;
  let total = 0;
  const completion: {
    exit: FiniteResult["exit"];
    drain: FiniteResult["drain"];
  } = { exit: null, drain: "complete" };
  const errors: string[] = [];
  let terminal = false;
  let sinkFailed = false;
  const cancellation = new AbortController();
  const child = spawn();
  const readers = [child.stdout.getReader(), child.stderr.getReader()];
  let signal!: () => void;
  const stopped = new Promise<void>((resolve) => {
    signal = resolve;
  });
  function stop(why: string) {
    if (terminal) return;
    if (!reason) {
      reason = why;
      signal();
    }
    try {
      child.kill();
    } catch {
      errors.push("kill_failed");
    }
  }
  const timer = setTimeout(() => stop("deadline"), limits.wallMs);
  const reserved = [0, 0], received = [0, 0], acknowledged = [0, 0];
  const drains = readers.map(async (reader, i) => {
    try {
      while (true) {
        const chunk = await reader.read();
        if (terminal) break;
        if (chunk.done) break;
        const size = chunk.value.byteLength;
        received[i] += size;
        const keep = Math.min(size, limits.streamBytes - reserved[i], limits.totalBytes - total);
        reserved[i] += keep;
        total += keep; // reservation is not retained-byte evidence
        if (keep < size) stop("log_cap");
        if (keep) {
          await save(
            i === 0 ? "stdout" : "stderr",
            chunk.value.subarray(0, keep),
            cancellation.signal,
          );
          if (terminal) break;
          acknowledged[i] += keep; // only a successful sink acknowledgement counts
        }
        if (keep < size) break;
      }
    } catch {
      if (!terminal) {
        sinkFailed = true;
        errors.push("drain_or_log_write_failed_unknown_partial");
        stop("drain_or_log_write_failed");
      }
    }
  });
  const status = child.status.then((value) => {
    if (!terminal) completion.exit = { ...value };
  }, () => {
    if (!terminal) {
      errors.push("status_failed");
      stop("status_failed");
    }
  });
  const complete = Promise.all([...drains, status]);
  await Promise.race([complete, stopped]);
  let drainTimer: ReturnType<typeof setTimeout> | undefined;
  try {
    await Promise.race([
      complete,
      new Promise<void>((resolve) => {
        drainTimer = setTimeout(() => {
          completion.drain = "incomplete";
          resolve();
        }, limits.drainMs);
      }),
    ]);
  } finally {
    clearTimeout(timer);
    clearTimeout(drainTimer);
    terminal = true;
    // Cancellation may itself hang; do not await it beyond the finite drain.
    if (completion.drain === "incomplete") {
      // Cooperative cancellation is requested, never assumed effective. A sink
      // may write later; the result records unknown partial retention and is a
      // detached snapshot, not a claim of immutable terminal log bytes.
      cancellation.abort();
      for (const reader of readers) reader.cancel().catch(() => {});
    }
  }
  const drain = completion.drain;
  const observedExit = completion.exit;
  if (!reason && observedExit && !observedExit.success) reason = "exit_failure";
  return {
    reason,
    exit: observedExit ? { ...observedExit } : null,
    drain,
    errors: [...errors],
    stdout_received_bytes: received[0],
    stderr_received_bytes: received[1],
    stdout_attempted_bytes: reserved[0],
    stderr_attempted_bytes: reserved[1],
    stdout_acknowledged_bytes: acknowledged[0],
    stderr_acknowledged_bytes: acknowledged[1],
    retention: drain === "incomplete"
      ? "incomplete_unknown_partial"
      : sinkFailed
      ? "failed_unknown_partial"
      : "acknowledged",
    process_tree_terminated: null,
    resource_measurements: null,
  };
}

export interface RetainedResult {
  stdout: Uint8Array<ArrayBuffer>;
  stderr: Uint8Array<ArrayBuffer>;
  result: FiniteResult;
  receipt: { path: string; sha256: string };
}

async function retainedParent(directory: string): Promise<void> {
  if (
    !directory.startsWith("/") || directory.endsWith("/") || directory.includes("\\") ||
    directory.split("/").slice(1).some((part) => !part || part === "." || part === "..") ||
    // deno-lint-ignore no-control-regex
    /[\x00-\x1f\x7f]/.test(directory)
  ) throw Error("noncanonical_retained_directory");
  let parent = directory.slice(0, directory.lastIndexOf("/")) || "/";
  while (true) {
    const info = await Deno.lstat(parent);
    if (!info.isDirectory || info.isSymlink) throw Error("invalid_retained_parent");
    if (parent === "/") break;
    parent = parent.slice(0, parent.lastIndexOf("/")) || "/";
  }
}

/** Retain bounded command evidence in one fresh directory, before spawning.
 * File publication failure throws even after child success. Cleanup never proves
 * daemon/process-tree completion; uncertain sinks retain the finite result.
 */
export async function runRetained(
  command: Command,
  options: {
    directory: string;
    limits: Limits;
    spawn?: (command: Command) => Child;
  },
): Promise<RetainedResult> {
  const selected = structuredClone(command);
  const limits = { ...options.limits };
  for (const n of Object.values(limits)) {
    if (!Number.isSafeInteger(n) || n <= 0) throw Error("invalid_finite_limit");
  }
  const directory = options.directory;
  await retainedParent(directory);
  await Deno.mkdir(directory, { mode: 0o700 });
  const stdout = await Deno.open(`${directory}/stdout.log`, {
    createNew: true,
    write: true,
    mode: 0o600,
  });
  let stderr: Deno.FsFile | null = null;
  const chunks: Uint8Array<ArrayBuffer>[][] = [[], []];
  let result: FiniteResult;
  const receipt = async (value: unknown) => {
    const bytes = new TextEncoder().encode(JSON.stringify(value, null, 2) + "\n");
    const path = `${directory}/result.json`;
    await Deno.writeFile(path, bytes, { createNew: true, mode: 0o600 });
    const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
    return { path, sha256: [...digest].map((n) => n.toString(16).padStart(2, "0")).join("") };
  };
  try {
    stderr = await Deno.open(`${directory}/stderr.log`, {
      createNew: true,
      write: true,
      mode: 0o600,
    });
    const spawn = options.spawn ?? ((call: Command): Child => {
      const child = new Deno.Command(call.executable, {
        args: call.args,
        cwd: call.cwd,
        env: call.env,
        clearEnv: call.clearEnv,
        stdin: "null",
        stdout: "piped",
        stderr: "piped",
      }).spawn();
      return {
        stdout: child.stdout,
        stderr: child.stderr,
        status: child.status,
        kill: () => child.kill("SIGKILL"),
      };
    });
    result = await runFinite(
      () => spawn(structuredClone(selected)),
      async (stream, bytes, signal) => {
        const data = bytes.slice();
        const file = stream === "stdout" ? stdout : stderr!;
        let offset = 0;
        while (offset < data.length) {
          if (signal.aborted) throw Error("retained_log_write_aborted");
          const count = await file.write(data.subarray(offset));
          if (count <= 0) throw Error("retained_log_short_write");
          offset += count;
        }
        chunks[stream === "stdout" ? 0 : 1].push(data);
      },
      limits,
    );
  } catch (error) {
    const retained = await receipt({
      command: selected,
      result: null,
      accounting: "unknown",
      error: String(error).slice(0, 4096),
    });
    throw Object.assign(new Error(String(error).slice(0, 4096)), { receipt: retained });
  } finally {
    stdout.close();
    stderr?.close();
  }
  const collect = (stream: number, count: number) => {
    const data = new Uint8Array(count);
    let offset = 0;
    for (const chunk of chunks[stream]) {
      const kept = chunk.subarray(0, data.length - offset);
      data.set(kept, offset);
      offset += kept.length;
      if (offset === data.length) break;
    }
    return data;
  };
  return {
    stdout: collect(0, result.stdout_acknowledged_bytes),
    stderr: collect(1, result.stderr_acknowledged_bytes),
    result,
    receipt: await receipt({ command: selected, result }),
  };
}
