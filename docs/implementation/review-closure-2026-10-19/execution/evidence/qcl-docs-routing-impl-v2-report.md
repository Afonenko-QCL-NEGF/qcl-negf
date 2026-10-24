# Routing I2 — частичный source result, НЕ готовая native integration

Selected worktree `/tmp/qcl-docs-test-routing-worktree`, branch
`codex/review-closure-docs-test-routing`, unchanged HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`; submodules uninitialized, gitlinks
не менялись. Native source overlay не committed и не READY. I1 report/identity/
complete patch и original RED receipts/raw не менялись. Разрешённый scope —
только source, finite round2; runtime/parser/formatter/compiler/tests/network/
server/CI/science=0. Числа ниже — декларации исходников, не измеренный report.

## Дельта и TDD граница

До production edits сохранён `/tmp/qcl-docs-routing-historical-RED-fixture.ts`
с SHA256 `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3`.
Current fixture получил две уже source-approved explicit nonnull guards, затем
три новых registrations: initial sourceGraph throw, throw после первого child,
terminal throw после четырёх captures. Прежние227 names/assertions сохранены,
current nominal230. Эти regression source написаны до helper fix; новый
behavioral RED не исполнялся и не заявляется. Старый RED TS2307/0registered и
CPP source failure scenario — отдельные исторические свидетельства.

Написаны сначала два новых manufactured test sources, затем production modules:
`tests/test_docs_test_native.py`:8 test methods; `tests/docs_test_native_protocol_test.ts`:
8 registrations (4literal+1literal graph healthy+3loop refusals). Они требуют
независимого CPP и отдельного finite DEV plan, не расходуют sole pure GREEN.
Они пока покрывают только перечисленные seams, **не весь D4 test matrix**.

## Исправлено в pure/owning source

`runChecks` ловит initial/per-child/final source observation rejection и
возвращает terminal aggregate с `source_observation.status=not_measured`, reason,
сохранёнными captures и null для unsubmitted steps. Unknown observation не
выдаётся за измеренную mutation; source_stable=false запрещает pass.
Step receipts теперь содержат exact cloned plan (argv/cwd/clearEnv/env/limits),
input/source revision+digest, retained runtime identity, attempt directory
identity, SHA256/UTF8 byte lengths captured strings. Native raw byte hashes
по-прежнему отдельное обязательство (invalid UTF8 cannot be represented by string).
Supervision frame сохраняется полностью в capture, synthetic booleans не
объявляются native authority.

`ops/git.ts` получил backwards-compatible injected GitReader, default git
для прежних callers сохранён; все sourceGraph internals используют readGit.
Owning graph semantics/argv/order/flat checks не forked. Новый driver подаёт
brokerReadGit и не выбирает default process.run/Command.output.

`ops/docs_tests_cli.ts` — permissionless bounded NDJSON driver, nine pure exports
helper остаются import-safe без CLI. Driver использует shared parse/preflight/
plan/validate/run, owning sourceGraph через injected reader; malformed/incomplete/
wrong sequence requests отказываются; native route не имеет script process grants.
Typed protocol tests используют actual reader APIs и owning graph, no product exec.

Tasks переведены на D4 quoted `$QCL_DOCS_PYTHON -I -S -B ... client MODE` с
`--inputs FILE`; без ambient Python fallback, unlimited Deno run или новых
child unit permissions. Existing workflow order/input quoting/full-vs-smoke из
I1 сохранён. Actual external wrapper не установлен.

## Native adapters, написанные в source

`ops/docs_tests_native.py` содержит closed bounded frame reader/writer с exact
keys/decoded duplicates/UTF8 checks; one-use PhaseLedger; bound regular nofollow
read; full version parsers; parent-registered retained observation reader;
closed Git argv validation; 13-node fixed seed+no-follow inventory; sampled
storage global/domain debit; explicit existing delegated cgroup guard; перенесённый
private uid/birth/pidfd owner по selected platform source; fresh fork subreaper
bounded stdout/stderr capture, dispatch gate и child cleanup attempt; constructor
start_docs_setup требует nonserializable trusted parent object и external gated
bootstrap API; client читает ровно четыре routing env fields и broker transport.
Это **source adapters**, без утверждения их работоспособности/безопасности.

## Существенная незавершённость — источник, НЕ сервер

В finite20min/source round2 весь принятый D3/D4 не реализован. `setup_main`
**явно отказывает** `source-incomplete-active-factory-and-broker`, а не принимает
непроверенный startup. Поэтому valid trusted handoff ещё не достигает actual
executor. Это нарушает обязательную complete-integration acceptance D4; такой
результат НЕ считается завершённым I2, НЕ READY и не закрывается pure GREEN.
Сохраняется только reviewable частичный code output; нужен отдельный authorised
source continuation после CPP, не автоматический runtime loop.

Точные оставшиеся source gaps:

1. ActiveDocsAttempt/bind_native_context и полноценный producer setup_main/
   broker отсутствуют. Нет ACK nonce+source/input/runtime binding и lifecycle
   parent EOF/cancel; нет authenticated SO_PEERCRED+proc ancestry+task leader
   pinning, consumed phase dispatch gate, terminal completion ACK. Parent hook
   `authorize_docs_setup()/spawn_gated()/runtime_closure_verified()` сейчас
   assumptions external trusted harness, а не окончательно implemented factory.
2. Нет executable driver launch/interactive native protocol owner, prepare/
   execute/finish state machine, independent exact plan validation native side,
   metadata projection из уже trusted readers. Нет runtime handoff to driver,
   no unit dispatch exposed by setup_main. Client challenge exchange — proposed
   source-only extension, пока не поддержан broker; D4 CPP должен отвергнуть
   этот protocol delta или согласовать exact compatibility.
3. Нет native16 commit-derived blob/working-byte binding reader, native closure
   attachment builder, повторных per-step/final full bindings, actual Git budget
   ledger≤512/8MiB/60s с per-snapshot≤128/2MiB/20s. Closed argv validator пока
   предполагает submodule section=name; owning sourceGraph допускает другие
   section names. Native route source schedule не посчитан, local Git config
   no-exec closure не проверен. Native startup поэтому не может ACK.
4. Retained tool reader частичный: нет producer measurement/parent registration
   construction, KaTeX/count readers, exact nested runtime ref checks и agreed
   UTC representation normalization, accepted capture/runtime digest registration
   import. Самосогласованный record или source16 не создаёт доверия.
5. Bounded capture adapter НЕ удовлетворяет final lifecycle contract: parent
   timeout/cancel finally может kill supervisor до доказанного descendant closure;
   source of combined failure raw partial capture может потеряться при transport
   refusal; status receipt_ref пока не создаётся exclusive/durable с actual SHA;
   global log debit применяется после capture и не ограничивает concurrent raw
   storage before-write; no robust EOF parent cancellation during blocking status
   read; supervisor result wall timestamps numeric и пока не преобразованы в
   pure ISO timestamps. Не использовать execute_bounded в production до CPP/fix.
6. Storage sampling может считать cross-domain overlap повторно, roots заранее
   не проверены disjoint; max sample storage в памяти bounded count, но transport/
   receipt metadata/global byte reserve incomplete. Seed exact links/13inventory
   проверяет path containment, но mode verification и canonical target comparison
   с literal backing path требуют усиления. Full seed+terminal guard integration
   отсутствует. Physical metrics честно unknown, sampled не hard disk quota.
7. Cgroup resource backend проверяет controls, но не доказывает independent parent
   authority/delegation/initial private-empty boundary/owning host admission expiry;
   terminal-empty API не подключён. Контрольный128MiB reserve и durable pre-child
   intent/owner setup placement не implemented. Не выдавать его observation за
   admitted backend без этих условий.
8. Driver protocol finish сейчас ограничен131072B, aggregate с full captures может
   превысить cap; нельзя объявить transport complete. Captures bounded per-frame,
   но общий frame/output debit+timeouts не implemented. Generated Python supervisor
   captures имеют extra supervision fields: exact private native evidence schema
   пока не bound к attempt+step/actual retained receipt bytes.
9. New DEV fixtures не покрывают D4 full required paired negatives: no gate-order
   fakeproc/cgroup suite, durable retention/storage-full/short-drain/parentEOF,
   source snapshot/global-budget/terminal failure native owner cases, forged
   producer registration+expiry/closure pairs. Native Python fixtures imports
   source via importlib only within test; product module has stdlib imports only.

## Проверки и frozen inventory

Только текстовый self-review и git diff --check: tracked whitespace diagnostics
нет. Ни formatter, ни Python AST/py_compile, ни Deno check/test не выполнялись;
возможные syntax/type/format defects остаются CPP/compiler gate. New-file textual
whitespace check отдельно отражён командным выводом, не formatter claim.
Полные file hashes, fixed16 source closure source-only refs, nominal test matrix и
complete patch находятся в v2 identity; источник не committed, blob IDs от final
HEAD недоступны и не выдуманы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure sourceGraph throw больше не теряет accumulated captures | Catch-bound observation helper +3prior-written source regressions | Не исполнялось | дополнительно измерить |
| Historical227 сохранены | Exact immutable04589 snapshot +two guards+three appended names | Current230 требует CPP/compiler | сохранить |
| Native integration завершена | setup_main refuses source-incomplete;9explicit gaps | Не source READY, не runtime/server limitation | изменить |
| Новые protocol tests подтверждают native guards | Source-only8Python/8Deno; actual dispatch0 | Большая часть D4 matrix ещё не написана | данных недостаточно |

STOP для Root independent CPP. No automatic retry/extra RED/GREEN/compiler/runtime.
I1 artifacts и historical RED остаются неизменны. Report+identity+complete patch
bounded≤160KiB; source reads conservative<6MiB. CPU/RAM/physical I/O не измерялись.
