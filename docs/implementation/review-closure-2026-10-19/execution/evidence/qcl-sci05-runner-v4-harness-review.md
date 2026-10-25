# C08 Runner harness v4: narrow independent source review

2026-10-19. **PASS — narrow CP-SOURCE изменение sampled owned TMP 16→128MiB.** Допустимо внутри явно перепланированного единственного call7 после fresh admission/source/target binding. C08 reviewer=0. Runtime и combined target results не проверены.

Primary inputs прочитаны до вывода: actual accepted-v3→v4 diff, harness guard composition, explicit `/tmp/qcl-checkpoint-C08-runner-TMP-replan.json`, existing `test/infrastructure/bounded_portable_recovery.jl:92–117`, unchanged sampler source. Никаких Python/Julia imports/parser/target tests/build/network/server/Git mutations/children не было. Sole output — этот report.

| Source | SHA256 |
| --- | --- |
| `/tmp/qcl-julia-c08-runner-v4.py` | `30054fe5c1ab3e7e7136057924c5a29d439958a115ec07da8333a885ad2ba5d3` |
| `/tmp/qcl-julia-c08-runner-v4.diff` | `a6ce662d7dc2bb748a4daa195fc9968f46600039e8abceee14365b4a857891a6` |
| Accepted `/tmp/qcl-julia-c08-run-v3.py` | `d454f20503108bfa7b40df921b7e4acf4fd4d049bbaf1801c4a3a05de36ad112` |
| Unchanged sampler `/tmp/qcl-owned-temp-sampler-v2.py` | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |

Diff ровно в двух literals: `temp_peak > 16*1024**2` заменён на128MiB и receipt `limits.temporary_bytes` заменён согласованно. Других изменений нет. CPU affinity1, Julia/BLAS/OMP threads1, offline prepared project/depot, RLIMIT_CPU570/575, wall trigger570, sampled process-tree RSS4GiB, raw8MiB threshold/post-drain predicate, RawCapture byte-preserving path, stop/kill/drain/final wait behavior, fail-closed guard errors и receipt facts byte-exact accepted v3. Runtime setup/install не добавлены.

Existing bounded_portable_recovery fixture использует finite budget32MiB и один повторно используемый sparse padding file; logical st_size при reached publication boundary намеренно доводит tree до32MiB. Sampler суммирует regular-file logical st_size и поэтому старые16MiB конфликтовали с неизменяемым существующим engineering control даже при малом physical disk allocation. Named replan разрешает128MiB только owned task TMP для одного combined call7, оставляя room для retained tiny producer/owned copied negatives. Нет основания менять test, scientific arrays, model, native experiment/campaign storage/I/O caps либо допуски.

Это **sampling limit**, не hard filesystem quota. Sampler не следует symlinks, считает regular logical bytes, терпит concurrent ENOENT; прочие ошибки попадают в guard. Нет adversarial namespace guarantee, physical storage bound или transient peak proof; explicit paths вне TMPDIR не измеряются. Intended retained producer root `/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture` лежит внутри measured tree только при exact task/attempt admission. Harness сам не закрепляет список пяти конкретных targets и env: fresh admission обязан связать intended two Core manufactured files, new reviewed Runner N1, existing portable и archive preflight с exact byte hashes и prepared dependency sources. Review двух literals не является независимой новой проверкой этих пяти tests либо их исполнения.

Accepted-v3 timing caveats сохранены: 570s wall trigger + nominal cleanup waits до23s =593s плюс sampling/read/write/scheduling overhead. Нет hard realtime ten-minute deadline proof; non-daemon RawCapture/fallback cleanup caveats не исчезли. Ordinary bounded stop path сохранён, runtime completion не предсказан.

Shared C08 max8/used6 не изменён. Перепланирование не разрешает rerun, дополнительный call, solver или full CI. Reviewer ничего не запускал. Этот report не объявляет root/source tuple release-ready.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Изменён только finite owned TMP sampling threshold | Exact two-line diff и receipt literal | Не hard quota/transient proof | сохранить |
|128MiB имеет конкретную engineering причину | Existing reused32MiB sparse boundary и explicit replan | Actual combined peak не измерен | дополнительно измерить |
| Остальные guards сохранены | Byte-exact remainder accepted v3 | Runtime/cleanup/native behavior не проверен | сохранить |
| Call7/source/native/science acceptance выполнены | Запусков нет | Требуется fresh admission и реальные raw/receipt | данных недостаточно |

**A STOP.** Narrow source PASS; no C08 consumed. Далее reviewer переходит к отдельно порученному DOC04 B без исполнения A.
