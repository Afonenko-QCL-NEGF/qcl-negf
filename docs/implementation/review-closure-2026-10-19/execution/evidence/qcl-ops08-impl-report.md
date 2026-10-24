# OPS08 — узкая реализация R1/R2 и R3

Статус: SOURCE IMPLEMENTED, independent high CPP и Root GREEN pending. Этап реализации поручен Root после source review PASS (`308b4e69…`) и observed RED. Writer не запускал runtime/import/parser/tests/build/network и не создавал commit/checkpoint. Изолированный `/tmp/qcl-ops08-worktree`, ветка `codex/review-closure-maintenance-failure-boundaries`, base `f5bc368654414039f7368bb19ca3201fa7f29f9d`.

## Before: различающее свидетельство

Прочитаны receipt и original log `/tmp/qcl-OPS08-RED-1/`. Receipt SHA256 `ff3740d1df91ce4c9edaae78b0a0e7d1007998527560c73b2af84b47442c3adf`, raw SHA256 `8aa4fecb085cc1c24c5f7818f334dc2daf7aca3598c2bf204f1c136985bc9890`. Root запуск: **8 failed, 3 passed**, wall6.365s, exit1; raw complete, guard_error/stop_reason отсутствуют. Sampled peak RSS68,263,936B/TMP65,484B — sampling, не hard peak proof.

R1: три correct-schema/correct-node release negatives (`ready_false`, `ready_missing`, `wrong_valid_release`) получили `second.status=verified` вместо literal not_attempted. Причина — catch `_deliver_pool_owned` выставлял failed, но break зависел от CommandFailure/uncertain. Known negative — реальный failure required node, но не native unknown.

R2: три local journal/unlink faults и recovery-close sibling оставляли summary без requires_reconciliation; deadline sibling сообщал open=True вместо unknown. Причина — `_finish_owned` после открытия admission находился вне существующей try/close_after_failure границы remote worker finish. Healthy и wrong-schema/node uncertain controls прошли на неизменённом production base.

## After: causal source delta

`ops/application_release.py::_deliver_pool_owned`: после любого перехваченного failure required node выполняется unconditional break. Existing failed status, CommandFailure record и uncertain classification остаются. Поэтому ни следующая identity/copy/activate/check, ни admit/RESUME/finish не могут быть вызваны циклом после такого failure. Не выставляем invented unknown/reconciliation для known semantic release negative.

`_deliver_cli_locked`: `_finish_owned(owner, deadline=deadline)` перенесён внутрь уже существующей post-open try после обоих worker finish responses. Его fallible local journal publication и own lifecycle-intent unlink теперь используют тот же `close_after_failure(report,expected,gate,owner,deadline)` и checkpoint. Не меняли publisher, owned artifact checks, journal contents, originals или удаление blocker; не добавляли retry.

Если финализация дала CommandFailure, исходный `.record` сохраняется в existing `report.command_failure`; исходный текст ошибки сохраняется как `admission_error`. Local fault больше не обходит recovery, но failure не превращается в успешное завершение. Recovery использует исходные owner/deadline/selected-release authority; никакого force-close, продления deadline или нового cleanup budget.

Если close publication подтверждено, existing helper даёт failed/reconciliation/open=False/admission_state=closed. Если deadline уже истёк, owner недействителен, gate чужой или recovery publication не удалось подтвердить, existing helper даёт **open=None, admission_state=unknown, critical_admission_failure=True**. Фактические bytes могут при этом оставаться open=True. Данная реализация не утверждает закрытие без свидетельства. При deadline checkpoint сохраняет прежний durable pending receipt и выдаёт truthful in-memory summary по existing policy; это не fresh durable receipt после expiry.

`docs/application-cd.md:382`: factual typo `32 MiB` → `64 MiB` per action. `UpdateScan.CAP` не меняли. Никакого изменения physical/scientific model, cancellation/force/ownership policy, cap или trust model.

## Файлы и artifacts

- Production SHA256 `e5537f1bc8825e2b4b93194b6c19cdd87a5296a0b42cf00bd3492110008813a8`.
- Docs SHA256 `1bf0d6229cb0135940ce8f3731a62eb687c8a62d9200a740fbbfdaf7bf57547b`.
- Approved fixture SHA256 **не изменён**: `4cf04db2e0884afd5c0ec24171df29374c363569209b2fd0c181f3a23b7c73ad` (11 nodeids в `/tmp/qcl-ops08-red-report.md`).
- Production/docs delta `/tmp/qcl-ops08-impl-delta.patch`, SHA256 `16c2ecc0d876f34f54dd7df697d2781122126a4db867a0c77a36ced3e8c9adef`.
- Полный relative-path patch, включая original approved fixture: `/tmp/qcl-ops08-impl-full.patch`, SHA256 `56e2d88bc8d51891f77c6671c6acc71ddf34e839d32f7f9e3cab83a9010c1271`.

Tracked production/docs diff **9 insertions, 5 deletions**. `git diff --check` exit0. Diff просмотрен полностью. Единственные tracked изменения — два порученных файла; новый approved tests файл сохранён без ослабления. Original RED receipt/raw, private inputs, foreign/native/S01/data не изменены.

## Предел проверки и ресурсы

Writer test/import/parser/runtime calls **0**. GREEN не заявляется. Independent high CPP обязателен перед Root единственным оставшимся GREEN; общий OPS08 cap2, OPS03/C08/full-CI counters не сбрасываются. Source-only вывод не доказывает native services/NFS/Slurm/AiiDA или scientific acceptance. Нового D не потребовалось: existing failure/close policy сохранена.

Assigned source phase ≤30min/1CPU/2GiB/read8MiB/output128KiB. Cached source trace использован повторно; новые product reads ограничены patch/diff/hash artifacts. Ledger `/tmp/qcl-ops08-impl-read-ledger.tsv` консервативно резервирует полные file passes и 256KiB для skill/receipt/raw/report. Charged upper-bound3,158,727B <8MiB. Ledger — логический reserve, не измерение physical OS I/O; точные RSS/aggregate output bytes writer не измерял. Original source-auditor FAILED_RESOURCE_CAP остаётся отдельным фактом, не переоценён.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 различён observed RED | 3 named semantic-negative failures в original raw | Synthetic host/commands, native не измерен | изменить |
| R1 прекращает любой required-node dispatch failure | Unconditional break в узком diff | After runtime ещё не выполнен | дополнительно измерить |
| R2 final local journal/intent использует existing recovery boundary | Move `_finish_owned` внутри try; raw5 failing siblings | Не universal crash-atomic protocol; deadline запрещает close без authority | изменить |
| Неизвестное закрытие не объявляется closed | Existing close_after_failure unchanged; report propagation | Actual gate при failed close может оставаться open | сохранить |
| Документирован actual64MiB cap | One-line doc diff, code CAP unchanged | Logical budget, не native physical I/O measurement | изменить |
| GREEN/full-final/native/science получены | Нет новых таких свидетельств | Root execution и CPP pending | данных недостаточно |

STOP: реализация передана Root, новых source reads/runtime calls не выполняю.
