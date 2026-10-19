# SCI05-N1 Runner — source candidate и STOP перед C08

2026-10-19. Этап: порученная реализация принятого SCI04-D2 и engineering attribute profile A. Статус: **SOURCE_CANDIDATE; runtime not_run; независимый R и CP-CODE остаются открыты**. Ни численная сходимость, ни physical/discretization/experimental acceptance не утверждаются.

## Identity и границы

Root фактически прочитан на `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`, `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`; root dirty coordination/gitlinks защищены. Runner actual исходник `9378396a3681c1eddf2c62f16674834fc4465583`, component status до работы чистый, recursive submodules отсутствуют. Изолированный Git worktree `/tmp/qcl-sci05-runner-worktree`, branch `codex/review-closure-final-audit-writer`, HEAD тот же; branch/worktree metadata creation потребовала разрешённой sandbox escalation после read-only filesystem error. Main Runner, root и original dirty checkout не редактировались. Stage/commit/push не выполнялись.

Read bindings: Core actual `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`; Contracts actual `12fc26462bbab3df76904c6deb01f8c6596de7be`. Selected root gitlinks не выдавались за actual owning revisions. Root recursive inventory был зафиксирован в tool output: Core7324, Runner937, AiiDAd8f8092, Contracts12fc264, Platformb067723, Portal2622de5, Research1eacefc, Resultse2fdeda.

Прочитаны root AGENTS/architecture и P1 science SCI04/SCI05/C08, Runner CONTRIBUTING; Runner-local AGENTS отсутствует. `using-superpowers` явно исключает dispatched subagents; `executing-plans` и `verification-before-completion` прочитаны как границы этапа. Runtime запрет прямого поручения имеет приоритет над skill RED→GREEN workflow: tests authored, **не выполнены и не объявлены passing**. QCL physics-audit прочитан для границы formula/acceptance ownership; новый физический аудит/эксперимент не проводился. Дочерних агентов нет.

Нормативные входы: D2 `/tmp/qcl-sci04-design-v2.md` SHA256 `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c`, review `ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1`; profile A `/tmp/qcl-sci05-attribute-encoding-design.md` SHA256 `1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206`, review `95518b6b9150b27ec490f2e30e5015511b300769fc3ed9443010591c1a010916`. Координатор отдельно подтвердил private transport guard без второго schema engine и Python invocation.

## Изменения и source trace

1. `physics_diagnostics.jl::_bound_final_audit/_final_audit_record`: Core internal template читается без identity; шесть actual fields execution_id,point_id,state_id,attempt,state_sequence,plan_fingerprint связываются ровно один раз после existing generation identity в `commit_point_artifacts`. Все шесть обязательны, attempt/seq positive integer non-bool, fingerprint lowercase64hex; никаких guessed context/default execution IDs. Наличие new production measurement context без template прекращает final publication. Legacy solution без обоих новых markers остаётся читаемым.
2. `point_artifacts.jl::commit_point_artifacts`: assessment формируется один раз; bound object переносится в nested commit key и оба native writers. Recovery удаляет nested key и не передаёт record writers, даже если supplied solution имеет template. Старые required args/dependencies и numeric arrays не изменены.
3. `physics_diagnostics.jl::_write_final_audit!`: единственный record_json fixed UTF8 scalar через pinned HDF5.jl instance-String dispatch; four exact literal constant attrs заданы до generic annotation, которая сохраняет existing attrs. Generic annotation не менялась. `hdf5.jl::_write_checkpoint` и optional analysis вызывают helper; no record→no new group.
4. `verify_point_artifacts` вызывает `_verify_final_audit_pair` для physics.full/analysis. Проверяются presence/final-versus-recovery, exact group child inventory, scalar fixed UTF8 type/width≤65536/no chunk/filter/external, four fixed scalar bounded constant attributes, exact six-field binding обеих копий и recursive semantic equality значений после readback. Owner SHA остаётся старым отдельным gate. Integer/bool types exact, floats exact Float64, object key order irrelevant, array order exact. Legacy absent+absent остаётся допустимым; одностороннее presence и stale recovery record отвергаются.
5. `_physical_certification_data`: stationary required list дополнен candidate Dyson/spectral/λ. Missing→not_evaluated, numeric nonfinite/error/tag→failed; supplied unavailable+finite0 не даёт passed. Существующие thresholds и nonlinear required gates сохранены, никакого Core recompute/equation evaluator не добавлено.
6. Existing `docs/src/user/results.md` native format section дополнен wire/legacy/recovery semantics и ownership link. `light_results.jl` не изменялся: existing shortest-roundtrip `_light_json` переиспользован после transport normalization signed zero→+0.

## Точный подход к validator и предел

Runner private guard — **не полная повторная реализация portable schema validator**. Он проверяет trusted Core producer template top-level inventory, schema/units, JSON-compatible values, finite numeric tokens, Measure status/value/nonfinite constraints, global mandatory status consistency, unavailable fresh statuses, UTF8/NUL/byte/depth/member budgets и actual identity. Readback использует уже существующий YAML JSON-compatible decoder для **собственного just-written JSON**, не вводит новый public arbitrary hostile JSON parser. Duplicate-key/hostile JSON/full nested schema/padding semantic policy остаются в independent published Contracts `final_audit.py` и Results consumer. Переносить их в Runner как новый schema engine координатор не потребовал и явно подтвердил этот подход. Новых scientific formulas/tolerances нет.

Scalar String producer dispatch подтверждён чтением pinned HDF5.jl0.17.4 `typeconversions.jl` datatype(instance), `dataspaces.jl`, `attributes.jl`. Это source evidence, не runtime observation. Runner attribute readback preflight проверяет fixed bounded atomic type/scalar/cset до собственного value read; независимый hostile padding reader относится к Results profile A.

## Неисполненная bounded test matrix

Новый distinct `test/infrastructure/final_fixed_point_audit.jl`, 217 строк на freeze:

- independent literal schema-shaped record без Core record-builder/продуктового encoder для expected values; measured0, UTF8 detail, tagged nonfinite/null, signed-zero normalization;
- все6binding fields, missing/invalid/mismatched attempt,seq,plan; wrong schema/units/status, unavailable finite0, numeric NaN, size/depth/members controls;
- stationary each candidate missing/nonfinite/error/unavailable controls;
- tiny existing native_physics_fixture energy9/Nk3/Nb2, no solve: actual commit+full/analysis writer, dtype/attrs/UTF8/readback equality и mutation raw value/identity/presence;
- recovery omits record despite supplied template, legacy absent final accepted, new production marker missing template rejected.

Эта fixture вызывает existing seed/embedding construction и persistence helpers в будущем разрешённом C08, но не SCBA/Poisson solve. Её literal raw measurements — manufactured format values, **не утверждение согласованности этих чисел с synthetic Green arrays**. Результат нельзя использовать как scientific evidence. Full schema independent validator в call8 должен проверить portable transport и оба record values.

## Fixture handoff для оставшихся call7/call8

При call7 координатор может задать ровно:

`QCL_SCI05_RUNNER_FIXTURE_ROOT=/tmp/qcl-sci05-runner-portable-fixture`

и запустить source-bound prepared Julia с `--startup-file=no --check-bounds=yes`, целевой test `test/infrastructure/final_fixed_point_audit.jl` из isolated Runner worktree. Runtime env/project должен связать Core7324 и этот Runner source **до запуска**, без instantiate/precompile/setup. Test требует несуществующий output path и не стирает старые данные. Без переменной все temporary outputs очищаются.

Точные **будущие**, ещё не созданные locators:

- `/tmp/qcl-sci05-runner-portable-fixture/archive/final/commit.json`
- соседние `physics.h5`, `analysis.h5`, `receipt.json` — actual Runner SHA-bound publication;
- `/tmp/qcl-sci05-runner-portable-fixture/fixture-source.txt` — literal source-base + synthetic/no-science label после успешного test body;
- рядом будут synthetic recovery `artifacts/generation-000001/*` и `legacy/archive/final/*` для negative/legacy consumers. Generation может отличаться только если добавлены существующие outputs, что test fresh-path guard не разрешает.

Call7 original log/receipt/source binding обязан сохранить координатор. Independent Results call8 читает actual producer canonical full/commit по этим locators, используя опубликованный Contracts helper и frozen Results code; сравнение hash alone не достаточно. Здесь не создан placeholder receipt и не подменён runtime pass. Никакие public fixtures/raw arrays в Git не добавлены.

## Выполненная проверка / STOP

Выполнены только чтение, bounded текстовые изменения, Git diff/source hashes. `git diff --check` exit0. Diff просмотрен по разрешённым paths; docs external link указывает на уже опубликованный exact Contracts commit, существование local path проверено чтением. Network check не выполнялся. `git diff --no-index /dev/null test/...` exit1 означает сохранённый новый-file diff, не test failure.

Не выполнялись Julia/Python/HDF imports, parser, tests, solver, build/install, network/server, stage/commit/push. C08 consumed здесь **0**, оставшийся aggregate cap не изменён. CP-CODE runtime и independent R не закрыты. Научная модель, arrays/layout/values, caps и допуски не менялись. **STOP: source frozen; не запускать автоматически и не повторять calls.**

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Actual identity переносится в один canonical record | source trace commit_point_artifacts→_bound_final_audit→writers/assessment | Runtime ещё не измерен | дополнительно измерить |
| Native/commit values проверяются до publication | _verify_final_audit_pair и mutation fixtures | Trusted producer guard не полный hostile schema engine | сохранить |
| Missing/error candidate summary не даёт false passed | required list + status/tag logic и literal controls | Tests not_run | дополнительно измерить |
| Legacy/recovery не получают fabricated final record | scoped absence branches и fixtures | Нет runtime evidence | дополнительно измерить |
| Full physics/discretization/model accuracy достигнуты | Нового scientific artifact нет | Manufactured persistence fixture не scientific oracle | данных недостаточно |
