# I2F: конечный source-only correction packet B1r+B2a/B2b/B2c

Статус: **source candidate, STOP для fresh independent high CPP**. Runtime,
native READY и scientific acceptance не получены. HEAD worktree:
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`.

## Входная identity и граница владения

Worktree `/tmp/qcl-docs-test-routing-worktree`. Прочитаны его AGENTS.md,
docs/architecture.md, применимые TDD/systematic-debugging инструкции. Source-only
запрет исполнения имеет приоритет над runtime шагами RED/GREEN навыка: fixtures
написаны, но RED/GREEN не наблюдались. Другие агенты не создавались.

Приняты bounded I2E review SHA256
`c8224246cc32b3327680841a292a9b232fa82b87834ad52067577b1805827e62`,
его review-identity `3aa4e19f53e445c95c73bba9b5f53c17d491e6e37b5e05f10108fc1ea2122d36`
и отдельная author-identity
`569fd093509c4d388b51c4be40bd82b502b3e212ee43a63b924892b6232a194a`.
Accepted D4/D5/D6 не переоткрывались. Перед первой правкой четыре exact I2E
файла скопированы в `/tmp/qcl-docs-routing-i2e-frozen-before-i2f`, manifest
проверен `sha256sum -c`: четыре OK. Это сохранение входных bytes, не новый
проектный lock-file ревизий.

Изменены только ops/docs_tests_native.py, ops/docs_tests_cli.ts,
tests/test_docs_test_native.py, tests/docs_test_native_protocol_test.ts.
Root-owned pure файлы сохранены с SHA256 `68f0efb5b45a03f130a52d14279e427c83c11b317a3c244e43375dbac5b8d3f5`
и `2639be2132a88adb3e1ccd204112180efa065089e9ade5cae87e38c970952f99` соответственно.
Исходные незакоммиченные config/workflow/ci/git изменения не менялись;
index, CP, сервер, submodules не менялись. Все восемь gitlinks остаются
uninitialized, как при начале. Git status сохранил прежний набор путей.

## Что меняет packet

**B1r.** `validate_registered_shape`, `read_registered_payload` и `same_record`
применяются к actual initial-empty/allocation/admission до использования.
Registration вызывает те же validators. Сравнение canonical JSON bytes
устраняет Python aliases False/0, True/1 и 1.0/1; coercion не добавлена.
Runtime manifest и reviewed-unit actual records тоже сравниваются canonical;
expected_tests получает integer validation. Accepted finish-validation binding
проходит validate_binding. Actual setup ACK получает typed version/PID/birth/UID,
finite phase list, capsule identities и запрет duplicate phases. CLI actual start
проходит startFor с integer/hash/enum guards.

**B2a.** `cleanup_stage` хранит первый и bounded secondary stage/error identities
(до16 различных пар, поля32 символа), независимо пытаясь следующие stages.
Private worker разделяет TERM/drain/KILL/reap, pipes/raw/selector/gate/owner close,
raw reread и transport settlement. Ошибки reread больше не заменяют первичный
failure и не выходят до terminal serialization. Partial originals остаются на
диске; worker failure/transport failure receipts публикуются existing owning
publisher. Неуспешный frame write не вызывает ожидание ACK. Already pinned
pidfds получают попытки сигнала даже при новом census failure; отдельный
ошибочный PID не исключает остальные. Reap отдельно обрабатывает leader poll,
census и известные UID/birth identities.

Parent execute закрывает gate и пытается bounded waitpid даже после fork-success
с birth/pidfd/attach failure; dispatch остаётся закрытым. Ошибки signal/wait не
пропускают FD/channel closes и fallback. Sole subreaper принудительно не убивается;
unknown ownership остаётся задачей существующего outer watchdog. Active command
независимо пытается raw и metadata settlement, сохраняет original execute error,
не освобождает reservation при неизвестном actual объёме или failed commit,
пытается сохранить command-settlement failure record. Driver adopted reap error
не прерывает последующие cleanup stages. Повреждённый старый phase ref больше не
прерывает setup fallback readback/publication loop.

**B2b.** Actual private fork-child вызывает FD census до worker/gate/command,
сохраняя только stdio, exact private channel и gate. CLOEXEC не используется как
замена fork closure. Gate закрывается после чтения. Все inherited FD close
attempts выполняются, а non-EBADF failure предотвращает dispatch.

**B2c.** `validate_terminal_retention` связывает producer evidence.streams с тем
же typed closure.streams; перечитывает actual originals, проверяет SHA/length и
publication proofs именно этого manifest. Producer caps остаются262144 на stream.
Для каждого participant проверяется pinned identity, closure, raw_complete,
originals и proofs; retention_status сам по себе не является доказательством.
Participant list ограничен256, duplicates запрещены, все parent pinned leaders
должны присутствовать. Participant existing closure caps24MiB stdout/262144stderr
не увеличены. Phase/setup receipts не требуют собственных будущих SHA и не
переписывают ранее опубликованный positive phase.

## Fixtures и выполненная проверка

Новые finite source fixtures расширяют существующие8 Python methods и8 Deno
registrations. Добавлены actual storage-reader positive/negative пары для bool/
int/float aliases, actual accepted finish-validation binding, ACK malformed
version/PID/phases и actual CLI start. Actual fork-child seam проверяет closure
producer/broker FD и FD65537 перед worker. Fake OS/process matrix проверяет
birth/pidfd/attach errors после fork, original exception, gate/reap/close,
worker observer→secondary drain/signal/reap/close/reread errors и terminal frame,
доступные reservation stages после partial/commit/release/stat failure. Retention
fixtures используют actual validator с producer/participant identity mismatch,
different stream map, missing proof/raw и raw_complete=false.

Сделаны только text/hash/Git reads и правки. Четыре `git diff --no-index --check`
не выдали whitespace diagnostics; frozen manifest проверен. Выполнение fixtures,
парсинг Python/TS, import, compiler, prepared scripts, runtime, native, сеть,
сервер, CI и science: **0**. Номинальные counts не означают observed coverage.
Полная failure-permutation/runtime/C8 матрица не заявляется доказанной.

## Сохранённые остатки и ledger

B3 exact ordinal Git schedule/debits, failed-call raw/time accounting,
protocol stdout physical-domain binding, полный storage/metadata/aliases trace
и independent source-status truthfulness остаются отдельным packet.
B4/full C8 factory→broker→driver→D6 manufactured route и последующий конечный
DEV8+8/compiler admission остаются отдельным packet. Existing trusted external
provider всё ещё prerequisite actual BIND: реализация provider/broker/trust
architecture не добавлена. Все historical failures/caps сохранены. Product calls87
и source calls7 не увеличивались.

Бюджет поручения25min,1CPU,2GiBRAM, read≤8MiB, output≤256KiB. Консервативный
верхний read estimate4MiB; CPU/RSS/physical I/O отдельно не измерялись. Первые
batched source reads дали truncation; точный aggregate byte counter transcript
не снимался, поэтому соблюдение output cap по всему transcript **не подтверждено**.
Дополнительных runtime calls для устранения этой неопределённости не было.

Complete I2E→I2F delta: `/tmp/qcl-docs-routing-impl-i2f-complete.patch`,60319bytes,
SHA256 `1ac2e0b556153a05905542c01ce606d10bb5b10bb20cbdb225293a34e2ade464`.
Exact four-file manifest — companion identity; дальше только fresh high CPP.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Actual nested JSON aliases закрыты | Python validate_registered_shape/read_registered_payload; CLI startFor; новые storage/ACK/finish fixtures | Source-only, не наблюдались RED/GREEN | дополнительно измерить |
| Cleanup продолжает независимые stages и сохраняет primary | Python cleanup_stage, _CommandOwner.signal/reap, _capture_worker, execute_bounded, ActiveDocsAttempt.command; fake OS matrix | Нет native/process execution, bounded diagnostics | дополнительно измерить |
| Private fork не удерживает чужие control FD | Actual child census до worker, exact keep set; FD65537 fixture | Реальный fork не выполнялся | дополнительно измерить |
| Producer/participant originals замкнуты на exact closure/proofs | validate_terminal_retention и _await_terminal callers | External provider/runtime не наблюдались | дополнительно измерить |
| B3/full C8/native READY закрыты | Перечисленные отдельные остающиеся gates | Packet их не реализует и не исполняет | данных недостаточно |
| Independent source verdict получен | Этот author packet передан Root | Fresh high CPP ещё нужен | дополнительно измерить |
