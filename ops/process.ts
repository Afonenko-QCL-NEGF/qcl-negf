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
