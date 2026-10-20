# Routing RED fixture v2 — узкий независимый high source review

Вердикт: **PASS_SOURCE** для correction scope R1/R2. Blocking findings в проверенной delta отсутствуют. Это допускает отдельный Root bounded RED, но не является выполненным RED/GREEN либо доказательством actual integration/native readiness.

## Набор исходников и метод

| Артефакт | SHA256 |
| --- | --- |
| Current fixture `/tmp/qcl-docs-test-routing-worktree/tests/docs_test_routing_test.ts`,38723 B | `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3` |
| Immutable v1 `/tmp/qcl-docs-test-routing-red-v1-test.ts`,33358 B | `f3db415342457e3f05434f5ed5e3c49f83796f6d91eddffdd76846363b64f0c5` |
| `/tmp/qcl-docs-test-routing-red-v2-delta.patch`,7284 B | `9bdfa42f1dbc3ca7e104ea7ca8bef24e11faa124368a7d54ff1b205db35fd0c9` |
| Prior independent review `/tmp/qcl-docs-test-routing-red-review.md` | `705bea4364bbaf6053fd51cb7ea7acb48a2776d19e8f6002f9dddbd7e6302eb7` |

Нормативная база сохранена: D1 `fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270`, D2 `bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70`, accepted D2 review `939555c9291e98be1200b063bcf06e344a7597907dfbf498bf28029927728967`. Эти ранее прочитанные контракты не пересматривались.

Сначала прочитаны actual source regions и delta; выполнен текстовый `diff -u` exact immutable v1/current. Author v2 report прочитан после независимой проверки изменений. Diff совпадает с предоставленной delta по changed hunks. HEAD остаётся `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`; status содержит только untracked requested fixture. Импортов/парсеров/target execution не было.

## R1 закрыт

`absolute source path` теперь меняет одну entry, сохраняя12 entries и остальные11 entries побайтно по serialization assertion (current:347–358). Потеря всего source closure больше не является посторонней причиной отказа этой строки.

Test-only `relocatedStorage` (160–181) одновременно перепривязывает descriptor storage, directory keys/canonical values, absence paths и admission.exclusive_storage. Synthetic admission reference digest меняется согласованно в трёх местах: descriptor ref, observed file hash, normalized admission.ref. Source graph/revision/source_files не менялись; новый parse/preflight получает новый descriptor, старый ready outcome не переиспользуется. OTHER остаётся manufactured hash, без заявления о вычислении реальных admission bytes либо BIND.

Новые12 lexical cases (779–787) вызывают только parseInputs на полном descriptor. Они не могут пройти благодаря отсутствию metadata для нового имени. Healthy relocation controls (789–814) требуют ready для каждого из трёх допустимых переименований; дополнительно проверяют admission inclusion, digest equality и canonical/absence facts, включая три TMP children. Родители выбранных healthy paths уже представлены в metadata: /tmp, /fixture/retained, /fixture/cache.

Workspace negatives (815–825) используют тот же механизм фактов и admission, но workspace path. Для attempt leaf присутствует fresh absence; для TMP/cache — существующая canonical directory fact. Отказ нельзя объяснить старой exclusive_storage либо отсутствием нового leaf fact. Комментарий корректно сохраняет multi-rule характер TMP-under-workspace. Отдельный owned TMP=/tmp control (827–834) имеет согласованные canonical/admission/child facts и проверяет запрет всего /tmp.

Прежние18 broad negatives сохранены с тем же отказным predicate (408–424), но rebind facts устраняет основной stale-admission mask. Они явно ограничены общей rejection проверкой там, где одновременно нарушаются несколько правил; отдельного доказательства каждого semantic predicate из каждой такой строки не заявляется. Сам relocation helper не устанавливает production ownership и не копирует будущий production path validator.

## R2 закрыт

Новый async test (835–853) создаёт ready и exact plan, затем меняет graph fake executor до runChecks. `executor.setGraph(OTHER)` меняет возвращаемые sourceGraph facts; outcome.source_stable не выставляется fixture заранее. Assertions требуют ноль child submissions, aggregate non-pass, source_stable=false, exact required obligations, отсутствие passed child states/исполненных captures и retained references без cleanup.

Следовательно, implementation с только after-child graph comparison уже не удовлетворит этому control: первый execute попадёт в calls. Исходный healthy aggregate остаётся positive pair. Прежний after-child mutation control сохранён без изменения assertions и проверяет другой момент drift. Реальный Git/source reader этим fake не исполняется и отдельно требует production review.

## Сохранность и пределы

Полный textual diff содержит только test-only relocation helper, две узкие замены R1 и appended20 registrations. Existing rejection/healthy/argv/env/report/failure/retention assertions не удалены и не ослаблены. Requested production API exports не менялись; новых imports либо FS/env/run/net/ffi обращений нет. Runtime purity будущего helper сохраняется отдельным условием import-safe implementation и focused deny-permission harness.

Count:207+12 lexical+3 healthy+3 workspace+1 /tmp+1 pre-start=**227**. Это source arithmetic, не observed engine result. Async pre-start callback await runChecks; no skip/filter/only registration не добавлено. Synthetic20/15/7 не менялись;7 по-прежнему не published final DOC06 count.

Обязательный actual integration gate из prior review сохранён и конкретизирован author v2 report: actual deno.json task bytes; ops/ci.ts Deno.args→shared parser/planner→spawn; actual CI/release triggers/inputs/step order/quoting/smoke/full routes; helper CLI→те же tested functions→trusted reader/bounded executor; final source/tool/count binding. Pure workflowRoute/genericCheckPlan exports сами по себе не закрывают этот gate. Здесь actual integration не проверялась, production helper отсутствует в данном correction scope.

Author report `/tmp/qcl-docs-test-routing-red-v2-report.md` используется как сопоставление, не oracle. Его выводы о R1/R2 подтверждены exact source/diff; native FS/admission/process-tree enforcement не подтверждены.

Учёт named source reads:255332 B, включая каждое полное underlying read для hash/diff/nl/sed/cat. Округлённый reserve bound327680 B <2MiB; Git metadata отдельно. Physical I/O/CPU/RSS не измерены. Бюджет review≤10min/1CPU/1GiB/output96KiB; target runtime/import/parser/typecheck/tests/build/network/CP/product changes=0. Созданы только requested review artifacts.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 masked path controls исправлены | Current160–181,347–358,779–834; exact delta | Manufactured metadata, broad multi-rule limits сохранены | сохранить |
| R2 проверяет drift до первого child | Current835–853, zero calls и non-pass; old after-control сохранён | Real source reader не выполнялся | сохранить |
| Existing assertions/API сохранены | Exact v1→v2 diff | Narrow correction review | сохранить |
| Fixture runtime/actual integration/native/full CI приняты | Только source evidence | Execution0, отдельные gates не закрыты | данных недостаточно |

STOP. Root может отдельно связать finite RED с exact fixture SHA/count; reviewer calls не расходовал и checkpoint не менял.
