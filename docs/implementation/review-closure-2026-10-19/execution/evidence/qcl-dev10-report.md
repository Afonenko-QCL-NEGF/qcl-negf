# DEV10 CP-CODE correction — author round 2/5

2026-10-19. I medium gpt-6.1-sol. Статус: узкий source/test candidate по independent CHANGES_REQUESTED; GREEN-3 подтвердил 118 passed на текущем исправлении, ждёт final independent CP-CODE receipt review. Прежние GREEN2 `107 passed` относятся к source до этого исправления. Первые 4/4 invocation бюджета сохранены и исчерпаны; GREEN-3 отдельно выполнен root по новому прямому user engineering resource grant, без сброса прежнего счётчика. Автор новых test/import/build процессов не запускал. Shared test slot свободен. Commit/push/branch switch не выполнялись.

## Primary evidence и исправление

Independent reviewer обнаружил воспроизводимый source counterexample: в `_export_child` после dict-type check `record.get("execution_id") == requested` игнорирует запись без execution_id либо с None/nonstring. Если оставить единственный C2, malformed publication превращается в legacy fallback, после чего читаются selected result/inventory. Это противоречит accepted `docs/export-selection.md` paragraph5/error table: malformed published metadata -> ValueError/422 до selected metadata read, без fallback. Прежний fixture matrix не покрывал missing/invalid execution_id.

Исправление проверяет тип и длину published execution_id (string1–128, как request contract) до фильтрации на requested execution. Только record с валидным другим execution ID игнорируется, сохраняя allowed single-child legacy resolution. `_select_child`, `_attempt` и existing single-file APIs по-прежнему не менялись. Изменение confined `src/aiida_qcl_negf/service.py` и `tests/test_export_selection.py`; contract docs, Portal/Runner/Core/physics не менялись.

Добавленные meaningful fixtures (вошли в GREEN-3):

- `test_malformed_published_execution_id_never_uses_single_child`: обе новые операции x missing/None/nonstring/empty/oversized published execution ID, единственный C2; требует точный published-invalid ValueError, отсутствие selected result handles и repository events. Selected inventory read дополнительно запрещён; если до него дойти, другое error message не удовлетворит assert.
- `test_valid_other_execution_publication_allows_single_child_fallback`: valid different-execution publication + sole C2 даёт literal identity/status и selected-only literal inventory; положительный контроль не позволяет отвергать все unrelated publications.

Fixtures записаны перед source fix; дополнительный pre-fix RED не выполнялся вследствие exhausted-budget ограничения. После нового прямого user grant root выполнил GREEN-3: все 118 targeted cases прошли, включая новые fixtures. Это не заявляется отдельным завершённым RED/GREEN cycle для corrective hunk.

## Immutable current candidate

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, source composition исходно root `e0f244d075dd49874ba4f3847f4efa693f3b3622`, AiiDA baseline `53e2a20544a469dd7ee5560243ebe530a6310f0a`. Owning branch `codex/review-closure-export-selection`, base/HEAD `67287afb53960b27e830b529c2149833db92a0ba` (accepted DEV09 docs).

Current complete review diff `/tmp/qcl-dev10-fix-review.diff`: **26773 bytes**, SHA256 `d4392d21c6ef1c48ffa4c7f3061e98fce4a6ab2053ffb429cd310315c9febebb`. Содержит full permitted diff относительно67287afb с append untracked new test через no-index, а не только corrective hunk.

| Current file | SHA256 |
| --- | --- |
| src/aiida_qcl_negf/service.py | 5cd701303c1c5416c5c593ecc6574e9e2bcdbddc35cca900d001ba06cc835cd5 |
| tests/test_export_selection.py | 3ae667df4237e9a75d38ab66a107c94d741621ff827f6f841712d9eed8c31754 |
| tests/test_export_plan.py | cc8b8c878e8a8a60570e7e1acc75be0a07abbb4f80adb29f7418938ba1de9814 |
| README.md | 0cfb04d64e01def176ab946c4b7740cb0c995287f20abc8c649e5f6cbb0b7486 |

Source-only checks выполнены после corrective write: `git diff --check` exit0, прочитан точный corrective hunk и fixtures; no-index diff exit1 ожидаем для добавленного файла. Targeted runtime checks на текущем candidate выполнены root в GREEN-3; receipt и log ниже прочитаны автором. Код и test contents после GREEN-3 не менялись.

## GREEN-3 по новому прямому user grant

Координатор передал новое прямое решение пользователя: для engineering использовать все доступные ресурсы здесь и в будущей работе. Прежние bounded receipts не переписаны; strict science S1 и единственный final CI остаются без изменений. Этот grant разрешил отдельную конечную GREEN-3 проверку; он не объявляется расширением scientific scope или разрешением rerun final CI.

Root как единственный runner выполнил `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/.venv/bin/python -m pytest components/qcl-negf-aiida/tests/test_export_selection.py components/qcl-negf-aiida/tests/test_artifact_locator.py components/qcl-negf-aiida/tests/test_export_plan.py -q -p no:cacheprovider --basetemp /tmp/qcl-DEV10-GREEN-3/tmp`, cwd `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.

- Начало 2026-10-19 12:39:01.737431 UTC; receipt 12:39:05.857391 UTC.
- Exit0, **118 passed** (pytest0.38s), measured wall4.12s; sampled peak process-tree RSS145096704B, output180B, temporary0B, stop_reason null.
- Retained run bounds90s/1CPU/1GiB sampled RSS/16MiBtemporary/2MiBlog; no sync/download, prepared locked Python3.14 env. Это выбранный finite run envelope внутри нового engineering grant.
- `/tmp/qcl-DEV10-GREEN-3/receipt.json` SHA256 `abf7111146ad3621ae09f9c9e1446b85a0be82f4ea8adecafed244e66ddd7d4f`.
- `/tmp/qcl-DEV10-GREEN-3/original.log` SHA256 `a436cbdac0b203d1627e8ae967813190f0a00dc9707cf13da4befccfef13b31d`.

Автор прочитал полный actual receipt/log и повторил только source-only `git diff --check` (exit0). Никакого дополнительного тестового процесса автор не запускал. Current full diff SHA256 остаётся `d4392d21c6ef1c48ffa4c7f3061e98fce4a6ab2053ffb429cd310315c9febebb`.

Round2 pre-GREEN3 report сохранён `/tmp/qcl-dev10-report-round2-before-green3.md`, SHA256 `f7a3ba803d2b72cdd4b56e41cdd1765e288c6372397c63b52517a839e9d59730`; его отсутствие current runtime evidence отражает прежний момент времени и superseded GREEN-3. Суммарно пять сохранённых invocation,20.845s measured wall; первые4 не скрыты и не сброшены.

## Сохранённое historical evidence

Неизменённый round1 report `/tmp/qcl-dev10-report-round1.md`, SHA256 `d0b759b577dbd80d2fb04463d073aa009d65e7ef2eb79f5fb7c8c8f4d1a82712`, содержит exact commands, Python3.14.7 owning import receipt, все original RED/GREEN logs и hashes, envelope и limitations. Round1 diff `/tmp/qcl-dev10-review.diff`, SHA256 `93049ef348031c992b53dbc25ea02778e1da4add07d920ea6d38db6e96943b1d`, сохранён. Это исторические candidate evidence, не current pass.

Budget receipt chronology: RED1 missing operations74failed -> GREEN1 106passed -> RED2 present malformed attempt DID NOT RAISE -> GREEN2 107passed. Всего4/4invocation,16.725s charged wall; каждый≤90s,1CPU/1GiB sampled guard,16MiB temporary,2MiB logs; no stop. Original logs `/tmp/qcl-DEV10-{RED-1,GREEN-1,RED-2,GREEN-2}/original.log` и receipts сохранены. Source change текущего round2 инвалидирует GREEN2 как evidence final current runtime behavior.

Full suite, actual native AiiDA profile/daemon, Portal archive integration, build, network, server, solver, scientific convergence/physics/adequacy/experimental validation не выполнялись и не заявляются. Независимый reviewer должен проверить corrective source semantics и actual GREEN-3 receipt перед publication; новых полномочий этот отчёт не выдаёт.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Malformed published execution_id ранее допускал fallback | Independent source counterexample + прежняя ветка filter/fallback | Новый runtime reproduction не запускался | изменить |
| Current fix отвергает malformed ID до фильтрации/metadata | Corrective hunk + negative fixtures/valid-other positive; GREEN-3 118 passed | Final independent CP-CODE receipt review pending | изменить |
| Current candidate имеет targeted runtime pass | GREEN-3 exit0,118 passed на unchanged current diff | Synthetic boundaries; не full suite/native/science acceptance | сохранить |
| Прежний бюджет и failed evidence сохранены | Четыре original receipts/logs + отдельно GREEN-3 по новому user grant | Engineering resource grant не расширяет science S1/final CI | сохранить |
