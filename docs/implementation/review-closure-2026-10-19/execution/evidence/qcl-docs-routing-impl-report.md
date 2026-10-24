# Docs routing source I, round 1 — частичная реализация, STOP для CPP

Selected isolated worktree `/tmp/qcl-docs-test-routing-worktree`, branch
`codex/review-closure-docs-test-routing`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`.
Начальный status: только untracked frozen `tests/docs_test_routing_test.ts`.
Восемь gitlinks прочитаны; submodules в этой worktree не initialized (префикс `-`),
не изменялись. Exact final source hashes находятся в соседней identity.

Это **частичный source implementation**, не завершённая actual integration.
Ни parser/typecheck/formatter/test/runtime/build, ни CLI/target import, ни network,
ни CI/server/science не выполнялись. Использованы только чтение/редактирование,
Git diff/status, SHA256 и текстовая самопроверка. RED fixture byte-exact SHA256
`04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3` сохранён.
Original RED `/tmp/qcl-DOCS-ROUTING-RED-1` не менялся; exit1/TS2307 и зависимый
TS7006 не переопределяются как выполненные tests. GREEN остаётся у Root.

## Что написано

`ops/docs_tests.ts` self-contained, без imports, top-level cwd/env/I/O и без
process side effects при import. Девять requested exports: genericCheckPlan,
parseInputs, preflightInputs, planChecks, validatePlan, parseUnitReport,
runChecks, parseCiArgs, workflowRoute. Pure parser проверяет exact nested keys,
duplicate decoded JSON keys, finite sizes/paths/counts, source closure; считает
SHA256 исходного descriptor. Normalized metadata — только injected trusted-reader
protocol для pure logic, не публичная persisted schema и не native authority.

Planner задаёт base/Python/Node/DOC06 по D1/D2 с exact argv, clearEnv/maps,
лимитами и before/after source checks. Reader разделяет composite passed_base и
source-bound positive-count passed_unit; rejected/partial captures остаются в
receipts, unsubmitted steps имеют null capture, cleanup отсутствует. Fake
executor path не объявлен production executor и не доказывает native guards.

`deno.json`: прежняя цепочка check перенесена в check:base, добавлены ровно две
точные exceptions, generic suite permissions сохранены. check/docs:check/
docs:preflight идут в guarded CLI; inputs обязательны, fallback отсутствует.
`ops/ci.ts` использует shared parseCiArgs; input-only full, targeted scopes прежние,
full aggregate вызывает ровно один раз перед owning component branches.
Workflow dispatch inputs передаются step-local env, quoted argument; preflight
перед bootstrap/prepare; standalone full check удалён; runner-smoke base-only;
manual trigger и cancel-in-progress:false сохранены.

## Неустранённый interface/design blocker — требуется локальный D3

D1/D2 требуют actual externally admitted process-tree/storage supervisor и trusted
retained readers, но не определяют их persisted APIs. Fixture прямо предупреждает,
что `normalized-tool-identity`, `externally_measured`, `fresh`,
`process_tree_supervision` — injected doubles, не accepted persisted schema/BIND.
Поэтому CLI читает descriptor bounded≤32769B, вызывает тот же parseInputs и
возвращает bounded blocked/exit1 до любого child. Он **не** проверяет native
предпосылки и **не** выдаёт ready_for_unit_attempt, passed или fake receipts.
Always-blocked CLI не является завершённой routing integration.

Нужны точные design решения, а не только отсутствующий сервер:

1. Owning platform retained-tool/admission reader: persisted versions, required
   fields, byte-hash rules, freshness clock/expiry, producer trust root и active
   caller identity; как authentic retained bytes преобразуются в normalized
   Metadata без принятия caller labels/booleans. D1 Ref(path,sha256) связывает bytes,
   но сам по себе не утверждает trust, ownership или measured version. Рабочие
   места будущей Root integration: private reader в ops/docs_tests.ts либо отдельно
   согласованный Root module; создание owning platform contract требует своего PR.
2. Active supervisor API: какой admitted launcher/cgroup/storage backend владеет
   процессным деревом, hard quotas или явно принятой measurement policy; как helper
   подаёт exact executable/argv/cwd/clearEnv/env и limits, получает cancellation,
   terminal closure/evidence и не расширяет authority base/dedicated. Нельзя просто
   Deno.Command.kill + descriptor boolean назвать external supervision.
3. Capture/retention API: bounded concurrent stdout/stderr drains, общий byte
   budget/deadline, exclusive original stream/receipt files, failure handling при
   storage/drain refusal, provenance source before/after and descriptor hash,
   actual supervision evidence tied to attempt+step, terminal missing measurements.
4. Reviewed unit-count source binding: trusted producer reviewed_units должен
   зафиксировать final selected test SHA+tool/report contract. Synthetic7 не final
   DOC06; published56 необходимо связать exact final bytes. Source-only unit counts
   и external retained evidence имеют разные типы доказательств.
5. DOC06 seeding integration: **не реализовано** без пункта2/3, чтобы не создавать
   fixture перед admission. D3 должен привязать fixed two-tree layout из accepted
   symlink D к owned child lifecycle, bounded no-follow inventory (10dirs/2links/
   1empty regular), exact relative targets, canonical owned ancestors, fresh0700
   dirs/0600file, seed/prelaunch/terminal samples, refused collision, failure
   retention. Scoped child argv planner уже сохраняет exact2codefiles+ownTMP,
   one TMP positional arg, only DENO_DIR env; никакие child privileges не добавлены.

Таким образом native executor/seed отсутствуют, actual CLI не достигает
preflightInputs/planChecks/runChecks при native handoff. Это явный incomplete
source gate, который pure GREEN закрыть не может. Подключение всегда-блокирующего
CLI в workflows означает full pipeline остановится до heavy prepare, как и
должно быть до принятия missing native APIs; такой diff не READY к final CI.

## Source self-review и typing gap

Текстовый git diff проверен: только четыре tracked integration paths + новый
helper и frozen untracked fixture. git diff --check не выдал diagnostics;
new-file whitespace check отдельно сохранён в output commands, это не formatter.
Никакой numerical/unit/full check не приписывается этому результату.

Frozen fixture читает `failed.capture.stdout/stderr/exit_code` без capture null
narrowing после find (около638), но pre-start control требует null/undefined
для unsubmitted captures (около854). Реализация честно имеет Capture|null.
Предполагаемая TS18047 требует independent CPP и узкого reviewed fixture typing
correction перед GREEN, если подтвердится; writer fixture не менял. Это source
inference, не выполненная compiler диагностика. Возможны и другие type/format
issues: execution запрещён, formatter/parser не выполнялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure/source routing представлен reviewable diff | 9 exports, exact child plans, tracked task/workflow diff, complete patch+hashes | Runtime/typecheck/format не выполнены | дополнительно измерить |
| Frozen RED fixture и raw сохранены | Fixture SHA; RED path unchanged | RED зарегистрировал0tests из-за missing module | сохранить |
| Actual full CI/native routing реализован | CLI возвращает blocked до child | Missing trusted reader/supervisor/capture API; seed deferred | данных недостаточно |
| Нужен D3 перед native integration | Точные5design вопросов выше | Не подменять fake metadata trust доказательством | изменить |

Бюджет source read консервативно<3MiB, report+identity+patch<96KiB; тяжелых
процессов не запускалось; RSS/physical I/O/CPU не измерены как hard quota.
Source round1 завершён; STOP, no commit/push/CP writes. Root owns next CPP/GREEN.
