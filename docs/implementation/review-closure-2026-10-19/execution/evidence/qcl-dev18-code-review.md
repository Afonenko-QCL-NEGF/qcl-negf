# DEV18 CP-CODE: независимая проверка исходников

Вердикт: **production source соответствует принятому DEV17; runtime acceptance pending GREEN2**. В production-коде блокирующих замечаний не найдено. В замороженном новом fixture найдено одно воспроизводимое расхождение H01 между literal ожидаемой YAML-кодировкой и контрактом встроенного codec. GREEN1 не является pass; existing integrity fixture в нём не была исполнена. Требуется отдельный разрешённый bounded GREEN2 после указанной узкой коррекции.

Этап: read-only code review, без Julia/import/тестов/сборки/solver, без изменений исходников и Git. Создан только этот review artifact. Сначала прочитаны AGENTS.md, docs/architecture.md, owning durability contract, CP-DESIGN и production source; авторский отчёт прочитан после самостоятельной оценки source и 55 cells. Применимых вложенных AGENTS.md в Runner не обнаружено. Рецензент не делегировал работу.

## Точная идентичность среза

Worktree `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Фактический root HEAD `7d179b28647f0b89347d2d6358f08cf2fe479653`; Runner checkout HEAD из recursive submodule status `647055e6bed794ddfc15f0bca4e18468195079df` с изменённым `src/infrastructure/runtime/filesystem_repository.jl` и untracked новым fixture. Источником проверенного candidate являются следующие SHA256, а не предположение о clean HEAD:

| Артефакт | SHA256 |
| --- | --- |
| `src/infrastructure/runtime/filesystem_repository.jl` | `44a1d6e907b985bdcd5fb89b73a50ca434ab6209462564d63936562317521849` |
| `test/infrastructure/runtime_checkpoint_durability_faults.jl` | `4e74a26ab5caf80e12ddae3e85ca4b3bb793081686bd0bbaeeb0fa35028ac429` |
| `docs/runtime-checkpoint-durability.md` | `d6df20992e22296eeeaa38d80919b39f6d439788a4ab7f4dceb942324f139ffc` |
| `/tmp/qcl-dev17-design-review.md` | `bbe7e46b440db2d02a361949cfa55e7ab7895bb470375bfc5af0038308f0eadb` |
| `/tmp/qcl-dev18-full.patch` | `7b699bfa2e4bc129a1c2303ed7382917c46b43f44966c49c577cd9356e0875bf` |
| existing `test/infrastructure/yaml_repository_provenance_spans_and_checkpoint_integrity.jl` | `a672cc8313f92446b05778422c9d23408f47983782da0dc14822c94d92bc45ef` |
| unchanged `src/infrastructure/persistence/atomic_files.jl` | `7bfdcf14c2cee4a2c6fa63d0c739ed6c93f1d74b729a5abd3d22a9220eb6a9a4` |
| GREEN1 original log `/tmp/qcl-DEV18-GREEN-1/original.log` | `6bf402e734e539fab69afffc8f3eb5393a9384c0257bb91fcb164d28aa2cb9b1` |

Git inspection была только read-only; root status содержит также другие component/evidence changes, которые этому checkpoint review не приписываются. Source hash сверён непосредственно с файлами, patch hash также сверён.

## Production protocol

`filesystem_repository.jl:673–769`, `_save_runtime_checkpoint!`: проверка Unix, identity, positive non-Bool Int-representable attempt/iteration, portable kind/metadata выполняется до mutation. Полный save под `repository.lock`; private `_checkpoint_active` запрещает reentry до allocation. `finally` снимает active, `lock do` освобождает lock; cleanup/delete и маскирующей вторичной операции нет.

Anchor вычисляется до `mkpath` (589–602,699–700). Payload writer должен завершить закрытую запись; regular/nonlink и chmod0640 идут до hash/file fsync. После одного publication rename синхронизируется полная цепочка каталогов от checkpoint directory до anchor включительно (714–740). Затем separate metadata temporary получает закрытую YAML-запись, regular/nonlink, chmod0640, file fsync, rename, final checkpoint directory fsync (742–754). Только после повторного YAML-чтения, canonical equality с ожидаемым envelope и проверки actual payload identity/bytes/SHA возвращается reference (756–763). Codec reader writer-readback повторно не вызывается.

Private publisher (535–555) требует same-directory source, regular nonlink, absent destination включая dangling symlink и вызывает ровно один `jl_fs_rename`. Нет `mv`, post-fsync chmod, copy/delete/retry fallback или overwrite существующего destination в разрешённой single-writer постановке. Это не конкурентный POSIX no-replace primitive; cross-object/process/machine coordination остаётся precondition.

File fsync проверяет syscall result (511–518). Directory fsync (520–533) захватывает errno до close и сохраняет первый fsync error, если close тоже отказывает. Writer readback с `preserve_read_errors=true` сохраняет исходные parser/I/O exceptions; явные integrity failures остаются `CheckpointIntegrityError`. Уже опубликованные файлы, partial temporaries и старые поколения не удаляются. Allocation 392–411 учитывает named payload/metadata orphan; повторный save не переиспользует orphan generation.

## Reader и compatibility

`load_latest_checkpoint` (773–795) валидирует explicit `expected_attempt` до directory listing. Default `nothing` сохраняет cross-attempt resume. Guard mismatch (629–630) после проверки envelope и до payload/codec вызывает locator-bearing `CheckpointIntegrityError(..., "attempt mismatch")`. Bool/zero отвергаются, отсутствие metadata возвращает `nothing`.

Последний metadata filename выбирается без fallback. Filename/generation correspondence (470–473), metadata regular/nonlink (624–625), payload regular/nonlink, length и SHA (642–648) проверяются до decode. Parse/read/envelope/decode failures нормализуются в `CheckpointIntegrityError` с locator; `InterruptException` пробрасывается (604–613). Reader не исправляет файлы и не стартует fresh state при corrupt latest.

Три существующих coordinator callsites (`coordinator.jl:441,516,560`) используют default; checkpoint status сохраняет `checkpoint.attempt` (149–157). Они не выдают новую exact-attempt гарантию. Schema/reference/wire fields сохранены. Generic `_atomic_yaml`, `_immutable_yaml` и `_atomic_replace_file` не менялись; scientific generations, receipts, pointers/current/previous, HDF5/model/discretization/acceptance не затронуты.

## Независимость и покрытие 55 cells

Fixture включает реальный solver-independent composition module; не подменяет Core/HDF5/package. Independent oracle (43–86) сам перечисляет metadata, выбирает latest, читает raw YAML/payload, проверяет literal schema/identity/generation/attempt/basename, regular files, length и SHA. Он не вызывает production load/validation/reference/hash helper. Общие YAML/SHA libraries явно ограничивают независимость; это не независимая реализация криптографии/parser.

Подтверждены 20 C +9 E +16 R +2 guard R +5 H +3 L =55 отдельные деревья. C проверяют все десять cuts на empty/old baselines, exact trace и отсутствие acknowledgement; E различают ENOSPC/EIO и readback same-size corruption; R отдельно вызывают production reader и проверяют zero decoder calls; H требуют complete exact expected bytes/hash и public state; L различают task serialization, release after failure/orphan allocation и same-task reentry. Старое literal generation snapshot проверяется побайтно. E09 вызывает действительную writer readback failure, а не fixture-only assertion. Полный healthy ancestry trace не допускает пропуска intermediate parents.

## Единственное finding: H01 literal encoding

Локатор: frozen fixture SHA `4e74a26…`, `runtime_checkpoint_durability_faults.jl:342–348`, конкретно `complete(r,1,1,NEW)` на347; byte/hash assertions125–126.

H01 вызывает встроенный `YamlCheckpointCodec` со state `Dict("state"=>"new")`. Production `_write_checkpoint_payload(::YamlCheckpointCodec)` делегирует `YAML.write_file`, который сериализует string scalar в quoted representation. Literal `NEW="state: new\n"` на9 предназначен для остальных raw Callback writer cells и не описывает встроенный YAML writer. GREEN1 log показывает actual `state: "new"\n` и ровно два провала125/126; state roundtrip и trace H01 при этом прошли. Это ошибка expected encoding fixture, не основание менять production serializer или durability protocol.

Допустимая узкая коррекция: только H01 передать independent `complete` literal `"state: \"new\"\n"`, сохранив raw `NEW`, все остальные cells, точное byte/hash сравнение и production source неизменными. Expected bytes нельзя извлекать из production output или вычислять вызовом codec. После этой правки требуется новый fixture/fullpatch hash и фактический GREEN2; данный review ещё не утверждает её выполнение или pass.

## Фактический GREEN1 и ограничения

По независимо прочитанным `/tmp/qcl-DEV18-GREEN-1/receipt.json` и complete original log:3197pass/2fail/0error, exit1;55cells дошли до L03. Wall18.252s, sampled peak process-tree RSS530972672B, sampled owned TMP283633B, raw9646B; guards/overrun отсутствуют. Это измерение root, рецензент повторно тесты не запускал. Exception завершения первого include остановила второй include: existing integrity fixture в GREEN1 **не запускалась**.

Receipt sampling50ms не доказывает отсутствие transient memory/TMP peak, hard cgroup/disk quota отсутствуют. Source-selected execution не подменяет native owning-package acceptance. Synthetic live-process cuts не моделируют исчезновение dirty pages, NFS coherence, device/power loss. Гарантия условна для local POSIX fsync/rename, trusted real/stable ancestry выше anchor, closed codec handles и одного writer между object/process/machine. Никакие scientific/numerical/model/experimental gates или S1 этим review не закрыты.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Production candidate реализует принятый scoped durability/failclosed protocol | exact source SHA44a1d6…, перечисленные symbols/order и55cell source review | runtime gate пока failed по fixture H01 | сохранить |
| H01 expected YAML bytes ошибочны | literal NEW9, встроенный codec345, assertion347/125–126, GREEN1 raw | нужна ровно одна узкая encoding correction | изменить |
| 55-cell runtime packet принят | GREEN1 3197/2, complete raw | GREEN2 после correction ещё не измерен | дополнительно измерить |
| Existing integrity fixture прошла | в GREEN1 второй include не выполнен | фактических pass данных нет | данных недостаточно |
| Native/NFS/power-loss durability и научная приёмка установлены | свидетельство отсутствует | source и synthetic cuts не заменяют native/scientific evidence | данных недостаточно |

STOP. Review frozen до отдельного exact-delta/actual-GREEN2 follow-up. Source/Git/test executions не выполнялись.
