# SCI08-R2 I1: source call/cleanup table, partial refusal-only

Baseline Runner `4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`.
All locators below are baseline symbol/line; patch adds lines. Strict is globally
refused, not admitted with a lifecycle. `NOT READY` applies to all writer traces.
This table covers the D2 named edges; it is not an exhaustive call graph proof.
Unenumerated transitive branches remain NOT READY, dominated only by entry refusal.

| Caller → callee / branch | First mutator and cleanup | Strict disposition | Remaining proof |
| --- | --- | --- | --- |
| execute_scientific_plan → scientific preflight:449 | mkpath(root):460 later | Existing unconditional strict refusal before root create | Full admission/lifecycle absent |
| execute_scientific_plan_staged:123 → direct scientific path | direct call may publish | Added early preflight + forwarded policy/envelope | No standalone fallback from strict |
| staged:150 → scratch workspace | mkpath; mktempdir(cleanup=false) | Added early preflight dominates | Parent/child permits absent |
| staged:155 → stage_result_tree | copy then delivery | Policy forwarded + stage entry guard | Composite domain reservation absent |
| staged:156 → whole workspace success rm | recursive rm includes source payload | Early strict refusal dominates, branch unreachable | Ownership/lifetime/exact unlink proof absent |
| scientific:635 → commit_operator_artifacts | mkpath; mktempdir automatic cleanup; finally rm stage | Policy forwarded; callee entry strict refusal | No independent verified replacement; no deletion credit |
| scientific:1093 durable_state → commit_point_artifacts | mkpath; mktempdir automatic cleanup | Policy forwarded; callee strict refusal before create | Typed parent/child permits and bounded inventory absent |
| scientific:1267 final → commit_point_artifacts | same entry | Policy forwarded; callee refusal | No final acceptance claim |
| point commit pre-rename → finally:1103 | failed partial stage recursive rm | Unreachable under strict | Preserve partial/unknown via lifecycle NOT implemented |
| point commit post-rename → verify/receipt/pointers | rename + root sync + verifier + receipt + previous/current sync | Standalone order preserved | Published-unacknowledged typed outcome NOT implemented |
| point commit → prune:780 | broad generation recursive rm | Unreachable strict | Protected current/previous/failed selection NOT implemented |
| operator pre/post-rename:1286–1326 | stage→final; pointer; finally rm | Strict entry refuses | Independent durable verifier missing; no cleanup credit |
| scientific:1069 → ScientificHistoryRecorder | mkpath(history) | Policy forwarded; constructor guard before create | Persistent context absent |
| record_scientific_history! → automatic flush:97/112 | buffer/segment then temp | Strict recorder cannot be constructed through keyword entry | No context stored in recorder; NOT READY |
| scientific:1090/1264 → flush_scientific_history! | segment increment then mktemp | Policy forwarded; guard before segment mutation | Needs-reconcile/rows preservation absent |
| scientific:1485 history finalizer → flush | finalizer can mask primary in standalone | Strict execution never enters; policy forwarded | Primary/secondary lifecycle treatment NOT implemented |
| history flush:185–225 post-rename/index | segment rename; counters; atomic index; finally rm temp | Strict flush refuses before any mutation | No acknowledgement inference from counters |
| point receipt/pointers/history index → _observability_atomic_text:597 | mkpath; mktemp; catch close/rm temp | Added strict entry guard, do/path-first keyword forwarding | Caller context propagation incomplete; NOT READY |
| atomic text → _atomic_replace_file:8 | chmod; native rename | Added strict entry guard before chmod | No native backend claim |
| _atomic_checkpoint:3 → save_checkpoint + replace | mkdir/temp; catch removes temp | Added strict entry guard | Nested context/preservation absent |
| save_checkpoint:678 | mktemp; finally rm temp | No low-level policy hook; unreachable from admitted strict because none admitted | Transitive writer NOT READY |
| import archives:388 → copy/publish | mkpath; mktempdir automatic cleanup; finally rm:423 | Added helper entry guard, scientific caller forwards policy | Post-rename identity/outcome and auto-cleanup absent |
| scientific:1117 → imported-* recursive rm | post-checkpoint imported data deletion | Global strict refusal dominates | No deletion authority/lifetime proof; NOT READY |
| scientific:1334–1347 optical branch | write .pending; rename; receipt; finally rm pending | Global strict refusal dominates | Typed bound/child permit/partial preservation absent |
| stage_result_tree:50–113 pre/post-rename | mkdir/temp(cleanup=false); copy; rename child outside; finally rm container | Added strict entry guard | Source retained; no assumed empty-container proof; lifecycle absent |
| all catch/finally/implicit temporary cleanup | may run during failure/exit | Strict refuses before entering writers | No strict cleanup implementation; no writer-ready status |

No protected/failed/final pruning was added; no cleanup was credited; no strict
partial was created. This is source dominance reasoning, not runtime evidence.
