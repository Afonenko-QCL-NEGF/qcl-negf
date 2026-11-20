# Core #32: независимый API/architecture review

**Решение:** разделение aligned-state readiness и forced full audit оправдано, но существующее checkpoint-поведение нужно сохранить по умолчанию. Рекомендую одну явную opt-in extension существующего request hook, без нового scheduler/observer framework. Это design review, не implementation acceptance или разрешение менять active Core.

Источник: чистый Core `e171caa60cce676c6c4238dd671e7c527f2bd977`/tree742ed5a6 через read-only symlink; relevant solver/markers/types побайтно не менялись в принятом db26. Runner53b source прочитан из прежнего read-only archive. Новый cwd — directory, не Git repository. Прочитан [issue32](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/issues/32). Reviewer не запускал Julia/Pkg/HDF5/numerical work и не менял reviewed source.

## Что уже является обещанием

`production_solver.jl:721–761` вычисляет checkpoint request, затем передаёт `terminal=decision.terminal || checkpoint_due` markers helper и вызывает callback **до mixing**. `physics_markers.jl:407–432` делает audit first ν1/cadence/forced terminal, не повторяет уже прикреплённый marker. Связь защищена прямым тестом `test/numerics/scba_physical_markers.jl:178–214`: каждый checkpoint обязан иметь current-row markers. Поэтому удалить `|| checkpoint_due` молча — наблюдаемая API regression, а не только устранение accidental expense.

`ProductionOptions` обещает checkpoint cadence, counter-only request, synchronous borrowed callback (`production_contracts.jl:69–108,418–435`; `production_solver.jl:8–16`). Explicit request владеет cadence, переопределяя числовой interval; return принимается через `===true`. History observer вызывается на каждой завершённой карте после optional markers, перед callback. Callback не означает convergence: aligned SCBAResult имеет running/false. Copy(history) копирует vector, **не** full Green/families. Arrays borrowed; synchronous serialize допустим, async retention требует owned copy. При consume_initial=true владение private restart передаётся solver; внешние aliases опасны.

Marker policy прямо названа observational и не меняющей acceptance (`types.jl:829–852`, `physics_markers.jl:1–2`). Raw convergence/diagnostic assessment и decision уже выполнены до marker phase (`production_solver.jl:689–713`). First/known terminal audits необходимо сохранить независимо от callback frequency; off-cadence отсутствие marker — not_measured, не pass и не zero.

## Реальные consumers и лишняя цена

Runner `configured_run.jl:880–894` и `scientific_execution.jl:934–952` возвращает bool по cadence/deadline/pause, сохраняет checkpoint синхронно; `analysis=false` **не** отменяет уже выполненные Core markers. `solve_production` дополнительно интегрирует checkpoint density и собирает NEGFSolution (`production_solver.jl:1008–1048`): это отдельная цена promised persisted state, не автоматически ненужная работа.

Schema уже допускает **sparse** markers: Runner `physical_markers_and_packed_history.jl:74–105` сохраняет available=[1,0,1]/NaN для missing row; missing typed TABLE при этом остаётся corruption. Поэтому state-only checkpoint технически возможен без новой HDF schema, но latest-row-unmeasured ещё надо проверить реальным roundtrip/restart. Нельзя удалять таблицу или переносить старый marker на новый ν. Existing boolean Runner routes должны сохранить прежнюю семантику без конфиг-миграции.

Полный audit включает raw Keldysh block reconstruction/normalization/FDT, linewidth sampling, boundary exposures и дополнительные обходы (`physics_markers.jl:249–395`). `_fresh_map_markers:185–218` считает3component norms по mixed/fresh families и **10** отдельных mixed/fresh collision integrals для5channels. Harness embedding+/− balances — ещё иные integrals. Эти состояния/семейства различны: просто суммировать или переиспользовать один ответ вместо всех нельзя. При последующей fusion reusable result должен иметь ровно тот же G, mixed/fresh identity, family, wE·wk, spin/(2π), definition и normalization; агрегированный rΣ не заменяет channel marker. Cross-iteration cache здесь особенно опасен. В выбранный первый API change fusion/редукции не включать.

Snapshot ν2…20 (19 zero-branch iterations), `phase-partial-2-20-withalloc.json`: residuals3.33035wall/82.0076CPU≈**24.6CPU**; physics_markers .37844wall/.39531CPU, allocated≈513.26MB. Последнее — накопленные allocations, не peak/RSS/full-array-copy proof. Это sample текущей cadence, не all-checkpoints A/B. Снять coupling не значит ускорить весь residual phase; end-to-end gain пока **not_measured**.

## Один минимальный design

Расширить только return contract `checkpoint_request(context)` новым **`:state_only`**; никаких новых production policy structs/queues/config registries:

| Request | Aligned callback | Forced audit сверх ordinary marker policy |
|---|---|---|
| false / прежний no-request result | нет | нет |
| true / default numerical checkpoint cadence | да | **да, legacy semantics** |
| :state_only, explicit opt-in | да | нет; first/cadence/known terminal остаются |

Разрешать request **один раз** на boundary и декодировать в private `(state_due, force_audit)`, сохраняя short-circuit при absent sink. Не вызывать closure второй раз ради audit: deadline/pause/request hooks могут иметь state/side effects. Callback payload/argument order/lifetime и history observer ordering не менять. `_production_checkpoint_requested` используется также outer path (`production_solver.jl:1164`): обработать extension последовательно, не сломав bool consumers. Численные algorithms/restart-contract и native gates не меняются; custom harness должен зафиксировать новую telemetry policy в provenance.

Для planned softstop/pause request возвращает **true** на той границе, где нужен full final audit; остальные per-map observations могут быть :state_only. Неожиданный callback throw нельзя объявить Core terminal audit: solver ещё не знает, что client остановится. Если caller требует гарантированный full audit на таком throw, он должен использовать legacy true route. Из существующих Runner bool callers ничего автоматически не переводить в state-only. Первая версия — Core opt-in+docs/tests; изменение Runner/harness отдельно и только при явно выбранной policy.

## Достаточные адресные проверки перед приёмкой implementation

1. Сохранить существующий checkpoint/cadence test неизменным. На tiny max5/cadence3 со state-only every map проверить callbacks1…5, markers1/3/5; явный true на2 добавляет marker2. Existing false override и exactly-one hook invocation проверить отдельно, включая absent sink.
2. На одном fixed tiny input сравнить no-request/legacy/state-only: те же map counts, final fields/raw rD/rA/rK/rΣ/rλ/PSD/causality witnesses и strict decisions; markers на общих measured rows равны. Не заменять raw критерии mixed step или masked not_measured.
3. Known terminal/domain-stop markers сохраняются. Planned softstop true даёт current-ν marker до callback throw и aligned saved arrays; state-only/unexpected throw не получает ложную terminal/full-audit guarantee.
4. Runner checkpoint с latest physical_markers=nothing: typed available0/NaN roundtrip, exact counters/mixer/source identity, remaining-budget restart и следующий map против uninterrupted oracle. Existing corruption rejection, ownership/consume_initial и resource-pause lifecycle tests сохранить. Serialization — внутри callback; full fields не копировать для каждого history event и не удерживать borrowed snapshots async.
5. Затем один matched performance control на frozen fields с одинаковыми workers/maps/cadence и единственным intent delta; wall/CPU/allocations/GC/peak, marker invocation counts и отсутствие дополнительного Φ. Timing assertions не делать нормативным correctness gate. Общую экономию измерить, не выводить из operator/sample ratio.

**Риски:** default compatibility, неожиданная потеря audit на client-driven stop, ложная freshness sparse markers, двойной request, retained borrowed arrays, смешение persistence с scientific acceptance. Предложенная opt-in extension адресует первую связку с минимальной областью изменения; eligibility/fusion/residual arithmetic остаются отдельными независимыми задачами.
