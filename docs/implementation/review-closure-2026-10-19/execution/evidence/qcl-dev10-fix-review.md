# DEV10 R1 — независимый narrow static re-review

2026-10-19, /root/reviewer, gpt-6.1-sol high.
Final verdict после GREEN3: **CP-CODE PASS; DEV10-R1 ADDRESSED.**
Первый narrow review давал static addressed/runtime NOT_VERIFIED. Ниже сохранены
его основания; финальное обновление с regression evidence находится в конце.

Проверен corrective delta `/tmp/qcl-dev10-fix-delta.diff` и соответствующие
live source/test hunks. Full candidate `/tmp/qcl-dev10-fix-review.diff`
SHA256 `d4392d21c6ef1c48ffa4c7f3061e98fce4a6ab2053ffb429cd310315c9febebb`;
updated report SHA256 `f7a3ba803d2b72cdd4b56e41cdd1765e288c6372397c63b52517a839e9d59730`
независимо измерены и совпали с handoff. Base67287afb, scope прежний.

`service.py:155–159` теперь проверяет required published execution_id string
length1–128 до applicability filter. Missing/None/nonstring/empty/oversized
record не становится отсутствующим: exception выходит до candidate selection
и selected result/inventory reads. Valid other-execution record по-прежнему
пропускается; explicit selector path и old single-file semantics не изменены.

Новые fixtures: обе operations ×5 invalid-ID variants с soleC2, exact error
message, no result handle/payload events и forbidden inventory read; отдельный
valid-other positive проверяет literal identity/status/inventory. Exact error
assert не позволяет пойманному AssertionError из forbidden inventory скрыть
позднюю проверку: wrapper translation имела бы другой message. По чтению
fixtures различают исходный defect и чрезмерный reject-all fix.

Новых test/import/build invocations0. Прежние107passed относятся к pre-fix
source и не являются current runtime pass; все4/4 calls остаются исчерпанными.
Report явно сохраняет old evidence и этот gap.

Конкретный CP-EXCEPTION packet: одна дополнительная targeted invocation
трёх прежних test files на frozen current candidate, прежние1CPU/1GiB/90s,
16MiB temp/2MiB logs, no setup/full-suite; сохранить actual command, import
ownership, hashes, exit/status и original log. Этот review не активирует
exception и не расходует дополнительный slot.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 malformed-ID fallback устранён | service.py155–159 и direct negative/positive fixtures | Static source reasoning | сохранить |
| Current candidate прошёл regression | СтарыйGREEN2 для другихbytes | Новый check ещё не разрешён/не выполнен | данных недостаточно |
| DEV10 CP-CODE полностью закрыт | Source fix reviewed, runtime gap открыт | Нужен конкретный finite exception/check | дополнительно измерить |

## Финальное обновление после authorized GREEN3

Coordinator передал новое прямое human resource grant; дополнительный
targeted check выполнен root, reviewer не запускал tests повторно.
`/tmp/qcl-DEV10-GREEN-3/receipt.json` SHA256
`abf7111146ad3621ae09f9c9e1446b85a0be82f4ea8adecafed244e66ddd7d4f`;
`original.log` SHA256
`a436cbdac0b203d1627e8ae967813190f0a00dc9707cf13da4befccfef13b31d`.
Reviewer прочитал оба файла и независимо измерил hashes.
Log: **118 passed**, receipt exit0, wall4.120s, sampled tree RSS145096704B,
output180B, temporary0B, stop null. Command включает те же три targeted
files, выбранный owning `.venv/bin/python`, root cwd, no cacheprovider.

Полный package SHA остаётся d4392d21…febebb; четыре final file hashes
сверены с fix report и не изменились. Reverse-apply check exact package к
current owning files exit0. Новая narrow regression закрывает прежний runtime
gap; pre-fix107green остаётся только historical evidence. Других load-bearing
findings при предыдущем полном и текущем scoped review не найдено.

**CP-CODE PASS ограничен exact producer source и synthetic targeted fixtures.**
Native AiiDA daemon/profile, Portal DEV11 archive/cache integration, full suite,
build, server и scientific acceptance этим результатом не устанавливаются.
