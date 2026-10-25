# I2D boundary1 — truthful evidence / validators, candidate PARTIAL

Source-only correction в `/tmp/qcl-docs-test-routing-worktree`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`. Governing I2C CPP
`caeb6ee6f85b19ba0fa2d748c1256aaac60c5497b829e70a1285cbe2f1f19a5f`.
**Не PASS/READY.** Реализован узкий boundary1 candidate; полный scalar/union
набор ещё не закрыт. Cleanup/publication boundary2, schedule boundary3 и full
C8 не заявляются завершёнными и не переделывались этим поручением.

Изменены ровно4native owning paths. Complete patch — **полный I2D delta от
exact frozen I2C четырёх файлов**, standard unified patch с labels a/path и
b/path;67002B, SHA256
`0ed917aaefeab58b04a661c6b2406f62a08846c669576d11576029794aee1c9b`.
Он не заменяет cumulative I2C237096B patch и не включает чужой FORMAT1.
Predecessor SHA каждого файла и итоговый SHA — companion identity.

I2C report/identity/patch остались56a4dc… /398e50… /7fd92c….
Pure файлы я не редактировал. Во время I2D Root отдельно выполнил свой
разрешённый FORMAT1 в shared worktree и подтвердил это сообщением: actual
helper теперь38a56bff… и fixture8946e323…, вместо frozen676a…/f02f….
Эти внешние изменения **не входят** в I2D native delta и не отменялись.
Native production import closure не увеличена; gitlinks/Root/CP/index не менялись.

## Исправленные поддефекты и граница проверки

Здесь «исправлен» означает добавленный source guard и подготовленный paired
control, а не independent CPP PASS или observed test result.

| Поддефект | Owning guard | Paired fixture | Remaining gate |
| --- | --- | --- | --- |
| Rejected validation ref превращал failed source read в measured | `run_phase:1619–1714`: отдельные source_bound/observations_valid/source_validated. Before required bind состояние сбрасывается; measured требует successful bind, validated native observations и full finish validation. Наличие ref ничего не повышает. | Python `test_version_parsers_have_full_match`: actual run_phase с injected Driver/native readers; final source throw после retained work даёт rejected validation ref, source not_measured, result failed, zero execute dispatch. | Fresh CPP; later finite DEV. Это status path с injected providers, не full C8. |
| Driver exit сам давал retention complete | `validate_phase_retention:1298`: actual index/readback, pending/command refs, bound ledger rows, raw SHA/bytes и supervisor reap/driver terminal proof; missing index→partial, invalid/unknown→unknown. `run_phase` запрещает positive result при incomplete retention. | Тот же owning run_phase control: missing index, driver close healthy; retention не complete, result failed, forbidden dispatch0. | Actual durable publication принадлежит boundary2, см. ниже. |
| Смешение retention и driver closure | `run_phase:1702–1714`: driver_closed устанавливается отдельно через strict actual terminal validator; receipt phase_driver_closure не выводится из retention label. | Исходный terminal proof healthy/EOF/reap pairs + injected terminal proof в run_phase status control. | Real drains/reap/cleanup — boundary2/native gate. |
| Bool-as-int, negative individual caps и malformed terminal | Central integer/finite_number/boolean/hash/enum/identity/exit/ref guards; `validate_terminal:1896`; `validate_request:1146`; observation tool/duration/UTC checks; resource/storage caps проверяют каждый value. | Existing Python terminal method: bool/negative pid/birth/exit; source-Git method: negative stdout with positive combined sum, bool stdout, negative stderr; invalid request must never reach grant authorization. | Full nested registration/receipt unions ещё не завершены. |
| Tiny unregistered task audit intent | `validate_intent:142` закрывает exact D5 bootstrap/phase union, refs/scalars/hashes/null branches/16KiB; RunningDocsSetup сохраняет ephemeral startup и передаёт **полную redacted phase projection** existing lease через durable_intent. Producer phase-intent также validated. Raw nonce/capsule/env туда не включаются. | Python forged-grant/intent method: bootstrap/phase same exact field set; raw nonce/token absent; bool version/extra tokens/null phase hash rejected. | Independent CPP projection/authority audit; actual trusted lease publication later. |
| TS responses не имели единого union reader | `responseFor:62` + checked transport: metadata/prepared/Git/capture/chunk/finish/refused exact top keys, common typed version/request/sequence, nested refs/streams/capture metadata/normalized metadata; malformed union fails before downstream parsing/execute. | Deno refusal case: metadata extra key, bool sequence, relative retained_ref, invalid cleanup enum и extra field rejected; existing no-prepare/no-execute assertion сохранён. | All semantic/dynamic map constraints не закрыты; no runtime execution. |
| Legal16KiB refusal превращался в cap error для Git | TS stdio reader `Math.max(normal cap,16384)`; normal response после union discrimination снова проверяется по своему smaller cap. ProtocolRefusal сохраняет code/ref/cleanup_status; native refusal_frame — exact bounded common union. | Deno typed-refusal pair для git-read; malformed fields rejected; healthy Git fixture теперь использует реальные32hex request/ticket IDs. | Wire-level4096…16384 refusal streaming и late delivery требуют finite DEV. |
| Native per-op scalar/header/read bounds | Native common version/sequence/index/offset typed; DriverPipe.receive выбирает finite reader envelope из allowed ops, первый union только preflight; each op smaller encoded cap проверяется до dispatch. Bounded refusal отправляется при matching known request where possible. | Existing framing/depth/finite controls и new typed cases. | Exact full ordinal operation/source slots остаются boundary3; malformed/EOF before request cannot produce matching typed reply. |

## Durable publication — явная dependency boundary2

Нынешний I2C `retain_record` ещё не имеет no-replace atomic publication и
directory fsync proof (P1-C). Source readback/file fsync не выданы за эти
свойства. Поэтому ActiveDocsAttempt создаёт **пустой native-owned**
`durable_publications` proof set; retention validator требует, чтобы все
required raw/index/command/closure refs были подтверждены owning publisher.
Текущий publisher этого **не делает**: ordinary native phase останется
retention unknown/failed, даже при healthy driver. Это намеренная честная
граница до boundary2, а не заявление нового healthy native acceptance.

Поле не загружается из descriptor/startup JSON; filename/hash или caller
boolean не заполняют его. Следующая owning publication correction должна
связать entries с **actual** successful exclusive atomic publication и
directory durability. Просто добавить refs в set без таких observations
будет тем же defect и не закроет boundary2. Текущий source candidate поэтому
не объявляется complete reachable healthy final route или native READY.

## Остаточные обязанности этого validator scope

1. Полный exact nested scalar contract parent registration/runtime manifest/
   initial-empty/allocation/control proofs и всех receipts ещё не завершён.
   Добавленные finite guards не являются доказательством всех possible unions.
2. TS metadata maps проверяются по нормализованной форме; descriptor-specific
   exact path/count/admission equality по-прежнему проверяет owning pure
   preflight. Полная independent native consistency matrix не получена.
3. Phase/setup receipt full exact unions на всех parent/client branches ещё
   неполны; dispatcher теперь отказывает positive outcome с unknown source/
   retention/closure, но полного reader closure этим не доказано.
4. Typed refusal не обещается при EOF/malformed frame до установления common
   request identity; cleanup/ref fallback остаются partial/unknown. First-FD,
   dual-store failure и safe error-preserving finalization — boundary2.
5. Новый run_phase control изолирует status propagation с mocked lower proof
   providers. Он **не** full parent/kernel/broker lifecycle; полного C8 нет.
   Ни native SourceGraph schedule, ни raw byte family freeze не исполнялись.

Основные evidence/scalar/union fixtures подготовлены перед соответствующими
production changes. Затем добавлены supplemental request/intent/status cases
при source inspection; они не выдаются за observed RED/GREEN.
Top-level denominators остаются8Python methods +8Deno registrations;
observed=null. Pure denominator230 — внешний Root format scope.

## Source phase и бюджет

Прочитан high I2C CPP, relevant owning sections, captured exact four-file
baseline и source diff/hash inventory. Git HEAD/status/submodule observations
повторены;8gitlinks прежние/uninitialized. Только source edits/read-only Git,
textual diff, SHA/wc/symbol inventory. Parser/compiler/import/scripts/tests/
Deno/Julia/native/network/server/CI/science=0. Syntax/type/format correctness
не заявляется. Source hashing — identity deliverables, не actual native source
freeze/measurement; physical thresholds не вводились.

Conservative content-read upper bound3MiB (<5MiB); CPU/RSS/physical I/O не
измерены. Cap20min/1CPU/1GiB, один finite pass; output≤192KiB. Сумма
report+identity+delta ниже cap. Старые artifacts не заменены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Rejected ref сам повышает source label | Новый independent source state + paired owning finalizer control | Не исполнено; CPP впереди | изменить |
| Unknown retention может дать positive phase | Actual ref ledger guard + explicit publication unknown + result gate | Durable publisher ещё boundary2 | изменить |
| Все validator unions завершены | Explicit residual list выше | Partial source candidate | данных недостаточно |
| Cleanup/schedule/full C8 закрыты | Не входят в I2D | Требуют своих finite boundaries | данных недостаточно |
| Native/CI/science выполнены | execution0 | Source-only | данных недостаточно |

STOP отдельный fresh high CPP; никаких product calls по I2D grant.
