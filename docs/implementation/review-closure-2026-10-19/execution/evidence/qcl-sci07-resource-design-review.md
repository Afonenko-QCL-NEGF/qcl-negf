# SCI07 — независимый high review resource/storage design

**Вердикт: REQUEST_NARROW_D2.** Один адресный P2 finding R1 в admission inequality нужно закрыть до переноса этого predicate в SCI08. Семь tickets содержат достаточные source loci и различающие controls для условного source I после этого уточнения; их наличие не закрывает native dependencies. Отдельный P3 provenance erratum R2 нужно сохранить при handoff. Физика, S1 caps и исходники не менялись.

Статусы SCI07 **needs_admission/needs_guard** обоснованны. READY, host capacity, работающий cumulative guard, native durability и scientific acceptance этим review не выданы. Свежие hypervisor/native данные reviewer не читал.

## Frozen inputs и фактический graph

| Артефакт | SHA256 |
| --- | --- |
| `/tmp/qcl-sci07-resource-design.md`,42322 B | `1f569ba726873d80715523621933caa6c0a0b0ad84e5a59ba9ef077b12001635` |
| `/tmp/qcl-sci07-resource-source-ledger.md`,11040 B | `cf625aefd68f7335e34a5cb07900ee743e8e6ba45142bd79dbe99c26824fedfe` |
| `/tmp/qcl-sci07-resource-design-identity.json`,22478 B | `0d652cf597008ce67957d99c22e81a3ad147e31fd1ce620ed2dbdcff2b6b2479` |
| Root `docs/implementation/review-closure-2026-10-19/science.md` | `0f52fc7148456b9eeff6bb993b5d1e701825781c58733dc519972c5312b8c26a` |
| Root `docs/implementation/review-closure-2026-10-19/operator-permissions.md` | `4887a5d4ad67a84424225d5b827ba2975ec97e319c94efe59a3e67b9120054a0` |

Прочитаны первичный D, science/P1, применимые audit skills/references и owning source. Source verdict установлен до чтения author ledger/identity. Skills: qcl-performance-audit и qcl-physics-audit; они не дают разрешения на runtime. Root architecture и границы owners учтены. No child agents.

Наблюдённый managed Root HEAD: `469ef4ec36c1dfb967856108e5f9455429559c15`. Read-only `git ls-tree HEAD` независимо подтвердил selected gitlinks:

- Core `9f4a96d032ad868ec010ce92d915bb81087c8d92`;
- Runner `fefaa27f194bfddf85dd51a0e255beef2218c06d`;
- Platform `f729e2681224d6537538179ab760fefefd575003`;
- AiiDA `d8f8092ca1c76523d85384b4bac8198d8bfa736b`.

Рецензент использовал `git show` этих immutable owning commits, не current mutable index. `git status --short` Root содержит coordinator execution/evidence edits, untracked DOC06 source/test и untracked состояние Contracts; они не scientific inputs, не изменялись и не дают clean/final release claim. Recursive submodule status соответствует восьми selected heads. Root graph identity не заменяет fresh runtime/release admission.

## R1 — P2: total capacity и remaining growth headroom смешаны в одном predicate

**Локатор:** D§6:233–236; downstream SCI08-R2/P1/C1 в D:356,358,361. Primary distinction: P1§S1 resident/copies/caps; Runner `point_artifacts.jl:536–545`, `scratch_execution.jl:47–53,76–79`.

D требует:

`existing resident + outstanding reserved growth + proposed growth + remaining stop reserve <= min(owned authority, free/quota after protected reserves, assigned attempt bound)`.

`existing resident` — уже занятые bytes. Filesystem free/available и quota remaining обычно уже исключают их. Подставлять эти remaining values в RHS total-resident comparison повторно списывает existing resident. Для SCI08 writer не определено, какой baseline подразумевается под `free/quota`: total authority или incremental headroom. Сходные input obligations D:128 прямо допускают quota hard **и remaining**, поэтому различие нельзя оставить reader inference.

Различающий scalar пример, без исполнения: existing resident=90 GiB, incremental reservations+proposed+stop=15 GiB, assigned total allowance=128 GiB, remaining allocatable headroom после остальных reserves=40 GiB. Total105≤128 и growth15≤40 помещаются; написанный predicate105≤min(128,40) отказывает. Это **conservative false refusal**, не обнаруженный путь превышения cap. Однако он противоречит заявленному exact-fit/one-byte-short смыслу guard и делает medium implementation неоднозначным. Native availability здесь не предполагается: числа только literal oracle.

**Минимальная D2-коррекция:** явно разделить два baseline-consistent predicate, сохранив все существующие caps:

1. `existing attributable resident + disjoint outstanding growth + proposed growth + not-yet-materialized stop growth <= assigned total resident authority/attempt cap` и отдельно shared campaign total≤2TiB.
2. `disjoint outstanding growth + proposed growth + not-yet-materialized stop growth <= independently remaining physical/quota headroom after other reservations/protected reserves` для соответствующего filesystem/quota domain.

Определить, какие outstanding tokens уже вычтены из reported headroom, чтобы второй раз их не списывать; либо использовать gross free и вычитать их один раз. Hard quota и remaining quota не взаимозаменяемы. Existing stop payload уже в resident не прибавлять заново. Поля logical/allocated physical и inode domains проверяются отдельно в их единицах; alias и cross-FS constraints остаются. Это уточнение resource baseline, без нового trust policy или physics decision.

В required controls SCI08-R2/P1/C1 добавить/уточнить paired scalar case: existing bytes>remaining free, но новое growth помещается; затем one-byte-short только одного соответствующего cap/headroom. Старые pre-prune/pointer/receipt controls сохранить. Никакие реальные arrays/FS/native calls для этой source correction не нужны.

## R2 — P3: chronology/source-graph erratum для handoff

**Локатор:** D§1:28–36 и identity `published_root`, `metadata_snapshot_later.head`, `metadata_snapshot_later.published_gitlinks`.

D честно описывает initial e22+owning overlay. Identity позднее связывает head469ef4e с `published_gitlinks`, где всё ещё старые Coree431609/Runner1acc165/Platformf5bc368. Это не actual tree469ef4e: независимый `git ls-tree HEAD` выше содержит9f4a96d/fefaa27/f729e26. Named source bytes при этом совпадают с заданным current selected graph — ошибка не меняет проведённый source review.

Сохранить immutable historical packet и добавить точный chronology erratum/new handoff binding: initial published e22 observation отдельно от позднего actual Root469 и его Git-derived links. Не называть старую таблицу результатом чтения tree469 и не превращать список reviewer hashes в новый composition lock. Это не основание молча объявить final release graph/runtime readiness; coordinator execution state остаётся dirty, final Code/release binding ещё обязателен.

## Проверка primary science/caps

P1§S: stationary thermal equilibrium0mV/period, lattice/LO70K, LO/acoustic/impurity/IFR/alloy, electron_electron=none сохранены. В этом resource review не изменяются grids/basis/window/embedding/mixing/thresholds и scientific gates. Zero bias не объявляется самодостаточным equilibrium proof.

P1§S1 и science Admission/guards совпадают с D§2:13 attempts/936 execution node-hours;72h/attempt; concurrency≤2; один node/threaded Julia process, BLAS1. W1=4 attempts/288h с128GiB/2TiB writes/4TiB reads/1GiB logs; остальные9=648h с256GiB/4TiB/8TiB/1GiB; shared resident2TiB,44TiB writes,88TiB reads,13GiB logs. Arithmetic4×2+9×4=44;4×4+9×8=88. Shared resident не получается суммой independent maxima; retained finals/failures не исчезают с job exit. Attempts/failure fingerprints/wave transitions не расширены. Stop time/bytes входят в те же limits.

Нет numerical verdict о total RSS, node count или available RAM/storage. Сообщение coordinator о newly connected hypervisor не является fresh allocation/cgroup/quota/admission packet. D не заимствует32 CPU/12VM как готовый grant и не выдумывает availability.

## Owning source: нагрузочные факты и limits

| Вопрос | Независимо просмотренный source | Вывод / предел |
| --- | --- | --- |
| Five-channel estimator | Runner auto_strategy149–173,229–253; Core production_cache431–608 | Actual enabled channels передаются estimator; resident/peak используют BigInt breakdown, candidate/warm-state/residual/FFT/workers. Smaller temporary chunks допустимы existing equivalent policy; не total RSS/audit/native capacity proof |
| Envelope / unknowns | Runner resource_contract18–54; linux_resources1–15,68–87,160–194; native_phase_telemetry138–210 | Explicit numerical/runtime/allocator sum≤hard полезен. Missing/malformed/max conflation, current→0 и unavailable phase paths существуют; strict admitted S1 refusal адресован R1 ticket, general low-level defaults не надо молча менять |
| Full native inventory | Runner hdf5467–516; point_artifacts808–851 |4 Green +15 scattering+9 embedding =28C при five-channel full state. Kernels/basis/history/metadata сверх этого. recovery.json — reference к тому же physics.h5, не ещё одна full copy |
| Serialization | hdf530–121,128–144 | Lossless split-complex, deflate1, reusable1MiB slab есть. HDF5/deflate/chunks/native memory и physical amplification не ограничены одним slab literal |
| Existing storage arithmetic | point_artifacts513–545,760–787 | Root filesize sum checked, forecast intermediates unchecked; free check лишь local observation; archive обходит recovery logical budget branch. Required overflow/fail-before-growth tickets обоснованны |
| Publication/pre-prune | point_artifacts986–1057 | Stage/verify→rename/fsync→readback→receipt→current/previous→prune; old pointers плюс new serialized metadata tail учтены. Pending full generation уже существует до final check: это не every-write enforcement |
| Recovery/scratch | scratch_execution34–112,134–136 | Controlled copy учитывает source+pending, free checks per block, repeated digests/verify/fsync. Recovery-enabled execution bypasses scratch and writes output directly. Ни quota, ни exclusion чужих writers этим не доказаны |
| Trigger multiplicity/final | scientific_execution1080–1162,1264–1278 | Timer, observer snapshots, SCBA/outer cadence, pause и terminal paths различны. Final full archive — отдельный mandatory branch;144 timer intervals не bound общего publications |
| Phase pressure/last state | scientific_execution1377–1400; native_phase_telemetry152–210 | Current mixed G/Σ нельзя признать checkpoint. Existing catch берёт latest_commit; stop reserve/no-state/real quiescence требуют явного guard, не allocation failure как normal pause |
| AiiDA consumers | validation76–104; calculation102–147; parser recovery/archive locators | One threaded process/BLAS1 request; optional max_memory_kb. Retrieval archive/recovery/executions/stdout/stderr и local recovery/prior-archive copies реальны. Request/list не capacity, не cumulative byte guard, не zero-cost parser/repository operation |
| Native mount/authority | Platform cluster53–75,89–100; storage17–25 | Declared cgroup-v2 constraints и hard NFS4/sync export есть. Actual installed limits/quotas/NFS completion/attribution не следуют из Nix. Existing cutover/job evidence helpers не являются campaign admission |

B0 literal arithmetic в D верна: C=16×30721×11×25=135172400B,28C=3784827200B,3×28C=11354481600B. Это uncompressed selected-fields planning inventory; compression неизвестна, HDF5 expansion/native metadata отдельно. Поэтому default8GiB не сертифицируется для2 retained+pending без дополнительных bounds. D корректно не называет uncompressed число measured compressed lower bound.

Core ProductionOptions100–101 подтверждает default outer5/scba25. Runner1151–1155 добавляет эти triggers поверх clock; observer1141–1146 имеет своё snapshot правило. D illustration128×floor(2048/25)=10368 cadence opportunities не означает ни actual config, ни разрешение такого write count. Per-event history growth/consolidation/readback/prune/hash должны входить в cumulative admission. D требует actual resolved event counts до допуска, а не выдаёт count144 за upper bound.

## Coverage/lifetimes и seven-ticket disposition

D§4–8 охватывает active/inherited/source/consolidated histories, retained/pending/final/failed/unacknowledged generations, pointer/receipt temps, logs/telemetry, recovery import, earlier archives, staging/retrieval/AiiDA repository/export duplicates. Сосуществование source/destination, per-FS identity, mount aliases, inodes, logical/allocated physical, copy/hash/parser/protocol costs и observer self-cost названы. No dedup/compression/prune credit без proof. Final/failed raw не удаляются ради fit. Post-exit readers несут debit исходного slot/campaign; новый host/agent не обнуляет counters.

Unknown/reset/wrap/stale/negative-delta/PID/boot/mount discontinuities сохраняют outstanding reservations, не возвращают missing tail как unused grant. Independent resident enforcement отделён от cumulative overwrite/read coverage. io.stat не назван NFS coverage; samples/free/quota не подменяют cumulative hard guard. Условная альтернатива storage-side attribution либо доказанно полная bounded-I/O coverage остаётся proof obligation: неизвестный механизм означает needs_guard, а не произвольный выбор medium writer.

Durable-stop reserve содержит time/CPU/RAM/disk/inodes/read/write/log и actual stop path; новые payloads включаются, если нужны именно этому stop. До первого checkpoint требуется explicit no-state, не fake resumable current state. Hard NFS + LAN/powerloss может не завершиться bounded-time; D сохраняет failed/unknown и не обещает direct-child kill как writer quiescence. Это sound refusal boundary, но native bound не доказан.

| Ticket | Source readiness после R1 clarification | Native/other dependency, сохраняемая явно |
| --- | --- | --- |
| SCI08-R1 checked forecast/strict S1 unknowns | Ready для tiny literal arithmetic/probe doubles и no-allocation sentinels | Missing source guard не становится current runtime proof; не менять standalone policy автоматически |
| SCI08-R2 common growth/resident gate | Ready после исправленного baseline predicate и scalar pairs; existing producer без второго writer | Full per-operation bound/FS attribution/liveness нужны до S1 admission |
| SCI08-R3 stop reservation | Ready для source ordering/no-state/last-pointer controls | Actual process-tree ownership, NFS blocking/quiescence и bounded stop остаются separate native gates |
| SCI08-P1 capacity/authority | Ready как fail-closed input/validation/admission work | Реальные inventory/cgroup/quota/storage/signing facts не могут быть заполнены из Nix или catalogue |
| SCI08-P2 cumulative/debits | Ready для fail-closed coverage/debit interfaces и fake counter controls | Выбор/доказательство actual attributable NFS mechanism остаётся prerequisite, не guessed implementation success |
| SCI08-A1 consumers | Ready для attempt-bound budget/copy lifetime checks у owning consumers | Real AiiDA/retrieval/repository/export placements/UUID только при actual node/receipt; Results source interface needs named owning review перед I |
| SCI08-C1 single campaign authority | Ready для existing authority reservation/reconcile controls | No new independent status journal; signed/fresh authority и durable ownership должны быть реально bound |

SCI08 source controls не расходуют исчерпанный C08 автоматически. Ссылки на existing C08 fixtures означают сохранение regressions/их исходников; любой новый runtime/fault check требует отдельного finite envelope coordinator. Общие≤2 code rounds и существующие scientific caps не размножаются tickets/агентами. Этот review не выдаёт новый test call.

## Независимо проверенные source hashes

Следующие SHA вычислены reviewer через `git show <pinned-ref>:<path> | sha256sum`; полные файлы использовались для hash, но semantic review ограничен named ranges выше. В таблице refs соответствуют четырём полным owning commits из начала report.

| Owner/path | SHA256 |
| --- | --- |
| Core `src/numerics/optimized/production_cache.jl` | `5c10eda35300c4c1fcbe46e23f0f95a3e9e9783b280504fc2dc4bd4575c70ee8` |
| Runner `src/application/auto_strategy.jl` | `810c72af8e4289c3dd61d4f49549a083568472646fa69eb625f41c5702840326` |
| Runner `src/application/resource_contract.jl` | `6be67c1ca1ded92b57063cec6e493a589c1520ccc282e569ca131b5f65effb8c` |
| Runner `src/infrastructure/resources/linux_resources.jl` | `eed7dc41e655fa94d3b29db514b5e5682e3023b862b91e53f58dbc18f3f363b8` |
| Runner `src/composition/native_phase_telemetry.jl` | `9605f1a4852f5edbe8ca83652500c2e0a2352feec7a04cf9d0e85bd0e712f173` |
| Runner `src/infrastructure/persistence/point_artifacts.jl` | `9e8c1d8f624bb828134129c10226211968360950cbac9ffd82e247a8ec294cd4` |
| Runner `src/infrastructure/persistence/hdf5.jl` | `d9ceeec9a76b8a7bc4c41eb24aaa2d4bb1fc1994cbce0407b9a344bdacb8d143` |
| Runner `src/composition/scientific_execution.jl` | `55a3737a35b21867d91992a2a3a7807729a3b9d83b0931006d99dc82addbf9cd` |
| Runner `src/composition/scratch_execution.jl` | `cad52756bb47a6d1fa63cd8c86a03c4e4dcd0d9a4e12383a0671dd766697f395` |
| AiiDA `src/aiida_qcl_negf/calculation.py` | `677eccfcf211b24230d8cb912955d2ec80a508d2d31d4e60d81cfbd2db1a156c` |
| AiiDA `src/aiida_qcl_negf/validation.py` | `f646ec62add9f5720ca5f70bd91ff29a99f363eff3f5fe796a780389bb495e50` |
| Platform `modules/cluster.nix` | `2353d2013359e720cd5712a27827dbd47a611996623db4b483b5a1c250a0f636` |
| Platform `modules/storage.nix` | `1518be74a9c353adaa547047635dc5bbd90cda0374ac50ce08d0631bf44eb0b1` |

Дополнительно semantic excerpts: Core production_contracts85–125; Runner results125–148; AiiDA parser named recovery/archive checks; Platform host_storage_receipt header/identity и slurm_job_evidence1–65. Они не полного audit отдельных modules, не pipeline/native proof.

## Ресурсный ledger и окончательное решение

Полные underlying files начислялись для каждого repeated hash/rg/nl/sed/cat; не только printed ranges. Known named-content charge1,334,625B, плюс131072B reserve для metadata/locator/малых неинструментированных reads; conservative upper bound **1,572,864B** <6,291,456B. Git-object decompression/physical I/O/CPU/RSS не измерены. Часть ранних multi-source outputs truncation: cited D middle ranges затем прочитаны отдельно; truncated author output не заменяет semantic evidence.

Envelope≤25min/1CPU/2GiB/read6MiB/output192KiB; no target runtime/import/parser/tests/build/network/server/native probes/Git mutations/CP/code edits. Только requested review artifacts. Не использованы ни science attempts, ни C08 calls, ни final CI.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| S1 model/caps сохранены | P1/S1, science Admission/guards, D§1–2 | Actual resolved/runtime artifacts отсутствуют | сохранить |
| Required lifecycle/trigger/cumulative/stop domains названы | Owning sources и coverage table выше | Их actual bounds/enforcement ещё не получены | сохранить |
| Admission predicate однозначен для medium I | R1: total resident сравнивается с remaining free/quota | Conservative false-refusal, ambiguous exact-fit baseline | изменить |
| Root/source handoff chronology точна | R2: initial e22 vs later469/old links; current tree проверен отдельно | Source pins совпадают, current final release не принят | изменить |
| Seven guard tickets можно реализовать условно | D§9 + ticket dispositions | R1 fix и native prerequisites обязательны; runtime grants отдельные | сохранить после уточнения |
| Native capacity/counters/durable stop доказаны | Reviewer native access0, D unknowns | Fresh inputs и coverage proof отсутствуют | дополнительно измерить |
| SCI08/S1/physics READY достигнут | Только source/design packet | needs_admission/needs_guard; no science acceptance | данных недостаточно |

STOP. Requested correction — baseline-consistent inequalities/controls и chronological erratum; не новый resource policy, не новый scientific approval и не product implementation.
