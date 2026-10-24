# SCI05-N1 Runner: независимый CP-CODE source review

Дата: 2026-10-19. Вердикт: **REQUEST_CHANGES / SOURCE_NOT_READY**. Найдены четыре локализованных разрыва transport/readback-контракта и один известный blocker подготовленного C08 handoff. Исполнение, импорты, parser, тесты, solver, сборки, сеть, серверы, Git mutations и дочерние агенты не использовались. C08 данным review: **0**. Это не разрешение дополнительного corrective/runtime цикла и не увеличение оставшегося общего бюджета.

## Неизменяемый объект review и порядок чтения

Reviewed worktree: `/tmp/qcl-sci05-runner-worktree`, HEAD/base `9378396a3681c1eddf2c62f16674834fc4465583`, branch `codex/review-closure-final-audit-writer`. Git status показывает ровно пять фактически изменённых paths: четыре tracked файла плюс новый test. Recursive submodules отсутствуют; `git diff --check` завершился с exit0. `light_results.jl` перечислен в identity как прочитанный dependency, но не изменён. Это согласуется с заявленными пятью changed paths.

Сначала прочитаны архитектура, applicable physics-audit/CONTRIBUTING, D2 §8.3–8.8, принятый profile A и actual diff/source/test. Затем прочитан авторский отчёт. Исторический root HEAD автора `9d8cf0c...` не подменяет actual: при review root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` был `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, clean; selected gitlinks Core7324 / Runner937 / Contracts12fc / Resultse2fd совпадают с относящимися к этому review owning sources. Root не является источником reviewed uncommitted Runner patch.

| Артефакт / путь | SHA256 |
| --- | --- |
| `/tmp/qcl-sci05-runner-identity.json` | `7d2a44cee5c8074e6b4a1db1c421ea080e32cae57f3d1b42c14d6cfc61878857` |
| `/tmp/qcl-sci05-runner-patch.diff` | `9fc71bb3ca3c9724b6d545c7b231c90dd4b053455f7d298eb63692d523e6ad70` |
| `/tmp/qcl-sci05-runner-report.md` | `0e0c89e6ba8c641399268eb633bd78310d7f70b0134bb8626f3d61d6e319fa94` |
| `src/infrastructure/persistence/physics_diagnostics.jl` | `e57d57ef46bf2b4cf36e21fee0a59d8607d8c4aced808fc9bcfa16c410345a83` |
| `src/infrastructure/persistence/hdf5.jl` | `d9ceeec9a76b8a7bc4c41eb24aaa2d4bb1fc1994cbce0407b9a344bdacb8d143` |
| `src/infrastructure/persistence/point_artifacts.jl` | `c59cc27dc5c4e3b5e640105ad362a89365285e03d3d741c8141598dfd7e9329d` |
| `src/infrastructure/persistence/light_results.jl` (unchanged) | `75c418fcc02e1023f951ccca216d60a0fd78e662f2a21fac1a477e609b141f06` |
| `test/infrastructure/final_fixed_point_audit.jl` | `2deeff785cc09ee724dbbaffd0d99693178483c90b7b5685eefe47bbcc773e8b` |
| `docs/src/user/results.md` | `e67f5b22b23d1f1f7edd03d7d9e20935cbd63e681d743739eca62f5c3f65e06f` |
| `/tmp/qcl-sci04-design-v2.md` | `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` |
| `/tmp/qcl-sci05-attribute-encoding-design.md` | `1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206` |

Profile A принят отдельно: independent review SHA `95518b6b9150b27ec490f2e30e5015511b300769fc3ed9443010591c1a010916`. Старый conditional attr cap512 не является нормой этого review. Core read source — `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`; Contracts — `12fc26462bbab3df76904c6deb01f8c6596de7be`.

## Findings — весь коллированный набор

### F1 — P2: explicit null commit key проходит как legacy/recovery отсутствие

Локатор: `src/infrastructure/persistence/physics_diagnostics.jl:630–640`, `_verify_final_audit_pair`; особенно `record=get(assessment,"final_fixed_point_audit",nothing)` и проверки `record===nothing`.

D2 §8.7 требует отсутствия самого nested key в recovery и обеих копий в legacy final. Present malformed record нельзя превратить в reader-derived отсутствие. Здесь отсутствующий key и присутствующий JSON `null` неразличимы. При отсутствующей native group helper принимает `stationary_assessment.final_fixed_point_audit = null` как recovery (`!present && record===nothing`) либо как legacy final (`!present && record===nothing && return`). Он вообще не доходит до object guard `_final_audit_record`.

Воспроизводимая различающая проверка без изменения physical fixture: взять созданный test legacy final или recovery, добавить nested key со значением `nothing`, оставить group отсутствующей и вызвать helper/public verifier; по указанным веткам ожидается acceptance, хотя D2 требует corrupt/reject. Текущий test проверяет удаление key при существующей group (172–173), но не эту present-null ветку.

Минимальный repair contract: различать `haskey` и значение; present null отвергать в final и recovery, сохранив old absent+absent final и recovery omission. Нужны healthy absence controls и present-null negatives. Это presence policy, не второй numeric/schema evaluator.

### F2 — P2: разрешённая отсутствующая analysis copy отвергается

Локаторы: `point_artifacts.jl:1188–1189` передаёт analysis owner в тот же helper; `physics_diagnostics.jl:639–640` без role-specific semantics требует native group при присутствующем commit record.

D2 §SCI05-N1 и §8.7 задают обязательную canonical copy в physics.full и **опциональную** идентичную copy в physics.analysis. Существование analysis owner не делает саму audit copy обязательной. При здоровом canonical full+commit и analysis owner без audit group эта реализация бросает `ArgumentError("final audit presence differs")`. Writer вправе всегда создавать optional copy, однако общий native verifier не должен сужать принятый формат.

Воспроизводимый контроль: взять actual writer archive с full+analysis; удалить только новую audit group из analysis, обновить его bytes/SHA в commit, сохранив native identity и остальные обязательные metadata. D2-valid архив будет отвергнут на analysis call. Текущий roundtrip всегда создаёт group в обоих owners, поэтому этой ветки нет.

Минимальный repair contract: canonical full сохраняет strict parity; отсутствие optional analysis copy допустимо; если analysis copy present, всё содержимое и identity обязаны совпадать с canonical. Recovery group по-прежнему запрещена. Нужны positive absent-analysis-copy и negative contradictory-present-copy controls.

### F3 — P1: presence нового record не гарантирует привязку к native identity при legacy top-level guard

Локаторы: `point_artifacts.jl:1174–1183` сравнивает native identity только внутри `if haskey(commit,"state_id")`; новый `_verify_final_audit_pair` (`physics_diagnostics.jl:630–667`) проверяет record против `commit["identity"]`, но не требует native identity и не отменяет legacy bypass при новом record.

D2 §8.7 требует три связи: native record ↔ commit record ↔ actual commit/native point identity. Шесть полей внутри `commit.identity` присутствуют и проверяются, однако удаление отдельного top-level `commit.state_id` отключает всю проверку metadata/point_identity_json (full) или metadata/identity_json (analysis). После этого две равные audit copies с правильной commit.identity принимаются при противоречащей либо отсутствующей native identity. Собственный обычный writer создаёт top-level state_id, но public verifier объявляет verification именно persisted artifact и не может при новом record понизить его до legacy, если required binding marker удалён.

Воспроизводимый source-derived counterexample: начать с здорового archive; изменить только full `metadata/point_identity_json.attempt`, обновить full owner bytes/SHA, оставить artifact declaration identity и оба records равными исходной `commit.identity`; удалить top-level `commit.state_id`. В `verify_point_artifacts` role/hash/internal-storage/native-marker checks сохраняются, обе legacy-условные identity проверки пропускаются, `_final_audit_record` видит прежнюю полную commit.identity, equality records проходит. Receipt validation не является частью этой функции и не закрывает её обещание; при необходимости receipt может быть пересоздан владельцем архива.

Минимальный repair contract: присутствующий новый audit требует native identity binding независимо от legacy top-level marker, либо malformed new-generation commit с удалённым required marker явно отвергается. Старые truly absent-record bundles могут сохранить прежнюю совместимость. Проверить missing native identity и stale attempt/sequence/plan при deleted top-level marker; также сохранить positive canonical/analysis identities. Исправление не требует менять scientific evaluator или native numeric arrays.

Контраргумент учтён: guard существовал до patch. Finding относится к новой D2-гарантии для **present audit**, которая сейчас наследует этот bypass, а не требует широкого переустройства всех legacy native readers.

### F4 — P2: actual attempt/sequence не ограничены переносимым Int диапазоном D2

Локатор: `physics_diagnostics.jl:500–503`, `_final_audit_identity` требует только positive Integer non-Bool. D2 §8.5 устанавливает для Int верхнюю границу `2^53−1`; `state_identity.attempt` и `state_sequence` относятся к этому inventory. Значение `9007199254740992` принимается guard и сериализуется unchanged, после чего published Contracts schema должна его отвергнуть.

Воспроизводимый дешёвый контроль: literal template из test13–55 + корректная identity, заменив только attempt на `9007199254740992`; `_final_audit_record(...;bind=true)` не имеет reject path по диапазону. Аналогично sequence при прямом helper input; публичный state_sequence keyword также принимает Int без этого format ceiling. Это внешний фактический identity input, не trusted Core nested physics data.

Минимальный repair contract: оба поля должны удовлетворять `1 <= value <= 9007199254740991` без Bool/Float coercion. Добавить границы max-valid/max+1 вместе с существующими positive/type controls. Scientific thresholds и точность физических измерений не меняются.

### F5 — P1 runtime-admission blocker: hardcoded retained path не совпадает с coordinator-owned measured TMP

Локатор: `test/infrastructure/final_fixed_point_audit.jl:202–208`, особенно строка206. Test разрешает только `/tmp/qcl-sci05-runner-portable-fixture`. В конце review coordinator независимо сообщил окончательный intended owned path `/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture`. При таком env test заведомо завершится `unexpected synthetic fixture output` до `native_roundtrip`.

Это проверено по исходнику, без запуска. Известный mismatch нельзя расходовать как диагностический C08. Старый path вне предназначенного measured TMP не должен использоваться как обход согласованного resource envelope. Минимальный repair contract — связать единственный разрешённый retained path с фактическим coordinator-owned measured TMP и сохранить fresh-path отказ, отсутствие overwrite/recursive cleanup чужих результатов и synthetic/no-science label. Обновить отчёт/identity/handoff locators согласованно. Finding не требует запуска либо нового общего budget grant.

## Что подтверждено по исходникам

1. `commit_point_artifacts:795–802` сначала создаёт actual state_id/sequence, затем один раз вызывает `_bound_final_audit`; все шесть fields берутся из фактического identity, defaults для execution/attempt/plan отсутствуют. Template не получает mutation: recursive transport copy создаёт отдельный bound object. Этот объект передаётся full writer (`812–819`), optional analysis writer (`854`) и commit assessment (`933`). При обычном producer path full/analysis metadata получает тот же actual identity.
2. Recovery `_bound_final_audit(...;final_state=false)` возвращает nothing до чтения supplied template; commit pop! удаляет Core-provided nested key. Full и analysis новые группы не создаются при nothing. Legacy final без template и без new acceptance context marker остаётся без record; new context marker без template вызывает ошибку. F1 относится к persisted readback, а не к обычному write branch.
3. `_write_final_audit!` использует pinned HDF5.jl scalar String dispatch для fixed UTF8 scalar JSON и четырёх constant attributes. Dataset/attrs создаются **до** generic annotation, которая `haskey`-ветками сохраняет заданные units/description/axes (`point_artifacts:177–197`); это прямо разрешённый profile A recipe, хотя формулировка задачи упоминала «после». Global annotation semantics не изменены. Source pinned type/space dispatch ранее проверен отдельно profile A review; actual runtime dtype пока не установлен.
4. Readback проверяет bounded fixed scalar string, UTF8, layout contiguous/compact, отсутствие filters/external storage, четыре exact constants и native inventory. `_require_internal_hdf5_storage` остаётся дополнительным existing gate против links/external/virtual. JSON serializer unchanged; конечные числа сохраняют Float64 round-trip, finite signed zero в record канонизируется. Recursive equality сравнивает keys без порядка, arrays по порядку, bool/integer types точно и floats после Float64 точно; numeric tolerance не введён.
5. `_physical_certification_data:291–323` дополняет stationary required list тремя candidate gates и использует прежний Core `_solution_validation_limits`, где candidate rD/rA получают прежний rK threshold, candidate lambda — прежний rλ. Старые required gates и comparison не удалены. Missing -> not_evaluated; error/nonfinite -> failed; unavailable finite0 не проходит. Это summary выбранных gates, не новая authority full acceptance. Scientific_accepted в Core assessment остаётся false без campaign evidence.
6. Новый тест — independent literal format object, без Core record builder для expected raw values. Проверяются six-field binding, некоторые malformed status/type/budget cases, tagged nonfinite, measured0, -0 normalization, candidate missing/error controls; actual tiny native writer/readback/full+analysis/recovery/legacy path подготовлен. Подключение через infrastructure group автоматически выбирает новый .jl. Fixture выполняет existing seed/embedding preparation при будущем разрешённом test, но не SCBA/Poisson solve. Literal record не является oracle физических Green arrays; это честно отражено автором.

## Пределы и решение

Runner trusted producer guard намеренно не копирует полный nested Contracts schema или hostile JSON parser. Это не finding само по себе: owning Core template и published independent Contracts остаются источниками policy, Results выполняет bounded hostile-input parsing. Здесь не требуется импортировать Python из Runner или дублировать физические формулы. F1–F4 относятся к узким presence/role/actual-identity границам нового Runner transport, а не к произвольному требованию полного второго schema engine.

`_require_final_audit_constant` проверяет file type/scalar/cset/width перед собственным high-level read just-written values; он не реализует весь identical-memory-type raw hostile padding reader profile A, который принадлежит Results. Поэтому данное source review не подтверждает hostile-input native/library memory bound либо actual producer→Results roundtrip. Dataset/native ID lifecycle, HDF native behavior и Julia parsing не проверялись исполнением. Текущие positive tests не закрывают F1–F5.

C08 остались два на всех по coordinator admission; review не расходует их. До коллированного owning repair и нового immutable binding не следует запускать известный path-guard failure. Никакого automatic rerun/repair loop этот отчёт не разрешает. Core CPP2/E1 и его закрытый corrective cap не переоткрываются. Full S1 all-five/e–e/finite_chain4/current-bound gaps, integration/native release gates, final CI и scientific acceptance остаются вне этого review; tiny manufactured archive не доказывает full S1 или independent device physics.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Обычный writer связывает один object и шесть actual fields | commit_point_artifacts:795–819/854/933; _bound_final_audit | Нет runtime; Int ceiling F4 отсутствует | изменить |
| Final/recovery presence policy полностью соответствует D2 | _verify_final_audit_pair:630–640 | F1 present-null; F2 optional analysis | изменить |
| Native point identity всегда связана при новом record | point_artifacts:1174–1189 + new helper | F3 legacy top-level marker bypass | изменить |
| Profile A producer recipe и неизменность старых numeric gates сохранены | String writer, annotation haskey, Core limits + stationary list | Source only; no actual HDF roundtrip | сохранить |
| Prepared C08 может дать различающее свидетельство | actual tiny writer tests + env guard | F5 known retained-path mismatch | изменить |
| Новая физическая/экспериментальная приёмка установлена | Новых измерений нет | C08=0 у reviewer; fixture synthetic | данных недостаточно |

**STOP.** Sole output — этот отчёт. Product, tests, archives и Git state не изменены; source candidate не объявлен eligible для исполнения до закрытия findings.
