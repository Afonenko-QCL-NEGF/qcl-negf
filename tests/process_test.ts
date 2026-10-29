// The original independent byte/deadline controls follow the shared transport.
import { type Child, runFinite, runRetained } from "../ops/process.ts";
import { readBounded } from "../ops/docs.ts";
function assert(value: unknown, message = "assertion failed"): asserts value {
  if (!value) throw Error(message);
}
function immediatePromise<T>(work: () => T | PromiseLike<T>): Promise<T> {
  return new Promise((resolve) => resolve(work()));
}
function fake(data: Uint8Array, status: Promise<{ code: number; success: boolean }>): Child {
  return {
    stdout: new ReadableStream({
      start(c) {
        c.enqueue(data);
        c.close();
      },
    }),
    stderr: new ReadableStream({
      start(c) {
        c.enqueue(new Uint8Array([21, 22, 23, 24, 25, 26, 27, 28]));
        c.close();
      },
    }),
    status,
    kill() {},
  };
}
Deno.test("finite drains preserve partial logs on combined cap and failed exit", async () => {
  const saved: Record<string, number[]> = { stdout: [], stderr: [] };
  const result = await runFinite(
    () =>
      fake(
        new Uint8Array([11, 12, 13, 14, 15, 16, 17, 18]),
        Promise.resolve({ code: 7, success: false }),
      ),
    (stream, bytes) =>
      immediatePromise<void>(() => {
        saved[stream].push(...bytes);
      }),
    { wallMs: 100, drainMs: 20, streamBytes: 6, totalBytes: 9 },
  );
  assert(result.reason === "log_cap");
  assert(JSON.stringify(saved) === '{"stdout":[11,12,13,14,15,16],"stderr":[21,22,23]}');
  assert(result.stdout_acknowledged_bytes === 6 && result.stderr_acknowledged_bytes === 3);
  assert(result.stdout_received_bytes === 8 && result.stderr_received_bytes === 8);
  assert(result.retention === "acknowledged");
  assert(result.exit?.code === 7);
  assert(result.process_tree_terminated === null);
});
Deno.test("rejecting sink distinguishes received bytes from acknowledged retention", async () => {
  const saved: number[] = [];
  const result = await runFinite(
    () => fake(new Uint8Array([31, 32, 33]), Promise.resolve({ code: 0, success: true })),
    (stream, bytes) =>
      immediatePromise<void>(() => {
        if (stream === "stderr") throw new Error("sink rejected; partial write unknown");
        saved.push(...bytes);
      }),
    { wallMs: 100, drainMs: 20, streamBytes: 16, totalBytes: 32 },
  );
  assert(JSON.stringify(saved) === "[31,32,33]");
  assert(result.stdout_acknowledged_bytes === 3 && result.stderr_acknowledged_bytes === 0);
  assert(result.stderr_received_bytes === 8 && result.stderr_attempted_bytes === 8);
  assert(result.retention === "failed_unknown_partial");
});
Deno.test("deadline retains exact nonzero prefix and snapshots a hanging sink", async () => {
  let release!: () => void;
  const saved: number[] = [];
  const result = await runFinite(
    () => fake(new Uint8Array([41, 42]), new Promise(() => {})),
    async (stream, bytes) => {
      if (stream === "stdout") saved.push(...bytes);
      else {await new Promise<void>((resolve) => {
          release = resolve;
        });}
    },
    { wallMs: 5, drainMs: 5, streamBytes: 16, totalBytes: 32 },
  );
  assert(JSON.stringify(saved) === "[41,42]");
  assert(result.reason === "deadline" && result.drain === "incomplete");
  assert(result.stdout_acknowledged_bytes === 2 && result.stderr_acknowledged_bytes === 0);
  assert(result.stderr_received_bytes === 8 && result.retention === "incomplete_unknown_partial");
  const snapshot = JSON.stringify(result);
  release();
  await Promise.resolve();
  await Promise.resolve();
  assert(JSON.stringify(result) === snapshot, "late sink completion must not mutate receipt");
});
Deno.test("incremental reader enforces cap plus one sentinel despite small metadata", async () => {
  let received = 0, closed = false;
  const requests: number[] = [];
  let refused = false;
  try {
    await readBounded(
      {
        read(buffer) {
          return immediatePromise<number | null>(() => {
            requests.push(buffer.length);
            buffer.fill(71);
            received += buffer.length;
            return buffer.length;
          });
        },
        close() {
          closed = true;
        },
      },
      4,
      1,
    ); // observed metadata is small, actual stream grew
  } catch {
    refused = true;
  }
  assert(refused && closed && received === 5);
  assert(requests.every((n) => n <= 5), "no read beyond cap plus sentinel");
  let offset = 0;
  const bytes = new Uint8Array([81, 82, 83]);
  const retained = await readBounded(
    {
      read(buffer) {
        return immediatePromise<number | null>(() => {
          if (offset === bytes.length) return null;
          const n = Math.min(buffer.length, bytes.length - offset);
          buffer.set(bytes.subarray(offset, offset + n));
          offset += n;
          return n;
        });
      },
      close() {},
    },
    4,
    3,
  );
  assert(JSON.stringify([...retained]) === "[81,82,83]");
  let changedClosed = false, sent = false, changedRefused = false;
  try {
    await readBounded(
      {
        read(buffer) {
          return immediatePromise<number | null>(() => {
            if (sent) return null;
            sent = true;
            buffer.set([91, 92]);
            return 2;
          });
        },
        close() {
          changedClosed = true;
        },
      },
      4,
      1,
    );
  } catch {
    changedRefused = true;
  }
  assert(changedRefused && changedClosed, "growth within cap still invalidates metadata binding");
});
Deno.test("deadline plus unclosed pipes return finite drain failure", async () => {
  let killed = false;
  const result = await runFinite(
    () => ({
      stdout: new ReadableStream(),
      stderr: new ReadableStream(),
      status: new Promise(() => {}),
      kill() {
        killed = true;
      },
    }),
    async () => {},
    { wallMs: 5, drainMs: 5, streamBytes: 6, totalBytes: 9 },
  );
  assert(killed && result.reason === "deadline");
  assert(result.drain === "incomplete");
  assert(result.exit === null);
});

Deno.test("retained transport owns argv before dispatch and publishes acknowledged bytes", async () => {
  const dir = await Deno.makeTempDir({ prefix: "qcl-process-test-" });
  const command = { executable: "/inert", args: ["original"], env: { A: "one" } };
  const promise = runRetained(command, {
    directory: `${dir}/attempt`,
    limits: { wallMs: 100, drainMs: 20, streamBytes: 32, totalBytes: 64 },
    spawn(call) {
      assert(call.args[0] === "original" && call.env?.A === "one");
      call.args[0] = "reader mutation";
      return fake(new Uint8Array([1, 2]), Promise.resolve({ code: 0, success: true }));
    },
  });
  command.args[0] = "borrowed mutation";
  command.env.A = "two";
  const result = await promise;
  assert(JSON.stringify([...result.stdout]) === "[1,2]");
  assert(JSON.stringify([...result.stderr]) === "[21,22,23,24,25,26,27,28]");
  const receipt = JSON.parse(await Deno.readTextFile(result.receipt.path));
  assert(receipt.command.args[0] === "original" && receipt.command.env.A === "one");
  assert(receipt.result.process_tree_terminated === null);
  await Deno.remove(dir, { recursive: true });
});
Deno.test("spawn failure has durable source error and occupied directory cannot replay", async () => {
  const dir = await Deno.makeTempDir({ prefix: "qcl-process-test-" });
  let calls = 0;
  const options = {
    directory: `${dir}/attempt`,
    limits: { wallMs: 100, drainMs: 10, streamBytes: 10, totalBytes: 20 },
    spawn() {
      calls++;
      throw Error("source-error");
    },
  };
  for (let i = 0; i < 2; i++) {
    let failed = false;
    try {
      await runRetained({ executable: "/inert", args: [] }, options);
    } catch {
      failed = true;
    }
    assert(failed);
  }
  assert(calls === 1);
  const receipt = JSON.parse(await Deno.readTextFile(`${dir}/attempt/result.json`));
  assert(receipt.accounting === "unknown" && receipt.error.includes("source-error"));
  await Deno.remove(dir, { recursive: true });
});
Deno.test("retained parent symlink is rejected before spawn", async () => {
  const dir = await Deno.makeTempDir({ prefix: "qcl-process-test-" });
  await Deno.mkdir(`${dir}/real`);
  await Deno.symlink(`${dir}/real`, `${dir}/link`);
  let calls = 0;
  try {
    await runRetained({ executable: "/inert", args: [] }, {
      directory: `${dir}/link/attempt`,
      limits: { wallMs: 100, drainMs: 10, streamBytes: 10, totalBytes: 20 },
      spawn() {
        calls++;
        throw Error("must not spawn");
      },
    });
    throw Error("accepted link");
  } catch (error) {
    assert(String(error).includes("invalid_retained_parent"));
  }
  assert(calls === 0);
  await Deno.remove(dir, { recursive: true });
});
