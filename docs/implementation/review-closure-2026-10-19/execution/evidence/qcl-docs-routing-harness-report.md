# Локальный routing engineering harness v1 — только подготовка

Подготовлены Python guard и отдельный finite plan. Target/fixture/helper imports,
Deno/tool/version invocations, target parsers/tests/build/native/network=0.
Product/checkpoint, Git index/commit/push не менялись. Это предложение для
независимого high review; READY не создан и ни один attempt не зарезервирован.

Root checkout HEAD e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1; исходный dirty status
сохранён. Frozen routing worktree HEAD e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b,
status содержит только untracked tests/docs_test_routing_test.ts. Все восемь
root gitlinks прочитаны git submodule status --recursive; не обновлялись.
Architecture и D1/D2/accepted D2 review/v2 fixture report/accepted v2 review прочитаны.

Fixture SHA04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3,
38723B,227 nominal registrations. ops/docs_tests.ts отсутствует по retained review
и initial status; harness заново проверяет его отсутствие до RED. Количество227
не measured engine result. RED ожидает missing helper diagnostic до регистрации;
этот loader failure не является выполнением227 assertions.

Exact child command (single file, typecheck включён):

```text
/nix/store/xn4n2ijvg7pq49qm8kl5252j21sq3g3m-deno-2.8.3/bin/deno test --no-config --no-lock --cached-only --no-npm --no-remote --no-prompt --reporter=tap /tmp/qcl-docs-test-routing-worktree/tests/docs_test_routing_test.ts
```

Deno SHA cdd88de791341a151d80ee5c189abb4b7681beb0aca9f5c1a4b0f4fe9429e26c
задан из поручения, binary при подготовке не читался и не запускался; guard
проверит digest перед child. CLI source loader может читать module source;
script allow-read/write/env/run/net/ffi не выдаются. Нет deno task, directory
search/discovery, --no-check, --filter, --only, arbitrary command или target unit.

Два exact attempt: DOCS-ROUTING-RED-1 и DOCS-ROUTING-GREEN-1. Каждый имеет
отдельную exclusive mkdir reservation /tmp/qcl-ATTEMPT; повторное имя отвергается.
No aliases/fallback/retries. Exact --scope docs-routing-pure-local-engineering-v1
и --execute обязательны. Fresh Root READY (≤300s) связывает scope/phase,
harness/plan/fixture/runtime hashes. RED требует helper absent/null identity;
GREEN требует exact helper hash и canonical owned bounded /tmp/qcl-docs-* review
reference с hash. READY — active Root authorization consistency, не доказательство
native admission или доверия к произвольному caller JSON.

Перед GREEN независимый reviewer должен установить self-contained helper closure:
только fixture→ops/docs_tests.ts, без дополнительных local/npm/remote/static/dynamic
imports и без import-time product/native execution. Review ref/hash сам по себе
не доказывает это условие. Новый helper либо дополнительные imports требуют
новой source binding/review, не implicit source-loader permission expansion.

Child env полностью заменяется ровно DENO_DIR/TMPDIR/HOME с новыми owned0700
children в attempt/owned-tmp; ambient PATH/loader/DENO/NODE/PYTHON fields не
наследуются. Все три каталога входят в общий16MiB TMP census, вместе с файлами,
каталогами и symlink lstat.st_size metadata; directory symlinks не обходятся.
Reviewed regular-byte sampler SHA16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e
и RawCapture module SHAe88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f
проверяются перед guarded import и после child. Guard dependencies сейчас не
импортировались. RawCapture пишет merged stdout/stderr побайтно и дренирует EOF
на success/error, включая fallback при thread-start failure. Original log/receipt
сохраняются; никакой cleanup результатов не выполняется.

На каждый child:120s,1CPU affinity+RLIMIT_CPU120s,1GiB sampled RSS stop,
16MiB sampled owned TMP stop,2MiB raw envelope с128KiB early-stop reserve.
Polling50ms, terminal observation обязательна даже для fast child. Все source
bindings проверяются до/после; receipt содержит raw digest/size/completeness,
stop/error/exit и measured samples. CPU affinity ограничивает параллелизм;
RSS не является hard peak, RAM/TMP не являются cgroup/disk quotas. Output/TMP/RSS
могут перескочить stop threshold между samples; overrun остаётся failure с
original output, не выдаётся как truncate+complete. Census st_size — logical
metadata/payload, не physical allocated storage. Same-user trees не являются
adversarial race sandbox. Process-group kill не доказывает production tree
supervision; это узкий trusted permissionless engineering child.

Guard return0 означает только завершённый captured engineering call без guard
failure, включая ожидаемый nonzero RED. Он не означает unit pass. Receipt
observed_engine_tests=null и unit_result=requires_independent_raw_report_review.
Root должен отдельно проверить RED diagnostic либо GREEN complete TAP227/all
passed/zero failures/skips/ignore/todo/cancel и источник. Unknown layout/counter,
nonzero GREEN или unrelated RED failure не дают pass и не разрешают retry.

Finite plan сохраняет original DOC04/DOC06/native/build/full-CI caps. Pure GREEN
не закрывает actual task/workflow/CLI integration, production admission/native,
sole final CI и scientific acceptance. После каждого call STOP и review evidence;
эта подготовка не запускает следующий этап.

Подготовка ограничена named source reads с консервативным reserve≤1MiB<2MiB;
physical I/O/CPU/RSS не измерялись. Совокупные owned output artifacts<96KiB.
Первый combined source read был слишком объёмным и tool display его обрезал;
последующие focused reads дочитали нужные основания. Совокупный terminal display
не инструментировался, поэтому отдельное соблюдение96KiB display bound не заявляю.
Code source прочитан при генерации; harness/parser/typecheck/self-tests не запускались.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Finite deny-permission harness подготовлен | Exact source/plan hashes в identity; fixed argv/attempt/scope | Независимый high source review ещё требуется | дополнительно измерить |
|227 tests или RED/GREEN выполнены | Execution0, observed count=null | Только nominal reviewed source count | данных недостаточно |
| Raw logs, source equality и sampled limits будут фиксироваться | Guard source, digest-bound RawCapture/sampler, terminal observation | Runtime пока0; sampled caps не hard quotas | дополнительно измерить |
| Existing native/full-CI/science budget сохранён | Plan явно отделяет2engineering calls; original caps unchanged | Ни integration, ни native readiness не приняты | сохранить |

STOP для независимого high review. Не создавать READY и не запускать этот guard
на основании данного author report.
