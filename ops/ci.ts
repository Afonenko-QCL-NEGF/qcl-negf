import { type Command, main, run, workspace } from "./process.ts";
import { type SourceGraph, sourceGraph } from "./git.ts";
import {
  checkCommands,
  type ImpactContext,
  type ImpactPlan,
  parseImpactOptions,
  resolveImpact,
} from "./impact.ts";

export async function runPlanCommands(
  plan: ImpactPlan,
  context: ImpactContext,
  commands: readonly Command[],
  execute: (command: Command) => Promise<string> = run,
  readGraph: () => Promise<SourceGraph> = () => sourceGraph(context.root),
): Promise<void> {
  const graph = structuredClone(await readGraph());
  if (plan.head !== null && graph.revision !== plan.head) {
    throw Error("Selected head differs from clean checkout");
  }
  for (const gate of plan.nativeGates) console.error(`Prerequisite/review gate: ${gate}`);
  for (const command of commands) await execute(command);
  if (JSON.stringify(await readGraph()) !== JSON.stringify(graph)) {
    throw Error("The Git source graph changed during checks");
  }
}
export async function runChecks(
  plan: ImpactPlan,
  context: ImpactContext,
  execute: (command: Command) => Promise<string> = run,
  readGraph: () => Promise<SourceGraph> = () => sourceGraph(context.root),
): Promise<void> {
  await runPlanCommands(plan, context, checkCommands(plan, context), execute, readGraph);
}
if (import.meta.main) {
  await main(async () => {
    const plan = await resolveImpact(parseImpactOptions(Deno.args));
    await runChecks(plan, { root: workspace, julia: Deno.env.get("JULIA") ?? "julia" });
  });
}
