# DEV11 — Portal composite export consumer: author candidate

Дата: 2026-10-19. Исполнитель I / gpt-6.1-sol / medium. Этап: изменение owning Portal source и ограниченные engineering fixtures. Статус: **awaiting independent CP-CODE**, без commit/push/merge/deploy. Product files frozen после final candidate; результаты ниже не являются полной release/scientific приёмкой.

## Immutable packet и границы

- Root worktree `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `e0f244d075dd49874ba4f3847f4efa693f3b3622`.
- Portal baseline `36837e98a8d1f85820f2807d0212ec92e73c3c7b`; новая ветка `codex/review-closure-export-consumer` остаётся на этом HEAD с uncommitted candidate.
- Producer AiiDA `5579d55684939495230241f446b7ea07c8ae0224`, accepted `docs/export-selection.md`; Contracts `e5c056c47fc3bde3e0ca32866692d740ef9b325c`; Results `fe27a2a9ed065f9afacecc84113311f30d0c68d6`.
- Review diff `/tmp/qcl-dev11-review.diff`, SHA256 **775fd77480598ad1be338282957ce62ae989688d88fd0070e63236afea773a98**, 56031 bytes. Diff against Portal baseline включает untracked `frontend/tests/export-selection.test.ts`.
- Изменены только десять разрешённых paths: README; frontend `src/{api.ts,main.tsx}`, `tests/export-selection.test.ts`; backend `src/qcl_negf_api/{service,exports,api}.py`; `tests/{test_exports,test_api,test_service}.py`.
- Соседние gitlinks/root staged/untracked changes сохранены. Не менялись lockfiles, actor lifecycle, auth/capability, formula/status policy владельцев, светлая тема или существующие spool/reserve/receipt-tail guards.

## Реализация

`ExportStore.create` canonicalizes full run UUID, получает exact selection ровно один раз, проверяет четырёхполевой scalar response и отделяет binding до следующего service call. Exact selected inventory проверяется целиком: shape/bounds/identity/path/size/duplicates; foreign row не фильтруется. Cache lookup идёт после resolve/inventory, использует `(run,execution,attempt,CalcJob,profile)` и дополнительное равенство frozen status. Изменившийся status оставляет старый export ID неизменным до TTL; занятый worker возвращает прежний busy/409.

Preparation передаёт оба selectors в frozen-plan и каждый payload open, не вызывает `get_run` или повторный selection resolve. Results получает literal selected frozen status; `unknown`, `paused`, `running` не заменяются на другой status. Missing producer operation fail-closed /503. Ошибки selected metadata сохраняют 422/404; asynchronous plan/copy failure сохраняет failed preparation и cleanup.

HTTP body принимает strict positive integer attempt, full UUID string и null/omitted forms. Новые actor operations добавлены в существующий owner-thread registry. Frontend отправляет оба selectors выбранного child, отображает returned attempt/CalcJob/status и продолжает authorize/download по exact export ID через native browser transfer.

## Проверки и первичные receipts

Все test/check commands исполнял root coordinator в общем slot; writer не запускал tests самостоятельно. Ни один guard не сработал.

| Packet | Фактический результат | Raw/receipt |
| --- | --- | --- |
| RED-1 | 3 semantic failures `all-attempt inventory read`, 10 deselected; дефект baseline consumer воспроизведён | `/tmp/qcl-DEV11-RED-1/{original.log,receipt.json}` |
| GREEN-1 | Collection error: отсутствовал уже locked `httpx2`; не semantic failure | `/tmp/qcl-DEV11-GREEN-1/{original.log,receipt.json}` |
| RED-NODE-1 / NODE-DIAG-1 | Sandbox whole-file failure без достаточного semantic evidence | `/tmp/qcl-DEV11-{RED-NODE-1,NODE-DIAG-1}/{original.log,receipt.json}` |
| NODE-DIAG-2 | Под escalated context: missing `prepareExport` semantic RED; existing native download 1 pass | `/tmp/qcl-DEV11-NODE-DIAG-2/{original.log,receipt.json}` |
| GREEN-2 | **125 passed, 1 failed**: единственный failure `test_browser_is_served_from_the_python_package` (404, отсутствуют compiled static assets) | `/tmp/qcl-DEV11-GREEN-2/{original.log,receipt.json}` |
| GREEN-NODE-1 | **9 passed**: existing api tests + new explicit child POST/returned status/native download test | `/tmp/qcl-DEV11-GREEN-NODE-1/{original.log,receipt.json}` |
| TSC-1 | **exit0** `tsc --noEmit`, без diagnostics | `/tmp/qcl-DEV11-TSC-1/{original.log,receipt.json}` |
| Diff check | `git diff --check` exit0 на final frozen candidate | Author read-only command; no separate runner receipt |

GREEN-2 выполнял ровно три файла `test_exports.py test_api.py test_service.py`; никакого deselect/xfail и изменения падающего assertion не было. Полный component suite, Ruff, frontend production build, wheel/full build, CI, server и solver в этом candidate не выполнялись.

Root отдельно восстановил locked test extras; evidence `/tmp/qcl-int01-python-extras-2-receipt.json`: Python3.14.7, httpx2 2.13.1, TestClient synthetic GET200, source imports owning checkouts, lock hashes unchanged. Этот environment setup учитывается отдельно, не скрывается в successful tests.

Первый RED packet запрашивался до дописывания дополнительных cases; до уведомления о его старте writer дописывал другие tests. Исходные три target cases не менялись, raw collection показывает исходные 10 deselected; stronger immutable-all-files RED source claim не делается. После согласования freeze GREEN/Node/TSC packets выполнялись без product mutations. Исходные environment/sandbox failures сохранены, не переименованы в semantic RED.

### Что различают synthetic fixtures

Real AiiDA producer selection/inventory/frozen-plan/open functions работают над synthetic ORM/repositories без profile/daemon. Два attempts содержат одинакового размера разные `AAAA`/`BBBB` bytes в общем path и разные disjoint paths. Два plans различаются raw whitespace, но decoded-equal с workflow input. Oracle проверяет literal bytes2, selected raw plan2/source2, status2, отсутствие child1 opens и единственный resolve; publication меняется после resolve. Затем проверены другое cache/export ID для child1 и неизменность старого status. Отдельно покрыты same-child unknown→known status, busy409 во время подготовки, TTL, legacy one-child four selector forms, invalid/mismatch/foreign selectors до payload, invalid producer rows и отсутствующий new operation.

Storage/native regressions сохранены: explicit failed retry, shutdown callback, exact frozen plan, no-copy invalid plan, derived spool budget, free-space change, receipt tail, retained accounting, Range/If-Range/cookie scope, existing single-file exact-child race/error checks. Actor fixture проверяет owner thread/loop для additive operations без изменения lifecycle.

Results exporter здесь заменён bounded test exporter с прямым чтением/assertion selected bytes и записью их в tiny archive, поэтому tests доказывают consumer binding/data flow и admission/cleanup, **не** полную scientific schema/real archive validation. Нет scientific arrays, SCBA/Poisson, numerical acceptance или experimental validation.

### Единственный failure GREEN-2

`src/qcl_negf_api/static` отсутствует в свежем managed worktree; `.gitignore:10` исключает generated assets. Baseline `36837e9:src/qcl_negf_api/api.py` и candidate имеют один и тот же хвост `if static.is_dir(): app.mount(...)`; baseline browser test содержит тот же GET `/` и assertion200. `hatch_build.py:12` требует compiled index/assets для distributable wheel; README описывает frontend build как их источник. Это не изменённый DEV11 route. Готовый browser bundle не выдумывался, assertion не ослаблялся. Source-wise baseline diagnosis установлен; отдельный baseline runtime не запускался. Полная package/browser asset приёмка остаётся отдельным gate.

## Ресурсы

Восемь DEV11 runner receipts выше: суммарно **16.295 s wall**, максимальный sampled process-tree RSS **323313664 B** (TSC), всего stdout/stderr **13855 B**, sampled basetemp bytes0, stop_reason=null. Каждый packet: affinity1CPU, wall90s, sampled RSS1GiB, temporary16MiB, output2MiB. RSS — sampled guard, не hard cgroup quota. Actual CPU time и полный `/tmp` high-water не измерены; нулевой basetemp не утверждает нулевой filesystem I/O. Root environment setup отдельно: 125.315s, .venv delta29708227B, locks unchanged. Общий admission/accounting и чужие reserves принадлежат root coordinator.

## Решения

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Composite export сохраняет один exact child для inventory/plan/bytes/status/cache | Diff `exports.py::create/_prepare`; GREEN-2 targeted cases с literal bytes/plans/status | Synthetic ORM и bounded exporter, без real profile/архива | изменить |
| Legacy one-child и native download/capability/storage semantics сохраняются | GREEN-2 positive selector forms и existing regression assertions; Node9pass | Packaged static route не прошёл, full suite/build не выполнены | сохранить |
| Scientific status не выводится из process exit и immutable для export ID | Real producer failed/exit0, missing-result unknown, changed-status/busy/cache fixtures | Recorded scientific status не доказательство convergence | сохранить |
| Candidate полностью готов как distributable web release | GREEN-2:125pass+static404; Node9pass; TSC0 | Нет compiled assets, wheel/native/server/CI приёмки | данных недостаточно |
| CP-CODE и публикация завершены | Immutable author diff/report готовы | Независимый reviewer ещё не вынес verdict; commit/push отсутствуют | дополнительно измерить |
