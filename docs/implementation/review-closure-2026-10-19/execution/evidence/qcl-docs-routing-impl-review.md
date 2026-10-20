# DOC04/DOC06 routing I round 1 — независимый source review

Вердикт: **CHANGES REQUIRED для pure failure path; native integration остаётся blocked**.
Проверка только по исходникам, без Deno/parser/typecheck/formatter/tests/imports,
native processes, сборок, сети и CI. Product и checkpoint writes=0.

## Immutable input

Worktree `/tmp/qcl-docs-test-routing-worktree`, branch
`codex/review-closure-docs-test-routing`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`.
Status: modified deno.json, ops/ci.ts и два workflows; untracked helper и frozen
fixture. Восемь gitlinks присутствуют, submodules не initialized (`-`), не менялись.
Прочитаны architecture, D1/D2/R, все шесть candidate product paths, затем author report.
Primary fixture SHA256 `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3`.
Helper SHA256 `bdc1684faffa4e6606b1667675f335768e3eb6216ae64b5842d2431460063356`.
Complete patch SHA256 `26882ff074c0f8c8ded44f34b0caa288c62da30ef6afc5dad42d420d0c6a057e`.
Все шесть actual file SHA совпали с предоставленной identity.

## R1 — P1: отказ final sourceGraph теряет доступные aggregate receipts

Локатор: этот HEAD + candidate helper SHA выше, `ops/docs_tests.ts:348`
(`runChecks`), также initial await на строке325; controls
`tests/docs_test_routing_test.ts:835` проверяют только возвращённый mismatch.

Воспроизводимый source scenario без исполнения: injected Executor возвращает
правильный Graph на первом вызове и после каждого из четырёх healthy children
(вызовы1–5), затем отклоняет Promise на final sourceGraph (вызов6). К строке348
все четыре captures уже записаны в локальный receipts. Последний await находится
вне try/catch, поэтому Promise runChecks отклоняется, return349–352 не достигается,
caller не получает ни terminal aggregate, ни доступные captures/retention locator.
Та же форма initial graph failure325 не даёт typed blocked/failed aggregate.
Это не pass-on-error, но нарушает D1§6 сохранение failed receipts/partial evidence.
Source inspection достаточно для этого вывода; фактическая ошибка Git не измерена.

Исправление: представить отказ source-guard как terminal failed/unknown source
evidence с reason, сохранить уже полученные receipts и запретить следующие children.
Не подменять отсутствующий Graph исходным или false measurement. Добавить узкие
fake-executor controls initial/final rejection и особенно final rejection после
четырёх captures. Обязательство относится к pure API независимо от будущего D3.

## R2 — оставшийся receipt contract, gate D3

`StepReceipt` (`ops/docs_tests.ts:58`) сохраняет name/result/summary/capture;
создание324 и return349–352 не сохраняют exact plan, descriptor digest, source
revision/digest, argv/cwd/clearEnv/env binding и stdout/stderr hashes/byte counts.
`Capture.supervision` проверяется334–340 по двум booleans и форме hash; самого
attempt+step binding supervisor evidence здесь нет. Поэтому этот object пока
не является полным D1§6/D2§4 private receipt. Caller, сохраняющий только return,
не сможет восстановить provenance exact environment из результата.

Это согласуется с признанным author missing capture/retention/supervisor API,
а не опровергает blocked CLI. В D3 явно связать полный receipt с immutable plan,
source/input identity и trusted attempt+step supervision; не трактовать текущий
synthetic passed как native evidence. Pure GREEN не закрывает этот gate.

## Что source review подтверждает

- Девять exports присутствуют; imports отсутствуют. Top-level не читает env/cwd,
  filesystem и не запускает процессы. CLI guarded import.meta.main.
- Strict descriptor проверяет exact nested keys, decoded duplicate members,
  32KiB, paths/hashes/counts и пустой loader_env. Positive manufactured handoff
  отделён от mutations независимых metadata facts и от expected report counts.
  Это содержательные pure controls; их выполнение и custom SHA не проверены.
- plan/validate дают exact base/Python/Node/DOC06; лишние permissions/args/env
  отвергаются сравнением полного reviewed plan. passed_base не заменяет unit
  summary; docs-only не получает full scope; missing steps/zero/skips/unknown
  outputs и failed guards по доступным веткам не дают aggregate pass.
- deno.json base chain совпадает с genericCheckPlan, исключения ровно два,
  generic suite permissions сохранены. ops/ci.ts использует shared parseCiArgs;
  full aggregate вызывается один раз перед component branches. Actual workflows
  согласованы с workflowRoute по чтению: quoted step-local input, preflight до
  prepare, один full test call; runner-smoke base-only; cancel-in-progress:false.
  workflowRoute tests проверяют модель маршрута, YAML ими не читается; поэтому
  эта согласованность установлена ручным source review, не выполненным тестом.
- Native CLI читает bounded descriptor, вызывает общий parseInputs, затем всегда
  blocked/exit1 (378–402); ни preflightInputs, ни planner, ни runChecks не достигаются.
  Это честная fail-closed частичная реализация, но actual aggregate integration
  не готова. DOC06 seed отсутствует; пять author D3 вопросов остаются gates.
- TAP/unittest happy samples manufactured. Совместимость exact выбранных tool
  reports/CLI, formatter и typecheck не установлена; unit GREEN, даже если будет,
  не докажет native report/capture/runtime readiness.

## Proposed fixture typing patch

SHA256 `7d65aba44b29dcccdcbd079fc0f804c5afee29646cdc195e39b9e55ae42f9a5b`,
unapplied. Два explicit capture non-null assertions перед frozen631–633/760
логически корректны: submitted failed capture и completed base обязаны иметь
capture. Assertions с asserts value сужают Capture|null; прежние equal проверки
сохраняются; casts/any, skips, ослабление expected values не добавлены.
**Source-approved** как узкая typing correction с сохранением historic RED
отдельно. Это не compiler-confirmed исправление и не обещание отсутствия других
type/format failures. Frozen fixture не изменена reviewer.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure failure retention полна | Final/initial graph await вне catch, R1 | Source scenario, без исполнения | изменить |
| Narrow fixture typing patch сохраняет assertions | Две добавленные guards, exact patch SHA | Typecheck не запускался | изменить |
| Actual routes согласованы с pure contracts | Ручное чтение шести bound paths | workflow tests сами YAML не проверяют | сохранить |
| Pure GREEN означает native/full integration | Always-blocked CLI; missing readers/supervisor/seed | Runtime и CI=0 | данных недостаточно |
| Full provenance receipts готовы | R2 + author capture API blocker | D3 ещё не принят | изменить |

Reads консервативно <1MiB; wall <15min; CPU/RSS/physical I/O отдельно не измерены.
Никаких scientific/numerical проверок. STOP; product/CP/git writes, commit/push=0.
