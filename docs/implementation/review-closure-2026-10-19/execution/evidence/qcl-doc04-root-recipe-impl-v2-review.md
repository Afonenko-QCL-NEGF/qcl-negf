# DOC04 I-Root v2 — focused independent high source re-review

**R1 CLOSED_SOURCE, R2 CLOSED_SOURCE.** В точных v2 bytes оба конкретных замечания I1 устранены на уровне исходников. Новых блокирующих замечаний в этой узкой correction не найдено. **Общий I-Root остаётся PARTIAL / NOT_READY**: source integration и внешние BUILD prerequisites не закрыты; общего PASS и runtime verdict нет.

## Identity и scope

Проверен `/tmp/qcl-doc04-root-recipe-worktree`, HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`. Status содержит ровно три прежних untracked files: `docs/public/make.jl`, `ops/docs.ts`, `tests/docs_recipe_orchestration_test.ts`. Gitlinks не менялись; Core `9f4a96d032ad868ec010ce92d915bb81087c8d92`, Runner `fefaa27f194bfddf85dd51a0e255beef2218c06d`, submodules не инициализированы. Ни owning default profiles, ни общий SourceGraph этим re-review не переаттестованы.

| Frozen input | SHA256 |
| --- | --- |
| `ops/docs.ts`, 16757 B | `0837ceda6be4fbfbd90e411fe6e4fe665f8bc8979e63ac1fbfe6bacedd8b178a` |
| `tests/docs_recipe_orchestration_test.ts`, 11328 B | `697b1774ee0573acfc6ec5e5c6ebf4b3c922fb6588cc9d291deab2f10f3408c3` |
| Unchanged `docs/public/make.jl` | `b673bf4e2ba53179bccd7dcff631c8c1fe03893944cf2add868155e133705c8b` |
| v2 complete patch, 33380 B | `aef4548dbd662d201057dbe5c92b71767d9fdd55df3893c1b788adeff5f06585` |
| v2 report | `12f05352105dc6c86b53de6cc66d83ec4199c1c0a09bd324d0628398b08c526b` |
| v2 author identity | `17479b52402cd8a2a57c394af559abc1a6a5dcf101f15e580d4f907f1de3cbe0` |
| I1 independent review | `6c405424aad14554e579f31c9675969ba0510e43abd4b17326c22ff10f9e1f3b` |
| I1 independent review identity | `4fd0d4ff100f56e4257d52f7bc16025f31206b62438689a5fef74b2dca9f8bdd` |

Исходный I1 review сохранён. Здесь проверены full v2 TS sources, соответствующие source contracts и hashes; I1 architecture/design/recipe выводы использованы как уже прочитанный контекст, без нового broad audit. Полная проверка содержимого complete patch против отдельной reconstructed tree не выполнялась; individual actual source hashes сверены напрямую.

## R1: actual bounded reads

I1 R1 закрыт source correction в `ops/docs.ts:261–304`:

- `readBounded` проверяет cap/expectedSize до allocation. Один buffer имеет размер cap+1. Каждому read передаётся view длиной не больше min(65536, оставшиеся cap+1 bytes); actual увеличивается только на проверенное положительное целое число не больше view length. При cap+1 немедленно возникает overflow error. Whole-file `Deno.readFile` в production input/inventory paths отсутствует.
- EOF раньше/позже expectedSize при actual≤cap даёт `source_changed_during_read:277`. Таким образом маленький stat больше не позволяет неограниченное чтение выросшего файла. Нулевой cap допускает только пустой файл плюс один overflow sentinel.
- `finally:279` закрывает owned reader на success, invalid limit/metadata, read error, invalid progress и overflow. В `readRegularBounded` metadata failure до передачи владения закрывает handle через `finally:304`; после передачи `readBounded` закрывает его сам, прежде чем выполняется final lstat. Двойного обычного close path не видно.
- `readRegularBounded:282–301` проверяет nonsymlink regular path/ancestors, metadata открытого handle и повторного path lstat, dev/ino/size, затем final regular-kind/dev/ino/size/mtime. Metadata/access exceptions не превращаются в success.
- `inventoryTree:243` передаёт remaining total tree byte budget; при overflow traversal прекращается. Успешные файлы входят в total по actual bytes. `boundedFile:307` использует тот же reader.

Новые controls `tests/docs_recipe_orchestration_test.ts:114–144` различают metadata1/actual>cap4 (получено ровно5 bytes и close), валидные ненулевые [81,82,83], и growth within cap с отказом/close. Это meaningful source fixtures: возврат к whole-file/metadata-only модели нарушил бы явно проверяемый read count contract. Source покрытия всех close/error branches не заявляю: success-close/read-error/invalid-progress отдельными assertions пока не проверены, хотя finally виден непосредственно в коде.

Границы сохранены честно: эти metadata checks не устраняют symlink replacement между проверками, concurrent same-size overwrite, hardlink/bind aliases или отсутствие exclusivity. Один buffer cap+1 и возвратная копия ограничивают собственные byte buffers примерно 2cap+1, но не устанавливают total process RSS. Ни `Deno.open/stat/read`, ни injected reader не имеют здесь I/O wall deadline. Это закрытие фактического byte-allocation замечания; не finite filesystem wall-time sandbox и не BUILD admission.

## R2: retention evidence и detached terminal result

I1 R2 закрыт source correction в `ops/docs.ts:120–220`:

- Result отдельно хранит received, attempted/reserved и acknowledged bytes по каждому stream. Reservation ограничивает общий cap; ack увеличивается **после** успешного `await save:175–177` и только до terminal state. Reservation больше не выдаётся за сохранённые данные.
- Rejecting sink оставляет ack0 для этого write и `failed_unknown_partial`; это правильно допускает частичную физическую запись до rejection. Catch объединяет reader/sink error консервативным unknown-partial статусом; он не заявляет известную нулевую потерю.
- При drain expiry выставляется terminal, вызывается cooperative AbortSignal и reader cancellation, возвращается `incomplete_unknown_partial`. Эффективная остановка зависшего sink не заявляется. Late physical writes допустимы согласно ограничению, поэтому result не является доказательством immutable terminal log payload.
- Terminal guards `157,167,176,182,189–190` не допускают поздних обновлений counters/errors/exit. Return `214–220` содержит numeric snapshots и копии errors/exit. Snapshot отцеплен от асинхронного состояния; это source observation, не measured concurrency test.
- `process_tree_terminated` и `resource_measurements` остаются null. Save acknowledgement не доказывает fsync/durable storage, а retention=`acknowledged` подтверждает только выбранный capped prefix; log_cap reason и received>ack остаются видимыми.

Усиленные controls достаточно различают исходный дефект. `tests:70–83` требует точные ненулевые stdout[11..16] и stderr[21..23], ack6+3 при received8+8, stream tags и отдельный failed exit. Удаление save или сохранение нуля байт больше не удовлетворит source assertions. `85–95` требует stdout[31,32,33], stderr attempted8/ack0 и failed_unknown_partial. `97–112` требует сохранённый stdout[41,42], incomplete/deadline/unknown-partial, затем неизменность result после release зависшего sink. AbortSignal не проверяется отдельным fixture assertion, но передача signal и abort на incomplete видны в source; это не новый blocker исходного R2.

Spawn failure до создания result, filesystem sink completion/abort, effective descendant termination, output/scratch resource enforcement и production terminal-receipt wiring остаются прежними открытыми контрактами. Узкий source closure R2 их не закрывает.

## Общее состояние и следующий конечный source ticket

`buildBlockers:100–110` сохранён; `preflight:317–338` всегда blocked, source graph null, admission null, steps пусты. Старый unbounded buffered sourceGraph/run не импортирован и не вызван. Caller marker не создаёт BUILD READY. Operator recipe byte-exact I1; прежние Module[]/sitename/guard выводы не изменены этой correction.

Следующий минимальный source contract: **bounded SourceGraph runner seam + before/after identity control**, при сохранённом blocked BUILD. Owning ticket должен разрешить нужный path `ops/git.ts` сверх текущего трёхфайлового scope, сохранить существующие clean/gitlink/URL/nested-submodule проверки и общий SourceGraph format, определить injected argv runner, capped stdout/stderr/deadline/error receipts. Fake Git control должен менять source graph либо input hash между двумя снимками и проверять failure binding, сохранность original attempt и отсутствие candidate. Это source/API работа; внешняя inventory/admission не заменит её. Исторический buffered default не должен вызываться из нового docs path. Actual execution такого control требует отдельного finite envelope.

Отдельный assembly/schema owner должен дать accepted complete entrypoint/transport/error contract и shared validation binding. Existing pure plan loader не равен final admitted assembly API. Root actual staging/readback, recipe dispatch, plan/effect manifest validation, full input recheck, actual Julia guard sentinels и production runner/wrapping остаются source implementation gaps.

Nested/dynamic docstrings/import/cache, installed Documenter/toolchain identity, assets/licenses/CSS, fresh inventory, namespace ownership/exclusivity и process-tree/network/CPU/RAM/wall/output budget — отдельные внешние evidence/BUILD prerequisites. Их отсутствие объясняет запрет BUILD, но не является оправданием незавершённых source integrations. BUILD/native/browser/public/scientific acceptance не измерены.

## Ledger и запреты

Только named source reads, text searches, SHA and Git/path metadata. Source/Git/CP edits, target runtime, Deno/Julia/Python/JS execution, parser/compiler/format/lint/tests, imports/render/build/native/network/server/science —0. Записаны только этот report и companion identity. Source fixtures не исполнялись: RED/GREEN/typecheck/test PASS не заявляются.

Для повторных чтений/hash/search консервативно предзаряжено512KiB из4MiB read grant; named source payload текущих двух TS+v2 report/identity/patch составляет71998B, старый review/identity и unchanged recipe малы и включены в резерв. Physical I/O/RSS и transport output отдельно не инструментированы; формальный enforcement PASS не заявляю. Review artifacts существенно меньше128KiB output cap. Исходный failed resource history не изменён.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 исправлен на уровне source | readBounded261–279; regular wrapper281–304; growth controls114–144 | No I/O deadline/TOCTOU/exclusivity/runtime proof | сохранить |
| R2 исправлен на уровне source | separate counts125–131; save175–177; terminal202; exact controls70–112 | Ack не fsync; sink может дописать позже; execution отсутствует | сохранить |
| Operator/default scope не изменён correction | Unchanged recipe hash и прежние gitlinks; три owning paths | Не новый полный owning-profile review | сохранить |
| Полный I-Root READY | Missing graph/assembly/schema/staging/runner/recheck/sentinels | R1/R2 closure не закрывает orchestration | изменить |
| BUILD/native/public/science выполнены | Execution receipts отсутствуют | Этапы не запускались | данных недостаточно |

STOP. Два concrete findings закрыты source-only; общий PARTIAL / NOT_READY сохраняется.
