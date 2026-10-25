# I2G: I2F-R1 healthy-return cleanup propagation

**Source candidate; STOP для fresh high CPP.** Worktree
`/tmp/qcl-docs-test-routing-worktree`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`.

Входной I2F review SHA256
`c74872ae57d8da9a3b6c0384a131f84d65a71102da57f3606da901ac4d79cab0`,
review identity `c8c918b7e6292f40d90b29be32b80f3012746c54902f017a4ea90296b174e2a4`
проверены. До правок сохранены exact четыре I2F файла в
`/tmp/qcl-docs-routing-i2f-frozen-before-i2g`; manifest.sha256:4 OK.

Исправлен только I2F-R1. `ActiveDocsAttempt.command` импортирует
`launch_state.failures`, записанные actual `execute_bounded.finally`, прежде
чем может выдать ticket. Healthy capture с pidfd/channel close failure теперь
получает overall outcome unknown и Refusal после остальных settlement attempts.
Good raw bytes, их SHA и уже опубликованный successful command receipt не
меняются. При исходном execute exception сохраняется тот же exception object;
owner cleanup failures входят в bounded secondary history.

Отдельный owning settlement record публикуется по `<id>.settlement.json` с
primary/secondary, owner history, pending_ref, original terminal_ref и streams.
`entry.failure_ref` связывает его с native ledger. Failed row command index
ссылается на этот SHA и suffix settlement.json; исходный good receipt остаётся
доступен через ledger/settlement original terminal_ref. Healthy index row и
positive capture contract не менялись. Ошибка самой failure publication остаётся
unknown, не превращается в successful command.

Fixture написан перед production correction и проходит actual
execute_bounded→ActiveDocsAttempt.command. Mock заменяет только OS/process/
storage boundaries; actual raw/record publishers, hashes, propagation и index
writer сохранены. Пары: healthy baseline; sole pidfd-close fault; sole parent
channel-close fault; original terminal-observe RuntimeError плюс pidfd-close
fault. Проверяются отсутствие positive ticket, unknown ledger, primary/secondary
ordering, последующие close и raw/metadata settlement attempts, exact неизменные
good receipt bytes/hash, raw bytes/hash и actual failure-ref в опубликованном
index. Старый settlement fixture адаптирован к actual fixed-path publisher.

Изменены только ops/docs_tests_native.py и tests/test_docs_test_native.py.
Оба TS файла побайтно сохранены; exact manifest содержит все четыре paths.
Номинальные8 Python methods и8 Deno registrations сохранены. Pure pair другого
writer не читался и не менялся. B1r/B2b/B2c не переоткрывались; B3/B4/provider,
CP/index Git, config/workflows, сервер и gitlinks не менялись. Index в тексте
выше означает runtime command evidence index, не Git index.

Проверка: text/hash/Git reads, frozen manifest4 OK и два diff --check без
whitespace diagnostics. RED/GREEN не наблюдались: source-only поручение
запрещает imports/parsers/compiler/scripts/tests/runtime/native/network/CI и
science; все эти execution counters0. Product89/source8 не увеличены,
mathGREEN90 не использован. Native READY не заявлен.

Бюджет8min/1CPU/1GiB/read≤2MiB/output≤64KiB; короткие outputs без truncation.
Точные aggregate CPU/RSS/physical-I/O/transcript-byte counters не измерялись;
строгую метрическую аттестацию cap не заявляю. Никакого исполнения для проверки
этих counters не добавлено.

Complete I2F→I2G delta11988bytes,
SHA256 `6d35679f6c0b06242b8f876c72769968b2adfb73f5ce3d097bd691c18c39558f`.
Exact four-file hashes находятся в companion identity. Следующий шаг — только
fresh independent high CPP на этом manifest.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Owner close failure запрещает positive ticket | Imported launch_state history, actual execute→command fixture | Source-only, fixture не исполнялся | дополнительно измерить |
| Good raw и successful original receipt сохранены | Immutable publisher path, fixture сравнивает exact bytes/SHA | Нет runtime evidence | сохранить |
| Failure связан с ledger/index, original primary сохранён | failure_ref, settlement.json row и paired original exception | Fresh CPP впереди | дополнительно измерить |
| Native READY/full C8/provider BIND получены | Не выполнялись | Отдельные сохранённые gates | данных недостаточно |
