# SCI05 — независимый review одного known-red all-block diagnostic

2026-10-19. **PASS source/plan eligibility для одного coordinator C08 call3 на diagnostic v2 SHA `949d2b5d621ac3b23196e61116334731ca3871163411b1ac2a21f277b8de60a0`**, при fresh intent/source/runtime BIND. V2 явно связывает `JULIA_TEST_FAILFAST=false`. Внешний stdlib `Test.@testset` переносит момент итогового RED к концу внешнего набора и позволяет продолжить последующие sibling testsets после обычных внутренних Test errors. Продуктовые assertions, fixtures, expected values и допуски не меняются. Это диагностический сбор оставшихся gaps на известном RED, не scientific acceptance и не попытка объявить текущий test зелёным.

Review≤15 min /1 CPU/1 GiB/read≤2 MiB/output≤32 KiB. Сначала целиком прочитаны original.log и receipt call2; затем actual product source, harness diff и локальный Julia stdlib Test source. Единственный новый файл — этот отчёт. Julia/parser/import/tests/solver/build/install/network/native calls=0; дополнительных C08 calls=0; Git/product/harness mutations=0. Дополнительных агентов нет. Применена source-only граница ранее прочитанного `qcl-physics-audit`.

## Неизменяемые источники

Actual Core `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGF.jl`: HEAD `e86ac74c4fe04a8999b889970c5a9f3c65575694`, status пуст, recursive submodule status пуст, `git diff --check` успешен. Test SHA `d4ac564013d46021a84b323338635f6860f16d1aa76e4b417c4aaf64debf64c4`; после call2 продукт не изменён.

Пять production source SHA остались CPP2: QCLNEGF.jl `cec01e69f58466511102138f01d7f2ab26624b22c3d0af77e825a0b8c51481f2`; validation.jl `50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c`; final_audit.jl `ac20ca9ded521220224d4e3c0688b0149db0c1b3b9fb264c25b1cabd4367be73`; poisson.jl `730777452e3f17c6b55490fb05f190a9d97806d533a13b45666a91e1427e39c5`; production_solver.jl `5d0fa48c016877897f97ccc919e3100fd4ba9fdedcd907166447d2bbc89ad0c2`.

Root actual HEAD `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`; concurrent status содержит modified Core/Runner gitlinks, execution checkpoint/census, deployment document и untracked execution evidence/bindings. Actual recursive submodules: Core `+e86ac74...`; Runner `+9378396a3681c1eddf2c62f16674834fc4465583`; AiiDA `d8f8092ca1c76523d85384b4bac8198d8bfa736b`; Contracts `02a564b78dc9c5e19eacf496bc8c891361eafaab`; Platform `b067723c82382689bff5cc366981c56e99b926f8`; Portal `2622de5ee28b454ff4f809cc3dd00c1e5bc2295d`; Research `1eacefcd81a50e245ea9da74a0b717b33818c61e`; Results `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Это наблюдение, не новый source lock. Fresh BIND обязан учитывать actual source/runtime, а не только прежний root/Runner ref.

| Проверенный артефакт | SHA256 |
| --- | --- |
| `/tmp/qcl-SCI05-C08-CORE-2/original.log` | `55996891e3287948b43d922f6ee683000df531e9c367d29af0cae98295d17693` |
| `/tmp/qcl-SCI05-C08-CORE-2/receipt.json` | `9d5b4129c634bd6e4f1407516401ba7e4259f92eee8ad3f83788b8b8566ea7cd` |
| Accepted `/tmp/qcl-julia-c08-run-v3.py` | `d454f20503108bfa7b40df921b7e4acf4fd4d049bbaf1801c4a3a05de36ad112` |
| Proposed `/tmp/qcl-julia-c08-diagnostic-v1.py` | `2072728bb8bfe0055705ef6a0db7ce6c8a7c1a9c7bbb9427e3df594101e6a2c4` |
| Reviewed final `/tmp/qcl-julia-c08-diagnostic-v2.py` | `949d2b5d621ac3b23196e61116334731ca3871163411b1ac2a21f277b8de60a0` |
| Local Julia1.13 stdlib `Test/src/Test.jl` | `36bf481a76fd9aa3166cc69af165a10052893935da63e7456174f8e06f7a1d7e` |

Локальный Test source: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGFRunner.jl/.build/julia/share/julia/stdlib/v1.13/Test/src/Test.jl`. Он прочитан как первичный исходник поведения; module не импортировался и parser не вызывался.

## Что call2 действительно измерил

Raw полностью содержит два successful testsets:26 и24 passes. Третий набор `Frozen complex matrix, weighted number and unnormalized candidate` имеет21 passes и1 Error. Совокупно видны71 Pass/1 Error до прерывания include; это не общий pass всего файла.

Receipt: exact test SHA d4ac..., harness d454..., exit1, wall39.041s, sampled peak RSS1246842880 B, owned TEMP0 B, raw2259 B; raw_capture_complete=true; guard_error/raw_capture_error/stop_reason=null, output_envelope_overrun=false. Следовательно, наблюдённый исход — Test error, а не hard-guard failure. Sampling limits не становятся hard quotas из факта их отсутствия в этом запуске.

**Наблюдённый контрактный gap с воспроизводимым локатором:** `test/numerics/final_audit_evidence.jl:154–162` строит malformed lesser field через ordinary transpose `permutedims(r)` вместо adjoint. Затем строка162 требует finite числовую разность от публичного `number_functional(wrong_transpose, grids, 2)`. Функция `src/numerics/reference/greens.jl:99–108` сначала вычисляет полный complex weighted sheet functional и проверяет realness, и только после этого возвращает real(value). Structural limit задан `src/domain/numerical_invariants.jl:5` как1e−10, с нормировкой `max(abs(real(value)),1)`.

Actual value из DomainError: `0.2582304378268251 - 0.8300177489439131im`. Здесь разрешённый imaginary defect≤1e−10, observed magnitude≈0.83001775. Публичная функция закономерно отклоняет этот вход своим realness contract до return. Это не свидетельство неправильного штатного number evaluator и не physical negative population. Test assertion162 ожидал числовой результат у входа, нарушающего public precondition, и записал Error. Отдельный literal `wrong_number` на155–160 берёт real projection и поэтому не заменяет realness precondition публичного API. Это конкретный gap negative-control contract, без предложений изменять код, нормировку или tolerance в этом review.

First call2 include завершился после third top-level testset: тот был outermost и выбросил `TestSetException` при finish. Отсутствие логов последующих четырёх наборов не является их pass/error measurement.

## Почему proposed wrapper собирает оставшиеся результаты и остаётся RED

Diff diagnostic v1 к accepted harness v3 содержит **одну строку argv `-e`**:

```julia
using Test; @testset "C08 all-block diagnostic (known red)" begin; foreach(include, ARGS); end
```

V2 к v1 добавляет ровно `JULIA_TEST_FAILFAST='false'` в существующий `env.update`, без других отличий; v1 сохранён. Файл/fixture path и его bytes не изменяются. В argv нет нового solver, import package setup, catch с подавлением Test errors, `@test_broken`, skip, изменения expected result или переноса fail в pass. `using Test` — stdlib existing prepared environment, не установка dependency. Harness exit condition остаётся прежним: process exit0 и complete capture/no guard errors; known Test error должен дать nonzero Julia exit и итоговый harness RED.

Независимая цепочка из local Test source:

1. `@test` ловит обычную exception и делает `Threw`; `do_test:761–789` превращает её в `Error(:test_error,...)` и вызывает `record` текущего testset. Это именно observed DomainError162.
2. `record(DefaultTestSet, Fail/Error):1283–1299` печатает/сохраняет результат; без failfast не выбрасывает исключение. Потому следующие assertions того же блока продолжаются. Observed21 passes в call2 согласуются с этим.
3. `@testset` использует scoped current testset/depth (`@with_testset:2127–2136`, `get_testset/get_testset_depth:2144–2155`), а не namespace/module-local переменную. Вызов include и объявленный внутри файла module выполняются в том же динамическом task scope; module boundary не делает каждый child заново outermost.
4. `finish(DefaultTestSet):1426–1453` при ненулевой parent depth вызывает `record(parent, child)` и возвращает child без `TestSetException`. С outer wrapper все семь file-level testsets становятся вложенными и ordinary failure третьего блока не прерывает include перед четвёртым.
5. При завершении wrapper parent depth0; recursive counts сохраняют все Fail/Error, печатают summary, и `finish` выбрасывает `TestSetException`, если есть любой Fail/Error. Код не превращает known failure в GREEN. Parent summary печатает вложенные counts при error; ошибки печатаются непосредственно при record.

**Binding нюанс закрыт v2:** DefaultTestSet constructor1241–1253 наследует failfast от родителя, а outermost читает `JULIA_TEST_FAILFAST` через `global_fail_fast:41–43`. Diagnostic v1 копировал environment без override; чтение selected `printenv JULIA_TEST_FAILFAST` при review не вернуло значения. До исполнения координатор выпустил v2 с единственным дополнительным override `JULIA_TEST_FAILFAST='false'`; exact hash/diff независимо проверены. `Base.get_bool_env` в stdlib source получает false для outermost набора; вложенные DefaultTestSet наследуют false. Поэтому all-block plan больше не зависит от этого unbound inherited environment flag. Это tooling binding, продукт не правился.

Это continuation после обычных внутренних failures/errors, **не** абсолютная гарантия выполнения всех строк: unexpected exception вне inner testset, ParseError, InterruptException, resource stop/unknown process outcome могут оборвать include. Ошибка вне отдельного `@test` внутри testset завершает остаток этого блока, но его outer sibling blocks всё ещё могут продолжиться. Нельзя объявить все blocks исследованными без их фактических counts/raw evidence.

## Различающее свидетельство одного вызова

Тот же immutable файл содержит семь testset entrypoints:19,50,119,294,385,489,606. У call2 нет evidence для последних четырёх:

- `One owning Poisson solve with independent literal residual/gauge enclosure` (294);
- `Approved D2 finite ratio0 with overflowed normalization` (385);
- `Bounded Core template, explicit unavailable and signed/nonfinite charge` (489);
- `Public validation retains failed outcome, raw rU and compatible assessment transport` (606).

Один diagnostic call3 ожидает сохранить known Error162 и впервые получить counts/errors для этих блоков, либо точный более ранний runtime/guard blocker. Их existing tiny manufactured Poisson measurements входят в уже принятый fixture; wrapper не добавляет новых physical maps, SCBA/Poisson loops, новых inputs или study run. Повторное прохождение известных первых блоков — необходимый prefix неизменяемого файла ради этой новой coverage, не loop до pass.

Outcome фиксируется как diagnostic known-red с полным original raw/receipt, фактическими reached blocks и отдельным gap inventory. Нельзя использовать aggregate exit1 как доказательство отказа каждого gate; нельзя использовать passes доступных блоков как полную научную приёмку. Неожиданный GREEN также требует reconciliation с known-red исходником, а не автоматического объявления исправления.

## Envelope и остановка

Никаких resource predicates сверх accepted harness v3 не изменено; итоговый diff — только outer-testset argv и failfast=false override: wall trigger570s, per-process CPU570/575, Julia child affinity1/threads1/BLAS1, sampled tree RSS4GiB, sampled owned logical TMP16MiB, raw stop8MiB−128KiB/post-drain8MiB; прежние raw-preservation/drain/unknown-outcome caveats действуют. Nominal cleanup reserve не становится hard realtime600s; sampled values не дают hard quota/transient proof. Prepared runtime/depot и actual source должны быть fresh-bound координатором; missing dependency означает stop без install.

SCI05/08 C08 counter по поручению и двум original receipts=2/8 consumed, remaining6 перед proposed diagnostic. Этот review не расходует invocation. PASS ограничен **одним** discriminating call3 после intent BIND. Corrective code counter=2/2 consumed; этот wrapper не даёт ещё одного product correction round. После диагностики semantic failures остаются concrete blockers. Любое новое изменение кода требует отдельного explicit finite engineering replan по актуальному grant; автоматического третьего SCI corrective loop нет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Known call2 failure локализован | Raw DomainError162 и public realness check greens106–107 | Malformed transpose fixture, не production physics failure | сохранить |
| Outer stdlib testset даёт нужную continuation без превращения RED в GREEN | Local Test record/finish/scoped-depth source; v2 argv + explicit failfast=false | Внеблочные/interrupt/guard errors могут остановить include | сохранить |
| One-call diagnostic даёт новое различающее evidence | Четыре поздних immutable blocks294/385/489/606 ещё не измерены | Runtime counts пока отсутствуют | дополнительно измерить |
| Product/oracle/thresholds unchanged | Test SHAd4ac..., clean Coree86ac74..., five source SHA equal CPP2 | Tooling argv меняет aggregation scope, что явно отражается в intent | сохранить |
| Дополнительная product correction разрешена автоматически | Counter2/2 consumed; explicit stop scope | Требуется отдельный finite replan после gap inventory | данных недостаточно |
| Full runtime/scientific acceptance получена | Known Error сохраняется; этот review ничего не исполнял | Новый test result и scientific run отсутствуют | данных недостаточно |

STOP после отчёта. No execution или product/harness edits проверяющим.
