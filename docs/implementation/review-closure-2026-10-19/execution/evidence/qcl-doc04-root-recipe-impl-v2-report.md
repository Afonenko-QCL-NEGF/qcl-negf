# DOC04 I-Root v2 — узкое source-only исправление R1/R2

STOP для отдельного independent high review. Общий статус остаётся PARTIAL /
NOT_READY; runtime evidence не получено. Изолированный HEAD неизменен:
`b07974b8e46bf8afdf1740947b842669a62a5ccc`, ветка
`codex/review-closure-doc04-root-recipes`. В этой фазе изменены только
`ops/docs.ts` и `tests/docs_recipe_orchestration_test.ts`.
`docs/public/make.jl` byte-exact сохранён:
`b673bf4e2ba53179bccd7dcff631c8c1fe03893944cf2add868155e133705c8b`.

## Первичные замечания и исправления

Review `/tmp/qcl-doc04-root-recipe-impl-review.md`, SHA256
`6c405424aad14554e579f31c9675969ba0510e43abd4b17326c22ff10f9e1f3b`;
companion identity SHA256
`4fd0d4ff100f56e4257d52f7bc16025f31206b62438689a5fef74b2dca9f8bdd`.
Первичные R1 locators: I1 `ops/docs.ts:223–228`, `207–214`.
Первичные R2 locators: I1 `tests/docs_recipe_orchestration_test.ts:69–79`,
`ops/docs.ts:160–163,176–188`. Это старые locators frozen I1, не номера v2.

R1: `readBounded` v2 `ops/docs.ts:261` читает incremental в один buffer cap+1,
подставляя remaining view ≤64KiB в каждый read. Совокупные фактически полученные
байты ≤cap+1; extra1 — явный overflow sentinel, после которого немедленный отказ.
Short reads не создают новые chunks/неограниченную очередь allocations. Результат
копируется в массив actual bytes: peak собственных byte buffers ≤2cap+1.
Handle закрывается в finally на success/error/invalid metadata/read error.
Mismatch actual length и expectedSize отвергается даже при actual≤cap.
`readRegularBounded:281` проверяет observed nonsymlink regular metadata до open,
по открытому handle, повторный lstat и после чтения; observed dev/ino/size/mtime
changes отказывают. Metadata/access failures не подменяются success.
`inventoryTree:243` использует общий remaining tree byte budget, `boundedFile:307`
тот же reader; whole-file Deno.readFile в обоих production paths удалён.

Эти проверки не доказывают отсутствие TOCTOU, concurrent same-size overwrite,
symlink replacement between checks или filesystem exclusivity. Не вводился
O_NOFOLLOW/openat sandbox или deadline для underlying filesystem read. Конечный
byte/allocation bound не равен гарантии конечного I/O wall time. Missing external
namespace/resource binding сохраняется; no BUILD dispatch.

R2: `FiniteResult:125–131` разделяет received, attempted/reserved и acknowledged
bytes по streams. Reserved ограничивает общий cap; acknowledged увеличивается
только после успешного `await save`. Sink rejection оставляет zero acknowledged
для этого write и `failed_unknown_partial`: sink мог записать часть до ошибки.
Deadline/drain expiry даёт `incomplete_unknown_partial`, cooperative AbortSignal
и bounded return. Поздний sink вправе физически завершиться: effective cancellation
не заявляется. После terminal guard поздние callbacks не меняют counters/errors;
returned result копирует exit/errors и содержит только numeric snapshots.
Это не доказательство immutable terminal log payload или остановки descendants.

Controls сначала усилены, затем исправлен implementation; execution RED/GREEN не
выполнялся. v2 fixtures: точные nonzero stdout[11..16] и stderr[21..23] при cap9;
received8+8 против acknowledged6+3. Zero-retention реализация провалит exact bytes
и acknowledged assertions. Rejecting sink требует stdout[31,32,33], ack3+0,
stderr received/attempted8 и unknown-partial failure. Hanging sink/deadline требует
stdout[41,42], ack2+0 и snapshot неизменности после release. Reader growth fixture
с metadata1/actual stream>cap4 требует actual consumed5 и закрытый reader;
отдельный fixture отвергает growth within cap. Valid read сохраняет [81,82,83].

## Identity, сохранность и проверки

Новые hashes:

| Файл | SHA256 |
| --- | --- |
| ops/docs.ts,16757B | 0837ceda6be4fbfbd90e411fe6e4fe665f8bc8979e63ac1fbfe6bacedd8b178a |
| tests/docs_recipe_orchestration_test.ts,11328B | 697b1774ee0573acfc6ec5e5c6ebf4b3c922fb6588cc9d291deab2f10f3408c3 |
| v2 complete patch,33380B | aef4548dbd662d201057dbe5c92b71767d9fdd55df3893c1b788adeff5f06585 |

I1 report/identity/complete patch сохранены с первоначальными hashes соответственно
`dbcb6dbb7463839d95bda76b70b989ba90c6787444cf025d4d7bfaa7c34c3f1f`,
`4320cfcaa0a7f5962c046b2ef81ea517e43ecf2a4d91d1afe54a13911135a006`,
`6f2e25ab81a25223f957d92edee7fab6ea34400bd22eb46ec92bda16156a0b81`.
V2 complete patch содержит полный трёхфайловый I-Root delta от HEAD, включая
неизменённый operator recipe; это не изменение owning scope данной correction.
Git status по-прежнему ровно три untracked files; index/commit/CP не изменялись.

Выполнены только named source read/edit, SHA checks, Git metadata и whitespace
проверки двух изменённых files через git diff --no-index --check: без диагностик.
Target runtime/parser/compiler/format/lint/tests/Julia/import/render/build/native/
network/server/science =0. Test source не является test PASS. Independent review
ещё предстоит. No READY/overall source acceptance.

Envelope этой новой фазы10min,1CPU,1GiB,read2MiB,output128KiB. Консервативный read
reserve1MiB покрывает named review+identity, I1 artifacts hash pass, два source
extract passes, apply_patch reads, final SHA/search/patch passes. Physical I/O/RSS
не измерялись. Output complete patch33380B плюс report/identity <128KiB.
Original phase failures/history не изменялись; новый budget не retroactive PASS.

## Остаточные gaps

Always-blocked CLI сохранён. Не добавлены API/dispatch/новые trust predicates.
Все I1 gaps остаются: bounded sourceGraph binding; accepted complete assembly /
shared-schema validation APIs; plan/effect/source validation; actual owner staging
и readback; nested docstring/import/cache/assets/toolchain proofs; fresh external
admission/exclusivity/process-tree resources; recipe dispatch, final input recheck
и immutable candidate; actual Julia sentinel/source-change controls. Spawn-failure
production receipt и effective sink/descendant cancellation не заявлены закрытыми.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Actual read bytes ограничены cap+1 | readBounded261, calls243/307; growth fixture114 | Source only; I/O wall/TOCTOU не доказаны | сохранить |
| Acknowledged retention больше не равен reservation | FiniteResult125; ack после save; nonzero fixtures69/85/97 | Sink failure/timeout явно unknown partial | сохранить |
| Возвращённый snapshot не меняют поздние callbacks | terminal guard202, copied fields214; hanging fixture97 | Physical sink may still complete; no immutable-log claim | сохранить |
| Полный I-Root orchestration готов | Missing API/integration/evidence gaps выше | Узкая correction не закрывает их | изменить |
| Runtime/build/native/science выполнены | Execution отсутствует | Not measured | данных недостаточно |

STOP для отдельного high source review R1/R2 на точных v2 bytes.
