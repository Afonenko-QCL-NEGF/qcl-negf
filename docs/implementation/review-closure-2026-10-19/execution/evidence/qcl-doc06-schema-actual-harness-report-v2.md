# DOC06 corrected actual9 replay: separate source-only packet v2

2026-10-20. **STOP_SOURCE_ONLY_FOR_SEPARATE_HIGH_REVIEW**. Подготовлены новые plan, preparation и guarded launcher; snapshot не создан, scripts не импортированы/скомпилированы/исполнены. Root code/CP, unit scripts/outcomes и old namespaces сохранены. Этот packet не READY и не execution grant.

## Source identities

| Artifact | Bytes | SHA256 |
| --- | --- | --- |
| `/tmp/qcl-doc06-schema-actual-plan-v2.json` | 3962 | `1f0f73b9216aa097a1b86ba455192820b6ebb872a8d7d9d57e1b5b682ccecceb` |
| `/tmp/qcl-doc06-schema-actual-local-run-v2.py` | 21737 | `322c38d71f67c037e780e0f811b8ea67cd863d61f9a1bf7690391ffdaf3976f8` |
| `/tmp/qcl-doc06-schema-actual-preparation-v2.py` | 11134 | `55dba3288b2c1e8fbf84f6f03d2cda171d0466107d60db26fbd4746e175bd9b0` |

Requested published Root `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0` в `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`; это exact target нового packet, не старый author2bb или executionb079. На future readiness/prelaunch/terminal scripts проверяют actual read-only Git HEAD==c5ef. Source-only preparer текущий HEAD не probe-ил.

Adapter pinned `a852318af5105aaf224913e2264342c4349cb0ed70991842f00ab78e4d6c4b72`; test binding `45febb3ccfdd9d641447d5cec6e26bbfc6c9b97f188c2e9a620142794c1a3b31`. Tests не исполняются. Source CPP2706…, final format review0130…, outcome reviewee8620… связаны exact path/SHA в plan и проверяются future READY. Outcome review сохраняет unit74/74 software evidence при failed resource guard29valid+1unknown; не объявляется resource closure и не разрешает unit retry.

Прочитаны old launcher/preparation/control/plan и metadata original `/tmp/qcl-DOC06-ACTUAL-2bb05d3-v1`, high actual source review `97efc49edccf2ae54fb67189c09792971e796d1991e6659c3fa2e6bad17403b0`, meaning review `4c35b2517718e3b9a137047a45652c4924de7e21ae3ad9041cd8d1e90df56861`. Old control CP-writing logic **не перенесён**. Старые actual attempts и M1/M2/M3 negative evidence не переименованы.

## Finite identities и будущая последовательность

Namespace только `/tmp/qcl-DOC06-ACTUAL-c5ef91f-schemafix-v2`. Preparation ID DOC06-SCHEMA-ACTUAL-PREP-1: максимум1export,120s/1CPU, bounded9source≤512KiB/per-file128KiB, input receipt16KiB/preparation32KiB. Старый aggregate245338B — ориентир; новый фактический aggregate вычисляется из selected objects, не приравнивается без чтения.

Product IDs DOC06-SCHEMA-ACTUAL-A1 и A2: по1call, каждый120s/1CPU/1GiB sampled process-tree RSS/16MiB sampled owned regular TMP/1MiB original raw. No automatic retry/fallback attempt/alias; oldunit2/2, oldE1, currentfailedE1 и oldactual2/2 сохранены. Нет solver/CI/C08/source-tool/unit reopening.

Future argv, только после отдельного high source review и fresh Root READY:

- `python3 /tmp/qcl-doc06-schema-actual-preparation-v2.py /tmp/qcl-doc06-schema-actual-prep-READY-v2.json`
- `python3 /tmp/qcl-doc06-schema-actual-local-run-v2.py DOC06-SCHEMA-ACTUAL-A1 /tmp/qcl-doc06-schema-actual-A1-READY-v2.json`
- `python3 /tmp/qcl-doc06-schema-actual-local-run-v2.py DOC06-SCHEMA-ACTUAL-A2 /tmp/qcl-doc06-schema-actual-A2-READY-v2.json`

Preparation BASE.mkdir(exist_ok=False) permanently reserves namespace; each product permanently reserves own attempt folder before READY/dependency checks. Reservation failure never reuses existing folder. Root alone issues READY, executes and reconciles calls; scripts never touch CP. Failed/inconclusive artifacts remain; no rerun.

## Exact Git export и Root R1/R2

Preparation derives8 gitlinks from `git ls-tree -rz HEAD components`; each of exact9allowlisted owner paths reads committed regular100644 Git blob at corresponding gitlink. Size checked before reading, aggregate bounded. Snapshot bytes written readonly; graph/input receipt/preparation are derived ephemeral evidence, not a manually maintained revision lock. Unrelated component working files/submodule updates/checkout do not enter authority. Administrative Git uses GIT_OPTIONAL_LOCKS=0, GIT_NO_REPLACE_OBJECTS=1 and isolated Git config; no network.

After export preparation itself rereads exact Git objects and checks full snapshot inventory/no symlinks, graph bytes/manifest/source bytes. `preparation.json` status prepared_exact_Git_R1_candidate содержит binding with root_head,graph_sha256,input_receipt_sha256,files map{sha256,bytes},aggregate_source_bytes. Exporter verification is not independent Root R1.

**Root R1 explicit prerequisite:** before A1 READY Root independently reads root tree/gitlinks and all9 Git blobs, compares every exported byte, graph/manifest/preparation linkage and exact inventory, then writes its own readback JSON:

```json
{
  "status": "exact_Git_R1_verified",
  "preparation_sha256": "<SHA of new preparation.json>",
  "binding": "<full object with root_head, graph/input SHA, files map and aggregate>"
}
```

`binding` должен быть JSON object, здесь placeholder только для описания. Root uses `git ls-tree -rz c5ef… components`, per-owner `git cat-file -s/blob <gitlink>:<relpath>`, raw byte equality, hashes and no-extra-files enumeration; это реализуемый read-only workflow без old Root-control/CP writes. READY.root_r1_readback={path,sha256} binds that independent record. Launcher then independently repeats `exact_binding()` at before/after, so supplied Root readback не заменяет Git equality.

**Root R2:** A1before=after=RootR1binding; A2 requires A1 receipt guarded_pass=true/complete_partial_projection and READY.prior_receipt_sha256. Guard enforces prior.before=prior.after=current A2before, then A2after=before. Root separately rechecks captured records after each call before admitting A2. Failed A1 cannot unlock A2; no gap repaired by repeated execution. Output byte equality remains later separate postprocessing, not acceptance inside launcher.

## READY contract

format `qcl-negf.doc06-schema-actual-ready.v2`; coordinator_authorized=true; exact id/root_head=c5ef/script_sha256/plan_sha256; source_review={path,sha256,status:accepted}; evidence_sha256 exact plan evidence map; created_unix age≤300s; phase-specific limits exact plan map. Preparation limits map keys wall_seconds/CPU_count/source_cap/file_cap/receipt_cap. Product keys wall_seconds/CPU_count/sampled_RSS_bytes/sampled_TMP_regular_bytes/raw_bytes/sample_seconds. Product additionally preparation_sha256,input_receipt_sha256,root_r1_readback ref; A2 prior_receipt_sha256. No READY written by this packet.

## Resource/capture/failure honesty

Pinned Deno2.8.3/runtimeSHA unchanged. Runtime hash streamed64KiB; helper/sampler exact bounded bytes SHA checked then same buffer compile/exec in fresh non-main ModuleType, no importlib/pyc. Those execution statements only authored as source here. Child env fixed HOME/TMPDIR/DENO_DIR inside owned attempt, updates disabled, BLAS/MKL/OMP/Rayon1; no inherited env. Deno run no-config/no-lock/cached-only/no-npm/no-remote/no-prompt; read only trusted adapter+snapshot+input receipt+ownedTMP, write ownedTMP only; no env/run/net/FFI. Exact selected nine source strings remain inert. Trusted adapter execution is the only intended product call.

RSS starts null, successful/failed counts and errors/gaps explicit. Immediate postspawn sample before poll, loop and live terminal samples; missingVmRSS stores timestamp/PID and available status fields, never0. Any sampling error or zero valid measurements fails NotCapable. Old failedE1 policy не ослаблена. TMP startsnull and prelaunch/loop/terminal samples enforce same16MiB threshold. Parent and child affinity1; finite CPU limits retained. RSS/TMP are sampled lower bounds, no hard transient peak/disk quota guarantees.

Original RawCapture full drain/fallback retained, raw stop headroom128KiB and overrun honest failure. Raw above1MiB kept untouched and metadata marked overrun_retained_not_summarized with SHA unknown; within cap raw/status parsed as bounded bytes, facts/output receipt32KiB each and linked SHA/bytes checked. Meaning/all10/locators/privacy comparisons are separate later checks, not inferred from CLIexit0 or identical bytes.

All work after permanent reservation has outer best-effort failure path, including tmp/seed/log creation, capture.finish, terminal binding, hashes/readback and receipt persistence. Finalization steps guarded independently; missing raw/hash/measurements stay null/not_measured. Tries receipt.json then failed-receipt.json and explicit stderr fallback with consumed identity/Root reconciliation if I/O prevents persistence. No impossible unconditional durability claim. Failure outcomes remain failed/inconclusive, and no duplicate is authorized.

## Source self-review и пределы

Только own source text generation/reads and SHA/metadata, no new script import/compile/AST/target parser/harness/selftest/runtime/Deno/Julia/network/Git/actual/snapshot execution. No Root source/CP edits. Code text reviewed for old namespace/HEAD/hash leakage: only new namespace/Root and final source bindings used. Source input revisions derive from Git; no manual component SHA table added. Existing records retained.

Logical source read conservative≤2MiB under4MiB; wall<12min;1CPU/1GiB; report<192KiB. Physical CPU/RSS/I/O не измерялись. Helper generation scripts manipulate only inert own strings/plan JSON; они не запускают prepared guards. Runtime/fault-injection correctness не установлена — отдельный high review следующий gate.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| New exact9 export/currentRoot binding подготовлен | Graph/object derivation + full before/after equality in source | Snapshot/export ещё не созданы | дополнительно измерить |
| R1/R2 prerequisites implementable и обязательны | Root readback contract + guard exactGit verification + prior A1 continuity | Root должен выполнить independent reads | сохранить |
| Unit resource gate закрыт/replayed | Outcome reviewee8620…:29valid+1unknown failed | Никакого новогоunit scope | данных недостаточно |
| Actual projections/meaning приняты | Product executions0 | Два future calls и independent meaning review отдельно | дополнительно измерить |
| CI/native/science/C08 закрыты | Таких gates здесь нет | Engineering source-only packet | данных недостаточно |

STOP для separate independent high source review.
