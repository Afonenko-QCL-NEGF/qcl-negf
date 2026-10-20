# SCI08-R2 I1 — частичная реализация refusal-only

Исполнитель работал только в owning Runner worktree
`/tmp/qcl-sci08-r2-runner-worktree`, исходный HEAD
`4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`. Начальный `git status --short`
и `git submodule status --recursive` пусты. Ветка
`codex/review-closure-sci08-r2-resident-lifecycle`. HEAD/index не изменены;
commit/push/deploy, Core/Contracts/superproject, модель и solver не затрагивались.

Основания: v1 SHA256 `69313bd117c140cf28b68d62ebb85b09bbc078a0ad305b3199c65ee55636e08c`;
D2 `664fce6abccd4517a2bb8e2bd87caefff77cfbc5ee6d5991afed66d731fceeae`;
accepted high `bc5f2544d193cc1c13815acc29c15928bca1a64e98bbc4c8541d4ec65c58742f`.
Три документа прочитаны ограниченными релевантными excerpts, не полностью.
Прочитана архитектура root/Runner; иных AGENTS в Runner обнаружено не было.

## Реализованный результат

1. Проверяемая логическая арифметика E+U+P+S≤A и U+P+S≤H. Unknown, отрицательное,
boolean и переполнение дают false. Predicate никогда не выдаёт permit.
2. Типизированный exception и абстрактный authority port с отказом всех default
методов, включая release. Нет выдуманного свободного места/forecast-bound.
3. Strict guard до первого mutator у point/operator/stage/history, history
constructor, atomic text/path-first/do, atomic replace и atomic checkpoint.
4. Staged entry теперь preflight до mkdir/workspace и передача policy/envelope
во все direct/scientific/stage пути. Scientific forwarding к point/operator/
history/import исключает явные fallback в добавленных вызовах.
5. Standalone statements публикации, rename/fsync/verifier/receipt/pointers/
cleanup не переставлялись. Опциональные keywords сохраняют прежние вызовы.

**Это не выполнение полного SCI08-R2 и не writer-ready.** Существующий строгий
scientific preflight по-прежнему безусловно отказывает; новый low-level strict
preflight тоже всегда отказывает. Поэтому strict не достигает partial writers,
неконтролируемого cleanup или finalizers. Реализован разрешённый bounded fallback.

## Незакрытый точный разрыв

Нет ResidentIdentity/StorageDomain/StorageSnapshot/StorageOperationInventory
proof objects, scoped parent/child permits, finite native bounds, typed
pre/post-rename outcome, conservative settlement, registration-before-create,
needs-reconcile history, первичной/вторичной ошибки или guarded deletion.
Транзитивные save_checkpoint/implicit mktemp cleanup, optical/import-delete и
другие helper callers НЕ стали strict writer-ready от добавления внешнего guard.
Подробный named-edge inventory — в call-cleanup-table. Его полнота как всего
call graph не доказана; непокрытые ветки strict-refused на входе и NOT READY.
Нельзя включать strict writers снятием одного общего preflight.

C1/P1 backend отсутствует и не имитировался. No future unlink admission credit,
H+=filesize или уменьшение cumulative materialization не введены. Ни один
protected/failed/final объект в этой работе не удалён.

## Конечная nominal control matrix — fixture definitions, NOT EXECUTED

| Контроль | Созданное свидетельство | Ограничение |
| --- | --- | --- |
| E100/duplicate40/E60, границы A/H, one-byte-short, overflow/unknown/bool | Handwritten arithmetic fixtures | Только predicate, не deletion/authority |
| Fake authority snapshot/reserve/materialize/commit/release отказ | Handwritten fake subtype fixture | Нет concurrency/native proof |
| Four writers, nested/finalizer named strict guard | Fake event log с недостижимым mutate | Проверяет общий guard, не фактические writer тела |
| Atomic callback и stage path strict refusal | Direct helper fixture definitions | Не выполнены, нет FS mutation |
| Partial→next denial, pre/post rename, invalid/protected generation | Только указан remaining control | Lifecycle отсутствует, данных недостаточно |
| Unknown unlink debt, success-deferred→one-byte-short | Только указан remaining control | Нельзя заявлять conservation test passed |
| Primary/secondary/finalizer | Только указан remaining control | Lifecycle отсутствует |

Fixture file намеренно не подключён в runtests до разрешённого исполнения и
независимого source review. Никакие Julia/import/compiler/parser/scripts,
tests/linter/formatter, native/network/solver команды не запускались.
`git diff --check` выполнен, без диагностик; это только whitespace проверка.
Source diff просмотрен ограниченными excerpts. Нужен новый independent high CPP.

## Read/output ledger и бюджет

Использовались только shell read-only inventory/rg/sed/head/hash/git/diff и
apply_patch; существующие результаты не открывались. Читались D1/D2/review,
using-superpowers (с явным subagent-stop), root/Runner architecture и owning
source symbols, перечисленные в call-cleanup-table; добавлялись только source,
fixture и пояснение Runner. Полные source/archive datasets не читались.

Начальные несколько tool responses превысили per-response 3000-character cap
из-за длинных строк design/source; часть вывода tool была truncated. Это нарушение
не скрывается. Затем применялись ограниченные excerpts, но не каждый response
измерен в символах. Совокупные read/output bytes, peak RAM и CPU НЕ измерялись;
точное соблюдение 4MiB/96KiB/1GiB не заявляется. Disk sizes артефактов измерены
отдельно, они не эквивалентны aggregate read/output ledger. Никаких тяжёлых jobs.

## Передача

`/tmp/qcl-sci08-r2-i1-identity.json`: точные before/after SHA256 по каждому
owning path, absent явно обозначен. `/tmp/qcl-sci08-r2-i1-complete.patch` включает
tracked и новые файлы. `/tmp/qcl-sci08-r2-i1-call-cleanup-table.md` содержит
named-edge source inventory. Parent владеет CP/READY/ops и независимым review.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Strict staged обход закрыт source guard | scratch_execution preflight и forwarding diff | Runtime не проверен | изменить |
| Unknown/overflow не выдаёт arithmetic admission | resident_storage predicate + handwritten fixtures | Predicate не permit; fixtures не исполнены | сохранить |
| Production strict остаётся fail-closed | scientific preflight + новые writer guards | Нет writer lifecycle | сохранить |
| Полный SCI08-R2 writer-ready | Отсутствуют permits/settlement/native proof | Нельзя снимать refusal | данных недостаточно |
| Source готов к независимому CPP | Полный patch + hash identity + named-edge table | Независимого review ещё нет | дополнительно измерить |
