# Независимый high source review SCI08-R2 D2

2026-10-20. Объект `/tmp/qcl-sci08-r2-design-v2.md`, SHA256 `664fce6abccd4517a2bb8e2bd87caefff77cfbc5ee6d5991afed66d731fceeae`, вместе с неизменённым v1 `69313bd117c140cf28b68d62ebb85b09bbc078a0ad305b3199c65ee55636e08c` и независимым D1 review `0b720a06e1b0386be753ae00814da4d0db5df5933fa1d000d14c97af523d76f9`.

**Вердикт: PASS_SOURCE для узкой design-поправки F1 и одного конечного owning Runner I ticket. Новых блокирующих design findings нет.** Это готовность написать и проверить source hooks в разрешённом этапе, а не доказанный production writer, native enforcement, runtime PASS либо campaign READY. Полнота transitive coverage ещё должна стать проверяемым deliverable I; неподключённая ветвь обязана strict-refuse до первой mutation.

Фактический selected Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `107bac5697b37cf0e47c3feb44883a907837645c`; Runner gitlink `4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`. HEAD/status/submodule status прочитаны; компоненты не отмечены dirty, root содержит прежние checkpoint/docs artifacts из author identity. Gitlinks остаются authority; JSON review — forensic record, не maintained lock.

## Почему F1 закрыт на design уровне

Непосредственно прочитаны четыре cleanup тела: `point_artifacts.jl:1100–1101,1323–1324`, `scratch_execution.jl:110–111`, `scientific_history.jl:222–223`. Все удаляют stage/temp в `finally`, поэтому outer permit не может сохранить partial payload после вложенного удаления. D2 §§1–3 требует заменить именно внутренние strict transitions, передавать identity/debt и сохранять standalone contract. Отдельный partial-write-then-denial fixture достигает проблемного cleanup, тогда как начальный refusal с zero mutations этого не делает.

Дополнительно подтверждены `progress.jl:597–609` с удаляющим temp catch и `_prune_recovery_generations!` в `point_artifacts.jl:751–783`: финальный цикл удаляет любую matching generation вне keep, включая не попавшую в verified список. D2 закрывает оба обхода: strict-aware atomic helper, guarded eligibility/defer вместо broad prune. Marker до create, non-auto-cleaning temp lifecycle и unknown-create retained debt закрывают ложный refund при частично успешном mutator. Scratch уже использует `cleanup=false` в `:56`; point/history/atomic temp constructors в прочитанных местах explicit `cleanup=false` не имеют. Их native defaults здесь не исполнялись и не предполагаются безопасными.

До rename partial остаётся на месте; после rename новый path остаётся `published_unacknowledged`, а disappearance старого имени не означает lifetime end. Strict success cleanup требует ownership + existing policy + independently verified durable replacement + matching identities + cleanup capability, затем actual unlink/barrier/lifetime evidence. Только после этого возможно уменьшение logical E в доказанной view; физический H нельзя увеличивать на filesize. High-water и cumulative I/O неизменны. При unknown/denied cleanup объект остаётся resident. Это разрешает F1 без удаления failed/raw/finals ради лимита.

## Точный I-ready объём и границы покрытия

Один Runner PR может включать v1 types/arithmetic/authority port и D2 writer hooks. Production backend по умолчанию отказывает. Следующие call edges должны присутствовать в source call/cleanup table и handwritten controls:

| Source edge на Runner4f60 | Требуемый конечный control / граница |
| --- | --- |
| `scientific_execution.jl:1090,1093` recovery callback; `:1264,1267` final; `:635` operator; history callbacks `scientific_history.jl:97,112`; finalizer `scientific_execution.jl:1485` | Strict dispatch без standalone fallback; guard до mutation; partial→deny сохраняет temp и debt; pre/post-rename outcomes; finalizer не получает новый normal grant и не маскирует primary failure. |
| Четыре cleanup bodies и `progress.jl:597–617` | Strict partial retained/delete0; paired standalone cleanup/signature control; pointer/index temp failure не повышает состояние в acknowledged. История: counters до index не считаются durability proof, retry требует reconcile. |
| `_prune_recovery_generations!` | Protected current/previous/failed/final/unacknowledged/invalid receipt не удаляются; success cleanup — отдельная eligibility цепочка и actual unlink; deferred cleanup сохраняет E и может отказать следующему one-byte-short reservation. |
| `execute_scientific_plan_staged` → `stage_result_tree` `scratch_execution.jl:155`, затем `rm(workspace)` `:156` | Последующий success cleanup всего workspace также требует отдельной eligibility/authority. Verified destination result не доказывает, что весь workspace покрыт replacement. Нельзя считать guard только внутри stage_result_tree достаточным. |

Последняя строка уточняет конкретный обязательный I call edge, а не требует нового D: D2 §3.2 уже обязывает проверить wrapping/transitive cleanup и strict-refuse непокрытые branches. Прочитанный `:156` находится после успешного staging; не удаляет данные при exception из staging, но без guarded eligibility может нарушить success cleanup contract.

Ещё три точных transitive места найдены и прочитаны в `scientific_execution.jl`: import temp `:410–423` (`finally rm`), post-checkpoint `imported-*` deletion `:1116–1117`, optical temp `:1335–1347` (`finally rm`). V1 §2 уже относит imports/optical к permit-or-refuse scope; D2 §3.2 распространяет cleanup правило на них. Полный writer-enabled coverage claim не допускается, пока I не подключит эти transitions либо не покажет strict refusal до входа в их mutating branches. Особенно success imported deletion не получает право на удаление от одного факта появления нового checkpoint. Никакой отдельный generic redesign или C1/P1 implementation для этого не требуется.

Готовые fixture definitions D2 достаточны как начало I: literal E=100/duplicate40/E=60; denied/unknown unlink без уменьшения E; ordered publication с deferred cleanup; distinct pre/post-rename; nested atomic failure; standalone compatibility. К coverage table необходимо привязать перечисленные дополнительные caller edges и подтвердить отказ/сохранение для каждой reachable ветви. Эти fixtures здесь не писались и не исполнялись.

## Сохраняемые ограничения

V1 §§4–6 сохраняет `E+U+P+S≤A` и независимое `U+P+S≤H` в совместимой physical view; E не debit второй раз к already-remaining H. Unknown capacity/native growth/authority не означает 0/pass. 2 TiB shared resident и attempt 128/256 GiB — caps, не измеренная capacity. Forecaster не становится HDF5 upper bound. Source refusal-only реализация при missing bound остаётся допустимым результатом.

Полученный frozen S1 context не меняется: no ee; LO/acoustic/impurity/IFR/alloy, 0 mV/period, 70 K. Physics/model/mesh/basis/tolerances/full_final не меняются. Здесь модель и numerical acceptance независимо не аудировались. R1 «349 PASS» — историческое квалифицированное evidence, не результат этого review. R3/P1/P2/A1/C1 остаются open. C08 SCI05/SCI08 **8/8 EXHAUSTED**; review не сбрасывает счётчики и не выдаёт новый grant.

Использован qcl-performance-audit как source audit хранения; physics audit не требовался: формулы транспорта/solver не рассматривались. Прочитаны AGENTS/architecture и перечисленные source ranges. Component AGENTS отсутствует; `rg --files -g AGENTS.md` в Runner не дал дополнительных файлов. Полный callgraph и native temp/unlink semantics не доказаны. D1 читался выбранными §§1–6/8 и controls locators, не весь документ; в длинных чтениях skill/D1 были truncations, непрочитанный хвост не используется как evidence. Hashing полного файла не означает полный semantic read. CPU/RAM и aggregate tool-output bytes независимо не измерены, соблюдение измеренного лимита не заявляется.

Только чтение/hash/read-only Git и два review outputs в `/tmp`. Не выполнялись scripts/parsers/imports/compiler/tests/runtime/native/server/network/solver/CI. Нет implementation, source/index/CP/READY mutations, детей нет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 закрыт обязательным внутренним strict cleanup contract | D2 §§1–3; четыре непосредственно прочитанных finally + progress catch | Design/source reasoning, fault fixture не выполнен | сохранить |
| Один finite Runner I готов | V1 §§1–6/8 + D2 §3; точные callers/controls выше | Все непокрытые branches strict-refuse; не production writer pass | изменить |
| Transitive import/optical/workspace cleanup автоматически покрыт outer wrapper | Runner4f60 scratch:156; scientific_execution:423,1117,1347 | Нужен I trace/guard-or-refuse, whole-callgraph не доказан | изменить |
| Допустимость E release после success cleanup определена | D2 §2 eligibility + actual unlink + lifetime barriers | Native facts неизвестны, physical H без fresh proof не растёт | сохранить |
| Campaign/native/scientific readiness доказана | Evidence отсутствует; открытые R3/P1/P2/A1/C1, C08 exhausted | Source review не закрывает gates | данных недостаточно |

**STOP: review only. Передать один qualified source-I ticket с указанными binding call edges; никакого исполнения или READY из этого вердикта.**
