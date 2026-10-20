# SCI08-R2 I1 — независимый high CPP, partial refusal-only

2026-10-20. **PASS_SOURCE_PARTIAL для заявленного refusal-only scope; новых блокирующих source findings в этом scope не обнаружено. Полный SCI08-R2 не завершён и writer-ready не стал.** Отсутствующие permits/lifecycle/cleanup здесь не основание отклонить ограниченный I1: автор явно сохраняет unconditional strict refusal. Вердикт не является выполненным тестом, native acceptance, CP-SCI READY или разрешением исполнения.

Объект: owning worktree `/tmp/qcl-sci08-r2-runner-worktree`, branch `codex/review-closure-sci08-r2-resident-lifecycle`, HEAD `4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`. Полный patch прочитан byte chunks: SHA256 `296de59f4bfbd30543c540f9710892e7f7c9f947b24646dc43ca45660f6aebbc`; identity `362de806b022e94185fc56d6ac63b867fb3021775fe3fb8d6b0a87b3d637bf65`. After hashes всех 12 путей непосредственно сверены с identity, совпали. HEAD неизменён; status показывает девять изменённых tracked и три новых untracked файла, ожидаемые в patch. Recursive submodule status пуст. Исходный Root107/Runner4f60 и D1/D2/high D2 сохраняются; Gitlinks — source authority, review JSON — forensic record, не revision lock.

## Проверенные свойства

1. `src/infrastructure/resources/resident_storage.jl:34–45`: predicate принимает только non-Bool `Integer` в `[0,typemax(Int)]`, складывает через checked_add и сравнивает `E+U+P+S≤A` и `U+P+S≤H`. E не debit второй раз к remaining H. Unknown/nothing/negative/Float/Bool/out-of-range не проходят; overflow сумм возвращает false. Predicate не создаёт proof/lease/permit и отдельно оговаривает physical/inode/freshness obligations. Integer restriction консервативен, Double/coercion overflow не введены.
2. Там же `:17–26`: все abstract-authority default methods, включая release, бросают typed refusal. `UnavailableResidentAuthority` не выдаёт snapshot или capacity. `:48–56` возвращает nothing лишь для standalone, strict безусловно бросает refusal, unknown policy отклоняется. Поле verified_state остаётся unknown, не pass.
3. `scratch_execution.jl:140` вызывает существующий `_scientific_resource_preflight` раньше scratch mkdir/temp. В прямой scientific путь и local scientific путь передаются resource_policy/envelope, в delivery — resource_policy. Существующий preflight в `native_phase_telemetry.jl:237–247` при strict всегда бросает: без envelope needs_admission, с envelope bindings pending. Поэтому strict staged invocation не создаёт workspace и не доходит до success `rm(workspace)` (baseline156, теперь163).
4. Новые guards стоят первыми statements в `commit_point_artifacts`, `commit_operator_artifacts`, `stage_result_tree`, `ScientificHistoryRecorder`, `flush_scientific_history!`, `_import_completed_archives!`, `_atomic_checkpoint`, `_observability_atomic_text`, `_atomic_replace_file`. В history guard предшествует даже `recorder.segment+=1`. В atomic replace — chmod/rename. У atomic text обе positional/do формы передают resource_policy. Guard до входа в try не запускает прежний destructive catch/finally. Проблемный partial scenario D2 здесь не создаётся, поскольку strict не входит в writer.
5. `scientific_execution.jl` передаёт policy в imports, operator, history constructor, recovery/final history flush и point commits, history finalizer. `_resident_writer_preflight` импортирован в `QCLScientificWorkflow`; его defining include предшествует atomic/helpers/scientific workflow. Staged code находится в parent module, где уже определены ExecutionEnvelope/default_execution_envelope и `_scientific_resource_preflight`. Отсутствующих bindings на прочитанных edges не обнаружено.

Standalone default остаётся `:standalone`, envelope default — существующее nothing. Новый early staged preflight с этими defaults не мутирует состояние и возвращает nothing; forwarding передаёт прежние defaults. Существующие positional arguments и do signatures сохранены; publish/fsync/verify/receipt/pointer/rename/cleanup statements не перемещались. Это source compatibility reasoning, не исполненный standalone regression control.

## Граница фактического покрытия

Заявленный narrow staged bypass закрыт. Однако низкоуровневые guards не являются persistent context: atomic text вызывает atomic replace без keyword; nested save_checkpoint и автоматические history flush вызываются по прежним standalone defaults. Через текущий strict entry это безопасно лишь вследствие более раннего безусловного отказа. Эти вызовы нельзя выдавать за готовое strict writer enforcement. Авторская таблица прямо отмечает incomplete forwarding/NOT READY; ложного writer coverage в заявленном результате не найдено.

Binding cleanup edges прежнего high D2 сохраняются: workspace success rm, import temp finally, post-checkpoint imported-* rm и optical pending finally. I1 не меняет эти cleanup тела и не выдаёт deletion credit. Они недостижимы из strict scientific/staged entrypoints благодаря отказу до mutation. Нет обещания удержать partial при admitted strict writer — admitted strict writer отсутствует. Также существующие standalone entrypoints/CLI остаются standalone; это не доказательство campaign enforcement без будущего binding C1/A1.

Fixtures `test/contracts/resident_refusal_contract.jl` прочитаны. Arithmetic/default-authority assertions — unexecuted definitions; fake operation-name loop проверяет только общий guard. Он не достигает four writer bodies, import/delete/optical/finalizer и не является fault-injection coverage этих traces. Автор это явно раскрывает. Только atomic text и stage имеют direct named helper definitions; do-order/point/operator/history/staged controls ещё не доказаны. `100-40==60` — буквальная константа, не lifecycle/unlink evidence. File не подключён в runtests. RED/GREEN, tests passing или выполненные controls не заявляются.

## Что остаётся finite I-ready

Нового общего design gap не найдено: D1+D2+high D2 задают конечный owning ticket. Продолжение полного R2 может реализовать proof identity/domain/snapshot/inventory, parent/child permits и monotonic settlement, затем context-aware writer/cleanup hooks и handwritten controls. Пока этого нет, нельзя снимать общий strict refusal.

| Обязательный remaining edge | Требуемое source/fixture evidence до writer-enabled claim |
| --- | --- |
| Point/operator/history/stage → atomic/temp/helper → catch/finally | Context до первого mutator, explicit non-auto cleanup lifecycle; actual partial→next-denial retained, old verified state unchanged, debt не released. |
| Scratch workspace rm; import finally; imported-* rm; optical pending finally | Guarded eligibility либо strict branch refusal до mutation. Replacement result не доказывает покрытие всего workspace/import lifetime. |
| Rename→receipt/index/pointer acknowledgement и history finalizer | Pre/post-rename outcomes; failed history needs-reconcile без blind sequence reuse; original/secondary errors; stop uses только заранее bound capability. |
| Existing broad recovery prune и successful duplicates | Protected/failed/final/unacknowledged/invalid receipt сохранены; authority+verified durable replacement+actual unlink/lifetime proof перед E release; H не увеличивается на filesize. |
| Arithmetic/authority/compatibility controls | Literal cap/free exact/one-byte-short, disjoint views/IDs/overflow/unknown; actual caller fixtures, do-order signatures и standalone ordered publication. Выполнение требует отдельного grant. |

Native finite HDF5 physical growth, ownership/quota/inode capacity, C1 persistent authority, R3 stop, P2 cumulative I/O и A1 consumers остаются отдельными gates; unknown → refusal. Caps shared2 TiB/attempt128–256 GiB сохранены как ограничения, не capacity proof. Нет cleanup/cap raise/model fallback. Frozen S1 no-ee, LO/acoustic/impurity/IFR/alloy, 0 mV/period,70 K, grids/basis/tolerances/full_final в patch не менялись. R1 qualified349 PASS не переносится на I1. C08 SCI05/SCI08 **8/8 EXHAUSTED**.

Проверка: source/patch/hash/read-only Git и `git diff --check` (без диагностик). Не выполнялись Julia/compiler/import/parser/project scripts/tests/native/network/solver/CI. Полный callgraph и физика транспорта не аудировались; fixture source не означает execution. Использован ранее прочитанный qcl-performance-audit для storage source scope, physics audit не требовался. Reviewer не менял worktree/index/CP/READY, создал только два review outputs. Дети не создавались.

В начале review report/identity и позднее некоторые source outputs превысили per-chunk3000chars; отдельные searches/cat были truncated и затем ключевые места дочитаны более узко. Это процедурное ограничение раскрыто. Aggregate reads/output/CPU/RSS отдельно не измерялись; измеренное соблюдение общего бюджета не заявляется. Полный patch дочитан по chunks; непрочитанные хвосты searches не используются как evidence.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| I1 соответствует partial refusal-only scope | Complete patch + actual source hashes + guards до mutation | Только source reasoning | сохранить |
| Staged entry больше не создаёт scratch перед strict отказом | scratch_execution early preflight + existing unconditional scientific preflight | Не исполненный mutation-count control | сохранить |
| Standalone signatures/order сохранены | Additive keyword diff и unchanged statements | Нет runtime/dispatch/compiler проверки | сохранить |
| Полный strict partial preservation/settlement/cleanup реализован | Отсутствует; explicitly NOT READY | Нельзя снимать early refusal | изменить |
| Native/scientific/campaign READY установлен | Свидетельств нет, R3/P1/P2/A1/C1 open | C08 exhausted; нового grant нет | данных недостаточно |

**STOP review-only. Qualified partial source verdict; полного R2 closure или execution approval нет.**
